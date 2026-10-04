---
name: ChatDOC Studio--KnowledgeMate
description: Create and operate ChatDOC Studio knowledge bases through pd_router using a Bearer API key and JavaScript helpers. Use when Codex needs to upload one or more PDF/DOC/DOCX files, skip failed files without aborting the whole job, create a knowledge base from successful uploads, or call the ChatDOC Studio knowledge-base skill endpoints through `https://platform.paodingai.com/openapi/chatdoc-studio/...`.
metadata: {"author":"PAODINGAI","version":"1.0.1","openclaw":{"emoji":"📝","requires":{"env":["PAODINGAI_API_KEY"],"bins":["node"]}}}
---

# ChatDOC Studio KnowledgeMate

Run a JavaScript workflow that uploads local PDF/DOC/DOCX files to ChatDOC Studio through PDRouter, waits for successful parsing, and creates a knowledge base from the successful uploads in one step.

This is suitable for creating knowledge bases from local files or folders, then using the returned `library_id` for document listing, retrieval, grep, syllabus reading, and block reading.

## Installation

```bash
npx skills add PaodingAI/skills
```

For a local Codex installation, place this skill directory under:

```bash
$CODEX_HOME/skills/chatdoc-studio-knowledgemate
```

## Usage

Create a knowledge base from files:

```bash
node scripts/knowledge-mate.mjs upload-and-create \
  --name "Quarterly KB" \
  --file ./docs/a.pdf \
  --file ./docs/b.docx \
  --file ./docs/c.pdf
```

Create a knowledge base from a folder recursively:

```bash
node scripts/knowledge-mate.mjs upload-and-create \
  --name "Quarterly KB" \
  --dir ./docs
```

Query an existing knowledge base:

```bash
node scripts/knowledge-mate.mjs retrieval --library-id <id> --query <text>
node scripts/knowledge-mate.mjs list-documents --library-id <id>
node scripts/knowledge-mate.mjs stats --library-id <id> --upload-id <id>
node scripts/knowledge-mate.mjs grep --library-id <id> --upload-id <id> --pattern <text>
node scripts/knowledge-mate.mjs read --library-id <id> --upload-id <id> --offset <n>
node scripts/knowledge-mate.mjs read-syllabus --library-id <id> --upload-id <id>
```

## Execution Constraints

- You must invoke `scripts/knowledge-mate.mjs` directly. Do not reimplement the PDRouter or ChatDOC Studio API flow yourself during normal use.
- Route every request through PDRouter at `/openapi/chatdoc-studio/...`.
- Authenticate only with `Authorization: Bearer <PAODINGAI_API_KEY>`.
- Do not call `chatdoc_studio` directly.
- Do not add internal `X-PD-*` signature headers in this skill.
- Do not expose or use separate upload-only or create-only commands; use `upload-and-create` for new knowledge bases.
- Only inspect or modify the script implementation when the script itself is unavailable, failing, or needs a fix.
- The behavior contract below explains what the script does, what it outputs, and when to use it. It is not a manual checklist for the model to imitate step by step.

## When to Use

- Use this skill when the user wants to create a ChatDOC Studio knowledge base from local PDF, DOC, or DOCX files.
- Use this skill when the user provides a folder and asks to build a knowledge base from the documents inside it.
- Use this skill when the user wants knowledge retrieval, document search, document stats, syllabus inspection, or reading specific document blocks from a ChatDOC Studio knowledge base.
- Use this skill when the workflow must skip failed or unsupported files without aborting the entire upload batch.
- Use this skill only for PDRouter-backed ChatDOC Studio skill APIs, not for direct ChatDOC Studio internal APIs.

## Environment Variables

- `PAODINGAI_API_KEY`: Required. The Bearer API key for PDRouter. If it is missing, the script fails immediately and tells the user to create a Bearer API Key in pdrouter, then export it before retrying.

The PDRouter base URL is fixed in the script as `https://platform.paodingai.com`. The service code is fixed in the script as `chatdoc-studio`; users do not need to set base-url or service-code environment variables.

The API key can be obtained from the PDRouter platform.

## Default Behavior and Optional Settings

- Upload concurrency is fixed at `5`.
- Supported upload file types are `.pdf`, `.doc`, and `.docx`.
- `--dir` is scanned recursively.
- `--file` and `--dir` can be mixed in one command.
- Duplicate file paths are removed before upload.
- Unsupported file types are not uploaded and are reported as skipped failures.
- If more than `300` supported files are found, the script stops before uploading and asks the user to clean the folder to at most `300` PDF/DOC/DOCX files.
- If every file fails to upload or parse, knowledge-base creation is skipped and the script exits with a non-zero status.

## Script Behavior

1. Read `PAODINGAI_API_KEY` from the environment and use the fixed PDRouter base URL `https://platform.paodingai.com`.
2. Expand all `--file` inputs and recursively scanned `--dir` inputs into one de-duplicated file list.
3. Count supported `.pdf`, `.doc`, and `.docx` files before uploading. If the count is greater than `300`, fail immediately without uploading anything.
4. Upload supported files through `POST /openapi/chatdoc-studio/knowledge-base/upload` with concurrency `5`.
5. Skip unsupported files, upload failures, parse failures, and per-file backend errors without aborting the whole batch.
6. Call `POST /openapi/chatdoc-studio/knowledge-base` only with successful `upload_id`s.
7. Print JSON output. Successful API responses are unwrapped to their `data` payload. Failed requests print a clear error reason and include the backend response when available.
8. After `upload-and-create` returns a `library_id`, use the read/query commands for retrieval, listing documents, stats, grep, syllabus reading, or block reading.

## Resources

- Run [scripts/knowledge-mate.mjs](./scripts/knowledge-mate.mjs) instead of rewriting the HTTP client by hand.
