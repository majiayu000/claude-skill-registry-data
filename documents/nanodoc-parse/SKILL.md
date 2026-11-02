---
name: nanodoc-parse
description: Use when a local PDF, JPG/JPEG, PNG, DOCX, PPTX, or XLSX must be parsed through PDRouter into Markdown, result.json, and images, or when later reading, extraction, search, summary, or Q&A depends on that parse. Triggers include NanoDoc parse, /openapi/nanodoc/parse, and PAODINGAI_API_KEY. Do not use for the direct nanodoc.ai API, unsupported file types, or knowledge-base chat.
metadata: {"author":"PAODINGAI","version":"1.0.0","openclaw":{"emoji":"📄","requires":{"env":["PAODINGAI_API_KEY"],"bins":["node","unzip"]}}}
---

# NanoDoc Parse

Run the bundled script to upload one local supported document to NanoDoc through PDRouter, wait until parsing finishes, and extract the result archive.

The archive contains `result.json` (the structured content list), one root-level Markdown file, and figure images under `images/`. Use the returned `output_directory` for summarization, field extraction, search, or Q&A.

## Installation

This copy lives at `nanodoc-parse` in the `PaodingAI/skills` repository. For a local Codex installation, place that directory under:

```bash
$CODEX_HOME/skills/nanodoc-parse
```

After it is published to `PaodingAI/skills`, `npx skills add PaodingAI/skills` installs the same directory.

## Usage

```bash
node scripts/nanodoc-parse.mjs parse \
  --file ./report.pdf \
  --output ./report-nanodoc
```

From this repository:

```bash
node nanodoc-parse/scripts/nanodoc-parse.mjs parse \
  --file ./report.pdf \
  --output ./report-nanodoc
```

The output directory must be empty or nonexistent. On success, stdout is JSON with `output_directory`, `markdown`, and `result_json`.

## Execution Constraints

- Invoke `scripts/nanodoc-parse.mjs` directly. Do not reimplement the upload, wait, or unzip flow.
- Route every request through PDRouter at `/openapi/nanodoc/parse`.
- Authenticate only with `Authorization: Bearer <PAODINGAI_API_KEY>`.
- Do not call NanoDoc directly, including `https://nanodoc.ai` and `/pdrouter/api/v1`.
- Do not add internal `X-PD-*` signature headers in this skill.
- Parse one document per command. Supported formats are PDF, JPG/JPEG, PNG, DOCX, PPTX, and XLSX. Do not batch files, and do not send legacy DOC/PPT/XLS, GIF, or other unsupported types.
- For summaries, search, field extraction, or Q&A, parse first and continue from the extracted files.
- Read the Markdown path printed by the script. Use `result.json` for structured blocks, coordinates, tables, formulas, or image paths.
- Keep `images/` next to the generated files. Return only the content needed unless the user asks for the full result.
- Only inspect or modify the script when the script itself is unavailable, failing, or needs a fix.
- The behavior contract below explains what the script does. It is not a checklist to imitate over HTTP.

## When to Use

- Use this skill when the user wants NanoDoc to parse a local PDF, JPG/JPEG, PNG, DOCX, PPTX, or XLSX through PDRouter.
- Use this skill when later work depends on the document content, such as summarization, field extraction, table reading, or question answering.
- Use this skill when the user asks to convert a supported document to Markdown or structured JSON.
- Do not use this skill for the direct NanoDoc API (`NANODOC_API_KEY`, `/api/v1/parse`). That flow is `parse-pdf-with-nanodoc`.
- Do not use this skill for knowledge-base upload, retrieval, grep, or syllabus reading. This gateway only parses one supported document and returns the archive.
- Do not use this skill for legacy DOC/PPT/XLS, GIF, or other unsupported files. The parse endpoint accepts PDF, JPG/JPEG, PNG, DOCX, PPTX, and XLSX filenames with their corresponding file headers.

## Environment Variables

- `PAODINGAI_API_KEY`: Required. Bearer API key for PDRouter. If it is missing, the script fails immediately and tells the user to create a Bearer API key in PDRouter, then export it before retrying. Never pass the key as an argument, and never print it.
- `PAODINGAI_API_BASE_URL`: Optional. Exact PDRouter origin. Defaults to `https://platform.paodingai.com`. The script does not append `/platform` or `/openapi`. Set it only for a non-production PDRouter. Do not point it at NanoDoc itself.

The service code is fixed as `nanodoc`. Callers do not set a service-code variable.

## Default Behavior and Optional Settings

- One supported document per invocation. `--file` and `--output` are both required.
- The file must use one of `.pdf`, `.jpg`, `.jpeg`, `.png`, `.docx`, `.pptx`, or `.xlsx`. Before uploading, the script checks `%PDF-` for PDF, JPEG/PNG magic bytes for images, and the ZIP magic bytes used by Office Open XML files.
- The output directory must be empty or absent. A symbolic link is rejected.
- The script performs one synchronous `POST`. It does not poll `/parse/{job_id}`.
- The gateway waits up to its configured parse deadline (default 1800 seconds). The script aborts the HTTP call after 1920 seconds.
- Input documents are limited to NanoDoc's default 200 MiB upload limit. Downloaded result archives are limited to 512 MiB, and extracted output is limited to 2 GiB.

## Script Behavior

1. Read `PAODINGAI_API_KEY`. Use `PAODINGAI_API_BASE_URL` when set, otherwise `https://platform.paodingai.com`.
2. Reject a missing key, an unsupported extension, an invalid file header, an unsafe path, or a non-empty output directory before uploading.
3. `POST /openapi/nanodoc/parse` with multipart field `file` and `Authorization: Bearer <PAODINGAI_API_KEY>`.
4. On HTTP success, require a zip archive. Validate entries, reject path traversal and symbolic links, then extract into `--output`.
5. Print JSON on stdout: `output_directory`, the root `*.md` path as `markdown`, and `result_json`.
6. On HTTP failure, print JSON `{"error":"...","response":...}` on stderr and exit non-zero. NanoDoc errors look like `{ "code": 422, "error_code": "PARSE_FAILED", "message": "..." }`. PDRouter errors look like `{ "code": "gateway.insufficient_credits" }`. A gateway timeout is HTTP 504 `PARSE_TIMEOUT`.
7. Write progress to stderr. Do not print the API key.

## Resources

- Run [scripts/nanodoc-parse.mjs](./scripts/nanodoc-parse.mjs) instead of rewriting the HTTP client.
