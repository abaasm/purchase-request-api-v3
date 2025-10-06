import requests

# Configuration
API_URL = "http://localhost:5000/generate_purchase_request"  # Change to your Render URL after deployment
INVENTORY_FILE = "Shaghlaty_inventory_testing.xlsx"

# Request parameters
files = {'file': open(INVENTORY_FILE, 'rb')}
data = {
    'supplier_name': 'شركة نوال - Newal - كرار',
    'months_of_cover': 6,
    'months_to_average': '05-25,06-25,07-25,08-25'  # Optional: omit to use all months
}

# Make the request
print("Sending request to API...")
response = requests.post(API_URL, files=files, data=data)

# Handle response
if response.status_code == 200:
    output_filename = 'purchase_request_output.xlsx'
    with open(output_filename, 'wb') as f:
        f.write(response.content)
    print("Success! Purchase request saved to: " + output_filename)
else:
    print("Error " + str(response.status_code) + ":")
    print(response.json())
