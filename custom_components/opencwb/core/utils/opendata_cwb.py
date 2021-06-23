""" Opendata CWB convertor """
import time
from datetime import datetime

class OpendataCWB:

    @staticmethod
    def _get_weather(the_dict, index, wx_index, last_pop, mode):
        value = {}
        start_time = None
        value["dt"] = int(time.time())
        if index < len(the_dict[wx_index]["time"]):
            start_time = the_dict[wx_index]["time"][index]["startTime"]
        if start_time:
            try:
                value["dt"] = int(time.mktime(datetime.strptime(
                    start_time.strip(), "%Y-%m-%d %H:%M:%S").timetuple()))
            except ValueError as error:
                pass
        value["weather"] = [{}]
        value["main"] = {}
        value["calc"] = {}
        value["feels_like"] = {}
        value["pop"] = last_pop
        pop_mode = "PoP12h"
        if mode == "hourly":
            # PoP6h or PoP3h
            pop_mode = "PoP"
        for i in the_dict:
            element_value = None
            if index < len(i["time"]):
                element_value = i["time"][index].get("elementValue", None)
            if element_value is None:
                continue
            if "WeatherDescription" == i["elementName"]:
                value["weather"][0]["description"] = element_value[0]["value"]
                value["weather"][0]["icon"] =  ""
            elif "Wx" == i["elementName"]:
                value["weather"][0]["main"] = element_value[0]["value"]
                value["weather"][0]["id"] = int(element_value[1]["value"])
            elif pop_mode in i["elementName"]:
                for j in i["time"]:
                    if start_time == j["startTime"]:
                        pop = element_value[0]["value"]
                        if pop == " ":
                            pop = "0"
                        value["pop"] = float(int(pop)/100)
                        break
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
        for i in the_dict["records"]["locations"]:
            if len(i["location"]) >= 1:
                record = i
                break

        if record is None:
            return value

        value["lon"] = float(record["location"][0]["lon"])
        value["lat"] = float(record["location"][0]["lat"])
        value["timezone"] = 8

        mode = ""
        dataset_desc = record["datasetDescription"]
        if dataset_desc == "\u81fa\u7063\u5404\u7e23\u5e02\u9109\u93ae\u672a\u4f861\u9031\u901012\u5c0f\u6642\u5929\u6c23\u9810\u5831":
            mode = "daily"
        if dataset_desc == "\u81fa\u7063\u5404\u7e23\u5e02\u9109\u93ae\u672a\u4f863\u5929(72\u5c0f\u6642)\u90103\u5c0f\u6642\u5929\u6c23\u9810\u5831":
            mode = "hourly"

        wx_index = 0
        length = 0
        last_pop = 0
        for i in record["location"][0]["weatherElement"]:
            if i['elementName'] == "Wx":
                length = len(i["time"])
                break
            wx_index = wx_index + 1

        value["current"] = OpendataCWB._get_weather(
            record["location"][0]["weatherElement"], 0, wx_index, last_pop, mode)
        last_pop = value["current"]["pop"]

        value[mode] = []
        for i in range(1, length):
            value[mode].append(OpendataCWB._get_weather(
                record["location"][0]["weatherElement"], i, wx_index, last_pop, mode))
            last_pop = value["current"]["pop"]

        return value
