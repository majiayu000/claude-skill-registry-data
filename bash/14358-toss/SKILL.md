---
name: toss
description: File a reproducible bug report directly into another registered x-kit project's inbox — captures a repro command + output (secret-redacted), a fix direction, writes a durable local outbox record, and best-effort notifies the target via mem-mesh. Use when a repro found while working in project A actually implicates project B's code, or the user says "toss this to <project>" / "이거 다른 프로젝트 버그같은데 던져줘".
---

# x-toss — Cross-Project Bug Handoff

## Overview

When work in project A surfaces a bug that actually belongs to project B, `/xm:toss`
files the report directly into B without switching sessions or directories. It:

1. Captures the repro command + its actual output (redacted for secrets, tail-bounded)
2. Writes a durable record into the SENDER's own `.xm/outbox/<id>.json` via the CLI —
   this succeeds even if step 3 never happens
3. **You (the skill), not the CLI, deliver a pin + memory into the TARGET project's
   mem-mesh space** by calling the `mcp__mem-mesh__pin_add` / `mcp__mem-mesh__add` tools
   directly, using the exact arguments the CLI printed in step 2
4. You record the returned `pin_id`/`memory_id` back into the same outbox item via
   `xm inbox record`

Toss never touches the target project's `.xm/` directly (ownership invariant) — only its
own outbox. **The CLI itself makes zero network calls** — it has no MCP session and no
auth, so it cannot call mem-mesh. Delivery only happens when the Skill runs in Claude
Code or Codex with live mem-mesh MCP tools and makes the calls itself.

## When to Use

- "이거 우리 프로젝트 버그가 아니라 git-kit 버그 같은데 던져줘" / "toss this to git-kit"
- A repro command's output implicates another **registered** project's code, not this one
- You want the other project to see the report next session without opening this repo
- The user explicitly asks to notify a Claude session or queue a Codex session about that same durable report

## Do NOT Use When

- The bug is in THIS project — just fix it, or file it with `/xm:later` instead.
- The target isn't a registered x-kit project (`xm project list`) — register it first
  (`xm project add <path>`); toss refuses to guess an unregistered name.
- You don't have a concrete repro command + actually-captured output yet — get that
  first. Toss refuses a "be careful"-level report with no repro/fix direction.

## CLI Invocation

