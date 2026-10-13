---
name: vault-health
description: "Audits Supabase Vault secrets — lists all stored secrets, tests API token validity, checks OAuth token freshness, and reports missing or expired credentials. Use when troubleshooting auth failures, after setup, or for periodic health checks."
allowed-tools:
  - Bash(curl:*)
  - Bash(*/get-secret.sh:*)
  - Bash(*/send-pushover.sh:*)
  - Read
  - Grep
  - ToolSearch
---

# /vault-health — Secret & Token Audit

Enumerates all secrets in Supabase Vault, compares against the expected registry, and tests every testable API token. Reports a single status table so you know what works, what's broken, and how to fix it.

## Runtime Context

At the start of each audit, retrieve the user's Supabase project reference for constructing API URLs:

```sql
SELECT email FROM user_profiles WHERE user_id = auth.uid()
```

For Supabase API endpoints that require the project reference (e.g., REST API base URL), retrieve the project ref dynamically:

```bash
SUPABASE_TOKEN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" supabase_access_token)
PROJECT_REF=$(curl -s -H "Authorization: Bearer $SUPABASE_TOKEN" \
  https://api.supabase.com/v1/projects | python3 -c "
import json, sys
projects = json.load(sys.stdin)
# Use the first project, or filter by name if multiple
if projects:
    print(projects[0]['id'])
")
```

Use `PROJECT_REF` to construct Supabase URLs dynamically: `https://{PROJECT_REF}.supabase.co/rest/v1/`

For the Supabase dashboard, construct URLs as: `https://supabase.com/dashboard/project/{PROJECT_REF}/settings/api`

## Data Storage Rules

- **Vault is source of truth.** All secrets are retrieved via `$OUTWORKOS_ROOT/scripts/get-secret.sh <label>`.
- **Never hardcode MCP tool names.** Use `ToolSearch` to discover Supabase tools at runtime if needed.
- **Never log secret values.** Only log pass/fail status and HTTP codes.

---

## Step 1: List Secrets from Vault

Enumerate all expected secrets from `references/secret-registry.md`. For each label, attempt retrieval:

```bash
LABEL="fireflies_token"  # example — iterate over all 21 labels
VALUE=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" "$LABEL" 2>/dev/null) && echo "FOUND" || echo "MISSING"
```

Run all 21 retrievals in parallel (separate Bash calls) for speed. Record which labels returned a value and which are missing.

---

## Step 2: Compare Against Registry

Load the full registry from `references/secret-registry.md`. For each entry:
- **Present**: Mark for testing (if `Testable? = Yes`) or mark as `·` (exists, not testable).
- **Missing**: Mark as `✗` with note "secret not found in Vault".

---

## Step 3: Test API Tokens

For each testable secret that was found in Step 1, run the corresponding validation call from `references/test-patterns.md`. **Run all tests in parallel** (separate Bash calls).

Each test follows this pattern:
```bash
TOKEN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" "<label>")
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" <endpoint with TOKEN>)
if [ "$HTTP_CODE" = "200" ]; then echo "PASS"; else echo "FAIL:$HTTP_CODE"; fi
```

**Important:** Never store token values in variables that appear in output. Only capture and display HTTP status codes.

---

## Step 4: Test OAuth Tokens

OAuth services (Google, LinkedIn) require a token refresh test, not just a simple API call.

### Google OAuth
Retrieve `google_client_id`, `google_client_secret`, and `google_refresh_token`. Attempt a token refresh:
```bash
CLIENT_ID=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" google_client_id)
CLIENT_SECRET=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" google_client_secret)
REFRESH_TOKEN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" google_refresh_token)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  -d "client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET&refresh_token=$REFRESH_TOKEN&grant_type=refresh_token" \
  https://oauth2.googleapis.com/token)
```
- **200**: Google OAuth is healthy.
- **400/401**: Refresh token expired or revoked. Provide re-auth instructions.

### LinkedIn
Retrieve `linkedin_access_token` and test the userinfo endpoint:
```bash
ACCESS_TOKEN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" linkedin_access_token)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  https://api.linkedin.com/v2/userinfo)
```
- **200**: LinkedIn access token is valid.
- **401**: Token expired. Provide re-auth instructions.

---

## Step 5: Report Results

