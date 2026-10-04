---
name: website-extraction-api
description: Extract typed JSON from public website pages using a schema.
---

# Website Extraction API

Extract typed JSON from public website pages using a schema.

**Cost:** 1 credit per website extraction

## Prerequisites

You need an Iteration Layer API key. Get one at [platform.iterationlayer.com](https://platform.iterationlayer.com) during the 7-day trial.

For full integration guidance (SDKs, auth, MCP, error handling), see the [Iteration Layer Integration Guide](https://iterationlayer.com/SKILL.md).

## API Reference

Extract structured data from one public website page with a single API call. Send one public URL and a schema defining the fields you need, and receive typed, validated results with confidence scores and source citations.

## Key Features

- **Website URL Input** — Send a public `https` URL as a URL file input with optional website fetch settings.
- **Rich Field Types** — Primitive types (text, number, date, boolean, email, enum) plus purpose-built validated types: `IBAN` (validated against the standard format), `ADDRESS` (returns a structured object with street, city, region, postal code, and country), `CURRENCY_CODE` (normalized to ISO 4217), `CURRENCY_AMOUNT` (numeric monetary value), and `COUNTRY` (normalized to ISO 3166-1 alpha-2). These validated types mean you get clean, usable data — not raw strings you have to parse yourself.
- **Structured Arrays** — Extract repeating website data like pricing tiers, product variants, job listings, menu items, or page tables with nested schemas.
- **Calculated Fields** — Define arithmetic operations (sum, subtract, multiply, divide) computed from other extracted fields.
- **Confidence Scores** — Every extracted value includes a confidence score between 0 and 1.
- **Source Citations** — Verbatim quotes from the fetched page content support each extracted value.
- **Referenced Image Context** — A bounded set of usable image assets referenced by the page will be included as extraction context. Logos, favicons, tracking pixels, sprites, decorative icons, and semantically decorative images are skipped. Image binaries are not returned in the API response.
- **Schema Validation** — Field schemas are validated before extraction, catching errors like circular dependencies or type mismatches early.

## Overview

The Website Extraction API fetches one public website URL and extracts structured data based on a schema you define. You send one URL input and a schema with field definitions, and receive a JSON response with typed values, confidence scores, citations, and source metadata.

**Endpoint:** `POST /website-extraction/v1/extract`

**Limits:**

- HTTPS URLs only (HTTP is not accepted)
- Public website pages only
- One URL file input per request

Use Website Extraction when you want structured fields from a single public web page. Use [Document Extraction](/docs/document-extraction) when you have uploaded files, multiple inputs, or mixed formats like PDFs and images in the same request.

## How It Works

Every Website Extraction request resolves the URL input first, then runs the same extraction schema pipeline used by Document Extraction.

1. **Validate** — the URL file input and extraction schema are checked before processing starts. Schema validation checks that CALCULATED source field references exist, CALCULATED source fields use numeric types, circular dependencies are rejected, and default values match their field type. The first validation failure stops processing before extraction starts.
2. **Fetch** — the public URL is fetched as page content.
3. **Collect context** — usable images referenced by the page may be fetched with internal limits and added as extraction context. Failed, invalid, decorative, or semantically unhelpful referenced images are skipped.
4. **Ingest** — the fetched content and usable referenced images are converted into the normalized representation used by extraction.
5. **Extract** — your schema is applied to the ingested content, including rich field types, nested arrays, and CALCULATED fields.
6. **Consolidate** — default values are applied to fields that were not extracted, and required field constraints are checked.
7. **Return** — the response includes extracted field results and the requested URL in metadata.

**Intelligent extraction** — the API automatically selects the best extraction approach based on the complexity of your schema and the page content. You don't configure this.

By default, Website Extraction fetches static HTML directly. Set `should_render_javascript` when the target page needs browser rendering before extraction. Browser rendering can execute public page JavaScript, but it does not bypass bot protection, CAPTCHA, login walls, or network blocks. Proxy and region controls are not currently supported, so some sites may return country-specific content, consent pages, or anti-bot verification pages.

For a technical deep dive into the ingestion pipeline that converts website pages and files into markdown before extraction, see [How Our Document Ingestion Pipeline Turns Files into LLM-Ready Markdown](/blog/how-our-document-ingestion-pipeline-works).

## Request Format

<!-- tabs -->

```bash
curl -X POST \
  https://api.iterationlayer.com/website-extraction/v1/extract \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "file": {
      "type": "url",
      "url": "https://example.com/pricing"
    },
    "schema": {
      "fields": [
        {
          "name": "plan_name",
          "type": "TEXT",
          "description": "The name of the pricing plan"
        },
        {
          "name": "monthly_price",
          "type": "CURRENCY_AMOUNT",
          "description": "The advertised monthly price"
        },
        {
          "name": "features",
          "type": "ARRAY",
          "description": "Included plan features",
          "fields": [
            {
              "name": "feature",
              "type": "TEXT",
              "description": "Feature label"
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

const result = await client.extractWebsite({
  file: {
    type: "url",
    url: "https://example.com/pricing",
  },
  schema: {
    fields: [
      { name: "plan_name", type: "TEXT", description: "The name of the pricing plan" },
      { name: "monthly_price", type: "CURRENCY_AMOUNT", description: "The advertised monthly price" },
      {
        name: "features",
        type: "ARRAY",
        description: "Included plan features",
        fields: [{ name: "feature", type: "TEXT", description: "Feature label" }],
      },
    ],
  },
});
```

```python
from iterationlayer import IterationLayer

client = IterationLayer(api_key="YOUR_API_KEY")

result = client.extract_website(
    file={
        "type": "url",
        "url": "https://example.com/pricing",
    },
    schema={
        "fields": [
            {"name": "plan_name", "type": "TEXT", "description": "The name of the pricing plan"},
            {"name": "monthly_price", "type": "CURRENCY_AMOUNT", "description": "The advertised monthly price"},
            {
                "name": "features",
                "type": "ARRAY",
                "description": "Included plan features",
                "fields": [{"name": "feature", "type": "TEXT", "description": "Feature label"}],
            },
        ]
    },
)
```

```go
import il "github.com/iterationlayer/sdk-go"

client := il.NewClient("YOUR_API_KEY")

result, err := client.ExtractWebsite(il.ExtractWebsiteRequest{
	File: il.FileInput{Type: "url", Url: "https://example.com/pricing"},
	Schema: il.ExtractionSchema{
		Fields: []any{
			il.TextFieldConfig{Type: "TEXT", Name: "plan_name", Description: "The name of the pricing plan"},
			il.CurrencyAmountFieldConfig{Type: "CURRENCY_AMOUNT", Name: "monthly_price", Description: "The advertised monthly price"},
			il.ArrayFieldConfig{
				Type: "ARRAY",
				Name: "features",
				Description: "Included plan features",
				Fields: []any{
					il.TextFieldConfig{Type: "TEXT", Name: "feature", Description: "Feature label"},
				},
			},
		},
	},
})
```

<!-- response -->

```json
{
  "success": true,
  "data": {
    "plan_name": {
      "type": "TEXT",
      "value": "Build",
      "confidence": 0.97,
      "citations": [
        "Build — $99 per month"
      ],
      "source": "pricing.html"
    },
    "monthly_price": {
      "type": "CURRENCY_AMOUNT",
      "value": 99,
      "confidence": 0.95,
      "citations": [
        "$99 per month"
      ],
      "source": "pricing.html"
    }
  },
  "metadata": {
    "url": "https://example.com/pricing"
  }
}
```

<!-- /tabs -->

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | object | Yes | Website URL input. Must have `type: "url"` and a public `url`. |
| `schema` | object | Yes | Extraction schema defining the fields to extract. |
| `webhook_url` | string | No | HTTPS URL to receive results asynchronously. If provided, returns 201 immediately. See [Webhooks](/docs/webhooks). |

### Async Mode

Add a `webhook_url` parameter to process the request in the background. The API returns `201 Accepted` immediately and delivers the result to your webhook URL when processing completes. See [Webhooks](/docs/webhooks) for payload format and retry behavior.

### Website URL Input

The `file` object must be a URL input. Website Extraction does not accept base64 uploads or multiple files.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | `"url"` | Yes | Input method. Must be `"url"`. |
| `url` | string | Yes | Public HTTPS URL to fetch and extract from. HTTP is not accepted. |
| `name` | string | No | Optional source name. If omitted, the API assigns a website file name internally. |
| `fetch_options` | object | No | Advanced retrieval controls for public pages that need explicit retrieval settings. |

Website Extraction always checks the site's `robots.txt` before fetching the page. If the URL is disallowed for the effective `User-Agent`, the request fails with `400 Bad Request` and the page is not fetched. Sitemap entries in `robots.txt` are recorded as metadata only; they are not traversed.

Website fetches are rate-limited per destination host. The service automatically respects `robots.txt` crawl-delay hints, slows down after upstream `429 Too Many Requests` responses, and uses upstream `Retry-After` or rate-limit reset headers when provided. This protects public sites and may delay later requests to the same host; it is not configurable through `fetch_options`.

If the initial fetch looks like a WAF or security challenge, the API automatically retries the same URL in an isolated Chromium browser session. Detection covers common Cloudflare, Akamai, AWS WAF/CloudFront, Imperva/Incapsula, DataDome, PerimeterX, Sucuri, F5/BIG-IP, hCaptcha, reCAPTCHA, and generic verification pages. If the browser retry succeeds, `metadata.security` records the detected provider, reason, and bypass result. If the browser retry fails or still returns a challenge page, the request fails with `400 Bad Request` and a clear security-challenge message.

### Fetch Options

`fetch_options` lets you control retrieval behavior for the website URL input. Robots compliance and per-host rate limiting are mandatory and are not configurable.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `locale` | string | No | BCP 47 locale tag sent as `Accept-Language` (e.g., `"en-US"`, `"de-DE"`, `"fr"`). |
| `user_agent` | string | No | Custom `User-Agent` header string (1–500 characters). |
| `auth` | object | No | Authentication for the website request. Supports bearer tokens, HTTP Basic auth, and a custom auth header. Secret values are not returned in metadata. |
| `headers` | object | No | Additional request headers for the website request. Header names and values are validated; unsafe headers such as `Cookie`, `Set-Cookie`, `Host`, `Content-Length`, hop-by-hop headers, and browser-controlled `Sec-*` headers are rejected. |
| `timeout_ms` | integer | No | Website fetch timeout in milliseconds. Must be between `1000` and `60000`. |
| `should_render_javascript` | boolean | No | Use Chromium browser rendering before extraction. Default: `false`. |

Fetch options control retrieval behavior, not billing. Each Website Extraction request counts as 1 page-equivalent.

### Custom Headers

Custom headers are sent on direct fetches and, when JavaScript rendering is enabled or security-challenge fallback is needed, as Chromium request headers where supported by the browser. Each Chromium fetch uses an isolated browser context that is disposed after the request; cookies and session state are not persisted across URLs or requests.

### Auth Examples

Use one auth shape per request.

```json
{ "auth": { "type": "bearer", "token": "..." } }
{ "auth": { "type": "basic", "username": "...", "password": "..." } }
{ "auth": { "type": "custom_header", "name": "x-api-key", "value": "..." } }
```

### Schema Definition


The `schema` object contains a `fields` array. Each field has these base properties:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique field identifier (used as key in the response) |
| `type` | string | Yes | One of the supported field types (see Field Types below) |
| `description` | string | Yes | Natural language description of what to extract |
| `is_required` | boolean | No | If `true`, returns an error when the field cannot be extracted and has no default. Default: `false` |

Each field type supports additional type-specific properties described below. Schema validation happens before extraction starts, so invalid calculated references, circular dependencies, and type-mismatched defaults fail early.

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

Responses return typed field values plus confidence, citations, and source metadata for each extracted result.

### Success Response

```json
{
  "success": true,
  "data": {
    "plan_name": {
      "type": "TEXT",
      "value": "Build",
      "confidence": 0.97,
      "citations": ["Build — $99 per month"],
      "source": "pricing.html"
    },
    "monthly_price": {
      "type": "CURRENCY_AMOUNT",
      "value": 99,
      "confidence": 0.95,
      "citations": ["$99 per month"],
      "source": "pricing.html"
    }
  },
  "metadata": {
    "url": "https://example.com/pricing"
  }
}
```

Each field in `data` contains:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | The field type from the schema |
| `value` | varies | Extracted value (type depends on field type — see below) |
| `confidence` | float | Confidence score between 0.0 and 1.0 |
| `citations` | string[] | Verbatim quotes from the fetched page content |
| `source` | string | Source name for the fetched page content |

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

The raw HTTP response also includes `metadata.requested_url`, `metadata.final_url`, and rich page metadata for the fetched page. When security-challenge fallback runs, `metadata.security` may include `waf_detected`, `waf_provider`, `waf_reason`, `waf_bypass_attempted`, and `waf_bypass_succeeded`. SDK methods return the extracted `data` object directly.

## Public Page Responsibilities

Website Extraction is intended for public pages only. You are responsible for site terms, robots rules, lawful basis, personal-data handling, and whether the page may be processed in your workflow.

Do not use Website Extraction for login-protected content, private dashboards, pages requiring credentials, or content you are not allowed to process.

## Recipes

For complete, runnable examples see the [Recipes](/recipes) page.

- [Extract Pricing Table from Website](/recipes/extract-pricing-table-from-website) — Extract plan names, prices, and feature lists from a public pricing page.
- [Extract Product Data from Website](/recipes/extract-product-data-from-website) — Extract product names, prices, descriptions, and availability from a product page.
- [Extract Job Listings from Website](/recipes/extract-job-listings-from-website) — Extract role titles, locations, compensation, and requirements from a public careers page.

## Error Responses

All errors return a JSON body with `{ "success": false, "error": "<message>" }`.

| Status | Description |
|--------|-------------|
| 400 | Invalid request, missing URL input, invalid URL input, or invalid schema. |
| 401 | Missing or invalid API key. |
| 402 | Insufficient credits or budget cap exceeded. |
| 422 | The page could not be fetched, processed, or extracted. |
| 429 | Rate limit exceeded. |

## Links

- [Integration guide](https://iterationlayer.com/SKILL.md)
- [Full documentation](https://iterationlayer.com/docs/website-extraction)
- [OpenAPI spec](https://api.iterationlayer.com/openapi.json)
- [Browse recipes](https://iterationlayer.com/recipes)
