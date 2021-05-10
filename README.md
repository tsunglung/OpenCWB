

Home assistant support for [Opendata CWB](https://opendata.cwb.gov.tw/index) (Taiwan Centtal Bureau).
[中文版說明](https://github.com/tsunglung/OpenCWB/blob/master/README_zh-tw.md).


This integration is based on [OpenWeatherMap](https://openweathermap.org) ([@csparpa](https://pypi.org/user/csparpa), [pyowm](https://github.com/csparpa/pyowm)) to develop.

## Install

You can install component with [HACS](https://hacs.xyz/) custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `tsunglung/OpenCWB` > Category: Integration

Or manually copy `opencwb` folder to `custom_components` folder in your config folder.

And `do not forget` to restart Home Assistant.

# Pre-reqirement

**Apply a API key from Opendata CWB**
1. Browse to [Opendata CWB](https://opendata.cwb.gov.tw/userLogin) account page.
2. Login or [register an account](https://pweb.cwb.gov.tw/CWBMEMBER3/register/authorization).
3. Get your personal API Key.

# Config

**Please follow the config flow of Home Assistant**


1. With GUI. Configuration > Integration > Add Integration > OpneCWB
   a. If the integration didn't show up in the list please REFRESH the page.
   b. If the integration is still not in the list, you need to clear the browser cache.
2. Enter API key from previous step.
3. Enter the location name of Taiwan (in Chinese. XD). Please reference to the offical [documents](https://opendata.cwb.gov.tw/opendatadoc/CWB_Opendata_API_V1.2.pdf) appendix A.
   a. Some location name need to include the city name.

# Option

1. You could setup for the scan interval. One call per hour or per day.

Buy Me A Coffee

If you think the add-on is useful for you, please consider to buy me a coffee for support my work.

<a href="https://www.buymeacoffee.com/tsunglung" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="30" width="120"></a>

And for people live in Taiwan, you could use services below since Paypal might not wirk due to the goverment policy.

|  LINE Pay | LINE Bank | JKao Pay |
| :------------: | :------------: | :------------: |
| <img src="https://github.com/tsunglung/OpenCWB/blob/master/linepay.jpg" alt="Line Pay" height="200" width="200">  | <img src="https://github.com/tsunglung/OpenCWB/blob/master/linebank.jpg" alt="Line Bank" height="200" width="200">  | <img src="https://github.com/tsunglung/OpenCWB/blob/master/jkopay.jpg" alt="JKo Pay" height="200" width="200">  |
