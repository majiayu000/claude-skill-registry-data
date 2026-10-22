---
name: reflect
description: "Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect."
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Use the current chat context or an explicitly scoped raw transcript, following [CODEX.md](../../CODEX.md). Do not scan private transcript directories or unrelated projects. When only a digest or truncated tool summaries are available, say which evidence is missing and pass that limitation to every reviewer. Never claim a full transcript audit from a summary.

## 2. Spawn three reviewers in parallel

Use three independent read-only reviewers, Judgment, Tooling, and Divergent. Launch through the selected host adapter within actual free slots and inherited parent model settings. Reviewers may consult connected read tools for referenced evidence. The read-only assignment is not an enforced tool sandbox.

| Lens | Runtime role | Prompt template |
|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings through the actual host-native task result channel.

## 3. Synthesize

Spawn a fresh read-only synthesizer with inherited settings under the runtime model policy. It spot-verifies available citations using actual connector tools. Pass `references/synthesizer.md` with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Keep Backlog as a reviewable local proposal. File tracker items only when the user explicitly authorizes that external action. Approval of selected skill edits does not imply approval of tracker posts.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the available `skill-creator` skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `skill-creator` and run its description-optimization loop.
- `new skill via skill-creator: <kebab-name>`: hand creation to `skill-creator`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog proposed locally or explicitly authorized and filed: `<issue title>`. State which, one line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
