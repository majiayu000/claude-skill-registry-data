---
name: refresh-claude-account
description: Repair a dead or expired Claude Code account by restoring a full OAuth login — re-seed it from a machine that still has a live copy, or re-authenticate with `claude auth login` — then capture it with `cswap add` and export `claude-accounts.json` for the `sync-claude-accounts` skill to distribute. Use when `cswap list` says "re-login needed — refresh token dead", when `cux status` shows an account as EXPRD, when `cswap auto --dry-run` reports null headroom, or when `fleet-refresh-credentials` aborts because the refresh authority holds a dead account.
---

# Repair a dead Claude account (OAuth)

Restores an account to a **full OAuth login** — `accessToken` + `refreshToken` + `expiresAt` +
the complete scope set — and produces a `claude-accounts.json` that
the `sync-claude-accounts` skill distributes to the rest of the fleet.

OAuth is the only credential that works end to end here. It is the only one that can report
usage (`/api/oauth/usage` needs `user:profile`), and usage is what drives rotation at all —
`cswap auto` is purely usage-polling. cux, which is what the fleet actually rotates with
(it is the only layer that can continue an unattended session through a rate limit), is built
around the `/login` credential bundle and cannot hold anything else. So a repair that does not
end in a full OAuth bundle leaves the account unrotatable. See "Why not setup-tokens" at the
bottom.

## Pick the cheap path first

| | Path A — re-seed | Path B — re-authenticate |
|---|---|---|
| **Use when** | Any machine still holds a live copy of this account | The account is dead everywhere |
| **Needs a browser** | No | Yes, and the user must drive it |
| **Interrupts sessions** | No | Yes — rewrites the machine-global login |
| **Effort** | Two commands | Interactive OAuth round trip |

Always check Path A first. On a fleet, an account that died on one machine is very often
still alive on another — the refresh-token race has a *winner*, not just losers, and the
winner's credential is a perfectly good seed.

## Why the refresh token died

`cswap add` stores a full OAuth credential and renews it by POSTing `grant_type=refresh_token`.
**The server rotates the refresh token on every use**, so the lineage is single-use: if anything
else spends it — a parallel session, cux, a fleet peer that imported the same export — the stored
copy becomes a spent generation and the next refresh returns `invalid_grant`. That verdict is
permanent on the first strike (`AUTH_DEAD_STRIKES = 1`), which is why the account goes straight to
`re-login needed` with no retry.

It is a race, not a hierarchy: the loser can be either machine and the survivor looks fine, which
is why this reads as accounts dying at random days later rather than at import time.

**Repairing the credential does not fix the cause.** If N machines keep refreshing the same
account, it will die again within days. The structural fix is a single-writer refresh authority —
exactly one machine may refresh, and it pushes its credentials to the others, which only ever
*consume* access tokens. On this fleet that is
`~/.local/bin/fleet-refresh-credentials` on **mac-mini-m2**.

## 1 — Detect

```bash
cswap list                          # "re-login needed — refresh token dead"
cswap list --token-status           # per-slot: refresh token yes/no, expiry
cswap auto --once --dry-run --json  # null headroom = unreadable usage; never switches
```

`cux list` shows the same accounts as `EXPRD`. Collect the **email and slot number** of every
dead account.

Three red herrings:
- `usage unavailable (http-429)` is the usage probe being rate-limited — transient, unrelated
  to expiry. `http-403` is different and real: that credential lacks `user:profile`.
- cux caches its verdict. A just-healed account keeps showing `EXPRD` until `cux list --refresh`.
- **cux also shows the reverse — a long-dead account rendered `READY` with usage bars.** Same
  cache, opposite direction, and far more dangerous because it reads as health and can talk you
  out of a repair that is genuinely needed. The tell is that the numbers *disagree between
  machines*: one account polled live at one moment must return one answer, so `38%/91%` on one
  host and `20%/86%` on another proves both are stale. Observed 2026-08-19 on an account cswap
  correctly reported dead on all five machines. **cswap's verdict is authoritative here; cux's
  display is not** — and `cux-backup` keychain items cannot be inspected to settle it, as they
  are not JSON.

Confirm "dead" against cswap before spending an interactive login on it:

