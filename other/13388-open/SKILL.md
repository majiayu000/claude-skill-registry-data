---
name: open
description: "Activate at session start when .bon/ exists AND before any bon CLI command. Handles session orientation (process contributions, present hierarchy, pick direction), structures draw-down workflow (bon show → bon work → bon step), and covers roaming — orienting against a named repo from a session launched elsewhere. Triggers on: session start with .bon/, /open, '/open REPO' (a path or repo name), /bon, 'bon init', 'bon new', 'bon list', 'bon done', 'what can I work on', 'next action', 'desired outcome', 'file this for later', 'track this work', 'work on that repo from here', or when .bon/ directory exists."
allowed-tools:
  - "Bash(bon:*)"
  - Read
  - Glob
  - Edit
  - Write
---

# Bon

Bon tracks work as **Outcomes** (desired results) and **Actions** (concrete next steps). No sprints, no story points, no priority levels — just ordering and a clear answer to "what can I work on now?"

---

## The Brief

Every bon item answers up to five questions. Three are required, two optional:

| Flag | Question | Required |
|------|----------|----------|
| `--why` | Why are we doing this? | Yes |
| `--how` | How will we approach it? | No |
| `--what` | What will we produce? | Yes |
| `--done` | How do we know it's complete? | Yes |
| `--badly` | What would show this went wrong? | No — outcomes, and **the human writes it** |

**`--badly` is the falsifier, and it is not a fifth flag bolted onto a four-field
form** — it restores the half of GTD's first planning phase that bon dropped
(purpose *and principles*). `--done` asks how we know the work is complete, which
a Claude can satisfy by construction and routinely does; `--badly` asks what
would show it went wrong. Those catch different failures, and "met the criteria
but built the wrong thing" is now the more common one.

It only works if the implementer didn't author it. **If you are filing the item,
leave `--badly` absent** — an absent falsifier is an honest, visible gap, while
one you wrote is `--done` in a hat: a test that cannot fail. `/lay-out` asks the
human for it, in their words, verbatim. `/bon-review` checks work against it.
Outcomes only; the CLI nudges if it lands on an action.

`--how` captures approach, strategy, constraints, and sequencing — things that don't belong in `--what` (deliverables) or `--why` (motivation). For simple work, skip it. For anything with technology choices, ordering dependencies, or coordination needs, include it.

**For outcomes:** `--how` is the overall strategy. "Use Redis distributed locks, not file locks. Coordinate with API gateway. Don't modify auth middleware."

**For actions:** `--how` is the specific approach. "Parse the JSONL with streaming reads, not load-all. Test with the 10k-item fixture."

**`bon work` surfaces `--how` as "Approach:" above the step list**, so the executing Claude has strategy context before touching code.

---

## Plans Become Bons

When you'd normally enter plan mode, create bon items instead. A bon hierarchy **replaces** a plan file — it's persistent, trackable, and the next Claude can pick it up.

| Plan mode | Bon |
|-----------|-----|
| Goal/context | `--why` |
| Approach, strategy, constraints | `--how` |
| Steps (ordered) | `--what` (numbered → tactical steps) |
| Success criteria | `--done` |

**The transmutation:**
1. Think through the work as you normally would
2. Create an outcome with `--why` (motivation) and `--how` (strategy)
3. Break into actions with `--how` (approach per step) and `--what` (numbered deliverables)
4. The plan IS the bon hierarchy — no separate document to maintain

**The test:** After creating the bons, could you delete the plan file with no information loss?

---

## Session Start Ritual

The session-start hook provides orientation automatically (handoff, outcomes, suggested items). Your job is the LLM-mediated work the hook can't do.

The hook output may be truncated in the system-reminder preview. When you see "Output too large ... Full output saved to: {path}", Read that file — the handoff (including "For Claudes to come") is likely past the truncation point.

### 1. Sweep and Synthesize Knowledge

