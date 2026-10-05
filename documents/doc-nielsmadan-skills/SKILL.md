---
name: doc
description: "Assess documentation for gaps, staleness, quality, and files outside the defined doc set. Preserve useful knowledge in canonical docs, then remove superseded or unnecessary files. Check changed code when the tree is dirty, otherwise assess the whole repo. Explicit modes: --review, --update, --generate, or --session to capture durable knowledge from a conversation or transcript. Use for doc creation, cleanup, freshness, quality, or saving occasional manual test procedures and results whose numbers a later run will compare against; routine suite runs and ordinary QA passes do not need test records."
argument-hint: "[ (no args = context-aware assess) | --review | --update | --generate <target> | --session [--md <file>]] [--all | --staged | --unpushed]"
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Doc

Assess, review, update, generate, and prune documentation following consistent principles.

## Reference files (load what the run needs)

| File | Load when |
|------|-----------|
| `references/principles.md` | Writing, sizing, or judging docs — the 8 principles and the Minimal/Lean/Structured profiles. Assess needs it to pick a profile; review/update/generate to apply it. |
| `references/cleanup.md` | Assessing which docs belong, or applying a cleanup: extract useful knowledge, repair links, then remove the superseded files. |
| `references/mode-review.md` | `--review` |
| `references/mode-update.md` | `--update` |
| `references/mode-generate.md` | `--generate` |
| `references/mode-session.md` | `--session` |
| `references/manual-tests.md` | Capturing occasional manual tests, or generating/updating/reviewing `docs/tests/` |
| `references/generate-templates.md` | Writing a new doc from scratch |

Routing (below) does not need any of them.

## Which mode runs (read first)

**Bare `/doc` = context-aware assess.** It adapts its *scope* to git state but always runs
all four lanes (Generate / Update / Review / Cleanup) and never writes without a plan, it proposes,
then runs your picks.

- **Dirty tree (staged or unstaged changes) → "is what I just did documented?"** Center the
  assess on the changed files: are the docs covering them still accurate (**Update** lane),
  and does new behavior need a doc (**Generate** lane)? Add a quick whole-repo glance for
  structural gaps, obvious staleness, and docs outside the defined set so it doesn't
  tunnel-vision. Lead with the changed-files verdict. Staged wins; fall back to unstaged.
- **Clean tree → general review.** Whole-repo assess across all four lanes.

In either state, include uncaptured occasional manual tests from the current session in the
Generate lane. Running a test may leave no code diff; apply `references/manual-tests.md` to
decide whether it warrants a record.

**The guard that still holds** (this is why the skill used to force whole-repo): auto-scoping
to the diff is fine, but **never collapse into a single silent action and never skip the
Generate/structure or Cleanup question.** Dropping a lane, or writing without showing a plan, is the bug,
not the narrowing. If the changed files reveal a missing docs tree or a bloated instruction
file, that surfaces even on a one-file diff.

**Explicit flags override** the auto-scope and auto-mode:
- Scope: `--all` (force whole repo), `--staged` / `--unpushed`, or `<target>`.
- Mode: `--update` / `--review` / `--generate <target>` / `--session` force that action
  regardless of git state.

**Requests to “create/apply our standard doc format” are structural.** Assess the
repository's documentation against the current profiles in `references/principles.md`,
even when the tree is dirty or existing docs need updating. Propose the missing docs and
folders warranted by the chosen profile, folder moves, index/link repairs, and updates to
instruction references. Existing documents or legacy folders do not satisfy this request
by themselves. Use the assess plan-and-approval workflow, then create or migrate the
approved layout; reformatting one document does not complete it. A request explicitly
limited to formatting one document keeps that scope.

## Modes

All modes use code and session evidence according to each doc's lifecycle: current procedures
track today's code, while historical records describe the run or decision that produced them.

| Mode | Intent | Writes? | Default scope |
|------|--------|---------|---------------|
| **(no args) — assess** | Survey docs state, propose & run an action plan | No → plan, then runs your picks | **auto: changed files if the tree is dirty, else whole repo** |
| `--review [target]` | Assess accuracy / completeness / quality | No → findings, then interactive apply | context (or `<target>`) |
| `--update [target]` | Sync existing docs to current code | Yes — in place, replace stale parts | staged code, falling back to unstaged |
| `--generate <target>` | Create docs that don't exist yet | Yes — new files | the target |
| `--session [--md <file>]` | Capture durable knowledge, including occasional manual tests | Yes — after preview | current conversation, or the supplied transcript |

**Assess is the default** — it's what a bare `/doc` runs (see "Which mode runs"
above). It surveys, classifies, and routes into the matching modes and cleanup workflow. The
explicit modes are opt-in via their flag: `--review` and `--update` are the same
comparison (review reports and lets you pick what to apply; update applies
directly from a diff); `--generate` is for greenfield.