```bash
cswap list --token-status                     # per slot: fresh/expired + refresh token yes/no
cswap auto --once --dry-run --json | head -1  # headroomPct null for that slot = unmeasurable
```

## 2 — Path A: re-seed from a machine that still works

Find a machine whose copy of that account is healthy (usage percentages render, no
`re-login needed`), export just that account, and import it authoritatively:

```bash
# on the healthy machine — NOTE: path before flags, cswap's argparse requires it
cswap export /tmp/acct.json --account someone@example.com
chmod 600 /tmp/acct.json

# on the broken machine
cswap import /tmp/acct.json --force
rm -f /tmp/acct.json      # also remove it on the source machine
```

Expect `Overwrote <email> (slot N)` followed by `└ cleared this slot's stored dead-token
strike` — that second line is cswap lifting the permanent quarantine, and is how you know the
repair took.

The account is now shared by two machines, so the race is live again until the single-writer
discipline covers it — push from the authority (step 5) promptly.

Skip to step 4.

## 3 — Path B: re-authenticate

Only when the account is dead on every machine. **This is not out-of-band**: `claude auth login`
rewrites the machine-global credential, and step 3a rewrites it again. Every running Claude
session on this machine flips accounts mid-flight. Do it at an idle moment, and tell the user
before you start.

**3a. Make the dead slot live first.** The new login must land on the slot it belongs to:

```bash
cswap switch <slot> --force
```

Order matters. If you log in while cswap thinks a *different* slot is active, the live bytes no
longer match cswap's idea of the active account — the `displaced-live-login` condition — and the
next `cswap switch` backs the new credential up over the **wrong** slot, corrupting a healthy one.

**3b. The user signs in** (interactive browser OAuth — hand it over; inside a Claude Code session
they can run it with a leading `!`):

```bash
claude auth login --email someone@example.com
```

`--email` pre-populates the login page, which is the main guard against authorizing the wrong
account.

**3c. Verify the right account actually authorized**, before capturing it:

```bash
claude auth status
```

Returns JSON — check `email` matches the target and `subscriptionType` is a paid tier:

```json
{"loggedIn": true, "authMethod": "claude.ai", "email": "someone@example.com",
 "orgName": "...'s Organization", "subscriptionType": "max"}
```

A mismatch here means the browser signed in as the wrong account. Redo 3b; do not capture it.

**3d. Capture it into the slot:**

```bash
cswap add --slot <slot>
```

`cswap add` stores whatever is *currently live*, which is why 3c comes first.

**3e. Restore the account that was active before**, so you leave the machine as you found it:

```bash
cswap switch <original-slot> --force
```

### Run 3a–3e as one trapped script, from a separate terminal

Two things make the bare sequence fragile in practice, both observed 2026-08-19:

- **Between 3a and 3e the machine is live on the dead account.** If the user abandons the
  browser flow — closes the tab, Ctrl-C, authorizes the wrong account — the machine is
  *stranded* there, and every Claude session on it stays broken until someone notices. A trap
  makes the restore unconditional.
- **`cswap add` stores whatever is currently live.** If the browser signed in as the wrong
  Google/Anthropic account, 3d silently overwrites the target slot with the wrong identity.
  3c must therefore *gate* 3d, not merely precede it.

Do not run this inside a Claude Code session on the machine being repaired — 3a rewrites the
machine-global login, so that session flips onto the dead account mid-flight. Use a separate
terminal.

```bash
#!/bin/bash
set -uo pipefail
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
TARGET_EMAIL="someone@example.com"; TARGET_SLOT=1; ORIG_SLOT=2

restore() { cswap switch "$ORIG_SLOT" --force </dev/null \
            || echo "!! RESTORE FAILED — run: cswap switch $ORIG_SLOT --force"; }
trap restore EXIT INT TERM                      # survives Ctrl-C and any early exit

cswap switch "$TARGET_SLOT" --force </dev/null || exit 1      # 3a
claude auth login --email "$TARGET_EMAIL"       || exit 1      # 3b (browser)

GOT="$(claude auth status 2>&1 | /usr/bin/python3 -c \
  'import json,sys
try: print(json.loads(sys.stdin.read()).get("email",""))
except Exception: print("")')"                                 # 3c
[ "$GOT" = "$TARGET_EMAIL" ] || { echo "authorized as \"$GOT\" — NOT capturing"; exit 1; }

cswap add --slot "$TARGET_SLOT" </dev/null      || exit 1      # 3d
# 3e happens in the trap
```