Display a summary table in the terminal:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VAULT HEALTH — YYYY-MM-DD HH:MM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Service          Secret                    Status
─────────────────────────────────────────────────────
Google           google_client_id          ·  exists (not testable)
Google           google_client_secret      ·  exists (not testable)
Google           google_refresh_token      ✓  OAuth refresh OK
Google           google_redirect_uri       ·  exists (not testable)
Google           google_token_uri          ·  exists (not testable)
LinkedIn         linkedin_client_id        ·  exists (not testable)
LinkedIn         linkedin_client_secret    ·  exists (not testable)
LinkedIn         linkedin_refresh_token    ✓  OAuth refresh OK
LinkedIn         linkedin_access_token     ✓  API call OK (200)
LinkedIn         linkedin_person_urn       ·  exists (not testable)
Fireflies        fireflies_token           ✓  GraphQL ping OK (200)
Supabase         supabase_access_token     ✓  list projects OK (200)
— (supabase_service_role_key lives in Keychain, not Vault — excluded)
Netlify          netlify_auth_token        ✓  user endpoint OK (200)
Anthropic        anthropic_api_key         ✓  models list OK (200)
Todoist          todoist_api_token         ✓  sync OK (200)
ElevenLabs       elevenlabs_api_key        ✓  user endpoint OK (200)
Pushover         pushover_user_key         ·  exists (not testable alone)
Pushover         pushover_api_token        ✓  validate OK (200)
ScrapingDog      scrapingdog_api_key       ✓  usage endpoint OK (200)
─────────────────────────────────────────────────────

Summary: 19 secrets checked — 12 passed, 7 not testable, 0 missing, 0 failed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Status legend

| Symbol | Meaning |
|--------|---------|
| `✓` | Secret exists and API test passed |
| `✗` | Secret missing or API test failed (error details shown) |
| `·` | Secret exists but not testable (client IDs, URNs, URIs) |
| `⚠` | OAuth token expired — re-auth needed (instructions shown) |

### On failure

For each failed or expired secret, display remediation instructions inline:

- **Missing secret**: `Run: $OUTWORKOS_ROOT/scripts/set-secret.sh <label> <value>`
- **Google OAuth expired**: `Run: $OUTWORKOS_ROOT/scripts/google-auth.sh`
- **LinkedIn expired**: `Re-authorize at https://www.linkedin.com/developers/apps — generate new tokens and store via set-secret.sh`
- **Supabase token failed**: `Regenerate at https://supabase.com/dashboard/account/tokens`
- **Netlify token failed**: `Regenerate at https://app.netlify.com/user/applications#personal-access-tokens`
- **Anthropic key failed**: `Regenerate at https://console.anthropic.com/settings/keys`
- **Todoist token failed**: `Find token at https://app.todoist.com/app/settings/integrations/developer`
- **ElevenLabs key failed**: `Regenerate at https://elevenlabs.io/app/settings/api-keys`
- **Fireflies token failed**: `Regenerate at https://app.fireflies.ai/integrations/custom/fireflies`
- **Pushover token failed**: `Check at https://pushover.net/apps`
- **ScrapingDog key failed**: `Check at https://www.scrapingdog.com/dashboard`

---

## Step 6: Send Pushover Alert (if issues found)

After generating the report, if there are ANY missing or failed secrets (status `✗`), send a Pushover notification summarizing the issues. **Do not send a notification if everything is healthy.**

```bash
bash "$OUTWORKOS_ROOT/skills/notify-user/send-pushover.sh" \
  "Vault Health: {N} issue(s)" \
  "{list of failed/missing secret labels, one per line}"
```

Example message for 2 issues:
```
elevenlabs_api_key: FAIL (401)
linkedin_refresh_token: MISSING
```

Keep the message concise — just the label and status. The full remediation details are in the terminal output and log file.

**Do not alert** for secrets marked as `·` (exists, not testable) — only for `✗` (missing/failed) and `⚠` (expired OAuth).

---

## Notes

- All tests use lightweight read-only endpoints. No data is modified.
- Pushover validation requires both `pushover_api_token` and `pushover_user_key` together — tested as a pair.
- The `supabase_service_role_key` is excluded from checks — it lives in macOS Keychain (not Vault) as the bootstrap credential needed to access Vault itself.
- Run this skill after `/setup-project` to verify all secrets are in place, or whenever API calls start failing unexpectedly.
