---
name: extract-multi-invoice-data
description: Extract structured data from multiple invoice files in a single API call using an array schema.
---

# Extract Multi-Invoice Data

Accounts payable teams and finance platforms use this recipe to process many invoices at once. Pass multiple invoice files and define an array schema to extract each invoice's vendor, date, line items, and total — ready for import into your accounting system.

## APIs Used

Document Extraction (1 credit per page)

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## Implementation


```bash
curl -X POST https://api.iterationlayer.com/document-extraction/v1/extract \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {
        "type": "url",
        "name": "invoice-acme.pdf",
        "url": "https://example.com/invoices/invoice-acme.pdf"
      },
      {
        "type": "url",
        "name": "invoice-global-freight.pdf",
        "url": "https://example.com/invoices/invoice-global-freight.pdf"
      }
    ],
    "schema": {
      "fields": [
        {
          "name": "invoices",
          "type": "ARRAY",
          "description": "One entry per invoice file",
          "fields": [
            {
              "name": "vendor_name",
              "type": "TEXT",
              "description": "Vendor or supplier name"
            },
            {
              "name": "invoice_number",
              "type": "TEXT",
              "description": "Invoice reference number"
            },
            {
              "name": "invoice_date",
              "type": "DATE",
              "description": "Invoice date"
            },
            {
              "name": "line_items",
              "type": "ARRAY",
              "description": "Individual line items",
              "fields": [
                {
                  "name": "description",
                  "type": "TEXT",
                  "description": "Item description"
                },
                {
                  "name": "quantity",
                  "type": "TEXT",
                  "description": "Quantity ordered"
                },
                {
                  "name": "amount",
                  "type": "CURRENCY_AMOUNT",
                  "description": "Line item amount"
                }
              ]
            },
            {
              "name": "total_amount",
              "type": "CURRENCY_AMOUNT",
              "description": "Total invoice amount"
            }
          ]
        }
      ]
    }
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });

const result = await client.extractDocument({
  files: [
    {
      type: "url",
      name: "invoice-acme.pdf",
      url: "https://example.com/invoices/invoice-acme.pdf",
    },
    {
      type: "url",
      name: "invoice-global-freight.pdf",
      url: "https://example.com/invoices/invoice-global-freight.pdf",
    },
  ],
  schema: {
    fields: [
      {
        name: "invoices",
        type: "ARRAY",
        description: "One entry per invoice file",
        fields: [
          {
            name: "vendor_name",
            type: "TEXT",
            description: "Vendor or supplier name",
          },
          {
            name: "invoice_number",
            type: "TEXT",
            description: "Invoice reference number",
          },
          {
            name: "invoice_date",
            type: "DATE",
            description: "Invoice date",
          },
          {
            name: "line_items",
            type: "ARRAY",
            description: "Individual line items",
            fields: [
              {
                name: "description",
                type: "TEXT",
                description: "Item description",
              },
              {
                name: "quantity",
                type: "TEXT",
                description: "Quantity ordered",
              },
              {
                name: "amount",
                type: "CURRENCY_AMOUNT",
                description: "Line item amount",
              },
            ],
          },
          {
            name: "total_amount",
            type: "CURRENCY_AMOUNT",
            description: "Total invoice amount",
          },
        ],
      },
    ],
  },
});
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")

result = client.extract_document(
    files=[
        {
            "type": "url",
            "name": "invoice-acme.pdf",
            "url": "https://example.com/invoices/invoice-acme.pdf",
        },
        {
            "type": "url",
            "name": "invoice-global-freight.pdf",
            "url": "https://example.com/invoices/invoice-global-freight.pdf",
        },
    ],
    schema={
        "fields": [
            {
                "name": "invoices",
                "type": "ARRAY",
                "description": "One entry per invoice file",
                "fields": [
                    {
                        "name": "vendor_name",
                        "type": "TEXT",
                        "description": "Vendor or supplier name",
                    },
                    {
                        "name": "invoice_number",
                        "type": "TEXT",
                        "description": "Invoice reference number",
                    },
                    {
                        "name": "invoice_date",
                        "type": "DATE",
                        "description": "Invoice date",
                    },
                    {
                        "name": "line_items",
                        "type": "ARRAY",
                        "description": "Individual line items",
                        "fields": [
                            {
                                "name": "description",
                                "type": "TEXT",
                                "description": "Item description",
                            },
                            {
                                "name": "quantity",
                                "type": "TEXT",
                                "description": "Quantity ordered",
                            },
                            {
                                "name": "amount",
                                "type": "CURRENCY_AMOUNT",
                                "description": "Line item amount",
                            },
                        ],
                    },
                    {
                        "name": "total_amount",
                        "type": "CURRENCY_AMOUNT",
                        "description": "Total invoice amount",
                    },
                ],
            },
        ]
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
				Name: "invoice-acme.pdf",
				Url: "https://example.com/invoices/invoice-acme.pdf",
			},
			il.FileInput{
				Type: "url",
				Name: "invoice-global-freight.pdf",
				Url: "https://example.com/invoices/invoice-global-freight.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.ArrayFieldConfig{
					Name: "invoices",
					Type: "ARRAY",
					Description: "One entry per invoice file",
					Fields: []any{
						il.TextFieldConfig{
							Name: "vendor_name",
							Type: "TEXT",
							Description: "Vendor or supplier name",
						},
						il.TextFieldConfig{
							Name: "invoice_number",
							Type: "TEXT",
							Description: "Invoice reference number",
						},
						il.DateFieldConfig{
							Name: "invoice_date",
							Type: "DATE",
							Description: "Invoice date",
						},
						il.ArrayFieldConfig{
							Name: "line_items",
							Type: "ARRAY",
							Description: "Individual line items",
							Fields: []any{
								il.TextFieldConfig{
									Name: "description",
									Type: "TEXT",
									Description: "Item description",
								},
								il.TextFieldConfig{
									Name: "quantity",
									Type: "TEXT",
									Description: "Quantity ordered",
								},
								il.CurrencyAmountFieldConfig{
									Name: "amount",
									Type: "CURRENCY_AMOUNT",
									Description: "Line item amount",
								},
							},
						},
						il.CurrencyAmountFieldConfig{
							Name: "total_amount",
							Type: "CURRENCY_AMOUNT",
							Description: "Total invoice amount",
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
  "name": "Extract Multi-Invoice Data",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract Multi-Invoice Data\n\nAccounts payable teams and finance platforms use this recipe to process many invoices at once. Pass multiple invoice files and define an array schema to extract each invoice's vendor, date, line items, and total \u2014 ready for import into your accounting system.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
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
      "id": "88ebde32-f53e-4b9a-bc00-b0ad32f1c536",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Extract Data\nResource: **Document Extraction**\n\nConfigure the Document Extraction parameters below, then connect your credentials.",
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
      "id": "08ca77ff-edfb-4300-b612-ef2c7a851ff1",
      "name": "Step 1 Note"
    },
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        250,
        300
      ],
      "id": "a3b4c5d6-e7f8-9012-abcd-123456789abc",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\"fields\":[{\"name\":\"invoices\",\"type\":\"ARRAY\",\"description\":\"One entry per invoice file\",\"fields\":[{\"name\":\"vendor_name\",\"type\":\"TEXT\",\"description\":\"Vendor or supplier name\"},{\"name\":\"invoice_number\",\"type\":\"TEXT\",\"description\":\"Invoice reference number\"},{\"name\":\"invoice_date\",\"type\":\"DATE\",\"description\":\"Invoice date\"},{\"name\":\"line_items\",\"type\":\"ARRAY\",\"description\":\"Individual line items\",\"fields\":[{\"name\":\"description\",\"type\":\"TEXT\",\"description\":\"Item description\"},{\"name\":\"quantity\",\"type\":\"TEXT\",\"description\":\"Quantity ordered\"},{\"name\":\"amount\",\"type\":\"CURRENCY_AMOUNT\",\"description\":\"Line item amount\"}]},{\"name\":\"total_amount\",\"type\":\"CURRENCY_AMOUNT\",\"description\":\"Total invoice amount\"}]}]}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "invoice-acme.pdf",
              "fileUrl": "https://example.com/invoices/invoice-acme.pdf"
            },
            {
              "fileInputMode": "url",
              "fileName": "invoice-global-freight.pdf",
              "fileUrl": "https://example.com/invoices/invoice-global-freight.pdf"
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
      "id": "b4c5d6e7-f8a9-0123-bcde-234567890bcd",
      "name": "Extract Data",
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
            "node": "Extract Data",
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
Extract data from multiple invoices at [file URL 1] and [file URL 2]. Use the extract_document tool with these fields:

- invoices (ARRAY): One entry per invoice file, each with:
  - vendor_name (TEXT): Vendor or supplier name
  - invoice_number (TEXT): Invoice reference number
  - invoice_date (DATE): Invoice date
  - line_items (ARRAY): Each with description (TEXT), quantity (TEXT), amount (CURRENCY_AMOUNT)
  - total_amount (CURRENCY_AMOUNT): Total invoice amount
```