## 4 — Verify

```bash
cswap list --token-status
```

Done when the repaired email appears exactly once, with **`refresh token yes`**, no
`re-login needed`, and real 5h/7d percentages instead of `http-403`. Usage rendering is the
proof the credential carries `user:profile` — i.e. that cux and `cswap auto` can see it.

Then clear cux's cached verdict and confirm it agrees:

```bash
cux list --refresh
```

Confirm the credential actually works with a real call — `claude -p 'say ok'` on the active
slot, or `cswap run <slot> -- -p 'say ok'` for any other.

Repeat 2–4 for each dead account.

## 5 — Export `claude-accounts.json` and hand off

```bash
cd ~ && cswap export claude-accounts.json && ls -l claude-accounts.json
```

**Write it outside any git repo** — cswap exports credentials in plaintext, so an export dropped
in a working tree is one `git add -A` away from publishing account access. `cd ~` first. cswap
writes mode `600`; confirm it.

**Refuse to publish an export that still contains a dead account.** `sync-claude-accounts` uses
`--force`, which overwrites every receiver — so pushing a dead slot destroys working copies
elsewhere. This is not hypothetical: the authority once held a dead copy of an account while a
single receiver held the only live one; pushing would have killed it fleet-wide.

```bash
cswap list | grep -c 're-login needed'    # must print 0 before you sync
```

Then distribute with the `sync-claude-accounts` skill:

```bash
IMPORT_FORCE=1 scripts/push-claude-accounts ~/claude-accounts.json <hosts...>
rm -f ~/claude-accounts.json
```

`N ok, 0 failed` is **not** proof the receivers took the repaired credential — a machine whose
active slot is that account keeps its old one and still reports success. Verify by fingerprint
on every host and fix any that did not converge; both the check and the repair sequence are in
`sync-claude-accounts` ("After you push, verify convergence").

On a fleet with a refresh authority, repairing **on the authority** is enough — its scheduled
push distributes the fix on the next cycle, and `fleet-refresh-credentials` has the same
dead-account guard built in (it aborts rather than publishing a bad export). Repairing on a
*receiver* instead will be silently overwritten by the next push, so repair the authority.

Every account in the export carries a rotating `refreshToken`. That is expected and required —
it is what makes the account renewable and measurable. Keeping it alive across machines is the
single-writer authority's job, not this skill's.

## OAuth login vs setup-token

Both are OAuth credentials for the same subscription, minted through the same browser
authorization flow. The difference is what you receive and what it is allowed to do.

| | `claude /login` (OAuth login) | `claude setup-token` |
|---|---|---|
| **What you get** | A bundle: `accessToken` + `refreshToken` + `expiresAt` + `scopes` (observed structure, not officially documented) | One bearer token (`sk-ant-oat01-…`), printed once, saved nowhere |
| **Access token life** | Short-lived (order of hours; ~8h commonly observed, undocumented) | ~1 year |
| **Renewal** | Automatic silent refresh — but **not indefinite**: the stored login itself expires. Claude Code warns 3 days out; after expiry, requests fail until you re-run `/login` | None; re-run `claude setup-token` before it expires |
| **Capabilities** | Full: inference, Remote Control, claude.ai connectors, file upload, etc. (scope strings like `user:inference`, `user:profile`, `user:sessions:claude_code`, `user:mcp_servers`, `user:file_upload` are observed, version-dependent) | Model requests only. No Remote Control, no claude.ai-hosted connectors. **Locally configured MCP servers still work** |
| **Storage** | macOS: encrypted Keychain (`Claude Code-credentials`). Linux: `~/.claude/.credentials.json` (mode 0600). Windows: `%USERPROFILE%\.claude\.credentials.json`. Rewritten on each refresh | Nowhere — you copy it and set `CLAUDE_CODE_OAUTH_TOKEN` yourself |
| **Shareable across machines** | Fragile — copying the bundle breaks when either machine refreshes (rotation is observed, not documented) | Yes — intended for CI, scripts, headless environments. Usage still counts against the one subscription; sharing across *people* violates ToS |
| **Gotchas** | — | Not read in bare mode (`--bare`) — use `ANTHROPIC_API_KEY` / `apiKeyHelper` there. In precedence, `CLAUDE_CODE_OAUTH_TOKEN` ranks **below** `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY`, and `apiKeyHelper`, but **above** `/login` credentials — a stray env var silently wins over your interactive login |

