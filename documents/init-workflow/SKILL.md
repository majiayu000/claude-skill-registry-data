---
name: init-workflow
description: >
  Bootstraps and validates the AI workflow in a project that has this
  plugin installed: scaffolds whichever project-owned files are missing,
  detects the project's commands, fills AGENTS.md, points it at
  review/planning guidance (seeding docs/agent-rules/ or reusing an
  existing doc), and verifies the review gate. Re-run any time as a
  doctor — it reports what is missing or drifted. (Named init-workflow so
  it does not collide with Claude Code's built-in /init command, which
  generates a CLAUDE.md.)
---

# /init-workflow — Bootstrap and Validate the Workflow

Run this skill inside a project once this plugin is installed. It
scaffolds whichever project-owned files are missing from this skill's
bundled templates — independently of one another, so a project can already
have its own `AGENTS.md`, its own `CLAUDE.md`, or none of it — then fills
them with *this* project's facts, interactively, and verifies the setup end
to end. It is idempotent — re-run it after a plugin update or whenever
setup drift is suspected, and it acts as a doctor, reporting what is
missing rather than redoing what is already filled.

**Division of labor:** this skill scaffolds, adapts, and validates
project-owned files. It never edits the plugin's own mechanism — the
skills, sub-agents, and the plugin's own documentation are off limits;
updates to those come from updating the plugin itself, not from this skill.

**Ground rules:**

- **Propose, then write.** Every value you detect is a proposal until the
  user confirms it. Batch the confirmations (one round for the initial
  scaffold, one for commands, one for AGENTS.md sections, one for review
  and planning guidance) instead of asking one question at a time — Step 4's
  own "do you already have docs?" question is a separate, necessarily-first
  round of its own, since it decides what the rest of that step even asks.
  Never invent facts about the project; where the user defers, leave an
  explicit `[TODO: …]` rather than a guess.
- **Keep `AGENTS.md` lean.** You are filling a map, not writing the
  territory — one line per command, one line per module, one bullet per
  sensitive area. Depth belongs in `docs/`.

---

## Step 1 — Scaffold if needed, then assess the current state

Every file under `${CLAUDE_SKILL_DIR}/templates/` maps to a
project-relative destination (this is the plugin's canonical enumeration —
see the file tree in the plugin's own documentation, kept in sync with this
directory by rule), **except** `docs/agent-rules/code-critic.md` and
`docs/agent-rules/plan-critic.md`, which Step 4 creates (or doesn't, if the
project already has equivalent docs) once it knows the answer; writing them
here too would leave an orphaned stub if Step 4 points elsewhere instead.
Check every other mapped file's destination on its **own** trigger — one
file's presence never gates another's, since a project can have
hand-written its own `AGENTS.md` long before adopting this plugin's review
gate, or vice versa:

- **Destination missing → scaffold it.** Strip the `.template` suffix from
  `AGENTS.md.template` and `CLAUDE.md.template` (landing at
  `AGENTS.md`/`CLAUDE.md`) and from `settings.json.template` (landing at
  `.claude/settings.json`, **not** project root) — on the destination copy
  only; never strip it on the source inside `templates/` itself, since an
  un-suffixed `AGENTS.md`/`CLAUDE.md` left there would be auto-loaded by
  Claude Code as this project's live guidance instead of a template. Copy
  every other file (the rest of the `docs/` tree) to the same relative
  path it has under `templates/`.
- **Destination exists as plain content** (`AGENTS.md`, `docs/adr/*`,
  `docs/product-context/*`) → leave it untouched and list it as "already
  present" in Step 6's report — never overwrite a file the project
  already owns.
- **Destination exists but needs special handling** (`CLAUDE.md`,
  `.claude/settings.json`, `githooks/pre-push`, `scripts/review-ok.sh`,
  `scripts/check-hook-status.sh`) — see immediately below.

