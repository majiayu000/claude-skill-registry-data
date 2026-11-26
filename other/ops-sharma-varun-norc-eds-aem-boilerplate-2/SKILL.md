---
name: ops
description: Execute AEM Edge Delivery Services admin operations - list admins, add/remove users, preview, publish, unpublish content, clear cache, sync code, reindex, generate sitemap, manage snapshots, view logs, manage jobs, list sites, configure org/site settings, manage secrets and API keys. Also supports Document Authoring (DA) operations via admin.da.live - list/get/put content, copy, move, delete, versioning, and DA-specific preview/publish. Use for any Edge Delivery Services administrative task.
license: Apache-2.0
allowed-tools: Read, Write, Edit, Bash, Skill
metadata:
  version: "1.0.0"
---

# Edge Delivery Services Admin Operations

Execute admin operations on AEM Edge Delivery Services projects using natural language commands.

## Quick Reference

| Category | Examples |
|----------|----------|
| **Content** | preview /path, publish /path, unpublish /path, status /path |
| **Cache** | clear cache /path, force clear cache |
| **Code** | sync code, deploy code |
| **Index** | reindex /path, remove from index |
| **Sitemap** | generate sitemap |
| **Snapshots** | create snapshot X, publish snapshot X, approve snapshot X |
| **Logs** | show logs, show logs last hour |
| **Users** | add user@email as author/publish/develop, remove admin user@email, who am i |
| **Jobs** | list jobs, job status X, stop job X |
| **Sites** | list sites, switch to site-X, use branch feature-X |
| **Config** | show org config, show site config, update robots.txt |
| **Secrets** | list secrets, create secret, delete secret |
| **API Keys** | list API keys, create API key, revoke API key |
| **Tokens** | list tokens, create token, revoke token |
| **Profiles** | show profile config, create profile, delete profile |
| **Index Config** | show index config, update index config (query.yaml) |
| **Sitemap Config** | show sitemap config, update sitemap config (sitemap.yaml) |
| **Versioning** | list versions, restore version, rollback config |
| **Pages** | list pages, list all pages, show indexed pages |
| **DA (Document Authoring)** | da list, da source /path, da copy, da move, da delete, da config, da update config, da versions, da create version, da upload media, da auth |

---

## Communication Guidelines

- **NEVER use "EDS"** as an acronym for Edge Delivery Services in any responses
- Always use the full name "Edge Delivery Services" or "AEM Edge Delivery Services"
- Show clear, actionable error messages when operations fail
- Confirm destructive operations before executing — see `resources/security.md`

---

## Welcome Message

If the user invokes the skill without a specific command (e.g., just `/ops` or "help me with ops"), show:

```
Edge Delivery Services Operations

Quick commands to try:
  list pages       - Show all indexed pages
  who am i         - Check your user profile
  list sites       - Show available sites
  show site config - View site configuration
  preview /path    - Preview a content path
  show logs        - View recent activity

For the full command list: type help, /ops help, or what can you do?
```

---

## Cross-Platform Notes

Shell commands use POSIX-compatible syntax (works on macOS/Linux). On Windows, Git Bash or WSL works as-is. The agent should adapt syntax to the user's environment.

---

## Intent Router

### Step 0: Get Organization and Site (REQUIRED FIRST)

Check `~/.aem/ops-config.json` for previously stored org and site:

```bash
eval $(node -e "
  const fs = require('fs');
  try {
    const c = JSON.parse(fs.readFileSync(process.env.HOME + '/.aem/ops-config.json', 'utf8'));
    console.log('ORG=' + JSON.stringify(c.org || ''));
    console.log('SITE=' + JSON.stringify(c.site || ''));
  } catch(e) {
    console.log('ORG='); console.log('SITE=');
  }
")
echo "org=${ORG:-NOT SET} site=${SITE:-NOT SET}"
```

If both `ORG` and `SITE` are set, confirm with the user:

> "Previously used: org=`{ORG}`, site=`{SITE}`. Do you want to continue with these? If not, provide a different site URL (e.g., `https://main--mysite--myorg.aem.page/`)."

- If user confirms → proceed
- If user provides a URL → parse org and site from it, save the new values

