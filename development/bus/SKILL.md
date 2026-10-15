---
name: bus
description: Read or post to the coordination bus (append-only TSV message log).
version: 0.1.2
execution-mode: side_effecting
argument-hint: "[post \"MESSAGE\" | tail [N] | search \"PATTERN\" | status]"
category: fleet-ops
status: candidate
---
## Context Gathering

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: host=agent-node surface=<observed-surface> lane=<lane> [skill=bus] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(Use the caller's bare canonical identity as `from`; for Codex, use `codex`.
On agent-node, send the receipt with `bus-post.ps1` as shown below. Replace metadata
placeholders with observed values; use `unknown` for an unevidenced surface.)

Before executing this skill, gather the following context:

**On Windows (PowerShell):**
- Run `python $HOME\bin\bus-global.py status` (if error → "global bus status unavailable")
- Run `python $HOME\bin\bus-global.py tail 5` (if error → "global bus not readable")

**On Unix (bash/zsh):**
- Run `python ~/bin/bus-global.py status 2>/dev/null || echo "(global bus status unavailable)"`
- Run `python ~/bin/bus-global.py tail 5 2>/dev/null || echo "(global bus not readable)"`

# Bus Command

## When to Use
- Checking what agents have been doing
- Posting coordination messages
- Debugging agent communication issues
- Monitoring multi-agent workflow progress
- Searching for specific events or decisions
The canonical coordination bus is hosted on `hummbl-vps` and exposed at
`https://bus.hummbl-dev.com`. Use the canonical client to read it:

- On agent-node: `python $HOME\bin\bus-global.py tail 20`.
- Local read cache: `~/.cache/bus/messages.tsv` (or `%USERPROFILE%\.cache\bus\messages.tsv` on Windows). A cache is never the bus authority or a direct write target.
- The founder-mode TSV is retired [RETIRED: 2026-09 remote-bus migration]. Never use it as authority or append to it.
- `CACHED_MIRROR` output is cached evidence; preserve that label and its freshness information when reporting activity.

## Usage

```bash
[bus]                     # Default: show global bus status
[bus] tail 20             # Show last 20 global bus entries
[bus] search "PATTERN"    # Search global bus entries by pattern
[bus] post "MESSAGE"      # Post to the global bus (default: caller -> all SITREP)
[bus] post "MESSAGE" TYPE # Post with an allowed type (STATUS, BLOCKED, REVIEW, etc.)
[bus] status              # Report client bridge/cache status and freshness
```

Concrete commands on agent-node:

**PowerShell (recommended on Windows):**
```powershell
# Use $HOME instead of ~ in PowerShell
python $HOME\bin\bus-global.py status
python $HOME\bin\bus-global.py tail 20
python $HOME\bin\bus-global.py search "SITREP"   # bridge first; labeled cache fallback

# Inspect recent posts; preserve any CACHED_MIRROR warning in the result:
python $HOME\bin\bus-global.py tail 20 | Select-String -Pattern "^# CACHED_MIRROR|SITREP" -CaseSensitive:$false

# For regex/alternation (search is substring-only, not regex):
python $HOME\bin\bus-global.py tail 100 | Select-String -Pattern "^# CACHED_MIRROR|doc-cleanup|PR #738"
```

**Git Bash / WSL (if preferred):**
```bash
python ~/bin/bus-global.py status
python ~/bin/bus-global.py tail 20
python ~/bin/bus-global.py search "SITREP"
python ~/bin/bus-global.py tail 20 | grep -iE "^# CACHED_MIRROR|SITREP"
python ~/bin/bus-global.py tail 100 | grep -iE "^# CACHED_MIRROR|doc-cleanup|PR #738"
```

To post a SITREP to the bus:
```
Type: SITREP
To: all
Message: host=agent-node surface=<observed-surface> lane=<lane> Task complete. Ready for review.
```
(Send with the caller's bare canonical identity through the host's approved writer.)

## Bus Format

The bus is a TSV file with these columns:
```
timestamp_utc	from	to	type	message
```

### Rules (from CAES spec)
- **UTC timestamps only**:
  - Unix: `date -u '+%Y-%m-%dT%H:%M:%SZ'`
  - Windows PowerShell: `(Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")`
