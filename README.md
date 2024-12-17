<a href="https://www.buymeacoffee.com/tsunglung" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="30" width="120"></a>

Home assistant support for [Opendata CWA](https://opendata.cwa.gov.tw/index) (prvious Opendata CWB). [The readme in Traditional Chinese](https://github.com/tsunglung/OpenCWB/blob/master/README_zh-tw.md).


This integration is based on [OpenWeatherMap](https://openweathermap.org) ([@csparpa](https://pypi.org/user/csparpa), [pyowm](https://github.com/csparpa/pyowm)) to develop.

## Install

You can install component with [HACS](https://hacs.xyz/) custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `tsunglung/OpenCWB` > Category: Integration

Or manually copy `opencwb` folder to `custom_components` folder in your config folder.

Then restart HA.

# Setup

**Apply a API key in Opendata CWA**
1. Open the [Opendata CWA](https://opendata.cwa.gov.tw/devManual/insrtuction) Web Site
2. Register your account
3. Get your personal API Key.

# Config

**Please use the config flow of Home Assistant**


1. With GUI. Configuration > Integration > Add Integration > OpneCWA
   1. If the integration didn't show up in the list please REFRESH the page
   2. If the integration is still not in the list, you need to clear the browser cache.
2. Enter API key.
3. Enter the location name of Taiwan. Please reference to the name in the [doc](https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf).
   1. Some location name need to include the city name.

Buy Me A Coffee

|  LINE Pay | LINE Bank | JKao Pay |
| :------------: | :------------: | :------------: |
| <img src="https://github.com/tsunglung/OpenCWB/blob/master/linepay.jpg" alt="Line Pay" height="200" width="200">  | <img src="https://github.com/tsunglung/OpenCWB/blob/master/linebank.jpg" alt="Line Bank" height="200" width="200">  | <img src="https://github.com/tsunglung/OpenCWB/blob/master/jkopay.jpg" alt="JKo Pay" height="200" width="200">  |
