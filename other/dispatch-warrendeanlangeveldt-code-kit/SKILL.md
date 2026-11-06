---
name: dispatch
description: Hand stories from the plan to their lane agents, one per lane, every free lane at once. Picks the ready stories, checks each is buildable, briefs each lane agent with its story, requirements and acceptance criteria, and starts it on its own branch and worktree. Use when the lead is ready to start building, asks what to work on next, or runs /code-kit:dispatch [story IDs, a milestone, or "next"].
---

# Dispatch stories to lanes

Only the lead dispatches. Lane agents build; the lead writes contracts, reviews and merges.

The argument names what to dispatch: story IDs (`ST-4 ST-7`), a milestone, or `next` (everything that's ready). With no argument, show what's ready and ask.

The CLI is `node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs"`, run from the project root.

## 1. See what's ready

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" status
```

A story is **ready** when its dependencies are done and nobody has started it. `status` also lists gaps between the specs and the plan; a story with a gap (an unknown lane, a requirement no spec defines) isn't dispatched until the lead fixes the plan. Stories in the `lead` lane are never dispatched: the lead builds them itself. Nor are design stories (`**Lane:** design`): the lead designs them with the person (`/code-kit:design`), and the screen stories that depend on them wait until their designs are approved and merged.

If the project has no `docs.plan`, or the plan has no stories in the `### ST-n` form (`${CLAUDE_PLUGIN_ROOT}/templates/plan.md`), stop and suggest the spec-design skill.

## 2. Check each story before it goes

For every story you're about to dispatch, read in full:

- the story in the plan;
- every requirement it cites, in its spec, with the spec's open questions;
- the lane's agent file in `.claude/agents/`.

Then check:

- **No open question blocks it.** If a spec's open questions touch a cited requirement, don't dispatch the story; list the question for the person.
- **The contracts exist.** If the story needs an API schema, event or database contract that isn't written yet, that's the lead's work first. Write it (the lead owns contracts), commit it on the lead's branch, then dispatch. A lane never invents a contract.
- **The lane is right.** Run `who` on the paths the story will touch. If they belong to two lanes, split the story or sequence it; don't hand one lane another's files.
- **One story per lane.** A lane runs one story at a time across the whole project, every session included: two agents in one lane build on the same files in their worktrees and conflict at merge. Different lanes run in parallel; that's what the plan's dependencies are for. `code-kit next` offers at most one story for each free lane, the open slice's first (`**Slice:**`), and starting a second agent for a lane that's running one is refused, naming the story and the session that has it. `code-kit lanes` lists what each lane is running. If a lane's agent stopped without finishing (it was stopped, or its session ended), `code-kit lanes release <lane>` frees the lane for its next story.

Commit everything the lanes need first. Each lane branches from the lead's branch as committed, so uncommitted work isn't there.

## 3. Brief and start each lane

**In a team** (the config has `team`): claim each story before you brief its agent, leasing what it will change, so nobody else's agents build on the same files meanwhile:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" team claim ST-<n> --lease "<glob>,<glob>"
```

When the story carries out an intent the team agreed (`code-kit intend`), add `--intent <its number>`, so the team sees which pull request is the intent's. The lease is the paths the story will create or change: its lane's folders for this feature, and any contract it changes. A claim someone else holds is refused with who holds it; pick another story or ask them. Stories in a lane another person owns are theirs to dispatch. Making the story's branch also claims it, and each commit on it adds what it changed to the lease; merging it ends the claim.

One agent per story: never send a running lane agent a second story, or a send-back. A story that goes on (sent back, or handed back at its context limit) gets a fresh agent: first run `node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" worktrees release <branch>`, which keeps the branch's commits and moves its report to the main checkout, then start the agent as below with the brief, "Read your earlier report first: `.claude/state/reports/<branch with / as _>.md` in the main checkout", and what `node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" replay <story> --brief` prints: the story's last commit, the tests last run, what changed since, and what was reconciled, from its event log, which holds them even when the stopped agent wrote no report. A long-lived agent rereads its whole context on every step, which is most of what a build costs.

Start each story with the Agent tool: `subagent_type` is the lane's agent, `model` the one `code-kit next --json` gives the story in `models` (with the lane model `story`, each story's model follows its `**Size:**`, raised for a security requirement, a fix or a send-back; a story with no size runs on Sonnet, so size it in the plan first if it's plainly small or large), `isolation: "worktree"`, and run them in the background, with a `description` that starts with the story's id ("ST-12 booking form"): the loop reads it to know the story is in flight, and won't ask for it again while the agent works. Each lane works in its own worktree, `.claude/worktrees/lane-<lane>`, kept from story to story with its installs: code-kit gives it to the lane's agent when it starts, detached at the main checkout's HEAD, so the agent makes or switches to its story's branch as the brief says. So start the agents one per message, each right after the last (they still run in parallel in the background): code-kit tells each agent's worktree whose it is as it starts, and refuses a second agent with a worktree in the same message.

The brief is the agent's whole context. Write it so the agent needs nothing else:

```text
Story ST-<n>: <title>   (lane <lane>)
Branch: <lane>/st-<n>. Create it first, from the lead's branch: git switch -c <lane>/st-<n> <lead's branch>

Requirements (read each one in full, with its acceptance criteria):
- <spec path>#<ID> <name>
- …

What to build: <the story's description, and anything the lead decided that the spec doesn't say>
Fixes: <for a fix story, what was broken and where it was seen; write the test that fails because of it first>
Contracts to use: <paths of the schemas, events or tables this story relies on>
Designs: <for a story that builds screens, what `code-kit designs ST-<n>` lists: each screen file, and for every state its image, its code and its viewport, and the tokens file. Read every state's image and code before writing the screen; match its layout, copy, spacing and states exactly; build it from the design system's components rather than pasting the export; and account for every state in your report>
Out of scope: <what neighbouring stories or other lanes will do>

Steps:
1. Run the spec-check skill against these requirements and save the report, with its `| Requirement |` table (the path guard requires it, and reads a report without that table as none).
   If it recommends "blocked on questions", stop and report the questions.
2. Build it end to end in your lane's paths. No mocks, stubs, placeholder screens or "coming soon".
3. Write tests that prove each acceptance criterion. Name the requirement ID in each test's title,
   e.g. test('BOOK-4 a customer can cancel up to 24 hours before'), so `code-kit status` can trace it.
4. Run <the lane's proving command> until it passes.
5. Commit on your branch. The message names ST-<n>, what changed and the proof.
6. Finish with: what you built, per requirement; the commands you ran and their output; open questions.
```

**A person running a lane** instead of an agent gets its own worktree, marked with the lane:

```bash
git worktree add ../<repo>-<lane>-st-<n> -b <lane>/st-<n> <lead's branch>
echo <lane> > ../<repo>-<lane>-st-<n>/.lane
```

Give them the same brief. Claude Code opened in that worktree then acts as the lane.

## 4. Keep track

- Set each dispatched story's `**Status:**` in the plan to `in progress`, and commit it on the lead's branch.
- Tell the person, in a few lines: what was dispatched, to which lane and branch, what's still blocked and on what, and what's ready next.
- As each agent finishes, read its hand-back: a few lines saying done or blocked, and the path of its full report (`.claude/state/reports/<branch>.md`). Open the report only when you need its detail: in the review, or to decide what it asks. If it came back with a change request or a question, decide it yourself with `/code-kit:decide`, and bring to the person only what crosses a guardrail. If it came back done, run the review skill on its branch.
