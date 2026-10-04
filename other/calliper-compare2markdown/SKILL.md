---
name: Calliper-Compare2Markdown
description: Compare two local documents and convert differences into LLM-ready Markdown in one synchronous call. Supports PDF, Word, PPT, and image documents accepted by Calliper, and returns a structured markdown diff table suitable for change review, clause comparison, downstream extraction, and rule-based validation.
metadata:
  {
    'author': 'PAODINGAI',
    'version': '1.1.0',
    'openclaw':
      {
        'emoji': '🔍',
        'requires': { 'env': ['PD_ROUTER_BASE_URL'], 'bins': ['node'] },
      },
  }
---

# Calliper-Compare2Markdown

Run a JavaScript workflow that submits two local files to the `calliper` synchronous API through PDRouter (`POST /openapi/{serviceCode}/compare/markdown` by default) and returns Markdown diff output in one step. This is suitable for document comparison, change extraction, compliance checks, and feeding structured diff content into follow-up scripts.

## Installation

```bash
npx skills add PaodingAI/skills
```

## Usage

```bash
node skills/calliper-compare2markdown/scripts/compare_to_markdown.js <left-file-path> <right-file-path> [output-markdown-path]
```

## Execution Constraints

- You must invoke `scripts/compare_to_markdown.js` directly. Do not reimplement the API flow yourself.
- The behavior contract below explains what the script does, what it outputs, and when to use it. It is not a manual checklist for the model to imitate step by step.
- For any task that depends on cross-document differences, you must run this script first and continue from the generated Markdown result.
- Only inspect or modify the script implementation when the script itself is unavailable, failing, or needs a fix. Do not bypass it during normal use.

## When to Use

- Use this skill when the user wants to compare two documents and get structured differences in Markdown.
- Use this skill when the user says things like "diff to markdown", "compare and output markdown", "导出差异 markdown", or asks for a machine-readable diff summary.
- When downstream work depends on differences, such as clause extraction, mismatch validation, or rule checks, use this skill first.
- When the diff content is only intermediate input, prefer writing to a working file and extract only required segments instead of returning full raw Markdown.
- When the user explicitly asks for the original markdown diff output, return the full Markdown directly.

## Environment Variables

- `PAODINGAI_API_KEY`: Preferred bearer token used by the script.
- `CALLIPER_ACCESS_TOKEN`: Optional fallback bearer token when `PAODINGAI_API_KEY` is absent.
- `PD_ROUTER_BASE_URL`: Optional. Defaults to `https://platform.paodingai.com/platform/`.
- `PD_ROUTER_SERVICE_CODE`: Optional. Defaults to `calliper`.
- `PD_ROUTER_COMPARE_ENDPOINT`: Optional. Defaults to `/compare/markdown`. Use only when routing endpoint differs.
- `CALLIPER_COMPARE_CONFIG`: Optional. JSON string forwarded as `config` form field. Default is `{}`.

## Script Behavior

1. Read bearer token from `PAODINGAI_API_KEY`; fallback to `CALLIPER_ACCESS_TOKEN`; fail if both are missing.
2. Validate both local input files exist.
3. Send one multipart request with `file1`, `file2`, and optional `config` to `POST /openapi/{serviceCode}{compareEndpoint}` using `Authorization: Bearer <token>`.
4. Parse final response and output:
   - Markdown text directly when response is markdown/plain text.
   - Otherwise, resolve markdown from common JSON fields (`data.markdown`, `markdown`) or fallback to JSON text.
5. If `output-markdown-path` is provided, also write the same output text to that file while still printing to stdout.
6. Write progress and errors to stderr and return non-zero exit code on failure.
7. For field/table extraction tasks, parse and return only required fragments unless user explicitly asks for the full markdown diff.
