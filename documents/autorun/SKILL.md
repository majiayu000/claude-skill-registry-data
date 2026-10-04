---
name: autorun
description: "Run the cards that do not need you. One `/super-bootstrap:autorun` turn = read every open card → admit the ones whose next step needs no user (shared/user-wall.md) → one isolated git worktree + one headless `claude -p` per card, each running the whole card to done and committing on its branch → when all have stopped, one sheet: DONE rows carry the merge line, WALL rows ask resolve / park / drop. Never merges. Sub-verbs: `status`, `release {id}`. User-invoked only."
disable-model-invocation: true
tags: [autorun, worktree, parallel, unattended]
---

# autorun — run what does not need you

Pick → run → sheet. The gateway orchestrates; each admitted card is one worktree session that runs to done or to its first wall. State lives in files — the next invocation re-reads and picks again.

**Consumer contract:** the super-bootstrap runway — `docs/work/{BUG,DEBT,GAP}-###.md` cards, `/super-bootstrap:commit`, `/super-bootstrap:merge`. First run self-installs the worktree infra (`assets/ensure-infra.md`).

## Pre-flight

1. **Infra** — `assets/ensure-infra.md`; absent → one-time install confirm, decline ends the turn.
2. **Base** — `git fetch` + fast-forward the base branch; a conflict surfaces and ends the turn.
3. **In flight** — `Glob .claude/worktrees/autorun-*/OWNED_BY`. Each hit is a claimed card: it is skipped by the pick below and listed under `status`. A worktree whose card file is gone → surface for `release`.

## Pick

Read every open card thread (`docs/work/{BUG,DEBT,GAP}-###.md` — the cold-reader read set, `docs/work/README.md` § Thread contract). Admit a card when its next step needs no user — the test is `${CLAUDE_PLUGIN_ROOT}/shared/user-wall.md`, read at pick time — and none of these hold:

- claimed (an `autorun-{id}` worktree exists) or already on an unmerged branch (`git branch --no-merged {base}`);
- the deliverable is a harness file (`CLAUDE.md`, `.claude/**`, plugin-source skills / agents / rules) — a worktree cannot audit the harness it runs under; route to `/super-bootstrap:needs-me`;
- held by an open `docs/outward/OUT-###.md` whose `Owning card:` names it.

A prose argument narrows the set (`/super-bootstrap:autorun 不碰 business`, `only DEBT`). Cards whose `Area:` / thread name overlapping files share one worktree and run in dependency order; the rest run in parallel.

Print the pick, then proceed — the user interjects in prose if the pick is wrong:

```
autorun — {N} cards
run:   {ID}  {one-line aim}           (grouped rows share a worktree, "→" between them)
skip:  {ID}  {reason — needs you: decision | taste | eyes | waiting on X | claimed | harness | held}
```

Zero admitted → print the skip list and end the turn.

## Run

Per admitted card or group — `assets/parallel-worktrees.md` § Warm (claim = `mkdir .claude/worktrees/autorun-{id}`, branch `autorun/{id-lower}`, template copied, `OWNED_BY` written), then one background dispatch (§ Dispatch step, `--` before the brief, no model pin — the session inherits the default). Append the tools the card's next step needs to that worker's `--allowedTools` — `WebSearch,WebFetch` for web research; stack runners come from the repo's own settings, not the dispatch line (§ Worker grants beyond the base set).

**Brief** — rendered fresh from files at spawn, five parts:

1. `assets/worktree-boundary.md`, verbatim.
2. The card path(s) — "read the cold-reader read set `docs/work/README.md` § Thread contract names — the origin, the latest block of each type, and the Amendments after them."
3. **Work order** — run the card whole under this repo's `CLAUDE.md` envelope: ground it if no Verdict block grounds it yet (`/super-bootstrap:triage {ID}`), build, verify, then commit on this branch via `/super-bootstrap:commit` (deferred mode — doc-sync belongs to the merge). A group runs its cards in the listed order, one commit each. Resolve the card as the envelope says (delete the card file in the resolving commit).
4. **Stop conditions** — `${CLAUDE_PLUGIN_ROOT}/shared/user-wall.md` verbatim: the moment finishing needs one of those, land what is done (block appended, commit made), write the status, stop. Missing context the tree does not hold → `BLOCKED`, never a guess.
5. **Status contract** — one line at `.autorun-status` in the worktree root, written atomically (temp file + rename), uncommitted:
   `DONE` · `WALL — {one line: what is needed, from whom}` · `BLOCKED — {what is missing}`.

The turn ends after the last dispatch. Completions arrive as background notifications; a notification with no status file reads as `BLOCKED — no status written`.

## Sheet

When every spawned session has returned, read each status via `cat .claude/worktrees/autorun-{id}/.autorun-status` (never `Read` inside a worktree — `assets/parallel-worktrees.md` § Read discipline) and render one sheet:

```
autorun — sheet
DONE   {ID}  {aim}                        → inspect, then /super-bootstrap:merge autorun/{id-lower}
WALL   {ID}  {the one line}
BLOCKED {ID} {the one line}
```

Then one `AskUserQuestion` per WALL / BLOCKED row — three options, always:

| Pick | Gateway action |
| --- | --- |
| **Resolve now** | The user's answer appends to the card (`## Amendment` / `## Design` per `docs/work/README.md`); re-render the brief and re-spawn in the same worktree. |
| **Park** *(default when the user has no time)* | Append `## Progress — {date} · autorun` to the card: the wall line + `branch: autorun/{id-lower}` + what landed. Tear the worktree down (§ Cleanup), keep the branch. A later session picks the card up cold from its thread. |
| **Drop** | The card is not worth finishing: delete the card file, tear the worktree down, delete the branch — one commit naming why. |

DONE rows wait for the user; the merge runs only through `/super-bootstrap:merge`.

## Sub-verbs

- `status` — list `autorun-*` worktrees with card, branch, age, and the status line. Read-only.
- `release {id}` — tear down a crashed or abandoned worktree (`assets/parallel-worktrees.md` § Cleanup); the card and branch stay.

## Rules

- **Gateway holds destructive git.** Merge, push, worktree removal, branch deletion — gateway only, each behind a user prompt. Sessions hand off through the status line.
- **State = file presence.** Worktree dir + `OWNED_BY` + card thread + branch. Every invocation re-reads; nothing is remembered across turns.
- **Read-around, never Read-in.** `git show autorun/{id-lower}:<path>`, `cat` the status file, `Grep` / `Glob` markers — mechanically backed by the `PreToolUse(Read)` hook ensure-infra installs.
- **Verification that depends on module resolution runs at the merge, on the base tree** — a nested worktree can resolve phantom deps from the parent (`assets/parallel-worktrees.md` § Nested-worktree false-greens).