- **Append-only** -- NEVER edit or delete historical entries
- **Z suffix** -- use `Z` not `+0000` for UTC indicator

### Valid Types
The canonical client accepts `SKILL_INVOKE` and the operational message types
reported by `python ~/bin/bus-global.py permissions` (on Windows,
`python $HOME\bin\bus-global.py permissions`). `DECISION` and `DIRECTIVE`
require authenticated operator principal proof; the current client rejects
these types because it does not accept that proof. Use agent-authored
`STATUS` or `REVIEW` for findings, retaining the provenance of any operator
instruction. A bus type check does not replace the sender's actual scope or
credential restrictions.

## Posting

On agent-node, use the Windows Credential Manager-backed wrapper. It requires
four positional arguments: sender, recipient, type, and message.

```powershell
& "$HOME\bin\bus-post.ps1" codex all SITREP "host=agent-node surface=<observed-surface> lane=<lane> Task complete. Ready for review."
```

For an invocation receipt:
```powershell
& "$HOME\bin\bus-post.ps1" codex all SKILL_INVOKE "host=agent-node surface=<observed-surface> lane=<lane> [skill=bus] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]"
```

- These examples are for Codex on agent-node. Other callers use their own canonical sender and observed host/surface; never infer identity from a model or executable.
- Skill shorthand defaults to `to=all`, `type=SITREP`; the concrete wrapper requires both arguments explicitly.
- The wrapper loads the bridge credential from Windows Credential Manager and invokes `bus-global.py post`. Never put credentials in a message or command-line argument.
- The client delivers through the configured bridge, with an existing SSH fallback for retryable bridge failures. Local cache refresh is not a local bus write.
- Never append directly to any mirror/cache or the retired founder-mode TSV [RETIRED: 2026-09 remote-bus migration].
- Read the delivery result: an exit code of 0 alone does not distinguish canonical delivery from local queue preservation.

### Offline ordering for invocation receipts

`SKILL_INVOKE` is an allowed offline-queue type. For a retryable bridge
failure with no successful SSH delivery, or an active offline marker, the
client can preserve the intended type and message in the local queue for
ordered delayed replay. Authentication or other non-retryable failures are
not proof of a queued receipt.

When the assigned scope calls for preserving an offline invocation receipt,
the existing `--queue` option deliberately queues without a delivery attempt.
This is a queue-only client operation, not an alternative live writer:

```powershell
python "$HOME\bin\bus-global.py" post codex all SKILL_INVOKE "host=agent-node surface=<observed-surface> lane=<lane> [skill=bus] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]" --queue
```

A successful queue operation includes `OFFLINE-QUEUED` or
`OFFLINE-QUEUED-DUPLICATE` in its output. Automatic fallback can prefix that
receipt with `POSTED`; it still records local intent, not canonical delivery.
Report the queue receipt as pending until canonical delivery/replay is
evidenced. Never queue privileged `DECISION` or `DIRECTIVE` messages.

### PROPOSAL posts — proposal_id generation

PROPOSAL messages should include a `[proposal_id=<8-hex>]` field for
threading. Use an existing proposal ID when following that proposal. The
client generates an ID when omitted, but currently prepends it ahead of the
message; provide the field after `host=agent-node` to preserve the required prefix.

```powershell
& "$HOME\bin\bus-post.ps1" codex all PROPOSAL "host=agent-node surface=<observed-surface> lane=<lane> [proposal_id=<8-hex>] <proposal>"
```

Replace `<8-hex>` with the actual proposal ID; do not post placeholders.
For a new proposal, an available host-approved ID helper may supply the value.

## Reading

On Windows (PowerShell), read through the canonical client:
```powershell
python "$HOME\bin\bus-global.py" tail 20
```

On Unix (bash/zsh) with the approved client installed:
```bash
python ~/bin/bus-global.py tail N
```

The client tries the canonical bridge first. If it falls back to a local
cache, report its `CACHED_MIRROR` label and freshness rather than claiming
current live activity. `status` may refresh the cache; read operations do
not append messages to the canonical bus.

### Concurrent Work Check

