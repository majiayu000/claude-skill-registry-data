---
name: product-card
description: >-
  Principal PM-posture skill that writes what a product turned out to be, once
  its foundation has settled — the project card's architecture-determined fields
  (Languages:, Language roots:, Test command:) and the product's README.md, both
  derived from the settled document set. Requires Principal PM posture (halts if
  invoked outside a principal-pm session or the principal-pm subagent). It runs
  after the FDR, ADR and NFDR have landed and before anything is built, and it is
  the step that makes the skeleton launcher runnable — product-skeleton reads the
  card this writes, so this runs first and never the other way round. Writes two
  files and nothing else: no code, no document under the product's docs/, and no
  skeleton. Use when a product's foundation step has settled and the card or the
  README has not caught up, when the card is missing Language roots: or Languages:,
  when a README still calls a defined product a proposal, or when someone asks to
  set a product up after foundation. Do not use for scaffolding a new project's
  management folder (project-stamp), placing the language frames (the
  product-skeleton launcher), the definition documents (product-prd, product-srs,
  product-uxd, product-sdd), the foundation records (product-fdr,
  product-architecture), or cutting seeds from them (seeds-from-product-docs).
license: MIT
metadata:
  author: Eyal Golan
  version: "1.3.2"
  created: "2026-09-05"
  category: product-definition
  tags: card, readme, principal-pm, foundation-step, language-roots, product-card
  risk: safe
---

# product-card

## Purpose

Write the two things a settled product still has not said about itself: **the project card's
architecture-determined fields**, and **the product's `README.md`**. Both are derived from the
document set the definition chain and the foundation step have already settled; neither carries a
judgment those documents did not make.

This file is the **orchestrator**: posture, path resolution, the two repositories, the gates and the
commit. **How to derive** — which documents win where they disagree, how each card field is read out
of the architecture, what a settled product's README may claim, and what to do with a field the
documents do not determine — is the authoring prompt
**`prompts/rich.md`**, applied at Step 3. Nothing in it is restated
here.

**It runs after the foundation step and before the skeleton.** The order is not a preference:
`<CORE>/launchers/product-skeleton/launcher.sh` reads `Languages:` at `:307` and `Language roots:` at
`:448`, both off the card this skill writes, so a skeleton run that precedes it places every frame at
the product root. Running the skeleton is not this skill's — see § *Critical rules*.

---

## Posture

**Principal PM role required.** If invoked outside Principal PM posture (neither a `principal-pm:`
session nor the `principal-pm` subagent), stop and say: *"product-card requires Principal PM
posture. Switch? (Open a session with the `principal-pm:` prefix, or run the `principal-pm`
subagent.)"* Do not shed the role. Where the **Principal PM** ends and the delivery-tier **PM**
begins is the Principal PM loader stack's to say; take the boundary from there.

---

## The two files, and the two repositories

| File | What this skill writes in it |
|---|---|
| `system/projects/<name>/project.md` | `Languages:`, `Language roots:`, `Test command:` — and nothing else on the card, comments included. A field the card lacks arrives as a whole line, its comment copied from the template. |
| `<Product path>/README.md` | the product's front door, corrected against the settled set. Created if absent. |

**These two can sit in different repositories, and usually do.** The card is in the instance repo —
the directory this session opened in. The README is in whatever repo holds the product. Resolve both:

- **`<instance-repo>`** — the session's own repo root. Every `system/…` and `.claude/…` path in this
  file resolves from it, and no step `cd`s away from it.
- **`<product-repo>`** — for a relative `Product path:`, this is `<instance-repo>` and the product is
  inside it. For an absolute one, `git -C "<Product path>" rev-parse --show-toplevel`, because a
  product with its own repo need not sit at that repo's root.

When the two are the same path, this run makes **one** commit. When they differ, it makes **two** —
one per repo, each staging only its own file. A commit cannot span repositories, and the alternative
to two commits is leaving one of the two files uncommitted, which is the state this skill exists to
end.

---

## Inputs and where they resolve

- **`system/projects/<name>/project.md`** — the card, and the binding. Its `Product path:` field
  resolves the product; every later `Product path:` in this file means that field. A placeholder or
  an unfilled value halts the run: both outputs resolve from it, and there is nowhere to write even a
  report of the gap.
- **The foundation set** — `<Product path>/docs/SDD.md`, `<Product path>/docs/adr/`,
  `<Product path>/docs/fdr.md`, `<Product path>/docs/nfdr.md`. **All four must exist: if any is
  missing at its resolved path, halt and name which.** This skill writes down what the architecture
  decided, and the foundation step is where it was decided; run before it lands, the derivation has
  nothing to read and the card would carry a guess.
- **The rest of `<Product path>/docs/`** — read it by **listing the directory**, not by recalling
  filenames. Whatever else is there is input the run is entitled to. Skip binary assets.
- **`system/projects/<name>/agari.md`** — the declared terminus. It bounds what the README may
  promise. Absent or still the stamped placeholder: record it in the report and derive best-effort;
  never halt.
- **`<CORE>/templates/project_template.md`** — the grammar of every card field, in that field's own
  inline comment.

---

## Workflow

### Step 1 — Identify the project, resolve the paths

