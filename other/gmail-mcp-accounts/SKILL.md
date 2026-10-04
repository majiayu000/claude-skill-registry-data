---
name: gmail-mcp-accounts
description: >
  Add, remove, or authenticate accounts for the self-hosted multi-account
  Gmail MCP (local.gmailMcp.accounts, modules/home/gmail-mcp.nix, launchers
  from packages/gmail-mcp.nix, declared by the `gmail` plugin's .mcp.json) —
  TRUE simultaneous multi-account Gmail via ArtyMcLabin/Gmail-MCP-Server, one
  process per account, unlike the built-in single-account connector. Use when
  asked to "add a gmail account", "authenticate gmail mcp", "gmail multi
  account setup", "rotate the gmail oauth client", or when a gmail-mcp
  account seems to be authenticated as the wrong person.
---

# Gmail MCP multi-account operator

Canonical docs: [`docs/gmail-mcp-multi-account-runbook.md`](../../../docs/gmail-mcp-multi-account-runbook.md).

> **LANE CHANGE 2026-10-01/02 — the capability is LIVE, the plumbing moved.** The central MCP
> gateway and its Cloudflare portal are **destroyed** and `modules/shared/mcp.nix` is **deleted**.
> Gmail was deliberately kept. Substitute as you read:
>
> | Then | Now |
> |---|---|
> | `local.mcpGateway.gmail.accounts` | **`local.gmailMcp.accounts`** (`modules/home/gmail-mcp.nix`), set in `hosts/macos.nix` |
> | `mkGmailMcp` inline in `mcp.nix` | **`packages/gmail-mcp.nix`** → one `nix-mcp-gmail-<alias>` launcher per account, on PATH |
> | one long-lived process per account under a shared proxy | **one stdio child per account PER SESSION**, spawned by Claude Code from the `gmail` plugin's `.mcp.json` in `github:kattakath/skills` |
> | reachable from Claude Code, Claude Desktop and Cowork | **Claude Code only** — Desktop loads no plugins and now has no MCP servers at all |
>
> **Two steps are therefore NOT enough on their own.** Adding an address to
> `local.gmailMcp.accounts` only puts a launcher on PATH; the `gmail` plugin's `.mcp.json` must
> also name that binary, or nothing spawns it. And **an already-running session will never see a
> new account** — its tool namespace was fixed at session start, so start a fresh one.
>
> Everything about Google, OAuth, the test-user cap, the 7-day Testing expiry and the
> wrong-account grab below is **unchanged** — none of it was ever about the gateway.

## Rules

- **Never print a client secret, access token, or refresh token** — pipe
  values directly between Keychain/file/curl, report only success/failure.
- **Which addresses may be listed at all**: only add an email to
  `hosts/<host>.nix` if it is already public elsewhere in that same tree (an
  identity the operator has already named). Anyone else's address does NOT go in
  — and there is no longer a private flake to put it in: nix-personal was
  retired 2026-09-15, and of the seven extra accounts it carried the operator
  kept exactly two (#524) and dropped the rest rather than publish them. If
  unsure, ask — do not add.
- **A Console test user MUST exist before auth is attempted** — Audience →
  Add users, or the flow rejects the account outright.
- **A test user cannot rescue an INTERNAL client.** If the consent screen says
  "can only be used within its organization", the app's user type is Internal
  and an out-of-org account is hard-blocked no matter how the test-user list is
  configured — check that first for any account outside the client's own
  Workspace org. Measured 2026-09-29: 3 of 4 declared accounts had never had a
  working credential for exactly this reason.
- **Testing status expires refresh tokens after 7 days** (External + restricted
  Gmail scopes), so a working account going `invalid_grant` is expected
  maintenance, not corruption — see the runbook's setup step 2 for the citation
  and the per-org-Internal-client alternative.
- **The OAuth client must be Desktop app type**, not Web application — Web
  clients don't support the loopback redirect this tool uses.
- **ALWAYS verify the result of a one-time auth run with a direct API call**
  (`curl` the Gmail profile endpoint with the saved access token) — the CLI's
  own "Authentication completed successfully" message is not sufficient
  evidence. There is a known failure mode (see below) where it silently
  authenticates the *wrong* account with no error and no visible prompt.
- When editing a Nix file that already has unrelated uncommitted changes
  (e.g. a private flake with other work in progress), never `git add -A` and
  never hand-edit `git add -p` hunks — use the base+edit+`hash-object`+
  `update-index` reconstruction in the runbook to isolate exactly your
  change in the index, leaving the rest of the working tree untouched.

## Known failure mode (read before running auth on more than one account)

The tool opens the OS default browser. If that browser already has an active
Google session, the flow can complete instantly with **no account picker and
no visible interaction**, silently using whatever account is active — not
necessarily the target. Observed pattern: requesting account N produces
account N−1's token, and N's real token shows up under the tool's *default*
credentials path (`~/.gmail-mcp/credentials.json`, when
`GMAIL_CREDENTIALS_PATH` was omitted) on the *next* run. Check that file
before assuming a failure — the token may just be misfiled, fixable with a
`mv`, not a full re-auth. Full details and recovery steps: runbook § "Known
issue".

## Commands

```bash
# One-time OAuth client setup (per Google Cloud project) — see runbook for
# the full Console walkthrough (Desktop app type, External+Testing, enable
# Gmail API, register gmail.modify + gmail.settings.basic scopes).
secret set GMAIL_OAUTH_CLIENT_ID <client_id>
secret set GMAIL_OAUTH_CLIENT_SECRET <client_secret>

# Per-account: after adding as a Console test user AND to the right Nix list
# (public/private) AND activating —
GMAIL_OAUTH_PATH="$HOME/.gmail-mcp/gcp-oauth.keys.json" \
  GMAIL_CREDENTIALS_PATH="$HOME/.gmail-mcp/credentials-<alias>.json" \
  npx -y @artymclabin/gmail-mcp auth

# MANDATORY verification — never skip:
tok="$(jq -r '.tokens.access_token' "$HOME/.gmail-mcp/credentials-<alias>.json")"
curl -s -H "Authorization: Bearer $tok" \
  "https://gmail.googleapis.com/gmail/v1/users/me/profile"
unset tok
```

`<alias>` = the email, lowercased, with `@`/`.`/`+` replaced by `_` (matches
`gmailAlias` in `packages/gmail-mcp.nix`, where it is **derived, never passed in** — e.g.
`a@b.com` → `a_b_com`). It names both the launcher binary (`nix-mcp-gmail-a_b_com`) and the
per-account credentials file, which is why the account list cannot simply be read from a local
file at runtime.

## Failure modes

| Symptom | Action |
|---|---|
| `redirect_uri_mismatch` | Client is Web-app type — create a Desktop app client instead |
| Auth rejects the account | Add it as a Console test user first — but if the screen says "can only be used within its organization", the client is Internal and a test user cannot fix it (Audience → Make external) |
| Worked before, now `invalid_grant` | Testing-status 7-day refresh-token expiry — just re-auth that account |
| Declared in the Nix list but never worked | Roster ≠ credentials on disk; nothing reconciles them. Compare against `ls ~/.gmail-mcp/credentials-*.json` (names only) |
| Verified email doesn't match target | Known failure mode above — check the default-path file before re-running |
| One account's server exits immediately at spawn | No completed auth for that account yet — cannot affect the others, each is its own process and (since 2026-10-01) its own per-session child, so there is no shared proxy left to dark |
| New account not visible after `activate` | Three distinct causes, check in this order: Nix file not staged (`git add`); the `gmail` plugin's `.mcp.json` doesn't name the new launcher; or the session **predates** the change — start a fresh one. **No `nix flake check` leg can see any of this** |
| Launcher is on PATH and auth verified, but still no tools | The `gmail` plugin isn't enabled, or you are in a stale session. Prove it with `claude mcp list` in a fresh process, then invoke a tool with the plugin-lane `--allowedTools` spelling (see `docs/mcp-gateway.md` § How to verify a plugin-owned server actually answers) |

## Removing an account

Remove from `local.gmailMcp.accounts` (`hosts/macos.nix`),
evaluate/commit/push/activate, **remove its entry from the `gmail` plugin's
`.mcp.json` too** (otherwise Claude Code keeps trying to spawn a launcher that
is no longer on PATH), then `rm ~/.gmail-mcp/credentials-<alias>.json`. See
runbook for full rotation/revocation steps.
