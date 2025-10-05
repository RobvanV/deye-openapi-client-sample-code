import requests
import hashlib
from clientcode import variable
"""
The token serves as the credential for accessing resources. Currently, registration via mobile number, email address, 
or username is supported on DeyeCloud. Users can choose one of three options for login (either the mobile, email, 
or username field is required;When the field mobile is used, the field countryCode must also be included). 
If companyId is not provided, the token retrieved will correspond to the Personal user. 
When companyId is provided, the token retrieved will correspond to the business member companyId can be 
obtained through endpoints ‘/v1.0/account/info’
"""
if __name__ == '__main__':
    appId = '202510052724002'      # Replace with  your appId
    url = variable.baseurl + '/account/token?appId=' + appId
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
            "appSecret": "346bb5e95ec2d3adb895ff01f54e8e46",      # Replace with your appSecret
            "email": "Rob.van.voorbergen@hetnet.nl",      # Replace with your email
                            #   "companyId": "0", Replace with your companyId
            "password": "35de3ea327784618385284a8b79c69efede850327225acb8eaa9ce938a383e05"
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        print(response.status_code)
        print(response.json())

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


