---
name: docs-project-management
description: "Universal, project-agnostic playbook for managing an ENTIRE project inside the repo's docs/ folder — the docs/-native system of record, reusable in any project, new or existing, with no external issue tracker. Defines WHAT it manages: the work-item TAXONOMY (Roadmap → docs/ROADMAP.md + docs/roadmap.json, PRD → docs/prd/, TRD → docs/trd/, Epic → docs/epics/, User Story → docs/user_stories/, Test Case → docs/test_cases/, Bug → docs/bugs/, per-session team reports → docs/sessions/, feature work-log → docs/reports/), the cross-document LINK GRAPH written as relative-markdown links (User Story part-of Epic; Test Case is-tested-by User Story; Bug blocks its story; PRD↔TRD), the YAML-frontmatter STATUS lifecycle + the bookend rule (transition status: forward before starting work, again when done), required frontmatter fields, the mandatory Test Case Template and the Bug+RCA report format, the TEAM WORK-REPORTING convention (one session folder per run; every agent bookends a start/completion report there + appends to its feature log), and the docs/ vs .ai_log/ split — durable records are committed markdown in docs/; .ai_log/ holds ONLY temporary git-ignored evidence (screenshots, run logs, scratch payloads, pipeline-state handoff JSON) passed by path and PROMOTED to docs/ if it turns out durable. Attached to EVERY agent."
---

TASKLANG
TYPE SKILL

IDENTITY "Docs Project Management (the docs/-native system of record)"
  > A universal, reusable playbook for running a whole project — requirements, planning, build
  > tracking, testing, bugs, and team reporting — as committed markdown inside the repo's `docs/`
  > folder. It works in ANY project, in any stack, from day one of a NEW project: no external issue
  > tracker, no ticket system, no proprietary tooling. A work item is a markdown file with YAML
  > frontmatter; a relationship is a relative markdown link; a status change is a frontmatter edit;
  > the full history is git.
  >
  > It does three jobs:
  >   1. WORK-ITEM MODEL — WHAT document types exist (PRD, TRD, Epic, User Story, Test Case, Bug,
  >      Roadmap), WHERE each lives, HOW they link, and HOW status is tracked.
  >   2. TEAM WORK-REPORTING — HOW every agent/contributor reports its work so anyone can see, in one
  >      committed place, everything that was done (who, what, when, with which evidence).
  >   3. DURABLE vs TEMPORARY — WHAT belongs in committed `docs/` versus the git-ignored `.ai_log/`
  >      temp-evidence folder, and when to promote content from one to the other.

---

## §1 Document types — WHAT the system manages

> Every work item is a committed markdown file in its `docs/` subfolder: descriptive kebab-case
> filename (never an opaque ID), YAML frontmatter for status/metadata, relative-markdown links for
> relationships. Full field-level detail: [[work-item-taxonomy]].

TABLE document-types
  COLUMNS: Type, Lives in, What it is / holds
  ROW: Project brief | docs/project_brief.md   | The product spec — the SOURCE OF TRUTH the whole project derives from; wins over any assumption
  ROW: Project config| docs/project_config/info.md | The single home for project-specific FACTS (product name, app name, stack, domain, scope, success scenarios) — agents read it instead of hard-coding facts
  ROW: Roadmap       | docs/ROADMAP.md + docs/roadmap.json | The milestone/release plan (human file) + a machine-readable MIRROR of every work item's current status (JSON cache, regenerated from docs/, committed)
  ROW: PRD           | docs/prd/               | Product Requirements Document — WHAT to build and WHY: objectives, in-scope / out-of-scope, testable acceptance criteria per success scenario
  ROW: TRD           | docs/trd/               | Technical Requirements Document — HOW to build it: architecture, data model, migrations, jobs, authz. Canonical TRD home; keep `index.json` (machine registry, one entry per TRD) + `index.md` (human index) beside the files
  ROW: Epic          | docs/epics/             | A large feature/theme grouping related User Stories; carries goal + scope + its story list
  ROW: User Story    | docs/user_stories/      | The smallest shippable requirement — "as a <user> I want <capability>" + numbered acceptance criteria; filename `NNN-<kebab-title>.md`
  ROW: Test Case     | docs/test_cases/        | A verification script for ONE behavior — numbered navigate→action→expected steps; filename `tc-NNN-<kebab-behavior>.md`; MUST follow the [[test-case-template]] and link its story "is tested by"
  ROW: Bug           | docs/bugs/              | A defect AND its Root-Cause-Analysis in ONE file — Symptom/Reproduction + 5-Whys RCA + Preventative Action at detection; Fix/diff/Resolved sections completed by whoever fixes it ([[bug-rca-report]]); `blocks` its story
  ROW: Session report| docs/sessions/<YYYY-MM-DD>-<slug>/ | Per-run team work folder — a README manifest + one bookended report per agent/phase ([[session-reporting]])
  ROW: Feature log   | docs/reports/feature-log.md + feature-log/ | The team work-log split by feature: one lean index row per feature, linking a per-feature file where each run appends a row

  RULES
    - Filenames: descriptive kebab-case, never opaque IDs. External refs (ticket numbers), when they
      exist, go in frontmatter + the title line — not the filename.
    - Each subfolder may carry a `template_<type>.md` seed; new items copy its shape.
    - Only APPROVED/final content advances status; drafts stay in their lifecycle state.

