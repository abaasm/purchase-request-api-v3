# Shaghlaty Purchase Request API Documentation

## Base URL
```
https://purchase-request-api-v3.onrender.com
```

## Version
1.2

---

## Endpoints

### 1. Health Check / Service Info

**GET** `/`

Returns basic information about the API service and available endpoints.

#### Request
No parameters required.

#### Response
```json
{
    "service": "Shaghlaty Purchase Request API",
    "version": "1.2",
    "endpoints": {
        "/generate_purchase_request": {
            "method": "POST",
            "description": "Generate a purchase request Excel file",
            "parameters": {...},
            "returns": "Excel file download with LC in USD and LC in IQD columns"
        }
    }
}
```

#### Example (cURL)
```bash
curl https://purchase-request-api-v3.onrender.com/
```

---

### 2. Generate Purchase Request

**POST** `/generate_purchase_request`

Generates a purchase request Excel file for a specific supplier based on inventory data, sales history, and desired months of stock coverage.

#### Request Parameters

All parameters are sent as **multipart/form-data**.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | Excel file (.xlsx) containing inventory data with columns: Products, Supplier, Current Stock, LC (optional), and month columns (datetime format) |
| `supplier_name` | String | Yes | Exact name of the supplier as it appears in the inventory file (case-sensitive, including Arabic characters) |
| `months_of_cover` | Integer | Yes | Number of months of stock coverage to target (e.g., 6 for 6 months) |
| `months_to_average` | String | No | Comma-separated list of months to include in sales average calculation. Format: MM-YY (e.g., "05-25,06-25,07-25"). If omitted, all month columns in the file are used. |

#### Input File Format

Your Excel file should have the following structure:

| Products | [Month Columns] | Current Stock | SUPPLIER | LC |
|----------|----------------|---------------|----------|-----|
| SKU123 | Sales data... | 100 | Supplier Name | 12.50 |
| SKU456 | Sales data... | 50 | Supplier Name | 8.75 |

**Column Requirements:**
- **Products**: Product SKU/identifier
- **Month columns**: Datetime columns representing sales data for each month (e.g., 2025-05-01, 2025-06-01)
- **Current Stock**: Current inventory quantity
- **SUPPLIER**: Supplier name (must match `supplier_name` parameter exactly)
- **LC** (optional): Landed cost in USD

#### Output File

The API returns an Excel file with the following columns:

| Column | Description |
|--------|-------------|
| products | Product SKU |
| product_image | Excel IMAGE formula linking to product image URL |
| supplier | Supplier name |
| [Selected month columns] | Sales data for the months used in averaging |
| avg_monthly_sales | Average monthly sales across selected months |
| current stock | Current inventory level |
| target_stock | Target stock level (avg_monthly_sales × months_of_cover) |
| purchase_qty | Recommended purchase quantity (sorted descending) |
| lc_in_usd | Landed cost in USD (if LC column present in input) |
| lc_in_iqd | Landed cost in IQD (LC × 1550, if LC column present) |

**Formatting:**
- Row height: 100 pixels (to accommodate product images)
- Image column width: 25 units
- Sorted by `purchase_qty` in descending order (highest purchase needs first)

#### Response

**Success (200 OK)**
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- File download with name: `purchase_request_{supplier}_{months}months.xlsx`

**Error Responses**

| Status Code | Error Message | Cause |
|-------------|---------------|-------|
| 400 | "No file provided" | Missing file in request |
| 400 | "No file selected" | Empty filename |
| 400 | "supplier_name is required" | Missing supplier_name parameter |
| 400 | "months_of_cover is required" | Missing months_of_cover parameter |
| 400 | "months_of_cover must be an integer" | Invalid months_of_cover value |
| 404 | "Supplier not found in the inventory file" | supplier_name doesn't match any supplier in the file |
| 500 | Error details | Server error (check file format, column names, etc.) |

---

## Usage Examples

### Example 1: Using Postman

1. **Create a new POST request**
   - URL: `https://purchase-request-api-v3.onrender.com/generate_purchase_request`

2. **Set Body to form-data**
   - Key: `file`, Type: File, Value: Select your inventory Excel file
   - Key: `supplier_name`, Type: Text, Value: `شركة نوال - Newal - كرار`
   - Key: `months_of_cover`, Type: Text, Value: `6`
   - Key: `months_to_average`, Type: Text, Value: `05-25,06-25` (optional)

3. **Send the request**

4. **Save the response**
   - Click "Save Response" → "Save to a file"
   - Open the downloaded Excel file

