---
name: spirit-world
description: Aang crossing into the spirit world to recover what was lost. Use for recall, /recall, "recall my work on X", "what have I been working on", "where did I leave off", before starting or resuming work, and before telling the user that something was never recorded. Rebuilds recent working context from your own Claude Code and Codex chat history, live git and PR state, and the shared record (user reports, prior fixes, reverts, incidents), then hands back a tight current-state brief.
---

# Aang's journey to the spirit world

When something is lost in the physical world, Aang meditates, crosses over, and finds it where memory still lives. The spirits remember what the living forgot. Your past chats are that place. Cross over before you start or resume work, bring back only what the current task needs, and return quickly. A spirit-world trip that wanders loses the body it left behind.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

Keep it tight and on-topic. Read only what the in-scope threads need, then stop.

## Two records

Your context lives in two records. Your own chat history holds what you did and decided. The shared record holds everything that happened around the same code under other names. That includes the symptoms users keep reporting, the fixes that shipped and got reverted, and the errors still firing in production. The shared record is what `past-lives` searches, across source control, the issue tracker, team chat, long-form docs, and error tracking. A feature with a long bug tail keeps most of its story there, so never rebuild it from transcripts alone.

## Where the transcripts live

Check the real layout with `ls` before you read. The layouts below were confirmed on a real machine.

**Claude Code.** Transcripts live at `~/.claude/projects/<encoded-cwd>/` (or under `$CLAUDE_CONFIG_DIR/projects/` when it is set). `<encoded-cwd>` is the workspace path with every character that is not a letter or digit turned into `-`, so `/Users/you/proj` becomes `-Users-you-proj` and `/Users/you/My App` becomes `-Users-you-My-App`. Each directory holds three shapes.

- `<uuid>.jsonl`, one chat. Every line is one record.
- `<uuid>/subagents/<child>.jsonl`, the subagent chats that session dispatched.
- `<uuid>/tool-results/`, large tool outputs saved beside the chat.

**Codex.** Sessions are not split by project. They live at `~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl` (or under `$CODEX_HOME/sessions/`), with older ones moved flat into `~/.codex/archived_sessions/`. The first line of each rollout is a `session_meta` record whose `payload.cwd` names the workspace. Filter on it before you read anything else.

```bash
for f in $(ls -t ~/.codex/sessions/*/*/*/rollout-*.jsonl); do
  head -n 1 "$f" | grep -q "\"cwd\":\"$PWD\"" && echo "$f"
done
```

In a rollout, a typed prompt is a `response_item` record whose `payload.role` is `user`. Skip the injected ones that open with `# AGENTS.md instructions`, `<environment_context>`, or `<codex_internal_context`. A rollout whose `session_meta` carries `parent_thread_id` or a `source.subagent` field is a subagent chat.

## Steps

1. **Classify, then route.** Resuming one specific prior chat is `break-camp`, not this. Turning habits into a durable skill is `invention-workshop`. A human-readable summary of your work for someone else is `war-journal`. This skill loads working context across recent chats before you act. If the user already gave you a full state capsule (paths, branch, the change), use it and skip the mining.
2. **Lock the scope before you search.** Pin the window ("recent" is a real range, default the last 7 days), the topic if named, and the workspace (default the active one). Never read another project's transcripts without being asked. On Codex that means the `cwd` filter above, every time. State the scope back. Never quietly turn "all" into "recent N".
3. **Fan out across your chat history.** Dispatch parallel `team-avatar:momo` agents, each taking a slice of the corpus, with Momo's model from the `momo` line of the avatar-setup sheet and `run_in_background: true`. Tell each one to:
   - order candidates by real modification time (`ls -t`), never by UUID name
   - grep the topic first, then read only the matching chats and only their relevant regions
   - skip the current chat and obvious noise (subagent, eval, and test chats)
   - write nothing

   Each returns the same schema, one block per chat. The block holds the topic, the user's goal, decisions, open threads, struggles and corrections, and artifacts (PRs, tickets, branches), each citing the chat UUID. For one or two chats, skip the fan-out and search directly. The raw transcripts stay in the subagents. The main thread gets only their findings. Pick each dispatch's effort for the job, as the dispatch rules in `avatar-mode` describe. When you run as a subagent yourself, do the slices one after another.
4. **Sweep the shared record** whenever the topic names a feature, file, subsystem, area, or bug. This is the default, not a judgment call, and "my work on X" does not exempt it. Hand it to the source investigators in `past-lives`, but steer their question from "why was this built this way" to "what is the current state, what has been tried and did not hold, and what are users still reporting". Reuse its per-source playbooks and run the investigators in parallel with the chat mining. Inherit its posture. One investigator per source, null results are findings, and an unavailable MCP is skipped and named.

   Also sweep every location the project's standing rules name for queued or recorded items (a memory directory, a decisions log, a `.planning/` tree, a pointer in `CLAUDE.md` or `AGENTS.md`) before you report anything as never recorded. A search that skips a place the project's rules name is not exhausted.

   Skip this step only for pure activity recall with no named target ("what did I do this week"). There your own history and live state are the entire answer.
5. **Keep human rulings exact.** For claims about what a person decided, apply [Claims about human decisions](../past-lives/references/epistemics.md#claims-about-human-decisions). Keep the attributable original wording and its source when exact scope matters, separate agent interpretations, and treat copied summaries as one evidence chain.
6. **Verify against live state.** Take the PRs, branches, and tickets the mining and the sweep surfaced and check each with `git` and `gh`. When the answer hinges on what an agent actually did (the tools it ran, the files it read, the errors it hit), read the full transcript, not a trimmed copy.
7. **Write the brief** to the contract below. Group by thread. Stay on the named topic.

## Output contract

Lead with the capsule, then thread status, then problems, then the next move. Deeper detail goes below or gets cut.

- **Capsule.** At most 5 bullets. What this work is and where it stands overall.
- **Threads.** One line each, prefixed with exactly one status tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, or `[planned, not started]`. A thread with no tag is not done, so tag it.
- **Problems.** At most 5, the recurring ones. Include the symptoms users keep reporting and any fix that shipped and was reverted, so the next attempt starts where the last one failed.
- **Next move.** The single most useful next action, concrete.

An adjacent feature or ticket stays out unless it blocks this one. When the capsule and thread lines outgrow a screen, cut detail before you cut threads. Write the brief by `tea-time`. Cite chat findings by UUID and shared-record findings by their source (PR number, ticket ID, chat permalink, error-tracker issue). Strip private context before any public output.

**Reply.** The brief, to the contract above.
