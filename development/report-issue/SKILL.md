---
name: report-issue
model: claude-sonnet-5-5
category: analysis
userInvocable: true
description: Draft and submit a bug report or feature request to the nexus plugin repository, using current conversation context to auto-populate details.
argument-hint: "[--feature-request]"
allowed-tools: "Read, Bash(gh issue create:*), Bash(gh auth status:*), Bash(jq:*), Bash(mkdir:*), Bash(umask:*), Bash(printf:*), Bash(grep:*), Bash(sed:*), Bash(sort:*), Bash(rm:*), Bash(cat:*), Bash(echo:*), Bash(false:*), AskUserQuestion"
---

# Report Issue

Arguments: $ARGUMENTS

Draft a GitHub issue for the nexus plugin repository based on the current conversation context. Invoke this immediately after noticing a bug or wanting to request a feature — while the context is still fresh.

## Usage

```bash
/report-issue                    # Report a bug (default)
/report-issue --feature-request  # Report a feature request
```

---

## Step 1: Determine Issue Type

Parse `$ARGUMENTS`:
- If `--feature-request` is present → `TYPE=feature-request`, label `enhancement`
- Otherwise → `TYPE=bug`, label `bug`

---

## Step 2: Early Auth Check

```bash
gh auth status 2>/dev/null
```

If the command fails (exit code non-zero), stop immediately:

```
⚠️  Not authenticated with GitHub. Run: gh auth login
Issue cannot be submitted without authentication.
```

---

## Step 3: Get Plugin Version

```bash
jq -r '.plugins["nexus@claude-skills"][0].version // "unknown"' \
  ~/.claude/plugins/installed_plugins.json 2>/dev/null || echo "unknown"
```

Store as `PLUGIN_VERSION`.

---

## Step 4: Build Draft from Conversation Context

Using the current conversation context, extract the following. Be concise — aim for enough detail to reproduce or understand the issue, not a full session dump.

### For `TYPE=bug`

Extract:
- **What happened** — the error or unexpected behavior observed
- **Error message** — exact error text if visible in the conversation (quote verbatim, but redact secrets — see field instructions below)
- **Context** — which skill or agent was running, what the user was trying to do (general terms only, no internal hostnames or paths)
- **Trigger** — what action or input caused it

**Per-field constraints** (apply during extraction, before the Step 5 scan):

- **Description**: One sentence summarizing the bug. No file paths, hostnames, tokens, or PII.
- **Error**: Quote verbatim if available. If the error contains tokens, passwords, API keys, connection strings, email addresses, internal hostnames, or absolute file paths, replace those substrings with `[REDACTED]` *before* including the quote. Keep the structural shape of the error (e.g., `connection refused: [REDACTED]`).
- **Context**: Describe what skill/agent was active and what the user was attempting in general terms. Do NOT include internal hostnames, service names, cluster names, or absolute file paths.
- **Steps to Reproduce**: Describe steps abstractly. Do NOT include credentials, absolute paths, or hostnames in step descriptions.
- **Environment**: Plugin version only — no OS, shell, CWD, git remote, or username.

Compose the issue body using this template:

```markdown
## Description

{one-sentence summary of the bug}

## Error

{verbatim error with secrets redacted as [REDACTED]; if no error available, describe behavior}

## Context

{skill/agent that was active, what the user was attempting — general terms only}

## Steps to Reproduce

1. {step 1, abstract — no paths/hosts/credentials}
2. {step 2}
3. {add more if clear from context, otherwise omit}

## Environment

- Plugin version: {PLUGIN_VERSION}
```

### For `TYPE=feature-request`

Extract:
- **What capability is missing or needed** — derived from what the user was trying to do
- **Problem it solves** — why this matters based on the conversation

Compose the issue body using this template:

```markdown
## Description

{one-sentence summary of the requested feature}

## Problem

{what the user was trying to do and why the current behavior falls short}

## Proposed Behavior

{what the skill/agent/workflow should do instead}

## Context

{which skill or agent this relates to, if applicable}

## Environment

- Plugin version: {PLUGIN_VERSION}
```

Generate a concise issue title:
- Bug: `[bug] {skill-or-agent}: {short description}` — e.g., `[bug] nexus:commit: unknown skill nexus:git-operator error`
- Feature: `[feature] {short description}` — e.g., `[feature] report-issue: support attaching file paths`

---

## Step 5: Sensitivity Check

