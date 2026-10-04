---
name: html2link
description: Publish and manage browser-viewable artifacts with html2link. Use when a user asks an agent to deploy, publish, host, share, update, replace, or delete generated HTML, a static website ZIP, PDF, Markdown, spreadsheet, DOCX, or PPTX as a public link.
---

# html2link Artifact Publishing

Publish a finished local artifact and return the exact URL from the API. Treat every generated URL as public.

## Core workflow

1. Finish and verify the artifact before uploading it.
2. Package a multi-file static site as a ZIP containing `index.html`.
3. Check that the artifact contains no secrets, credentials, or unintended private data.
4. Prefer the `html2link` CLI when it is installed; otherwise use the anonymous curl fallback.
5. Parse the exit status and JSON response. Do not claim success unless it contains `url`.
6. Return the exact `url` value as a clickable link. Do not reconstruct it from `slug`.

## Publish a new artifact

With the CLI:

```bash
html2link publish /absolute/path/to/report.html
```

Anonymous curl fallback for files up to 1 MB:

```bash
curl --fail-with-body -F "file=@/absolute/path/to/report.html" https://html2link.dev/api/upload
```

For larger files, use an API token from the signed-in home page:

```bash
HTML2LINK_API_TOKEN="..." html2link publish /absolute/path/to/report.html
```

Keep authenticated operations in the CLI so credentials stay in the local process environment rather than being embedded in reusable shell commands.

Use `--json` when another program needs the complete response:

```bash
html2link publish /absolute/path/to/report.html --json
```

## Handle a successful response

```json
{
  "slug": "a1B2c3D4",
  "updateToken": "keep-this-private",
  "url": "https://html2link.dev/x/a1B2c3D4",
  "kind": "html",
  "size": "42 KB",
  "updated": false
}
```

- Return `url` to the user.
- Keep `updateToken` private. Never include it in a public link or expose it unless the user explicitly needs to manage the upload.
- Retain `slug` with `updateToken` only when the user asks to update or delete the same link later.

## Update an existing link

Use the original `slug`, its `updateToken`, and the replacement file. A successful update keeps the public URL unchanged.

```bash
html2link update /absolute/path/to/report.html --slug a1B2c3D4 --update-token "keep-this-private"
```

## Delete or list links

```bash
html2link delete --slug a1B2c3D4 --update-token "keep-this-private"
html2link list --token "$HTML2LINK_API_TOKEN"
```

## Handle errors

- `400`: Fix the multipart body, file type, slug, or update token before retrying.
- `401` with `requiresLogin: true`: Tell the user the anonymous limit was exceeded and ask them to provide an API token.
- `411`: Retry with the CLI or a client that sends `Content-Length`.
- `413`: Reduce or split the artifact. Do not retry the same file unchanged.
- Network error or a response without `url`: Treat publishing as failed and do not invent a link.

## Supported files and limits

- Extensions: `.html`, `.htm`, `.zip`, `.pdf`, `.md`, `.markdown`, `.xlsx`, `.xls`, `.csv`, `.docx`, `.pptx`
- Static site ZIPs must contain `index.html`; a single top-level folder is normalized automatically.
- Anonymous uploads: up to 1 MB.
- Authenticated uploads: up to 100 MB.

## Safety and handoff rules

- Use an absolute local file path.
- Keep HTML self-contained when possible; remote assets can disappear or be blocked.
- Never upload environment files, access tokens, cookies, private keys, or credential-bearing logs.
- Never reveal `HTML2LINK_API_TOKEN` or `updateToken` in the user-facing response.
- Do not describe a link as private or permanent.
- On success, provide a concise clickable link. On failure, state the blocker and next required action.
