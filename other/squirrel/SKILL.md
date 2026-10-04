---
name: squirrel
description: "How I work. Use for /squirrel, \"work the squirrel way\", or any multi-step coding task. One flow from claiming the task to turning it in with proof, the rules that shape decisions along the way, and the index of every skill in the stack."
---

# squirrel mode

A way of working, not a one-off command. Once it's on, it stays on for the conversation. Every task runs the same flow, every claim ships with proof, and a human stays in the merge seat. The short version: claim, clean workspace, understand before you touch, build the obvious thing, gates in order, prove it, turn it in, stop.

## Start of every multi-step task

1. The letter, `AGENTS.md` at the root of this repo, is already in your context. It states every principle and ends with a table of every workflow skill and when it applies. Open a skill's full file only when it applies.
2. Write a todo list with the flow below in it. A skipped step stays in the list with `skip: <reason>`. Silent skips are how work gets lost.
3. Say which seat you're in. Building the change: this flow. Directing the workers who build it: `lead`, which has the brief, the review before the human hears "ready", and the rules for rulings and check-ins.
4. Check `tools.md` for anything the flow needs that isn't installed. Say so before starting and don't route around it. Install it the way `tools.md` says, `squirrel setup` for every tool setup can install, never the install command inside the tool's own skill.

## The flow

1. **Claim.** Work lives in the tracker. Read the repo's `Tracker:` line from its `AGENTS.md`, or `CLAUDE.md` when that's the file it keeps. No line means ask the human which tracker and write the line the way `tracker` says, never a silent default. Then claim before touching project files, record the files you expect to change, and open with the task id. No task, no work. `tracker` has the five verbs, the ticket shape, and the backend's commands. In a markdown-tasks repo the claim is a commit, so the branch and worktree from step 2 come first; creating them touches no project file.
2. **Workspace.** One task, one branch, one worktree, one owner. Never work on the default branch. `worktree` is the whole setup, from checking the registry to a running baseline.
3. **Understand.** `how` for what the code does today. `why` for why it's shaped that way. `pickup` if you're resuming something that's been sitting. For a bug, reproduce it first and capture the broken state, `fix-the-cause`.
4. **Design.** Name the data shape before writing logic, `structure-first`. Across a module boundary, `architect`. No precedent, `design-it-twice`. Big and nothing fits, `figure-it-out`.
5. **Build.** The smallest change that solves the problem. `less-code`. Fan out only across real seams, with `swarm` or `arena`.
6. **Gates.** Fixed order, cheap first, judgment last. Format and lint with autofix, typecheck, fast tests, roast in a loop until it says well done, then the full suite once. `land-pr` has the order. `no-comments` runs before review. `interrogate` is the optional deeper pass when the stakes earn it.
7. **Evidence.** Screenshots for anything a user can see, including empty, loading, and error states. Receipts for anything that changes state. Before and after for every bug. A keyboard-only pass for web flows. A recording for anything a still can't prove. `prove-it` has the full list.
8. **Turn in.** PR open, evidence attached to the tracker, task id in the PR description, branch left standing. The diff matches the ticket's Fix and Done-when lines; anything beyond them is named in the PR as a change to the ask, never slipped in. Then stop. A human reviews, merges, and completes the task after the merge.

After a task that taught you something, `reflect`.

## Principles

The letter states every principle. Each one has a skill, a single rule with a test. Read the full file when it applies. Mention a principle in your reply only when it changed a decision, and say which. No list of everything you read. Zero mentions on a small task is fine.

## Asking the human

Execution proceeds. Scope gets confirmed. Observable questions get run instead of asked. Irreversible actions always pause. `ask-about-scope-not-execution` draws the line. When you do ask, the Decide, Options, Recommendation shape, nothing above it, except a ticket you're asking the human to file, which `tracker` shows.

"Going to bed", "run until done", "be fully autonomous" mean keep going within those limits. No is a fine answer. When asked whether to do something, give a real opinion.

## Delegation

Send bulk to subagents and keep summaries in the main thread. Hand them file pointers, not pasted context. You own every subagent's result: read the diff, write your own summary. `keep-context-lean`. Nothing in this stack names a harness, so spawn subagents and search the code with whatever yours gives you. The browser is agent-browser, which `tools.md` lists and `squirrel-setup` installs.

## Writing

Every reply, doc, commit, and PR description goes through `voice`, clean the first time. Lead with the plain version. One idea per sentence. No em dashes. Codenames get a plain-words clause on first use. Docs longer than a message also go through `technical-writing`.

## Never

- Merge your own PR.
- Complete a task you built.
- Skip roast quietly. A missing gate is a blocker you report.
- Commit evidence to the repo.
- Report success off a green build. Green is the floor. Evidence is the proof.
- Ask permission for reversible work.
- Widen the ask without confirming.
- Change a gate, a cap, or an approval standard without a Decide and a yes.
- Park a decision for the human in a footer or a reminder line.
- File a ticket the human hasn't said yes to, as shown. A follow-up is one sentence in your report.
