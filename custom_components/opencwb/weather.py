"""Support for the OpenCWB (OCWB) service."""
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.weather import Forecast, WeatherEntityFeature, SingleCoordinatorWeatherEntity
from homeassistant.const import UnitOfPressure, UnitOfTemperature
from homeassistant.util.unit_conversion import PressureConverter
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import (
    UnitOfSpeed
)

from .const import (
    ATTR_API_CLOUDS,
    ATTR_API_CONDITION,
    ATTR_API_DEW_POINT,
    ATTR_API_FEELS_LIKE_TEMPERATURE,
    ATTR_API_FORECAST,
    ATTR_API_HUMIDITY,
    ATTR_API_PRESSURE,
    ATTR_API_TEMPERATURE,
    ATTR_API_WIND_BEARING,
    ATTR_API_WIND_GUST,
    ATTR_API_WIND_SPEED,
    ATTRIBUTION,
    CONF_LOCATION_NAME,
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
    location_name = domain_data[CONF_LOCATION_NAME]

    unique_id = f"{config_entry.unique_id}"
    ocwb_weather = OpenCWBWeather(f"{name} {location_name}", f"{unique_id}-{location_name}", weather_coordinator)

    async_add_entities([ocwb_weather], False)


class OpenCWBWeather(SingleCoordinatorWeatherEntity[WeatherUpdateCoordinator]):
    """Implementation of an OpenCWB sensor."""
    _attr_attribution = ATTRIBUTION
    _attr_native_wind_speed_unit = UnitOfSpeed.METERS_PER_SECOND

    def __init__(
        self,
        name,
        unique_id,
        weather_coordinator: WeatherUpdateCoordinator,
    ):
        """Initialize the sensor."""
        super().__init__(weather_coordinator)
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._weather_coordinator = weather_coordinator
        split_unique_id = unique_id.split("-")
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, f"{split_unique_id[0]}-{split_unique_id[1]}")},
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
    def cloud_coverage(self) -> float | None:
        """Return the Cloud coverage in %."""
        return self._weather_coordinator.data[ATTR_API_CLOUDS]

    @property
    def native_apparent_temperature(self) -> float | None:
        """Return the apparent temperature."""
        return self._weather_coordinator.data[ATTR_API_FEELS_LIKE_TEMPERATURE]

    @property
    def native_temperature(self) -> float | None:
        """Return the temperature."""
        return self._weather_coordinator.data[ATTR_API_TEMPERATURE]

    @property
    def native_pressure(self) -> float | None:
        """Return the pressure."""
        return self._weather_coordinator.data[ATTR_API_PRESSURE]

    @property
    def humidity(self) -> float | None:
        """Return the humidity."""
        return self._weather_coordinator.data[ATTR_API_HUMIDITY]

    @property
    def native_dew_point(self) -> float | None:
        """Return the dew point."""
        return self._weather_coordinator.data[ATTR_API_DEW_POINT]

    @property
    def native_wind_gust_speed(self) -> float | None:
        """Return the wind gust speed."""
        return self._weather_coordinator.data[ATTR_API_WIND_GUST]

    @property
    def native_wind_speed(self) -> float | None:
        """Return the wind speed."""
        return self._weather_coordinator.data[ATTR_API_WIND_SPEED]

    @property
    def wind_bearing(self) -> float | str | None:
        """Return the wind bearing."""
        return self._weather_coordinator.data[ATTR_API_WIND_BEARING]

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