Before showing the draft, scan **the full body and the title** for sensitive content. This is a soft, LLM-driven first pass; a deterministic bash gate in Step 7 catches anything missed here.

### Patterns to detect

**Known prefixes (high-confidence — match by prefix anywhere in the text):**

- `AKIA[0-9A-Z]{16}`, `ASIA[0-9A-Z]{16}` — AWS access key IDs
- `ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_` followed by alphanumerics — GitHub personal access tokens
- `xox[baprs]-` followed by alphanumerics — Slack tokens
- `-----BEGIN` (any header) — private keys, certificates, PEM blocks (redact the entire block through `-----END ...-----`)
- `eyJ` followed by a long base64 string with two more `.`-separated segments — JWTs
- `postgres://`, `mysql://`, `mongodb://`, `redis://` — database connection strings (especially if `user:password@` is embedded)
- `AIza[0-9A-Za-z_-]{35}` — Google API keys
- `sk_live_…`, `rk_live_…`, `pk_live_…` — Stripe live keys
- `sk-ant-` followed by alphanumerics — Anthropic API keys
- `sk-` followed by 32+ alphanumerics — OpenAI-style API keys
- `Authorization: Bearer …` and `Authorization: Basic …` — auth header values (redact the value, keep the header name)

**Structural patterns (match by shape):**

- Absolute paths: `/home/[name]/…`, `/Users/[name]/…`, `C:\Users\…`, `\\[host]\[share]\…`, `/mnt/c/Users/…`, `/private/var/folders/…`
- `.env`-style assignments where the key name suggests a secret — `PASSWORD=`, `SECRET=`, `TOKEN=`, `API_KEY=`, `PRIVATE_KEY=`, `DATABASE_URL=`, `DSN=`, `AUTH_TOKEN=` — redact the value regardless of length
- Email addresses matching `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` — but keep GitHub `@username` mentions (shape: `@` + 1–39 alphanumerics/hyphens, no domain)
- Internal hostnames or service names that weren't already part of the error/context (e.g., `db-prod-1.corp.internal`, `kafka-east-cluster`)

### Action

For each match, replace the matched substring with `[REDACTED]` in both the body and the title. Preserve the surrounding text so the issue remains intelligible.

After redaction, surface a summary of what was redacted (by category, not by value):

```
⚠️  Sensitivity scan — redacted content:
  - 1× AWS access key ID
  - 2× absolute paths
  - 1× email address

The draft below shows redacted content. Review before confirming.
```

If nothing was redacted, say so:

```
✓ Sensitivity scan — no patterns matched.
```

---

## Step 6: Show Draft and Ask for Additions

Display the full draft:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Issue Draft
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Repo:  nexus-a1/claude-skills
Type:  {bug | feature-request}
Label: {bug | enhancement}

Title: {title}

{body}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then use the AskUserQuestion tool:

```
header: "Add notes"
question: "Anything to add to this issue before sending?"
options: ["No, looks good", "Yes, I want to add a note"]
```

If the user selects "Yes", use AskUserQuestion again with an open prompt to collect their note.

If the user provides input, append it to the body under a `## Additional Notes` section.

### Second sensitivity scan (after notes appended)

If the user added a note, **re-run the full Step 5 sensitivity check against the complete updated body** (description + error + context + steps + environment + additional notes). User-supplied notes never reach `gh issue create` without being scanned. If new patterns are detected, redact them in place and surface a fresh summary:

```
⚠️  Second sensitivity scan (after Additional Notes) — redacted content:
  - 1× GitHub PAT
```

If the user added no note, skip the second scan.

---

## Step 7: Confirm and Submit

### Render exact final payload

Show the user the **exact** title and body bytes that will be POSTed — not a paraphrase. This must reflect post-Step-5 (and post-Step-6 second-scan) content:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Final payload (post-redaction)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Repo:  nexus-a1/claude-skills (PUBLIC — visible to anyone, indexed by search engines)
Label: {bug | enhancement}

Title: {final title}

{final body}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Confirmation

Use the AskUserQuestion tool:

```
header:   "Confirm"
question: "Submit this issue to nexus-a1/claude-skills (public GitHub repository — will be publicly visible and indexed by search engines)?"
options:  ["Yes, submit to public repo", "No, cancel"]
```

If **No**: stop and display `Issue cancelled. Draft was not submitted.`

### Deterministic pre-submit scan gate (hard block)

