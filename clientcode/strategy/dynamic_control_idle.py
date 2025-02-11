import requests
from clientcode import variable

# The battery ceases both charging and discharging.
# PV generation is abundant：workMode=SELLING_FIRST, the PV output flows to the load first and then to  grid;
# PV generation is insufficient, power is purchased to supply the load.
if __name__ == '__main__':
    url = variable.baseurl + '/strategy/dynamicControl'
    headers = variable.headers

    targetSOC = 70;  # current soc, through endpoint /device/latest
    power = 10000;  #your target power, range: 0~rated power
    # request body
    data = {
      "deviceSn": "2301316667",
      "solarSellAction": "on",
      "touAction": "on",
      "touDays": ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"], # 7days: SUNDAY to SATURDAY
      "workMode": "SELLING_FIRST",
      "timeUseSettingItems": [
        {
          "enableGeneration": True,
          "enableGridCharge": True,
          "power": power,
          "soc": targetSOC,
          "time": "02:30", # control time
        },
        {
          "enableGeneration": True,
          "enableGridCharge": True,
          "power": power,
          "soc": targetSOC,
          "time": "06:30",  # control time
        },
        {
          "enableGeneration": True,
          "enableGridCharge": True,
          "power": power,
          "soc": targetSOC,
          "time": "20:30" # control time
        },
        {
          "enableGeneration": True,
          "enableGridCharge": True,
          "power": power,
          "soc": targetSOC,
          "time": "21:30", # control time
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
          "time": "23:30" # control time
        },
      ]
  }

    # request post
    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())