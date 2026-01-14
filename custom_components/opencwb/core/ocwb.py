#!/usr/bin/env python
# -*- coding: utf-8 -*-

from httpx import AsyncClient

from . import constants
from .utils import strings
from .utils import config as cfg
from .commons import cityidregistry
from .weatherapi12 import weather_manager


class OCWB:

    """
    Entry point class providing ad-hoc API clients for each OCWB web API.

    :param api_key: the OCWB API key
    :type api_key: str
    :param config: the configuration dictionary (if not provided, a default one will be used)
    :type config: dict
    """
    def __init__(self, api_key, config=None):
        assert api_key is not None, 'API Key must be set'
        self.api_key = api_key
        if config is None:
            self.config = cfg.get_default_config()
        else:
            assert isinstance(config, dict)
            self.config = config

    @property
    def configuration(self):
        """
        Returns the configuration dict for the OCWB

        :returns: `dict`

        """
        return self.config

    @property
    def version(self):
        """
        Returns the current version of the OCWB library

        :returns: `tuple`

        """
        return constants.OCWB_VERSION

    @property
    def supported_languages(self):
        """
        Returns the languages that the OCWB API supports

        :return: `list` of `str`

        """
        return constants.LANGUAGES


    def weather_manager(self, client: AsyncClient | None = None):
        """
        Gives a `pyocwb.weatherapi25.weather_manager.WeatherManager` instance that can be used to fetch air
        pollution data.
        :return: a `pyocwb.weatherapi25.weather_manager.WeatherManager` instance
        """
        if client is not None:
            return weather_manager.AsyncWeatherManager(client, self.api_key, self.config)
            
        return weather_manager.WeatherManager(self.api_key, self.config)


    def __repr__(self):
        return "<%s.%s - API key=%s, subscription type=%s, OCWB version=%s>" % \
                    (__name__,
                     self.__class__.__name__,
                     strings.obfuscate_API_key(self.api_key) if self.api_key is not None else 'None',
                     self.config['subscription_type'].name, self.version)
