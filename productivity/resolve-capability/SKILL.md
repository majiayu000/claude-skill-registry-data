---
name: resolve-capability
description: Say how each thing a pstack step asks for (start a helper, start a worker on another agent, ask the user, wait for an event, find past sessions, and so on) is done in this environment, and what to do when it cannot be. Read at the start of a task. Use when a step names a capability.
disable-model-invocation: true
---

# Resolve a capability

A pstack step names what it needs by a capability name in backticks, such as `spawn-worker`. It does not name a tool. This skill says how to find the tool that does it here. The skills that name capabilities live next to this one, so read this file as `../resolve-capability/SKILL.md`.

This file names no product. The mechanisms live in [`adapters/`](adapters/), one folder per product, each with an `adapter.md`. A harness adapter covers the agent a session runs in. An environment adapter covers a layer that runs on top of harnesses and adds to them. This file holds the vocabulary, the rules for choosing among the adapters' mechanisms, and what to do when no adapter has one. A new adapter starts from [`references/adapter-template.md`](references/adapter-template.md).

## 1. Which environment is this

Answer these as separate questions. They are not alternatives. A session runs in exactly one harness and in any number of environments.

1. **Which environments are here?** Run `sh <folder of this file>/scripts/detect.sh` now, before you plan or start anything, and also when the task says to plan only. It prints the id of each environment adapter whose check answers yes. Read `adapters/<id>/adapter.md` for each id it prints. Do not decide this from the harness you are, from `which`, or from memory, and do not put the check off to a later step. No output means no environment: read [`references/plain.md`](references/plain.md).
2. **Which harness are you?** Your own tool list and instructions tell you. Read the harness adapter in `adapters/` whose Detect section matches you now, in the same step as the environment adapters, also when the task plans no spawn. Most capabilities have the `own harness` scope, so that adapter answers them, `track-todos` and `ask-user` included. When none matches, pstack has no adapter for your harness. Use the fallbacks in the index and say so once.
3. **This computer and this user.** `~/.agents/skills/select-model/SKILL.md` records which products and models are installed, which environments exist, and what the user prefers. Read it too. When it is missing, say so once and use the defaults in `../poteto-mode/SKILL.md`.

## 2. How to use the index

Each capability in the index has a scope. The scope says whose mechanism answers.

| Scope | Who answers |
| --- | --- |
| own harness | A heading for the capability in an environment adapter that applies, marked `Overrides.`, wins within the conditions it states. A heading marked `Adds to.` runs after your harness's mechanism. Otherwise the heading in your harness adapter answers. Otherwise the fallback in the index does. |
| every harness | The heading in every harness adapter, for each store or source that exists on this computer, not only your own harness's. Then the environment headings, by the same markers. |
| target product | The adapter of the product you start: its Start me from outside section, or the Launching harnesses section of an environment that applies. Pick the one that accepts the model and effort you were asked for. When both do, prefer the environment, because it supervises the run. When the product has no adapter, use the fallback. |
| contract | The mechanism in the index. A heading marked `Adds to.` in an environment adapter that applies runs after it. |

- A mechanism marked `(unverified)` has not been run on a real session yet. Use it, and say in your reply if it failed.
- When a heading points to a reference file, read that file before the first use in the run.
- `select-model` records what was true when it was generated. When it says a product starts only through an environment that is not here, read that product's Start me from outside before you give up on it.
- A step that cannot be done and has no fallback is skipped with one line: `Skipped: <step>. <reason>.`
- Where a mechanism says "exact", copy the command from [`references/exact-steps.md`](references/exact-steps.md) as written, and read the same-named section of each environment adapter that applies. Do not rebuild it.
- A seat that needs one of your MCP servers stays on your own harness. A worker on another product loads only that product's MCP configuration.

## 3. Index

**Agents and work**

- `spawn-subagent` (own harness): a helper inside your harness that returns its result to you. Give a read-only job a read-only agent type (one whose tool list has no edit or write tool) and a brief that says not to edit, and check `git status` after. A general-purpose type is not read-only even when the brief says so. Fallback: do the work yourself and say so.
- `spawn-worker` (target product): an asynchronous worker on another agent product, with a report. Any session with a shell can start another product's CLI headless, as [`references/cli-workers.md`](references/cli-workers.md) says. An environment can add supervision and a durable run. Read the target's adapter, and each environment adapter that applies, before the first start and when you plan one, because they say which model and effort flags each way of starting takes. Fallback: when the other product is not installed, not logged in, or has no adapter, run the seat on your own model and say in one line which product would run it.
- `isolate-checkout` (own harness): its own worktree, ports, and temp paths for a seat that writes. Fallback: `git worktree add` by hand, and remove it with the exact step.
- `run-remote` (own harness): a run that survives this computer sleeping. Fallback: run here and say that it ends with this session.
- `coordinate-workers` (own harness): dispatch, dependencies, an inbox, and decision gates. Fallback: one tracker file in `durable-store` with a line per unit (its owner, state, PR, head SHA, and verdict), or the plan in the reply. Verdicts always stay in that file.
- `control-agent` (own harness): probe, message, stop, or replace an agent. Fallback: say the agent cannot be probed.
- `choose-model` (contract): which model and effort for a seat. Read `select-model`. When it is missing, use the defaults in `../poteto-mode/SKILL.md`. No fallback is needed.

