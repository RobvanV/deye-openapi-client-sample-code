import requests
from clientcode import variable

# Set time of use for the device
if __name__ == '__main__':
    url = variable.baseurl + '/strategy/dynamicControl'
    headers = variable.headers

    targetSOC = 15;  # low value (like 15)
    power = 10000;  # this is just an example, fill in your target power, range: 0~rated power; would affect the rate of change
    # request body
    data = {
      "deviceSn": "2301316667",
      # "maxSellPower": 100, #rated power, through endpoint /device/latest
      # "maxSolarPower": 100, #rated power, through endpoint /device/latest
      "solarSellAction": "on",
      "touAction": "on",
      "touDays": ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"], # 7days: SUNDAY to SATURDAY
      "workMode": "ZERO_EXPORT_TO_CT",
      "timeUseSettingItems": [
        {
          "enableGeneration": True,
          "enableGridCharge": True,
          "power": power,
          "soc": targetSOC,
          "time": "02:30",   # your control time
        },
        {
          "enableGeneration": True,
          "enableGridCharge": True,
          "power": power,
          "soc": targetSOC,
          "time": "06:30",  # your control time
        },
        {
          "enableGeneration": True,
          "enableGridCharge": True,
          "power": power,
          "soc": targetSOC,
          "time": "20:30" # your control time
        },
        {
          "enableGeneration": True,
          "enableGridCharge": True,
          "power": power,
          "soc": targetSOC,
          "time": "21:30", # your control time
        },
        {
          "enableGeneration": True,
          "enableGridCharge": True,
          "power": power,
          "soc": targetSOC,
          "time": "22:30" #control time
        },
        {
          "enableGeneration": True,
          "enableGridCharge": True,
          "power": power,
          "soc": targetSOC,
          "time": "23:30" # your control time
        },
      ]
  }

    # request post
    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())