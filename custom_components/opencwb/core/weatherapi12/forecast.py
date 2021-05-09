#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from ..commons import  exceptions
from ..utils import timestamps, formatting
from . import location
from . import weather
from ..utils.opendata_cwb import OpendataCWB


class Forecast:
    """
    A class encapsulating weather forecast data for a certain location and
    relative to a specific time interval (forecast for every three hours or
    for every day)

    :param interval: the time granularity of the forecast. May be: *'3h'* for
        three hours forecast or *'daily'* for daily ones
    :type interval: str
    :param reception_time: GMT UNIXtime of the forecast reception from the OCWB
        web API
    :type reception_time: int
    :param location: the *Location* object relative to the forecast
    :type location: Location
    :param weathers: the list of *Weather* objects composing the forecast
    :type weathers: list
    :returns:  a *Forecast* instance
    :raises: *ValueError* when negative values are provided

    """

    def __init__(self, interval, reception_time, location, weathers):
        self.interval = interval
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self.rec_time = reception_time
        self.location = location
        self.weathers = weathers

    def get(self, index):
        """
        Lookups up into the *Weather* items list for the item at the specified
        index

        :param index: the index of the *Weather* object in the list
        :type index: int
        :returns: a *Weather* object
        """
        return self.weathers[index]

    def reception_time(self, timeformat='unix'):
        """Returns the GMT time telling when the forecast was received
            from the OCWB Weather API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError

        """
        return formatting.timeformat(self.rec_time, timeformat)

    def actualize(self):
        """
        Removes from this forecast all the *Weather* objects having a reference
        timestamp in the past with respect to the current timestamp
        """
        current_time = timestamps.now(timeformat='unix')
        actualized_weathers = filter(lambda x: x.reference_time(timeformat='unix') >= current_time, self.weathers)
        self.weathers = list(actualized_weathers)

    @classmethod
    def from_dict(cls, the_dict):
        """
        Parses a *Forecast* instance out of a raw data dictionary. Only certain properties of the data are used: if
        these properties are not found or cannot be parsed, an error is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a *Forecast* instance or ``None`` if no data is available
        :raises: *ParseAPIResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the input dictionary embeds an HTTP status error

        """
        if the_dict is None:
            raise exceptions.ParseAPIResponseError('JSON data is None')
        if 'success' in the_dict:
            if not the_dict['success']:
                return None
            try:
                the_dict = OpendataCWB.to_dict(the_dict)
            except ValueError:
                raise exceptions.ParseAPIResponseError(
                    f"{__name__}: impossible to read weather info from input data")
        try:
            place = location.Location.from_dict(the_dict)
        except KeyError:
            raise exceptions.ParseAPIResponseError(''.join([__name__,
                                                               ': impossible to read location info from JSON data']))
        # Handle the case when no results are found
        if 'count' in the_dict and the_dict['count'] == "0":
            weathers = []
        elif 'cnt' in the_dict and the_dict['cnt'] == 0:
            weathers = []
        else:
            forecast_mode = "daily" if "daily" in the_dict else "hourly"
            if len(the_dict[forecast_mode]) >= 1:
                try:
                    weathers = [weather.Weather.from_dict(item) \
                                for item in the_dict[forecast_mode]]
                except KeyError:
                    raise exceptions.ParseAPIResponseError(
                          ''.join([__name__, ': impossible to read weather info from JSON data'])
                                  )
            else:
                raise exceptions.ParseAPIResponseError(
                          ''.join([__name__, ': impossible to read weather list from JSON data'])
                          )
        current_time = int(time.time())
        return Forecast(None, current_time, place, weathers)

    def to_dict(self):
        """Dumps object to a dictionary

        :returns: a `dict`

        """
        return {"interval": self.interval,
               "reception_time": self.rec_time,
               "location": self.location.to_dict(),
               "weathers": [w.to_dict() for w in self]}

    def __len__(self):
        return len(self.weathers)

    def __iter__(self):
        return iter(self.weathers)

    def __repr__(self):
        return "<%s.%s - reception_time=%s, interval=%s>" % (__name__, \
              self.__class__.__name__, self.reception_time('iso'),
              self.interval)