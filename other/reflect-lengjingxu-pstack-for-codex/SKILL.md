---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "$reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Before fanning out, find this conversation's transcript under `$CODEX_HOME/sessions/`, newest first by modification time. Do not read sessions outside this workspace. That crosses workspace boundaries and reads private chats from unrelated projects.

```bash
ls -t "$CODEX_HOME"/sessions/*/*/*/rollout-*.jsonl 2>/dev/null | head -10
```

Each file holds one session. For each candidate, read the first JSONL line and take the file whose `session_meta` payload names this workspace and whose opening user message matches this conversation. If none matches, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

One message, three spawn_agent calls, each with a write scope. Reviewers need MCP access to look up the tickets, chat threads, and observability traces the transcript references, and a read-only scope strips MCP access.

Each reviewer and the synthesizer name a role line in the `~/.codex/pstack-models.md` file and a default. Set `model` to that line's value, or to the default if the rule or the line is missing. Leave `model` unset when the value is `auto` or `inherit-parent`. If spawn_agent rejects a slug, use the default and say so. If it rejects the default, use the closest valid slug of the same family from its error message. Pick each subagent's reasoning effort for the job, per the Subagents section of the **poteto-mode** skill.

| Lens | Role line | Default `model` | Prompt template |
|---|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `gpt-6-astra` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `gpt-6.1-sol` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `gpt-6-astra` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the the subagent's returned message.

## 3. Synthesize

One spawn_agent call with `model` from the `reflect judgment, divergent, synthesizer` line (default `gpt-6-astra`) and a write scope. It spot-verifies citations through MCP, and a read-only scope strips MCP access. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

File each Backlog item to your team's devex or backlog tracker without waiting. Only the Accepted list waits for approval.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the `skill-creator` skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `skill-creator` and run its description-optimization loop.
- `new skill via skill-creator: <kebab-name>`: hand creation to `skill-creator`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
