import logging

import requests
from clientcode import variable

# Set operation mode as Fully Charge via dynamic control
# - When PV generation is sufficient, after supplying the load, the battery is charged until it reaches the preset value:
#   - If workMode is set to SELLING_FIRST, no further charging occurs;
#   - If workMode is not set to SELLING_FIRST, charging continues until it is no longer possible, at which point any excess is sold to the grid.
# - When PV generation is insufficient, the deficit is met by purchasing electricity from the grid.
if __name__ == '__main__':
    url = variable.baseurl + '/strategy/dynamicControl'
    headers = variable.headers

    targetSOC = 90;  # high value(like 90)
    power = 4000;  #this is just an example,fill in your target power (Reference valu : power = min(maxAcharge current, gridChargeAmpere) * vol)
    # request body
    data = {
        "deviceSn": "2301316667",
        "gridChargeAction": "on",
        #"gridChargeAmpere": 0,  # BMSCharge current limit;
        "touAction": "on",
        "touDays": ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"],
        # 7days: SUNDAY to SATURDAY
        "workMode": "ZERO_EXPORT_TO_CT",  #  ZERO_EXPORT_TO_CT(if CT exists) or ZERO_EXPORT_TO_LOAD
        "timeUseSettingItems": [
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "soc": targetSOC,  # high value
                "power":power,
                "time": "00:10"  # your control time
            },
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "soc": targetSOC,  # high value
                "power": power,
                "time": "02:10"  # your control time
            },
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "soc": targetSOC,  # high value
                "power": power,
                "time": "04:10"  # your control time
            },
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "soc": targetSOC,  # high value
                "power": power,
                "time": "15:10"  # your control time
            },
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "soc": targetSOC,  # high value
                "power": power,
                "time": "20:10"  # your control time
            },
            {
                "enableGeneration": True,
                "enableGridCharge": True,
                "soc": targetSOC,  # high value
                "power": power,
                "time": "23:10"  # your control time
            }
        ]
    }

    # request post
    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())
