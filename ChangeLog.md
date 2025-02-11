# DeyeCloud API ChangeLog

## December, 2024

### Dec 11
**Feature**
- Launched Strategy Dynamic Control:( /v1.0/strategy/dynamicControl under model:Strategy Operation)
  - Set multiple parameters through a single interface, including: 
    - gridChargeAction: "on/off"; Enable or disable gridCharge
    - gridChargeAmpere: Set the value of gridChargeAmpere
    - maxSellPower: Set the value of maxSellPower 
    - maxSolarPower: Set the value of maxSolarPower
    - solarSellAction: "on/off"; Enable or disable solarSell
    - timeUseSettingItems: set the value of timeOfUse for 6 time intervals(For details, please refer to endpoint /v1.0/order/sys/tou/update under Comission Operation Model)
    - touAction: "on/off"; Enable or disable timeOfUse Settings
    - touDays: ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]; Specify the days on which you want TOU to be active
    - workMode: "SELLING_FIRST/ZERO_EXPORT_TO_LOAD/ZERO_EXPORT_TO_CT"; set the system's operating mode to one of these three options

  You don't need to set all of these parameters; any parameter left unset will retain its previous value.

### Dec 18
**Feature**
- Launched Station Alert List, retrieving station alert list using 10-digit Unix timestamps (in seconds) for stations, with support for paginated queries
- Launched Device Alert List, retrieving device alert list using 10-digit Unix timestamp(in seconds)


## February, 2025
### Feb 10
**Feature**
- Launched function:grid peak shaving(/v1.0/order/gridPeakShaving/control)
    - action: "on/off"; Enable or disable gridPeakShaving
    - power: grid output power will be limited within the set value
  
   When gridPeakShaving is active, grid output power will be limited within the set value. 
   If the load power exceeds the allowed value, it will take PV energy and battery as supplement. 
   If still can’t meet the load requirement, grid power will increase to meet the load needs. 
 
