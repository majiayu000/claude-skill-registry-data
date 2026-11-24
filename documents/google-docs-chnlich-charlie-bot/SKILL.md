---
name: google-docs
description: Use when the user asks to read, create, or edit Google Docs documents, or import a PPTX deck into Google Slides.
version: 1.1.0
---

# Google Docs

Read, create, and edit Google Docs using the Google Docs API with a selected Google account.

**IMPORTANT: User approval required for all writes.** Before any create, update, append, or move action, show the planned content first and wait for explicit `take off` approval. Do not mutate anything before that approval.

## Configuration

The shared Google credential configuration is defined once in the **google-oauth** skill: `skills/google-oauth/SKILL.md`.

The `google` section can set `docs_default_folder_id` for the default account.

## API Reference

Send every Google API request through `charliebot google request`.
The command mints the selected account's access token inside its own process, so the token never appears in a command, in the output or in a run record.
A JSON body goes in `--json`, which sets `Content-Type: application/json`; `--data-file <path>` reads the body from a file instead.
The command prints the response body on stdout and exits 0 for an HTTP 2xx answer; another status exits 1.

### Choose the Account

Choose the account using the **Accounts** section in the **google-oauth** skill.
Pass `--account <name>` on every request, and omit `--account` for the default account.

If the refresh token is invalid or revoked, follow **Add or Re-Authorize an Account** in the **google-oauth** skill: `skills/google-oauth/SKILL.md`.

### Create a Google Doc

Docs API create defaults to the user's root folder:

```bash
charliebot google request POST https://docs.googleapis.com/v1/documents --json '{"title":"Document Title"}'
```

After a successful create, return the editor URL:

`https://docs.google.com/document/d/{documentId}/edit`

If you need explicit folder placement, use the Drive API instead. Docs API create does not place the doc into a chosen folder.

### Read a Document

```bash
charliebot google request GET "https://docs.googleapis.com/v1/documents/DOCUMENT_ID"
```

To turn `documents.get` JSON into readable plain text, walk `body.content[]`, then each `paragraph.elements[]`, and concatenate any `textRun.content` values. Preserve paragraph breaks when a paragraph ends; ignore non-paragraph structural elements unless you need tables, headers, or footnotes.

### Append or Write Content

Use `documents.batchUpdate` with `insertText` requests:

```bash
charliebot google request POST "https://docs.googleapis.com/v1/documents/DOCUMENT_ID:batchUpdate" \
  --json '{"requests":[{"insertText":{"location":{"index":1},"text":"Hello, world\n"}}]}'
```

For appending to an existing doc, fetch the current document first and insert at the last body `endIndex - 1`. For a freshly created empty doc, `index: 1` is the usual insertion point.

### Formatting Content

After inserting text, use `updateParagraphStyle` and `updateTextStyle` in the same `batchUpdate` to apply formatting. Requests are applied in order, so insert text first, then style it.

**Headings** — set a paragraph's named style (HEADING_1 through HEADING_6, or NORMAL_TEXT):

```json
{
  "updateParagraphStyle": {
    "range": { "startIndex": 1, "endIndex": 25 },
    "paragraphStyle": { "namedStyleType": "HEADING_1" },
    "fields": "namedStyleType"
  }
}
```

**Bold / Italic** — set text style on a character range:

```json
{
  "updateTextStyle": {
    "range": { "startIndex": 1, "endIndex": 25 },
    "textStyle": { "bold": true },
    "fields": "bold"
  }
}
```

**Practical tips:**
- Use `fields` to specify which style properties to update (e.g. `"bold"`, `"namedStyleType"`, `"bold,italic"`). Omitting `fields` clears unset properties.
- To find the correct index range for inserted text: if you insert N characters at index I, the text occupies `[I, I+N)`.

### Folder Behavior

- `documents.create` always creates in root.
- To create directly inside a folder or move a document later, use the Drive API.
- Typical Drive operations:
  - create a Google Doc with `mimeType: application/vnd.google-apps.document` and `parents: ["FOLDER_ID"]`
  - move an existing doc with `files.update(addParents=..., removeParents=...)`

Use Drive API placement only after the write plan is approved.
For another account, create the document in that account's Drive root and state the location in the write draft.

## Import a PPTX as Google Slides

Upload a PPTX with conversion to Google Slides, then check these known effects:

- Conversion replaces fonts that Google does not host (Microsoft YaHei and Courier New are common casualties): name Google Fonts families in the deck, for example Noto Sans SC for CJK text and Roboto Mono for code. Verify by exporting to PDF and listing the embedded fonts.
- Full-width punctuation directly followed by a Latin word is treated as unbreakable and wraps to the next line's start. Insert a plain space after the punctuation.
- Speaker notes survive the import.
- The PDF export takes each paragraph-end mark's font from that paragraph's `a:endParaRPr`, which overrides the theme or table default. Give every paragraph an `a:endParaRPr` with its last run's typeface and size.
- Assert at build time that every text box lies inside the slide. A box that crosses the slide edge keeps its unwrapped line, so the page clips text that a box-local line check passes.

## Bootstrap / Re-Authorization

Choose an account in the **Accounts** section and follow **Add or Re-Authorize an Account** in the **google-oauth** skill: `skills/google-oauth/SKILL.md`.
