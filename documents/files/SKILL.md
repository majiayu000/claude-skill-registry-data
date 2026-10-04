---
name: files
description: >
    How to list, get, download, and delete files attached to rows
    in tables and objects using the Frontline CLI.
allowed-tools: Bash(frontline:*)
---

# File Management

Files are binary attachments linked to individual rows. Each file has an
auto-incremented ID, original filename, content type, and size.

> **Note**: File _upload_ via CLI is not yet supported because it requires
> multipart form-data. Use the web UI or direct API calls for uploads.

## List Files for a Row

```bash
frontline object file list <object> <row-id>
frontline table file list <table> <row-id>
```

Returns an array of file objects with `id`, `originalName`, `contentType`,
`size`, and `createdAt`.

## Get File Metadata

```bash
frontline object file get <object> <file-id>
frontline table file get <table> <file-id>
```

## Download a File

```bash
# Download to current directory (uses original filename)
frontline object file download <object> <file-id>

# Download to a specific path
frontline object file download <object> <file-id> --output ./contracts/proposal.pdf
frontline table file download <table> <file-id> --output ./data/report.xlsx
```

## Delete a File

```bash
frontline object file delete <object> <file-id>
frontline table file delete <table> <file-id>
```

---

## Typical Workflow

```bash
# 1. Find the row
frontline object row list deals --search "Acme Corp"
# → row ID = 6625abc123def456

# 2. List attached files
frontline object file list deals 6625abc123def456
# → [{ id: 15, originalName: "contract_v2.pdf", size: 245000, ... }]

# 3. Download a file
frontline object file download deals 15 --output ./contract_v2.pdf

# 4. Delete an outdated file
frontline object file delete deals 15
```

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