If `ORG` or `SITE` is empty, ask:

> "Enter the site preview/live URL for which you want to perform ops (e.g., `https://main--mysite--myorg.aem.page/`)."

Parse org and site from the URL:

```bash
URL="$USER_INPUT"
if echo "$URL" | grep -q '\.aem\.page\|\.aem\.live'; then
  HOST_PART=$(echo "$URL" | cut -d'/' -f3 | cut -d'.' -f1)
  ORG=$(echo "$HOST_PART" | awk -F'--' '{print $NF}')
  SITE=$(echo "$HOST_PART" | awk -F'--' '{print $(NF-1)}')
  echo "Parsed from URL: org=$ORG site=$SITE"
fi
```

If the user provides something other than a valid `.aem.page` or `.aem.live` URL, ask again.

Save org and site:

```bash
mkdir -p "${HOME}/.aem"
node -e "
  const fs = require('fs');
  const p = process.env.HOME + '/.aem/ops-config.json';
  let c = {};
  try { c = JSON.parse(fs.readFileSync(p, 'utf8')); } catch(e) {}
  c.org = '${ORG}';
  c.site = '${SITE}';
  fs.writeFileSync(p, JSON.stringify(c, null, 2));
"
```

Only use org/site from `~/.aem/ops-config.json` or direct user input. Never infer from `git remote`, `fstab.yaml`, or folder/repo names.

Do NOT proceed until both org and site are confirmed.

### Step 1: Authenticate (REQUIRED)

Before ANY API call, check if auth token exists:

```bash
AUTH_TOKEN=$(node -e "
  const fs = require('fs');
  try {
    const t = JSON.parse(fs.readFileSync(process.env.HOME + '/.aem/ims-token.json', 'utf8'));
    if (t.authToken && t.authTokenExpiry > Math.floor(Date.now()/1000) + 60) {
      process.stdout.write(t.authToken);
    }
  } catch (e) {}
")
echo "auth=${AUTH_TOKEN:+set}"
```

If `AUTH_TOKEN` is empty, invoke the auth skill before proceeding:

```
Skill({ skill: "aem-project-management:auth" })
```

Use `-H "x-auth-token: ${AUTH_TOKEN}"` header for all `admin.hlx.page` API calls.

For sensitive endpoints and destructive operations, read `resources/security.md` and `resources/sensitive.md` before proceeding.

### Step 2: Load Full Configuration and Validate Role

```bash
eval $(node -e "
  const fs = require('fs');
  try {
    const c = JSON.parse(fs.readFileSync(process.env.HOME + '/.aem/ops-config.json', 'utf8'));
    console.log('ORG=' + JSON.stringify(c.org || ''));
    console.log('SITE=' + JSON.stringify(c.site || ''));
    console.log('REF=' + JSON.stringify(c.ref || 'main'));
  } catch(e) {
    console.log('ORG='); console.log('SITE='); console.log('REF=main');
  }
")
AUTH_TOKEN=$(node -e "
  const fs = require('fs');
  try {
    const t = JSON.parse(fs.readFileSync(process.env.HOME + '/.aem/ims-token.json', 'utf8'));
    process.stdout.write(t.authToken || '');
  } catch (e) {}
")
echo "Config: org=$ORG site=$SITE ref=$REF auth=${AUTH_TOKEN:+set}"
```

Fetch profile to verify auth and record user identity:

```bash
PROFILE_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "x-auth-token: ${AUTH_TOKEN}" \
  "https://admin.hlx.page/profile")
HTTP_CODE=$(echo "$PROFILE_RESPONSE" | tail -n1)
PROFILE=$(echo "$PROFILE_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "401" ]; then
  echo "Auth token expired. Need to re-authenticate..."
  echo "REAUTH_REQUIRED"
  exit 1
elif [ "$HTTP_CODE" != "200" ]; then
  echo "Failed to fetch profile (HTTP $HTTP_CODE). Check network/API status."
  exit 1
fi

eval $(echo "$PROFILE" | node -e "
  const d = require('fs').readFileSync(0,'utf8');
  try {
    const p = JSON.parse(d).profile || {};
    console.log('USER_EMAIL=' + JSON.stringify(p.email || ''));
    console.log('USER_NAME=' + JSON.stringify(p.name || ''));
  } catch(e) { console.log('USER_EMAIL=\"\"'); console.log('USER_NAME=\"\"'); }
")

echo "Authenticated as: $USER_EMAIL ($USER_NAME)"
```

