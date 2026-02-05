---
name: atlassian-attachments
description: Attach documents, screenshots, PDFs, and files to Jira issues and Confluence pages via REST API. Use when uploading evidence, documentation, or media to Atlassian products.
---

# Atlassian Attachments Skill

Attach files, screenshots, and documents to Jira issues and Confluence pages using the Atlassian REST API.

## Authentication Setup

### API Token (Required)

Generate an API token at: https://id.atlassian.com/manage-profile/security/api-tokens

### Environment Variables

```bash
export ATLASSIAN_DOMAIN="your-domain"
export ATLASSIAN_EMAIL="your-email@example.com"
export ATLASSIAN_API_TOKEN="your-api-token"
```

### Setup via .envrc (Recommended)

If environment variables are not set, add them to `.envrc` in your project root for automatic loading with [direnv](https://direnv.net/):

```bash
# .envrc
export ATLASSIAN_DOMAIN="your-domain"
export ATLASSIAN_EMAIL="your-email@example.com"
export ATLASSIAN_API_TOKEN="your-api-token"
```

Then allow the file:
```bash
direnv allow
```

**Security Note:** Add `.envrc` to `.gitignore` to prevent committing credentials:
```bash
echo ".envrc" >> .gitignore
```

### Check Environment Setup

```bash
# Verify variables are set
echo "Domain: ${ATLASSIAN_DOMAIN:-NOT SET}"
echo "Email: ${ATLASSIAN_EMAIL:-NOT SET}"
echo "Token: ${ATLASSIAN_API_TOKEN:+SET}"
```

If any show "NOT SET", prompt the user to configure `.envrc`.

### Base URLs

```
Jira:       https://{domain}.atlassian.net/rest/api/3
Confluence: https://{domain}.atlassian.net/wiki/rest/api
```

## Jira REST API - Upload Attachments

### Endpoint

```
POST https://{domain}.atlassian.net/rest/api/3/issue/{issueIdOrKey}/attachments
```

### Required Headers

| Header | Value | Purpose |
|--------|-------|---------|
| `X-Atlassian-Token` | `no-check` | CSRF protection bypass (required) |
| `Content-Type` | `multipart/form-data` | File upload format |

### cURL Command

```bash
curl --location --request POST \
  'https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123/attachments' \
  -u 'email@example.com:<api_token>' \
  -H 'X-Atlassian-Token: no-check' \
  --form 'file=@"./screenshots/bug-evidence.png"'
```

### Python Example

```python
import requests
from requests.auth import HTTPBasicAuth

def upload_jira_attachment(domain, email, api_token, issue_key, file_path):
    url = f"https://{domain}.atlassian.net/rest/api/3/issue/{issue_key}/attachments"

    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "X-Atlassian-Token": "no-check"
    }

    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, auth=auth, headers=headers, files=files)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")

# Usage
result = upload_jira_attachment(
    domain="your-domain",
    email="your-email@example.com",
    api_token="your-api-token",
    issue_key="PROJ-123",
    file_path="./screenshots/bug-evidence.png"
)
```

### Bash Script - Multiple Files

```bash
#!/bin/bash
DOMAIN="your-domain"
EMAIL="your-email@example.com"
API_TOKEN="your-api-token"
ISSUE_KEY="PROJ-123"
FILES_DIR="./qa-tests/screenshots/"

for file in "$FILES_DIR"*.png; do
    echo "Uploading: $file"
    curl --silent --location --request POST \
      "https://${DOMAIN}.atlassian.net/rest/api/3/issue/${ISSUE_KEY}/attachments" \
      -u "${EMAIL}:${API_TOKEN}" \
      -H "X-Atlassian-Token: no-check" \
      --form "file=@\"$file\""
    echo " Done"
done
```

## Confluence REST API - Upload Attachments

### Endpoint

```
POST https://{domain}.atlassian.net/wiki/rest/api/content/{pageId}/child/attachment
```

### Required Headers

| Header | Value | Purpose |
|--------|-------|---------|
| `X-Atlassian-Token` | `nocheck` | CSRF protection bypass (required) |
| `Content-Type` | `multipart/form-data` | File upload format |

### cURL Command - Basic Auth

```bash
curl -u "${USER_EMAIL}:${API_TOKEN}" \
  -X POST \
  -H "X-Atlassian-Token: nocheck" \
  -F "file=@./diagram.png" \
  -F "comment=Uploaded via REST API" \
  "https://${DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}/child/attachment"
```

### cURL Command - Personal Access Token

```bash
curl -X POST \
  -H "Authorization: Bearer ${PAT_TOKEN}" \
  -H "X-Atlassian-Token: no-check" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@./document.pdf" \
  "https://${DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}/child/attachment"
```

### Python Example

```python
import requests
from requests.auth import HTTPBasicAuth

def upload_confluence_attachment(domain, email, api_token, page_id, file_path, comment=""):
    url = f"https://{domain}.atlassian.net/wiki/rest/api/content/{page_id}/child/attachment"

    auth = HTTPBasicAuth(email, api_token)
    headers = {
        "X-Atlassian-Token": "nocheck"
    }

    with open(file_path, 'rb') as file:
        files = {'file': file}
        data = {'comment': comment} if comment else {}
        response = requests.post(url, auth=auth, headers=headers, files=files, data=data)

    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")

# Usage
result = upload_confluence_attachment(
    domain="your-domain",
    email="your-email@example.com",
    api_token="your-api-token",
    page_id="123456789",
    file_path="./docs/architecture.png",
    comment="Architecture diagram v2"
)
```

### Get Page ID by Title

```bash
# Find page ID from title
curl -u "${EMAIL}:${API_TOKEN}" \
  "https://${DOMAIN}.atlassian.net/wiki/rest/api/content?title=Page%20Title&spaceKey=SPACE" \
  | jq '.results[0].id'
```

### Embed Attachment in Page Content

After uploading, the attachment is in the page's attachment list but **NOT embedded** in content. You must update the page body to display it.

#### Important: Use Markdown, Not Wiki Markup

| Format | Syntax | Works with API? |
|--------|--------|-----------------|
| Wiki markup | `!image.png!` | **NO** - Not converted |
| Markdown | `![alt text](image.png)` | **YES** - Converted to storage format |
| Storage format | `<ac:image>...</ac:image>` | **YES** - Native format |

**Key insight:** Markdown image syntax gets automatically converted to Confluence storage format when using the API.

#### CRITICAL: Storage Format for Attachments vs External URLs

When using storage format directly, you MUST use the correct element for referencing attachments:

| Reference Type | Element | Use Case |
|----------------|---------|----------|
| Page attachment | `<ri:attachment ri:filename="..."/>` | Files uploaded to the page |
| External URL | `<ri:url ri:value="..."/>` | External image URLs |

**WRONG - Using ri:url for attachments (images won't display):**
```xml
<ac:image ac:src="screenshot.png">
  <ri:url ri:value="screenshot.png" />
</ac:image>
```

**CORRECT - Using ri:attachment for uploaded files:**
```xml
<ac:image>
  <ri:attachment ri:filename="screenshot.png" />
</ac:image>
```

The `ri:url` element is for external URLs only. For files uploaded as attachments to the page, you MUST use `ri:attachment` with `ri:filename`.

#### Method 1: Markdown (Recommended)

Use `representation: "wiki"` with Markdown syntax:

```bash
curl -u "${EMAIL}:${API_TOKEN}" \
  -X PUT \
  -H "Content-Type: application/json" \
  "https://${DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}" \
  -d '{
    "version": {"number": NEW_VERSION},
    "title": "Page Title",
    "type": "page",
    "body": {
      "wiki": {
        "value": "# My Page\n\nHere is the diagram:\n\n![Architecture Diagram](architecture.png)\n\nMore content here.",
        "representation": "wiki"
      }
    }
  }'
```

#### Method 2: Storage Format (Direct)

Use native Confluence storage format with `representation: "storage"`:

```bash
curl -u "${EMAIL}:${API_TOKEN}" \
  -X PUT \
  -H "Content-Type: application/json" \
  "https://${DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}" \
  -d '{
    "version": {"number": NEW_VERSION},
    "title": "Page Title",
    "type": "page",
    "body": {
      "storage": {
        "value": "<p>Here is the diagram:</p><ac:image ac:align=\"center\" ac:width=\"800\"><ri:attachment ri:filename=\"architecture.png\"/></ac:image>",
        "representation": "storage"
      }
    }
  }'
```

#### Storage Format Image Options

**IMPORTANT:** Always use `<ri:attachment ri:filename="..."/>` for page attachments, never `<ri:url>`.

**RECOMMENDED for QA screenshots:** Use `ac:width="600"` to prevent images from being too wide and hindering readability:

```xml
<!-- RECOMMENDED: Centered image with controlled width (best for QA screenshots) -->
<ac:image ac:align="center" ac:layout="center" ac:width="600">
  <ri:attachment ri:filename="screenshot.png"/>
</ac:image>

<!-- Basic image (attachment) - will be full width, may be too large -->
<ac:image>
  <ri:attachment ri:filename="screenshot.png"/>
</ac:image>

<!-- Element screenshots (smaller width for UI elements) -->
<ac:image ac:align="center" ac:layout="center" ac:width="400">
  <ri:attachment ri:filename="button-element.png"/>
</ac:image>

<!-- Full-width diagram (use sparingly) -->
<ac:image ac:align="center" ac:layout="center" ac:width="800">
  <ri:attachment ri:filename="architecture-diagram.png"/>
</ac:image>

<!-- As thumbnail (clickable to expand) -->
<ac:image ac:thumbnail="true">
  <ri:attachment ri:filename="photo.jpg"/>
</ac:image>

<!-- With border -->
<ac:image ac:border="true" ac:width="400">
  <ri:attachment ri:filename="ui-mockup.png"/>
</ac:image>

<!-- External URL (only for images NOT uploaded as attachments) -->
<ac:image>
  <ri:url ri:value="https://example.com/external-image.png"/>
</ac:image>
```

**Width Guidelines:**
| Image Type | Recommended Width | Notes |
|------------|-------------------|-------|
| Full page screenshots | `600` | Readable without scrolling |
| Element screenshots | `300-400` | Small UI components |
| Architecture diagrams | `800` | Complex diagrams need more space |
| Thumbnails | Use `ac:thumbnail="true"` | Clickable to expand |

#### Python Example - Upload and Embed

```python
import requests
from requests.auth import HTTPBasicAuth
import json

def upload_and_embed_image(domain, email, api_token, page_id, file_path, alt_text=""):
    base_url = f"https://{domain}.atlassian.net/wiki/rest/api"
    auth = HTTPBasicAuth(email, api_token)
    filename = file_path.split('/')[-1]

    # 1. Upload attachment
    upload_url = f"{base_url}/content/{page_id}/child/attachment"
    headers = {"X-Atlassian-Token": "nocheck"}
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(upload_url, auth=auth, headers=headers, files=files)

    if response.status_code not in [200, 201]:
        raise Exception(f"Upload failed: {response.text}")

    # 2. Get current page version
    page_url = f"{base_url}/content/{page_id}?expand=body.wiki,version"
    page = requests.get(page_url, auth=auth).json()
    current_version = page['version']['number']
    title = page['title']

    # 3. Update page with embedded image using Markdown
    update_url = f"{base_url}/content/{page_id}"

    # Get existing content or start fresh
    existing_content = page.get('body', {}).get('wiki', {}).get('value', '')

    # Append image in Markdown format
    new_content = f"{existing_content}\n\n![{alt_text}]({filename})"

    payload = {
        "version": {"number": current_version + 1},
        "title": title,
        "type": "page",
        "body": {
            "wiki": {
                "value": new_content,
                "representation": "wiki"
            }
        }
    }

    response = requests.put(
        update_url,
        auth=auth,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Update failed: {response.text}")

# Usage
upload_and_embed_image(
    domain="your-domain",
    email="your-email@example.com",
    api_token="your-api-token",
    page_id="123456789",
    file_path="./screenshots/feature-demo.png",
    alt_text="Feature Demo Screenshot"
)
```

#### Complete Workflow Script

```bash
#!/bin/bash
# upload-and-embed.sh - Upload image and embed in Confluence page

DOMAIN="${ATLASSIAN_DOMAIN}"
EMAIL="${ATLASSIAN_EMAIL}"
API_TOKEN="${ATLASSIAN_API_TOKEN}"
PAGE_ID="$1"
FILE_PATH="$2"
FILENAME=$(basename "$FILE_PATH")

# 1. Upload the attachment
echo "Uploading ${FILENAME}..."
curl -s -u "${EMAIL}:${API_TOKEN}" \
  -X POST \
  -H "X-Atlassian-Token: nocheck" \
  -F "file=@${FILE_PATH}" \
  "https://${DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}/child/attachment" > /dev/null

# 2. Get current page version
VERSION=$(curl -s -u "${EMAIL}:${API_TOKEN}" \
  "https://${DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}?expand=version" \
  | jq '.version.number')

TITLE=$(curl -s -u "${EMAIL}:${API_TOKEN}" \
  "https://${DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}" \
  | jq -r '.title')

# 3. Update page with embedded image (Markdown format)
NEW_VERSION=$((VERSION + 1))
echo "Embedding image in page (version ${NEW_VERSION})..."

curl -s -u "${EMAIL}:${API_TOKEN}" \
  -X PUT \
  -H "Content-Type: application/json" \
  "https://${DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}" \
  -d "{
    \"version\": {\"number\": ${NEW_VERSION}},
    \"title\": \"${TITLE}\",
    \"type\": \"page\",
    \"body\": {
      \"wiki\": {
        \"value\": \"![${FILENAME}](${FILENAME})\",
        \"representation\": \"wiki\"
      }
    }
  }" > /dev/null

echo "Done! Image embedded in page."
```

## Supported File Types

### Jira Attachments

| Category | Extensions | Max Size |
|----------|------------|----------|
| Images | `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp` | 10 MB |
| Documents | `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx` | 10 MB |
| Text | `.txt`, `.md`, `.csv`, `.json`, `.xml`, `.yaml` | 10 MB |
| Archives | `.zip`, `.tar`, `.gz` | 10 MB |
| Code | `.js`, `.py`, `.java`, `.ts`, `.html`, `.css` | 10 MB |

### Confluence Attachments

| Category | Extensions | Max Size |
|----------|------------|----------|
| Images | `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg` | 25 MB |
| Documents | `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx` | 100 MB |
| Media | `.mp4`, `.mov`, `.mp3` | 100 MB |
| Design | `.sketch`, `.fig`, `.psd`, `.ai` | 100 MB |

## Workflow Examples

### Attach QA Screenshot to Jira Issue

```bash
# Single screenshot
curl --location --request POST \
  "https://${DOMAIN}.atlassian.net/rest/api/3/issue/BUG-456/attachments" \
  -u "${EMAIL}:${API_TOKEN}" \
  -H "X-Atlassian-Token: no-check" \
  --form "file=@./qa-tests/screenshots/QA-20250105-001/error-state.png"
```

### Upload All Test Evidence

```bash
#!/bin/bash
ISSUE_KEY="$1"
SCREENSHOT_DIR="$2"

for file in "$SCREENSHOT_DIR"/*; do
    echo "Uploading: $(basename $file)"
    curl --silent --location --request POST \
      "https://${DOMAIN}.atlassian.net/rest/api/3/issue/${ISSUE_KEY}/attachments" \
      -u "${EMAIL}:${API_TOKEN}" \
      -H "X-Atlassian-Token: no-check" \
      --form "file=@\"$file\"" > /dev/null
done
echo "All files uploaded to ${ISSUE_KEY}"
```

### Upload Documentation to Confluence Page

```bash
# Upload PDF to specific page
PAGE_ID="123456789"
curl -u "${EMAIL}:${API_TOKEN}" \
  -X POST \
  -H "X-Atlassian-Token: nocheck" \
  -F "file=@./docs/api-specification.pdf" \
  -F "comment=API Spec v3.0" \
  "https://${DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}/child/attachment"
```

## Attachment Naming Conventions

### For QA Evidence

```
{test-id}-{description}-{timestamp}.{ext}

Examples:
- QA-20250105-001-login-error-20250105T143022.png
- QA-20250105-001-form-validation-20250105T143045.png
```

### For Bug Reports

```
{issue-key}-{description}.{ext}

Examples:
- BUG-123-stack-trace.txt
- BUG-123-screenshot-before.png
- BUG-123-screenshot-after.png
```

### For Documentation

```
{feature}-{version}-{type}.{ext}

Examples:
- auth-flow-v2-diagram.png
- api-v3-specification.pdf
- deployment-guide-v1.docx
```

## QA Screenshot to Confluence Mapping

### Local QA Structure vs Confluence Attachments

The QA test screenshots use a specific local directory structure that needs mapping when uploading to Confluence.

#### Local Structure (product-design plugin)

```
qa-tests/
├── active/
│   └── QA-20250105-001-login.md          # Test document
└── screenshots/
    └── QA-20250105-001/                   # Test ID folder
        ├── 01-initial-state.png
        ├── 02-form-filled.png
        ├── 03-success-state.png
        └── elements/
            ├── login-button.png
            ├── email-field.png
            └── password-field.png
```

#### Confluence Attachment Names (Flattened)

When uploading to Confluence, flatten the structure with prefixed names:

| Local Path | Confluence Attachment Name |
|------------|---------------------------|
| `QA-20250105-001/01-initial-state.png` | `QA-20250105-001-01-initial-state.png` |
| `QA-20250105-001/02-form-filled.png` | `QA-20250105-001-02-form-filled.png` |
| `QA-20250105-001/elements/login-button.png` | `QA-20250105-001-elem-login-button.png` |
| `QA-20250105-001/elements/email-field.png` | `QA-20250105-001-elem-email-field.png` |

#### Naming Rules

1. **Prefix with test-id**: All screenshots get `{test-id}-` prefix
2. **Element prefix**: Files from `elements/` get `-elem-` infix
3. **No nested folders**: Confluence attachments are flat
4. **Preserve sequence**: Keep `01-`, `02-` numbering

### Upload Script with Renaming

```bash
#!/bin/bash
# upload-qa-screenshots-confluence.sh
# Upload QA screenshots to Confluence with proper naming

TEST_ID="$1"
PAGE_ID="$2"
LOCAL_DIR="qa-tests/screenshots/${TEST_ID}"

# Upload main screenshots
for file in "$LOCAL_DIR"/*.png; do
    filename=$(basename "$file")
    # Prefix with test-id
    new_name="${TEST_ID}-${filename}"

    echo "Uploading: $new_name"
    curl -s -u "${ATLASSIAN_EMAIL}:${ATLASSIAN_API_TOKEN}" \
      -X POST \
      -H "X-Atlassian-Token: nocheck" \
      -F "file=@${file};filename=${new_name}" \
      "https://${ATLASSIAN_DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}/child/attachment"
done

# Upload element screenshots with elem- infix
if [ -d "$LOCAL_DIR/elements" ]; then
    for file in "$LOCAL_DIR/elements"/*.png; do
        filename=$(basename "$file")
        # Add elem- infix
        new_name="${TEST_ID}-elem-${filename}"

        echo "Uploading element: $new_name"
        curl -s -u "${ATLASSIAN_EMAIL}:${ATLASSIAN_API_TOKEN}" \
          -X POST \
          -H "X-Atlassian-Token: nocheck" \
          -F "file=@${file};filename=${new_name}" \
          "https://${ATLASSIAN_DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}/child/attachment"
    done
fi

echo "Done! All screenshots uploaded to page ${PAGE_ID}"
```

### Python Upload with Mapping

```python
import os
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path

def upload_qa_screenshots_to_confluence(
    domain: str,
    email: str,
    api_token: str,
    page_id: str,
    test_id: str,
    local_dir: str = "qa-tests/screenshots"
):
    """Upload QA screenshots with Confluence-compatible naming."""

    base_url = f"https://{domain}.atlassian.net/wiki/rest/api"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"X-Atlassian-Token": "nocheck"}

    screenshot_dir = Path(local_dir) / test_id
    uploaded = []

    # Upload main screenshots
    for file in screenshot_dir.glob("*.png"):
        confluence_name = f"{test_id}-{file.name}"
        with open(file, 'rb') as f:
            files = {'file': (confluence_name, f, 'image/png')}
            response = requests.post(
                f"{base_url}/content/{page_id}/child/attachment",
                auth=auth, headers=headers, files=files
            )
        if response.ok:
            uploaded.append({"local": str(file), "confluence": confluence_name})

    # Upload element screenshots
    elements_dir = screenshot_dir / "elements"
    if elements_dir.exists():
        for file in elements_dir.glob("*.png"):
            confluence_name = f"{test_id}-elem-{file.name}"
            with open(file, 'rb') as f:
                files = {'file': (confluence_name, f, 'image/png')}
                response = requests.post(
                    f"{base_url}/content/{page_id}/child/attachment",
                    auth=auth, headers=headers, files=files
                )
            if response.ok:
                uploaded.append({"local": str(file), "confluence": confluence_name})

    return uploaded

# Generate mapping table for documentation
def generate_mapping_table(uploaded: list) -> str:
    """Generate markdown table of local-to-confluence name mapping."""
    lines = ["| Local Path | Confluence Name |", "|------------|-----------------|"]
    for item in uploaded:
        lines.append(f"| `{item['local']}` | `{item['confluence']}` |")
    return "\n".join(lines)
```

### Updating Markdown References

After upload, update the QA test document to use Confluence attachment names:

**Before (local references):**
```markdown
![Initial state](./screenshots/QA-20250105-001/01-initial-state.png)
![Login button](./screenshots/QA-20250105-001/elements/login-button.png)
```

**After (Confluence references):**
```markdown
![Initial state](QA-20250105-001-01-initial-state.png)
![Login button](QA-20250105-001-elem-login-button.png)
```

### Automated Reference Update Script

```python
import re
from pathlib import Path

def update_qa_doc_for_confluence(qa_doc_path: str, test_id: str) -> str:
    """Update QA doc image references for Confluence."""

    content = Path(qa_doc_path).read_text()

    # Pattern: ./screenshots/{test-id}/filename.png
    # Replace with: {test-id}-filename.png
    content = re.sub(
        rf'\./screenshots/{test_id}/([^)]+\.png)',
        rf'{test_id}-\1',
        content
    )

    # Pattern: ./screenshots/{test-id}/elements/filename.png
    # Replace with: {test-id}-elem-filename.png
    content = re.sub(
        rf'{test_id}-elements/([^)]+\.png)',
        rf'{test_id}-elem-\1',
        content
    )

    return content
```

### Fixing Broken Image References in Existing Pages

If a page was created with `ri:url` instead of `ri:attachment`, images won't display. To fix:

```bash
#!/bin/bash
# fix-confluence-image-refs.sh - Fix broken image references in Confluence page

PAGE_ID="$1"

# 1. Get current page content
curl -s -u "${ATLASSIAN_EMAIL}:${ATLASSIAN_API_TOKEN}" \
  "https://${ATLASSIAN_DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}?expand=body.storage,version" \
  > /tmp/page.json

VERSION=$(jq '.version.number' /tmp/page.json)
TITLE=$(jq -r '.title' /tmp/page.json)

# 2. Extract and fix the content
jq -r '.body.storage.value' /tmp/page.json > /tmp/content.html

# Fix: Replace ri:url with ri:attachment for local filenames (not full URLs)
# This converts: <ri:url ri:value="filename.png" />
# To: <ri:attachment ri:filename="filename.png" />
sed -i '' 's/<ri:url ri:value="\([^"]*\)" \/>/<ri:attachment ri:filename="\1" \/>/g' /tmp/content.html

# Remove ac:src attribute (not needed with ri:attachment)
sed -i '' 's/ ac:src="[^"]*"//g' /tmp/content.html

# 3. Update the page
NEW_VERSION=$((VERSION + 1))
CONTENT=$(cat /tmp/content.html | jq -Rs .)

curl -s -u "${ATLASSIAN_EMAIL}:${ATLASSIAN_API_TOKEN}" \
  -X PUT \
  -H "Content-Type: application/json" \
  "https://${ATLASSIAN_DOMAIN}.atlassian.net/wiki/rest/api/content/${PAGE_ID}" \
  -d "{
    \"version\": {\"number\": ${NEW_VERSION}},
    \"title\": \"${TITLE}\",
    \"type\": \"page\",
    \"body\": {
      \"storage\": {
        \"value\": ${CONTENT},
        \"representation\": \"storage\"
      }
    }
  }"

echo "Fixed image references in page ${PAGE_ID}"
```

**Common symptoms of broken image references:**
- Images show as broken/missing icons
- Images display with blob URLs like `blob:https://media.staging.atl-paas.net/...`
- Alt text shows but image doesn't load

## Jira Attachment Commands

### Add Attachment

```
Action: Add attachment to Jira issue
Issue: PROJ-123
File: /path/to/screenshot.png

Expected behavior:
- File uploaded to issue attachments
- Visible in Attachments section
- Downloadable by team members
```

### List Attachments

```
Action: List all attachments on PROJ-123

Response format:
- screenshot.png (234 KB) - Added by John on 2025-01-05
- error-log.txt (12 KB) - Added by Jane on 2025-01-04
```

### Delete Attachment

```
Action: Remove old-screenshot.png from PROJ-123

Note: Requires appropriate permissions
```

## Confluence Attachment Commands

### Add to Page

```
Action: Attach file to Confluence page
Space: TEAM
Page: "Sprint Review"
File: /path/to/presentation.pdf
```

### Embed in Content

```
Action: Embed image in page content
Space: TEAM
Page: "Architecture Overview"
File: system-diagram.png
Position: After "System Components" heading
Width: 800px
```

### Replace Attachment

```
Action: Update existing attachment
Space: TEAM
Page: "API Docs"
File: api-spec-v2.pdf
Replace: api-spec-v1.pdf
```

## Integration with QA Workflows

### Attach QA Test Evidence

When a QA test is executed:

1. **Capture screenshots during test**
   ```
   qa-tests/screenshots/QA-20250105-001/
   ├── 01-initial-state.png
   ├── 02-form-filled.png
   └── 03-error-state.png
   ```

2. **Create/update Jira issue**
   ```
   Create bug: "Login form validation not working"
   Project: QA
   ```

3. **Attach evidence**
   ```
   Attach all screenshots from qa-tests/screenshots/QA-20250105-001/
   to the created issue
   ```

4. **Add summary comment**
   ```
   "Test execution evidence attached:
   - [^01-initial-state.png] - Before test
   - [^02-form-filled.png] - Form with test data
   - [^03-error-state.png] - Error encountered"
   ```

### Sync QA Documentation to Confluence

```
Action: Upload QA test procedure to Confluence

Steps:
1. Convert QA markdown to Confluence format
2. Create/update page in QA space
3. Attach all element screenshots
4. Embed screenshots in page content
```

## Batch Operations

### Upload Directory Contents

```
Prompt: "Upload all files from ./release-assets/ to the 'v2.0 Release' Confluence page"

Behavior:
- Scan directory for supported files
- Upload each file as attachment
- Report progress and results
```

### Sync Screenshots to Issue

```
Prompt: "Sync screenshots from ./qa-tests/screenshots/PROJ-123/ to Jira issue PROJ-123"

Behavior:
- Compare local files with existing attachments
- Upload new files
- Optionally replace updated files
- Skip unchanged files
```

## Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| File too large | Exceeds size limit | Compress or split file |
| Unsupported type | Extension not allowed | Convert to supported format |
| Permission denied | No attach permission | Request project/space access |
| Issue not found | Invalid issue key | Verify issue exists |
| Page not found | Invalid page title/space | Check space key and page title |

### Handling Large Files

```
If file > max size:
1. For images: Compress or resize
2. For documents: Split into parts
3. For archives: Use cloud storage link instead

Alternative: Upload to cloud storage and link in description
```

## Best Practices

### Organization

1. **Use consistent naming** - Follow naming conventions above
2. **Group related files** - Attach all evidence for one issue together
3. **Add descriptions** - Include context in comments
4. **Clean up old attachments** - Remove outdated files

### Performance

1. **Compress images** before upload (PNG → optimized PNG or JPEG)
2. **Batch uploads** when attaching multiple files
3. **Check existing attachments** before uploading duplicates

### Security

1. **Redact sensitive data** from screenshots
2. **Check file contents** before uploading logs
3. **Use appropriate spaces/projects** for confidential docs

## Confluence Macros for Attachments

### Image Display

```
!filename.png!                    # Basic
!filename.png|width=600!          # With width
!filename.png|thumbnail!          # As thumbnail
```

### File Links

```
[^filename.pdf]                   # Download link
[View Document^filename.pdf]      # Custom link text
```

### Gallery View

```
{gallery:include=*.png}           # All PNG attachments
{gallery:include=screenshot-*}    # Matching pattern
```

### PDF Viewer

```
{viewfile:filename.pdf}           # Inline PDF viewer
{viewfile:filename.pdf|height=600}
```