**`CLAUDE.md`.** If it exists (e.g. from Claude Code's own `/init`) and
doesn't already contain `@AGENTS.md`, offer to append the import line —
never overwrite it with the template's version, and never append if the
import is already there (avoids a duplicate on a project that deleted
`AGENTS.md` but kept `CLAUDE.md`). If the user declines, report it in
Step 6 as a gap: `CLAUDE.md` won't load `AGENTS.md`'s guidance into Claude
Code.

**`.claude/settings.json`.** A merge target, not a copy target — a
project-scope plugin install can create this file (recording the install
itself) before `/init-workflow` ever runs, so "already exists" here is a
common case, not the exception. If it exists, read it and propose adding
whichever of `${CLAUDE_SKILL_DIR}/templates/settings.json.template`'s
`permissions.ask`/`permissions.deny` entries aren't already present,
preserving everything else the file already has — never a flat overwrite.
If it doesn't exist, scaffold it directly from the template. If the
existing file doesn't parse as JSON, its root value isn't an object, or
`permissions`/`permissions.ask`/`permissions.deny` are present but not the
expected shape (an object, and two arrays), do not attempt a merge and do
not guess a fix — flag it as an unresolved item in this step's proposal
(the same way a hook conflict is flagged) and continue with the rest of
Step 1; a malformed pre-existing file on this security-relevant path needs
the user's own eyes, not an agent's improvised repair.

**`githooks/pre-push`, `scripts/review-ok.sh`, `scripts/check-hook-status.sh`.**
Two separate questions. The first is decided here and, once the step's
proposal is confirmed, written as part of that same single confirmation
round below — never before the user confirms. The second is evaluated
only *after* that write (or after the user declines it), as the first
thing in "continue below" once Step 1's proposal is confirmed and
written — never before, since its verdict is only meaningful against the
settled state, not a proposal still awaiting confirmation.

**1. Is each of the three files, if it already exists, actually this
gate's own file?** Check each independently: `githooks/pre-push` and
`scripts/review-ok.sh` each count as ours if their content references
`.review-passed`; `scripts/check-hook-status.sh` counts as ours if its
content references `DEST_FOREIGN` (a verdict string that appears only in
that script — unlike `.review-passed` or `READY_TO_CONFIGURE`, both of
which also appear in `scripts/review-ok.sh`'s own logic, so neither is
unique enough to use here). This pair is not perfectly symmetric —
`check-hook-status.sh` necessarily contains the literal string
`.review-passed` too, since checking for that marker is its job — so a
contrived case (someone's `check-hook-status.sh` content placed at
`githooks/pre-push`) would misidentify as ours; accepted as a known,
low-probability gap rather than solved here.

- Any of the three is **missing** → scaffold it from the template,
  preserving the executable bit.
- Any of the three **exists but isn't ours** → a real conflict, not a
  benign "already present." Surface it explicitly and ask the user how to
  proceed: replace it with the template's version, or explicitly decline.
  For `githooks/pre-push` specifically, do **not** offer to chain the
  template's check into the existing script — a pre-push hook reads its
  ref list from stdin exactly once, and a naively chained script can
  silently consume it before the gate's own `while read` loop runs,
  producing a hook that exits 0 on every push with no error. A declined
  conflict is an open gap Step 6 must call out by name.
- Any of the three **exists and is ours** → leave it as is (Step 5 item 1
  checks it's still executable).

**2. Once question 1 has been written (or declined), is the gate actually
wired up?** Don't hand-roll it: run
`${CLAUDE_SKILL_DIR}/templates/scripts/check-hook-status.sh` — the
plugin's own read-only copy, safe to run regardless of whether question
1's write happened, since a declined or not-yet-scaffolded
`githooks/pre-push` shouldn't stop this check — from the project root, and
act on its one-line verdict:

- **`ACTIVE`** or **`NEEDS_CHMOD`** — already wired up (the second just
  needs `chmod +x`, safe since the marker already identifies it as this
  gate's file). Nothing else to do.
- **`READY_TO_CONFIGURE`** — `githooks/pre-push` is ready but
  `core.hooksPath` isn't wired to it. On a fresh project this is the
  ordinary, expected state right after question 1's scaffold — offer
  `git config core.hooksPath githooks` as the natural next step, not a
  special case.
- **`DEST_NEEDS_CHMOD`** — `githooks/pre-push` exists and is ours but
  isn't executable; offer `chmod +x`.
- **`UNCONFIGURED`** or **`DEST_FOREIGN`** — if question 1's proposal for
  `githooks/pre-push` was declined, this is that same gap, already in
  Step 6's report — don't report it a second time. If question 1 was
  instead confirmed and written, this verdict is unexpected: the write
  didn't take effect as intended, and that itself is what to report (Rule
  2), not something to act on here.
- **`FOREIGN`** — something else entirely already claims the active hook
  slot (another hook manager, or `core.hooksPath` pointing at a directory
  that isn't this project's own `githooks/`). Do **not** offer to change
  `core.hooksPath` or replace anything; report exactly what the script
  printed and leave reconciling it to the human — including, if they want
  the two to coexist, that their existing hook would need to invoke
  `githooks/pre-push` itself with correct stdin handling, not something to
  draft on their behalf here.

Known limitation: `check-hook-status.sh`'s marker check is a presence
check, not a version check, so a stale copy from before a later plugin
update still reads as `ACTIVE`; that gap is accepted for now, not solved
here.

Also append `.review-passed`, `.qa-evidence/`, and `.workflow-log/` to
`.gitignore` if not already present (create the file if it doesn't exist)
— these are what the workflow writes locally and Step 5 checks for.

Known limitation: this step has no memory of a prior decline. A file the
user chose not to scaffold (e.g. a deleted `docs/product-context/README.md`
placeholder) is proposed again on the next run, since "destination missing"
can't distinguish "never created" from "deliberately removed." Confirming
"no" each time is the workaround until this needs solving properly.

Present the full proposal — files to scaffold, the `.claude/settings.json`
merge diff if any, the `CLAUDE.md` append if applicable, any hook or
settings conflict, and what's already present and left alone — in one
block for confirmation before writing anything, the same confirm-then-write
pattern as every other step here. Once confirmed and written, run question
2's gate-wiring check above and act on its verdict, then continue below.

Read `AGENTS.md` (whether just scaffolded or pre-existing). If it has a
**Review & Planning Guidance** section, read the files it names. A named
file that doesn't exist yet is not a Rule 2 failure to stop on here — it's
expected input to Step 4, whether `AGENTS.md` was just scaffolded (its two
entries default to `docs/agent-rules/code-critic.md`/`plan-critic.md`,
which Step 4 hasn't created yet) or pre-existing (a project adopting this
flow for the first time, whose named or default files may not exist
either); Step 5 item 7 decides separately, in whichever mode you end up in,
whether a still-missing file gets reported. Otherwise (no section at all)
check `docs/agent-rules/code-critic.md` and `docs/agent-rules/plan-critic.md`
directly. Classify each placeholder / `[TODO: …]` as filled or open,
**except** those under `## Task Tracking` — that section is optional, so
its placeholders never count toward the mode.

- Mostly open → **first-run mode**: continue with Steps 2–4, then validate.
- Mostly filled → **doctor mode**: skip to Step 5, then report only what is
  open or drifted (plus Step 5 item 8's two informational Task Tracking
  notes — its absent-section offer and its QA-finding-bullet fallback
  note — which are neither, by design).

## Step 2 — Detect the commands, propose, confirm

Inspect the project's build configuration — whichever exist:
`package.json` scripts, `Makefile`, `justfile`, `build.gradle(.kts)`,
`pom.xml`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`,
`docker-compose.yml`. From them, propose values for every entry in
`AGENTS.md` → *Commands*:

- build / run-all-tests / all-checks / dev server / stop / single-test
  example. Prefer wrapper commands (`make …`, npm scripts, `just …`) over
  raw tools — the wrapper may add environment setup the raw tool skips.
- app URL: from the dev-server config (port, host) if discoverable.
- default branch: `git symbolic-ref refs/remotes/origin/HEAD` (fall back to
  asking).

Present the full proposed Commands list in one block for the user to
confirm or correct. Flag any entry you could not derive — a missing stop
command or check command is common and worth an explicit decision (the
adversarial-qa and feature skills depend on them). After confirmation,
write the section, replacing the placeholders.

## Step 3 — Fill the remaining AGENTS.md sections

For each still-open section, draft from evidence and confirm before writing:

- **Project Overview**: draft one paragraph from the project's README and
  manifest (purpose, stack, key dependencies). Replace `[PROJECT_NAME]`
  in the title.
- **Architecture**: generate the top-level directory tree (source dirs
  only — skip vendored/build output) with a one-line purpose per module,
  inferred from its contents. Ask the user to correct wrong inferences —
  a wrong map is worse than no map.
- **Testing**: name the framework(s) found, where tests live, and how to
  run one (mirrors the single-test command).
- **Sensitive Areas**: propose candidates by scanning for the usual
  expensive-mistake surfaces — auth/session/token code, security config,
  route definitions, payment or billing flows, schema migrations, personal
  data fields and their rendering paths, secret/config loading. One bullet
  per confirmed area, naming a concrete file/package/pattern. This list
  gates three workflow decisions (critic-skip, reviewer model escalation,
  PR security flag) — an empty list disables those protections, so if the
  user has no time now, leave the TODO in place and say so in the report.
- **Rule 5** (project hygiene rule): ask whether one applies (e.g. reset a
  dev database at session end); fill it or delete the placeholder.
- **Task Tracking** (optional): ask whether the project uses an issue
  tracker (GitHub issues, Jira, Trello, …) that agents should file and
  update tickets in. If yes, fill every bullet — the exact command or tool
  call where the bullet asks for one, or `none` where the tracker lacks the
  concept (only the two QA-finding bullets treat a `[TODO:]` or `none` as
  "fall back to `gh`"; a project can use its own tracker for tasks and still
  fall back to `gh` for deferred QA findings specifically, by leaving just
  those two as `none`) — and confirm before writing. If no, delete the
  whole section (this is the only way to say "no tracker at all"; the two
  QA-finding bullets then fall back to GitHub issues via `gh`, and the rest
  simply don't apply) — it is not a gap to report.

## Step 4 — Seed review and planning guidance

`AGENTS.md`'s `Review & Planning Guidance` section takes exactly two
entries, labeled precisely `Code review guidance` and `Planning guidance`
(Step 5 and both skills key on these literal labels — do not paraphrase
them).

First ask: does this project already have docs for code review standards
and/or planning risk areas — a style guide, `CONTRIBUTING.md`, an
engineering handbook, anything like that? Handle each of the two
(code review guidance, planning guidance) independently based on the
answer:

- **Doesn't have one** → copy `${CLAUDE_SKILL_DIR}/templates/docs/agent-rules/code-critic.md`
  (or `plan-critic.md`) to the default path as the starting point — it
  already carries the Rules/Checklist structure, the build-enforced-rules
  doctrine, and the guidance comments; do not draft either file from
  scratch. Interview briefly to fill it in, then point `AGENTS.md`'s
  section at it:
  - Does the app hold personal data? Which categories are sensitive, and is
    there a compliance doc? Which surfaces are public/unauthenticated? Any
    identifiers public by design? Do any of the three privacy fitness tests
    already exist?
    → fill the *Privacy anchors* section of `docs/agent-rules/code-critic.md`.
  - Any hard constraints the team already knows agents get wrong (framework
    conventions, forbidden APIs, required registrations)?
    → add them as rules with severities, mirrored in the *Checklist* section.
  - What are this product's highest-risk areas — the places where a generic
    plan would miss something that matters here?
    → fill 4–7 lenses in `docs/agent-rules/plan-critic.md`.
- **Already has one** → point `AGENTS.md`'s section at that existing file
  instead of copying the template. Still ask the privacy/compliance
  question above for code review guidance specifically — `code-critic`
  binds its privacy rules to whatever `## Privacy anchors` section it finds
  in the named file (see that skill), so if the existing doc doesn't have
  one, it needs a home. Offer to append a `## Privacy anchors` section to
  the *end* of the existing file (same heading the template uses, so
  `code-critic` recognizes it the same way; clearly delineated as an
  addition, not a rewrite of the user's own doc) — on the user's explicit
  confirmation, since this edits a file they own that this plugin didn't
  create. If they decline, say so plainly in the Step 6 report: privacy
  anchors are not captured, and why. The hard-constraints and
  high-risk-area questions are framed as "anything not already covered by
  your existing doc" rather than a full draft, and only produce output if
  the user has something to add.

Then present the drafted content (whichever combination of copied/filled
files, appended sections, and `AGENTS.md` pointer updates applies) in one
block for confirmation before writing — the same confirm-then-write
pattern as Steps 2 and 3; an answered question is input to the draft, not
approval of it. It is fine for newly filled files to stay thin beyond what
the interview produced — they are designed to accrete (see *Evolving the
System* in the AI Workflow plugin's own documentation). Record only what
the user confirms; keep the guidance comments in newly filled files for
future additions.

## Step 5 — Validate the setup (doctor checklist)

Check each item and collect the results — fix only with the user's
confirmation, report what you cannot fix:

1. `githooks/pre-push` and `scripts/review-ok.sh` exist, are executable,
   and their content references `.review-passed`; `scripts/check-hook-status.sh`
   exists, is executable, and its content references `DEST_FOREIGN` (the
   same three identity markers Step 1 uses) — existence alone isn't
   enough; a foreign file at any of the three paths (see Step 1's identity
   check) would pass an existence check while enforcing nothing or
   behaving unpredictably.
2. The pre-push review gate is active. Run `scripts/check-hook-status.sh`
   (the project's own copy, confirmed genuine by item 1) and map its
   one-line verdict directly — this is the same script Step 1 and
   `scripts/review-ok.sh` itself use, so there is nothing left to
   hand-roll or re-derive here:
   - `ACTIVE` → pass.
   - `NEEDS_CHMOD` → offer `chmod +x` on the path the script printed (safe;
     the marker already identifies it as this gate's file).
   - `READY_TO_CONFIGURE` → offer `git config core.hooksPath githooks`.
   - `UNCONFIGURED`, `DEST_FOREIGN`, or `DEST_NEEDS_CHMOD` → item 1 should
     already have caught this (a missing or foreign `githooks/pre-push`);
     if it didn't, that's the actual gap to report — don't act on this
     verdict directly.
   - `FOREIGN` → do **not** offer to change `core.hooksPath` or replace
     anything; report exactly what the script printed and leave
     reconciling it to the human (see Step 1's note on why chaining isn't
     offered).
3. `CLAUDE.md` exists and contains `@AGENTS.md`.
4. `.gitignore` covers `.review-passed`, `.qa-evidence/`, and
   `.workflow-log/`.
5. `.claude/settings.json` has the `ask` rules for `scripts/review-ok.sh`
   and the `deny` rules for the push-bypass flags.
6. `AGENTS.md` → *Commands* exists as a section and has no unfilled
   placeholder remaining in it — a project whose hand-written `AGENTS.md`
   never had a *Commands* section at all has nothing to flag as
   "unfilled," but `/feature`, `code-critic`, and `adversarial-qa` all read
   it by role and will fail at runtime without it; treat a missing section
   the same as an unfilled placeholder (other sections may legitimately
   keep TODOs the user deferred).
7. `AGENTS.md` has a `Review & Planning Guidance` section with entries
   labeled exactly `Code review guidance` and `Planning guidance` — a
   renamed or paraphrased label is invisible to both skills, which key on
   the literal text, and silently falls back to the default
   `docs/agent-rules/` paths with no warning. Every file an entry names
   must also actually exist: a missing section (or one missing an entry)
   falls back to the default path if present; an entry that names a file
   which doesn't exist runs that skill on base standards/lenses alone (it
   does *not* fall back further to the default path) — either gap should
   be surfaced, not left to fail silently on the next review.
8. **Task Tracking** — informational only, never a validation failure; an
   absent section is a legitimate choice, not a gap. If `AGENTS.md` has no
   `## Task Tracking` section at all **and Step 3 did not already ask about
   it this run** (the guard that stops this item from immediately
   re-asking a question the user just answered "no" to in Step 3 of the
   same session — without it, a doctor-mode project that has never seen
   the question, and a first-run project that just declined it minutes
   ago, would be indistinguishable), note that it's available and offer to
   run Step 3's Task Tracking interview now, same confirm-then-write. If
   the section exists, validate it like any other: no remaining `[TODO:]`
   means configured; open TODOs are a deferral to report like any other
   section's — **except** on the two QA-finding bullets specifically,
   where a `[TODO:]` is, per the template's own comment, an intentional
   way to skip just those two and fall back to `gh`; treat it the same as
   `none` there — the documented fallback — and note it informationally,
   not as a deferral (Step 1 and Step 6 both carry this exception too, so
   neither reports nor re-offers it as one). Known limitation, same as
   Step 1's decline-memory one: this skill has no memory of a prior
   decline across separate runs, so a project that deliberately deleted
   the section in an earlier session (the documented way to say "no
   tracker") looks identical to one that was never offered it, and gets
   re-offered here every run. Confirming "no" again is the workaround
   until this needs solving properly.

## Step 6 — Report

End with a short summary: what was written (file by file, including any
`.claude/settings.json` merge or `CLAUDE.md` import append), what already
existed and was left fully untouched (plain-content skips, or a
pre-existing gate script correctly identified as already this gate's),
any declined append or unresolved hook/settings conflict from Step 1 or
Step 5 item 2, what was deliberately deferred (the open TODOs and what
they disable, other than Step 5 item 8's QA-finding-bullet fallback note,
which is not a deferral), the doctor checklist results, and the suggested
next action — typically committing the setup changes, then starting the
first feature on a fresh branch with
`/feature`. For each item still open — including deferrals found in doctor
mode, but **excluding** Step 5 item 8's two informational notes (its
absent-section offer, already made — and, if accepted, already acted
on — inside Step 5 itself, and its QA-finding-bullet fallback note, which
is not a deferral) — offer to run the relevant step (2–4) for just that
item now, so deferred TODOs are re-offered on every run rather than
silently carried forward. Do not
commit or push yourself unless the user asks — setup
changes deserve the user's own review. (If asked to push, Rule 4 in
`AGENTS.md` applies as always: code-critic pass, then `scripts/review-ok.sh`.)