If `REAUTH_REQUIRED`, invoke the auth skill and retry.

To determine user role on the site, check the site access config:

```bash
curl -s -H "x-auth-token: ${AUTH_TOKEN}" \
  "https://admin.hlx.page/config/${ORG}/sites/${SITE}.json"
```

If an operation returns 403, inform the user which role is required:

| Permission | Required Role |
|-----------|---------------|
| Preview | `basic_author`, `author`, `publish`, or `admin` |
| Publish to live | `basic_publish`, `publish`, or `admin` |
| Unpublish | `publish` or `admin` |
| Code sync | `develop` or `admin` |
| Config read | `config`, `config_admin`, or `admin` |
| Config write | `config_admin` or `admin` |
| Snapshot manage | `author`, `publish`, or `admin` |

Save `email` to `~/.aem/ops-config.json` for future use.

Read `resources/config.md` if site or other values are missing.

### Step 3: Route by Intent

| User Intent | Resource Module |
|-------------|-----------------|
| preview, publish, unpublish, status, delete preview | `resources/content.md` |
| cache, purge, clear cache, invalidate | `resources/cache.md` |
| sync code, deploy code, update code | `resources/code.md` |
| reindex, index, remove from index, search | `resources/index.md` |
| sitemap, generate sitemap | `resources/sitemap.md` |
| snapshot, staged release, bundle | `resources/snapshots.md` |
| logs, audit, activity | `resources/logs.md` |
| user, access, permission, who am i, add user, remove user | `resources/users.md` |
| job, bulk operation, stop job | `resources/jobs.md` |
| site, branch, switch, list sites | `resources/sites.md` |
| org config, site config, robots.txt | `resources/config-api.md` |
| secret, secrets, create secret, delete secret | `resources/secrets.md` |
| API key, apikey, create key, revoke key | `resources/apikeys.md` |
| token, tokens, access token | `resources/tokens.md` |
| profile config, profile settings | `resources/profiles.md` |
| index config, helix-index, search config | `resources/index-config.md` |
| sitemap config, helix-sitemap, sitemap rules | `resources/sitemap-config.md` |
| version, versions, history, rollback, restore | `resources/versioning.md` |
| pages, list pages, indexed pages, all pages | `resources/pages.md` |
| da, da list, da source, da copy, da move, da delete, da config, da versions | `resources/da.md` |
| destructive operation, confirmation required | `resources/security.md` |
| sensitive endpoint (emails, credentials, API keys) | `resources/sensitive.md` |

### Step 4: Read Resource and Execute

1. Read the appropriate resource file from `resources/`
2. Follow instructions in that resource
3. For config updates: always GET current config first and show it to the user before modifying
4. For code sync: always check repoless status before syncing (see `code.md`)
5. For destructive operations: read `resources/security.md` and follow the Confirmation Protocol — no exceptions (state action, explain impact, ask "yes/no", only execute after "yes")
6. Execute the API call
7. Handle response per completion standards below

### Completion Standards

| HTTP Response | Meaning | Required Action |
|---------------|---------|-----------------|
| **200/201** | Success | Display result with full URLs (`https://{ref}--{site}--{org}.aem.page{path}`) |
| **202** | Async job started | Report job name; instruct: `check job status {jobName}` to track progress |
| **204** | Success (no body) | Confirm: "{action} completed for {path}" |
| **4xx/5xx** | Error | Show API error verbatim, then suggest fix per `resources/errors.md` |

Before reporting success:
- For content operations: include both preview and live URLs where applicable
- For bulk operations: never say "published" or "previewed" — say "job started" until job completes
- For destructive operations: confirm what was removed and what still exists

---

## URL Parsing Helper

If user provides an AEM URL instead of separate org/site/path values:

