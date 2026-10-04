---
name: invoice-to-pdf-report
description: Extract invoice data and generate a formatted PDF summary in a single pipeline.
---

# Invoice to PDF Report

Finance teams and invoice processing platforms use this recipe to automate the extract-to-report pipeline. Upload an invoice, extract structured data with confidence scores, and generate a branded PDF summary — all through two API calls.

## APIs Used

Document Extraction (1 credit per page), Document Generation (1 credits/request)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
# Step 1: Extract invoice data
EXTRACTION=$(curl -s -X POST https://api.iterationlayer.com/document-extraction/v1/extract \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {
        "type": "url",
        "name": "invoice-2026-0412.pdf",
        "url": "https://example.com/invoices/invoice-2026-0412.pdf"
      }
    ],
    "schema": {
      "fields": [
        { "name": "invoice_number", "type": "TEXT", "description": "Invoice number or identifier" },
        { "name": "vendor_name", "type": "TEXT", "description": "Name of the vendor or supplier" },
        { "name": "invoice_date", "type": "DATE", "description": "Date the invoice was issued" },
        { "name": "total_amount", "type": "CURRENCY_AMOUNT", "description": "Total amount due on the invoice" },
        {
          "name": "line_items",
          "type": "ARRAY",
          "description": "Individual line items on the invoice",
          "fields": [
            { "name": "item_description", "type": "TEXT", "description": "Description of the item or service" },
            { "name": "amount", "type": "CURRENCY_AMOUNT", "description": "Amount for this line item" }
          ]
        }
      ]
    }
  }')

# Step 2: Generate a PDF report from the extracted invoice data
curl -X POST https://api.iterationlayer.com/document-generation/v1/generate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "format": "pdf",
    "document": {
      "metadata": {
        "title": "Invoice Summary — INV-2026-0412",
        "author": "Accounts Payable"
      },
      "page": {
        "size": { "preset": "A4" },
        "margins": {
          "top_in_pt": 54,
          "right_in_pt": 54,
          "bottom_in_pt": 54,
          "left_in_pt": 54
        }
      },
      "content": [
        { "type": "headline", "level": "h1", "text": "Invoice Summary — INV-2026-0412" },
        {
          "type": "paragraph",
          "runs": [
            { "text": "Vendor: ", "font_weight": "bold" },
            { "text": "Pinnacle Office Supplies Ltd.\n" },
            { "text": "Invoice Date: ", "font_weight": "bold" },
            { "text": "2026-03-28" }
          ]
        },
        { "type": "separator" },
        { "type": "headline", "level": "h2", "text": "Line Items" },
        {
          "type": "table",
          "headers": [
            { "text": "Description" },
            { "text": "Amount" }
          ],
          "rows": [
            [
              { "text": "A4 Copy Paper (10 reams)" },
              { "text": "$84.50" }
            ],
            [
              { "text": "Black Ink Cartridges (6-pack)" },
              { "text": "$137.94" }
            ],
            [
              { "text": "Ergonomic Desk Chair" },
              { "text": "$449.00" }
            ],
            [
              { "text": "Monitor Riser Stand" },
              { "text": "$62.00" }
            ]
          ]
        },
        { "type": "separator" },
        {
          "type": "paragraph",
          "runs": [
            { "text": "Total Amount Due: $733.44", "font_weight": "bold" }
          ]
        }
      ]
    }
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

// Step 1: Extract invoice data
const extraction = await client.extractDocument({
  files: [
    {
      type: "url",
      name: "invoice-2026-0412.pdf",
      url: "https://example.com/invoices/invoice-2026-0412.pdf",
    },
  ],
  schema: {
    fields: [
      {
        name: "invoice_number",
        type: "TEXT",
        description: "Invoice number or identifier",
      },
      {
        name: "vendor_name",
        type: "TEXT",
        description: "Name of the vendor or supplier",
      },
      {
        name: "invoice_date",
        type: "DATE",
        description: "Date the invoice was issued",
      },
      {
        name: "total_amount",
        type: "CURRENCY_AMOUNT",
        description: "Total amount due on the invoice",
      },
      {
        name: "line_items",
        type: "ARRAY",
        description: "Individual line items on the invoice",
        fields: [
          {
            name: "item_description",
            type: "TEXT",
            description: "Description of the item or service",
          },
          {
            name: "amount",
            type: "CURRENCY_AMOUNT",
            description: "Amount for this line item",
          },
        ],
      },
    ],
  },
});