## Usage

```
/doc                              # Context-aware assess: dirty tree -> check the changes are documented; clean tree -> whole-repo review
/doc --all                        # Force a whole-repo assess even when there are uncommitted changes
/doc --staged                     # Assess, scoped to what staged changes touch (explicit)
/doc --review payments            # Review docs for a feature, then pick fixes to apply
/doc --review --all               # Review all docs (parallel agents)
/doc --update                     # Sync docs for staged code changes (end of a feature)
/doc --update auth flow           # Sync all docs for a feature/area
/doc --generate <target>          # Generate docs for file/module/feature
/doc --generate --staged          # Generate docs for staged code changes
/doc --generate --unpushed        # Generate docs for code changed across unpushed commits
```

Use `doc --session` to capture the current conversation, or `doc --session --md session.md`
for an exported transcript. This includes occasional manual test procedures and dated results.

## Gotchas
- `--update`/`--generate --staged` document uncommitted code that may change in
  review. If the code is revised but the docs are committed alongside, they drift.
- `--all` scope includes CLAUDE.md — the skill may propose edits to the project
  instructions file that governs its own behavior.
- **Consolidation includes removing the originals.** Load `references/cleanup.md` and
  name the files to retire and the destinations for their useful content in the plan.
  A cleanup item already approved by the user needs no second confirmation.
- **Not code-derived, not synced, and they don't count as a docs tree:** `docs/explain/`
  (the `explain` skill), `docs/product/` (`review-product`), and frozen `docs/superpowers/`
  (plans/specs). A repo whose only `docs/` content is `docs/superpowers/` is greenfield for
  assess. `docs/superpowers/` is gitignored scratch, harvest its decisions into ADRs then
  delete completed plans. By contrast `docs/features/` *is* `doc`'s.
- `docs/user/` is **NOT** frozen: it's the user-facing tree. `doc` keeps it accurate in
  human how-to format; agents don't auto-load it. Only a *published* docs site (outside
  `docs/`) is out of scope.
- `docs/decisions/` and `docs/log/` are **append-only**: `--update` never rewrites their
  bodies, only adds entries / fixes links. Superseding an ADR is the one sanctioned edit —
  flip its `**Status:**` line and link forward to the replacement, never touch the body
  (see Doc lifecycles in `references/principles.md`).
- `docs/reference/` is **externally anchored**: a source-scoped `--update` skips it, because
  our refactor cannot make it stale. It goes stale when a *dependency version* moves, and a
  verified claim is only re-stamped by re-running its probe.
- `docs/tests/` is for **occasional manual operations whose results a later run will compare
  against**, performance tests above all. Procedures are live; dated `runs/` records and
  evidence are historical. Apply `references/manual-tests.md`; routine automated suite runs
  and ordinary feature QA passes do not belong here.

## Assess Mode (default)

The no-args entry point. Use it when you don't know what the docs need: it
surveys the current state, classifies what's required, hands you a prioritized
action plan, then runs the parts you choose by delegating to the other modes.
It never writes without your go-ahead — the plan comes first.

### Workflow

