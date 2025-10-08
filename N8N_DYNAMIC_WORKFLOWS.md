# n8n Dynamic Workflows - Interactive & Multi-Supplier

## Workflow 1: Ask for Input Each Time (Interactive)

This workflow prompts you for supplier details every time you run it.

### Nodes Setup:
1. Manual Trigger
2. Set (input fields)
3. Read Binary File
4. HTTP Request
5. Save Result

### Step-by-Step Configuration:

**Node 1: Manual Trigger**
- Just add it, no config needed

**Node 2: Set Node**
- Click Add Value → String (repeat 4 times)

Add these fields:
- Name: supplier_name | Value: (empty)
- Name: months_of_cover | Value: (empty)
- Name: months_to_average | Value: (empty)
- Name: file_path | Value: (empty)

**Node 3: Read Binary File**
- File Path: {{ $json.file_path }}
- Property Name: data

**Node 4: HTTP Request**
- Method: POST
- URL: https://purchase-request-api-v3.onrender.com/generate_purchase_request
- Send Body: Yes
- Body Content Type: Form-Data (Multipart)

Form Parameters:
- file: n8n Binary File (data)
- supplier_name: {{ $json.supplier_name }}
- months_of_cover: {{ $json.months_of_cover }}
- months_to_average: {{ $json.months_to_average }}

Options:
- Response Format: File
- Put Output in Field: data

**Node 5: Write Binary File**
- File Path: /output/purchase_{{ $now.format('YYYY-MM-DD') }}.xlsx
- Binary Property: data

### How to Use:
1. Click Execute Workflow
2. In Set node, enter your values
3. Click Execute
4. File is generated!

---

## Workflow 2: Multi-Supplier Batch (Process Multiple at Once)

This processes multiple suppliers from one inventory file in a single run.

### Nodes Setup:
1. Manual Trigger
2. Code (suppliers list)
3. Read Binary File
4. Merge
5. Split In Batches
6. HTTP Request
7. Google Drive
8. (Loop back to Split In Batches)

### Step-by-Step Configuration:

**Node 1: Manual Trigger**
- Add it

**Node 2: Code Node**

JavaScript code:
```
return [
  {
    json: {
      supplier_name: 'شركة نوال - Newal - كرار',
      months_of_cover: '6',
      months_to_average: '05-25,06-25,07-25,08-25'
    }
  },
  {
    json: {
      supplier_name: 'Another Supplier',
      months_of_cover: '3',
      months_to_average: '06-25,07-25,08-25'
    }
  },
  {
    json: {
      supplier_name: 'Third Supplier',
      months_of_cover: '12',
      months_to_average: '05-25,06-25'
    }
  }
];
```

**Node 3: Read Binary File**
- File Path: /path/to/Shaghlaty_inventory_testing4.xlsx
- Property Name: data

**Node 4: Merge**
- Mode: Combine
- Combine By: Merge By Position
- Input 1: Code node (suppliers)
- Input 2: Read Binary File (inventory)

**Node 5: Split In Batches**
- Batch Size: 1
- Options → Reset: Yes

**Node 6: HTTP Request**
- Method: POST
- URL: https://purchase-request-api-v3.onrender.com/generate_purchase_request
- Send Body: Yes
- Body Content Type: Form-Data (Multipart)

Form Parameters:
- file: n8n Binary File (data)
- supplier_name: {{ $json.supplier_name }}
- months_of_cover: {{ $json.months_of_cover }}
- months_to_average: {{ $json.months_to_average }}

Options:
- Response Format: File
- Put Output in Field: data

**Node 7: Google Drive**
- Operation: Upload
- File Name: purchase_{{ $json.supplier_name }}_{{ $now.format('YYYY-MM-DD') }}.xlsx
- Binary Data: Yes
- Binary Property: data
- Parent Folder: (select folder)

**Connect back to Split In Batches:**
- Drag from Google Drive output to Split In Batches input
- This creates the loop

### How to Use:
1. Edit the Code node with your suppliers
2. Update file path in Read Binary File
3. Click Execute Workflow
4. All suppliers are processed automatically!
5. Files saved to Google Drive

---

## Workflow 3: Google Sheets Input (Best for Teams)

Use Google Sheets to manage suppliers - anyone can add/edit suppliers.

### Google Sheet Format:

Create a sheet with these columns:
| Supplier Name | Months of Cover | Months to Average |
|---------------|-----------------|-------------------|
| شركة نوال - Newal - كرار | 6 | 05-25,06-25,07-25,08-25 |
| Another Supplier | 3 | 06-25,07-25 |

### Nodes Setup:
1. Manual Trigger (or Schedule)
2. Google Sheets (read)
3. Read Binary File
4. Merge
5. Split In Batches
6. HTTP Request
7. Google Drive
8. (Loop back)

### Configuration:

**Node 2: Google Sheets**
- Operation: Get Many
- Document: (your sheet)
- Sheet: Sheet1
- Range: A2:C100
- Return All: Yes

**Rest same as Workflow 2**, but data comes from Google Sheets instead of Code node.

### Benefits:
- Team members can add suppliers without touching n8n
- Easy to manage
- Can schedule to run automatically

---

## Workflow 4: Web Form (For Non-Technical Users)

Create a simple web form where anyone can generate purchase requests.

### Nodes Setup:
1. Webhook
2. HTTP Request
3. Respond to Webhook

### Configuration:

**Node 1: Webhook**
- HTTP Method: POST
- Path: shaghlaty-form
- Response Mode: When Last Node Finishes
- Options → Binary Data: Yes

**Node 2: HTTP Request**
- Method: POST
- URL: https://purchase-request-api-v3.onrender.com/generate_purchase_request
- Body Content Type: Form-Data (Multipart)

Form Parameters:
- file: n8n Binary File (data)
- supplier_name: {{ $json.body.supplier_name }}
- months_of_cover: {{ $json.body.months_of_cover }}
- months_to_average: {{ $json.body.months_to_average }}

Options:
- Response Format: File

**Node 3: Respond to Webhook**
- Respond With: Binary File
- Property Name: data

### HTML Form:

Save this as shaghlaty_form.html and host it:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Purchase Request Generator</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #4CAF50; color: white; padding: 10px 20px; border: none; 
                 border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background: #45a049; }
    </style>
</head>
<body>
    <h1>Generate Purchase Request</h1>
    <form id="form" enctype="multipart/form-data">
        <div class="form-group">
            <label>Inventory File:</label>
            <input type="file" name="file" accept=".xlsx" required>
        </div>
        <div class="form-group">
            <label>Supplier Name:</label>
            <input type="text" name="supplier_name" required>
        </div>
        <div class="form-group">
            <label>Months of Cover:</label>
            <input type="number" name="months_of_cover" value="6" required>
        </div>
        <div class="form-group">
            <label>Months to Average (optional):</label>
            <input type="text" name="months_to_average" placeholder="05-25,06-25">
        </div>
        <button type="submit">Generate</button>
    </form>
    <div id="status"></div>

    <script>
        document.getElementById('form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const status = document.getElementById('status');
            status.innerHTML = 'Generating...';
            
            try {
                const response = await fetch('YOUR_WEBHOOK_URL_HERE', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'purchase_request.xlsx';
                    a.click();
                    status.innerHTML = 'Success!';
                } else {
                    status.innerHTML = 'Error: ' + await response.text();
                }
            } catch (error) {
                status.innerHTML = 'Error: ' + error.message;
            }
        });
    </script>
</body>
</html>
```

Replace YOUR_WEBHOOK_URL_HERE with your n8n webhook URL.

---

## Quick Comparison

| Workflow | Best For | Complexity |
|----------|----------|------------|
| Interactive (Set node) | Quick one-off requests | Easy |
| Multi-Supplier (Code) | Fixed list of suppliers | Medium |
| Google Sheets | Team collaboration | Medium |
| Web Form | Non-technical users | Advanced |

---

## Tips

**For Interactive Workflow:**
- Save common values in Set node as defaults
- Use dropdown for supplier names if you want

**For Multi-Supplier:**
- Start with 2-3 suppliers to test
- Check each file before processing all
- Add error handling with IF node

**For Google Sheets:**
- Add a Status column to track progress
- Use n8n to update status after each supplier
- Schedule to run daily/weekly

**For Web Form:**
- Host on Netlify, Vercel, or GitHub Pages (free)
- Add authentication if needed
- Style it to match your brand

---

## Next Steps

1. Choose the workflow that fits your needs
2. Build it in n8n following the steps
3. Test with one supplier first
4. Scale up to multiple suppliers
5. Automate with schedules if needed

