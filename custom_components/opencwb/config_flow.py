"""Config flow for OpenCWB."""
from .core.ocwb import OCWB
from .core.commons.exceptions import APIRequestError, UnauthorizedError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_API_KEY,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_MODE,
    CONF_NAME,
)
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_LANGUAGE,
    CONF_LOCATION_NAME,
    CONFIG_FLOW_VERSION,
    DEFAULT_FORECAST_MODE,
    DEFAULT_LANGUAGE,
    DEFAULT_NAME,
    DOMAIN,
    FORECAST_MODES,
    LANGUAGES,
)


class OpenCWBConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for OpenCWB."""

    VERSION = CONFIG_FLOW_VERSION
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OpenCWBOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            latitude = user_input.get(CONF_LATITUDE, self.hass.config.latitude)
            longitude = user_input.get(CONF_LONGITUDE, self.hass.config.longitude)
            location_name = user_input.get(CONF_LOCATION_NAME, None)
            if (location_name and
                    _is_supported_city(user_input[CONF_API_KEY], location_name) is None):
                errors["base"] = "invalid_location_name"
            else:
                await self.async_set_unique_id(f"{latitude}-{longitude}")
                self._abort_if_unique_id_configured()

                try:
                    api_online = await _is_ocwb_api_online(
                        self.hass, user_input[CONF_API_KEY], latitude, longitude, location_name
                    )
                    if not api_online:
                        errors["base"] = "invalid_api_key"
                except UnauthorizedError:
                    errors["base"] = "invalid_api_key"
                except APIRequestError:
                    errors["base"] = "cannot_connect"

                if not errors:
                    return self.async_create_entry(
                        title=user_input[CONF_NAME], data=user_input
                    )

        schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_LOCATION_NAME): str,
#                vol.Optional(
#                    CONF_LATITUDE, default=self.hass.config.latitude
#                ): cv.latitude,
#                vol.Optional(
#                    CONF_LONGITUDE, default=self.hass.config.longitude
#                ): cv.longitude,
#                vol.Optional(CONF_MODE, default=DEFAULT_FORECAST_MODE): vol.In(
#                    FORECAST_MODES
#                ),
#                vol.Optional(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): vol.In(
#                    LANGUAGES
#                ),
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)


class OpenCWBOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self._get_options_schema(),
        )

    def _get_options_schema(self):
        return vol.Schema(
            {
                vol.Optional(
                    CONF_MODE,
                    default=self.config_entry.options.get(
                        CONF_MODE, DEFAULT_FORECAST_MODE
                    ),
                ): vol.In(FORECAST_MODES),
#                vol.Optional(
#                    CONF_LANGUAGE,
#                    default=self.config_entry.options.get(
#                        CONF_LANGUAGE, DEFAULT_LANGUAGE
#                    ),
#                ): vol.In(LANGUAGES),
            }
        )


async def _is_ocwb_api_online(hass, api_key, lat, lon, loc):
    ocwb = OCWB(api_key).weather_manager()
    return await hass.async_add_executor_job(ocwb.one_call, lat, lon, loc)

def _is_supported_city(api_key, loc):
    ocwb = OCWB(api_key).weather_manager()
    return ocwb.supported_city(loc)
