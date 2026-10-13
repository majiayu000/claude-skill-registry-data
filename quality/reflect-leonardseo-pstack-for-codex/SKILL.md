---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface
  learnings, and route each to a concrete edit on an existing skill. Use when the
  user says reflect.
---

Read [Codex runtime contract](../../CODEX-RUNTIME.md) before applying this workflow. It governs tools, delegation, models, authorization and fallbacks.


# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Use only the current task transcript if the host exposes one. Otherwise construct a factual session digest with evidence pointers and label the missing transcript audit.

Only use an actual host-provided transcript path, or the factual digest above. Do not assume a transcript layout.

## 2. Spawn three reviewers in parallel

One message, three `spawn_agent` when available calls, the appropriate bundled role prompt, with `model` set as below, agent mode (an explicit role-scope instruction). Reviewers need MCP access for context lookups (tickets, chat threads, observability traces referenced in the exposed transcript or recorded receipts; missing transcript coverage must be labeled). Read-only is a role instruction; connector access follows host policy.

Use the native delegation and model rules in CODEX-RUNTIME.md. Default every role to inherit-parent.

| Lens | Role line | Default `model` | Prompt template |
|---|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `inherit-parent` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `inherit-parent` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `inherit-parent` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Collect the reviewers’ terminal completion reports through native messages or result tools. The spawn response contains only an identifier.

## 3. Synthesize

One `spawn_agent` when available call, the appropriate bundled role prompt, with `model` from the `reflect judgment, divergent, synthesizer` line (default `inherit-parent`), agent mode (an explicit role-scope instruction). The synthesizer's quality check includes spot-verifying citations, which can require MCP access. Read-only is a role instruction; connector access follows host policy. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

File each Backlog item to your team's devex or backlog tracker without waiting. Only the Accepted list waits for approval.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): follow the Skill authoring section of CODEX-RUNTIME.md and run representative draft / test / iterate checks.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to the Skill authoring section of CODEX-RUNTIME.md and inspect the trigger description against representative prompts and use a description eval harness only if available.
- `new skill via create-skill: <kebab-name>`: follow the Skill authoring section of CODEX-RUNTIME.md. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