---

## §2 The link graph — HOW documents relate

> Every relationship is a labelled RELATIVE-MARKDOWN link in a `## Linked Documents` section, written
> in BOTH files (add the reciprocal link). No link-type IDs, no tracker mechanics — the label carries
> the semantic. Full table + exact syntax: [[link-graph]].

  - User Story **is part of** its Epic; the Epic lists it back (**realized by**).
  - Test Case ↔ User Story is ALWAYS **"is tested by"** (story side) / **"tests"** (test-case side) —
    never "relates to" or "part of".
  - Bug **blocks** the User Story it breaks; the story links the bug back.
  - PRD ↔ TRD cross-link (**specified by**); User Story is **derived from** its PRD.

---

## §3 Status lifecycle — HOW progress is tracked

> Status lives in each file's YAML frontmatter `status:` field; changing status = editing that field.
> Full lifecycle, required frontmatter fields, and the signature convention: [[status-lifecycle]].

LIFECYCLE status
  VALUES: backlog → ready → in_progress → in_review → qa → done   (blocked = orthogonal flag)
  > Pick the closest value per item type: a Bug walks open → in_progress → fixed → verified → closed;
  > a Test Case walks draft → ready → automated.

BOOKEND both-ends
  - ON START: set `status: in_progress` BEFORE touching the work; stamp `updated:`.
  - ON COMPLETION: set the next appropriate state (`in_review` / `qa` / `done`); stamp `updated:`.
  - NEVER leave a worked file on its old status — that is an incomplete bookend.

SIGNATURE
  - Sign every file update / report entry: `— <agent-name> v<version> (<passport-id>)`.

---

## §4 Team work-reporting — HOW work becomes visible

> One committed place per run where anyone can see all work done. Full layout, report schema, and
> per-role sections: [[session-reporting]].

  1. The orchestrator (or the first agent of a run) CREATES the session folder
     `docs/sessions/<YYYY-MM-DD>-<slug>/` with a `README.md` manifest (request, plan, a
     phase→agent→status→report table) and passes `session_dir` to every worker.
  2. EVERY agent bookends its run there — `<session_dir>/<phase-N>-<agent>.md`, created with a
     STARTING entry, updated on COMPLETION (work done, work items touched as links, evidence links),
     flipping its row in the session README.
  3. Each agent ALSO appends a run-row to its feature's log `docs/reports/feature-log/<slug>.md`
     (indexed by the lean `docs/reports/feature-log.md`).
  4. Reports carry the role-specific section: QA → coverage report; security → findings + verdict;
     devops → deploy/CI status; architect → gate verdict; PM → acceptance verdict.

---

## §5 `docs/` vs `.ai_log/` — durable vs temporary

> The one split that keeps context lean AND the record complete. Never confuse the two.

**`docs/` — durable, committed, the system of record.** Anything with lasting value lives here:
specs, decisions, work items, reports, audits, backlog/deferred-work notes, coverage summaries.

