---
name: purge-private-info
description: "Scan the repo for private/confidential information and remove, rename, or replace it. Use when: (1) User says 'purge private info', 'check for secrets', or 'scan for credentials', (2) Before making a repo public, (3) User wants to ensure no client names, passwords, or personal info are exposed."
---

# Purge Private Info

The user is unsure whether unwanted private or confidential information exists in this repository. Your job is to thoroughly scan and identify any such information, then remove, rename, or replace it.

## Priority Levels

### HIGH PRIORITY (most important — always fix)

1. **Client/corporate information** — Company names that appear to be real clients (e.g., Sony, Rakuten, Yahoo, any recognizable corporation or brand that seems like an actual work client, not a generic example)

- In file contents (code, config, comments, docs)
- In directory names and file names
- In project names, package names, or identifiers
- In URLs referencing client domains or systems

2. **Passwords and secrets**

- Hardcoded passwords, API keys, tokens, secrets
- `.env` files with real credentials committed to the repo
- Private keys, certificates
- Database connection strings with credentials

### MEDIUM PRIORITY (fix when found)

1. **Concrete personal SNS accounts** — Real Twitter/X handles, GitHub usernames (other than the repo owner), Instagram, Facebook profiles, etc. that identify specific individuals
2. **Personal blog URLs** — URLs pointing to specific individuals' personal blogs or websites (other than the repo owner's)

## Scan Process

### Step 1: Broad Scan

Use parallel searches to scan the repository efficiently:

1. **Search file/directory names** for client-like or corporate names
- Look at directory structure for project names that might be client names
2. **Search file contents** for:
- Known corporate/brand names that look like client references (not generic library/tool names)
- Patterns like `password`, `secret`, `api_key`, `token`, `credential`, `apiKey`, `API_KEY`, `SECRET`, `PRIVATE_KEY`
- `.env` files or similar config with sensitive values
- SNS URLs: `twitter.com/`, `x.com/`, `instagram.com/`, `facebook.com/`, `github.com/` (check if they reference specific personal accounts)
- Personal blog-like URLs
3. **Check git history** (recent commits) for accidentally committed secrets

### Step 2: Analyze Findings

For each finding, classify it:

- **Clearly private** — Real client name, actual password, real SNS account → Fix immediately
- **Probably private** — Looks like it could be a client name or personal info → Ask user
- **False positive** — Library name, tool name, generic example → Skip

### Step 3: Fix Issues

For confirmed private information:

- **Client/project names in code** → Replace with generic placeholders (e.g., `acme-corp`, `example-project`, `client-project`)
- **Client/project names in filenames/dirs** → Rename to generic names
- **Passwords/secrets** → Remove the value, replace with placeholder like `YOUR_API_KEY_HERE` or `changeme`
- **SNS accounts** → Replace with generic example (e.g., `@example_user`, `https://twitter.com/example`)
- **Personal blog URLs** → Replace with `https://example.com/blog`

### Step 4: Report

After fixing, provide a summary:

1. What was found and fixed
2. What was flagged but skipped (with reason)
3. Any items you're unsure about (ask the user)

## Important Notes

- **When unsure, always ask the user** before making changes
- Do NOT flag common library/tool names as client info (e.g., "google" in `googleapis`, "amazon" in `aws-sdk` are fine)
- Do NOT flag the repo owner's own information as private (their own GitHub, their own blog)
- Be thorough — check all file types including markdown, config files, scripts, and comments
- Consider git-ignored files too if they exist in the working tree
- After making changes, verify the code still works if applicable
