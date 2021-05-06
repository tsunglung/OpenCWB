import time
from datetime import datetime
import logging
_LOGGER = logging.getLogger(__name__)

class OpendataCWB:

    @staticmethod
    def _get_weather(the_dict, index):
        value = {}
        start_time = the_dict[0]["time"][index]["startTime"]
        try:
            value["dt"] = int(time.mktime(datetime.strptime(start_time.strip(), "%Y-%m-%d %H:%M:%S").timetuple()))
        except ValueError as error:
            value["dt"] = int(time.time())
        value["weather"] = [{}]
        value["main"] = {}
        value["calc"] = {}
        value["feels_like"] = {}
        for i in the_dict:
            element_value = []
            if index < len(i["time"]):
                element_value = i["time"][index]["elementValue"]
            if "WeatherDescription" == i["elementName"]:
                value["weather"][0]["description"] = element_value[0]["value"]
                value["weather"][0]["icon"] =  ""
            elif "Wx" == i["elementName"]:
                value["weather"][0]["main"] = element_value[0]["value"]
                value["weather"][0]["id"] = int(element_value[1]["value"])
            elif "PoP" in i["elementName"]:
                pop = i["time"][index]["elementValue"][0]["value"]
                if pop == " ":
                    pop = "0"
                value["pop"] = float(int(pop)/100)
            elif "AT" == i["elementName"]:
                value["main"]["feels_like"] = int(element_value[0]["value"])
            elif "MaxAT" == i["elementName"]:
                value["main"]["feels_like"] = int(element_value[0]["value"])
                value["feels_like"]["max"] = int(element_value[0]["value"])
            elif "MinAT" == i["elementName"]:
                value["feels_like"]["min"] = int(element_value[0]["value"])
            elif "UVI" == i["elementName"]:
                value["uvi"] = 0
                for j in i["time"]:
                    if start_time == j["startTime"]:
                        value["uvi"] = int(j["elementValue"][0]["value"])
                        break
            elif "T" == i["elementName"]:
                value["main"]["temp"] = int(element_value[0]["value"])
            elif "MaxT" == i["elementName"]:
                value["main"]["temp_max"] = int(element_value[0]["value"])
            elif "MinT" == i["elementName"]:
                value["main"]["temp_min"] = int(element_value[0]["value"])
            elif "Td" == i["elementName"]:
                value["calc"]["dewpoint"] = int(element_value[0]["value"]) * 100
            elif "RH" == i["elementName"]:
                value["humidity"] = int(element_value[0]["value"])
            elif "MinCI" == i["elementName"]:
                value["calc"]["humidex"] = int(element_value[0]["value"])
            elif "MaxCI" == i["elementName"]:
                value["calc"]["heatindex"] = int(element_value[0]["value"])
            elif "WS" == i["elementName"]:
                value["wind_speed"] = int(element_value[0]["value"])
                value["wind_gust"] = int(''.join(
                    c for c in element_value[1]["value"] if c.isdigit()))
            elif "WD" == i["elementName"]:
                value["wind_deg"] = element_value[0]["value"]
            else:
                value[i["elementName"]] = element_value[0]["value"]
        return value

    @classmethod
    def to_dict(cls, the_dict):
        value = {}
        record = None
#        _LOGGER.error(the_dict)
        for i in the_dict["records"]["locations"]:
            if len(i["location"]) >= 1:
                record = i
                break

        if record is None:
            return value
#        _LOGGER.error(record)
        value["lon"] = float(record["location"][0]["lon"])
        value["lat"] = float(record["location"][0]["lat"])
        value["timezone"] = 8

        value["current"] = OpendataCWB._get_weather(
            record["location"][0]["weatherElement"], 0)
        if len(record["location"][0]["weatherElement"][0]["time"]) > 12:
            value["daily"] = []
            for i in range(1, len(record["location"][0]["weatherElement"][0]["time"])):
                value["daily"].append(OpendataCWB._get_weather(
                    record["location"][0]["weatherElement"], i))
        else:
            value["hourly"] = []
            for i in range(1, len(record["location"][0]["weatherElement"][0]["time"])):
                value["hourly"].append(OpendataCWB._get_weather(
                    record["location"][0]["weatherElement"], i))
#        _LOGGER.error(value)
        return value