### Response


```json
{
  "success": true,
  "data": {
    "invoices": {
      "value": [
        {
          "vendor_name": {
            "value": "Alpine Office Supplies GmbH",
            "confidence": 0.97,
            "citations": ["Alpine Office Supplies GmbH"],
            "source": "invoice-acme.pdf"
          },
          "invoice_number": {
            "value": "INV-2026-0041",
            "confidence": 0.99,
            "citations": ["Invoice #INV-2026-0041"],
            "source": "invoice-acme.pdf"
          },
          "invoice_date": {
            "value": "2026-03-01",
            "confidence": 0.98,
            "citations": ["Date: March 1, 2026"],
            "source": "invoice-acme.pdf"
          },
          "line_items": {
            "value": [
              {
                "description": {
                  "value": "Ergonomic Desk Chair",
                  "confidence": 0.96,
                  "citations": ["Ergonomic Desk Chair"]
                },
                "quantity": {
                  "value": "2",
                  "confidence": 0.98,
                  "citations": ["Qty: 2"]
                },
                "amount": {
                  "value": {
                    "amount": "699.98",
                    "currency": "EUR"
                  },
                  "confidence": 0.97,
                  "citations": ["EUR 699.98"]
                }
              },
              {
                "description": {
                  "value": "Standing Desk Converter",
                  "confidence": 0.95,
                  "citations": ["Standing Desk Converter"]
                },
                "quantity": {
                  "value": "1",
                  "confidence": 0.99,
                  "citations": ["Qty: 1"]
                },
                "amount": {
                  "value": {
                    "amount": "189.00",
                    "currency": "EUR"
                  },
                  "confidence": 0.96,
                  "citations": ["EUR 189.00"]
                }
              }
            ],
            "confidence": 0.96,
            "citations": []
          },
          "total_amount": {
            "value": {
              "amount": "888.98",
              "currency": "EUR"
            },
            "confidence": 0.98,
            "citations": ["Total Due: EUR 888.98"],
            "source": "invoice-acme.pdf"
          }
        },
        {
          "vendor_name": {
            "value": "Global Freight Solutions",
            "confidence": 0.96,
            "citations": ["Global Freight Solutions"],
            "source": "invoice-global-freight.pdf"
          },
          "invoice_number": {
            "value": "GFS-90215",
            "confidence": 0.99,
            "citations": ["Invoice No. GFS-90215"],
            "source": "invoice-global-freight.pdf"
          },
          "invoice_date": {
            "value": "2026-03-03",
            "confidence": 0.97,
            "citations": ["Date: 03/03/2026"],
            "source": "invoice-global-freight.pdf"
          },
          "line_items": {
            "value": [
              {
                "description": {
                  "value": "Overnight Parcel Shipping (5 kg)",
                  "confidence": 0.94,
                  "citations": ["Overnight Parcel Shipping (5 kg)"]
                },
                "quantity": {
                  "value": "3",
                  "confidence": 0.98,
                  "citations": ["Qty: 3"]
                },
                "amount": {
                  "value": {
                    "amount": "134.85",
                    "currency": "EUR"
                  },
                  "confidence": 0.95,
                  "citations": ["EUR 134.85"]
                }
              },
              {
                "description": {
                  "value": "Pallet Freight (LTL, 200 kg)",
                  "confidence": 0.93,
                  "citations": ["Pallet Freight (LTL, 200 kg)"]
                },
                "quantity": {
                  "value": "1",
                  "confidence": 0.99,
                  "citations": ["Qty: 1"]
                },
                "amount": {
                  "value": {
                    "amount": "420.00",
                    "currency": "EUR"
                  },
                  "confidence": 0.96,
                  "citations": ["EUR 420.00"]
                }
              }
            ],
            "confidence": 0.95,
            "citations": []
          },
          "total_amount": {
            "value": {
              "amount": "554.85",
              "currency": "EUR"
            },
            "confidence": 0.97,
            "citations": ["Total: EUR 554.85"],
            "source": "invoice-global-freight.pdf"
          }
        }
      ],
      "confidence": 0.96,
      "citations": []
    }
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
