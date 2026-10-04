---
name: r2-upload
description: >
  Upload images or files to Cloudflare R2 and get back a permanent public URL.
  Use this skill whenever any other skill (image generation, cover creation,
  infographic, comic, slide deck, etc.) produces an image that needs to be
  hosted or shared as a public URL. Also trigger directly when the user asks
  to "upload to R2", "store image on R2", "get a public URL for this image",
  "host this image", "save to Cloudflare", or "把图片上传到 R2". Supports
  local file paths, base64 / data-URL strings, and remote URLs (fetch +
  re-upload). Always invoke this skill rather than writing ad-hoc upload code.
metadata: 
  version: v1.0.0
  author: jiangding01
---

# R2 Upload Skill

Upload a file to Cloudflare R2 and return its permanent public URL.

---

## Step 0 — First-time setup (only when something fails)

Skip this step entirely if the user has used r2-upload before without issues —
go straight to Step 2. `upload.py` already reports clear errors on its own.

Run the environment checker **only when**:
- This is the user's first time using the skill, **or**
- An upload just failed with an unfamiliar error

```bash
python3 ~/.claude/skills/r2-upload/scripts/check_env.py
```

The script outputs JSON and exits with code 0 (all OK) or 1 (issues found).
Read the `fix` field of each failing item and work through them in order:

1. `python_version` fails → Python is too old or missing
2. `boto3` fails → run `pip3 install boto3`
   *(Note: `upload.py` already detects this and prints the install command itself — you may not need check_env.py for this one)*
3. Any `R2_*` env var fails → walk the user through setting it up (see below)

After applying fixes, re-run the checker to confirm before proceeding.

### If check_env.py itself fails to run (Python not found)

```
Python 3 is not available on this system. Please install it:
- macOS:   brew install python3  OR download from https://python.org
- Ubuntu:  sudo apt install python3
- Windows: download from https://python.org
After installation, restart your terminal and try again.
```

---

## Step 1 — First-time setup guide

Only needed when env var checks fail. Walk the user through this:

### 1a. Create a Cloudflare R2 bucket (if not already done)

1. Go to **Cloudflare Dashboard → R2**
2. Click **Create bucket**, choose a name (e.g. `my-assets`)
3. In bucket **Settings → Public Access**, enable public access
4. Copy the `pub-xxx.r2.dev` URL shown — this is `R2_PUBLIC_URL`

### 1b. Create an R2 API token

1. Go to **Cloudflare Dashboard → R2 → Manage API tokens**
2. Click **Create API token**
3. Set permissions: **Object Read & Write** on your specific bucket
4. Save the generated **Access Key ID** (`R2_ACCESS_KEY_ID`) and **Secret Access Key** (`R2_SECRET_ACCESS_KEY`)
5. Your **Account ID** appears in the URL: `dash.cloudflare.com/<account_id>/`

### 1c. Set environment variables

