---
name: meditation
description: Aang meditating to see clearly. Use for reflect, /reflect, "reflect on this session", "what did we learn", or "turn this into skill edits". Dispatches three parallel reviewers over the active Claude Code or Codex transcript, surfaces durable learnings, and routes each to a concrete edit on an existing skill, held for the user's approval.
---

# Aang's meditation

Aang does not find answers by charging ahead. He sits still, quiets the noise, and lets the truth of what happened surface. Then he opens his chakras one by one and lets go of what was blocking him. Meditation over a session is the same. Look back at the whole conversation with three sets of eyes, keep only the lessons that will still be true in six months, and turn each one into a change to a skill so the next agent does not have to learn it again.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

Mine the current conversation for durable learnings, then route them into skill edits.

Use it when the user says "reflect", "/reflect", or asks what the session taught. Skip it when the conversation is trivial, off-topic, or already covered by a skill the session followed correctly. A one-off is not a learning.

## 1. Locate the active transcript

Before you fan out, find this conversation's transcript. Stay inside this workspace. Never glob across every project's transcripts, because that reads private chats from unrelated projects.

- **Claude Code.** The per-project directory is `~/.claude/projects/<encoded-cwd>/`, where `<encoded-cwd>` is the workspace path with every character that is not a letter or digit turned into `-` (`/Users/you/proj` becomes `-Users-you-proj`).
- **Codex.** Rollouts for every project share `~/.codex/sessions/` (dated subfolders) and `~/.codex/archived_sessions/`. The finder keeps only rollouts whose `session_meta` cwd is the workspace.

Run the finder bundled with this skill, with the transcripts directory and a fragment of the conversation's opening user prompt.

```bash
node <this skill's directory>/scripts/find-transcript.mjs ~/.claude/projects/<encoded-cwd> "<opening prompt fragment>"
node <this skill's directory>/scripts/find-transcript.mjs ~/.codex/sessions "<opening prompt fragment>"
```

An optional third argument names the workspace for the Codex cwd check. It defaults to the current directory. The finder walks the layouts (flat `<id>.jsonl`, nested `<id>/<id>.jsonl`, subagent `<id>/subagents/<child>.jsonl`, and Codex's dated `rollout-*.jsonl`), newest first. It prints the first path whose opening typed prompt carries the fragment.

Do not reimplement the scan by hand. The first line of a transcript is session metadata, not a message. A Claude Code session that starts with `/clear` or a `!` shell command records that command's wrapper and output as `user` records before the prompt. A Codex rollout injects `AGENTS.md` instructions and environment context as `user` messages before the prompt. Files run to several megabytes, so the finder streams each candidate and stops at its first typed prompt.

If the finder exits 1, write a tight digest of the session and pass that instead. The digest lists, one line each in turn order, the user's prompts and corrections, the tool calls and their results, and the files touched. It states no diagnosis, verdict, or cause. The reviewers judge the session, not your conclusions about it.

## 2. Dispatch three reviewers in parallel

One message, three Agent calls, each with `run_in_background: true`. Reviewers need MCP access to look up the tickets, chat threads, and observability traces the transcript references, so never dispatch them as Toph, whose tool list has no MCP access. Each brief forbids file writes. You apply the edits.

| Lens | Character | Model from the avatar-setup sheet | Brief |
|------|-----------|-----------------------------------|-------|
| Judgment | `team-avatar:iroh` | the `iroh` line | [references/judgment-reviewer.md](references/judgment-reviewer.md) |
| Tooling | `team-avatar:sokka` | the `sokka` line | [references/tooling-reviewer.md](references/tooling-reviewer.md) |
| Divergent | `team-avatar:zuko` | the `zuko` line | [references/divergent-reviewer.md](references/divergent-reviewer.md) |

The sheet lives at `${CLAUDE_CONFIG_DIR:-~/.claude}/team-avatar-models.md` on Claude Code and `${CODEX_HOME:-~/.codex}/team-avatar-models.md` on Codex. A missing sheet or line means `opus` for all three. A value with `@<level>` sets the Agent tool's `effort` parameter on Claude Code and `spawn_agent`'s `reasoning_effort` on Codex. If the Agent tool rejects a model, use the default and say so. Pick each dispatch's effort for the job, as the dispatch rules in `avatar-mode` describe.

Pass each brief verbatim, substituting the transcript path or the digest where marked. Add nothing beside a transcript path, not even a focus note for a long transcript. Reviewers return findings in the Agent response body.

When you run as a subagent yourself, you cannot dispatch. Apply the three lenses yourself, one after another, then synthesize. Say so in the summary.

## 3. Synthesize

One more Agent call, `subagent_type: "team-avatar:iroh"`, with Iroh's model from the sheet. It spot-verifies citations through MCP, so it needs full tool access. Pass [references/synthesizer.md](references/synthesizer.md) verbatim, with each reviewer's full output inlined where marked. It returns an Accepted, Rejected, and Backlog list.

## 4. Structural enforcement check

Move to Backlog any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably than prose. This is the Encode Lessons in Structure principle (Fire in `four-elements`).

## 5. Apply

Present the synthesizer's full Accepted, Rejected, and Backlog output. Wait for explicit approval before you apply any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent. Never auto-apply.

File each Backlog item to the team's devex or backlog tracker without waiting. Only the Accepted list waits for approval.

Follow each approved row's Routing exactly.

- **Trivial existing-skill edit** (a one-line bullet, a tightened sentence, a corrected stale fact). Make it yourself.
- **Substantive existing-skill edit** (a new section, a new pattern table, more than about 10 lines). Hand it to `new-scroll` and run its draft, test, and iterate loop.
- **`tune description: <skill path>`** (the skill exists but did not trigger when it should have). Hand it to `new-scroll` and run its description loop.
- **`new skill via new-scroll: <kebab-name>`.** Hand creation to `new-scroll`. Do not invent the shape ad hoc.

If the repo ships a skill validator (Team Avatar's is `node scripts/validate-team-avatar.mjs` from the repo root), run it on every touched skill before you call the work done.

## 6. Summarize for the user

A short list, no preamble.

- **Edits applied.** `<skill path>`, then what changed, one line each.
- **New skills created.** `<skill path>`, one line each. This is rare.
- **Backlog filed.** `<issue title>` (`<tags>`), one line each.
- **Dropped.** One line per rejected finding, with the synthesizer's reason.
