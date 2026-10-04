---
name: "handoff"
description: "Hand work across a session boundary in either direction: pause cleanly with a resume note a cold-start agent can pick up, or take over work someone else left in flight. Use for pause safely, I need to go offline, before context compacts, take over this, resume this conversation, or pick up where X left off."
disable-model-invocation: true
argument-hint: "What will the next session focus on? (or leave blank)"
---

# Handoff

Two directions across one boundary. Pick by which side you are on.

- **Pausing.** You have work in flight and are about to stop. Go to [Pause](#pause).
- **Picking up.** Someone else's work is in flight and you are taking it. Go to [Pick up](#pick-up).

The two halves are one skill because they are one contract: what Pause writes
down is exactly what Pick up expects to read.

---

## Pause

**You own a clean stop. Leave a checkpoint a cold-start agent can resume
from.** For "pause safely", "I need to go offline", "restart", "board my
flight", and when context is about to compact.

**This is explicit only.** On "keep going", "going to bed, keep going", or
"don't stop", do not pause. Those mean continue.

1. **Stop at a safe boundary.** Finish the current atomic step or back out of it. Never stop mid-edit in a known-broken state. Start nothing new, and cancel any nested subagents.
2. **Do not cross an irreversible line to pause.** No PR and no push unless one was already out.
3. **Make the work durable.** Commit uncommitted edits as one clear `wip:` commit on the current branch so nothing is lost. If the tree is broken, say so in the commit body in one line.
4. **Write the resume note off-context.** Intent, what you were doing, progress and what is verified, current state, next steps, key files, gotchas. Write it to a file (`/tmp/<slug>-resume.md`), because an in-context plan does not survive summarization. If a **show-me-your-work** trail exists, point at it instead of duplicating it.
5. **Name the skills the next session should call**, so the pickup does not have to rediscover the routing.

Do not duplicate what other artifacts already hold (specs, plans, ADRs, issues,
commits, diffs). Reference them by path or URL. **Redact secrets**: API keys,
passwords, personal data. If the user passed an argument, treat it as what the
next session will focus on and tailor the note to it.

**Reply:** where you are in the loop, what is on disk versus still in your head
(paths, not diff dumps), the commits you made and whether the tree is clean, and
the first action on resume. This is a pause, not a final report.

### Handing to a fresh agent instead of a file

When the work should continue immediately rather than wait for a human, launch
a background agent seeded with the note rather than saving it:

```bash
claude --bg --name "<descriptive name>" "<resume note>"
```

Always pass a descriptive `--name`; it is what shows in the job list, session
picker, and terminal title. It starts in the current working directory and
returns immediately. Redaction matters more here, since the note becomes the
agent's prompt.

---

## Pick up

**You own the resume point. Read the prior trail, don't redo it.** For "take
over this", "resume this conversation", "continue from `<path>`", "you're
taking over", or a pushed branch you are meant to continue.

A pickup is inheritance. The prior agent already paid the cost of reading the
code, running the repros, and making the design choices. Redoing that loses the
independent check and burns context. **Resist the urge to re-derive. Read.**

1. **Locate the prior trail.** A resume note from Pause, a transcript at `~/.claude/projects/<slug>/<uuid>.jsonl` (slug is the workspace path with every "/" turned into "-", leading dash included), or a pushed branch. Do not glob across `~/.claude/projects/*/`; that crosses workspace boundaries and reads private chats from unrelated projects. Read the last messages first, then scan back for the decision points. Parse a long transcript in a subagent and keep only the reduced timeline in the main thread, per the **guard-the-context-window** principle (`principles/guard-the-context-window.md`).
2. **Reconstruct operational state.** Branch and worktree, what already landed (`git log`, `git diff` against the base), open todos, decisions made. The prior trail is authoritative input.
3. **Diff done against pending.** Name the resume point. Do not re-run the prior repro or redo completed work. A "let me verify from scratch" pass is the tell that you are treating an authoritative trail as untrustworthy.
4. **Route the remaining work** and pick the verdict: continue execution, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run. This skill ends here; the routed work owns the rest.
5. **Verify the inherited claims** against the original goal on the real artifact, per the **prove-it-works** principle (`principles/prove-it-works.md`). A passing prior self-report is not proof.

**Reply:** where the prior agent stopped, what you inherited versus redid
(ideally nothing redone), the resume point, and the outcome.