```bash
# Pattern: https://{ref}--{site}--{org}.aem.page{path}
URL="$USER_INPUT"
if echo "$URL" | grep -q '\.aem\.page\|\.aem\.live'; then
  DOMAIN=$(echo "$URL" | cut -d'/' -f3)
  HOST_PART=$(echo "$DOMAIN" | cut -d'.' -f1)
  REF=$(echo "$HOST_PART" | awk -F'--' '{print $1}')
  ORG=$(echo "$HOST_PART" | awk -F'--' '{print $NF}')
  SITE=$(echo "$HOST_PART" | awk -F'--' '{
    r=""; for(i=2;i<NF;i++) r=(r==""?"":r"--")$i; print r
  }')
  URL_PATH=$(echo "$URL" | sed 's|https://[^/]*||')
  URL_PATH=${URL_PATH:-/}
  echo "Parsed from URL: org=$ORG site=$SITE ref=$REF path=$URL_PATH"
fi
```

Examples: `uat--hmns-uat-kw--alshaya-axp.aem.page` → `ref=uat`, `site=hmns-uat-kw`, `org=alshaya-axp`.

---

## Prerequisites

1. **Onboarded to Admin Service** — Project must have admin.hlx.page access
2. **User has an account** — Required for authentication (supports federated login)
3. **User has a site role** — Roles defined in site configuration (`access.admin.role`). Eight roles: `admin`, `author`, `publish`, `develop`, `basic_author`, `basic_publish`, `config`, `config_admin`. If the user lacks a role, the API returns 403.
4. **Network access** — Can reach admin.hlx.page

---

## Help Response

When the user wants the command list (triggers: `help`, `what can you do?`, `/ops help`, `list commands`):

```
Content Operations:
  preview /path          - Update preview
  publish /path          - Publish to live
  unpublish /path        - Remove from live
  status /path           - Check preview/live status

Cache Operations:
  clear cache /path      - Purge CDN cache
  force clear cache      - Force purge

Code Operations:
  sync code              - Deploy latest code

Index Operations:
  reindex /path          - Re-index for search

Sitemap:
  generate sitemap       - Create sitemap.xml

Snapshots:
  create snapshot {name} - Create staged release
  publish snapshot {name}- Publish all in snapshot

Logs:
  show logs              - View recent logs
  show logs last hour    - Filtered by time

Users:
  add user@email as role - Grant access
  remove role user@email - Revoke access
  who am i               - Current user

Jobs:
  list jobs              - Show bulk operations
  stop job {name}        - Cancel job

Sites:
  list sites             - Show all sites
  switch to site-x       - Change active site
  use branch feat-x      - Set branch

Config:
  show org config        - View org settings
  show site config       - View site settings
  update robots.txt      - Modify crawler rules

Secrets:
  list secrets           - Show secrets
  create secret {name}   - Add new secret
  delete secret {name}   - Remove secret

API Keys:
  list API keys          - Show API keys
  create API key {name}  - Generate new key
  revoke API key {id}    - Delete key

Profiles:
  show profile config    - View profile settings
  create profile {id}    - Create profile config
  delete profile {id}    - Remove profile config

Index Config:
  show index config      - View query.yaml
  update index config    - Modify indexing rules

Sitemap Config:
  show sitemap config    - View sitemap.yaml
  update sitemap config  - Modify sitemap rules

Versioning:
  list versions          - Show config history
  restore version {id}   - Rollback to version

Pages:
  list pages             - Show all indexed pages
  list pages /blog       - Filter by path prefix

Document Authoring (DA):
  da auth                - Authenticate with DA
  da list                - List DA organizations
  da list /path          - List files in DA path
  da source /path        - Get file content from DA
  da copy /src to /dest  - Copy file/folder in DA
  da move /src to /dest  - Move/rename in DA
  da delete /path        - Delete from DA
  da upload /path        - Upload content to DA
  da upload media /path  - Upload image/media to DA
  da config              - View DA site config
  da update config       - Update DA site config
  da versions /path      - List file versions
  da create version      - Create labeled version snapshot
  da restore version X   - Restore a previous version
  da preview /path       - Preview DA content
  da publish /path       - Publish DA content
```
