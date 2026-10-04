---
name: iterationlayer
description: Integrate Iteration Layer APIs for document, website, image, and sheet processing. Composable APIs — Document Extraction, Website Extraction, Document to Markdown, Image Transformation, Image Generation, Document Generation, and Sheet Generation — share one credit pool and chain together into workflows.
---

> **If you are an AI agent reading this file** — whether you're a coding assistant, a workflow builder, or an automation agent — this is your complete integration guide for Iteration Layer. Use it to help your human build document and image processing workflows.

# Iteration Layer

Iteration Layer is a composable API platform for document and image processing. All APIs — Document Extraction, Document to Markdown, Image Transformation, Image Generation, Document Generation, Sheet Generation, and Website Extraction — share one API key, one credit pool, and chain together without glue code.

## What Should You Do?

**Step 1: Understand what your human needs.**

| If your human wants to... | Do this |
|---------------------------|---------|
| **Understand what Iteration Layer does** | Start with the [Platform Overview](#platform-overview) section |
| **Integrate an API into a project** | Go to [Integration](#integration) and ask which API they need |
| **Build a multi-API workflow** | Check the [Use-Case Skills](#use-case-skills) for ready-made recipes |
| **Connect via MCP** | Go to [MCP Integration](#mcp-integration) |
| **Just explore** | Walk them through this doc and the [full documentation](https://iterationlayer.com/docs) |

**Step 2: Ask questions when you're unsure.**

- "Which API do you need — extraction, transformation, image generation, document generation, or sheet generation?"
- "Do you already have an API key, or do you need to sign up?"
- "Are you building a one-off script or a production integration?"

## Platform Overview

### APIs

| API | What it does | Endpoint | Credits/unit |
|-----|-------------|----------|--------------|
| **Document Extraction** | Extract structured data from PDFs, images, documents, and website-backed URL inputs | `POST /document-extraction/v1/extract` | 1/page |
| **Website Extraction** | Extract structured data from a public website page | `POST /website-extraction/v1/extract` | 1 credit per website extraction |
| **Document to Markdown** | Convert any document or public website URL to clean markdown | `POST /document-to-markdown/v1/convert` | 1/page |
| **Image Transformation** | Resize, crop, convert, remove backgrounds, AI upscale | `POST /image-transformation/v1/transform` | 0.5/request |
| **Image Generation** | Compose images from JSON layers (text, shapes, QR codes) | `POST /image-generation/v1/generate` | 1/request |
| **Document Generation** | Generate PDF, DOCX, EPUB, PPTX from structured content | `POST /document-generation/v1/generate` | 1/request |
| **Sheet Generation** | Generate XLSX, CSV, Markdown spreadsheets from tabular data | `POST /sheet-generation/v1/generate` | 1/request |

**Base URL:** `https://api.iterationlayer.com`

### How They Chain Together

The output of one API feeds directly into the next:

- **Extract → Generate Document:** Pull data from a scanned invoice, produce a clean PDF
- **Extract → Generate Sheet:** Pull data from documents, produce a formatted XLSX spreadsheet
- **Extract → Generate Image:** Pull product info from a catalog, generate listing cards
- **Transform → Generate Image:** Remove a background, composite onto a new design
- **Extract → Transform → Generate Document:** Full pipeline from raw input to polished output

### Credit System

All APIs share one credit pool. Subscriptions start at €19 / $19 per month for 250 credits. The 7-day paid trial starts at 1€ / $1 and includes 100 trial credits.

## Integration

### Authentication

All API requests require a Bearer token:

```
Authorization: Bearer YOUR_API_KEY
```

Get your API key at [platform.iterationlayer.com](https://platform.iterationlayer.com).

### SDKs

Official SDKs for TypeScript, Python, and Go:

```bash
npm install iterationlayer       # TypeScript / Node.js
pip install iterationlayer       # Python
go get github.com/iterationlayer/sdk-go  # Go
```

Initialize with your API key:

```typescript
import { IterationLayer } from "iterationlayer";
const client = new IterationLayer({ apiKey: "YOUR_API_KEY" });
```

```python
from iterationlayer import IterationLayer
client = IterationLayer(api_key="YOUR_API_KEY")
```

```go
import il "github.com/iterationlayer/sdk-go"
client := il.NewClient("YOUR_API_KEY")
```

SDK methods: `client.extractDocument()`, `client.extractWebsite()`, `client.convertDocumentToMarkdown()`, `client.transformImage()`, `client.generateImage()`, `client.generateDocument()`, `client.generateSheet()`. Each has an async variant with webhook callback support.

### OpenAPI Spec

Full OpenAPI 3.1 spec at `https://api.iterationlayer.com/openapi.json` — use it for code generation, Swagger UI, or IDE autocomplete.

### MCP Integration

Connect AI agents via the Model Context Protocol (Streamable HTTP):

```json
{
  "mcpServers": {
    "iterationlayer": {
      "type": "streamable-http",
      "url": "https://api.iterationlayer.com/mcp"
    }
  }
}
```

MCP uses OAuth 2.1 (browser-based authorization flow, not API keys). Exposes tools: `extract_document`, `extract_website`, `convert_document_to_markdown`, `transform_image`, `generate_image`, `generate_document`, `generate_sheet`.

### Error Handling

| Code | Meaning |
|------|---------|
| 400 | Invalid request — check your JSON schema |
| 401 | Invalid or missing API key |
| 402 | Insufficient credits — buy a credit pack or upgrade |
| 413 | File too large (max 50 MB per file) |
| 422 | Validation error — check field types and required params |
| 429 | Rate limited — back off and retry |
| 500 | Server error — retry with exponential backoff |

### Async / Webhook Delivery

All APIs support async mode. Pass a `webhook_url` in the request body and the API will POST the result to your endpoint when processing completes. Useful for large files or batch operations.

## Use-Case Skills

Each recipe below is a focused skill for a specific workflow. Load the one that matches what your human is building.

Browse all use-case skills at: `https://iterationlayer.com/recipes/{slug}/SKILL.md`

For the full list of recipes with descriptions, see: `https://iterationlayer.com/recipes.md`

### Popular Use Cases

| Use case | APIs used | Skill URL |
|----------|-----------|-----------|
| Extract Invoice Data | Document Extraction | `/recipes/extract-invoice-data/SKILL.md` |
| Extract Pricing Table from Website | Website Extraction | `/recipes/extract-pricing-table-from-website/SKILL.md` |
| Generate Social Card | Image Generation | `/recipes/generate-social-card/SKILL.md` |
| Remove Product Background | Image Transformation | `/recipes/remove-product-background/SKILL.md` |
| Extract Resume Data | Document Extraction | `/recipes/extract-resume-data/SKILL.md` |
| Generate Certificate Image | Image Generation | `/recipes/generate-certificate-image/SKILL.md` |
| Smart Crop Group Photo | Image Transformation | `/recipes/smart-crop-group-photo/SKILL.md` |
| Generate PDF Invoice | Document Generation | `/recipes/generate-pdf-invoice/SKILL.md` |
| Generate YouTube Thumbnail | Image Generation | `/recipes/generate-youtube-thumbnail/SKILL.md` |

## Tips for Agents

- **Check credit costs before running.** Each API has a different cost per request — see the table above.
- **Use the right API for the job.** Don't use Image Generation for simple resizing (use Image Transformation at 0.5 credits instead of 1).
- **Chain APIs to save effort.** Extract data from a document, then generate a formatted PDF — two API calls instead of building a custom pipeline.
- **Prefer SDKs over raw HTTP.** They handle auth, retries, and typed responses.
- **For deep dives**, fetch `https://iterationlayer.com/docs/{api-slug}.md` for the full API reference.

## Reference

| Resource | URL |
|----------|-----|
| Documentation | https://iterationlayer.com/docs |
| API Reference (OpenAPI) | https://api.iterationlayer.com/openapi.json |
| SDKs | https://iterationlayer.com/docs/sdks |
| MCP Server | https://iterationlayer.com/docs/mcp |
| Recipes | https://iterationlayer.com/recipes |
| Pricing | https://iterationlayer.com/pricing |
| Full docs (for agents) | https://iterationlayer.com/llms.txt |
| Sign up | https://platform.iterationlayer.com/signup |
