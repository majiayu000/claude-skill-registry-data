---
name: auth
description: 'Provider credential state across the fleet — classify every profile, print the logins a human must run, watch for expiry and account drift Arguments: [selector] [--provider <id>] [--status] [--print-login] [--watch].'
---

# OpenClaw provider auth

Parse `[selector]` (default: managed), `[--provider <id>]`, `[--status]`, `[--print-login]`,
`[--watch]` from "$ARGUMENTS".

**Repeat is worse than refusal.** A refresh token is single-use, so a second attempt burns the one
another consumer holds: `gate.RETRY_RULES` gives `oauth-login`/`oauth-refresh` **zero attempts**.

## Process

1. **Load `provider-auth`** (`Skill`) — layers, profile states, one-owner rule, probe-free diagnosis,
   printed-login procedure. Then `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" resolve "<selector>" --table`; reads may include `all`.

2. **Classify each instance × provider**, without exercising any credential:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ocexec.py" <instance> --json -- models status --check
   ```
   Exit 0 healthy · 1 expired · 2 expiring (`ocjson.EXIT_CONTRACTS`); add the other probe-free signals from `provider-auth`. States: healthy · expiring · expired · **emptied** · absent · **orphan-runtime** · **shadowed**.

3. **Print the matrix**: instance × provider, state, expiry as a date, account fingerprint, which runtime
   serves the ref. `--provider <id>` narrows to one id from this instance's own catalogue; values never appear.

4. **Root cause before repair.** One fingerprint across several credential directories is
   `fleet.auth.token-sink` — architectural. Repairs leave as `/openclaw-ops:repair <sel> --issue <id>`.

5. **`--print-login` prints, never executes** — the callback is served by the login process itself on a
   loopback port nothing in a container can reach. Emit the five parts `provider-auth` lists, in order.

6. **The non-interactive steps this command runs** — register the backend, demote a dead primary, remove
   a shadowing or dead profile — are mutations carrying the eight blocks
   **TARGET · PRECHECK · CHANGE · BACKUP · IMPACT · VALIDATE · ROLLBACK · APPLY**, ROLLBACK executable
   (`cp <snapshot-path> <profile-path> && … ocexec.py <instance> --yes --plan-id <plan-id> -- gateway restart`).
   Show the plan, stop; `--yes` comes a later turn with the plan id (`gate.py plan mint auth <instance>`)
   as `--plan-id` — an id that was never issued, or was already used, is refused. **Take the fleet
   front lock around the procedure** (why: `provider-auth`):
   ```bash
   TOKEN=$(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/lib/gate.py" lock take fleet-auth --operation "<what>")
   … ocexec.py <instance> --yes --plan-id <plan-id> --lock-token "$TOKEN" -- <args>
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/lib/gate.py" lock release fleet-auth --token "$TOKEN"
   ```
   A single `models auth …` call needs no token — `ocexec.py` takes the lock and names the holder when busy.

7. **`--watch`** — snapshot and compare:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/healthcheck.py" "<selector>" --snapshot --json > /tmp/oc-auth.json
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/report.py" --input /tmp/oc-auth.json --compare-with auto --format md
   ```
   Read the auth family only; thresholds 72 h / 24 h / 0 h. A changed account fingerprint stops the run (`fleet.auth.account-drift`).

## Never

Retry a failed login or refresh · copy a profile between instances (key and static-token entries are
portable, OAuth is not) · read a credential value · leave a dead profile in the rotation, which costs a retry
and a cooldown on every request · point the embedding lane at a subscription session (`memory-ops`).