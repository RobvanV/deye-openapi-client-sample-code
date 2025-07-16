import requests
import variable
import crcmod
from binascii import unhexlify
import time

# Initialize CRC function for Modbus
crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)

def get_user_input():
    """Get operation parameters from user"""
    print("\n" + "="*40)
    print("Deye Modbus Control")
    print("="*40)

    # Get basic parameters
    slave_id = int(input("Slave_Id: ")or 1)
    fc = int(input("Function Code (3=read, 16=write multiple): ") or 3)
    reg = int(input("Register address (decimal): ") or 609)
    count = int(input("Number of registers (decimal): ") or 1)

    # Get data values if writing
    data_values = []
    if fc in [6, 16]:
        if fc == 6:  # Single register write
            value = int(input("Enter value to write (decimal): "))
            data_values.append(value)
        else:  # Multiple register write
            print(f"Enter {count} values (one per line):")
            for i in range(count):
                value = int(input(f"Value {i+1}: "))
                data_values.append(value)

    return slave_id, fc, reg, count, data_values

def build_modbus_message(slave_id, fc, reg, count, data_values=None):
    """Construct Modbus message with CRC"""
    # Build base message
    if fc == 3:  # Read holding registers
        message = bytes([
            slave_id,
            fc,
            (reg >> 8) & 0xFF,
            reg & 0xFF,
            (count >> 8) & 0xFF,
            count & 0xFF
        ])
    elif fc == 6:  # Write single register
        message = bytes([
            slave_id,
            fc,
            (reg >> 8) & 0xFF,
            reg & 0xFF,
            (data_values[0] >> 8) & 0xFF,
            data_values[0] & 0xFF
        ])
    elif fc == 16:  # Write multiple registers
        byte_count = count * 2
        message = bytes([slave_id, fc, (reg >> 8) & 0xFF, reg & 0xFF,
                        (count >> 8) & 0xFF, count & 0xFF, byte_count])
        for value in data_values:
            message += bytes([(value >> 8) & 0xFF, value & 0xFF])

    # Add CRC
    crc = crc16(message)
    message += bytes([crc & 0xFF, (crc >> 8) & 0xFF])

    # Format as spaced hex string
    return ' '.join(f"{b:02X}" for b in message)

def parse_response(hex_str):
    """Parse Modbus response into human-readable format"""
    try:
        hex_str = hex_str.replace(' ', '')
        data = unhexlify(hex_str)

        if len(data) < 3:
            return "Invalid response (too short)"

        slave = data[0]
        func = data[1]

        if func & 0x80:  # Error response
            error_code = data[2]
            errors = {
                1: "Illegal Function",
                2: "Illegal Data Address",
                3: "Illegal Data Value",
                4: "Server Failure"
            }
            return f"ERROR: {errors.get(error_code, f'Unknown ({error_code})')}"

        if func == 3:  # Read response
            byte_count = data[2]
            values = []
            for i in range(3, 3 + byte_count, 2):
                if i+1 < len(data):
                    values.append((data[i] << 8) | data[i+1])
            return {
                'Slave': slave,
                'Function': 'Read',
                'Values': values
            }
        elif func in [6, 16]:  # Write response
            return {
                'Slave': slave,
                'Function': 'Write',
                'Address': (data[2] << 8) | data[3],
                'Count': (data[4] << 8) | data[5]
            }
        else:
            return f"Unknown function code: {func}"
    except Exception as e:
        return f"Parse error: {str(e)}"

def get_order_status(order_id):
    """Check order status with retry logic"""
    url = f"{variable.baseurl}/order/{order_id}"
    max_retries = 30  # 30 retries * 2s = 60s timeout
    retry_count = 0
    
    while retry_count < max_retries:
        response = requests.get(url, headers=variable.headers)
        if response.status_code == 200:
            order_data = response.json()
            status = order_data.get("status")
            
            # Status meanings:
            # 0: Created (waiting)
            # 100: Sending (in progress)
            # 666: Success (with analysis result)
            # Other: Error, check documentation api to resolve

            
            if status == 666:  # Success
                return order_data
            elif status in [0, 100]:  # Still processing
                print(f"Status: {status} - Processing...")
                time.sleep(2)  # Wait 2 seconds before retrying
                retry_count += 1
            else:  # Error state
                return order_data
        else:
            print(f"Error fetching order: {response.status_code}")
            return None
    
    # Timeout reached
    print("Timeout: Order processing took too long")
    return None

def main():
    # Get user input
    slave_id, fc, reg, count, data_values = get_user_input()

    # Build message
    message = build_modbus_message(slave_id, fc, reg, count, data_values)
    print(f"\nGenerated Modbus message: {message}")

    # Send to device
    data = {   # REMEMBER TO SETUP CORRECTLY THE HEADERS ON variables.py
        "deviceSn": "1312", # <-------------------------------------------- your own SN
        "content": message, 
        "timeoutSeconds": 600
    }
    
    if(data.get("deviceSn") == "1312"):
        print("SETUP NOT CORRECTLY DONE, ADD yourSN")

    response = requests.post(variable.baseurl + '/order/customControl',
                           headers=variable.headers, json=data)

    if response.status_code == 200:
        order_id = response.json().get("orderId")
        print(f"Order ID: {order_id}")

        if order_id:
            # Get order status with retry logic
            order_data = get_order_status(order_id)
            
            if order_data:
                status = order_data.get("status")
                
                if status == 666:
                    print("STATUS: 666 (SUCCEED)")
                    analysis = order_data.get("analysisResult", "")
                    print(f"\nRaw Response: {analysis}")

                    # Parse and display
                    parsed = parse_response(analysis)
                    print("\nParsed Response:")
                    if isinstance(parsed, dict):
                        for k, v in parsed.items():
                            print(f"{k}: {v}")
                    else:
                        print(parsed)
                else:
                    error_msg = order_data.get("error", "Unknown error")
                    print(f"\nError Status: {status}")
                    print(f"Error Message: {error_msg}")
                    print("Full response:", order_data)
            else:
                print("Failed to get order status")
    else:
        print(f"Request failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