1. **Survey the landscape.** Separate the **two doc layers** — they're assessed
   differently and conflating them is the classic mistake (a repo with a README
   looks "documented" when it has no real docs tree):
   - **Ad-hoc top-level docs** — `README.md`, `CLAUDE.md`, `AGENTS.md`. Nearly
     every repo has these; their existence does **not** mean the project has a
     docs tree.
   - **Structured `docs/` tree** — `docs/features/` (what it does), `docs/tech/`
     (how it's built), `docs/decisions/` (ADRs), with `overview.md` indexes. This
     is the layer `--update`/`--generate` maintain. (`docs/features/` was formerly
     `docs/prd/`; it absorbs any legacy `docs/prd`, `docs/api` behavior.)
   - **External reference — `docs/reference/`:** how the *dependencies, platforms and APIs
     we build against* behave — verified findings stamped with date + version, and the
     upstream links. Doc-owned and maintained, but anchored to external things rather than
     to our code. Orthogonal to the profile (see "External reference" in
     `references/principles.md`), so a repo can warrant one at any size.
   - **Occasional manual tests — `docs/tests/`:** repeatable procedures and dated run records,
     including performance measurements. Assess procedures as living docs and runs as historical
     evidence; do not count accumulated runs toward the living-doc count or profile complexity.
   - **User-facing tree — `docs/user/`:** verbose human how-tos, README-linked, its
     own audience/format (see "Two audiences" in `references/principles.md`). Part of the
     project's docs, kept accurate when behavior changes, but not the terse agent-facing
     structured layer and not agent-loaded by default.
   - **Owned elsewhere / frozen — do NOT count as the structured layer:**
     `docs/explain/` (the `explain` skill), `docs/product/` (`review-product`),
     and frozen planning artifacts like `docs/superpowers/` (plans/specs). Their presence
     does **not** make a project "documented" — exclude them from the living-doc count
     and code-sync review; inventory completed scratch separately for Cleanup.
   - Inventory documentation in `docs/`, at the repo root, and in other documented
     locations, including legacy folders and completed scratch. Classify ownership and
     lifecycle before excluding anything; `references/cleanup.md` defines the retained set.
     Count living docs separately from historical records and other owners' files. Sketch
     the code surface worth documenting: top-level modules, features, services,
     APIs.
   - For a large tree (>~15 docs or a big codebase), fan out — one sub-agent per
     check in step 2 — and merge. Workers return verdicts without editing files.
     Disable delegation tools where supported; any coordinating role needs explicit
     subtasks, a descendant limit, and a stopping condition. Apply approved writes and
     removals after merging the findings; keep cross-file migrations with one owner.

2. **Run all four checks and reach a verdict for EACH lane.** Never silently
   skip a lane: if a lane has nothing, say so *and why* (this is what stops
   assess from quietly collapsing into "just review the existing docs").
   - **Gaps → Generate.** *The lane most often missed.* First answer the
     structure question, then pick the **doc profile** that fits the repo — load
     `references/principles.md` for the selection test and default to the smallest
     that covers it:
       - **Minimal** → lean `AGENTS.md` only; record it as **considered and skipped, with
         the reason**, don't just omit it.
       - **Lean** (the default) → `AGENTS.md` + bridge, `docs/decisions/`, a *handful* of
         `docs/<flow>.md`.
       - **Structured** → adds `docs/features/` + `docs/tech/`, only when the complexity test
         is met (not loc). Don't reach for it just because the app "has multiple modules" —
         nearly every app does.
     If the repo **already has a tree heavier than its profile warrants** (Structured on a
     small/simple repo, especially if it's drifting), that is itself a Generate/structure
     finding: **propose the smaller target structure**, with migrations and removals
     listed in Cleanup. Don't rubber-stamp an over-sized tree just because it exists.
     Then check for an **external-reference gap**: knowledge about a dependency, platform,
     harness or external API that this repo keeps re-establishing — a quirk that cost an
     experiment to find, a version-specific behavior, a contradiction with upstream's docs,
     something the session or git history shows being looked up more than once. That belongs
     in `docs/reference/`, not in `tech/`, and is warranted by the three-part test in
     `references/principles.md` rather than by repo size. Correct-usage conventions for a
     single library are **not** this — they belong to `library-docs` / `library-use`.
     Also check the **instruction file itself** (Principle 8 in `references/principles.md`):
     is `AGENTS.md`/`CLAUDE.md`
     bloated with derivable/enforceable content or over ~200 lines? That is a Generate/
     Review gap in its own right. Then the ordinary gaps: source areas with no doc,
     genuinely missing indexes. Don't over-reach to one-doc-per-file; when unsure between
     two profiles, propose the smaller and say why.
   - **Staleness → Update.** Living docs whose code changed after the doc was last
     touched (`git log -1 --format=%cd -- <doc>` vs recent commits to the code
     it covers), and docs referencing files / `file:line` / symbols that no
     longer exist.
   - **Quality → Review.** A light principles pass: local paths, restated
     signatures, verbatim duplication, placeholders/TODOs, missing required
     sections.
   - **Outside the defined set / redundant → Cleanup.** Apply `references/cleanup.md`:
     establish the retained doc set from project rules and the chosen profile, then
     inspect extra files for useful knowledge. List each source, what to extract, its
     canonical destination, and the original to remove. Include legacy buckets, redundant
     docs, integrated session harvests, and completed scratch plans. Reach a verdict even
     when the profile stays the same; cleanup is needed whenever extra files remain.

3. **Report state + action plan.** Always emit *this* assess report (titled
   **Docs Assessment**) — not a plain "Documentation Review". Reviewing existing
   docs is only the Quality lane; it must never replace the Generate (structure/
   gaps), Update (staleness), and Cleanup lanes. One categorized, sequentially-numbered
   list, with **every lane present even when empty**:
   ```markdown
   ## Docs Assessment: {repo/scope}
   State: {top-level docs: README/CLAUDE/AGENTS present?} · {instruction file: AGENTS.md/CLAUDE.md — ~N lines, lean / bloated} · {current profile: Minimal / Lean / Structured / none} · {N living docs · overview index present/missing}

   ### Generate (missing / structure)
   1. {e.g. "Small app, no docs/ tree — recommend Lean profile: AGENTS.md + docs/decisions + 1-2 flow docs" OR "AGENTS.md is 340 lines with restated dir layout — trim to lean" OR "Considered a docs/ tree — skipped: single-purpose repo, Minimal profile covers it"}

   ### Update (stale)
   2. {doc} — {code changed / broken ref / dependency bumped past a verified claim's version}
      (or: "none — docs match code")

   ### Review (quality)
   3. {doc} — {issue}   (or: "none — checked, conforms")

   ### Cleanup (outside the defined set / redundant)
   Retain: {chosen profile, canonical destinations, and protected or separately owned docs}
   4. {source} → {useful knowledge + destination, or reason nothing needs preserving}; remove {original path}
      (or: "none — every in-scope doc belongs to the defined set and has a distinct purpose")

   ### Healthy
   - {what's already fine — so the user knows it was checked}
   ```
   Number actionable findings sequentially across tiers so the user can select by number.

4. **Offer to execute.** Ask which to run (numbers, `all`, or `none`;
   multi-select where supported). Each selection runs the matching mode — load that
   mode's reference file and apply it to the target; Cleanup selections use
   `references/cleanup.md`. Keep each extraction and its source removal in one action.
   `none` → stop. An existing approval of the plan authorizes its full execution;
   do not ask again for the listed removals.

### Scope

**Auto-scopes to git state** (see "Which mode runs"): a dirty tree centers the assess on the
changed files (plus a whole-repo glance); a clean tree assesses the whole docs tree + key
source. Override with `--all` (force whole repo), `--staged` / `--unpushed`, or a `<target>`
(one feature/area).

## Examples

**Not sure what the docs need — just triage them:**
> /doc

Surveys `docs/` and the code surface, then reports a numbered plan: which areas have no
docs (Generate), which docs are stale vs the code (Update), which have quality issues
(Review), which extra files to extract and remove (Cleanup), and what's healthy.
Asks which to run and executes your picks in place.

**Bring a legacy docs tree into the defined set:**
> /doc --all

For a Lean repo with `docs/api/`, `docs/prd/`, and an integrated session harvest,
proposes retaining the needed flow docs and ADRs. After approval, merges useful behavior,
rationale, and gotchas into those destinations, repairs links, and removes the superseded
files. Reports preserved historical records and any unresolved candidates separately.

**Sync docs after finishing a feature:**
> /doc --update

Maps staged code changes to the docs that describe them and rewrites those sections in
place to match the new behavior. Run it while you still have the build context.

**Review a feature's docs and pick fixes:**
> /doc --review payments

Reviews every doc covering payments against the current code, lists numbered findings by
priority, then asks which to apply.

**Generate docs for a new service module:**
> /doc --generate lib/services/notification_service.dart

Reads the service, generates a module doc, ensures the index exists, and adds the
update-trigger note to the project's instruction file.

## Troubleshooting

### Assess proposes documenting the entire codebase on a fresh repo
**Cause:** Greenfield triage over-reaching. **Solution:** Assess should pick a
*starter set* — root `overview.md` plus the few highest-value modules — not one
doc per file. If it listed everything, narrow to the entry points and core
modules; the rest follows as those areas are built.

### Assess only reviewed the existing docs and never considered creating a `docs/` tree
**Cause:** Top-level docs (README/CLAUDE/AGENTS) — or frozen `docs/superpowers/`
artifacts — made it conclude "docs exist, just check them," collapsing into a
plain review and skipping the **Generate** lane. **Solution:** Assess must reach
a verdict on *every* lane, including the structure question. A README is not a docs
tree; frozen plan/spec artifacts don't count. If assess output is titled
"Documentation Review" rather than "Docs Assessment," it ran the wrong mode — re-run
bare `/doc`.

### Assess flags a doc as stale that's actually fine (or misses a stale one)
**Cause:** Staleness is a heuristic (doc edit time vs code change time, broken
refs) and can mis-fire. **Solution:** Assess only *proposes* — confirm before
running Update. For a definitive check, run `--review <target>`, which compares
the doc against the code directly.

### Consolidation wrote the new docs but left the old files behind
**Cause:** Treating migration as complete once the destination exists. **Solution:**
Finish the approved Cleanup items: verify the extracted knowledge, repair incoming links,
remove the superseded sources, and re-inventory the docs. Report any unresolved file and
the specific reason it remains.

## Notes

- All modes share the same principles and the compare-to-code engine.
- Bare `/doc` (context-aware assess) is the entry point when you don't know what the docs
  need. Reach for an explicit override when you already know the action: `--update` to force a
  sync, `--review` for a periodic human-facing audit, `--generate <target>` for one specific
  doc. Greenfield needs no flag, assess proposes the starter set on its own.
- Sub-agents parallelize large reviews/updates/generations (>5 files).
- Doctrine lives in one canonical place each: routing in "Which mode runs", everything about
  profiles, audiences, and lifecycles in `references/principles.md`.