Ask the user to add these five lines to their shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export R2_ACCOUNT_ID="<your-cloudflare-account-id>"
export R2_ACCESS_KEY_ID="<your-r2-token-key-id>"
export R2_SECRET_ACCESS_KEY="<your-r2-token-secret>"
export R2_BUCKET_NAME="<your-bucket-name>"
export R2_PUBLIC_URL="https://pub-xxx.r2.dev"
```

Then reload the shell:
```bash
source ~/.zshrc   # or source ~/.bashrc
```

After reloading, re-run the checker to confirm.

---

## Step 2 — Running the upload

### Auto-prefix by file type

When `--prefix` is not specified, the script automatically picks a prefix based on the
detected MIME type:

| File category | Auto prefix |
|---------------|-------------|
| Images (`image/*`) | `images` |
| Videos (`video/*`) | `videos` |
| Audio  (`audio/*`) | `audios` |
| Everything else    | `files`  |

You can always override this with `--prefix` for finer-grained organisation
(e.g. `--prefix images/covers`).

### From a local file (preferred)
```bash
python3 ~/.claude/skills/r2-upload/scripts/upload.py \
  --file /path/to/image.png \
  [--prefix images/covers] \
  [--name my-image] \
  [--bucket my-other-bucket]
```

### From a base64 / data-URL string
```bash
# Short strings — inline is fine
python3 ~/.claude/skills/r2-upload/scripts/upload.py \
  --base64 "data:image/png;base64,iVBORw0KGgo..."

# Long strings — always use --base64-file to avoid shell ARG_MAX limits
printf '%s' "<base64-data>" > /tmp/r2_b64.txt
python3 ~/.claude/skills/r2-upload/scripts/upload.py \
  --base64-file /tmp/r2_b64.txt
rm -f /tmp/r2_b64.txt
```

### From a remote URL (fetch + re-upload)
```bash
python3 ~/.claude/skills/r2-upload/scripts/upload.py \
  --url "https://example.com/photo.jpg"
```

### All options

| Flag                    | Description                                                    |
|-------------------------|----------------------------------------------------------------|
| `--file`                | Path to a local file                                           |
| `--base64`              | Base64 string or data URL (`data:image/png;base64,…`)          |
| `--base64-file`         | Path to a file containing base64 data (recommended for large payloads) |
| `--url`                 | Remote image URL to fetch and re-upload                        |
| `--prefix`              | Path prefix inside the bucket, e.g. `images/covers`           |
| `--name`                | Custom filename without extension (auto-generated if omitted)  |
| `--content-type`        | Override auto-detected MIME type                               |
| `--bucket`              | Override default bucket (`R2_BUCKET_NAME` env var)             |
| `--cache-control`       | Cache-Control header (default: `public, max-age=31536000, immutable`) |
| `--content-disposition` | Content-Disposition header, e.g. `attachment; filename=doc.pdf` |
| `--timeout`             | Network timeout in seconds (default: 60)                       |

---

## Step 3 — Output

On success, the script prints one JSON line to **stdout**:

```json
{
  "url": "https://pub-xxx.r2.dev/images/covers/my-image-a1b2c3d.png",
  "key": "images/covers/my-image-a1b2c3d.png",
  "size": 204800,
  "contentType": "image/png",
  "uploadedAt": 1710835200000
}
```

Capture the URL in a shell variable:
```bash
RESULT=$(python3 ~/.claude/skills/r2-upload/scripts/upload.py --file /tmp/out.png)
URL=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['url'])")
echo "Uploaded: $URL"
```

On error, the script writes to **stderr** and exits with a non-zero code.
Surface the full error message to the user.

### Presenting the URL to the user

Always display the final URL inside a code block so it can be copied in full
without line-break truncation:

```
`https://pub-xxx.r2.dev/images/my-image-a1b2c3d.png`
```

Never paste the URL as plain inline text — long URLs wrap in the terminal and
are easy to copy incompletely.

---

## Integration pattern for other skills

When another skill generates a file and wants a hosted URL, the prefix is chosen
automatically based on file type (images → `images/`, videos → `videos/`, etc.),
so you rarely need to pass `--prefix` explicitly.

```bash
# 1. Upload — prefix is auto-selected from MIME type
OUTPUT=$(python3 ~/.claude/skills/r2-upload/scripts/upload.py \
  --file /tmp/skill_output.png)

# 2. Extract URL
URL=$(echo "$OUTPUT" | python3 -c "import sys,json; print(json.load(sys.stdin)['url'])")
echo "Hosted at: $URL"
```

If the upload fails, run `check_env.py` to diagnose the issue.

Pass `--prefix` only when you need a specific sub-path (e.g. `--prefix images/covers`).

---

## Troubleshooting upload errors

| Error message | Likely cause | Fix |
|---------------|-------------|-----|
| `Missing required environment variable` | Env var not set | Re-run `check_env.py` and follow its `fix` instructions |
| `ModuleNotFoundError: No module named 'boto3'` | boto3 not installed | `pip3 install boto3` |
| `Upload failed: InvalidAccessKeyId` | Wrong key ID | Check `R2_ACCESS_KEY_ID` in Cloudflare R2 → Manage API tokens |
| `Upload failed: SignatureDoesNotMatch` | Wrong secret | Regenerate API token and update `R2_SECRET_ACCESS_KEY` |
| `Upload failed: NoSuchBucket` | Bucket doesn't exist | Create the bucket in Cloudflare Dashboard first |
| `Failed to fetch URL (HTTP 403)` | Remote URL is access-controlled | Download manually, use `--file` instead |
| `Remote file is too large` | File exceeds 500 MB limit | Download the file manually and use `--file` instead |
| `File is too large` | Local file exceeds 500 MB limit | Split or compress the file before uploading |
| `Decoded data is too large` | base64 payload exceeds 500 MB after decoding | Use a smaller file or compress first |
| `Invalid base64 data` | Corrupted or truncated base64 string | Re-generate the base64 data and try again |
| `File not found` | Path passed to `--file` or `--base64-file` does not exist | Check the file path and try again |
| URL returns 403 after upload | Bucket not public | Enable "Public access" in R2 bucket → Settings |
