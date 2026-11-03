---
name: nemawashi-refine
description: >-
  Principal PM-posture skill that answers a retired 根回し Nemawashi seed and re-reads the project's
  seedbed behind it — halts outside a principal-pm session or the principal-pm subagent. It runs after
  nemawashi-retire has filed the seed in `trail/`. It processes every recommendation the seed's
  shukuba-refine runs left for the Principal PM, re-reads every candidate in `unpicked/`, and acts:
  modify a candidate, drop one through nemawashi-drop, write a companion item on a product document,
  name a docs cut for work a document already states, cut work no product document should state
  through seeds-from-idea, route a cross-project ask, or ignore a recommendation with its reason. What
  it finds while reading it fixes, files in docs/findings/ or cuts — a dead journey pointer always
  repaired. It never cuts from the product's documents, never picks, never retires, and never writes
  into `trail/`, nor into `drop/` except through nemawashi-drop. It always writes
  one report, `system/projects/<project>/docs/nemawashi-refine/<seed>_report.md`, opening with the next
  moves — the companion sweep (chain-product or chain-agari, by the project card's Definition line),
  seeds-from-product-docs, nemawashi-pick and stations-from-seed, plus a halted cut's re-run or a
  route across projects where owed — each with its seat and the command that starts it.
when_to_use: >-
  Run by the Principal PM once nemawashi-retire has filed a project's walked seed in `trail/`. Trigger
  phrases — "nemawashi-refine", "answer the retired seed", "process the recommendations", "re-read the
  seedbed after the retire", "refine the seedbed". Do not use for retiring the seed itself
  (nemawashi-retire, the Scrum Master's), killing one seed on its own (nemawashi-drop), re-reading the
  route after a change unit lands (shukuba-refine, the PM's), cutting seeds from a product's documents
  (seeds-from-product-docs), or picking the next seed (nemawashi-pick).
license: MIT
metadata:
  author: Eyal Golan
  version: "1.3.0"
  created: "2026-09-25"
  category: journey
  tags: nemawashi, seedbed, recommendations, principal-pm, journey
  risk: safe
  depends-on: nemawashi-drop, seeds-from-idea
---

# nemawashi-refine

## Purpose

A walked seed carries asks nobody has answered yet: every `shukuba-refine` run left a
`<unit-key>_recommendations.md` in its folder, addressed to the Principal PM. `nemawashi-retire` files
that folder in `trail/` and reads none of it. This skill is the Principal PM's answer, run after the
retire: every recommendation processed, the whole candidate pool re-read, and one report that says what
was done and what is owed next.

**This file is the orchestrator.** It owns the posture gate, resolving the retired seed, running each
move through its owner, landing the report, and the commits. It makes no judgment about the seedbed.

**The method is `prompts/rich.md`**, beside this file — the one body this file points at. Read it in
full at Step 3 and apply it. What each recommendation owes, what a candidate is kept, modified or
dropped for, when a docs cut is owed, what is never done, and which moves are owed next all live there.
None of it is repeated here.

**The report's shape** is `templates/report.md`, beside this file.

**Not `shukuba-refine`.** That is the PM's, run after a change unit lands, and it re-reads the route
of the seed being walked. This one runs after a seed is retired, answers what those runs left for this
seat, and re-reads the pool the next pick is made from.

## Posture

**Principal PM only.** Run in a `principal-pm:` session or as the `principal-pm` subagent — the skill
launcher starts it as the latter (`launcher.md`). Invoked from anywhere else, halt at once, say the
posture is wrong, and name the way in. The seat's contract is
`<CORE>/roles/loaders/principal_pm_global.md`, whose § *Retiring a finished seed* is what this run
discharges. The gate is there because the run drops, edits and commits with nobody answering
(`<CORE>/doctrine/setup/authoring_layers.md` § *A skill that acts unattended gates to its seat*).

## Input

**The project** — `system/projects/<project>/` — and, optionally, **the retired seed's slug**
(`<YYYY-MM-DD>_<slug>`). Without a slug, the seed is the one the project's latest retire commit names:

```bash
git log -1 --format=%s --grep='^retire: nemawashi/' -- "system/projects/<project>/journey/nemawashi/trail/"
```

The subject is `retire: nemawashi/<seed> → trail/` (`nemawashi-retire` Step 5); `<seed>` is the slug.
Say in the report that the slug came from the retire commit.

The seed resolves to `journey/nemawashi/trail/<seed>/` (a folder holding `seed.md` and the refine
files) or `journey/nemawashi/trail/<seed>.md` (a file — no `shukuba-refine` ever wrote into it, so it
carries no recommendation).

**A seed already refined is refined again, in full.** An earlier report is never a reason to skip; the
method may have changed, and so may the pool. The report is replaced whole, and the earlier one stays
in git.

**Stop and say what is missing** when there is no project, when no slug was named and no retire commit
exists for the project, or when the seed is not in `trail/` — a seed at the root, in `unpicked/` or in
`drop/` was not retired, and this skill answers only a retired one.

**Project level only.** An instance seed under `system/nemawashi/` is answered by hand, as it is
retired by hand.

The run works in the instance it was started in, on its current branch. It opens no worktree.

## Workflow

### Step 1 — Gate, then resolve the seed

Check the posture (§ *Posture*) and halt there rather than proceeding. Resolve the seed (§ *Input*).
From here `<nema>` is `system/projects/<project>/journey/nemawashi/`.

### Step 2 — Gather what the run reads

- **The recommendations.** Every `<unit-key>_recommendations.md` in `<nema>/trail/<seed>/`, and the
  `<unit-key>_report.md` beside each. Number them as `<unit-key> #<n>`. A file reading "Nothing to
  recommend." contributes no item and is listed as read. A file-seed contributes none.
- **The pool.** Every candidate in `<nema>/unpicked/` — a `<slug>.md`, or a `<slug>/` folder whose
  `seed.md` is the seed.
- **The seedbed root.** Normally empty after the retire. A seed there has been picked already: it is
  the PM's, read for context and never touched.
- **The bearings.** `system/projects/<project>/agari.md` and `system/michi.md`.
- **Upstream.** Resolve `Product path:` from `system/projects/<project>/project.md`. Where it holds a
  `docs/`, read its documents and list every live `*_open_issues.md`. Where it holds none, there is no
  upstream; say so and go on.
- **What is already broken.** Run `python3 "<CORE>/tools/check_journey_links.py" --repo "<instance
  root>"` before acting. A move runs the check after, not before (`<CORE>/docs/journey_move.md` § *After
  the move, say which pointers it broke*), because it looks for what the move breaks; this run looks
  for what is already dead. Every pointer it names is a found defect the prompt's § *What you find
  while reading is yours to fix* owes a repair.
- **Chain in flight.** Read `system/logs/chain-<project>-state.json` by the test `shukuba-refine`
  Step 3 uses. A document on a live chain's spine, and its companion, is **held**: nothing is raised on
  it.

### Step 3 — Read the method, and decide

Read `prompts/rich.md` in full, then `templates/report.md`. Apply the prompt. Every judgment — what each
recommendation owes, what each candidate owes, whether a docs cut is owed, and what is named next — is
made there.

### Step 4 — Act on the seedbed

Make the moves in this order, so no move finds the ground changed by a later one:

1. **Modify a candidate, and repair what you found.** Edit in place in `unpicked/` — for a
   folder-seed, in `seed.md` or the file in its folder that holds the defect — and repair every dead
   pointer Step 2's check named, wherever it is; one in the product's repo goes with Step 4.3's commit
   there. Commit these edits
   together through `<CORE>/doctrine/governance/commit_via_builder.md` with
   `--actor principal-pm --skill nemawashi-refine --prompt nemawashi-refine/rich`.
2. **Drop a candidate.** Invoke `nemawashi-drop` on it, saying the kill and giving the reason the
   prompt wrote, in one invocation — that closes both halves of its Step 1A. It checks and commits
   itself; where it refuses, record the refusal as a non-move.
3. **Write companion items.** Per `<CORE>/../skills/companion/.claude/skills/companion-self-answer/SKILL.md` § *When a
   change belongs to another document*: append to the document's live companion, or open one from that
   document's own `*_open_issues_template.md`, in the section for items raised from downstream where the
   template has one. Commit in the product's own repo, one commit per companion. The document is never
   edited.
4. **Cut work no document should state.** Write the brief the prompt decided on, in the shape of
   `<CORE>/../skills/principal-pm/.claude/skills/seeds-from-idea/templates/brief.md`, at
   `system/projects/<project>/docs/seeds-from-idea/<YYYY-MM-DD>_<slug>_brief.md`, and invoke
   `seeds-from-idea` with its path. Nobody confirms it: its `## The ask` quotes the recommendation at
   its lines, which the cut checks before it reads anything else. The cut commits the brief with the
   seeds it lands in this project's `unpicked/`, and leaves its report beside the brief. **Read that
   report**: its line-by-line account of the ask is what this run's recommendation row records as what
   was done, and an ask line it left for a later cut is named as a next move. Where the cut halts,
   record the halt as a non-move and name its re-run as a next move.
5. **Re-check, repair, and file.** Run the check again: the drops can break pointers aimed at what
   they moved. Repair what it names, in one commit with the same `--actor`, `--skill` and `--prompt`.
   Then file a machinery finding, if the prompt found one, in `docs/findings/` in its own commit.

Never edit the retired seed, never write under `trail/`, never write under `drop/` except through
`nemawashi-drop`, never touch a seed at the root beyond repairing a dead pointer in it,
and never run `product-fdr`, `seeds-from-product-docs`, `nemawashi-pick`, `stations-from-seed` or
`nemawashi-retire` — each is named as a next move, or is not this run's.

### Step 5 — Land the report

Write `system/projects/<project>/docs/nemawashi-refine/<seed>_report.md` from the template — **every
run**, replacing an earlier one whole. It opens with `## Next moves`, names every move with the SHA
Step 4 produced, and carries every recommendation and every candidate as a row.

Commit through `<CORE>/doctrine/governance/commit_via_builder.md`: `--add` the report,
`--actor principal-pm --skill nemawashi-refine --prompt nemawashi-refine/rich`, subject
`nemawashi-refine: <seed> — <n> recommendations, <m> candidates`. The directional follows
`<CORE>/doctrine/governance/commit_format.md` § *Directional trailer*: `Agari: <project>`, with
`progress:` when the seedbed moved and `aside:` when nothing did.

### Step 6 — Report

Say how many recommendations were processed and how, what each candidate got, and where the report
is. Then list the report's `## Next moves` as written there — each move, whose it is, and its command —
and make none of them.

---

## Outputs

| File / effect | Produced when |
|---|---|
| `docs/nemawashi-refine/<seed>_report.md` (opening with `## Next moves`), one commit | Every run that passes Step 1 |
| Candidate edits and pointer repairs, one commit | The prompt found a candidate owed a change, or Step 2's check named a dead pointer (Step 4.1) |
| Pointer repairs after the drops, one commit | The re-check named a pointer the drops broke (Step 4.5) |
| A file in `docs/findings/`, its own commit | The prompt found a defect in kensaiapp's machinery (Step 4.5) |
| A `nemawashi-drop` commit per dropped candidate | The prompt found a candidate killed (Step 4.2) |
| A companion item in the product's repo, one commit per companion | A change belongs to a product document (Step 4.3) |
| New candidates in a project's `unpicked/`, `seeds-from-idea`'s commit | Work no product document should state (Step 4.4) |
| No change; what is missing, named | Wrong posture, no project, no retire commit and no slug, the seed not in `trail/`, or an instance seed |

---

## Critical Rules

- **The Principal PM's, and it halts elsewhere.** The run drops, edits and commits unattended.
- **After the retire, never instead of it.** The seed is already in `trail/`; the run answers it and
  never moves it.
- **Every recommendation processed, none silent.** A companion item, a docs cut, carried by a
  candidate, a drop, a seed cut from an idea, a route across projects, or ignored with its reason — the kinds are
  `prompts/rich.md`'s. A recommendation with no row is one nobody read.
- **The report, every run.** A run that moves nothing still writes it.
- **Never cut from the product's documents.** A docs cut is named as a next move, never run — and
  named whenever the documents hold work no candidate carries, whether or not `unpicked/` is empty.
  New work a document should state goes onto that document as a companion item first.
- **Never pick, never retire.** The pick is the PM's (`nemawashi-pick`), the retire the Scrum
  Master's (`nemawashi-retire`); the report names the pick and the route cut after it
  (`stations-from-seed`).
- **No write to `trail/`, none to `drop/` except `nemawashi-drop`'s move, and no edit to a product
  document.** The retired seed and its files are a record; a document changes only through its
  companion.
- **Each move through its owner.** Drop and cut run their skills; a companion item follows
  `companion-self-answer`'s mechanism. None is re-implemented here.
- **What it finds is fixed, filed or cut, never only reported** — the prompt's § *What you find
  while reading is yours to fix*.
- **The method is the prompt's.** Everything about what a recommendation or a candidate owes lives in
  `prompts/rich.md`. A second copy here is a copy free to drift.