If **Yes**: before invoking `gh issue create`, run a deterministic regex scan over the body and title. This is a non-LLM enforcement layer that catches secrets the Step 5 / Step 6 LLM scans may have missed. **A match here hard-blocks submission.**

```bash
# The draft lives in the project work area, not /tmp, and not under an mktemp
# name. Both matter, for different reasons:
#   - mktemp names do not survive a Bash tool call, and neither does the
#     variable holding one. The submit block below is a separate call, so it
#     could never have named the file the gate scanned.
#   - a PREDICTABLE name in a world-writable directory is the vector mktemp was
#     avoiding: another process can pre-create or symlink /tmp/<known-name>
#     between the write and the read. A private directory under .claude with
#     umask 077 gives a stable name without that exposure.
umask 077
SCAN_DIR=".claude/report-issue"
mkdir -p "$SCAN_DIR"
BODY_FILE="$SCAN_DIR/body.md"
ERROR_FILE_PRE="$SCAN_DIR/error.log"
# A stable name can be pre-created as a SYMLINK by anything that can write the
# directory, and `cat >` follows it: the draft would overwrite the link target
# and then be published from it. Refuse a symlink outright, and remove any
# existing file before writing so `set -C` cannot be satisfied by a leftover.
for _f in "$BODY_FILE" "$ERROR_FILE_PRE" "$SCAN_DIR/scan-patterns.txt"; do
  if [ -L "$_f" ]; then
    echo "⛔ Refusing to write: $_f is a symlink. Remove it and re-run." >&2
    return 1 2>/dev/null || exit 1
  fi
  rm -f "$_f"
done
set -C   # no clobber: a file appearing between the rm and the write is a race
ERROR_FILE="$SCAN_DIR/error.log"
PATTERN_FILE="$SCAN_DIR/scan-patterns.txt"
cat > "$BODY_FILE" << 'REPORT_ISSUE_BODY_EOF'
{full issue body, post-redaction}
REPORT_ISSUE_BODY_EOF

ISSUE_TITLE='{final title, post-redaction}'

# Written to a file as well as used here, so the re-scan in the submit block
# uses THE SAME patterns rather than a second copy that can drift from this one.
SCAN_PATTERNS='AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|ghp_[A-Za-z0-9_]+|gho_[A-Za-z0-9_]+|ghu_[A-Za-z0-9_]+|ghs_[A-Za-z0-9_]+|ghr_[A-Za-z0-9_]+|xox[baprs]-[A-Za-z0-9-]+|-----BEGIN [A-Z ]+-----|sk_live_[A-Za-z0-9]+|rk_live_[A-Za-z0-9]+|sk-ant-[A-Za-z0-9-]+|AIza[0-9A-Za-z_-]{35}'

printf '%s\n' "$SCAN_PATTERNS" > "$PATTERN_FILE"

if grep -qE "$SCAN_PATTERNS" "$BODY_FILE" || echo "$ISSUE_TITLE" | grep -qE "$SCAN_PATTERNS"; then
  echo "⛔ Submission blocked — deterministic scan detected a high-confidence secret pattern in the draft." >&2
  echo "Matched categories:" >&2
  { grep -oE "$SCAN_PATTERNS" "$BODY_FILE"; echo "$ISSUE_TITLE" | grep -oE "$SCAN_PATTERNS"; } \
    | sed -E 's/(AKIA|ASIA)[0-9A-Z]+/AWS access key/; s/ghp_[A-Za-z0-9_]+/GitHub PAT (ghp_)/; s/gho_[A-Za-z0-9_]+/GitHub PAT (gho_)/; s/ghu_[A-Za-z0-9_]+/GitHub PAT (ghu_)/; s/ghs_[A-Za-z0-9_]+/GitHub PAT (ghs_)/; s/ghr_[A-Za-z0-9_]+/GitHub PAT (ghr_)/; s/xox[baprs]-[A-Za-z0-9-]+/Slack token/; s/-----BEGIN.*-----/PEM key block/; s/sk_live_[A-Za-z0-9]+/Stripe live key/; s/rk_live_[A-Za-z0-9]+/Stripe restricted key/; s/sk-ant-[A-Za-z0-9-]+/Anthropic API key/; s/AIza[0-9A-Za-z_-]+/Google API key/' \
    | sort -u | sed 's/^/  - /' >&2
  echo "" >&2
  echo "The LLM redaction in Steps 5/6 missed at least one secret. Edit the conversation to remove the secret values, then re-run /report-issue." >&2
  rm -f "$BODY_FILE" "$ERROR_FILE" "$PATTERN_FILE"
  false
fi
```

