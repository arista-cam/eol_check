# Arista CVP End of Life (EoL) Report Generator

## Overview

This Python script connects to an Arista CloudVision Portal (CVP) instance and generates a comprehensive End of Life (EoL) report for all network devices in your inventory. 

## Prerequisites

- Python 3.7 or higher
- Network access to your CVP/CVaaS instance
- CVP service account token with appropriate permissions

## Installation

### 1. Clone or download this repository
```bash
git clone <repository-url>
cd cvp-eol-report
```

### 2. Install required dependencies
```bash
pip install -r requirements.txt
```

## Configuration

### Generate a CVP Service Account Token

1. Log into your CVP instance
2. Navigate to **Settings** → **Access Control** → **Service Accounts**
3. Click **+ New Service Account**
4. Provide a name
5. Assign appropriate roles
6. Click **Generate Service Account Token**
7. **Copy the token immediately**

### Update the Script

Edit the script and update the following variables:
```python
# For CVaaS (Cloud)
client.connect(
    nodes=['CVP_IP'],  # Your CVaaS URL
    username='',
    password='',
    is_cvaas=True,
    api_token='TOKEN'  # Replace with your token
)

# For On-Premise CVP
client.connect(
    nodes=['CVP_IP'],  # Your CVP hostname or IP
    username='',
    password='',
    is_cvaas=False,
    api_token='TOKEN'  # Replace with your token
)
```

## Usage

### Run the script
```bash
python eol.py
```

### Output

The script provides two types of output:

#### 1. Console Output
```
================================================================================
DEVICE END OF LIFE REPORT
================================================================================

Device: switch-01
  Model: DCS-7280SR-48C6
  Serial: JPE12345678
  IP Address: 192.168.1.10
  EOS Version: 4.28.3M
  End of Sale: 2024-12-31
  End of Support: 2029-12-31
  End of Life: 2034-12-31
  EoL Announcement: 2023-06-15
  Status: Available

...

================================================================================
Report exported to device_eol_report_20250205_143022.csv
Total devices processed: 45
Devices with EoL data: 42
Devices without EoL data: 3
================================================================================
```

#### 2. CSV File

A timestamped CSV file is generated with the following columns:

- `hostname` - Device hostname
- `model` - Hardware model number
- `serial_number` - Device serial number
- `ip_address` - Management IP address
- `version` - EOS software version
- `end_of_sale` - Date when the model was discontinued for sale
- `end_of_support` - Date when support ends
- `end_of_life` - Date when all support ends
- `eol_announcement_date` - Date when EoL was announced
- `eol_status` - Whether EoL data is available for this model
