import logging

import requests
from clientcode import variable

# When PV generation is abundant：after the PV system supplies the load, the excess PV generation along with the battery’s discharge power is sold to the grid;
# When PV generation is insufficient：after the battery (operating at its preset state-of-charge) supplies the load, any remaining discharged power is sold to the grid.
if __name__ == '__main__':
    url = variable.baseurl + '/strategy/dynamicControl'
    headers = variable.headers


    ratedPower = 2000 # this is just an example, get rated power through endpoint /device/latest
    power = 2000  # this is just an example, fill in your target power, range: 0~rated power; would affect the rate of change
    targetSOC = 15  # low value (like 15)
    # request body
    data = {
        "deviceSn": "2301316667",
        "maxSellPower": ratedPower,
        "maxSolarPower": ratedPower,
        "solarSellAction": "on",
        "touAction": "on",
        "touDays": ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"],
        # 7days: SUNDAY to SATURDAY
        "workMode": "SELLING_FIRST",
        "timeUseSettingItems": [
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "power": power,
                "soc": targetSOC,
                "time": "10:30"  # control time
            },
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "power": power,
                "soc": targetSOC,
                "time": "23:30"  # control time
            },
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "power": power,
                "soc": targetSOC,  # low value (like 15)
                "time": "04:30"  # control time
            },
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "power": power,
                "soc": targetSOC,
                "time": "05:30"  # control time
            },
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "power": 2000,
                "soc": 15,
                "time": "06:30"  # control time
            },
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "power": 2000,
                "soc": 15,
                "time": "07:30"  # control time
            },
        ]
    }

    # request post
    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())
