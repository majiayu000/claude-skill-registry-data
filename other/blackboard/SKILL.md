---
name: blackboard
description: Record and retrieve contemporaneous findings in the repository journal.
---

# Session journal

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/blackboard/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use when the current repository provides a journal, blackboard, or equivalent durable session
record. Read local `AGENTS.md` for the provider, credential, retention, and
subagent-identity rules.

Journal operations are tools of the `vouchington-tooling` MCP server (`vouchington mcp`):
`journal_append`, `journal_entries`, `outbox_status`, `outbox_flush`, `session_ensure`,
`snapshot_export`, and `session_archive`. Harnesses name them differently, so match the bare tool
name: `mcp__vouchington-tooling__<tool>`, `mcp__vouchington_tooling__<tool>` (the hyphen becomes an
underscore), or `vouchington-tooling__<tool>` reached through a `search_tool` and `use_tool` pair,
or the `vouchington-tooling` namespace reached through `GetDynamicTools` and `CallDynamicTool`.
Every call takes an exact `sessionId`, never inferred, whose meaning depends on the tool:

- `journal_append` and `session_ensure`: the session written or ensured, which is the caller's own
  session unless a runner ensures a child identity.
- `journal_entries` and `session_archive`: the session read or archived, which during distillation
  belongs to another agent.
- `snapshot_export`, `outbox_status`, and `outbox_flush`: only the caller. The outbox is per
  worktree, so `outbox_status` and `outbox_flush` report two counts: `pendingCount` is the unsent
  records of that `sessionId`, and `worktreePendingCount` is the unsent records of every session in
  the worktree outbox. `outbox_flush` delivers every retained record in the worktree.
  A permanently rejected record (`identity-conflict`, `event-conflict`, `archived-session`) is moved out
  of the pending set, not retained: `rejectedCount` and `worktreeRejectedCount` count the kept copies,
  `outbox_flush` reports them as `rejected` (`sourceEventId` and `diagnostic`), and a corrected retry
  with the same `sourceEventId` is accepted.

Every call may take `worktree`, the absolute path of a worktree of the current repository (the
launch worktree by default). Writing or retrying an entry needs no provider skill, temporary file,
`--file` flag, or replay command.
Search for `journal_append` (by bare name, so every prefix matches) before concluding the server is
unavailable; a deferred harness lists the tool only on request. A tool error is not
unavailability: act on its message and retry through MCP.

## When the server is unavailable

MCP is the supported journaling path. If the search finds no such tool, stop journaling and tell the
human which case applies before continuing:

- Not registered: the machine's agent configuration must register it; follow the consumer's
  registration and diagnosis steps.
- Registered but disconnected: reconnect it through the harness's MCP controls, or restart the
  harness.
- Automated runs with no human to ask: an unattended `interactive` run continues its primary work,
  while an `autonomous` run keeps its admission gate below. The final report states why journaling
  was unavailable, the `pendingCount` and `worktreePendingCount` (or that none was written), and
  each unjournaled finding.

Harness sandboxes commonly withhold `AGENT_BLACKBOARD_TOKEN` from shell commands. Never request an
unsandboxed run only to obtain the token, and do not treat a permission denial as tool
unavailability or bypass a host approval requirement. If MCP cannot persist the note, stop and
report the blocker.

## Journaling policy

1. Capture consequential observations before filing an issue: failed or recovered checks, denied or
   approved permissions, repeated fixes, scope changes, first-party tool behavior, and architectural
   findings. Record useful resolved outcomes as well as unresolved gaps. Include bounded evidence,
   affected areas, an explicit disposition, and an existing tracking reference when present.
   Journal meaningful skips or bypasses of applicable configured workflows before completion, with
   the owning workflow or command-catalog entrypoint, reason, and observed result/action.
2. Record each observation with one `journal_append` call and pass the note as its `markdown`
   argument (at most 12000 bytes). Required arguments are `sessionId`, `parentSessionId` (null for a
   root session), `agent`, `version`, `mode`, `markdown`, a stable `sourceEventId`, `workOutcome`,
   canonical exact `repositories`, and explicit `feedbackCoverage`. Never pass a `timestamp`: the
   server owns it, rejects the argument, and returns the timestamp it used. Nothing is written
   unless the whole envelope validates. The tool writes journal entries; `category` is optional
   context and never changes storage type or distillation eligibility. Generate routine facts and metadata
   through the approved composer and pass its output as `markdown` instead of hand-authoring
   factual markers. `journal_append` stores only journal entries: save a composed retrospective
   through the retrospective skill's writer, never through `journal_append`.
