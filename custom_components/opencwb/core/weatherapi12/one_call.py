from typing import Union, Optional

from ..commons import exceptions
from ..utils import geo
from .weather import Weather
from ..utils.opendata_cwb import OpendataCWB

class OneCall:

    def __init__(self,
                 lat: Union[int, float],
                 lon: Union[int, float],
                 timezone: str,
                 current: Weather,
                 forecast_minutely:Optional[Weather] = None,
                 forecast_hourly:Optional[Weather] = None,
                 forecast_daily: Optional[Weather] = None
                 ) -> None:
        geo.assert_is_lat(lat)
        self.lat = lat

        geo.assert_is_lon(lon)
        self.lon = lon

        self.timezone = timezone

        if current is None:
            raise ValueError("'current' must be set")
        self.current = current
        self.forecast_minutely = forecast_minutely
        self.forecast_hourly = forecast_hourly
        self.forecast_daily = forecast_daily

    def __repr__(self):
        return "<%s.%s - lat=%s, lon=%s, retrieval_time=%s>" % (
            __name__, self.__class__.__name__, self.lat, self.lon,
            self.current.reference_time() if self.current else None)

    def to_geopoint(self):
        """
        Returns the geoJSON compliant representation of the place for this One Call

        :returns: a ``.utils.geo.Point`` instance

        """
        if self.lon is None or self.lat is None:
            return None
        return geo.Point(self.lon, self.lat)


    @classmethod
    def from_dict(cls, the_dict: dict):
        """
        Parses a *OneCall* instance out of a data dictionary. Only certain properties of the data dictionary
        are used: if these properties are not found or cannot be parsed, an exception is issued.

        :param the_dict: the input dictionary
        :type the_dict: `dict`
        :returns: a *OneCall* instance or ``None`` if no data is available
        :raises: *ParseAPIResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the input dict embeds an HTTP status error

        """

        if the_dict is None:
            raise exceptions.ParseAPIResponseError('Data is None')

        # Check if server returned errors
        if 'success' in the_dict:
            if not the_dict['success']:
                return None
            try:
                the_dict = OpendataCWB.to_dict(the_dict)
            except ValueError:
                raise exceptions.ParseAPIResponseError(
                    f"{__name__}: impossible to read weather info from input data")

        try:
            current = Weather.from_dict(the_dict["current"])
            minutely = None
            if "minutely" in the_dict:
                minutely = [Weather.from_dict(item) for item in the_dict["minutely"]]
            hourly = None
            if "hourly" in the_dict:
                hourly = [Weather.from_dict(item) for item in the_dict["hourly"]]
            daily = None
            if "daily" in the_dict:
                daily = [Weather.from_dict(item) for item in the_dict["daily"]]

        except KeyError:
            raise exceptions.ParseAPIResponseError(
                f"{__name__}: impossible to read weather info from input data")

        return OneCall(
            lat=the_dict.get("lat", None),
            lon=the_dict.get("lon", None),
            timezone=the_dict.get("timezone", None),
            current=current,
            forecast_minutely=minutely,
            forecast_hourly=hourly,
            forecast_daily=daily
        )
