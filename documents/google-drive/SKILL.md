---
name: google-drive
description: Use when storing, fetching, or organizing customer documents in Google Drive ג€” file uploads from Gmail/WhatsApp attachments, folder structure per customer, link sharing.
---

# Google Drive skill

## When to invoke

- Touching `src/integrations/gdrive/` or `src/tools/store-document.ts`
- Storing classified documents (post `classify_document`)
- Generating shareable links for customer or advisor
- Migrating files between folders (status change)

## Folder structure

```
/Customers/{customer_id}_{full_name}/
  /Identification/        # ׳×׳´׳–, ׳“׳¨׳›׳•׳
  /Insurance/             # ׳₪׳•׳׳™׳¡׳•׳×
  /Pension/               # ׳§׳¨׳ ׳•׳× ׳₪׳ ׳¡׳™׳”, ׳’׳׳, ׳”׳©׳×׳׳׳•׳×
  /Income/                # ׳×׳׳•׳©׳™ ׳׳©׳›׳•׳¨׳×, ׳©׳•׳׳•׳× ׳׳¡
  /Correspondence/        # ׳׳›׳×׳‘׳™׳ ׳׳—׳‘׳¨׳•׳×
  /Signed/                # ׳׳¡׳׳›׳™׳ ׳—׳×׳•׳׳™׳ ׳¢׳ ׳™׳“׳™ ׳׳§׳•׳—
  /Misc/                  # ׳¡׳™׳•׳•׳’ ׳ ׳›׳©׳ / ׳˜׳¢׳•׳ ׳‘׳“׳™׳§׳” ׳™׳“׳ ׳™׳×
```

Folder mapping lives in `src/integrations/gdrive/folder-map.ts` ג€” single source of truth, do not hardcode elsewhere.

## Hard rules

1. **Always classify before storing** ג€” run `classify_document` first, route to correct subfolder
2. **Filename convention**: `{YYYY-MM-DD}_{doc_type}_{source}.{ext}` (e.g. `2026-05-30_pension-statement_migdal.pdf`)
3. **No PII in filenames** beyond what already exists in the folder path
4. **Permissions**: customer folders are accessible only to assigned advisor + admins. Never set "anyone with link" without explicit advisor approval
5. **Deduplicate**: hash file content (sha256) before upload ג€” if exists in customer folder, skip and log
6. **Soft delete**: never hard-delete a customer document; move to `/Archived/{customer_id}/` and log

## Sharing

Share links generated for customer signing flows must expire (7 days default). Never share a folder ג€” share specific files only.

## Error handling

Upload failure ג†’ retry once ג†’ store locally in `data/pending-upload/` and queue for retry job ג†’ alert admin if pending queue grows past 10 files.