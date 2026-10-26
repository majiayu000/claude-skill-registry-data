---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
disable-model-invocation: true
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Before fanning out, find this conversation's transcript among this workspace's transcripts, per [harnesses.md](../poteto-mode/references/harnesses.md) (Transcripts). Do not glob across every project's transcripts (`~/.claude/projects/*/`, or Codex sessions whose `cwd` is another workspace). That crosses workspace boundaries and reads private chats from unrelated projects.

```bash
# Claude Code
ls -t ~/.claude/projects/<slug>/*.jsonl ~/.claude/projects/<slug>/*/subagents/*.jsonl 2>/dev/null | head -10
# Codex: recent rollouts whose line-1 session_meta cwd is this workspace
for f in $(ls -t ~/.codex/sessions/*/*/*/rollout-*.jsonl 2>/dev/null | head -50); do head -1 "$f" | grep -qF "\"cwd\":\"$PWD\"" && echo "$f"; done | head -10
```

That covers the Claude Code session (`<id>.jsonl`) and subagent (`<id>/subagents/<child>.jsonl`) layouts and the Codex rollout layout. For each candidate, read its first user turns, using the record shape harnesses.md gives. Take the file whose opening user turn contains the conversation's opening user prompt. If none matches, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

One message, three subagent calls, each a read-only agent that keeps MCP access, per [harnesses.md](../poteto-mode/references/harnesses.md) (Subagents). That is `general-purpose` in Claude Code, and `pstack-reader` (which keeps MCP) or `default` in Codex. Reviewers need MCP access to look up the tickets, chat threads, and observability traces the transcript references, and the search-only agent (Claude Code `Explore`) strips MCPs.

Each reviewer and the synthesizer name a role. Resolve it from `~/.config/pstack/models.md` and apply it per [harnesses.md](../poteto-mode/references/harnesses.md) (Models), which holds the defaults. A reviewer on a cross-harness seat gets the other CLI's MCP servers, not yours. List them (`codex mcp list` from Claude Code, `claude mcp list` from Codex) and name them in its brief. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill.

| Lens | Role line | Prompt template |
|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the subagent's response body, or in the output file of a cross-harness seat.

## 3. Synthesize

One subagent call on the same MCP-keeping agent, `model` from the `reflect judgment, divergent, synthesizer` role. It spot-verifies citations through MCP, and the search-only agent strips MCPs. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

File each Backlog item to your team's devex or backlog tracker without waiting. Only the Accepted list waits for approval.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the `skill-creator` skill, per [harnesses.md](../poteto-mode/references/harnesses.md) (Skills), and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `skill-creator` and run its description-optimization loop.
- `new skill via skill-creator: <kebab-name>`: hand creation to `skill-creator`, and place the new skill where both harnesses discover it, per [harnesses.md](../poteto-mode/references/harnesses.md) (Skills). Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
