"""Support for the OpenCWB (OCWB) service."""
from homeassistant.components.weather import WeatherEntity
from homeassistant.const import PRESSURE_HPA, PRESSURE_INHG, TEMP_CELSIUS
from homeassistant.util.unit_conversion import PressureConverter
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    ATTR_API_CONDITION,
    ATTR_API_FORECAST,
    ATTR_API_HUMIDITY,
    ATTR_API_PRESSURE,
    ATTR_API_TEMPERATURE,
    ATTR_API_WIND_BEARING,
    ATTR_API_WIND_SPEED,
    ATTRIBUTION,
    DEFAULT_NAME,
    DOMAIN,
    ENTRY_NAME,
    ENTRY_WEATHER_COORDINATOR,
    MANUFACTURER,
)
from .weather_update_coordinator import WeatherUpdateCoordinator


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up OpenCWB weather entity based on a config entry."""
    domain_data = hass.data[DOMAIN][config_entry.entry_id]
    name = domain_data[ENTRY_NAME]
    weather_coordinator = domain_data[ENTRY_WEATHER_COORDINATOR]

    unique_id = f"{config_entry.unique_id}"
    ocwb_weather = OpenCWBWeather(name, unique_id, weather_coordinator)

    async_add_entities([ocwb_weather], False)


class OpenCWBWeather(WeatherEntity):
    """Implementation of an OpenCWB sensor."""

    def __init__(
        self,
        name,
        unique_id,
        weather_coordinator: WeatherUpdateCoordinator,
    ):
        """Initialize the sensor."""
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._weather_coordinator = weather_coordinator
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, unique_id)},
            manufacturer=MANUFACTURER,
            name=DEFAULT_NAME,
        )

    @property
    def should_poll(self):
        """Return the polling requirement of the entity."""
        return False

    @property
    def attribution(self):
        """Return the attribution."""
        return ATTRIBUTION

    @property
    def condition(self):
        """Return the current condition."""
        return self._weather_coordinator.data[ATTR_API_CONDITION]

    @property
    def available(self):
        """Return True if entity is available."""
        return self._weather_coordinator.last_update_success

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self._weather_coordinator.async_add_listener(
                self.async_write_ha_state)
        )

    async def async_update(self):
        """Get the latest data from OCWB and updates the states."""
        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_wind_speed_unit = self.anws_aoaws_now.wind_speed.units

        self._attr_forecast = self._weather_coordinator.data[ATTR_API_FORECAST]
        self._attr_temperature = self._weather_coordinator.data[ATTR_API_TEMPERATURE]
        pressure = self._weather_coordinator.data[ATTR_API_PRESSURE]

        # OpenWeatherMap returns pressure in hPA, so convert to
        # inHg if we aren't using metric.
        if not self.hass.config.units.is_metric and pressure:
            self._attr_pressure = PressureConverter.convert(pressure, PRESSURE_HPA, PRESSURE_INHG)
        self._attr_pressure = pressure

        wind_speed = self._weather_coordinator.data[ATTR_API_WIND_SPEED]
        if self.hass.config.units.name == "imperial":
            self._attr_wind_speed = round(wind_speed * 2.24, 2)
        self._attr_wind_speed = round(wind_speed * 3.6, 2)
        self._attr_humidity = self._weather_coordinator.data[ATTR_API_HUMIDITY]
        self._attr_wind_bearing = self._weather_coordinator.data[ATTR_API_WIND_BEARING]

        await self._weather_coordinator.async_request_refresh()
