---
name: gumroad-upload-management
description: Automate Gumroad product image uploads and listing maintenance with Selenium and Chrome profile sessions. Use when users ask to upload or replace Gumroad product images, map local image files to product pages, run `gumroad_image_uploader.py`, troubleshoot Chrome/Selenium session failures, or verify upload results from logs.
---

# Gumroad Upload Management

## Run Workflow

1. Ensure image files exist in `C:\Users\issda\OneDrive\Downloads` or `C:\Users\issda\Downloads`.
2. Prefer a preview first with `--dry-run`.
3. Run the real upload after preview confirms product-image matches.
4. Confirm success using `gumroad_upload.log`.

## Commands

Use these commands in order.

```powershell
# Start Chrome with remote debugging for stable attach mode
Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9222","https://app.gumroad.com/products"

# Dry-run preview (no upload)
python C:\Users\issda\.codex\skills\gumroad-upload-management\scripts\gumroad_image_uploader.py --debugger-address 127.0.0.1:9222 --images-dir "C:\Users\issda\OneDrive\Downloads" --dry-run

# Real upload
python C:\Users\issda\.codex\skills\gumroad-upload-management\scripts\gumroad_image_uploader.py --debugger-address 127.0.0.1:9222 --images-dir "C:\Users\issda\OneDrive\Downloads"
```

## Match Rules

- Match images to products by filename token overlap.
- Skip unmatched products instead of guessing.
- Rename files with product-identifying words when matching fails.

## Troubleshooting

Read `references/troubleshooting.md` when Selenium or Gumroad page automation fails.

## Artifacts

- Script: `scripts/gumroad_image_uploader.py`
- Log file output: `gumroad_upload.log`