**Waiting and time**

- `wake-on-event` (own harness): block on, or be woken by, a worker finishing, a CI result, or a PR change. See [`references/waiting-and-schedules.md`](references/waiting-and-schedules.md). Fallback: poll with a bounded shell loop, or stop and say what to re-run.
- `run-on-schedule` (own harness): a recurring tick for a long program. See [`references/waiting-and-schedules.md`](references/waiting-and-schedules.md). Fallback: skip, and tell the user to re-run by hand.

**Talking to the user**

- `ask-user` (own harness): a question with options, only for a call the user must make. Fallback: numbered options in the reply.
- `track-todos` (own harness): a visible plan with step status. Use the plan or todo tool in your tool list. Fallback: a list in the reply.

**Code hosting**

- `use-forge` (contract): create, list, review, and merge pull requests. `gh` in every environment. Exact steps for opening, stacking, merging, and re-basing are in the exact-steps reference. A step that needs the user to click or merge prints the exact command instead. No fallback is needed.
- `read-review-bot` (contract): read automated review threads and check runs on a PR. `gh`, with the bot named by the repository's own checks and logins. Fallback: skip the step when the PR has no review bot.

**Files, skills, and sessions**

- `run-skill` (contract): run another pstack skill. Read its `SKILL.md` at `../<name>/SKILL.md` and follow it. The form a user types is in your harness adapter's For users section. No fallback is needed.
- `author-skill` (own harness): write a new skill. Fallback: the Authoring a skill playbook.
- `find-sessions` (every harness): this workspace's past and running sessions and their transcripts. Each harness adapter names its store and how to pick your own session out of it, usually by its first user message. Fallback: say which store you could not read.
- `locate` (own harness): where instructions, skills, and worktrees live. The folder that holds the pstack skills is the parent of this skill's folder. Playbooks call it `<pstack>`, so `<pstack>/poteto-mode/SKILL.md` is `../poteto-mode/SKILL.md` from this file. Fallback: ask the user.
- `durable-store` (contract): a place that outlives a restart: decision trails, plan files, queue state. `~/.pstack/store/<repo-slug>/`. Name it in every worker spec. A one-off report or a worker's output is scratch, not durable: write it under a `mktemp -d` path. No fallback is needed.

**Driving and inspecting**

- `list-mcp-servers` (own harness): which MCP servers this session has. Your tool list shows the tools they provide. A worker has only its own agent's servers, not yours, so for a worker read the target product's adapter. Fallback: say which servers you could not see.
- `drive-app` (own harness): drive a browser, a terminal program, or a desktop window, and capture evidence. How to drive one step at a time and what to capture is in the bundled **control-ui** skill (browser, Electron, and web UIs) and **control-cli** skill (CLIs and TUIs). Fallback: a browser MCP, or the temporary harness those skills build (Playwright or the DevTools protocol, `tmux` or a PTY script), and screenshots. For a recording on macOS, `screencapture -v -V <seconds> <file>.mov` recorded a clip here (it films the whole screen, so tell the user and keep the file out of the repository). Playwright's video option is another way (unverified).
- `inspect-runtime` (contract): attach to a live process for CDP, a CPU profile, a heap snapshot, or code evaluated in it. The Node inspector or the Chrome DevTools protocol through the shell (unverified). Fallback: say which attach method was missing.

## 4. Bundled tools are not capabilities

`../poteto-mode/scripts/` ships tools that run the same everywhere: `watch-pr` (the READY, WAITING, ADVANCE, COMPLETE verdict for a PR), `check-plan.mjs`, and `worktree-audit.sh`. Several need `bun`. A step that uses one names it. Only the waiting is a capability: use `wake-on-event`.

## 5. When to read this again

At the start of a task, after a restart, after the context was compacted and before the next wave of spawns, on every heartbeat tick, and when you take over a run from an earlier session, which may have run in another environment. Before an irreversible command, reread only that command's section of the exact-steps reference, and the same-named section of each environment adapter that applies.

## 6. When this skill is wrong

If a mechanism fails or does not exist, use the fallback, say so in the reply, and tell the user what you saw. This skill and its adapters ship with pstack and are not edited from a task. A fact about this computer belongs in `select-model`, which asks the user before it changes.