**The sweep replaces latest-wins** (bon-supuko). The hook emits every handoff whose LEDGER.md line is still unticked, one `UNPROCESSED=<path>` line each, oldest first — and, in a ledgered dir, every handoff file NO ledger line mentions at all, annotated `[no ledger line — process, then ADD a ticked line for it]`. That annotation means some close never registered the file (an older plugin's close, a forgotten append, a hand-dropped file): process it identically, then ADD a fresh ticked line for it rather than editing one — without this, one coexisting unticked line would make that file permanently unreachable. Process ALL of them, not just the newest — two interleaved closes in a shared repo used to silently drop the older one: its For-Claudes-to-come never synthesised, its Candidates never minted, nothing said so. When no `UNPROCESSED=` lines appear (no ledger yet, or all ticked), process just the `HANDOFF=` file — that is the latest-wins fallback, and it stays correct for repos that haven't adopted a ledger.

For EACH unprocessed handoff, oldest first:

1. Read the project's `understanding.md` — the session-start hook resolves and prints its path as `UNDERSTANDING=<path>` (a visible root/nearest-room copy if the repo uses the visible convention, else `.bon/understanding.md`). Read *that* path (once is enough for the whole sweep).
2. Read the handoff's `## For Claudes to come` section, when present
3. **Rewrite** that same `understanding.md` (the resolved path — not blindly `.bon/`) — integrate the new knowledge, make salience judgments, restructure where needed. Don't append. In a multi-handoff sweep, integrate as you go — a later handoff may supersede an earlier one's framing, and processing in write order is what lets you see that happen.
4. Mint its Candidates (step 2 below), then **tick its ledger line**: edit `- [ ]` to `- [x]` and append `(processed YYYY-MM-DD)` — the generalisation of the candidates `(minted YYYY-MM-DD)` heading-edit. An unticked line is a handoff the next session will re-process; a ticked line without the processing done is a dropped baton. Tick AFTER the work, never before.

This synthesis is onboarding. Integrating new knowledge into an existing document forces you to read the existing understanding, find where the new insight fits, and rewrite with judgment. By the time you're done, you know the project — not just the words on the page.

> **Note — `understanding.md` has two authors.** `/open` *maintains* it (synthesizing each handoff's durable knowledge, as above); `/lay-out` *seeds* it with architectural framing when planning multi-session work (`/lay-out` Phase 2). Same file, two roles — don't clobber plan-seeded framing during synthesis; integrate around it.

The handoff stays on disk — never delete it. Not every handoff has a compost zone; when absent, skip this step.

**Transition:** If `.bon/contributions/` contains files, process those the same way (read, integrate into understanding.md, delete the contribution files). This path is being retired.

### 2. Mint Pending Candidates

Any swept handoff (step 1's loop — not only the newest) may carry a `### Candidates` section — board mutations proposed by a session that could see the board but couldn't reach a writer (candidate mode; the live case is a Cowork close). They are proposals, not tracked work: mint them now, or they're lost. When the handoff has no such section — the common case — skip this step for that file.

For each candidate, run the matching verb, tagging where it came from so provenance survives:

- **NEW** → `bon new` (JSON stdin); add its origin to the brief, e.g. `"(candidate from Cowork session local_7c379a74, 2026-06-10)"`
- **DONE** → `bon done ID --note "…"`
- **EDIT** → `bon edit ID …`

Mint deliberately, not on autopilot: if a candidate is stale, already done, or wrong, drop it and say so to the user — a conscious drop is a real decision; an unnoticed one is the leak this step exists to close. Two worked examples predate the spec and carry their candidates as an "Opportunities — bon candidates" prose list rather than a `### Candidates` heading — treat that shape as candidates too (citations: `docs/HANDOFF-CONTRACT.md`).

**Then mark them minted**, so a re-open doesn't double-mint: edit the handoff's candidate heading to `### Candidates (minted YYYY-MM-DD)`. This is the step that re-syncs the board with the handoffs — it's what cures "where do I pick up".

**And adopt the file when its candidates belong to another board.** A candidate-mode handoff lands on whatever mount its session had, which isn't always the board that owns the work. When the board you just minted on is a different repo, move the handoff into that repo's handoffs dir in the same change (updating any ledger line that links it) — the board item and its artefact travel together. Minting the item while leaving the file behind lets it drift into another room's briefing: the 2026-08-04 Cowork hello wrote a mit-commons handoff to the notes root, its candidate was minted on the mit-commons board five days later, and the stranded file was then served as the baton to an unrelated notes session.

### 3. Present Hierarchy

**On a JSONL board, refresh its truth first — one fetch per session, here** (bon-wevodu). The board is a local file, so a behind-origin clone renders a stale hierarchy and lets you file duplicates against it (the passe-partout twin was filed exactly this way — the duplicate-check ran clean against a stale clone). Dolt boards skip this: one networked writer, always current.

```bash
git fetch -q origin 2>/dev/null
behind=$(git rev-list --count HEAD..@{u} -- .bon/items.jsonl 2>/dev/null || echo 0)
```

If `behind` is greater than 0, say so in the orientation ("board is N commits behind origin") and bring it current with `git pull --ff-only` when the working tree is clean. One boundary, phrased by mechanism: the fetch touches only the remote-tracking ref, but a pull is a branch write — so in a repo whose git writes belong to a robot (an auto-committing sync agent; such boards carry `off` in `.bon/sync` for the same reason), stop at the warning and let the robot carry the merge. After this fetch, `bon new`'s own staleness check (which compares against the tracking ref without network) stays honest for the rest of the session.

Show the full picture — outcomes with progress and their actions — **as text in your response** (not via Bash, which collapses behind Ctrl+O).

Run `bon list`, capture to a temp file, Read and output:
```bash
OUT=$(mktemp "${TMPDIR:-/tmp}/bon-hierarchy.XXXXXX"); bon list > "$OUT"; echo "$OUT"
```

**The X's stay at the end, which is why there is no `.txt`.** macOS's BSD `mktemp` only randomises a run of X's at the very end of the template. With a suffix after them it creates the file at the literal path and exits 0, so the guard below silently becomes the fixed shared path it exists to prevent. Then it compounds: the literal file persists, every later call exits 1 with an empty string, and `bon list > ""` hands the next Claude a blank path. GNU `mktemp` accepts the suffix, so this was invisible from Linux. `TMPDIR` is per-user on macOS, which makes the path collision-proof by construction as well as by randomness. (A family user's fix, f359706 on their fork, 27 Aug. It had nowhere to land until 2026-09-23.)

Read the path it echoes. The path must be unique per session: a fixed
`/tmp/bon-hierarchy.txt` is shared by every concurrent `/open`, and on
2026-07-26 one session overwrote another's capture seconds before its Read —
the second session was one unnoticed glance from presenting a different repo's
board as its own (bon-potipe). Wrong-board orientation fails silently, so the
collision-proof path is the whole guard.

**Then declare the orientation** (bon-lateje). The estate's launch pattern has moved: sessions start in a high-level folder and `/open REPONAME` orients against a repo, but the statusline shows the directory the process was launched in — so a session working `mit-kg` reads as sitting in `~`. The dissolve is not to track the session but to have it *declare*, here, at the moment it commits to a board:

```bash
mkdir -p ~/.claude/state/oriented
printf '%s %s\n' "$CLAUDE_PID" "/absolute/path/of/the/repo/you/just/oriented/on" \
  > ~/.claude/state/oriented/"$CLAUDE_CODE_SESSION_ID"
```

Write it on **every** `/open`, not only a roaming one. A session that roams to another repo and later comes back would otherwise leave a breadcrumb still naming where it went, and the statusline would confidently show the wrong repo — which is the exact failure the card exists to prevent. Overwriting on every orientation keeps the file true by construction; when it names the launch dir the statusline draws nothing, so the plain in-repo case looks precisely as it does today.

**And the breadcrumb follows the DRAW-DOWN, not only the `/open`** (bon-monevu; Sameer's call, 2026-09-01). When you `bon work` a card whose board is not the one you declared here, write the breadcrumb again for that board — same command, new path. The case that decided it: a session launched at `~` `/open`ed `~/.claude` because that was where the unticked handoff sat, then drew down a notes-board card and spent its evening in a bench directory, with its statusline reading `.claude` the whole time. Orientation is where you read; the claim is where you commit, and the glance should show the commitment.

This stays a *rite* step rather than a side effect of the `bon work` command, and the reason is measured (2026-09-01): **the CLI cannot tell a dispatched worker from a top-level session, so a CLI-side write would defeat the subagent guard below.** A write from `bon work` was built, tested and published in suite 1.85.0, then reverted in 1.85.1 on that finding.

Three things are contract with the reader (`statusline.local.sh`, carte-kasepo) rather than free choices: the filename is the session id **from the environment**, never inferred from the newest file — deriving identity from ambient state is how two sessions come to read each other's state; the PID goes *inside* the file rather than in its name, because a session id survives `claude --resume` while a PID does not; and the format is one line, `<pid> <absolute path>`. The reader checks the PID with `kill -0` and renders nothing at all when the breadcrumb is absent, malformed or dead — a confidently wrong location is worse than a coarse right one, so if you cannot name the repo with certainty, write nothing.

**If you are a subagent, do not write it.** A dispatched worker inherits the PARENT's `CLAUDE_CODE_SESSION_ID` — measured 2026-08-31, byte-identical to the `--session-id` on the parent harness's own command line — and the parent's live `CLAUDE_PID` with it. So a worker that writes the breadcrumb does not mint its own: it overwrites the parent's, with a liveness token that passes every check the reader makes, and the human's statusline then confidently shows wherever the *worker* roamed. That is the failure this card exists to prevent, arriving through the one door that looks like a rounding error. **Knowing you were dispatched is the authority here, and `CLAUDE_CODE_CHILD_SESSION` is not even a hint — it marks nothing.** Measured 2026-09-01, and it retires the older reading of that variable as a worker marker that merely *leaks* sometimes (carte-suruta, 2026-08-24): the `claude` process itself carries neither `CLAUDE_CODE_CHILD_SESSION` nor `CLAUDE_CODE_SESSION_ID` (read straight off `/proc/<CLAUDE_PID>/environ` — 54 variables, zero matches), and **the Bash tool injects both into every subprocess it spawns.** So the variable means "your parent is a Claude Code session", which is true of every Bash call in an ordinary top-level session as much as in a worker. Anything keyed on it either fires always or never; it can never discriminate. That is why the estate's other worker-detector reads structure instead — a worker's tool_use lands in `subagents/*.jsonl`, never the root transcript — and why this guard is addressed to you rather than to a script.

**And there is no other variable to reach for: the door is measured shut** (bon-kigeti, same day, both arms running one script file so the instrument could not differ). Of 69 environment variables, a dispatched worker's Bash environment differs from its parent's in exactly **one** — `CLAUDE_EFFORT`, absent in the worker. `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID`, `CLAUDE_CODE_ENTRYPOINT` and even `CLAUDE_CODE_MESSAGING_SOCKET` (whose socket the worker confirmed live, killing the plausible guess that an unmessageable worker would lack it) are byte-identical. Do not build on that one difference: it exists only because this machine sets `effortLevel` in settings.json, so it evaporates wherever no effort is set — and if a future CC ever propagates effort to subagents, the guard inverts *toward* workers writing, silently. A guard whose failure is silent and unsafe is worse than none, which suite 1.85.0 already proved once. The leak is harmless here — a top-level session that wrongly skips the write leaves no breadcrumb, and the reader then shows the honest launch dir, which is the coarse-right answer we want. It is the opposite mistake that costs: a top-level session that wrongly skips leaves no breadcrumb and the reader falls back to the honest launch dir, where a worker that wrongly writes hands the human a confident lie.

And if you are roaming as a worker, the orientation you would be declaring is not the one the human is looking at anyway: the breadcrumb has no expiry and nothing restores it when you exit, so a worker's write to its repo would outlive the work and stand there after the worker is gone.

### 4. Personal Half (variation point `open.personal`)

`open.personal` names a POINT INSIDE this one rite — there is exactly one /open for everyone, never a personal /open beside a team one; the personal half is a file this step reads, silently absent on most machines. The spine ends at the hierarchy; what a given operator wants rendered between the hierarchy and the direction pick — a dispatch-queue digest, a calendar glance, nothing — is theirs, and lives in their personal half (`~/.claude/mit-accent.md`, spec: `docs/ACCENT.md`). The session-start hook prints `ACCENT=<path>` when the file exists. The four personal variation points are named by ownership, uniformly — `open.personal`, `close.personal`, `plan.personal`, `review.personal` (settled by the operator, 2026-08-30; "personal" not "local", because local means per-machine on this estate and this split is per-person) — and whatever the operator calls the content inside their own file is theirs to change without touching core.

- **`ACCENT=` present:** Read the file's `## open.personal` section and follow it here, then continue to step 5. The worked example is an operator whose accent renders a three-line digest of their own task-manager dispatch queue.
- **No `ACCENT=` line, or no `## open.personal` section in the file:** skip SILENTLY to step 5. The rite is complete without it — no nudge, no placeholder, no "you could configure this", ever (law 1: complete-without).
- **`ACCENT=` present but the file won't read, or its section errors mid-run:** one plain line — "personal half unreadable — running the team spine" — then continue. Never banners, never abort (law 3).
- **The accent fills THIS slot only** — it cannot skip, reorder or override steps 1–3 and 5–6 (law 2), and it writes into the operator's own systems only under a sanction the accent itself records (law 4).

### 5. Pick Direction

Assess which ready items align with what's already in context — files read, handoff content, understanding document, whatever the personal half rendered at step 4. State your reasoning briefly. When context is thin, just present the list.

User picks direction.

### 6. Read the Room

In a **multi-room repo** — one with a `rooms.md` index, or nested `CLAUDE.md` files below the root — read the tissue of the room you'll actually work in *before* touching its files: its `CLAUDE.md`, its `understanding.md`, and its recent `handoffs/`. Do this with the Read tool, yourself — the harness won't. It loads a subtree `CLAUDE.md` only on-demand (and Cowork not at all), and it *never* autoloads understanding.md or handoffs on any launch. A session that skips this works a room half-blind and mints twins — the `notes` egta twin was a duplicate room built beside its unread predecessor, caught twelve days later.

This fires **regardless of where the session launched**: a room-launched session still needs the explicit understanding.md + handoffs read, because the harness's upward walk carries only CLAUDE.md. `rooms.md`, when present, is the map of what rooms exist — read it first to place your work. In a single-room repo this is a no-op: the tissue the hook already resolved is the whole story.

Then **draw-down** before touching code.

---

## Roaming: `/open TARGET`

`/open` accepts a target — a path, or a repo name — and runs the whole ritual against *that* repo from wherever the session launched. Treat it as a first-class move, not an exotic one: a session launched at a root can work any repo beneath it, entering repos by name as the conversation turns.

**Resolving the target.** You are the resolver, so fuzzy input is fine — but converge deterministically, matching `bon move --to`'s convention so the two agree: anything containing a slash, or starting with `~` or `.`, is a path; a bare name globs `~/repos/*/NAME` (the owner-bucket layout). No exact hit → widen to a case-insensitive substring glob. Several candidates → list them and ask rather than guess; wrong-repo orientation fails silently, which is why guessing is the one move barred here.

The ritual is reliable only if you supply what the harness will not — each behaviour below was hit or measured live, not assumed:

1. **cd per command.** The harness re-anchors every Bash call at its recorded directory, so a lone `cd` does not persist. Every board or repo-relative command is `cd TARGET && …`. From a container directory a bare bon call adopts whatever board it finds walking upward — the filed-where-cd'd hazard.
2. **No orientation arrives for the target.** The session-start hook ran where you launched. Run steps 1–6 above by hand, anchored at TARGET: understanding.md, the handoff sweep (read the target's `handoffs/LEDGER.md` for unticked lines — not just the latest file; the sweep of step 1 applies to a roamed repo too), the board fetch, `bon list`. The handoff is the read sessions skip — it was skipped in the run that minted this section.
3. **Rank handoffs by header date, never `ls -t`** — file migrations reset mtimes, so a years-old handoff can look newest. `lib-handoff.sh` carries the ranking. **And if the target still has a `.bon/handoffs/` pile, converge it first**: `source <bon-scripts>/lib-handoff.sh; handoff_migrate_legacy TARGET`. The reader stopped looking under `.bon/` in bon-sedoze, and the session-start hook that normally migrates ran at your launch dir, not here — so a roaming session is the one path that can read a repo whose handoffs are still stranded, and conclude it has none.
4. **The target's CLAUDE.md self-loads only when TARGET sits under the session's working directories** (the launch dir, or an added one). Under a root launch that is everything beneath the root — measured: editing a sibling repo's files pulled its CLAUDE.md in unbidden. Anywhere else, Read it yourself before working.
5. **No tactical nudges for the target.** The UserPromptSubmit injection keys on the launch cwd, so step discipline is manual: `cd TARGET && bon work --status` on each return. Mirror hazard: claims key on the invoking cwd, so two roaming sessions working the same target read as one session to the claim guard — declare the lane where a collision is plausible.
6. **Check the target's billing pin.** A repo can pin its own billing route (an `env` block in its `.claude/settings.local.json`, or a launcher-level pin registry); pins bind at launch, so a roaming session silently dodges them. If the target carries a pin this session isn't honouring, say so in one line before heavy work — the user owns the lane choice.
7. **Tell /close where you were.** Handoff placement is work-based, not launch-based (the /close skill's placement table) — name the repo(s) actually worked, so the handoff lands in the target's `handoffs/`, not the launch cwd's.
8. **Declare the orientation** — step 3's breadcrumb, and this is the case it was built for: a roaming session is precisely the one whose statusline is otherwise wrong all session. Write it for TARGET, and rewrite it whenever you roam again — **unless you are a dispatched worker, which is the other thing roaming sessions usually are.** A worker's write lands on its parent's breadcrumb, not its own; step 3 has the mechanism and the reason.

A target carrying its own visiting protocol in CLAUDE.md (route → read on entry → search before mint → register on write) is stating this same rite in local terms — follow the stricter. The list covers the seams found so far, not every seam; where it runs out, reason from the mechanism: nothing launch-scoped follows you, everything on-demand does.

---

## The Draw-Down Pattern

**Pre-flight checklist** (before touching code):

1. **`bon show <id>`** — verify the item exists, check its type and brief
   - If the ID came from a handoff or memory, it may have been archived. Verify first.
   - If `Type: outcome`, pick one of its actions instead.
2. **Three legs of staleness** — see below. About thirty seconds; skip for a card you filed this session.
3. **`bon work <id>`** — initialize tactical steps from `--what`
   - Shows "Approach:" context from `--how` when present
   - If `--what` has no numbered steps, provide explicit ones: `bon work <id> "Step 1" "Step 2"`
   - **A `Baton (date): <handoff>` line means another session last worked this thread** (bon-jeweke: the newest handoff citing this item in its `items:` frontmatter). Read that handoff before starting — it is the directional briefing addressed to whoever picks the thread up, which is now you. A fresh item shows no Baton line.
   - **If this card's board is not the one you declared at orientation, re-write the breadcrumb for this board** (bon-monevu) — the same two-line write from step 3 of the session-start ritual, pointed at the board root you just claimed on. The statusline arrow then follows the work rather than the reading. Same subagent rule as there: dispatched workers do not write it.
4. **Work through with checkpoints:** `bon step` after each
5. **Final step auto-completes** the action

### Three legs of staleness (bon-kejika)

A brief is written at the moment of least knowledge about the work, and everything after that makes it wronger. The bon instruction shard has long said to check briefs for staleness before executing, without naming a method — this is the method, borrowed from the dispatch loop, where it caught two of ten queue lines describing work that had already shipped before any worker rebuilt it (2026-08-30). A solo session drawing a card down has the same exposure and nobody above it to catch the miss.

One command each, on the brief you just read:

1. **Do the named artefacts still exist?** `ls` the paths the brief names. Renames are invisible from a brief, and a path that moved reads as a path that was never built. Paths only — where the artefact is a database column, a doc section or a deployed behaviour, note that the leg didn't apply and move on rather than going looking.
2. **Has the card been overtaken?** Read the tail of `--how`, which `bon show` has already printed — no command. Supersession notes, `PARKED for Sameer:` lines and other lanes' claims all land there, because bon refuses a second `bon work` anywhere in one clone, so a parallel lane's claim arrives as appended brief prose rather than in `bon work --status` (bon-kapipu).
3. **Is a sibling already building it?** Scan the hierarchy you already presented at orientation for an open item producing the same artefact; re-run `bon list` only if the session has been going a while. Near-duplicate items spike when several sessions run in parallel, and the board is where that becomes visible.

**A failing leg is information, not a stop sign.** Say what you found before starting rather than discovering it forty minutes into an implementation: `bon edit ID --append-how "STALE <date>: <what you found>"`, then either pick something else or re-brief the card and carry on. Where the evidence needs a human — the desire may have changed, not just the facts — park it in the same append and move on.

Three legs is the whole check. A fourth, or a fifteen-minute investigation, is the failure mode this is guarding against: an orientation nobody finishes is worse than one that occasionally misses.

**Constraints:**
- **Actions only** — `bon work` on an outcome will error
- One active tactical per session (CWD) — different worktrees can run in parallel
- Two CWDs cannot claim the same action
- Context-switch: `bon wait <id> "reason"` (clears tactical — re-plan on return)
- Parking work that's waiting on a scheduled event, not on a blocker: `bon work --release`
  keeps the steps and your position, hands the claim back so the session can draw down
  something else, and stops the step being injected into every prompt. `bon work <id>`
  resumes at the same step, no `--force`. Reach for this over `--clear` (discards) or
  `bon wait` (silently discards) whenever the progress is worth keeping.

### UserPromptSubmit Hook

A hook injects the current tactical step into every prompt. When you see a `<user-prompt-submit-hook>` mentioning bon tactical, work on the current step and, when complete, run the `bon step --expect N` invocation the hook prints — the guard refuses without writing if another session moved the board (re-read with `bon work --status`).

**The injected tactical may belong to another live session.** Session identity is CWD-keyed, so a parallel session in the same repo (a bg fork, a second roster session, a dispatched agent) sees — and is invited to advance — a tactical it didn't claim. If the injected step doesn't match work you've been asked to do, leave it alone: it's another Claude's thread, and stepping it desynchronises their bookkeeping (observed 2026-06-10: an email-dispatched session finished a tester's tactical and closed an item under them).

---

## The Draw-Up Pattern

**When filing work for a future Claude:**

1. **Add `--how` for complex work** — approach, constraints, things to avoid
2. **Include concrete details** — file paths, API endpoints, error messages
3. **Number steps in `--what`** — these become extractable tactical steps
4. **Define `--done` clearly** — verifiable criteria, not vague "it works"
5. **Name the progenitor** — an item discovered mid-work opens `--why` with where it came from ("Discovered while working bon-A"). Write-once provenance: it never rots, grep finds it, and the genealogy survives without a schema field

**The test:** Could a Claude with zero context execute this from the brief alone?

### Use JSON stdin by default — for `bon new` **and** `bon edit`

**When creating outcomes or actions with `--how`, or with more than 3 numbered steps
in `--what`, use `bon new --json` — not flags.** Flags with backslash continuations
look like they work but produce quoting errors on special characters (quotes, backticks,
parentheses in technical content). JSON stdin eliminates this entire class of failure.

**`bon edit` reads JSON the same way**, and it matters more there, because an edit
rewrites content that already exists. Pipe an object with only the keys you want
changed — everything else is left alone:

```bash
printf '%s' '{"how": "Redis locks. Do not touch auth middleware."}' | bon edit bon-zovili
```

Brief fields work nested under `"brief"` or flat at the top level; an unrecognised key
is an error rather than a silent no-op. `"how": ""` clears the field.

**Annotating an item — appending to `--how` — is its own verb, never a
read-modify-write:**

```bash
bon edit bon-zovili --append-how "UPDATE: blocked on the API rename, resuming after."
printf '%s' '{"append_how": "Text with \"quotes\" survives the pipe."}' | bon edit bon-zovili
```

The append is atomic (sets the field when absent, joins with a blank line when
present). The old recipe — read the field, concatenate in python, write it back
with `--how` — silently REPLACES the field when any step misfires, which is how
a correction once destroyed the accurate half of another session's brief
(carte-vudusu). If you must script other whole-field edits, call bon via
`subprocess.run` with an argument **list** (no shell, so quotes can't be
reinterpreted), and read the field back — intent to encode is not execution
of encoding.

**Repairing a closing note:** `bon done ID --note` refuses to overwrite a note that's
already there, so a note mangled by shell quoting used to be permanent. `bon edit ID
--note "..."` is the way back (done items only; `--note ""` clears).

**The rule:** Pipe JSON to `bon new` for all real work. Flags are only for quick
throwaway stubs: `bon new "Fix typo" --why w --what x --done d -q`

```bash
cat <<'EOF' | bon new -q
{
  "title": "API stays responsive under peak load",
  "parent": "bon-zovili",
  "brief": {
    "why": "Load tests show 5s P99 at 200 RPS — users are dropping off",
    "how": "Redis distributed locks, not file locks. Don't modify auth middleware.",
    "what": "1. Add rate limiter middleware 2. Configure per-endpoint limits 3. Load test at 500 RPS",
    "done": "P99 < 500ms at 500 RPS sustained for 10 minutes"
  }
}
EOF
```

The JSON path honours `title`, `type`, `parent` (or `outcome`), `area`, `waiting_for` and `brief` — brief fields may also be given flat. `waiting_for` (a string or a list) lets an action be born blocked: `"waiting_for": ["bon-abc", "external review"]` creates it already waiting, and it may sit flat or inside `brief` (bon-pidajo — three items were born open when the nested form was silently dropped, 2026-09-14). Any other key is a hard error, never a silent drop — including a structural key such as `title` or `area` placed inside `brief` — the same contract as `bon edit`.

**Standalone actions** — for field reports, one-off fixes, observations — use `type: "action"`:

```bash
cat <<'EOF' | bon new -q
{
  "type": "action",
  "title": "Field Report: OAuth flaky under concurrent load",
  "brief": {
    "why": "Noticed 3 failures in 10 test runs under load",
    "what": "Document the pattern, identify root cause",
    "done": "Either fixed or filed as action under appropriate outcome"
  }
}
EOF
```

### When to Track vs Just Do

| Track in Bon | Just do it |
|-------------|------------|
| Multi-session work | Quick single-step action |
| Work needing handoff to future Claude | Research / exploration |
| Complex outcomes with multiple actions | Trivial fix (typo, config tweak) |
| Anything with approach worth preserving | Side quest done in minutes |

---

## Mid-Session Transitions

Between actions:
1. Complete current action: `bon done <id>`
2. Run `bon list --ready`, capture to file, Read and output
3. Draw-down the next action before starting

---

## Session Close

Use `/close` at session end. It handles reflection, handoff, and capture.

---

## Outcome Language Coaching

Outcomes describe what will be true, not work to be done. The CLI warns on activity-verb titles automatically.

| Activity | Achievement |
|----------|-------------|
| Implement OAuth | Users can authenticate with GitHub |
| Build rate limiter | API stays responsive under peak load |
| Add test coverage | Claudes don't hit surprising edges |

**Don't coach on actions.** Actions *should* be activity language.

---

## Core Commands

```bash
bon init --prefix myproj     # Initialize .bon/ with prefix
bon list                     # Hierarchical view
bon list --ready             # Actions with no blocker
bon list --group-by area     # Cluster by Area of Focus ((ungrouped) last); --area X filters to one

bon show ID                  # Full details including brief
bon show --current           # Active tactical steps
cat <<'EOF' | bon new -q                             # Pipe JSON to stdin (default)
{"title":"...","parent":"...","brief":{"why":"...","how":"...","what":"...","done":"..."}}
EOF
bon new "Quick fix" --why W --what X --done D -q     # Flags: only for one-line stubs
bon done ID                  # Complete (unblocks waiters)
bon done ID --note "reason"  # Complete with context
bon wait ID REASON           # Mark waiting (clears tactical!) — APPENDS to existing blockers, prints the resulting list
bon wait ID REASON --replace # Overwrite ALL blockers with this reason (correcting a stale one)
bon unwait ID                # Clear waiting (or one blocker: bon unwait ID BLOCKER)
bon unwait ID --note "..."   # Record WHY the block lifted (met/abandoned/decided against) — survives as released_note
bon work ID                  # Init tactical from --what
bon work ID "step1" "step2"  # Init with explicit steps
bon work --status            # Current tactical state
bon work --release           # Hand back the claim, KEEP the progress (resume with `bon work ID`)
bon work --clear             # Clear without completing (discards the progress)
bon step                     # Advance to next step
bon step --expect N          # Advance with CAS guard — refuses if the board moved (use the printed N)
bon step --skip "reason"     # Skip current step
bon step --no-complete       # Final step: don't auto-complete
bon edit ID --title/--why/--how/--what/--done/--note/--order  # Edit fields
printf '%s' '{"how":"..."}' | bon edit ID    # JSON stdin — only the keys present change
bon edit ID --how ""         # Clear how field
bon edit ID --note "..."     # Repair a closing note (done items only)
bon edit ID --parent NEW     # Move action to another outcome ('none' = standalone)
bon convert ID               # Action → outcome, or outcome → standalone action
bon convert ID --outcome P   # Outcome → action under P (demote + re-home in one move)
bon restore ID               # An item vanished from a JSONL board? Bring it back from git history — never hand-edit items.jsonl
bon move ID --to REPO        # Move to another repo's board (path or ~/repos name);
                             # filed where you're cd'd ≠ where it belongs — move is cheap

bon status                   # Overview counts
```

All commands support `--json` for output. `bon new` reads JSON from piped stdin by default — no flag needed. `bon new` supports `-q` (quiet, prints ID only).

---

## JSON Field Reference

**`bon show ACTION --json`** returns:
```json
{
  "id": "bon-muvuri", "type": "action", "title": "...",
  "brief": { "why": "...", "how": "...", "what": "...", "done": "..." },
  "status": "open", "parent": "bon-zovili",
  "waiting_for": null, "tactical": { "steps": [...], "current": 0, "session": "..." }
}
```

`how` is `null` in JSON output when not set. Absent from stored data when not provided.

**Field-name mapping:**

| Instead of | Use |
|---|---|
| `item["why"]` | `item["brief"]["why"]` |
| `item["how"]` | `item["brief"]["how"]` |
| `item["done"]` | `item["brief"]["done"]` (not `item["done_at"]`) |
| `item["parent_id"]` | `item["parent"]` |

**JSON shape contract:**
- `bon list --json` → `{"outcomes": [...], "standalone": [...]}`
- `bon show ID --json` → single object (use `.field` not `.[0].field`)

---

## Quick Corrections

| What you typed | Use instead | Why |
|---|---|---|
| `bon add "title"` | `bon new "title"` | `add` isn't a command |
| `bon work OUTCOME_ID` | Pick an action | `work` is for actions only |
| `bon step` (at session start) | `bon show --current` first | Check for active tactical |
| `bon done ID --resolution "text"` | `bon done ID --note "text"` | `--resolution` doesn't exist |
| Recreate item under new outcome | `bon edit ID --parent NEW` | Re-parenting is one edit, not a copy-and-close dance |

### Shell Escaping

**For creating items:** Pipe JSON to `bon new` with a heredoc for anything with special
characters (quotes, backticks, parentheses). Flags are only for quick stubs.

**For reading items:** When piping `bon --json` output through inline python, use `python3 -c` (script as an argument) — **not** a heredoc:

```bash
bon list --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for o in data['outcomes']:
    if o['status'] != 'done':
        print(o['id'])
"
```

`python3 -c '…'` keeps stdin pointed at the pipe. `bon list --json | python3 <<'PYEOF' … PYEOF` is **broken**: the heredoc claims stdin, so python reads its *script* from there and the piped JSON never arrives — `json.load(sys.stdin)` then reads empty and raises. (If a heredoc is unavoidable, write the JSON to a file first and `json.load(open(path))`.)

### Creating Multiple Items

Create sequentially, not in parallel tool calls. If one fails, Claude Code cancels all sibling calls.

Pipe JSON to `bon new` for each item — clean heredocs with no escaping concerns:
