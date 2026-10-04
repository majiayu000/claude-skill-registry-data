---
name: PDFlux-PDF2Markdown
description: Convert unstructured documents into LLM-ready structured data. Supports PDF, Word, PPT, and images; extracts paragraphs, formulas, tables, charts, and other elements in one step; generates up to 8 levels of headings; and outputs Markdown organized in reading order. Useful for field extraction, comparison and validation, knowledge retrieval, and intelligent Q&A.
metadata:
  {
    'author': 'PAODINGAI',
    'version': '1.0.1',
    'openclaw':
      {
        'emoji': '📝',
        'requires':
          {
            'env': ['PAODINGAI_API_KEY', 'PAODINGAI_API_BASE_URL'],
            'bins': ['node'],
          },
      },
  }
---

# PDFlux-PDF2Markdown

Run a JavaScript workflow that submits a single local file to the `pdflux` synchronous API through PDRouter (`POST /openapi/{serviceCode}/file/markdown`) and prints the response result in one step. This skill only targets the latest OpenAPI flow and does not support deprecated legacy routes.

## Installation

```bash
npx skills add PaodingAI/skills
```

## Usage

```bash
node skills/pdflux-pdf2markdown/scripts/upload_to_markdown.js <local-file-path> [output-markdown-path]
```

## Execution Constraints

- You must invoke `scripts/upload_to_markdown.js` directly. Do not reimplement the API flow yourself.
- The behavior contract below explains what the script does, what it outputs, and when to use it. It is not a manual checklist for the model to imitate step by step.
- Even if the task is only to extract tables, read fields, inspect body text, or prepare input for later scripts, you must run this script first and continue from the generated Markdown.
- Only inspect or modify the script implementation when the script itself is unavailable, failing, or needs a fix. Do not bypass it during normal use.

## When to Use

- Use this skill when the user wants to parse a document, retrieve specific document content, or extract tables from a document.
- Use this skill when the user says things like "convert to Markdown", "output Markdown", "export Markdown", or "extract Markdown", and return the Markdown content directly.
- When later work depends on the document content, such as summarization, field extraction, document-processing scripts, table comparison, or rule-based validation, use this skill first to parse the document.
- When the document content is only needed as input for subsequent steps, do not default to showing the full raw Markdown to the user. Prefer saving it to a temporary or working file first, then read, filter, and extract only what is needed.
- When the user explicitly asks for the original Markdown output or clearly wants a direct document-to-Markdown conversion, show the full Markdown directly.

## Environment Variables

- `PAODINGAI_API_KEY`: Required. The Bearer API key for PDRouter OpenAPI. If it is missing, the script fails immediately. In a skill workflow, the AI should ask the user to provide a valid key, or inject it into the environment before retrying.
- `PAODINGAI_API_BASE_URL`: Optional. Defaults to `https://platform.paodingai.com/platform/`.
- `PD_ROUTER_SERVICE_CODE`: Optional. Defaults to `pdflux`.
- `PDFLUX_INCLUDE_IMAGES`: Optional. Boolean. Markdown output does not include image data by default.

## Default Behavior and Optional Settings

- Parsed results do not include chart or image extraction by default.
- If charts, images, or similar content are required, enable them explicitly through API parameters. These results are usually returned as base64 and will increase token usage.
- Markdown output does not include image data by default. If you need embedded image data, set `PDFLUX_INCLUDE_IMAGES=true`.

## Script Behavior

1. Read the token from `PAODINGAI_API_KEY`. If it is missing, fail immediately and prompt the AI to ask the user for a key or inject the environment variable first.
2. Send one request with the local file to `POST /openapi/{serviceCode}/file/markdown` using `Authorization: Bearer <token>`.
3. Parse the final API response and output:
   - Markdown text if the response contains a markdown field.
   - Otherwise, output the JSON response payload.
4. If `output-markdown-path` is provided, the script also writes the same output text to that file while still printing it to stdout.
5. The script writes progress and errors to stderr and returns a non-zero exit code on failure.
6. When the goal is to retrieve specific content, fields, or tables, read the parsed result and return only the necessary information instead of echoing full raw output to the user.
7. When the user explicitly asks to "convert to Markdown", "output Markdown", or expresses an equivalent intent, return the Markdown content directly when present in the API response.