**The argument is a project name, and nothing else.** Given a path, a product name, or a card, halt
and say what was wanted: the name of a directory under `system/projects/`. Identity in, file derived —
a caller who may pass either form makes the run guess which one it holds, and a product name and a
project name coincide often enough that the guess is usually right and silently wrong the once it
matters.

Read `system/projects/<name>/project.md`. Resolve `Product path:`, `<instance-repo>` and
`<product-repo>` per § *The two files, and the two repositories*. If more than one project exists and
the target is ambiguous, halt and report the candidates — nothing resolves without a project.

### Step 2 — Read current state, and check the inputs are on the record

Read every input named in § *Inputs and where they resolve*, in full, plus the README on disk if
there is one.

**The foundation set must be committed.** Run
`git -C "<product-repo>" status --porcelain -- <the four resolved paths>`; any output halts the run,
naming the file, for the owner to commit or discard it before re-running. The card and the README
become the standing facts every later run reads, so a card derived from an uncommitted SDD can be
traced to text the owner later discards.

Note each input's `Status:` line as you read it. The report carries them (the prompt's § *Inputs you
work from* says why they are reported rather than written into either output).

### Step 3 — Derive and write the two files

Apply the authoring prompt **`prompts/rich.md`**. It owns the
derivation entirely; this step adds only where the writing lands, which § *The two files* above
states.

**Edit the card in place, field by field.** Replace the value between `**Label:**` and the field's
inline comment, and leave the comment untouched — it is the field's grammar and the only statement of
what the field accepts. A field the settled set does not determine keeps the value it had.

**A field the card does not carry at all is added, not skipped.** A card stamped before the template
grew a field is missing its line entirely, so there is no value to replace — `Language roots:` is the
live case, and the frontmatter `description`'s trigger list already names it. When the settled set determines such a
field, insert the whole line at the position `<CORE>/templates/project_template.md` gives it relative
to the fields the card does carry, and copy that template's inline comment for the field **byte for
byte**; never compose one, because the comment is the field's grammar and this skill is not its
author. When the settled set does not determine it, add nothing and say so in the report: the only
reader of `Language roots:` skips a value it finds empty
(`<CORE>/launchers/product-skeleton/launcher.sh:449`, `if roots_raw:`), so an absent line and a blank
one are the same line to it, and the blank one is a claim the run cannot make.

### Step 4 — Commit through the builder

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply
its variables. This step never hand-writes a `git commit`, spells a trailer, `cd`s into a repo, or
stages by hand.

- **The stage list.** `--add system/projects/<name>/project.md` in `<instance-repo>`;
  `--add <README path relative to <product-repo>>` in `<product-repo>`. One `--add` per commit, and
  each commit stages only its own repo's file.
- **Two repos, two calls**, with `--repo` naming each in turn. Run the card's commit first: the
  README is the readable half and the card is the half a machine reads, and a run interrupted between
  the two leaves the machine-read half landed rather than the prose.
- **A run that changed neither file makes no commit.** Report the state and stop.
- **Actor:** `--actor principal-pm --skill product-card` when running as the `principal-pm` agent;
  from an interactive `principal-pm:` session with no agent named,
  `--role "Principal PM" --skill product-card`.
- **And `--prompt product-card/rich`**, naming the body this skill carries.
- **The directional** is `Agari:` or `Shukuba:`, resolved against
  `<CORE>/doctrine/governance/commit_format.md` § *Directional trailer* — the trailer follows the
  commit's scope. Both files are project-scoped, and this step runs upstream of the delivery loop, so
  a project with no open station resolves to its Agari. The same directional rides both commits: the
  product repo carries no `system/projects/`, and the builder reports that referent as uncheckable
  rather than wrong.

### Step 5 — Report

Report, briefly:

- **the card fields written**, each with the value and the document it came from;
- **the fields left alone**, and why — unchanged by the settled set, or not determined by it;
- **the README**, by path, and which claims were corrected;
- **the inputs read and the status each carried**, every one of them, not only the unsettled;
- **anything the documents did not determine**, with what they would have to state for it to be
  derivable;
- **the commit SHA per repo**, or that the run changed nothing;
- **the next move: the skeleton.** Name `<CORE>/launchers/product-skeleton/launcher.sh <project>` as
  the owner's, and say whether the product already has a skeleton. Do not run it.

---

## Critical rules

- **Two files, and no third.** No code, nothing under `<Product path>/docs/`, no other card field, no
  other project's card.
- **Never run the skeleton, and never place, move or delete a frame file.** The launcher is
  deterministic and the owner runs it; this run only makes it correct to run.
- **The card's stamp-time fields are not yours** — `Product path:`, `Package slug:`,
  `Execution type:`, `Parallelism:` — nor is `Source material:`, which is upstream of the PRD.
- **Every inline comment on the card survives byte for byte.** A field the card carries is edited by
  replacing its value, never by rewriting its line; a field it lacks is added as a whole line, with
  the template's comment copied rather than composed.
- **A document found wrong is a finding, not an edit.** The definition and foundation documents
  belong to the seats that authored them; say so in the report and change nothing.
- **There is no companion open-issues file, and its absence is a decision.** What a run cannot derive
  reaches the owner in the report — the prompt's § *When the documents do not determine a field* owns
  why a card field is not the kind of thing a companion loop settles.
