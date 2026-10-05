---
name: session-to-meeting-log
description: Consolidate a Claude Code session JSONL log into a summary-only meeting record under meetings/ (decisions, rejected alternatives, hand-offs, open questions). Use when the user asks to turn a session into a meeting log, archive today's discussion, or extract a record from a .jsonl file; or when a long session is wrapping up before its context rolls. Not for in-flight notes during a subagent task (agent-impl-notes-log) and not for extracting recurring patterns across logs (methodology-pattern-extractor). Pass the invoker's `$CLAUDE_CODE_SESSION_ID` as the first argument; the fork has no conversation history, and its own-env fallback only works when that id resolves to exactly one transcript.
context: fork
agent: general-purpose
argument-hint: "[session-id-or-path] [topic]"
---

# Session → Meeting Log

## When to invoke

- The user says "turn this session into a meeting log" or "archive today's discussion".
- The session is approaching the context limit and needs a written artifact.
- The user mentions "extract notes from `~/.claude/projects/.../*.jsonl`".
- A long, multi-turn discussion is wrapping up before switching sessions.

## Inputs

### Arguments

- `$0` — `[session-id-or-path]`: the session id, or a full path to the `.jsonl`. Strongly recommended — see the fallback
  under "Locating the session file" when it is missing (the placeholder stays as literal `$0`).
- `$1` — `[topic]`: kebab-case topic for `meetings/{YYYY-MM-DD}_{topic}.md`. Optional — when
  no second argument is passed the placeholder stays as literal `$1`; derive the topic from
  the session's dominant subject instead.

### Locating the session file

- Default location: `~/.claude/projects/<encoded-project-path>/<sessionId>.jsonl` — don't
  compute `<encoded-project-path>` (the encoding rule is unofficial and unverified for every
  character); locate the file by id instead: `ls ~/.claude/projects/*/<sessionId>.jsonl`.
- `<sessionId>`: a UUID-like string, passed as the first argument. `context: fork` runs
  this skill in a subagent with no conversation history and no way to ask the user to
  confirm a guess — so the **invoker** should run `echo $CLAUDE_CODE_SESSION_ID`
  before dispatching (set automatically in Bash tool subprocesses) and pass the result as
  `[session-id-or-path]`.
- Missing argument fallback: read `$CLAUDE_CODE_SESSION_ID` in this fork's own Bash tool and
  accept it only if `ls ~/.claude/projects/*/<that-id>.jsonl` finds exactly one file. The docs
  don't say whether a fork sees the invoker's id or its own, and a fork's own transcript lives
  under `<sessionId>/subagents/`, so a wrong id fails this check instead of silently picking
  another session. If the variable is empty or the check doesn't find exactly one file, fail
  immediately and print the invoker instruction above rather than guessing from directory mtime.

### JSONL structure

One JSON event per line; common `type` fields:

| type | Content |
|---|---|
| `user` | User prompt, **or** a tool-execution result — a tool result is a `user` line whose `message.content[]` contains a `{type: "tool_result", …}` block and carries a top-level `toolUseResult` field. Filter these out before summarising; they are not human input. |
| `assistant` | Assistant response (incl. tool_use blocks) |
| `system`, `attachment`, `file-history-snapshot`, … | Harness metadata (queue state, mode, cost, permission state); skip anything that is not `user`/`assistant`. There is no top-level `tool_result` or `summary` type. |

Key fields: `timestamp`, `message.content`, `message.role`, `uuid`, `parentUuid`. Also present but not narrative content: `isSidechain`, `isMeta`, and `isCompactSummary` boolean flags (observed in local transcripts, not officially documented) — a line with any of these set to `true` is harness-internal bookkeeping or an auto-generated compaction summary, not a primary user/assistant turn; filter it out the same way as the non-`user`/`assistant` types above (use it as background context at most, never as a source for Decisions). Sub-agent transcripts live in a separate file, `<sessionId>/subagents/agent-*.jsonl`, not inline in the main log — combined with these flags, "no subagent noise" becomes a mechanical filter rather than a judgment call.

## Output

Write to `meetings/{YYYY-MM-DD}_{topic}.md`:

```markdown
# {YYYY-MM-DD} — {Topic}

Session id: `<sessionId>`
Mode: <e.g. AI Collaboration Mode (Leader/Developer)>

## Goal
<one-line statement of the session's goal>

## Timeline (milestones only)
- <milestone 1, e.g. "§How.3 round 1 accepted">
- <milestone 2, e.g. "Code Reviewer dispatch produced 7 BLOCKERs">

## Decisions
1. <decision 1>
2. <decision 2>

## Rejected alternatives
- <rejected option> — reason: <reason>

## Hand-offs
- <sub-agent dispatched / next session expected to ...>

## Open questions
- <open question 1>

## Next session
<one-line statement of the next session's intent>
```

### Extraction rules

1. **No verbatim copying.** Summarise decisions and their reasons; drop exploratory chatter, rhetoric, and repeated clarifications.
2. **Decisions**: only items the user explicitly confirmed or the Leader explicitly ACCEPTed.
3. **Rejected alternatives**: options that were discussed and turned down; include a one-line concrete reason.
4. **Hand-offs**: list sub-agents dispatched in this session, or explicitly state what the next session should pick up.
5. **Open questions**: items that didn't converge this session and need a decision next time.
6. **Don't record tool-call details** (e.g. "Read foo.md / Edit bar.md"); only **why** something was read / changed and the **result**.
7. **Timeline keeps only milestones**: e.g. "§How.3 round 1 accepted", "Code Reviewer dispatch produced 7 BLOCKERs".
8. **Never leak secrets**: if the JSONL contains tokens / PEM / API keys, **delete them, never copy** into the meeting log (even if the file itself is private).

## Verification checklist

- Filename format `YYYY-MM-DD_<topic-kebab>.md`, date in local timezone.
- Contains the seven main sections: Goal / Timeline / Decisions / Rejected alternatives / Hand-offs / Open questions / Next session.
- Entries are summaries, never verbatim copies.
- No secrets / tokens / PII.
- If the session spans multiple days, add a phase tag to the topic (e.g. `kickoff` / `spec-phase` / `cr-round1`).

## Deviation considerations

- **Session is too short (< 5 meaningful turns)**: a standalone log isn't necessarily warranted; append as an addendum to the previous log.
- **Session was highly divergent**: split into multiple topic-specific logs for the same day, named `{date}_{topic-a}.md` / `{date}_{topic-b}.md`.
- **Sub-agent internal exchanges**: usually not included in the meeting log; only record the main agent's dispatch + summary of the returned result. They live in `<sessionId>/subagents/agent-*.jsonl`, not the main session file, so this needs no filtering step of its own.

## Related skills

- `methodology-pattern-extractor`: meeting logs produced here are the input for methodology pattern extraction.
- `backlog-routing-by-topic`: open questions that can be classified can also be routed to the matching file's §Backlog.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
