""" Opendata CWB convertor """
import time
from datetime import datetime

class OpendataCWB:

    @staticmethod
    def _get_weather(the_dict, index, wx_index, last_pop, mode):
        value = {}
        start_time = None
        value["dt"] = int(time.time())
        time_str = "time"
        elementname = "elementName"
        elementvalue = "elementValue"
        starttime = "startTime"
        value_str = "value"
        if "Time" in the_dict[0]:
            time_str = "Time"
            elementname = "ElementName"
            elementvalue = "ElementValue"
            starttime = "StartTime"
            value_str = "ElementValue"

        if index < len(the_dict[wx_index - 1][time_str]):
            start_time = the_dict[wx_index - 1][time_str][index][starttime]
        if start_time:
            try:
                if "T" in start_time:
                    value["dt"] = int(time.mktime(datetime.strptime(
                        start_time.strip(), "%Y-%m-%dT%H:%M:%S+08:00").timetuple()))
                else:
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
            if index < len(i[time_str]):
                element_value = i[time_str][index].get(elementvalue, None)
            if element_value is None:
                continue

            if i[elementname] in ["WeatherDescription", "\u5929\u6c23\u9810\u5831\u7d9c\u5408\u63cf\u8ff0"]:
                if value_str in element_value[0]:
                    value["weather"][0]["description"] = element_value[0][value_str]
                    value["weather"][0]["icon"] =  ""
                else:
                    value["weather"][0]["description"] = list(element_value[0].values())[0]
                    value["weather"][0]["icon"] =  ""
            elif i[elementname] in ["Wx", "\u5929\u6c23\u73fe\u8c61"]:
                if value_str in element_value[0]:
                    value["weather"][0]["main"] = element_value[0][value_str]
                    value["weather"][0]["id"] = int(element_value[1][value_str])
                else:
                    value["weather"][0]["main"] = list(element_value[0].values())[0]
                    value["weather"][0]["id"] = int(list(element_value[0].values())[1])
            elif pop_mode in i[elementname] or "\u964d\u96e8\u6a5f\u7387" in i[elementname]:
                for j in i[time_str]:
                    if start_time == j[starttime]:
                        if value_str in element_value[0]:
                            pop = element_value[0][value_str]
                        else:
                            pop = list(element_value[0].values())[0]
                        if pop == " " or pop == "-":
                            pop = "0"
                        value["pop"] = float(int(pop)/100)
                        break
            elif i[elementname]in ["AT", "\u9ad4\u611f\u6eab\u5ea6"]:
                if value_str in element_value[0]:
                    value["main"]["feels_like"] = int(element_value[0][value_str])
                else:
                    value["main"]["feels_like"] = int(list(element_value[0].values())[0])
            elif i[elementname] in ["MaxAT", "\u6700\u9ad8\u9ad4\u611f\u6eab\u5ea6"]:
                if value_str in element_value[0]:
                    value["main"]["feels_like"] = int(element_value[0][value_str])
                    value["feels_like"]["max"] = int(element_value[0][value_str])
                else:
                    value["main"]["feels_like"] = int(list(element_value[0].values())[0])
                    value["feels_like"]["max"] = int(list(element_value[0].values())[0])
            elif i[elementname] in ["MinAT", "\u6700\u4f4e\u9ad4\u611f\u6eab\u5ea6"]:
                if value_str in element_value[0]:
                    value["feels_like"]["min"] = int(element_value[0][value_str])
                else:
                    value["feels_like"]["min"] = int(list(element_value[0].values())[0])
            elif i[elementname] in ["UVI", "\u7d2b\u5916\u7dda\u6307\u6578"]:
                value["uvi"] = 0
                for j in i[time_str]:
                    if start_time == j[starttime]:
                        if value_str in element_value[0]:
                            value["uvi"] = int(j[elementvalue][0][value_str])
                        else:
                            value["uvi"] = int(list(j[elementvalue][0].values())[0])
                        break
            elif i[elementname] in ["T", "\u6eab\u5ea6", "\u5e73\u5747\u6eab\u5ea6"]:
                if value_str in element_value[0]:
                    value["main"]["temp"] = int(element_value[0][value_str])
                else:
                    value["main"]["temp"] = int(list(element_value[0].values())[0])
            elif i[elementname] in ["MaxT", "\u6700\u9ad8\u6eab\u5ea6"]:
                if value_str in element_value[0]:
                    value["main"]["temp_max"] = int(element_value[0][value_str])
                else:
                    value["main"]["temp_max"] = int(list(element_value[0].values())[0])
            elif i[elementname] in ["MinT", "\u6700\u4f4e\u6eab\u5ea6"]:
                if value_str in element_value[0]:
                    value["main"]["temp_min"] = int(element_value[0][value_str])
                else:
                    value["main"]["temp_min"] = int(list(element_value[0].values())[0])
            elif i[elementname] in ["Td", "\u9732\u9ede\u6eab\u5ea6", "\u5e73\u5747\u9732\u9ede\u6eab\u5ea6"]:
                if value_str in element_value[0]:
                    value["calc"]["dewpoint"] = int(element_value[0][value_str]) * 100
                else:
                    value["calc"]["dewpoint"] = int(list(element_value[0].values())[0]) * 100
            elif i[elementname] in ["RH", "\u76f8\u5c0d\u6fd5\u5ea6", "\u5e73\u5747\u76f8\u5c0d\u6fd5\u5ea6"]:
                if value_str in element_value[0]:
                    value["humidity"] = int(element_value[0][value_str])
                else:
                    value["humidity"] = int(list(element_value[0].values())[0])
            elif i[elementname] in ["MinCI", "\u8212\u9069\u5ea6\u6307\u6578"]:
                if value_str in element_value[0]:
                    value["calc"]["humidex"] = int(element_value[0][value_str])
                else:
                    value["calc"]["humidex"] = int(list(element_value[0].values())[0])
            elif i[elementname] in ["MaxCI", "\u8212\u9069\u5ea6\u6307\u6578"]:
                if value_str in element_value[0]:
                    value["calc"]["heatindex"] = int(element_value[0][value_str])
                else:
                    value["calc"]["heatindex"] = int(list(element_value[0].values())[0])
            elif i[elementname] in ["WS", "\u98a8\u901f"]:
                if value_str in element_value[0]:
                    value["wind_speed"] = int(''.join(
                        k for k in element_value[0][value_str] if k.isdigit()))
                    value["wind_gust"] = int(''.join(
                        c for c in element_value[1][value_str] if c.isdigit()))
                else:
                    value["wind_speed"] = int(''.join(
                        k for k in list(element_value[0].values())[0] if k.isdigit()))
                    value["wind_gust"] = int(''.join(
                        c for c in list(element_value[0].values())[1] if c.isdigit()))
            elif i[elementname] in ["WD", "\u98a8\u5411"]:
                if value_str in element_value[0]:
                    value["wind_deg"] = element_value[0][value_str]
                else:
                    value["wind_deg"] = list(element_value[0].values())[0]
            else:
                if value_str in element_value[0]:
                    value[i[elementname]] = element_value[0][value_str]
                else:
                    value[i[elementname]] = list(element_value[0].values())[0]

        return value

    @classmethod
    def to_dict(cls, the_dict):
        value = {}
        time_str = "time"
        locations = "locations"
        location = "location"
        latitude = "lat"
        longitude = "lon"
        weatherelement = "weatherElement"
        datasetdescription = "datasetDescription"
        elementname = "elementName"
        if "Locations" in the_dict["records"]:
            time_str = "Time"
            locations = "Locations"
            location = "Location"
            latitude = "Latitude"
            longitude = "Longitude"
            weatherelement = "WeatherElement"
            datasetdescription = "DatasetDescription"
            elementname = "ElementName"

        record = None
        for i in the_dict["records"][locations]:
            if len(i[location]) >= 1:
                record = i
                break

        if record is None:
            return value

        value["lon"] = float(record[location][0][longitude])
        value["lat"] = float(record[location][0][latitude])
        value["timezone"] = 8

        mode = ""
        dataset_desc = record[datasetdescription]
        if dataset_desc == "\u81fa\u7063\u5404\u7e23\u5e02\u9109\u93ae\u672a\u4f861\u9031\u901012\u5c0f\u6642\u5929\u6c23\u9810\u5831":
            mode = "daily"
        if dataset_desc == "\u81fa\u7063\u5404\u7e23\u5e02\u9109\u93ae\u672a\u4f861\u9031\u5929\u6c23\u9810\u5831":
            mode = "daily"
        if dataset_desc == "\u81fa\u7063\u5404\u7e23\u5e02\u9109\u93ae\u672a\u4f863\u5929(72\u5c0f\u6642)\u90103\u5c0f\u6642\u5929\u6c23\u9810\u5831":
            mode = "hourly"
        if dataset_desc == "\u81fa\u7063\u5404\u7e23\u5e02\u9109\u93ae\u672a\u4f863\u5929\u5929\u6c23\u9810\u5831":
            mode = "hourly"

        wx_index = 0
        length = 0
        last_pop = 0
        for i in record[location][0][weatherelement]:
            if i[elementname] == "Wx" or "\u5929\u6c23\u73fe\u8c61" == i[elementname]:
                length = len(i[time_str])
                break
            wx_index = wx_index + 1

        value["current"] = OpendataCWB._get_weather(
            record[location][0][weatherelement], 0, wx_index, last_pop, mode)
        last_pop = value["current"]["pop"]

        value[mode] = []
        for i in range(1, length):
            value[mode].append(OpendataCWB._get_weather(
                record[location][0][weatherelement], i, wx_index, last_pop, mode))
            last_pop = value["current"]["pop"]

        return value