After scanning HANDOFFs for open items, check for active sessions that may
be working on the same items before acting:

1. **Check for active devin processes:**
   ```bash
   ps -eo pid,etime,cmd | grep "[d]evin"
   ```
   Long-running processes (etime > 10min) may indicate active sessions.

2. **Check for unmatched SKILL_INVOKE [start-session]:**
   ```bash
   python ~/bin/bus-global.py tail 20 | grep -E "^# CACHED_MIRROR|SKILL_INVOKE.*start-session"
   python ~/bin/bus-global.py tail 20 | grep -E "^# CACHED_MIRROR|SKILL_INVOKE.*end-session"
   ```
   If there are start-session entries without matching end-session entries,
   those sessions may still be active.

3. **Check for WIP_START or lane claims:**
   ```bash
   python ~/bin/bus-global.py tail 20 | grep -E "^# CACHED_MIRROR|WIP_START|lane="
   ```
   If another session has claimed a lane or started work on an item, do not
   start the same work. Coordinate via bus PROPOSAL/ACK instead.

Origin: 2026-09-02 AAR — sessions started work on items concurrent sessions
were already completing because the bus scan protocol did not include a
concurrent work check.

### Constraint Verification Before Operator-Level Label

Before labeling an item as requiring operator action, identify the actual
constraint: the current assignment, applicable policy, effective credentials,
or a concrete service/repository restriction. Available credentials establish
technical capability, not permission for new work. Conversely, do not invent
an extra approval requirement for work already authorized by the operator.
Name the specific unmet constraint and supporting evidence when escalating.
Do not require a new bus `DECISION` merely to recognize an existing operator
instruction; authority and the receipt of that authority are distinct.

## Status Check

For `[bus] status`, report the fields actually returned by the client:
- `canonical_live`, configured `bridge_url`, and `hub_host` when present
- Available hub count/write time and cache path/count/write time
- Any `CACHED_MIRROR`, offline-marker, or unavailable-hub information
- Last entry only when returned or separately read; do not invent missing fields

Do not claim whole-bus timestamp or TSV validation from a status response or
a limited tail sample.

## Constraints

- NEVER edit or delete existing bus entries.
- NEVER post empty or test messages to the bus.
- Always use UTC `Z` suffix timestamps.
- Canonical authority: `https://bus.hummbl-dev.com`, hosted on `hummbl-vps`.
- Read-only cache on agent-node: `~/.cache/bus/messages.tsv` (or `%USERPROFILE%\.cache\bus\messages.tsv` on Windows).
- Use `$HOME\bin\bus-post.ps1` for live posts from agent-node; the documented `bus-global.py post ... --queue` exception only preserves local offline intent.
- Keep `from=codex` bare for Codex; start Workstation message bodies with `host=agent-node`, then the observed surface and lane.
- The founder-mode TSV [RETIRED: 2026-09 remote-bus migration] must never be a write target or bus authority.
- Never append to the global mirror file with raw echo/printf or direct local file writes.

## Skill Chains
- For bridge posts delegation receipts to the coordination bus -> `[cross-runtime-bridge]` (`sessions`)

### Mandatory

- No additional skill chain is required for ordinary bus coordination within
  the caller's assigned scope. Use the approved writer and respect actual
  sender/type/credential constraints; append-only storage does not grant authority.

### Advisory

- **After post**: Inspect the receipt and distinguish canonical delivery from queued intent.
- **Read operations**: `tail`, `search`, `status` do not append bus messages; the client may refresh its local cache. No chains needed.
- **For fleet coordination**: `[fleet-status]`, `[sitrep]`, `[agent-roster]`

## Authority

- The operator is the sole owner and final binding authority. Follow the current
  owner-authorized scope and the canonical roster/operating model.
- Trust labels do not bypass sender admission, recipient/type restrictions,
  credentials, data boundaries, or the scope of an assignment.
- Client `permissions` output describes message-type handling, not a grant of
  authority or a live credential/bridge check. The current client rejects
  `DECISION`/`DIRECTIVE` as requiring operator principal proof it cannot accept.
- Preserve operator instructions as operator-authored evidence; do not
  impersonate the operator or treat an agent receipt as a new delegation.
