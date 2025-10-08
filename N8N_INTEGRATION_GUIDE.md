# Integrating Shaghlaty Purchase Request API with n8n

## Quick Start Guide

n8n is a workflow automation tool that can call your API and process results automatically.

---

## Step-by-Step Setup

### 1. Create New Workflow in n8n

1. Log in to n8n.io (or your self-hosted instance)
2. Click **New Workflow**
3. Name it: "Shaghlaty Purchase Request Generator"

### 2. Add Trigger Node

Choose based on your needs:

**For Manual Testing:**
- Add **Manual Trigger** node

**For Scheduled Reports:**
- Add **Schedule Trigger** node
- Set frequency (e.g., every Monday at 9 AM)

**For External Systems:**
- Add **Webhook** node
- Method: POST
- Save the webhook URL

### 3. Add HTTP Request Node

Click + and add **HTTP Request** node

**Configuration:**

**Method:** POST

**URL:** 
```
https://purchase-request-api-v3.onrender.com/generate_purchase_request
```

**Authentication:** None

**Send Body:** Yes

**Body Content Type:** Form-Data (Multipart)

**Body Parameters:**

Add these 4 parameters:

1. **file**
   - Type: n8n Binary File
   - Input Data Field Name: data

2. **supplier_name**
   - Type: String
   - Value: Your supplier name (e.g., شركة نوال - Newal - كرار)

3. **months_of_cover**
   - Type: String  
   - Value: 6

4. **months_to_average** (optional)
   - Type: String
   - Value: 05-25,06-25,07-25,08-25

**Options Tab:**
- Response Format: File
- Put Output in Field: data

### 4. Add File Input Node

**Before the HTTP Request node**, add one of these:

**Option A: Read Binary File**
- Node: Read Binary File
- File Path: /path/to/your/inventory.xlsx
- Property Name: data

**Option B: Google Drive**
- Node: Google Drive
- Operation: Download
- File ID: (your file ID)
- Binary Property: data

### 5. Add Output Node

**After the HTTP Request node**, add one of these:

**Option A: Save Locally**
- Node: Write Binary File
- File Path: /path/to/output/purchase_request.xlsx
- Binary Property: data

**Option B: Save to Google Drive**
- Node: Google Drive
- Operation: Upload
- File Name: purchase_request.xlsx
- Binary Data: Yes
- Binary Property: data

**Option C: Email**
- Node: Gmail (or your email service)
- Attachments: data
- To: your-email@example.com
- Subject: Purchase Request Generated

**Option D: Slack**
- Node: Slack
- Operation: Send Message
- Channel: #procurement
- Attachments: data

---

## Complete Workflow Examples

### Example 1: Simple Manual Workflow

```
Manual Trigger 
  → Read Binary File (inventory.xlsx)
  → HTTP Request (call API)
  → Write Binary File (save result)
```

### Example 2: Automated Google Drive Workflow

```
Schedule Trigger (every Monday 9 AM)
  → Google Drive (download latest inventory)
  → HTTP Request (generate purchase request)
  → Google Drive (upload result)
  → Gmail (email to team)
```

### Example 3: Webhook for External Systems

```
Webhook (receive file upload)
  → HTTP Request (process file)
  → Slack (notify completion)
```

### Example 4: Multi-Supplier Processing

```
Manual Trigger
  → Read Binary File (inventory)
  → Split In Batches (for each supplier)
    → HTTP Request (generate for supplier)
    → Google Drive (save file)
  → Slack (notify all complete)
```

---

## HTTP Request Node Details

### Request Settings

```
Method: POST
URL: https://purchase-request-api-v3.onrender.com/generate_purchase_request
Authentication: None
Send Body: Yes
Body Content Type: Form-Data (Multipart)
```

### Form-Data Parameters

| Parameter Name | Type | Example Value |
|----------------|------|---------------|
| file | n8n Binary File (data) | (binary from previous node) |
| supplier_name | String | شركة نوال - Newal - كرار |
| months_of_cover | String | 6 |
| months_to_average | String | 05-25,06-25,07-25,08-25 |

### Options

```
Response Format: File
Put Output in Field: data
```

---

## Using Variables

Instead of hardcoding values, use n8n expressions:

**From previous node:**
```
supplier_name: {{ $json.supplier_name }}
months_of_cover: {{ $json.months_of_cover }}
months_to_average: {{ $json.months_to_average }}
```

**From webhook:**
```
supplier_name: {{ $json.body.supplier_name }}
```

**Dynamic filename:**
```
purchase_request_{{ $now.format('YYYY-MM-DD') }}.xlsx
```

---

## Testing Your Workflow

1. Click **Execute Workflow** button
2. Check each node output (click on node)
3. Verify binary data appears in HTTP Request output
4. Check final node has the Excel file
5. Download and verify the file

---

## Troubleshooting

### Error: Binary data not found
**Fix:** Ensure previous node outputs binary with property name 'data'

### Error: File parameter missing  
**Fix:** Set file parameter type to 'n8n Binary File', not 'String'

### Error: Supplier not found
**Fix:** Copy exact supplier name from inventory file (including Arabic characters)

### Error: Response is not a file
**Fix:** In HTTP Request Options, set Response Format to 'File'

### Error: Cannot convert non-finite values
**Fix:** Ensure you're using API version 1.2 (already deployed)

---

## Advanced: Error Handling

Add IF node after HTTP Request:

```
HTTP Request
  → IF (check for errors)
    → TRUE path: Save File → Notify Success
    → FALSE path: Slack Error → Stop
```

**IF Condition:**
- Value 1: {{ $json.error }}
- Operation: Is Empty

---

## Webhook Testing

If using webhook trigger, test with cURL:

```bash
curl -X POST https://your-n8n.app.n8n.cloud/webhook/shaghlaty \
  -F "file=@inventory.xlsx" \
  -F "supplier_name=شركة نوال - Newal - كرار" \
  -F "months_of_cover=6" \
  -F "months_to_average=05-25,06-25"
```

---

## Integration Ideas

### With Airtable
Store request history and metadata

### With Notion  
Create pages with embedded reports

### With Microsoft Teams
Send reports to Teams channels

### With Dropbox
Archive all purchase requests

### With Google Sheets
Log all generated requests

---

## Best Practices

1. **Use Set node** before HTTP Request to organize parameters
2. **Add error handling** with IF nodes
3. **Log executions** to Google Sheets or Airtable
4. **Send notifications** on success/failure
5. **Use variables** instead of hardcoded values
6. **Test thoroughly** before automating

---

## Resources

- n8n Documentation: https://docs.n8n.io
- n8n Community: https://community.n8n.io
- Your API Docs: See API_DOCUMENTATION.md

---

## Need Help?

- n8n Support: https://n8n.io/support
- API Support: team@julius.ai
