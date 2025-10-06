# Shaghlaty Purchase Request API

A Flask-based REST API that generates purchase requests from inventory Excel files.

## Features
- Upload inventory Excel file
- Specify supplier, months of coverage, and optional months to average
- Returns formatted Excel with product images, sales data, and calculated purchase quantities
- Row height set to 100 for easy viewing of product images

## API Endpoints

### GET /
Returns API information and available endpoints.

### POST /generate_purchase_request
Generate a purchase request Excel file.

**Parameters (multipart/form-data):**
- `file`: Excel file with inventory data (required)
- `supplier_name`: Name of the supplier (required)
- `months_of_cover`: Number of months to cover (required, integer)
- `months_to_average`: Comma-separated list of month columns to average (optional)

**Example using curl:**
```bash
curl -X POST \
  -F "file=@Shaghlaty_inventory_testing.xlsx" \
  -F "supplier_name=شركة نوال - Newal - كرار" \
  -F "months_of_cover=6" \
  -F "months_to_average=05-25,06-25,07-25,08-25" \
  http://localhost:5000/generate_purchase_request \
  --output purchase_request.xlsx
```

**Example using Python requests:**
```python
import requests

url = "http://localhost:5000/generate_purchase_request"

files = {'file': open('Shaghlaty_inventory_testing.xlsx', 'rb')}
data = {
    'supplier_name': 'شركة نوال - Newal - كرار',
    'months_of_cover': 6,
    'months_to_average': '05-25,06-25,07-25,08-25'
}

response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    with open('purchase_request.xlsx', 'wb') as f:
        f.write(response.content)
    print("Purchase request generated successfully!")
else:
    print("Error:", response.json())
```

## Deployment on Render.com

### Step 1: Prepare your repository
1. Create a new GitHub repository
2. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `README.md`

### Step 2: Deploy on Render
1. Go to https://render.com and sign in
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: shaghlaty-purchase-api (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (or paid for production)
5. Click "Create Web Service"

### Step 3: Wait for deployment
Render will automatically build and deploy your service. Once complete, you'll get a URL like:
`https://shaghlaty-purchase-api.onrender.com`

### Step 4: Test your API
```bash
curl https://shaghlaty-purchase-api.onrender.com/
```

## Local Development

### Run locally:
```bash
pip install -r requirements.txt
python app.py
```

The API will be available at `http://localhost:5000`

## Input File Format

Your Excel file should contain:
- **Products**: Product code/SKU
- **supplier**: Supplier name
- **current stock**: Current inventory quantity
- **Month columns**: e.g., 05-25, 06-25, 07-25, 08-25 (sales for each month)

## Output File

The generated Excel includes:
- products
- product_image (Excel IMAGE formula)
- supplier
- Selected month sales columns
- avg_monthly_sales
- current stock
- target_stock
- purchase_qty

Row height is set to 100 and image column width to 25 for optimal viewing.

## Notes
- Maximum file size: 16MB
- Product images are pulled from: https://ecomedia.shaghlaty.net/media/catalog/<PRODUCT>.jpg
- If a supplier is not found, returns 404 error
- All calculations round up purchase quantities to nearest integer
