---
name: document-extraction-api
description: Extract structured data from documents using AI-powered field extraction.
---

# Document Extraction API

Extract structured data from documents using AI-powered field extraction.

**Cost:** 1 credit per page

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## API Reference

Extract structured data from any document with a single API call. Send one or more files and a schema defining the fields you need, and receive typed, validated results with confidence scores and source citations.

## Key Features

- **Multi-Format Support** — Extract from 40+ file formats: PDF, Office documents (DOCX, PPTX, ODT, ODS, XLSX), public website URLS, EPUB, LaTeX, email (EML), Jupyter notebooks, images, and text/markup formats.
- **Rich Field Types** — Primitive types (text, number, date, boolean, email, enum) plus purpose-built validated types: `IBAN` (validated against the standard format), `ADDRESS` (returns a structured object with street, city, region, postal code, and country), `CURRENCY_CODE` (normalized to ISO 4217), `CURRENCY_AMOUNT` (numeric monetary value), and `COUNTRY` (normalized to ISO 3166-1 alpha-2). These validated types mean you get clean, usable data — not raw strings you have to parse yourself.
- **Structured Arrays** — Extract repeating data like invoice line items with nested schemas.
- **Calculated Fields** — Define arithmetic operations (sum, subtract, multiply, divide) computed from other extracted fields.
- **Confidence Scores** — Every extracted value includes a confidence score between 0 and 1.
- **Source Citations** — Verbatim quotes from the document that support each extracted value.
- **Website Image Context** — Public website URL inputs include useful referenced images in the extraction context while skipping logos, tracking pixels, decorative graphics, and semantically unhelpful images.
- **Schema Validation** — Field schemas are validated before extraction, catching errors like circular dependencies or type mismatches early.

## Overview

The Document Extraction API analyzes documents and extracts structured data based on a schema you define. You send one or more files (base64 or URL) and a schema with field definitions, and receive a JSON response with typed values, confidence scores, and citations. Public website URLs are supported when you want website content included in a broader multi-file extraction.

**Endpoint:** `POST /document-extraction/v1/extract`

**Limits:**
- Max files per request: 20
- Max file size: 50 MB per file

## Supported File Formats

- **Documents:** PDF, DOCX, PPTX, ODT, EPUB, RTF
- **Spreadsheets:** XLSX, XLS, ODS, CSV, TSV
- **Email:** EML, MSG (headers, body, and attachment extraction — attachments are ingested and included in extraction context)
- **Notebooks:** Jupyter (.ipynb)
- **Academic & Publishing:** LaTeX (.tex, .latex), BibTeX (.bib), Typst (.typst, .typ)
- **Markup & Text:** HTML, Markdown, JSON, XML, YAML, TOML, RST, Org, Djot, MDX, TXT
- **Images:** PNG, JPEG, GIF, WebP, AVIF, HEIF, BMP, TIFF, JP2, PNM/PBM/PGM/PPM, SVG

## How It Works

Every extraction runs the same pipeline:

1. **Validate** — the schema is checked before any files are touched. Three things are validated: CALCULATED source field references (each must exist in the schema and be a numeric type), circular dependencies between CALCULATED fields, and default values matching their field type. The first failure stops validation with a descriptive error. No LLM call is made if the schema is invalid.
2. **Ingest** — files are converted to a normalized text representation.
3. **Extract** — each field is extracted according to its type and configuration. All non-CALCULATED fields are handled together, with all source files available during extraction. Every extracted value is tagged with the file it came from.
4. **Calculate** — CALCULATED fields are computed from the extraction results. Operations are pure arithmetic: `sum`, `subtract`, `multiply`, `divide`. The confidence of a CALCULATED field is the minimum confidence of its source fields. Division by zero returns `0`. The result is deterministic — if the source values are correct, the computed value is exact.
5. **Consolidate** — default values are applied to fields that were not extracted, and required field constraints are checked.

**Intelligent extraction** — the API automatically selects the best extraction approach based on the complexity of your schema and the nature of the documents. You don't configure this.

For a technical deep dive into the ingestion pipeline that runs before schema extraction, see [How Our Document Ingestion Pipeline Turns Files into LLM-Ready Markdown](/blog/how-our-document-ingestion-pipeline-works).

## Request Format

<!-- tabs -->

