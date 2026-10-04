---
name: extract-kpi-data
description: Extract campaign or business KPIs from report documents — metrics, values, periods, and targets.
---

# Extract KPI Data

Marketing agencies, analytics teams, and finance departments use this recipe to extract performance metrics from campaign summaries or quarterly reports — pulling out KPIs like impressions, conversions, spend, and ROAS for dashboards and automated reporting.

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
        "name": "campaign-summary-q1.pdf",
        "url": "https://example.com/reports/campaign-summary-q1-2026.pdf"
      }
    ],
    "schema": {
      "fields": [
        {
          "name": "client_name",
          "type": "TEXT",
          "description": "Client or company name"
        },
        {
          "name": "report_period",
          "type": "TEXT",
          "description": "Reporting period, e.g. Q1 2026"
        },
        {
          "name": "total_impressions",
          "type": "INTEGER",
          "description": "Total ad impressions"
        },
        {
          "name": "total_clicks",
          "type": "INTEGER",
          "description": "Total ad clicks"
        },
        {
          "name": "click_through_rate",
          "type": "DECIMAL",
          "description": "Click-through rate as a percentage"
        },
        {
          "name": "total_conversions",
          "type": "INTEGER",
          "description": "Total conversions or leads generated"
        },
        {
          "name": "cost_per_conversion",
          "type": "CURRENCY_AMOUNT",
          "description": "Average cost per conversion"
        },
        {
          "name": "total_spend",
          "type": "CURRENCY_AMOUNT",
          "description": "Total advertising spend"
        },
        {
          "name": "return_on_ad_spend",
          "type": "DECIMAL",
          "description": "Return on ad spend ratio"
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
      name: "campaign-summary-q1.pdf",
      url: "https://example.com/reports/campaign-summary-q1-2026.pdf",
    },
  ],
  schema: {
    fields: [
      { name: "client_name", type: "TEXT", description: "Client or company name" },
      { name: "report_period", type: "TEXT", description: "Reporting period, e.g. Q1 2026" },
      { name: "total_impressions", type: "INTEGER", description: "Total ad impressions" },
      { name: "total_clicks", type: "INTEGER", description: "Total ad clicks" },
      { name: "click_through_rate", type: "DECIMAL", description: "Click-through rate as a percentage" },
      { name: "total_conversions", type: "INTEGER", description: "Total conversions or leads generated" },
      { name: "cost_per_conversion", type: "CURRENCY_AMOUNT", description: "Average cost per conversion" },
      { name: "total_spend", type: "CURRENCY_AMOUNT", description: "Total advertising spend" },
      { name: "return_on_ad_spend", type: "DECIMAL", description: "Return on ad spend ratio" },
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
            "name": "campaign-summary-q1.pdf",
            "url": "https://example.com/reports/campaign-summary-q1-2026.pdf",
        }
    ],
    schema={
        "fields": [
            {"name": "client_name", "type": "TEXT", "description": "Client or company name"},
            {"name": "report_period", "type": "TEXT", "description": "Reporting period, e.g. Q1 2026"},
            {"name": "total_impressions", "type": "INTEGER", "description": "Total ad impressions"},
            {"name": "total_clicks", "type": "INTEGER", "description": "Total ad clicks"},
            {"name": "click_through_rate", "type": "DECIMAL", "description": "Click-through rate as a percentage"},
            {"name": "total_conversions", "type": "INTEGER", "description": "Total conversions or leads generated"},
            {"name": "cost_per_conversion", "type": "CURRENCY_AMOUNT", "description": "Average cost per conversion"},
            {"name": "total_spend", "type": "CURRENCY_AMOUNT", "description": "Total advertising spend"},
            {"name": "return_on_ad_spend", "type": "DECIMAL", "description": "Return on ad spend ratio"},
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
				Name: "campaign-summary-q1.pdf",
				Url: "https://example.com/reports/campaign-summary-q1-2026.pdf",
			},
		},
		Schema: il.ExtractionSchema{
			Fields: []any{
				il.TextFieldConfig{
					Name: "client_name",
					Type: "TEXT",
					Description: "Client or company name",
				},
				il.TextFieldConfig{
					Name: "report_period",
					Type: "TEXT",
					Description: "Reporting period, e.g. Q1 2026",
				},
				il.IntegerFieldConfig{
					Name: "total_impressions",
					Type: "INTEGER",
					Description: "Total ad impressions",
				},
				il.IntegerFieldConfig{
					Name: "total_clicks",
					Type: "INTEGER",
					Description: "Total ad clicks",
				},
				il.DecimalFieldConfig{
					Name: "click_through_rate",
					Type: "DECIMAL",
					Description: "Click-through rate as a percentage",
				},
				il.IntegerFieldConfig{
					Name: "total_conversions",
					Type: "INTEGER",
					Description: "Total conversions or leads generated",
				},
				il.CurrencyAmountFieldConfig{
					Name: "cost_per_conversion",
					Type: "CURRENCY_AMOUNT",
					Description: "Average cost per conversion",
				},
				il.CurrencyAmountFieldConfig{
					Name: "total_spend",
					Type: "CURRENCY_AMOUNT",
					Description: "Total advertising spend",
				},
				il.DecimalFieldConfig{
					Name: "return_on_ad_spend",
					Type: "DECIMAL",
					Description: "Return on ad spend ratio",
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
  "name": "Extract KPI data in Iteration Layer",
  "nodes": [
    {
      "parameters": {
        "content": "## Extract KPI Data\n\nMarketing agencies, analytics teams, and finance departments use this recipe to extract performance metrics from campaign summaries or quarterly reports — pulling out KPIs like impressions, conversions, spend, and ROAS for dashboards and automated reporting.\n\n**Note:** This workflow uses the Iteration Layer community node (`n8n-nodes-iterationlayer`). Install it via Settings > Community Nodes on self-hosted n8n, or add it directly on n8n Cloud with Verified Community Nodes enabled.",
        "height": 280,
        "width": 500,
        "color": 2
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [200, 40],
      "id": "e2f3a4b5-c6d7-8901-efab-678901234501",
      "name": "Overview"
    },
    {
      "parameters": {
        "content": "### Step 1: Extract KPI Data\nResource: **Document Extraction**\n\nConfigure the Document Extraction parameters below, then connect your credentials.",
        "height": 160,
        "width": 300,
        "color": 6
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [475, 100],
      "id": "e2f3a4b5-c6d7-8901-efab-678901234502",
      "name": "Step 1 Note"
    },
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [250, 300],
      "id": "e2f3a4b5-c6d7-8901-efab-678901234503",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "resource": "documentExtraction",
        "schemaInputMode": "rawJson",
        "schemaJson": "{\"fields\":[{\"name\":\"client_name\",\"type\":\"TEXT\",\"description\":\"Client or company name\"},{\"name\":\"report_period\",\"type\":\"TEXT\",\"description\":\"Reporting period\"},{\"name\":\"total_impressions\",\"type\":\"INTEGER\",\"description\":\"Total ad impressions\"},{\"name\":\"total_clicks\",\"type\":\"INTEGER\",\"description\":\"Total ad clicks\"},{\"name\":\"click_through_rate\",\"type\":\"DECIMAL\",\"description\":\"Click-through rate as a percentage\"},{\"name\":\"total_conversions\",\"type\":\"INTEGER\",\"description\":\"Total conversions or leads generated\"},{\"name\":\"cost_per_conversion\",\"type\":\"CURRENCY_AMOUNT\",\"description\":\"Average cost per conversion\"},{\"name\":\"total_spend\",\"type\":\"CURRENCY_AMOUNT\",\"description\":\"Total advertising spend\"},{\"name\":\"return_on_ad_spend\",\"type\":\"DECIMAL\",\"description\":\"Return on ad spend ratio\"}]}",
        "files": {
          "fileValues": [
            {
              "fileInputMode": "url",
              "fileName": "campaign-summary-q1.pdf",
              "fileUrl": "https://example.com/reports/campaign-summary-q1-2026.pdf"
            }
          ]
        }
      },
      "type": "n8n-nodes-iterationlayer.iterationLayer",
      "typeVersion": 1,
      "position": [500, 300],
      "id": "e2f3a4b5-c6d7-8901-efab-678901234504",
      "name": "Extract KPI Data",
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
            "node": "Extract KPI Data",
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
Extract KPI data from the file at [file URL]. Use the extract_document tool with these fields:

- client_name (TEXT): Client or company name
- report_period (TEXT): Reporting period, e.g. Q1 2026
- total_impressions (INTEGER): Total ad impressions
- total_clicks (INTEGER): Total ad clicks
- click_through_rate (DECIMAL): Click-through rate as a percentage
- total_conversions (INTEGER): Total conversions or leads generated
- cost_per_conversion (CURRENCY_AMOUNT): Average cost per conversion
- total_spend (CURRENCY_AMOUNT): Total advertising spend
- return_on_ad_spend (DECIMAL): Return on ad spend ratio
```

### Response


```json
{
  "success": true,
  "data": {
    "client_name": {
      "value": "Greenfield Organics",
      "confidence": 0.99,
      "citations": ["Client: Greenfield Organics"]
    },
    "report_period": {
      "value": "Q1 2026",
      "confidence": 0.99,
      "citations": ["Reporting Period: Q1 2026 (January — March)"]
    },
    "total_impressions": {
      "value": 1245800,
      "confidence": 0.98,
      "citations": ["Total Impressions: 1,245,800"]
    },
    "total_clicks": {
      "value": 37420,
      "confidence": 0.98,
      "citations": ["Total Clicks: 37,420"]
    },
    "click_through_rate": {
      "value": 3.0,
      "confidence": 0.97,
      "citations": ["CTR: 3.00%"]
    },
    "total_conversions": {
      "value": 1870,
      "confidence": 0.98,
      "citations": ["Total Conversions: 1,870"]
    },
    "cost_per_conversion": {
      "value": {
        "amount": "12.45",
        "currency": "EUR"
      },
      "confidence": 0.97,
      "citations": ["Cost per Conversion: EUR 12.45"]
    },
    "total_spend": {
      "value": {
        "amount": "23281.50",
        "currency": "EUR"
      },
      "confidence": 0.98,
      "citations": ["Total Spend: EUR 23,281.50"]
    },
    "return_on_ad_spend": {
      "value": 4.2,
      "confidence": 0.96,
      "citations": ["ROAS: 4.2x"]
    }
  }
}
```


## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse all recipes](https://iterationlayer.com/recipes)
