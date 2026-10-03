---
name: docs-architecture-setup
description: Use when bootstrapping or standardizing a project's documentation for AI navigation — a new project, or an existing one with no CLAUDE.md router, scattered/missing docs, or inconsistent ARCHITECTURE/ROADMAP. Also when onboarding a project into a portfolio that shares a doc convention.
---

# Docs-architecture setup

Bootstrap a project so an agent navigates it the same way as every other: one always-loaded
`CLAUDE.md` **router** pointing to a canonical, **charter-guarded** doc set. Carry the set as a
rule — never infer it from sibling repos. *(A sibling may not exist; inference drifts between
projects.)*

## Safety — restructure, never destroy (highest priority)
- **S1.** Consolidating = **merge** (drop nothing); moving history = **move**, not delete;
  renames preserve content. Unsure whether something is still needed → move it to `archive/`,
  never delete.
- **S2.** Apply on a **clean git tree** (commit first) and **present the diff for review before
  committing**. *(Every change stays recoverable.)*
- **S3.** Not a git repo? **Create the net first**: `git init` + commit the originals (or
  snapshot them to `archive/pre-setup/`) *before* any restructuring — never merge-and-delete on
  an unversioned tree. A pure-scaffold run (new files only) may proceed, noting the tree is
  unversioned.
- **S4.** A large/diverse project (many existing docs) deserves extra care: survey fully before
  touching anything; prefer several small reviewed applies over one big one.

## The enforced set — create every file, charter-guarded
| File | Role |
|---|---|
| `CLAUDE.md` | always-loaded **router** + load-bearing gotchas (kept thin — enforced by S7) |
| `ARCHITECTURE.md` | subsystem mechanics (how it works) |
| `ROADMAP.md` | forward-looking design + a short "Recently shipped" digest |
| `NOTEBOOK.md` | running **lab notebook** (chronological empirical findings); past its budget its oldest days roll into `NOTEBOOK/` (T1) |
| `VERIFICATION.md` | how to verify a change — *even if* just "= `dotnet test` / `npm test`, CI at X" |
| `DOMAIN.md` | the human/strategy home (science / conventions / site-process / UI rules) |
| `docs/` | journal: per-topic dated records, `YYYY-MM-DD-<slug>.md` by default or the pattern the router's journal line states (B2) |
| `CHANGELOG.md` | **conditional** — shipped-history journal (append-only, dated, newest first); create when history accrues; rolls into `CHANGELOG/` like NOTEBOOK |
| `README.md`, `RELEASING.md` | **conditional** — public entry point; project that ships |

- **S5.** **Charter-guard:** every file opens with a one-line charter (purpose / when to read).
  A thin file states an honest status ("verification = the test suite"; "no subsystems yet") —
  **never blank**. *(Charter'd-thin is legible and a ready home; blank is noise. NOTEBOOK and
  VERIFICATION are the two files unguided runs reliably omit — create them.)*
- **S6.** The domain doc is **always named `DOMAIN.md`** — do not elicit a content-specific
  name; do not rename an existing `DOMAIN.md`. Whatever the content *is*, it lives there; when
  absent, create it charter'd-thin. Never skip it.
- **S7.** **Lean an encountered fat router in this run:** reference content inside
  `CLAUDE.md` — glossary, contract/API prose, conventions, subsystem mechanics: anything
  that is neither routing nor a load-bearing gotcha — **moves now** to its charter home
  (glossary / authoring conventions → `DOMAIN.md`; mechanics / contracts →
  `ARCHITECTURE.md`), as an S1 content-preserving move with a router pointer where needed;
  name each move in the run report. The trigger is **content, never size** — a gotcha-dense
  router stays, a small glossary still moves. A hybrid block **splits**: the gotcha line
  stays in the router, the reference body moves. B2's "never clobber" forbids overwriting an
  existing setup, **not** relocating its off-charter weight — "noted as a follow-up" is the
  job left undone. *(Unguided runs leave a 24 KB router fat and grow it; oversized routers
  load every conversation and degrade the harness — the why, never the trigger.)*

## Tiers & routing — teach these in CLAUDE.md
- **T1.** **journal** (dated capture) = `docs/YYYY-MM-DD-*.md` + `NOTEBOOK.md` +
  `CHANGELOG.md`, plus their **overflow directories** (`NOTEBOOK/`, `CHANGELOG/`): when a
  journal passes its budget (40 KB by default), its oldest whole days roll into a directory
  named for the file, one frozen file per period named by its first date, with an
  `INDEX.md` listing every rolled entry (the maintain skill's job, its M17; entries keep
  their text). Three-way split: small finding from doing the work → NOTEBOOK; **shipped
  unit → CHANGELOG**; substantial standalone record → `docs/`.
- **T2.** **reference** (current truth) = ARCHITECTURE / ROADMAP / DOMAIN / VERIFICATION —
  edited in place.