The table names the in-session slash command `/login`; the CLI equivalent used in step 3b of
this skill is `claude auth login`. Same flow, same resulting bundle.

### Why this skill mints OAuth, not setup-tokens

An earlier version minted setup-tokens, because they carry no refresh token and so cannot lose
the rotation race. That was withdrawn — verified 2026-08-17, cux 0.3.9 and cswap 0.25.0:

- **cux cannot manage them at all.** It reads the live login only from the
  `Claude Code-credentials` keychain item; with a setup-token live, `cux add` answers
  `no active Claude Code login found` — and exits **rc=0**, so it fails silently.
- **They cannot be measured.** Scope is `user:inference` only, so `/api/oauth/usage` returns
  **403** (vs 200 for OAuth). `cswap auto` reports null headroom and `_pick_target` skips
  null-headroom candidates, so such an account can never be a rotation target.

Net: a setup-token survives being shared but cannot participate in automatic rotation, which
defeats the purpose of a multi-account fleet. Use OAuth plus a single-writer authority instead.

Two corollaries of the table worth pulling out, because both bite in practice:

- **`CLAUDE_CODE_OAUTH_TOKEN` outranks the interactive login.** A leftover export in a shell
  profile means every `claude` call in that shell runs as the token's account regardless of
  what `cswap`/`cux` believe is active — which looks exactly like a switching bug. Corroborated
  here 2026-08-17: `CLAUDE_CODE_OAUTH_TOKEN=<setup-token> claude -p …` answered on the token's
  account while the keychain held a different live login. Check `env | grep -i
  'ANTHROPIC\|CLAUDE_CODE_OAUTH'` before believing a switching problem is real.
- **An OAuth login expires as a whole**, not just its access token, so "automatic refresh" is
  not forever. When the login itself lapses, no amount of redistribution helps and Path B
  (re-authenticate) is the only repair.

Identify a stray setup-token by `refreshToken: false` / `scopes: ['user:inference']` — **not** by
the token prefix (both kinds start `sk-ant-oat01-`) and not by where it is stored (it can live in
the keychain on one machine and in `~/.claude/.credentials.json` on another).

## Verification status

Verified on this fleet 2026-08-17: Path A end to end (including the dead-token-strike clearing),
`cswap add --slot`, `cswap list --token-status`, `cux list --refresh`, the export/`--force`
overwrite semantics, and the `claude auth status` JSON shape. Also directly observed: the
403-vs-200 split on `/api/oauth/usage` between a setup-token and an OAuth login for the same
subscription, and `CLAUDE_CODE_OAUTH_TOKEN` overriding a different live keychain login.

Path B was executed end to end on this fleet 2026-08-19, on an account dead on all five
machines (so Path A was genuinely unavailable). Confirmed in that run: `claude auth login
--email`, the `claude auth status` JSON shape (`loggedIn`, `authMethod`, `apiProvider`,
`email`, …), `cswap add --slot N` capturing the new login into the intended slot, and the
repaired account going from `headroomPct: null` to a real percentage — i.e. measurable, and
therefore rotatable, again. The trapped-script form above is what that run used.

Not yet exercised: the 3c mismatch branch (authorizing the wrong account) has never actually
fired, so its refusal path is reasoned rather than observed.

In the comparison table, items flagged *observed* / *undocumented* (token lifetimes, the exact
credential structure, scope strings, refresh-token rotation) are behaviour seen in practice
rather than published guarantees — they can change between Claude Code versions, so re-check
them before depending on a specific number.

## Related

- `sync-claude-accounts` — distributes the `claude-accounts.json` this skill produces
- `sync-claude-accounts` — the scheduled push/monitor agents that call both, and the alerts
  (`ABORT`, dead slots, null headroom) that send you here in the first place

## Security

An export is a set of live account credentials in plaintext. Mode `600`, delete it after import,
never commit it, and keep tokens out of argv and out of your replies.
