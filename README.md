<a href="https://www.buymeacoffee.com/tsunglung" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="30" width="120"></a>

Home assistant support for [Opendata CWB](https://opendata.cwb.gov.tw/index). [The readme in Traditional Chinese](https://github.com/tsunglung/OpenCWB/blob/master/README_zh-tw.md).


This integration is based on [OpenWeatherMap](https://openweathermap.org) ([@csparpa](https://pypi.org/user/csparpa), [pyowm](https://github.com/csparpa/pyowm)) to develop.

## Install

You can install component with [HACS](https://hacs.xyz/) custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `tsunglung/OpenCWB` > Category: Integration

Or manually copy `opencwb` folder to `custom_components` folder in your config folder.

Then restart HA.

# Setup

**Apply a API key in Opendata CWB**
1. Open the [Opendata CWB](https://opendata.cwb.gov.tw/devManual/insrtuction) Web Site
2. Register your account
3. Get your personal API Key.

# Config

**Please use the config flow of Home Assistant**


1. With GUI. Configuration > Integration > Add Integration > OpneCWB
   1. If the integration didn't show up in the list please REFRESH the page
   2. If the integration is still not in the list, you need to clear the browser cache.
2. Enter API key.
3. Enter the location name of Taiwan. Please reference to the name in the [doc](https://opendata.cwb.gov.tw/opendatadoc/CWB_Opendata_API_V1.2.pdf) appendix A.

<img src="https://github.com/tsunglung/OpenCWB/blob/master/linepay.jpg" alt="Line Pay" height="200" width="200"><img src="https://github.com/tsunglung/OpenCWB/blob/master/jkopay.jpg" alt="JKo Pay" height="200" width="200">
