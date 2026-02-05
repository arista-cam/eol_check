from cvprac.cvp_client import CvpClient
import json
import csv
import warnings
import urllib3
from datetime import datetime

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Initialize CVP client
client = CvpClient()

# Connect with token authentication
client.connect(
    nodes=['CVP_IP'],
    username='',
    password='',
    is_cvaas=True,  
    api_token='TOKEN'
)

# Get inventory of all devices
inventory = client.api.get_inventory()

# Get all EoL data once (using POST instead of GET)
all_eol_data = {}
try:
    # Use POST for the EoL service API
    response = client.post('/api/v3/services/arista.eol.v1.EolService/GetAll', data={})
    
    if response and 'data' in response:
        # Create a lookup dictionary by model/hwSku
        for item in response['data']:
            hw_sku = item.get('key', {}).get('hwSku', '')
            if hw_sku:
                all_eol_data[hw_sku] = item.get('value', {})
    print(f"Successfully retrieved EoL data for {len(all_eol_data)} hardware models")
except Exception as e:
    print(f"Warning: Could not retrieve EoL data: {e}")

# Process each device
devices_info = []

for device in inventory:
    device_info = {
        'hostname': device['hostname'],
        'serial_number': device['serialNumber'],
        'model': device['modelName'],
        'system_mac': device['systemMacAddress'],
        'version': device.get('version', 'N/A'),
        'ip_address': device.get('ipAddress', 'N/A')
    }
    
    # Look up EoL info from the cached data
    model = device['modelName']
    if model in all_eol_data:
        eol_info = all_eol_data[model]
        device_info['end_of_sale'] = eol_info.get('endOfSale', 'N/A')
        device_info['end_of_support'] = eol_info.get('endOfSupport', 'N/A')
        device_info['end_of_life'] = eol_info.get('endOfLife', 'N/A')
        device_info['eol_announcement_date'] = eol_info.get('announcementDate', 'N/A')
        device_info['eol_status'] = 'Available'
    else:
        device_info['end_of_sale'] = 'Not Available'
        device_info['end_of_support'] = 'Not Available'
        device_info['end_of_life'] = 'Not Available'
        device_info['eol_announcement_date'] = 'Not Available'
        device_info['eol_status'] = 'No EoL Data'
    
    devices_info.append(device_info)

# Print results
print("\n" + "="*80)
print("DEVICE END OF LIFE REPORT")
print("="*80)

for device in devices_info:
    print(f"\nDevice: {device['hostname']}")
    print(f"  Model: {device['model']}")
    print(f"  Serial: {device['serial_number']}")
    print(f"  IP Address: {device['ip_address']}")
    print(f"  EOS Version: {device['version']}")
    print(f"  End of Sale: {device.get('end_of_sale', 'N/A')}")
    print(f"  End of Support: {device.get('end_of_support', 'N/A')}")
    print(f"  End of Life: {device.get('end_of_life', 'N/A')}")
    print(f"  EoL Announcement: {device.get('eol_announcement_date', 'N/A')}")
    print(f"  Status: {device.get('eol_status', 'N/A')}")

# Export to CSV
csv_filename = f'device_eol_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['hostname', 'model', 'serial_number', 'ip_address', 'version',
                  'end_of_sale', 'end_of_support', 'end_of_life', 
                  'eol_announcement_date', 'eol_status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for device in devices_info:
        writer.writerow({k: device.get(k, 'N/A') for k in fieldnames})

print("\n" + "="*80)
print(f"Report exported to {csv_filename}")
print(f"Total devices processed: {len(devices_info)}")
print(f"Devices with EoL data: {sum(1 for d in devices_info if d['eol_status'] == 'Available')}")
print(f"Devices without EoL data: {sum(1 for d in devices_info if d['eol_status'] == 'No EoL Data')}")
print("="*80)