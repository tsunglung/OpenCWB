"""Support for the OpenCWB (OCWB) service."""
from .abstract_ocwb_sensor import AbstractOpenCWBSensor
from .const import (
    ATTR_API_FORECAST,
    CONF_LOCATION_NAME,
    DOMAIN,
    ENTRY_NAME,
    ENTRY_WEATHER_COORDINATOR,
    FORECAST_MONITORED_CONDITIONS,
    FORECAST_SENSOR_TYPES,
    MONITORED_CONDITIONS,
    WEATHER_SENSOR_TYPES,
)
from .weather_update_coordinator import WeatherUpdateCoordinator


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up OpenCWB sensor entities based on a config entry."""
    domain_data = hass.data[DOMAIN][config_entry.entry_id]
    name = domain_data[ENTRY_NAME]
    weather_coordinator = domain_data[ENTRY_WEATHER_COORDINATOR]
    location_name = domain_data[CONF_LOCATION_NAME]

    weather_sensor_types = WEATHER_SENSOR_TYPES
    forecast_sensor_types = FORECAST_SENSOR_TYPES

    entities = []
    for sensor_type in MONITORED_CONDITIONS:
        unique_id = f"{config_entry.unique_id}-{sensor_type}-{location_name}"
        entities.append(
            OpenCWBSensor(
                f"{name} {location_name} {sensor_type}",
                unique_id,
                sensor_type,
                weather_sensor_types[sensor_type],
                weather_coordinator,
            )
        )

    for sensor_type in FORECAST_MONITORED_CONDITIONS:
        unique_id = f"{config_entry.unique_id}-forecast-{sensor_type}-{location_name}"
        entities.append(
            OpenCWBForecastSensor(
                f"{name} {location_name} Forecast {sensor_type}",
                unique_id,
                sensor_type,
                forecast_sensor_types[sensor_type],
                weather_coordinator,
            )
        )

    async_add_entities(entities)


class OpenCWBSensor(AbstractOpenCWBSensor):
    """Implementation of an OpenCWB sensor."""

    def __init__(
        self,
        name,
        unique_id,
        sensor_type,
        sensor_configuration,
        weather_coordinator: WeatherUpdateCoordinator,
    ):
        """Initialize the sensor."""
        super().__init__(
            name,
            unique_id,
            sensor_type,
            sensor_configuration,
            weather_coordinator
        )
        self._weather_coordinator = weather_coordinator
        self._attr_name = name.replace("_", " ")
        self._attr_unique_id = unique_id


    @property
    def state(self):
        """Return the state of the device."""
        return self._weather_coordinator.data.get(self._sensor_type, None)


class OpenCWBForecastSensor(AbstractOpenCWBSensor):
    """Implementation of an OpenCWB this day forecast sensor."""

    def __init__(
        self,
        name,
        unique_id,
        sensor_type,
        sensor_configuration,
        weather_coordinator: WeatherUpdateCoordinator,
    ):
        """Initialize the sensor."""
        super().__init__(
            name,
            unique_id,
            sensor_type,
            sensor_configuration,
            weather_coordinator
        )
        self._weather_coordinator = weather_coordinator
        self._attr_name = name.replace("_", " ")
        self._attr_unique_id = unique_id

    @property
    def state(self):
        """Return the state of the device."""
        forecasts = self._weather_coordinator.data.get(ATTR_API_FORECAST)
        if forecasts is not None and len(forecasts) > 0:
            return forecasts[0].get(self._sensor_type, None)
        return None