**`.ai_log/` — temporary, git-ignored, evidence offload ONLY.** The folder is tracked via
`.gitkeep`; its CONTENTS are ignored and therefore never committed — anything left only there is
effectively lost. Belongs in `.ai_log/`:
  - screenshots / diff images / browser captures taken as run evidence
  - run logs, test-run output, scratch files, intermediate payloads too big for context
  - the per-session pipeline-state handoff JSON (`.ai_log/session-<id>-<name>.json`) — the machine
    bus that carries key fields + PATHS between phases
  - naming: `.ai_log/<phase-N>-<agent>-<artifact>.<ext>`

  RULES
    - Hand off by PATH, never by inlining a blob into a prompt or a state file.
    - PROMOTE anything durable that lands in `.ai_log/` into the right `docs/` subfolder (with
      frontmatter + links) before relying on it — a decision or report parked only in `.ai_log/`
      does not exist as a record.
    - Reports in `docs/` may LINK to `.ai_log/` evidence, knowing it is ephemeral.

---

## §6 Adopting in a NEW project — bootstrap

CHECKLIST bootstrap
  [ ] Create the skeleton: `docs/{prd,trd,epics,user_stories,test_cases,bugs,sessions,reports/feature-log,project_config}/` + `docs/ROADMAP.md`
  [ ] Write `docs/project_brief.md` (the spec) and `docs/project_config/info.md` (the project facts)
  [ ] Create `.ai_log/` with a tracked `.gitkeep`; git-ignore its contents (`/.ai_log/*` + `!/.ai_log/.gitkeep`)
  [ ] Seed `docs/reports/feature-log.md` (empty index) and `docs/roadmap.json` (empty mirror)
  [ ] Drop a `template_<type>.md` into each work-item subfolder if you want enforced shapes
  > Nothing else is required — the model is just folders + markdown + frontmatter + relative links.

---

## The Map — load the one reference you need

> This SKILL.md is a MAP. Deep detail lives in atomized `references/` notes; load only what the task
> needs. Machine-readable nav: `maps/index.json` (+ `tags.json`, `links.json`, `manifest.json`).

TABLE references
  COLUMNS: Note, Owns, Load when
  ROW: [[work-item-taxonomy]]  | §1 detail — folder, filename pattern, owner per work item | You need a work item's folder, filename pattern, or owner
  ROW: [[link-graph]]          | §2 detail — every relationship's semantic, direction, exact syntax | Linking two work items / checking a relationship's direction
  ROW: [[status-lifecycle]]    | §3 detail — lifecycle values, bookend, required frontmatter fields, signature | Starting/finishing work, setting status, filling frontmatter
  ROW: [[test-case-template]]  | The mandatory Test Case Template (all fields) | Authoring/reviewing a docs/test_cases/ file
  ROW: [[bug-rca-report]]      | The Bug+RCA format — detection sections (Symptom/Repro/5-Whys/Preventative Action) + fix sections (Fix/diff/Resolved) | Authoring/completing a docs/bugs/ Bug file
  ROW: [[session-reporting]]   | §4 detail — session folder layout, report schema, role sections, feature log | Bookending your run as a report; organizing a session folder
  ROW: [[conventions-recap]]   | The non-negotiables checklist + the Knowledge Strategy | A one-glance rule check; rules for updating this skill

---

## Non-negotiables (one-glance)

CHECKLIST conventions
  [ ] Every work item = a committed markdown file in its §1 subfolder, kebab-named, frontmatter'd
  [ ] Every relationship = a labelled relative-markdown link, written reciprocally in both files
  [ ] Status bookended at BOTH ends by editing frontmatter `status:` — never left stale
  [ ] Test Cases follow the template AND link their story "is tested by"
  [ ] Bugs are one Bug+RCA file: detection sections at filing, fix sections completed by the fixer
  [ ] Every run bookends a report in `docs/sessions/<session>/` + a feature-log row
  [ ] Durable content in `docs/` (committed); ONLY temporary evidence in `.ai_log/` (git-ignored);
      promote anything durable that lands in `.ai_log/`
  [ ] No external tracker mechanics — everything is a local `docs/` file, linked by relative paths

---

## Knowledge Strategy
- Patterns to capture: recurring item shapes, link-graph edge cases, report sections that proved useful.
- Update permission: agents may freely add/update files in `references/`; changes to THIS SKILL.md map
  require user approval. Full strategy: [[conventions-recap]].

---

Made by **HasBrains** — https://hasbrains.com/
