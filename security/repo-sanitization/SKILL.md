---
name: repo-sanitization
description: Sanitize a private Hermes or agent repo for secure sharing or open-sourcing — scan for credentials, replace with placeholders, create templates, verify nothing personal leaked.
category: devops
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [repo-sanitization, open-source, credentials, security, secrets, git]
    triggers:
      - sanitize repo for sharing
      - prepare repo for open source
      - remove credentials from repo
      - make repo public safe
      - clean config for distribution
    related_skills: [hermes-system-backup, buzz-relay-ops]
---

# Repo Sanitization

Prepare a private agent setup for sharing or open-sourcing by removing
all personal credentials, paths, and identifiers while preserving
the full structure and functionality.

## When to Run

- Before making a private repo public
- When sharing configs as reference/template
- After discovering credentials in tracked files
- Before generating example/template configs
- Part of regular repo maintenance

## Method: Scan → Replace → Template → Verify

### Step 1: Scan for Personal Info

Search the entire repo for these patterns. Use `search_files` with
regex patterns and `grep -rn` for cross-file checks:

| Pattern | Example | Severity |
|---------|---------|----------|
| API keys | `sk-...`, `ghp_...`, `xoxp-...`, `hf_...` | 🔴 HIGH |
| Email + password | `user@gmail.com` + app password | 🔴 HIGH |
| Windows paths | `C:\Users\<user>\...` | 🟡 MEDIUM |
| Discord IDs | 17-19 digit numbers | 🟡 MEDIUM |
| Personal names | user's real name, nickname | 🟢 LOW |
| Private keys | 64-char hex Nostr secrets | 🔴 HIGH |
| Slack tokens | `xoxb-...`, `xoxp-...` | 🔴 HIGH |

Reference patterns file: `references/credential-patterns.md`

### Step 2: Sanitize Config Files

Apply these replacements to YAML config files:

```python
import re

def sanitize_yaml(content):
    """Replace personal info in config YAML with placeholders."""
    # Windows absolute paths → $HOME
    content = re.sub(r'C:\\\\Users\\\\\w+', r'$HOME', content)
    content = re.sub(r'C:/Users/\w+', r'$HOME', content)
    
    # Gmail credentials
    content = re.sub(
        r'GMAIL_SENDER_PASSWORD:\s*\S+',
        r'GMAIL_SENDER_PASSWORD: REPLACE_WITH_YOUR_APP_PASSWORD',
        content
    )
    content = re.sub(
        r'GMAIL_SENDER_EMAIL:\s*\S+',
        r'GMAIL_SENDER_EMAIL: REPLACE_WITH_YOUR_EMAIL@gmail.com',
        content
    )
    
    # Discord IDs at YAML keys — the single quotes matter
    content = re.sub(r"'?[0-9]{17,19}'?", "'<discord-channel-id>'", content)
    
    # Personal names
    content = content.replace('UserRealName', 'User')
    
    return content
```

⚠️ **Run this on the REPO COPY, not the live config.** The live
config at `C:\Users\<user>\AppData\Local\hermes\config.yaml` is what
Hermes reads — it must retain real credentials.

### Step 3: Redact Key Files

For Nostr key files and similar JSON stores:

```python
import json

def redact_keys(data: dict) -> dict:
    """Truncate secret keys for safe repo storage."""
    for name, entry in data.items():
        if 'secret_key' in entry and len(str(entry['secret_key'])) > 20:
            sk = entry['secret_key']
            entry['secret_key'] = sk[:8] + '...' + sk[-8:]
        if 'public_key' in entry and len(str(entry['public_key'])) > 20:
            pk = entry['public_key']
            entry['public_key'] = pk[:16] + '...'
    return data
```

### Step 4: Create .env.example Templates

```env
# Copy to .env and fill in your values

# Required
BUZZ_RELAY_URL=ws://localhost:3000
BUZZ_SECRET_KEY=<generate-with: python generate_buzz_keys.py>
BUZZ_PUBLIC_KEY=<from-key-generation>
BUZZ_CHANNELS=general

# Optional
DISCORD_BOT_TOKEN=
```

### Step 5: Create Sanitized .example.yaml Copies

After sanitizing the tracked config files, create distribution copies:

