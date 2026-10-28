---
name: ocr-space
description: Extract text from images or PDF documents using the OCR.space API. Use this skill whenever the user needs to recognize text from an image URL, a local image file, or a Base64-encoded image, including multilingual OCR, table extraction from scanned documents, or getting text coordinate overlays. Triggers on requests like "read text from this image", "extract text from PDF", "OCR this screenshot", "recognize Chinese/Japanese text in image", or "get bounding boxes for words in this picture".
license: MIT
---

# OCR.space — Image and PDF Text Recognition

## Capabilities Overview

Perform optical character recognition (OCR) on images and PDF files via the OCR.space API. Supports 30+ languages, three submission methods (URL, file upload, Base64), and can return recognized text along with coordinate information.

This plugin contains two endpoints:

| Endpoint | Method | Description | Billing |
|----------|--------|-------------|---------|
| `POST https://app-dohnbj5by5mp-api-W9z3M6eONl3L.gateway.appmedo.com/parse/image` | POST | Core OCR endpoint supporting URL / file upload / Base64 input methods, with advanced features such as table recognition and coordinate overlay | Billed per call |
| `GET https://app-dohnbj5by5mp-api-m9xKXDbRplNa.gateway.appmedo.com/parse/imageurl` | GET | Simplified GET endpoint supporting URL-only image submission, suitable for quick integration | Not billed |

> Prefer the **GET /parse/imageurl** endpoint (free) for simple URL-based image recognition. Use the **POST /parse/image** endpoint only when you need file upload, Base64 input, table recognition, coordinate overlay, or other advanced features.

---

## End-to-End Workflow

Both endpoints are **synchronous** — no polling required: submit the request and receive the recognition result directly.

```
User provides image source
    ↓
Determine input type
    ├─ Image URL (no advanced needs) → GET /parse/imageurl (free, simple, fast)
    └─ File upload / Base64 / advanced features → POST /parse/image (per-call billing)
    ↓
Parse ParsedResults[0].ParsedText from the response
    ↓
Return recognized text (or coordinate information)
```

---

## Generation-Time Usage (Agent Direct Call)

Use the built-in script for generation-time calls. The script reads `INTEGRATIONS_API_KEY` from the environment.

**The Bash tool timeout MUST be set to 600000ms (600 seconds).**

```bash
# OCR from an image URL (preferred — not billed)
python3 <skill-path>/scripts/call_ocr_space.py --url "https://example.com/document.jpg" --language eng

# OCR from a local file (billed)
python3 <skill-path>/scripts/call_ocr_space.py --file /path/to/document.png --language eng --engine 2

# With table recognition and scaling
python3 <skill-path>/scripts/call_ocr_space.py --url "https://example.com/table.jpg" --table --scale
```

The script prints `{"status":"succeed","result":{...}}` on success. On failure it prints an error to stderr and exits with a non-zero code.

See `references/parse-image-api.md` (POST, supports file/Base64) and `references/parse-imageurl-api.md` (GET, URL only) for the full parameter tables.

---

## Post-Generation Usage (Application Calls via Edge Function)

See the Edge Function boilerplate code in each endpoint reference file:

- POST endpoint Edge Function → read `references/parse-image-api.md`
- GET endpoint Edge Function → read `references/parse-imageurl-api.md`

Security contract:
- The frontend sends the image source (URL / Base64) to the Edge Function (JSON body).
- The Edge Function reads the API key from the Deno environment variable `INTEGRATIONS_API_KEY` and adds it to the `X-Gateway-Authorization` header.
- The raw API Key is never exposed to the browser.
- 429 (quota exceeded) and 402 (insufficient balance) errors are forwarded verbatim to the frontend.

---

## Notes

- **Key Security**: `INTEGRATIONS_API_KEY` can only be read server-side in the Edge Function; never expose it to the frontend.
- **Error Handling**: Always handle 429 (quota exceeded) and 402 (insufficient balance); also check `OCRExitCode` (1=success, 2=partial success, 3=failure, 4=error) and `IsErroredOnProcessing` in the response body.
- **Billing**: POST `/parse/image` is billed per call, but unnecessary repeated calls should still be avoided. GET `/parse/imageurl` is not billed and should be preferred.
- **Input Constraints**: The POST endpoint requires one of `url`, `file`, or `base64Image`; Base64 input must include the data type prefix, e.g. `data:image/jpeg;base64,`.
- **Language Codes**: Use OCR.space proprietary language codes (e.g. `chs` for Simplified Chinese, `cht` for Traditional Chinese), not standard BCP 47 codes.
