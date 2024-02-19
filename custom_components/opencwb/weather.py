"""Support for the OpenCWB (OCWB) service."""
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.weather import Forecast, WeatherEntityFeature, SingleCoordinatorWeatherEntity
from homeassistant.const import UnitOfPressure, UnitOfTemperature
from homeassistant.util.unit_conversion import PressureConverter
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

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
    FORECAST_MODE_DAILY,
    FORECAST_MODE_ONECALL_DAILY,
    MANUFACTURER,
)
from .weather_update_coordinator import WeatherUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up OpenCWB weather entity based on a config entry."""
    domain_data = hass.data[DOMAIN][config_entry.entry_id]
    name = domain_data[ENTRY_NAME]
    weather_coordinator = domain_data[ENTRY_WEATHER_COORDINATOR]

    unique_id = f"{config_entry.unique_id}"
    ocwb_weather = OpenCWBWeather(name, unique_id, weather_coordinator)

    async_add_entities([ocwb_weather], False)


class OpenCWBWeather(SingleCoordinatorWeatherEntity[WeatherUpdateCoordinator]):
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
        if weather_coordinator.forecast_mode in (
            FORECAST_MODE_DAILY,
            FORECAST_MODE_ONECALL_DAILY,
        ):
            self._attr_supported_features = WeatherEntityFeature.FORECAST_DAILY
        else:  # FORECAST_MODE_DAILY or FORECAST_MODE_ONECALL_HOURLY
            self._attr_supported_features = WeatherEntityFeature.FORECAST_HOURLY

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

    @property
    def forecast(self) -> list[Forecast] | None:
        """Return the forecast array."""
        return self._weather_coordinator.data[ATTR_API_FORECAST]

    @callback
    def _async_forecast_daily(self) -> list[Forecast] | None:
        """Return the daily forecast in native units."""
        return self.forecast

    @callback
    def _async_forecast_hourly(self) -> list[Forecast] | None:
        """Return the hourly forecast in native units."""
        return self.forecast

    async def async_update(self):
        """Get the latest data from OCWB and updates the states."""
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_wind_speed_unit = self.anws_aoaws_now.wind_speed.units

        self._attr_temperature = self._weather_coordinator.data[ATTR_API_TEMPERATURE]
        pressure = self._weather_coordinator.data[ATTR_API_PRESSURE]

        # OpenWeatherMap returns pressure in hPA, so convert to
        # inHg if we aren't using metric.
        if not self.hass.config.units.is_metric and pressure:
            self._attr_pressure = PressureConverter(pressure, UnitOfPressure.HPA, UnitOfPressure.INHG)
        self._attr_pressure = pressure

        wind_speed = self._weather_coordinator.data[ATTR_API_WIND_SPEED]
        if self.hass.config.units.name == "imperial":
            self._attr_wind_speed = round(wind_speed * 2.24, 2)
        self._attr_wind_speed = round(wind_speed * 3.6, 2)
        self._attr_humidity = self._weather_coordinator.data[ATTR_API_HUMIDITY]
        self._attr_wind_bearing = self._weather_coordinator.data[ATTR_API_WIND_BEARING]

        await self._weather_coordinator.async_request_refresh()
