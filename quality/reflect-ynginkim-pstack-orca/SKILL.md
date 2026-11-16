---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
disable-model-invocation: true
---

# Reflect

> Names in backticks, such as `spawn-worker` and `find-sessions`, are capabilities, not commands. Read `../resolve-capability/SKILL.md` before the first step. It says how each one is done here and whether a worker on another agent can be started.

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Before fanning out, find this conversation's transcript with `find-sessions`. Look only in your own agent's store, limited to this workspace. Do not glob across every project folder. That crosses workspace boundaries and reads private chats from unrelated projects.

List this workspace's sessions, newest first, and read each candidate's opening user prompt. Take the session whose opening prompt matches the conversation's. If none matches, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

Start all three at once. Reviewers need MCP access to look up the tickets, chat threads, and observability traces the transcript references. Pick a seat type that keeps your MCP tools, because some read-only types drop them (`spawn-subagent` says where the types are listed). Each brief says not to edit files, and you check `git status` afterward.

Read `~/.agents/skills/select-model/SKILL.md` and choose each seat's model and how to start it from it. Start every seat as the Subagents section of `../poteto-mode/SKILL.md` says, which also covers a missing `select-model` and keeps a seat that needs your MCP servers on your own harness. The table says what each seat needs, not which model fills it. Pick each subagent's reasoning level and speed for the job, per that section.

| Seat | Kind | Needs | Prompt template |
|---|---|---|---|
| Judgment reviewer | judgment | read-only, MCP lookups | `references/judgment-reviewer.md` |
| Tooling reviewer | code or read | read-only, MCP lookups | `references/tooling-reviewer.md` |
| Divergent reviewer | judgment | read-only, MCP lookups | `references/divergent-reviewer.md` |
| Synthesizer | judgment | MCP, for the citation spot-checks | `references/synthesizer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked, and add the absolute path of `../resolve-capability/SKILL.md` to each brief, which the reviewer reads for `locate`. Collect each reviewer's findings from its final result.

## 3. Synthesize

Start the Synthesizer seat once the three reviewers have returned, the same way and with MCP access, because it spot-verifies citations through MCP. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

File each Backlog item to your team's devex or backlog tracker without waiting. Only the Accepted list waits for approval.

Never edit a skill where an installer keeps it, such as a plugin cache or a skills folder the next install overwrites. Before approval, show where each edit will land: the skill's source checkout when you can find one, otherwise a copy of the skill folder in a project or user skill folder that `locate` lists. After approval, edit there. Never open a PR or push.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to `author-skill` and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `author-skill` and run its description-optimization loop.
- `new skill: <kebab-name>`: hand creation to `author-skill`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
