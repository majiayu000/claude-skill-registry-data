---
name: reflect
description: "Use for \"reflect\", after a complex task lands cleanly, after the human corrected your approach mid-task, or when a workflow emerged that isn't written down anywhere. Reviews the session from three angles, sorts what it finds into accepted, rejected, and backlog, and routes each accepted lesson to a concrete edit on an existing skill. Waits for approval before editing any skill."
disable-model-invocation: true
---

# Reflect

Mine the session for lessons that will still be true in six months, then put each one where it'll change behavior. Usually that's an edit to an existing skill. Sometimes a lint rule or a script. Never just a note.

## When

- The human said reflect.
- A complex task just landed cleanly and the recipe is worth keeping.
- You hit dead ends, found the path, and the path generalizes.
- The human corrected your approach mid-task.
- A non-trivial workflow emerged that isn't captured anywhere.

Skip when the session was trivial, off-topic, or already covered by a skill you followed correctly. A one-off is not a lesson.

## Step 1. Find the session record

Use whatever your harness gives you for the current conversation: a transcript file, a session log, a history export. Don't read other projects' sessions. If nothing is available, write a tight digest of the session yourself and pass that instead.

## Step 2. Three reviewers, in parallel

Spawn all three at once. They need tool access to look up context the session referenced, tickets, threads, traces, and they must not write anything. Each gets its template from `references/` with the transcript path or digest filled in.

- **Judgment.** `references/judgment-reviewer.md`. The durable principle behind a specific incident.
- **Tooling.** `references/tooling-reviewer.md`. The concrete command, flag, path, or quirk future agents would otherwise rediscover. Also flags every moment the human hand-fed context the agent could have fetched itself.
- **Divergent.** `references/divergent-reviewer.md`. The contrarian lens. Second-order effects, what didn't happen but should have, the lesson beneath the obvious one.

Use different models for the three if you can.

## Step 3. Synthesize

One subagent with `references/synthesizer.md` and all three reviewers' output inlined. It applies the durability and specificity tests, checks whether the target skill already covers each finding, and returns accepted, rejected, and backlog.

## Step 4. Structural check

Read the accepted list once more. Anything a lint rule, a hook, a script, or a runtime check would enforce more reliably than prose moves to backlog. Text is the last resort.

## Step 5. Apply, with approval

Show the human the full accepted, rejected, and backlog output. Wait. They pick which accepted rows to apply and can redirect any routing. A skill change affects every future session, so never auto-apply.

Backlog items go to the project's tracker or the decisions file without approval. They aren't skill edits.

For each approved row, follow its routing:

- Small edit to an existing skill, a line or a tightened sentence. Do it directly.
- Substantive edit, a new section or more than about ten lines. Draft it, then check the skill still reads as one piece.
- Tune description. The skill exists but didn't fire when it should have. Rewrite its description line so it triggers next time.
- New skill. Only when no existing skill is a real home and the pattern recurs. Write it in the stack's voice and shape.

## Step 6. Summarize

Short list, no preamble. Edits applied, with path and one line each. New skills, rare. Backlog filed, one line each. Dropped, one line per rejection with the reason.