### Example 2: Using cURL

**With specific months:**
```bash
curl -X POST \
  -F "file=@Shaghlaty_inventory_testing4.xlsx" \
  -F "supplier_name=شركة نوال - Newal - كرار" \
  -F "months_of_cover=6" \
  -F "months_to_average=05-25,06-25,07-25,08-25" \
  https://purchase-request-api-v3.onrender.com/generate_purchase_request \
  --output purchase_request.xlsx
```

**Using all available months:**
```bash
curl -X POST \
  -F "file=@Shaghlaty_inventory_testing4.xlsx" \
  -F "supplier_name=شركة نوال - Newal - كرار" \
  -F "months_of_cover=6" \
  https://purchase-request-api-v3.onrender.com/generate_purchase_request \
  --output purchase_request.xlsx
```

### Example 3: Using Python (requests library)

```python
import requests

url = "https://purchase-request-api-v3.onrender.com/generate_purchase_request"

files = {
    'file': open('Shaghlaty_inventory_testing4.xlsx', 'rb')
}

data = {
    'supplier_name': 'شركة نوال - Newal - كرار',
    'months_of_cover': '6',
    'months_to_average': '05-25,06-25,07-25,08-25'  # Optional
}

response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    with open('purchase_request.xlsx', 'wb') as f:
        f.write(response.content)
    print("Purchase request generated successfully!")
else:
    print(f"Error: {response.json()}")
```

### Example 4: Using JavaScript (fetch)

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('supplier_name', 'شركة نوال - Newal - كرار');
formData.append('months_of_cover', '6');
formData.append('months_to_average', '05-25,06-25,07-25,08-25');

fetch('https://purchase-request-api-v3.onrender.com/generate_purchase_request', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'purchase_request.xlsx';
    a.click();
})
.catch(error => console.error('Error:', error));
```

---

## Business Logic

### Calculation Method

1. **Average Monthly Sales**: 
   - Calculated from specified months (or all months if not specified)
   - Formula: `avg_monthly_sales = mean(selected_month_columns)`
   - Missing/NaN values are treated as 0

2. **Target Stock**:
   - Formula: `target_stock = avg_monthly_sales × months_of_cover`

3. **Shortfall**:
   - Formula: `shortfall = target_stock - current_stock`

4. **Purchase Quantity**:
   - Formula: `purchase_qty = ceiling(shortfall)` if shortfall > 0, else 0
   - Rounded up to nearest integer

5. **Landed Cost in IQD**:
   - Formula: `lc_in_iqd = lc_in_usd × 1550`
   - Exchange rate: 1 USD = 1550 IQD

### Product Images

Product images are embedded using Excel IMAGE formulas:
```
=IMAGE("https://ecomedia.shaghlaty.net/media/catalog/{SKU}.jpg")
```

Images will display in Excel when:
- Excel has internet connectivity
- The image URL is valid and accessible
- Excel version supports IMAGE function (Excel 365, Excel 2021+)

---

## Limitations

- **File Size**: Maximum upload size is 16 MB
- **File Format**: Only .xlsx files are supported
- **Column Names**: Must match expected format (case-insensitive)
- **Supplier Names**: Must match exactly (including spaces and special characters)
- **Month Format**: Datetime columns are automatically converted to MM-YY format

---

## Troubleshooting

### Images Don't Display in Excel
- Ensure you have internet connectivity
- Verify the product SKU matches the image filename on the server
- Check that you're using Excel 365 or Excel 2021+ (IMAGE function support)

### "Supplier not found" Error
- Copy the supplier name exactly from your inventory file
- Check for extra spaces or special characters
- Ensure the supplier name is case-sensitive match

### "Cannot convert non-finite values" Error
- This has been fixed in version 1.2
- Update to the latest version of the API

### Wrong Months Being Averaged
- Verify the month format is MM-YY (e.g., 05-25 for May 2025)
- Check that month columns in your file are datetime format
- Ensure comma separation with no spaces: `05-25,06-25` not `05-25, 06-25`

---

## Support

For issues or questions:
- Email: team@julius.ai
- Documentation: https://julius.ai/docs

---

## Changelog

### Version 1.2 (Current)
- Fixed datetime column handling for month selection
- Added support for LC (Landed Cost) columns
- Improved NaN and infinity value handling
- Added automatic datetime to MM-YY conversion

### Version 1.1
- Added LC in USD and LC in IQD columns
- Improved error handling

### Version 1.0
- Initial release
- Basic purchase request generation
- Product image formulas
- Configurable months of coverage