> **⚠ Call `xm toss` directly. Claude Code's Bash tool starts a fresh shell on every invocation — shell functions (`xtoss()`) defined in one call do NOT persist to the next, causing `command not found: xtoss`. Never define a helper across calls; always use the dispatcher.**
>
> **Fallback** (only when `xm` is not in PATH — rare; `${CLAUDE_PLUGIN_ROOT}` is NOT exported to Bash subprocesses, so don't rely on it bare):
> ```bash
> XTOSS_CLI=$(ls -d ~/.claude/plugins/cache/xm/xm/*/lib/x-inbox-cli.mjs 2>/dev/null | sort -V | tail -1)
> node "$XTOSS_CLI" toss <project> "<title>" --command "<cmd>" --output "<text>" --fix "<text>"
> ```
>
> **Forbidden:** `XTOSS="node ..."; $XTOSS toss ...` — zsh treats the quoted string as a single command and fails.

## Core Process

1. **Confirm the target is registered.** If unsure, run `xm project list` first (or let
   the CLI's own `resolveTarget()` reject an unregistered/ambiguous name) — never guess
   a project id that "looks close enough."
2. **Gather the four required pieces** before calling `xm toss`:

   | Flag | Content |
   |------|---------|
   | `<project>` | exact registry id from `xm project list` |
   | `"<title>"` | one-line problem statement |
   | `--command` | the exact reproducible command |
   | `--output` (or `--output-file <path>`) | actual captured stdout/stderr — never a paraphrase |
   | `--fix` | concrete fix direction — "be careful" is refused |
   | `--why` (optional) | why this matters / context |
   | `--to-files` (optional) | comma-separated files the fix likely touches |

3. **Capture + write the local record, with `--json`:**
   ```bash
   xm toss <project> "<title>" --command "<cmd>" --output "<captured text>" --fix "<fix direction>" [--why "<text>"] [--to-files a.js,b.js] --json
   ```
   On success this ONLY writes `.xm/outbox/<id>.json` and prints
   `{ ok, outbox_path, item_id, mem_mesh_project_id, mcp_calls: { pin_add, add } }`.
   It has not delivered anything to mem-mesh yet — that is your next step.

4. **Deliver it yourself, via MCP, using the printed arguments verbatim:**
   - `mcp__mem-mesh__pin_add(**mcp_calls.pin_add)` → capture the returned pin id.
   - `mcp__mem-mesh__add(**mcp_calls.add)` → capture the returned memory id.
   - Do not alter `content`, `project_id`, or `tags` — they were built by the CLI from
     the captured item and the resolved target identity; the target's `tags` MUST stay
     `["inbox"]` so the receiving side (mem-mesh reading tags) recognizes it as a toss.
   - `pin_add.content` deliberately starts with `<toss id> —`. The receiver uses that
     exact id to find the durable JSON memory because mem-mesh `search` cannot filter
     by tags. Preserve it verbatim.

5. **Record what happened back into the ledger:**
   ```bash
   xm inbox record <item_id> --pin-id <returned pin id> --memory-id <returned memory id> --json
   ```
   Run this even on a partial outcome (e.g. `pin_add` succeeded but `add` failed) —
   pass whichever id(s) you actually got; the CLI merges, it doesn't require both.

5a. **Optional live notice, only when the user requested it:** after both the pin and memory
   IDs have been recorded, use `/xm:relay sessions <project>` to find a recipient.
   Claude's native route reaches independent local Claude sessions. On macOS and Linux, Codex
   can target a local Claude session's inbox socket or list saved Codex threads on the shared App Server daemon;
   a listed Codex thread is not proof its UI is open. In Claude Code, use `--provider codex`
   when the user chooses a Codex thread; in Codex, use `--provider claude` for a local Claude
   session. If more than one candidate matches, let the user choose; never guess from a name or
   stale listing. If Claude
   withholds working directories, ask the user to select a specific address and disclose that
   its project affiliation is unverified. Use `/xm:relay send <session> <notice>` with the
   selected provider to send the toss ID, redacted title, source
   and target project IDs, and a pointer to `/xm:inbox`. The receiver's current task and
   permissions remain its own. Claude reports the native delivery result; Codex-to-Codex
   reports only that the message was queued and may run when its thread is next active;
   Codex-to-Claude reports only that message bytes were submitted to the local socket, not that
   Claude received them. Neither is an inbox
   `take` or a fix receipt. If the selected provider is unavailable, no target matches, the
   message is held/refused,
   or either mem-mesh ID is missing, report that separately and keep the durable outbox state.
   Do not send raw reproduction output or write the target project's `.xm/inbox/` directly.
   This is a Skill-only option expressed in the user's request (for example "toss this and
   notify the running session"); do not pass `--live` or `--notify-session` to `xm toss`.

6. **Report the actual outcome, not an assumption:**
   - *Delivered* — relay the outbox path and the pin/memory ids you got back from MCP.
   - *No MCP tools available (plain shell, no Claude Code session)* — this is a DESIGNED
     degraded path, not a tool failure: the local outbox write already succeeded in step
     3. **Say so explicitly to the user** — e.g. "recorded locally at `.xm/outbox/<id>.json`,
     but I have no MCP access here so it was never delivered to mem-mesh; deliver it from
     a session with mem-mesh MCP tools, or the receiving side's `xm inbox list` will not
     show it." Never claim delivery succeeded when you skipped steps 4-5.
   - *An MCP call itself failed (mem-mesh unreachable/error)* — same idea: outbox write
     already succeeded, tell the user it's recorded locally and mem-mesh delivery failed,
     with the specific tool error.
   - *Target unregistered/ambiguous* — relay the exact message and candidate list;
     ask the user to re-run with the exact id. Never silently pick one.
   - *Live notice requested* — report durable delivery and live message outcome on separate
     lines. A successful Claude `SendMessage` or Codex queue does not prove the receiving
     session took the report.

7. **Check terminal receipts when you need to know whether the target acted.** A delivered
   toss is not proof of a fix. The receiving inbox sends an immutable `inbox-receipt`
   memory after resolve/drop. Materialize it only after obtaining the receipt content from
   mem-mesh, then run:
   ```bash
   xm inbox receipt materialize <toss-id> --content '<receipt JSON>' --json
   xm inbox receipt status <toss-id> --json
   ```
   The CLI rejects a receipt for another source project, a receipt whose origin does not
   match this outbox's recorded target mem-mesh identity, and contradictory late receipts.
   Replaying the same receipt is idempotent. Do not infer completion from `take`: only a
   materialized receiver terminal receipt closes the sender outbox lifecycle.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll skip --output and just describe what happened." | The CLI refuses an empty `--output` by design — a bug report without real captured output isn't reproducible for the receiving side. |
| "Close-enough project name, I'll just try it." | `resolveTarget()` never guesses; an inexact match returns `ambiguous` with a candidate list. Re-run with the exact id instead of picking one for the user. |
| "The mem-mesh MCP call failed, so the toss failed." | The outbox write (the durable record) already succeeded before you made any MCP call — that IS the Degraded Path by design. Report the local record, not just the transport error. |
| "No MCP tools in this environment, I'll just say 'toss complete' since the CLI exited 0." | The CLI exiting 0 only means the outbox was written and the payload was printed — it never claims delivery. Skipping the MCP calls means nothing reached mem-mesh; say that plainly. |
| "I'll write --fix \"investigate further\"." | `fixDirection` must be a concrete direction; a vague placeholder defeats the "earn the send" bar the tool enforces. |
| "I'll paste the output back to the user as if it were the full raw capture." | The CLI redacts secrets and truncates to the last 2000 chars before storing — say that happened, don't claim it's the untouched original. |
| "No target given, I'll toss to the first project in the list." | An empty/missing `<project>` or `<title>` is refused outright (usage error) — never default to guessing a target. |
| "I'll tweak `mcp_calls.pin_add.tags` before calling MCP, the value looks arbitrary." | It's `["inbox"]` on purpose — the receiving side's re-notification logic and mem-mesh's own tag reading depend on this exact value. Pass it through unchanged. |
| "I called pin_add/add but skipped `xm inbox record` since the ids are in my chat output anyway." | The ledger file, not your chat transcript, is what the receiving side and future sessions read. Un-recorded ids are lost the moment this conversation ends. |

## Red Flags

- You typed a project name without checking `xm project list` first.
- You wrote `--output` from memory/description instead of an actual captured command run.
- You told the user "delivered to mem-mesh" without actually having called `pin_add`/`add` yourself.
- You called `pin_add`/`add` but never ran `xm inbox record` to persist the returned ids.
- You picked one candidate from an `ambiguous` result yourself instead of asking the user.
- You had no MCP tools available and didn't tell the user delivery never happened.

## Verification

- `xm toss ... --json` was run and its `mcp_calls` payload was passed to `pin_add`/`add` unmodified (aside from filling in `content`/`project_id`/`tags` already provided).
- `xm inbox record` was run with whatever id(s) MCP actually returned, even on a partial outcome.
- The reported outcome matches what actually happened: outbox path always shown; MCP delivery reported only if you actually made those calls, with their real result (success, partial, failed, or skipped because no MCP tools were available).
- `--output` reflects real captured text, not a summary.
- `--fix` names a concrete next step, not "investigate further."
- On an unregistered/ambiguous target, the user was asked to confirm rather than a guess being made.