const invoiceNumber = String(extraction["invoice_number"].value);
const vendorName = String(extraction["vendor_name"].value);
const invoiceDate = String(extraction["invoice_date"].value);
const totalAmount = String(extraction["total_amount"].value);
const lineItems = extraction["line_items"].value as Array<
  Record<string, { value: unknown }>
>;

// Step 2: Generate a PDF report from the extracted invoice data
const report = await client.generateDocument({
  format: "pdf",
  document: {
    metadata: {
      title: `Invoice Summary — ${invoiceNumber}`,
      author: "Accounts Payable",
    },
    page: {
      size: { preset: "A4" },
      margins: {
        top_in_pt: 54,
        right_in_pt: 54,
        bottom_in_pt: 54,
        left_in_pt: 54,
      },
    },
    content: [
      {
        type: "headline",
        level: "h1",
        text: `Invoice Summary — ${invoiceNumber}`,
      },
      {
        type: "paragraph",
        runs: [
          { text: "Vendor: ", font_weight: "bold" },
          { text: `${vendorName}\n` },
          { text: "Invoice Date: ", font_weight: "bold" },
          { text: invoiceDate },
        ],
      },
      { type: "separator" },
      { type: "headline", level: "h2", text: "Line Items" },
      {
        type: "table",
        headers: [{ text: "Description" }, { text: "Amount" }],
        rows: lineItems.map((item) => [
          { text: String(item["item_description"].value) },
          { text: String(item["amount"].value) },
        ]),
      },
      { type: "separator" },
      {
        type: "paragraph",
        runs: [
          { text: `Total Amount Due: ${totalAmount}`, font_weight: "bold" },
        ],
      },
    ],
  },
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

# Step 1: Extract invoice data
extraction = client.extract_document(
    files=[
        {
            "type": "url",
            "name": "invoice-2026-0412.pdf",
            "url": "https://example.com/invoices/invoice-2026-0412.pdf",
        }
    ],
    schema={
        "fields": [
            {"name": "invoice_number", "type": "TEXT", "description": "Invoice number or identifier"},
            {"name": "vendor_name", "type": "TEXT", "description": "Name of the vendor or supplier"},
            {"name": "invoice_date", "type": "DATE", "description": "Date the invoice was issued"},
            {"name": "total_amount", "type": "CURRENCY_AMOUNT", "description": "Total amount due on the invoice"},
            {
                "name": "line_items",
                "type": "ARRAY",
                "description": "Individual line items on the invoice",
                "fields": [
                    {"name": "item_description", "type": "TEXT", "description": "Description of the item or service"},
                    {"name": "amount", "type": "CURRENCY_AMOUNT", "description": "Amount for this line item"},
                ],
            },
        ]
    },
)

invoice_number = extraction["invoice_number"]["value"]
vendor_name = extraction["vendor_name"]["value"]
invoice_date = extraction["invoice_date"]["value"]
total_amount = extraction["total_amount"]["value"]
line_items = extraction["line_items"]["value"]

# Step 2: Generate a PDF report from the extracted invoice data
report = client.generate_document(
    format="pdf",
    document={
        "metadata": {
            "title": f"Invoice Summary — {invoice_number}",
            "author": "Accounts Payable",
        },
        "page": {
            "size": {"preset": "A4"},
            "margins": {
                "top_in_pt": 54,
                "right_in_pt": 54,
                "bottom_in_pt": 54,
                "left_in_pt": 54,
            },
        },
        "content": [
            {"type": "headline", "level": "h1", "text": f"Invoice Summary — {invoice_number}"},
            {
                "type": "paragraph",
                "runs": [
                    {"text": "Vendor: ", "font_weight": "bold"},
                    {"text": f"{vendor_name}\n"},
                    {"text": "Invoice Date: ", "font_weight": "bold"},
                    {"text": invoice_date},
                ],
            },
            {"type": "separator"},
            {"type": "headline", "level": "h2", "text": "Line Items"},
            {
                "type": "table",
                "headers": [
                    {"text": "Description"},
                    {"text": "Amount"},
                ],
                "rows": [
                    [
                        {"text": item["item_description"]["value"]},
                        {"text": str(item["amount"]["value"])},
                    ]
                    for item in line_items
                ],
            },
            {"type": "separator"},
            {
                "type": "paragraph",
                "runs": [{"text": f"Total Amount Due: {total_amount}", "font_weight": "bold"}],
            },
        ],
    },
)
```

```go
package main

import il "github.com/iterationlayer/sdk-go"

func main() {
	client := il.NewClient("YOUR_API_KEY")

	result, err := client.ExtractDocument(il.ExtractDocumentRequest{
		Files: []il.FileInput{
			il.FileInput{
				Type: "url",
				Name: "invoice-2026-0412.pdf",
				Url: "https://example.com/invoices/invoice-2026-0412.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "invoice_number",
					Type: "TEXT",
					Description: "Invoice number or identifier",
				},
				il.TextFieldConfig{
					Name: "vendor_name",
					Type: "TEXT",
					Description: "Name of the vendor or supplier",
				},
				il.DateFieldConfig{
					Name: "invoice_date",
					Type: "DATE",
					Description: "Date the invoice was issued",
				},
				il.CurrencyAmountFieldConfig{
					Name: "total_amount",
					Type: "CURRENCY_AMOUNT",
					Description: "Total amount due on the invoice",
				},
				il.ArrayFieldConfig{
					Name: "line_items",
					Type: "ARRAY",
					Description: "Individual line items on the invoice",
					Fields: []any{
						il.TextFieldConfig{
							Name: "item_description",
							Type: "TEXT",
							Description: "Description of the item or service",
						},
						il.CurrencyAmountFieldConfig{
							Name: "amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Amount for this line item",
						},
					},
				},
			},
		},
	})
	if err != nil {
		panic(err)
	}

	_ = result
}
```

```n8n
{
  "name": "Invoice to PDF Report",
  "nodes": [
    {
      "parameters": {
        "content": "## Invoice to PDF Report\n\nFinance teams and invoice processing platforms use this recipe to automate the extract-to-report pipeline. Upload an invoice, extract structured data with confidence scores, and generate a branded PDF summary \u2014 all through two API calls.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
        "height": 280,
        "width": 500,
        "color": 2
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        200,
        40
      ],
      "id": "cb1571ce-e625-45bf-9316-2617d43d6880",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Extract Invoice Data\nResource: **Document Extraction**\n\nConfigure the Document Extraction parameters below, then connect your credentials.",
        "height": 160,
        "width": 300,
        "color": 6
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        475,
        100
      ],
      "id": "f226bc1b-1ad5-4dad-9e7f-d4245823f4d4",
      "name": "Step 1 Note"
    },
    {
      "parameters": {
        "content": "### Step 2: Generate PDF Report\nResource: **Document Generation**\n\nConfigure the Document Generation parameters below, then connect your credentials.",
        "height": 160,
        "width": 300,
        "color": 6
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [
        725,
        100
      ],
      "id": "b2f28ece-0a45-4498-86de-232f2763fce4",
      "name": "Step 2 Note"
    },
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        250,
        300
      ],
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "[\n  {\n    \"name\": \"invoice_number\",\n    \"type\": \"TEXT\",\n    \"description\": \"The unique invoice identifier\"\n  },\n  {\n    \"name\": \"vendor_name\",\n    \"type\": \"TEXT\",\n    \"description\": \"Name of the vendor or supplier\"\n  },\n  {\n    \"name\": \"invoice_date\",\n    \"type\": \"DATE\",\n    \"description\": \"Date the invoice was issued\"\n  },\n  {\n    \"name\": \"line_items\",\n    \"type\": \"ARRAY\",\n    \"description\": \"List of line items on the invoice\",\n    \"children\": [\n      {\n        \"name\": \"item_description\",\n        \"type\": \"TEXT\",\n        \"description\": \"Description of the line item\"\n      },\n      {\n        \"name\": \"amount\",\n        \"type\": \"CURRENCY_AMOUNT\",\n        \"description\": \"Amount for this line item\"\n      }\n    ]\n  },\n  {\n    \"name\": \"total_amount\",\n    \"type\": \"CURRENCY_AMOUNT\",\n    \"description\": \"Total invoice amount\"\n  }\n]",
        "files": {
          "fileValues": [
            {
              "inputMode": "url",
              "fileUrl": "https://example.com/invoices/2026-001.pdf"
            }
          ]
        }
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        500,
        300
      ],
      "id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
      "name": "Extract Invoice Data",
      "credentials": {
        "iterationLayerApi": {
          "id": "1",
          "name": "Iteration Layer API"
        }
      }
    },
    {
      "parameters": {
        "resource": "documentGeneration",
        "format": "pdf",
        "documentJson": "{\n  \"pages\": [\n    {\n      \"width_in_pt\": 595,\n      \"height_in_pt\": 842,\n      \"blocks\": [\n        {\n          \"type\": \"paragraph\",\n          \"text\": \"Invoice Report\",\n          \"font_size_in_pt\": 28,\n          \"font_weight\": \"bold\",\n          \"color\": \"#1a1a1a\",\n          \"margin_top_in_pt\": 60,\n          \"margin_left_in_pt\": 50,\n          \"margin_right_in_pt\": 50\n        },\n        {\n          \"type\": \"paragraph\",\n          \"text\": \"Invoice #{{ $json.invoice_number }} \u2014 {{ $json.vendor_name }}\",\n          \"font_size_in_pt\": 14,\n          \"color\": \"#444444\",\n          \"margin_top_in_pt\": 20,\n          \"margin_left_in_pt\": 50,\n          \"margin_right_in_pt\": 50\n        },\n        {\n          \"type\": \"paragraph\",\n          \"text\": \"Date: {{ $json.invoice_date }}\",\n          \"font_size_in_pt\": 12,\n          \"color\": \"#666666\",\n          \"margin_top_in_pt\": 8,\n          \"margin_left_in_pt\": 50,\n          \"margin_right_in_pt\": 50\n        },\n        {\n          \"type\": \"table\",\n          \"margin_top_in_pt\": 30,\n          \"margin_left_in_pt\": 50,\n          \"margin_right_in_pt\": 50,\n          \"columns\": [\n            {\n              \"header\": \"Description\",\n              \"width_fraction\": 0.7\n            },\n            {\n              \"header\": \"Amount\",\n              \"width_fraction\": 0.3,\n              \"align\": \"right\"\n            }\n          ],\n          \"rows\": \"{{ $json.line_items }}\"\n        },\n        {\n          \"type\": \"paragraph\",\n          \"text\": \"Total: {{ $json.total_amount }}\",\n          \"font_size_in_pt\": 16,\n          \"font_weight\": \"bold\",\n          \"color\": \"#1a1a1a\",\n          \"margin_top_in_pt\": 20,\n          \"margin_left_in_pt\": 50,\n          \"margin_right_in_pt\": 50,\n          \"text_align\": \"right\"\n        }\n      ]\n    }\n  ]\n}"
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [
        750,
        300
      ],
      "id": "c3d4e5f6-a7b8-9012-cdef-345678901234",
      "name": "Generate PDF Report",
      "credentials": {
        "iterationLayerApi": {
          "id": "1",
          "name": "Iteration Layer API"
        }
      }
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [
        [
          {
            "node": "Extract Invoice Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract Invoice Data": {
      "main": [
        [
          {
            "node": "Generate PDF Report",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

```prompt
Extract data from the invoice at [file URL] using extract_document with fields for vendor name, invoice number, date, due date, line items (description, quantity, unit price, amount), subtotal, tax, and total. Then generate a formatted PDF summary using generate_document with the extracted data, including a header, invoice details, line items table, and totals.
```

### Response


```json
{
  "success": true,
  "data": {
    "buffer": "JVBERi0xLjQK...",
    "mime_type": "application/pdf"
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