```bash
cp config/config.yaml config/config.example.yaml
cp config/gateway.yaml config/gateway.example.yaml
```

### Step 6: Update .gitignore

Always protect:
```
.env
.env.*
!.env.example
*.key
*.pem
__pycache__/
*.db
*.sqlite*
*.log
.hermes/
```

### Step 7: Verify

Final scan across ALL tracked files:

```python
import re

BAD_PATTERNS = [
    (r'youraccount|youraccount2', 'personal email'),
    (r'${GMAIL_APP_PASSWORD}|${GMAIL_APP_PASSWORD}', 'gmail password'),
    (r'sk-[a-zA-Z0-9]{20,}', 'API key (sk-...)'),
    (r'[0-9]{17,19}', 'Discord ID'),
    (r'C:\\\\Users\\\\\w+|C:/Users/\w+', 'Windows path'),
]

for file in all_files:
    content = open(file).read()
    for pat, label in BAD_PATTERNS:
        if re.search(pat, content):
            raise Exception(f"UNSANITIZED: {label} in {file}")
```

## Pitfalls

### 🚨 Gmail app passwords are the #1 leak
Always check these 4 locations:
1. `GMAIL_SENDER_PASSWORD:` in YAML configs (2+ copies)
2. `ACCOUNT1_PASSWORD =` in Python scripts
3. Spaced version `"${GMAIL_APP_PASSWORD}"` (quoted, with spaces)
4. `.example.yaml` files that were copied from unsanitized originals

### 🚨 .example files go stale
Always regenerate `.example.yaml` files AFTER sanitizing the originals:
```python
shutil.copy('config/config.yaml', 'config/config.example.yaml')
```

### 🚨 .hermes/ directory in repo
The `.hermes/` directory is a local config copy that shouldn't be tracked.
Remove it from git and add to `.gitignore`:
```bash
git rm -r --cached .hermes/
echo ".hermes/" >> .gitignore
```

### 🚨 Discord IDs at YAML keys
The regex `r"'?[0-9]{17,19}'?"` catches IDs whether quoted or bare.
In YAML, they often appear as:
```yaml
'<discord-channel-id>': 'You are now Architect...'
```

### 🚨 Redacted keys lose sync
After running step 3 on `buzz_keys.json`, the redacted file is for
documentation only. Real keys stay in `.env` files (gitignored).
If someone clones the repo and runs key generation, they get fresh
keys — no need to un-redact.

### 🚨 Script files with embedded credentials
Python scripts like `scripts/email_intelligence.py` often embed Gmail credentials
directly in source code. These are EASY to miss because they look like configuration:

```python
# BAD — embedded credentials
ACCOUNT1_EMAIL = "<your-email>@gmail.com"
ACCOUNT1_PASSWORD = "${GMAIL_APP_PASSWORD}"    # <-- spaced version of app password
ACCOUNT2_EMAIL = "<your-email>@gmail.com"
```

Always scan `scripts/` directory for these patterns. The spaced version
(`"${GMAIL_APP_PASSWORD}"`) is a Gmail app password with spaces inserted every
4 chars — match the concatenated form too.

### 🚨 .example.yaml files go stale
`.example.yaml` files created BEFORE the originals were sanitized will contain
the original personal data. ALWAYS regenerate them from the now-sanitized originals:

```python
import shutil
shutil.copy('config/config.yaml', 'config/config.example.yaml')
shutil.copy('config/gateway.yaml', 'config/gateway.example.yaml')
```

### 🚨 SOUL.md and omniroute docs
Personal names often appear in `config/SOUL.md`, `config/omniroute/*.md`, and
other markdown documentation files. These are easy to miss because they look
like prose rather than config:

```bash
# Check for personal names in ALL markdown files
grep -rn "UserRealName" . --include="*.md"
```

Replace with "User" or "The Operator".

### 🚨 .hermes/ directory tracked in git
The `.hermes/` directory is a local config copy and should NOT be in the repo.
If it was tracked previously:

```bash
git rm -r --cached .hermes/
echo ".hermes/" >> .gitignore
git add .gitignore && git commit -m "fix: remove tracked .hermes, add to gitignore"
```

## References

- `references/credential-patterns.md` — regex patterns by credential type