If the gate hard-blocks, the skill stops here. Do not retry, do not call `gh issue create`. The user must remove the secret from conversation context (or paste a corrected note) and re-invoke.

### Submission

If the deterministic gate passes, create the issue. **The scan is re-run here,
in the same call as the publish.** The gate above runs in a different Bash tool
call, and between the two the file can change — the model can edit it, a stale
file can be left at the same path by an earlier run, another process can write
to it. A scan in one call and a publish in another cannot make the claim this
gate exists to make; only a scan and a publish in the same call can, so the last
thing before `gh issue create` is the scan itself.

```bash
umask 077
SCAN_DIR=".claude/report-issue"
BODY_FILE="$SCAN_DIR/body.md"
ERROR_FILE="$SCAN_DIR/error.log"
PATTERN_FILE="$SCAN_DIR/scan-patterns.txt"
ISSUE_TITLE='{final title, post-redaction}'
# Same symlink refusal on the read side: publishing through a link would send
# whatever the link points at, which is not what the gate scanned.
for _f in "$BODY_FILE" "$PATTERN_FILE"; do
  if [ -L "$_f" ]; then
    echo "⛔ Refusing to publish: $_f is a symlink, so it is not the file that was scanned." >&2
    false
  fi
done

# Re-scan the exact bytes about to be published, with the patterns the gate
# wrote. Refuse if either file is missing: an unreadable scan is not a clean
# scan, and "the gate already ran" is a claim about a different call.
if [ ! -r "$BODY_FILE" ] || [ ! -r "$PATTERN_FILE" ]; then
  echo "⛔ Refusing to publish: the scanned draft or its patterns are missing — re-run the gate." >&2
  false
else
  grep -qE -f "$PATTERN_FILE" "$BODY_FILE"
  body_rc=$?
  printf '%s' "$ISSUE_TITLE" | grep -qE -f "$PATTERN_FILE"
  title_rc=$?
  if [ "$body_rc" -eq 0 ] || [ "$title_rc" -eq 0 ]; then
    echo "⛔ Refusing to publish: a secret pattern is present in the bytes about to be sent." >&2
    false
  elif [ "$body_rc" -ge 2 ] || [ "$title_rc" -ge 2 ]; then
    echo "⛔ Refusing to publish: the pre-publish scan itself failed (grep exit $body_rc/$title_rc) — that is not a clean scan." >&2
    false
  else

gh issue create \
  --repo "nexus-a1/claude-skills" \
  --title "$ISSUE_TITLE" \
  --body-file "$BODY_FILE" \
  --label "{bug|enhancement}" 2>"$ERROR_FILE"

GH_RC=$?
if [ $GH_RC -ne 0 ]; then
  if grep -qi "label" "$ERROR_FILE"; then
    # Label doesn't exist — retry without it
    gh issue create \
      --repo "nexus-a1/claude-skills" \
      --title "$ISSUE_TITLE" \
      --body-file "$BODY_FILE"
    GH_RC=$?
  else
    # Different error — surface it
    cat "$ERROR_FILE" >&2
  fi
fi

    rm -f "$BODY_FILE" "$ERROR_FILE" "$PATTERN_FILE"
    [ $GH_RC -eq 0 ] || false
  fi
fi
```

> Using `--body-file` avoids shell quoting issues with error messages, stack traces, and special characters in the body. The title is passed through `--title "$ISSUE_TITLE"` (argv, never via `bash -c` or string interpolation) to prevent shell-metacharacter injection. Stderr is captured to a temp file so label-not-found errors trigger a no-label fallback; cleanup runs on every path before the final exit.

---

## Step 8: Report Result

On success:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Issue Submitted
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{issue URL}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

On failure:

```
⚠️  Could not create issue. gh error:
{error output}

The draft was not submitted. You can create it manually at:
https://github.com/nexus-a1/claude-skills/issues/new
```

---

## Error Handling

### `gh` not authenticated
```
⚠️  Not authenticated with GitHub. Run: gh auth login
```

### No conversation context to extract
If the conversation has no discernible error or feature request to base the draft on, use the AskUserQuestion tool to ask:

```
header: "Describe issue"
question: "What issue would you like to report?"
```

Use their response as the primary input for the draft.