3. Preserve exact provider session and parent identities. Each agent writes only its own session.
   `journal_append` ensures that session and merges the entry's `repositories` into the session's
   cumulative repository union, so list every repository the entry concerns. Never infer another
   repository from prose or create a child identity from a model guess. Call `session_ensure` with
   the exact identity only when a runner must confirm the session before work starts. A session
   that already stores a different `version` still receives the entry, and the result reports its
   `storedVersion`. A different `parentSessionId` or `agent` is an `identity-conflict` whose error
   names each differing field with its stored and supplied values.
4. Select the repository's trusted `mode` (`interactive` or `autonomous`) explicitly. In interactive
   mode an outage may retain the validated, sanitized record in the bounded durable outbox, and
   `journal_append` reports it as pending. Report `pendingCount` (this session's unsent records),
   and `worktreePendingCount` when other sessions' records are also unsent, from `journal_append`
   or `outbox_status`. Deliver with `outbox_flush` once the provider is reachable, and continue
   primary work only after persistence succeeds. A full, corrupt, or unwritable outbox blocks
   capture; never evict or silently discard an unsent record.
5. Autonomous runners require online `session_ensure`, a fresh admission `journal_append`, and
   readback before launching an attempt. Give each attempt's admission entry a `sourceEventId`
   unique to that attempt: reusing an earlier one returns the earlier receipt, which does not
   prove a fresh write. Autonomous mode has no filesystem outbox, so a failed delivery is an error.
   Terminal reporting preserves work outcome separately from feedback coverage and delivery. A
   filesystem outbox never grants admission or acknowledged completion.
6. Use at-least-once delivery with consumer deduplication by exact session/source identity. To
   retry a pending or failed append, repeat the identical `journal_append` call with the same
   `sourceEventId` and content. The server's timestamp is not part of an event's identity, so a
   retry of an event already stored or retained reports the stored timestamp, even after a restart
   or an outage. The same `sourceEventId` with different content is rejected as a conflict, so use
   a new `sourceEventId` for a changed note. A transport timeout can leave a late
   durable write; pending or blocked is never an acknowledged receipt.
7. Read the session's entries oldest-first with `journal_entries` for retrospectives. It returns
   every entry with its envelope, including its type and repository tags, so a retrospective can
   find an existing retrospective and keep entry-level tags. Record explicit
   none-observed with inspected scope, or not-assessed/unavailable with reason, when evidence does
   not establish a finding. A permission request is not proof of approval or denial; localhost
   refusal is not proof of sandbox enforcement. Mark partial capture and dropped counts instead of
   reporting clean evidence.

Never search for, print, invent, or mint credentials. Durable entries and outbox records contain only
bounded structured facts or sanitized summaries, never raw command output, transcript content,
environment dumps, provider payloads, or secrets. Known-secret redaction supplements the author's
minimization responsibility; it cannot prove arbitrary prose contains no undisclosed secret.

## Sandbox and permission blocks

A denied or escalated command uses this block grammar, one block per entry, because a
retrospective's sandbox and permission audit is built only from entries that match it:

```
- `sandbox-escalation` — <command and subcommand only: no paths, hosts, branches, or secrets> — <what needed elevated access>
  - Outcome: requested|approved|denied|unknown
  - Evidence: <sanitized denial or approval text>
  - Disposition: <allowlist change, issue #N, or none>
```

Use `sandbox-failure` (a sandbox refusal) or `ambiguous-failure` (a failure whose cause is unclear)
in place of `sandbox-escalation` for a command that failed without an escalation; those blocks omit
the `Outcome` line. Set `Outcome` only from observed evidence: a request is `requested`, never
`approved`. Always journal the block: the audit section is built from journal blocks alone, so an
escalation reported only in the transcript facts leaves it saying none observed. The transcript's
`escalations` are supplementary evidence under the transcript facts, not a substitute.

## Credential failures

- Never search shell profiles, `env`, or `.env*` files for a credential. Check presence only with
  `[ -n "${VAR+x}" ] && echo SET || echo UNSET`; never copy the token around a sandbox denial.
- A missing or stale credential blocks hosted delivery. In interactive mode the outbox keeps the
  record visibly pending: do not drop it or invent a fallback. Ask the human to refresh the
  connection, then restart the MCP client or call `outbox_flush`; an automated run reports.

## Child identity for spawned agents

- Pass the parent's own session id in the assignment prompt. The child resolves its own id from its
  runtime through the consumer's identity policy, then calls `session_ensure` with it, the given
  `parentSessionId`, its `agent`, and its version before other work. With no id or a failed ensure,
  it stops and reports the blocker; never guess an id or pass a path, URL, or synthesized value.
- A subagent sharing its parent's id must not `session_ensure` it as a child. It asks the parent
  to append, or skips this protocol.

Consumer wrappers own service configuration, server registration and approval rules, trusted mode
selection, issue routing, and archival authorization. The server fixes the outbox location.