```bash
curl -X POST \
  https://api.iterationlayer.com/document-extraction/v1/extract \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {
        "type": "base64",
        "name": "invoice.pdf",
        "base64": "<base64-encoded-file>"
      }
    ],
    "schema": {
      "fields": [
        {
          "name": "invoice_number",
          "type": "TEXT",
          "description": "The invoice number"
        },
        {
          "name": "total_amount",
          "type": "CURRENCY_AMOUNT",
          "description": "Total invoice amount"
        }
      ]
    }
  }'
```

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({
  apiKey: "YOUR_API_KEY",
});

const result = await client.extractDocument({
  files: [
    {
      type: "base64",
      name: "invoice.pdf",
      base64: new Uint8Array([/* file bytes */]),
    },
  ],
  schema: {
    fields: [
      {
        name: "invoice_number",
        type: "TEXT",
        description: "The invoice number",
      },
      {
        name: "total_amount",
        type: "CURRENCY_AMOUNT",
        description: "Total invoice amount",
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
            "type": "base64",
            "name": "invoice.pdf",
            "base64": b"...",
        }
    ],
    schema={
        "fields": [
            {
                "name": "invoice_number",
                "type": "TEXT",
                "description": "The invoice number",
            },
            {
                "name": "total_amount",
                "type": "CURRENCY_AMOUNT",
                "description": "Total invoice amount",
            },
        ]
    },
)
```

```go
import il "github.com/iterationlayer/sdk-go"
client := il.NewClient("YOUR_API_KEY")

result, err := client.ExtractDocument(il.ExtractDocumentRequest{
	Files: []il.FileInput{
		il.FileInput{Type: "base64", Name: "invoice.pdf", Base64: []byte{ /* file bytes */ }},
	},
	Schema: il.ExtractionSchema{
		Fields: []any{
			il.TextFieldConfig{Type: "TEXT", Name: "invoice_number", Description: "The invoice number"},
			il.CurrencyAmountFieldConfig{Type: "CURRENCY_AMOUNT", Name: "total_amount", Description: "Total invoice amount"},
		},
	},
})
```

<!-- response -->

```json
{
  "success": true,
  "data": {
    "invoice_number": {
      "type": "TEXT",
      "value": "INV-2024-001",
      "confidence": 0.98,
      "citations": ["Invoice No: INV-2024-001"],
      "source": "invoice.pdf"
    },
    "total_amount": {
      "type": "CURRENCY_AMOUNT",
      "value": 1250.00,
      "confidence": 0.95,
      "citations": ["Total: €1,250.00"],
      "source": "invoice.pdf"
    }
  }
}
```

<!-- /tabs -->

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `files` | array | Yes | List of file inputs to extract from (see File Input below) |
| `schema` | object | Yes | Extraction schema defining the fields to extract |
| `webhook_url` | string | No | HTTPS URL to receive results asynchronously. If provided, returns 201 immediately. See [Webhooks](/docs/webhooks). |

### Async Mode

Add a `webhook_url` parameter to process the request in the background. The API returns `201 Accepted` immediately and delivers the result to your webhook URL when processing completes. See [Webhooks](/docs/webhooks) for payload format and retry behavior.

### File Input

Provide each file as either base64 or a URL:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | `"base64"` or `"url"` |
| `name` | string | Required for `base64`, optional for `url` | Filename with extension (e.g., `invoice.pdf`). URL inputs without a name may be resolved as website pages. |
| `base64` | string | If type is `base64` | Base64-encoded file content |
| `url` | string | If type is `url` | Publicly accessible HTTPS URL to fetch the file from. HTTP is not accepted. |
| `fetch_options` | object | No | Website retrieval options for URL inputs. Use only when the URL should be treated as a website page with explicit retrieval controls. |

For websites the API always checks the site's `robots.txt` before fetching the page. If the URL is disallowed for the effective `User-Agent`, the request fails with `400 Bad Request` and the page is not fetched. Sitemap entries in `robots.txt` are recorded as metadata only; they are not traversed.

Website URL fetches are rate-limited per destination host. The service automatically respects `robots.txt` crawl-delay hints, slows down after upstream `429 Too Many Requests` responses, and uses upstream `Retry-After` or rate-limit reset headers when provided. This protects public sites and may delay later requests to the same host; it is not configurable through `fetch_options`.

If a website URL fetch looks like a WAF or security challenge, the API automatically retries the same URL in an isolated Chromium browser session. Detection covers common Cloudflare, Akamai, AWS WAF/CloudFront, Imperva/Incapsula, DataDome, PerimeterX, Sucuri, F5/BIG-IP, hCaptcha, reCAPTCHA, and generic verification pages. Successful browser fallback is recorded under `metadata.security`; failed fallback returns `400 Bad Request` with a clear security-challenge message.

### Fetch Options

`fetch_options` lets you control retrieval behavior for a URL input treated as a website page. Robots compliance and per-host rate limiting are mandatory and are not configurable.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `locale` | string | No | BCP 47 locale tag sent as `Accept-Language` (e.g., `"en-US"`, `"de-DE"`, `"fr"`). |
| `user_agent` | string | No | Custom `User-Agent` header string (1–500 characters). |
| `auth` | object | No | Authentication for website URL inputs. Supports bearer tokens, HTTP Basic auth, and a custom auth header. Secret values are not returned in metadata. |
| `headers` | object | No | Additional request headers for website URL inputs. Header names and values are validated; unsafe headers such as `Cookie`, `Set-Cookie`, `Host`, `Content-Length`, hop-by-hop headers, and browser-controlled `Sec-*` headers are rejected. |
| `timeout_ms` | integer | No | Website fetch timeout in milliseconds. Must be between `1000` and `60000`. |
| `should_render_javascript` | boolean | No | Use Chromium browser rendering before extraction. Default: `false`. |

### Custom Headers

Custom headers are sent on direct fetches and, when JavaScript rendering is enabled or security-challenge fallback is needed, as Chromium request headers where supported by the browser. Each Chromium fetch uses an isolated browser context that is disposed after the request; cookies and session state are not persisted across URLs or requests.

Fetch options control retrieval behavior, not billing.

### Auth Examples

Use one auth shape per request.

```json
{ "auth": { "type": "bearer", "token": "..." } }
{ "auth": { "type": "basic", "username": "...", "password": "..." } }
{ "auth": { "type": "custom_header", "name": "x-api-key", "value": "..." } }
```

### URL Example

Document Extraction can also ingest a public website URL as one input in a broader multi-file extraction. Use [Website Extraction](/docs/website-extraction) instead when the request should contain exactly one public website page.

```json
{
  "files": [
    {
      "type": "url",
      "url": "https://example.com/pricing"
    }
  ],
  "schema": {
    "fields": [
      {
        "name": "plan_name",
        "type": "TEXT",
        "description": "The name of the pricing plan"
      }
    ]
  }
}
```

### Schema Definition

The `schema` object contains a `fields` array. Each field has these base properties:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique field identifier (used as key in the response) |
| `type` | string | Yes | One of the supported field types (see Field Types below) |
| `description` | string | Yes | Natural language description of what to extract |
| `is_required` | boolean | No | If `true`, returns an error when the field cannot be extracted and has no default. Default: `false` |

Each field type supports additional type-specific properties described below.

## Field Types

### TEXT

Short single-line text value.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `max_length` | integer | No | Maximum character length (> 0) |
| `default_value` | string | No | Default value if not found |

```json
{
  "name": "company_name",
  "type": "TEXT",
  "description": "Name of the company"
}
```

### TEXTAREA

Multi-line text value.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `max_length` | integer | No | Maximum character length (> 0) |
| `default_value` | string | No | Default value if not found |

```json
{
  "name": "notes",
  "type": "TEXTAREA",
  "description": "Additional notes or comments"
}
```

### INTEGER

Whole number value.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `min` | integer | No | Minimum value (inclusive) |
| `max` | integer | No | Maximum value (inclusive) |
| `unit` | string | No | Unit label (e.g., `"kg"`, `"items"`) |
| `default_value` | integer | No | Default value if not found |

```json
{
  "name": "quantity",
  "type": "INTEGER",
  "description": "Number of items ordered",
  "min": 1
}
```

### DECIMAL

Floating-point number value.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `min` | float | No | Minimum value (inclusive) |
| `max` | float | No | Maximum value (inclusive) |
| `decimal_points` | integer | No | Number of decimal places to round to (>= 0) |
| `unit` | string | No | Unit label |
| `default_value` | float | No | Default value if not found |

```json
{
  "name": "weight",
  "type": "DECIMAL",
  "description": "Package weight",
  "unit": "kg",
  "decimal_points": 2
}
```

### DATE

Calendar date, extracted as an ISO 8601 string (`YYYY-MM-DD`).

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `allow_future_dates` | boolean | No | Whether to allow dates in the future |
| `allow_past_dates` | boolean | No | Whether to allow dates in the past |

```json
{
  "name": "invoice_date",
  "type": "DATE",
  "description": "Date the invoice was issued"
}
```

### DATETIME

Date and time, extracted as an ISO 8601 datetime string.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `allow_future_dates` | boolean | No | Whether to allow dates in the future |
| `allow_past_dates` | boolean | No | Whether to allow dates in the past |

```json
{
  "name": "timestamp",
  "type": "DATETIME",
  "description": "Transaction timestamp"
}
```

### TIME

Time value (e.g., `"14:30:00"`). No additional parameters.

```json
{
  "name": "delivery_time",
  "type": "TIME",
  "description": "Scheduled delivery time"
}
```

### ENUM

One or more values from a predefined list. Extracted as a string array.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `values` | string[] | Yes | Allowed options |
| `min_selected` | integer | No | Minimum number of selected values (>= 0) |
| `max_selected` | integer | No | Maximum number of selected values (> 0) |
| `default_value` | string[] | No | Default selected values |

```json
{
  "name": "payment_method",
  "type": "ENUM",
  "description": "How the invoice was paid",
  "values": ["bank_transfer", "credit_card", "cash", "paypal"],
  "max_selected": 1
}
```

### BOOLEAN

True or false value.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `default_value` | boolean | No | Default value if not found |

```json
{
  "name": "is_paid",
  "type": "BOOLEAN",
  "description": "Whether the invoice has been paid"
}
```

### EMAIL

Email address string.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `default_value` | string | No | Default value if not found |

```json
{
  "name": "contact_email",
  "type": "EMAIL",
  "description": "Contact email address"
}
```

### IBAN

International Bank Account Number. Validated against the pattern `^[A-Z]{2}\d{2}[A-Z0-9]{11,30}$`.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `default_value` | string | No | Default value if not found |

```json
{
  "name": "bank_account",
  "type": "IBAN",
  "description": "Recipient IBAN"
}
```

### COUNTRY

ISO 3166-1 alpha-2 country code (e.g., `"DE"`, `"US"`).

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `default_value` | string | No | Must be a valid ISO 3166-1 alpha-2 code |

```json
{
  "name": "origin_country",
  "type": "COUNTRY",
  "description": "Country of origin"
}
```

### CURRENCY_CODE

ISO 4217 currency code (e.g., `"EUR"`, `"USD"`).

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `default_value` | string | No | Must be a valid ISO 4217 code |

```json
{
  "name": "currency",
  "type": "CURRENCY_CODE",
  "description": "Invoice currency"
}
```

### CURRENCY_AMOUNT

Numeric monetary amount.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `min` | float | No | Minimum value (inclusive) |
| `max` | float | No | Maximum value (inclusive) |
| `decimal_points` | integer | No | Number of decimal places to round to (>= 0) |
| `default_value` | float | No | Default value if not found |

```json
{
  "name": "total_amount",
  "type": "CURRENCY_AMOUNT",
  "description": "Total invoice amount",
  "decimal_points": 2
}
```

### ADDRESS

Structured address object. Extracted as an object with `street`, `city`, `region`, `postal_code`, and `country` fields.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `allowed_country_codes` | string[] | No | Restrict to specific ISO 3166-1 alpha-2 country codes |

Response value shape:

```json
{
  "street": "123 Main St",
  "city": "Berlin",
  "region": "Berlin",
  "postal_code": "10115",
  "country": "DE"
}
```

```json
{
  "name": "billing_address",
  "type": "ADDRESS",
  "description": "Billing address",
  "allowed_country_codes": ["DE", "AT", "CH"]
}
```

### ARRAY

A list of structured objects, each conforming to a nested schema. Use this for repeating data like line items.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `fields` | array | Yes | Array of field configurations for each item |

The `fields` array uses the same field configuration format as top-level fields.

```json
{
  "name": "line_items",
  "type": "ARRAY",
  "description": "Invoice line items",
  "fields": [
    {
      "name": "description",
      "type": "TEXT",
      "description": "Item description"
    },
    {
      "name": "quantity",
      "type": "INTEGER",
      "description": "Quantity ordered",
      "min": 1
    },
    {
      "name": "unit_price",
      "type": "CURRENCY_AMOUNT",
      "description": "Price per unit",
      "decimal_points": 2
    },
    {
      "name": "total",
      "type": "CURRENCY_AMOUNT",
      "description": "Line item total",
      "decimal_points": 2
    }
  ]
}
```

### CALCULATED

A derived numeric value computed from other extracted fields. Not extracted from the document — calculated locally after all source fields are resolved.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `operation` | string | Yes | One of: `"sum"`, `"subtract"`, `"multiply"`, `"divide"` |
| `source_field_names` | string[] | Yes | Names of fields to apply the operation to, in order |
| `unit` | string | No | Unit label |

Source fields must be numeric types: `INTEGER`, `DECIMAL`, `CURRENCY_AMOUNT`, or another `CALCULATED`. Circular dependencies are detected and rejected at validation time.

The confidence score of a CALCULATED field is the minimum confidence of its source fields. Division by zero returns `0`.

```json
{
  "name": "tax_amount",
  "type": "CALCULATED",
  "description": "Tax amount (total minus net)",
  "operation": "subtract",
  "source_field_names": ["total_amount", "net_amount"]
}
```

## Response Format

### Success Response

```json
{
  "success": true,
  "data": {
    "invoice_number": {
      "type": "TEXT",
      "value": "INV-2024-001",
      "confidence": 0.98,
      "citations": ["Invoice No: INV-2024-001"],
      "source": "invoice.pdf"
    },
    "total_amount": {
      "type": "CURRENCY_AMOUNT",
      "value": 1250.00,
      "confidence": 0.95,
      "citations": ["Total: €1,250.00"],
      "source": "invoice.pdf"
    }
  }
}
```

Each field in `data` contains:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | The field type from the schema |
| `value` | varies | Extracted value (type depends on field type — see below) |
| `confidence` | float | Confidence score between 0.0 and 1.0 |
| `citations` | string[] | Verbatim quotes from the source document |
| `source` | string | Filename the value was extracted from |

**Value types by field type:**

| Field Type | Value Type |
|------------|------------|
| `TEXT`, `TEXTAREA`, `EMAIL`, `IBAN`, `COUNTRY`, `CURRENCY_CODE`, `DATE`, `DATETIME`, `TIME` | string |
| `INTEGER`, `DECIMAL`, `CURRENCY_AMOUNT`, `CALCULATED` | number |
| `BOOLEAN` | boolean |
| `ENUM` | string[] |
| `ADDRESS` | object |
| `ARRAY` | object[] |

Fields that could not be extracted and have no `default_value` are omitted from `data` (unless `is_required` is `true`, which causes an error). Fields resolved via `default_value` have a confidence of `1.0`.

## Best Practices

Use confidence scores as workflow inputs when extracted values can update records, trigger business decisions, or appear in generated outputs.

For low-risk fields, your application can auto-accept values above a field-specific threshold. For high-impact fields such as payment amounts, IBANs, tax IDs, contract dates, consent fields, or customer-facing claims, route low-confidence values to human review before the workflow continues. Store extracted values separately from approved values so downstream systems can tell whether a value is still a candidate or has been reviewed.

Downstream systems should read from approved values, not raw extracted values. An approved value may be auto-accepted or human-corrected. Keep confidence scores as routing signals, citations as review context, and audit events as metadata-only workflow facts rather than application logs that retain full document content.

For auditability, record the extraction schema version, provider route where your policy requires it, workflow version, source record ID, confidence summary, review decision, approved-value snapshot, and downstream delivery status. These fields let operators explain which workflow accepted a value without turning operational logging into a second content store.

See [Workflow Design Best Practices](/docs/workflow-best-practices) for reliability primitives such as confidence gates, review branches, approved values, audit records, retention boundaries, and clear data-flow behavior.

## Recipes

For complete, runnable examples see the [Recipes](/recipes) page.

- [Extract Invoice Data](/recipes/extract-invoice-data) -- Extract line items, totals, and vendor details from an invoice into structured JSON.
- [Extract Resume Data](/recipes/extract-resume-data) -- Extract contact info, work history, and skills from a resume into structured data.
- [Extract Medical Record](/recipes/extract-medical-record) -- Extract patient details, diagnoses, and medications from a medical record into structured JSON.
- [Extract Receipt Data](/recipes/extract-receipt-data) -- Extract merchant, amount, date, and line items from a receipt image or PDF.
- [Extract Multi-Invoice Data](/recipes/extract-multi-invoice-data) -- Extract structured data from multiple invoice files in a single API call using an array schema.

## Error Responses

All errors return a JSON body with `{ "success": false, "error": "<message>" }`.

| Status | Description |
|--------|-------------|
| 400 | Invalid request (missing files/schema, invalid base64, URL fetch failure, file size exceeded, invalid field config) |
| 401 | Missing or invalid API key |
| 402 | Insufficient credits or budget cap exceeded |
| 422 | Processing error (circular dependency in CALCULATED fields, required field not extractable, LLM parsing failure) |
| 429 | Rate limit exceeded |

## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs/document-extraction)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse recipes](https://iterationlayer.com/recipes)