- **T3.** **cold-rationale** (optional) = lengthy *evergreen* "why" not needed for immediate
  reasoning → a dated `docs/` note + a one-line reference back. Extract only when lengthy AND
  cold AND evergreen (not code-coupled).
- **T4.** The router names reference docs **by name**; the journal **by convention**
  (`glob docs/*.md` + grep) — never an enumerated, growing list. The journal line states
  the dated-record pattern and that a dated citation ("NOTEBOOK 2026-01-22") resolves by
  grep over the journal and its overflow directory.

## archive/ and the changelog — do not blur
- **A1.** `archive/` = **archival-only**: not-current-design-relevant, deletable (git is the
  backstop). Routing test: *"still current-design-relevant?"* No → `archive/` (or just let git
  hold it); yes → it stays live.
- **A2.** **Shipped history lives in `CHANGELOG.md`** (journal tier: append-only, dated,
  newest first); `ROADMAP.md` keeps a short Recently-shipped **digest + pointer**; never a
  long history embedded in ROADMAP; never shipped history in `archive/`. Git remains the
  commit-level backstop. Relocating an embedded history = **move**, content-preserving (S1).

## Boundaries
- **B1.** **Hard scope-exclusions — never scaffold into:** vendored trees (`vendor/`,
  `third_party/`, forked upstreams), generated output (`bin/`, `obj/`, `dist/`, `target/`),
  tooling (`.claude/`, `openspec/`). Their own READMEs are not this project's docs; `CLAUDE.md`
  notes them excluded — for `openspec/`, the note marks archived design docs
  (`changes/archive/*/design.md`) as historical records the **maintain** sweep reads (still
  never scaffolded into, and never an authoring target for the T1 journal split).
- **B2.** **Coexist, never clobber:** augment an existing setup — don't overwrite a present
  `CLAUDE.md` / `openspec/` / `.claude/`. Normalize filenames to the **project's stated**
  dated-record pattern (the router's journal line; the default is `YYYY-MM-DD-<slug>.md`),
  align casing; never impose the default over a pattern the project states *(a rename
  breaks every citation of the file: S1's restructure-never-destroy reaches names)*.
- **B3.** A **sub-project** (nested tree with its own router / own `.git`) is its own
  governance unit: **flag-and-skip** — leave its docs alone, note it excluded in the root
  router, and report *"run this skill from `<sub-dir>` to govern it as its own unit."* *(Not a
  submodule/vendoring call — that's the user's separate decision.)*
- **B4.** A **container root** (the invocation dir holds no first-party project content — only
  sub-projects + tooling/exclusions) gets the **router plus at most two thin portfolio
  docs**, never the rest of the enforced set: an optional **portfolio `DOMAIN.md`**,
  chartered *cross-repo truth only* (shared glossary terms, cross-store disambiguations,
  cross-repo contracts by pointer), created when such truth exists — e.g. surfaced by the
  S7 lean — never by default; and an optional thin status/sequencing `ROADMAP.md`.
  **Owner rule:** what one project's code defines lives in that project's docs — the
  portfolio DOMAIN points *down* by name, sub-projects point *up* for shared terms,
  **never mutual**. *(Ownerless truth improvised into routers, status docs, or sibling
  pointers is how cross-repo loops form; per-project docs remain the truth for everything
  owned.)* Leaning a container router routes cross-repo reference prose here — not into
  ROADMAP, not kept as router prose (a one-line disambiguation gotcha may stay).
- **B5.** **Design-heavy / code-light:** a large standalone design doc **is the project's
  DESIGN slot** — keep it whole: charter it, route it by name, and scaffold the rest of the
  enforced set charter'd-thin pointing into it ("mechanics live in `<doc>` §N until code
  lands"). Its content graduates into ARCHITECTURE/ROADMAP as code arrives (a later MAINTAIN
  job). Never split, relocate, or archive it. *("Distributed then archived verbatim" still
  destroys the single living home.)*
- **B6.** A **container root's `.gitignore` names each nested repository** (`/alpha/`), each
  reason on its own line, and **never wildcards the root's directories** (`/*/` plus
  exceptions): a wildcard silently drops any new directory (an overflow directory first),
  and a kit copied from what is committed ships without it. On encounter a wildcard is a
  safety flag, rewritten by name in the run (content-preserving: the same directories stay
  out; git reads a comment only on a line of its own, a trailing one makes the pattern
  literal). *(Found the first time a journal rolled over under such a file.)*

## Procedure
1. **Survey** the tree: existing docs, the exclusions (B1), sub-projects (B3), and the
   container-root / design-slot shapes (B4 to B6).
2. **Create/align** the enforced set, charter-guarded (S5, S6).
3. **Write `CLAUDE.md`** as the router (T4; exclusions noted; load-bearing gotchas only).
4. **Don't force content** — thin-but-charter'd is correct for a new/sparse project.

Full rationale + RED/GREEN provenance:
https://github.com/Apoplectic1/YetAnotherSkillsRepo/blob/main/docs/docs-architecture-design.md
