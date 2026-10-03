---
name: upload-gist
description: Upload markdown/text content to GitHub Gist via API
tags: [github, gist, upload]
---

# upload-gist

Upload markdown/text content to GitHub Gist using the raw GitHub API or the `gh` CLI, reading the token from `~/.hermes/.env`.

## Prerequisites

- `~/.hermes/.env` must contain `GITHUB_TOKEN=<token>` with `gist` scope
- `gh` CLI must be installed (skill auto-installs if missing)

## Workflow

### Step 1: Read the token from .env

```bash
grep '^GITHUB_TOKEN=' ~/.hermes/.env | cut -d'=' -f2-
```

If `GITHUB_TOKEN` is missing from the file, ask the user for a GitHub token with `gist` scope: https://github.com/settings/tokens

### Step 2: Install gh CLI if not present

```bash
command -v gh >/dev/null 2>&1 || {
  (
    type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)
    sudo mkdir -p -m 755 /etc/apt/keyrings
    wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg >/dev/null
    sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null
    sudo apt update
    sudo apt install gh -y
  )
}
```

### Step 3: Test the token

Fine-grained tokens don't work with `gh auth login --with-token`. Instead, test via API:

```bash
GH_TOKEN="$(grep '^GITHUB_TOKEN=' ~/.hermes/.env | cut -d'=' -f2-)"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" https://api.github.com/user \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github.v3+json")
if [ "$RESPONSE" = "200" ]; then
    echo "Token is valid"
else
    echo "Token validation failed with HTTP $RESPONSE"
    exit 1
fi
```

### Step 4: Create gist (Always use the Raw API approach)

The raw API approach works reliably with both fine-grained and classic tokens. Avoid `gh` — it requires interactive auth or classic tokens that don't work well with `--with-token`.

**CRITICAL:** To avoid `JSONDecodeError` or `API Error HTTP 422` caused by control characters or improper escaping in the content, **do not rely on shell interpolation**. Use a Python wrapper (via `execute_code`) to generate the JSON payload.

**Recommended Implementation (Python):**
1. Read token from `~/.hermes/.env`.
2. Use `json.dumps()` to create a valid JSON string of the payload.
3. Use `requests` or `curl` to POST to `https://api.github.com/gists`.

Example payload structure:
```json
{
  "description": "Description",
  "public": true,
  "files": {
    "filename.md": { "content": "Actual content here" }
  }
}
```

### Step 5: Verify

```bash
GH_TOKEN="$(grep '^GITHUB_TOKEN=' ~/.hermes/.env | cut -d'=' -f2-)"
FILEID=$(basename "$(echo $GIST_URL | rev | cut -d/ -f1 | rev)")
curl -s -o /dev/null -w "HTTP %{http_code}" https://gist.github.com/$FILEID \
  -H "Authorization: Bearer $GH_TOKEN"
```

## Error Handling

| Error | Fix |
|------|-----|
| `gh: command not found` | Run the install step (Step 2) |
| Token returns 404 on `/user` | Token expired or invalid — ask for new token from https://github.com/settings/tokens |
| `GITHUB_TOKEN not found in .env` | Ask the user to add it to `~/.hermes/.env` |
| `API Error HTTP 422` | Content might contain unescaped characters — use Python `json.dumps()` for the payload |

## Common Pitfalls

1. **Fine-grained tokens + `gh`**: Fine-grained tokens do NOT work with `gh auth login --with-token`. Use the raw API approach instead.
2. **Control Characters**: Raw text content often contains characters that break shell-interpolated JSON. Always use `json.dumps()` in Python.
3. **`GITHUB_TOKEN=` contains trailing whitespace**: Use `cut -d'=' -f2-` and quote the variable.
4. **Python `requests` and `curl` may timeout in sandbox**: If `curl` fails, fall back to Python `urllib` or `requests`.

## Tips

- Always use the **raw GitHub API** (`/gists`) instead of `gh gist create` — it works with any token type and avoids auth complexity.
- **Minimum scope for gist upload:** `gist`
- For private gists: change `'public': True` to `'public': False`
- After creating, always return the gist URL to the user.
