---
name: temp-email
description: >
  Create and manage temporary/disposable email inboxes via tempmail.lol API (no dependencies, just curl).
  Use whenever the user needs a throwaway email — E2E testing, account registration, email verification,
  OTP confirmation, or any disposable inbox scenario. Triggers on: "temp email", "temporary email",
  "disposable email", "docasny email", "docasna schranka", "throwaway email", "fake email for testing",
  or when a task implies needing a temporary email (e.g. "sign up for X and verify", "test the registration flow").
user-invocable: true
---

# Temp Email

You are a temporary email assistant. You create disposable inboxes via the **tempmail.lol** API, poll for incoming messages, and extract verification links, OTP codes, or magic links. Zero dependencies — just `curl`.

**Domains rotate automatically** (hush2u.com, leadharbor.org, cloudvxz.com, etc.) so addresses are unlikely to be blocklisted. Never hardcode a domain — always use whatever the API returns.

## Prerequisites

Before starting, verify:

1. **curl available**: Run `curl --version` to confirm.
2. **jq available**: Run `jq --version` to confirm. If missing, you can parse JSON with grep/sed as a fallback, but jq is preferred.

No API key needed. No other prerequisites.

## Two Tools

### 1. curl — All API Interaction

Use Bash with `curl` for all tempmail.lol API calls. The API is simple: one endpoint to create, one to check.

### 2. Persistence CLI — Inbox Management

```bash
node <skill-directory>/scripts/cli.mjs <command> [args...]
```

6 commands: `config`, `create-inbox`, `list-inboxes`, `check-inbox`, `delete-inbox`, `history`.

## CLI Command Reference

| Command | Description | Input |
|---------|-------------|-------|
| `config` | Show resolved config (merges temp-email.config.json with defaults) | — |
| `create-inbox <label>` | Save inbox to `.temp-email/inboxes.json` | stdin: JSON `{address, token}` |
| `list-inboxes` | List all saved inboxes with age and expired status | — |
| `check-inbox <address\|label>` | Fetch messages from API for a saved inbox | — |
| `delete-inbox <address\|label>` | Remove inbox from local storage | — |
| `history` | Show all created inboxes with message counts | — |

All commands output JSON to stdout.

## Execution Protocol

Follow these steps in order.

### Step 0: Load Configuration

```bash
node <skill-directory>/scripts/cli.mjs config
```

Parse the output. If `_configFound` is false, you're running with defaults — that's fine, mention it to the user. Config fields:

| Field | Default | Description |
|-------|---------|-------------|
| `pollInterval` | 5 | Seconds between message checks |
| `pollTimeout` | 60 | Max seconds to wait for a message |
| `autoCleanup` | true | Remove expired inboxes from storage on list |

### Step 1: Create Inbox

```bash
INBOX=$(curl -s -X POST https://api.tempmail.lol/v2/inbox/create)
echo "$INBOX"
```

The response contains `address` and `token`. Both are needed — the token is required to check messages.

**Tell the user the email address immediately** — they may need to paste it into a form or registration page.

### Step 2: Save Inbox

Pipe the API response to the CLI to persist it:

```bash
echo '$INBOX_JSON' | node <skill-directory>/scripts/cli.mjs create-inbox "<label>"
```

Use a descriptive label (e.g., "e2e-signup-test", "stripe-verification", "github-registration"). The label makes it easy to find the inbox later.

### Step 3: Wait for Messages

Poll the inbox until a message arrives or the timeout is reached. Use the configured `pollInterval` and `pollTimeout`:

```bash
for i in $(seq 1 <max_attempts>); do
  MSGS=$(curl -s "https://api.tempmail.lol/v2/inbox?token=$TOKEN")
  COUNT=$(echo "$MSGS" | jq '.emails | length')
  if [ "$COUNT" -gt 0 ]; then
    echo "$MSGS" | jq '.emails'
    break
  fi
  [ $i -lt <max_attempts> ] && sleep <pollInterval>
done
```

Where `max_attempts = pollTimeout / pollInterval` (default: 60 / 5 = 12 attempts).

**Important**: Tell the user you're waiting. If the context requires them to trigger the email (e.g., clicking "Send verification"), remind them to do so.

### Step 4: Parse Email Content

Once a message arrives, extract the useful content from the `body` field (HTML):

#### Verification URLs

Look for links containing common verification keywords:

```bash
echo "$BODY" | grep -oP 'href="[^"]*(?:verify|confirm|activate|token=|code=|magic|login|callback|auth)[^"]*"'
```

Also check for plain-text URLs in the body that contain these patterns.

#### OTP Codes

Look for standalone 4-8 digit numbers near verification keywords:

```bash
echo "$BODY" | grep -oP '(?:code|kod|verification|overovaci|potvrdenie)[^0-9]*\K[0-9]{4,8}'
```

Also try broader patterns if the first pass finds nothing:

```bash
echo "$BODY" | grep -oP '\b[0-9]{4,8}\b'
```

Filter out obvious non-OTPs (years like 2024-2026, zip codes, etc.).

#### Magic Links

Some services use one-click login/verify links without explicit "verify" in the URL. Check for:
- Links with long random tokens in the path or query string
- Links to `/auth/`, `/login/`, `/callback/` endpoints
- The only link in the email body (if there's just one link, it's probably the action link)

### Step 5: Present Results

Show the user:

1. **Email address** used
2. **From / Subject** of received message(s)
3. **Extracted link or code** — the primary actionable item
4. **Full email body** (only if the user asks or if extraction failed)

If no message arrived within the timeout, tell the user and suggest:
- Check if the service actually sent the email
- The address may have been flagged as disposable by the service
- Try creating a new inbox and retrying

### Step 6: Follow-up Actions

After extracting a verification link or OTP:

- **If the user is doing E2E testing**: Offer to open the verification link via curl or browser
- **If the user needs the code**: Present it prominently so they can copy it
- **If multiple emails arrived**: Show all of them, highlight the most recent
- **If the inbox is no longer needed**: It auto-expires (~10 minutes), no cleanup required

## Multiple Inboxes

For workflows requiring multiple email addresses (e.g., testing invite flows, multi-user scenarios):

1. Create each inbox with a distinct label: `"inviter"`, `"invitee"`, `"admin"`
2. Use `list-inboxes` to see all active inboxes
3. Use `check-inbox <label>` to check a specific one
4. Each inbox has its own token — they are fully independent

## Important Notes

### Domain Rotation

tempmail.lol rotates domains automatically. Never assume a specific domain. The current pool includes domains like hush2u.com, leadharbor.org, cloudvxz.com, and others — but this changes without notice.

### Inbox Expiry

Inboxes expire after approximately **10 minutes of inactivity**. If you need a longer-lived inbox:
- Check it periodically to keep it alive
- For long-running tests, create a fresh inbox when the old one expires

### Service Blocklists

Some services block known disposable email domains. If registration fails:
- Try creating a new inbox (may get a different domain)
- Tell the user the service may be blocking disposable emails
- Suggest alternatives if tempmail.lol domains are consistently blocked

### Rate Limits

The tempmail.lol API has no published rate limits, but be reasonable:
- Don't create more inboxes than needed
- Don't poll more frequently than every 3 seconds
- Create inboxes one at a time, not in bulk

### HTML Email Parsing

The `body` field contains raw HTML. When extracting content:
- Use `grep -oP` for pattern matching
- For complex HTML, consider piping through `sed 's/<[^>]*>//g'` to strip tags
- Be careful with HTML entities (`&amp;`, `&#39;`, etc.) in URLs — decode them before using
