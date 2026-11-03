---
name: product-content
description: Content-Manager-posture skill that authors a project's verbal language (CONTENT.md) — the standing source of truth for everything a product says to a person, covering voice and tone, grammar and mechanics, terminology, the message patterns for error/empty/loading/partial/recovered states, the accessibility bar for text, and localization rules. The peer of the CDO's DESIGN.md — how something looks belongs there, what it says belongs here. Requires Content Manager posture (halts outside a content-manager session or subagent). Non-interactive by design — it derives the whole verbal language best-effort off the settled UXD and the product's existing strings, and surfaces its load-bearing calls into a companion open-issues file for the owner to sign off async. On re-run it folds their answers in and clears the companion when nothing is left unresolved — its absence means the verbal language is done. Use when authoring, continuing, or revising a product's verbal language, content standard, voice and tone guide, terminology governance, or UX-writing rules — including when the request never says "CONTENT.md", such as "define how this product talks", "we need a voice and tone standard", or "our error messages are inconsistent". Do not use for per-change copy or interface strings, the design language (product-design), the experience definition (product-uxd), the PRD (product-prd), the SRS (product-srs), the project's Agari (project-agari), or downstream documents (SDD / Delivery Plan / FDR / ADR / NFDR).
license: MIT
metadata:
  author: Eyal Golan
  version: "1.4.5"
  created: "2026-08-05"
  category: product-definition
  tags: content-design, verbal-language, voice-and-tone, terminology, content-manager, product-definition, upstream-chain
  risk: safe
---

# product-content

## Purpose

Author a project's **verbal language** (`CONTENT.md`) — the standing source of truth for
everything the product says to a person. It is written **off the UXD**, which is the document
that names the states its message patterns answer to, and it holds **no per-change copy** — where
that boundary falls is the prompt's § What belongs in this document.

**The peer of the design language, not a part of it.** `DESIGN.md` is the visual language and is
the CDO's; this is the verbal one. A value carried in both is a defect of whichever document
copied it.

This file is the **orchestrator** — posture, the file loop, path resolution, staging, and the
commit. **How to author** — the completeness lens, the behaviour rule, the corpus test, the
checkability bar, the terminology rule, the stability rule and the boundaries — is the authoring
prompt **`prompts/rich.md`**, applied at Step 2; a rule referenced
below by name lives there and is not restated here. The document's **section shape as stamped** is
the template **`<CORE>/templates/product-templates/content_template.md`**; the companion's shape
is **`content_open_issues_template.md`** beside it.

**Non-interactive.** The run never blocks on the owner — it derives the whole verbal language
best-effort, writes its load-bearing calls into a companion open-issues file the owner signs off on
their own time, and a re-run folds those answers in. That is what lets it run headless (as the
`content-manager` subagent) as well as in an interactive `content-manager:` session.

**There is no machine gate.** Its peer runs an external linter before committing; nothing publishes
a schema or a lint for a verbal language, so this skill has no such step and no such evidence. The
bar is carried entirely in how each rule is worded, which is the prompt's § The checkability bar —
the one place this document can fail silently, and the reason that section is not optional reading.

---

## Posture

**Content Manager role required.** If invoked outside Content Manager posture (neither a
`content-manager:` session nor the `content-manager` subagent), stop and say — *"product-content
requires Content Manager posture. Switch? (Open a session with the `content-manager:` prefix, or run
the `content-manager` subagent.)"* Do not shed the role. Where this seat ends and the CDO's begins
is a posture fact the Content Manager loader stack owns, and the split that governs *while
authoring* is the prompt's § The ground you stand on — neither is restated here.

---

## The files and the loop

product-content produces the files below under the product's `docs/` — the skill resolves the
locations (next section); a caller names the **project**, never the paths.

| File | What it is | Lifecycle |
|---|---|---|
| `<Product path>/docs/CONTENT.md` | The verbal language — best-effort complete on every run. | Permanent; one document, revised and versioned in place (the bump-on-revision rule is the template's own header note), never forked. |
| `<Product path>/docs/CONTENT_open_issues.md` | The companion, holding the calls awaiting the owner's sign-off and the few things the run could not settle, in the buckets `content_open_issues_template.md` defines — kept distinct, never blurred. Which bucket an item lands in is the prompt's. | Transient — exists only while something is unresolved. **Its absence is the done signal.** |
| `<Product path>/docs/trail/content/cycle-<N>.md` | Each answered companion, retired whole. | Permanent. |

**Cycle numbering:** `N` is one higher than the **highest** `cycle-<N>.md` already in
`trail/content/` — list the directory and take the max, so a removed or renamed cycle can't make
you collide with an existing one. The first is `cycle-1.md`; create `trail/content/` if it isn't
there. Never overwrite an existing cycle.

**The loop, repeated until clean:**

1. The run derives/updates the verbal language and writes the companion with what it couldn't
   ground.
2. The **owner answers inline** — filling the companion's answer slots, whose names and shape are
   `content_open_issues_template.md`'s, stated there and not here — and re-runs the skill.
3. The run **copies the answered companion whole to the next trail cycle**, folds the answers into
   the verbal language, and rewrites the companion with only what is still unresolved — an answer
   the fold leaves unsettled still drops, its residue re-raised as a fresh unanswered item. This is
   the ordinary cycle. A run where nothing would survive is step 4's, and step 4 alone says what it
   may touch.
4. When the answers resolve everything, the run is the close — one run that folds, copies the
   answered companion to the trail, and **removes** the companion instead of rewriting it, through
   the builder's `--rm` at Step 3, never a hand-`rm`. **No open-issues file = the verbal language
   is done.** The close has a precondition the ordinary cycle does not — the owner's answers must
   already be committed (Step 3 owns the rule and why). Re-entry is inline answers, so the first
   closing touch normally finds them uncommitted, and then it **changes nothing at all**: no fold,
   no trail copy, no rewrite, no commit; the companion survives intact, answers and all, for the
   owner to commit. It reports the state and asks for that commit; the re-run after it is the
   close, start to finish, in one run. That stop is a report with an ask, not a live interview.

Step 3 is why the trail exists. Folding rewrites the companion and the close removes it — so
without the trail the owner's answers are destroyed twice, and their reasoning for a decision
survives only in git history. The trail costs one `cp` on the same commit and makes every owner
answer permanently citable. It is the skill's job; the owner never manages it.

---

## Inputs and where the files land

- **The UXD** — your primary input; read it in full. Its location is `product-uxd`'s to name — that
  skill wrote it, and its own file table owns where the UXD lands under the product's `docs/`;
  resolve the path from `<CORE>/../skills/cdo/.claude/skills/product-uxd/SKILL.md`, never from a path remembered here.
  It must exist — if nothing is at the resolved path, halt and report, because the states that
  carry the product's words are named there and there is nothing to derive patterns from without
  them. What its content means for the derivation is the prompt's rule.
- **The product's existing strings — the corpus.** Locate and read them. What counts as the corpus,
  where it is kept, and what to do when there is none, is the prompt's § Inputs you work from. Finding nothing is a finding the prompt says how to route, never
  a halt.
- **The PRD** — beside the UXD under the product's `docs/`; its location is `product-prd`'s to
  name, resolved from `<CORE>/../skills/cpo/.claude/skills/product-prd/SKILL.md`. Read it if it is there; what it feeds
  is the prompt's. **Its absence does not halt the run** — the state reaches the owner through the
  companion like any other input gap.
- **`system/projects/<name>/agari.md`** — the project's 上がり Agari, beside the card below. Read it
  in full; what the terminus bounds is the prompt's rule. **Absence does not halt the run**, nor
  does an unfilled placeholder — the state reaches the owner through the companion.
- **`system/projects/<name>/doctrine/`** — the project's own doctrine, if the folder holds anything.
  Read what is there; what it binds is the prompt's rule. Empty or absent is silence, not a halt.
- **The product's `docs/` folder** — read it by **listing the directory**, not by recalling a set of
  filenames. Beyond the files named here and the loop files above, whatever else the folder holds is
  input the run is entitled to — brand material, a tone-of-voice note, the design language, the
  upstream trails of owner answers. What each carries, and which supersedes which, is the prompt's
  § Inputs you work from. Skip binary assets. Enumerating rather than naming is deliberate — a list
  of filenames kept here goes stale the day the product gains a document, and the run would never
  know what it had missed.
- **Context and constraints** — whatever the owner hands you, or the docs it points at.
- **`system/projects/<name>/project.md`** — the directed project's card. Its `Product path:` field
  resolves where every output lands; the field is the card template's
  (`<CORE>/templates/project_template.md`, the shape `project-stamp` stamps the card from), so
  read it from the card in hand. Every later `Product path:` in this file means that field.

**Path resolution.** A relative `Product path:` is inside the instance repo; an absolute one is
outside it, in whatever repo holds the product (which need not be its root — Step 1 resolves that
repo as `<repo>`). Every instance-relative path this file names (`system/…`, `.claude/…`) resolves
from the instance repo root — the directory the session opened in; no step `cd`s away from it. If
`Product path:` is a placeholder or awaits an owner value, halt and report: both outputs resolve
from it, so there is nowhere to write even an open issue recording the gap. Never invent one.

---

## Workflow

### Step 1 — Identify the project, read current state

Identify the target project and read:

- `system/projects/<name>/project.md` — the binding. Resolve the file locations from
  `Product path:`, and resolve **`<repo>`** with it — the repo the commit lands in: the instance
  repo (`.`) for a relative path; for an absolute one,
  `git -C "<Product path>" rev-parse --show-toplevel`, because a product with its own repo need not
  sit at that repo's root. If more than one project exists and the target is ambiguous, halt and
  report the candidates — nothing can be resolved or filed without a project.
- the UXD, at the path resolved under *Inputs and where the files land* — in full. **It must be on
  the record:** run `git -C <repo> status --porcelain -- <the resolved UXD path>`; any output halts
  the run, naming the file, for the owner to commit or discard it before re-running. Settled rules
  are derived from the UXD and then held stable against re-derivation (the prompt's *stability
  rule*), so deriving from an uncommitted UXD can leave settled rules sourced to text the owner
  later discards — settled output whose source was never on the record. One path, one question:
  this asks about no other file, and the UXD's existence is established above, so the only states
  left to tell apart are clean and not-clean.
- `<Product path>/docs/CONTENT.md` — the existing verbal language, if any. It is the settled
  baseline the prompt's *stability rule* reproduces; none here means this run is a first authoring.
- `<Product path>/docs/CONTENT_open_issues.md` — the existing companion, if any. **This is the
  loop's re-entry point**, and it is where the owner's inline answers are read. Whether what you
  find may be folded, and how narrowly, is the prompt's *stability rule*; this file only tells you
  to read it.
- `<Product path>/docs/trail/content/` — every answer the owner has already given, and their
  reasoning. Read it: a rule the owner set in an earlier cycle is authorized, and changing it needs
  a fresh authorization (the prompt's *stability rule*). It also gives you the next cycle number.
- the product's existing strings — locate and read them, per *Inputs and where the files land*.
- the rest of `<Product path>/docs/` — **list the directory** and read what the bullets above have
  not already named. Skip binary assets.
- `system/experience/voice_direction.md` — the instance's **voice direction**, and the one input
  this run *inherits* from rather than derives from. Its §§ 2–6 cover the same ground `CONTENT.md`
  covers — voice, tone and address, terminology, message patterns, the reading bar, localization —
  so a line stated there is one this product **holds**, not evidence to derive a line from, and a
  section the instance settles as `n/a` is a declaration that each product decides that section for
  itself, never a missing input. § Overview supplies the rest: how a run decides when neither a
  fence entry nor an inherited line covers the case.
- `system/experience/voice_restrictions.md` — the instance's **verbal fence**: the verbal limits
  every product under this instance holds, and which no product may relax. The verbal language is
  written inside it, and a rule that breaks a fence entry is not a rule you may write.

**Then the experience gate — the last check in this step, and the only one that asks about the
instance.** It runs after every check above deliberately: a halt firing before the product's own
input checks stands in for whichever of them would have fired, and then neither this run's report
nor an assertion written against those halts can tell which one was hit. Run it from the instance
repo root:

```
python3 <CORE>/tools/experience_gate.py
```

Pass it no root. *Path resolution* above already fixes where an instance-relative path resolves
from, and that holds whatever `Product path:` says — an absolute one moves `<repo>` to the
product's own repo and moves nothing here, because the layer being graded is the **instance's**,
not the product's.

**For this gate the exit code *is* the verdict** — 0, 1 and 2 are the whole answer, and there is no
bar to consult beside it. This skill runs no second gate to confuse it with (§ Purpose, *There is
no machine gate*), so the code stands alone.

Whichever branch fires, **reprint the tool's own output** — its header line, each question's line
with the detail indented under it, and its verdict line — instead of summarising it. The tool
separates a root it could not use from an instance that never took the layer, and those two have
different fixes; a paraphrase throws the distinction away.

- **exit 0** (`GREEN — all three questions passed`) — the layer is ratified. Continue to Step 2 and
  author normally.
- **exit 1** (`RED — <n> of 3 questions failed`) — the layer was read and **judged not ratified**.
  **Halt**, and report the failing question(s) with the detail lines the tool named under them: the
  open companions, the pairing findings, or the reach hits. The recovery is the **owner's**: they
  answer those open companions in `system/experience/`, and the layer's own authoring pass closes
  them. Say so, and say that nothing this run can do moves the verdict.
- **exit 2** (`NOT EVALUATED — <n> of 3 questions could not be asked`) — the gate **could not
  look**, and **nothing was judged**. **Halt**, report that plainly, and give the reason line the
  tool printed against each question. The recovery is a **path or an authoring pass**: correct the
  root this run is standing in, or author the instance's experience layer if this instance never
  took one. It is explicitly **not** answering companions — nothing was read, so nothing was found
  open, and pointing the owner at open questions here sends them to a file that may not exist.

Both halts stop the run where it stands: no `CONTENT.md`, no companion, no trail copy, no commit.
Steps 2 through 4 do not run — the run's whole report is the gate's own output plus the recovery
named above, the same shape as the halts earlier in this step.

Gather any context and constraints the owner handed you, and read them.

### Step 2 — Derive/revise the verbal language and write the companion (no interview)

**Gate first — detect the first closing touch before you write anything.** When a companion existed
at intake, its inline answers would resolve everything unresolved, and the file is uncommitted
(check the companion's git cleanliness in `<repo>`), this run is the first closing touch and
**writes nothing** — no derivation or fold, no trail copy, no companion rewrite. Skip the rest of
this step and Step 3, and report CLOSING at Step 4. Why the close needs committed answers is Step
3's (`--rm` mechanics); the two touches are the loop's, step 4. Everything below runs only when this
gate passes.

Derive or revise `<Product path>/docs/CONTENT.md` by applying the authoring prompt
**`prompts/rich.md`** (how to think) and the template
**`<CORE>/templates/product-templates/content_template.md`** (the section shape as stamped).
Write the companion from **`<CORE>/templates/product-templates/content_open_issues_template.md`**
(its bucket and slot shape). The prompt's *stability rule* reads its baseline where that baseline
lives — the document on disk at the CONTENT path, which Step 1 has already read; none there is a
first authoring, and the rule does not bind it. This step restates none of the prompt's thinking.

Set the template's `Status:` line from Step 4's DONE condition — the companion's absence — not from
your tally of answers: **Settled** only when this run ends with no companion on disk (it removed
one, or a first run grounded everything from its inputs and never wrote one); **Draft** otherwise.
All three ways a run can end are settled here, because there is no later step that can raise an
item — the close folds every answer and ends with the companion removed, the first closing touch
writes nothing at all, and every other run leaves a companion behind. Leave **Locked** alone —
ratification is the owner's act, not yours. Bump the template's `Version:` line on any run that
changes the document's content.

Do **not** interview. When anything lands in any bucket, write/update the companion from its
template. When nothing is unresolved, write none — an empty companion would read as OPEN and invert
the done signal: if none existed at intake, create nothing; if one existed, Step 3's `--rm` removes
it.

**Consuming an answered companion.** A companion that existed at intake with at least one answer
slot filled is **consumed** — what counts as an answer slot is the companion template's, read from
its current shape, never from a name remembered here, so a template rename cannot make filled
answers read as unfilled. Consuming is three moves, in this order: copy the companion whole (an
ordinary `cp`) to the next trail cycle, *before* the fold rewrites it; fold the owner's answers into
the verbal language; then drop every **answered** item from the companion.

**An answered item never survives the drop.** Where the answer settles its item, the item is
resolved and gone. Where the answer leaves something unsettled, the item still drops and the residue
**re-enters as a fresh item with an empty answer slot** — a new item this run raises, never the old
one surviving. Whether an answer settles its item is the prompt's rule; this step only moves the
files that rule implies. What the drop buys is the invariant the rest of the loop keys on: a filled
slot in a surviving companion is always the owner's writing, never this run's, so a run's own
rewrite can never re-fire this detection at the next intake.

A companion with no slot filled is not consumed — no trail cycle, nothing to fold. And when the drop
resolves **every** item, the *write none* rule above owns the disk: leave the companion as intake
read it (the trail copy already holds it) and let Step 3's `--rm` remove it. No state of this run —
a halt between Step 2 and Step 3 included — ever leaves an empty companion behind.

### Step 3 — Commit through the builder

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply
its variables (`<repo>` from Step 1, the `--add`/`--rm` paths, the actor, subject/body, the
directional). The builder stages, derives `Role:`, and lays the whole trailer block; this step never
hand-writes a `git commit`, spells a trailer, `cd`s into the repo, or resolves the directional
*shape*. What follows is only the values product-content feeds it.

**A run that changes nothing builds no commit — and touches no disk.** If this run folded no answer,
changed no content and has nothing to stage, make no file change at all: don't copy to the trail,
don't rewrite the companion. (This is *not* the recipe's `--allow-empty` marker case —
product-content makes no commit at all on an empty run.) Report the state (Step 4) and stop.

**The stage list — compose it from what this run actually did.** Pass every qualifying path in
**one** `--add` (and the companion as the one `--rm` path, when removed) — the recipe's flag rule
owns why. `<D>` below is the resolved docs directory, `<Product path>/docs` expressed relative to
`<repo>` (plain `docs` when the product *is* the repo's root; the subpath when it sits deeper; the
instance-relative path when `<repo>` is `.`).

- `--add <D>/CONTENT.md` — always, on any run that builds a commit.
- The companion, exactly one of: `--add <D>/CONTENT_open_issues.md` (something is unresolved) ·
  `--rm <D>/CONTENT_open_issues.md` (nothing unresolved *and* one existed at intake — its removal is
  the done signal) · **neither** (nothing unresolved and none existed, so nothing is on disk to
  stage either way). The owner answers *inside* the companion, so the close needs their answers
  already committed — git won't remove a dirty file, and their words aren't yours to commit. A dirty
  companion when everything would resolve marks the first closing touch: Step 2's gate stopped that
  run before any write, so it never reaches this step.
- `--add <D>/trail/content/cycle-<N>.md` — only if this run consumed an answered companion. The
  trail copy rides the same commit as the fold it precedes; neither fires without the other.

**Actor:** `--actor content-manager --skill product-content` when running as the `content-manager`
agent (the usual path — the subagent, or a `--bg` run launched `--agent content-manager`); from an
interactive `content-manager:` session with no agent named, `--role "Content Manager" --skill
product-content` instead. Both derive the same `Role:`; why `--skill` is explicit is the recipe's to
say. Subject/body, the directional, and the surface / co-author trailers are the recipe's variables
— fill them per the recipe, not from an example copied here.

**And `--prompt product-content/rich`**, naming the body this skill is the carrier for. A thin skill over a fat prompt is recorded by both lines and neither implies the other (`<CORE>/doctrine/governance/commit_format.md` § *`Prompt-Version:` trailer*); it takes the bare name, never a path.

### Step 4 — Close / report

Report:

- the CONTENT.md path, and the commit SHA (or that the run changed nothing and built no commit);
- on any run that consumed an answered companion, the **trail cycle path** —
  `<Product path>/docs/trail/content/cycle-<N>.md`, the copy Step 2 made. The loop (its step 4) owns
  why that copy is the surviving record of the owner's answers; the report names it so the owner can
  verify their answers survived without opening the commit;
- the **loop status**, exactly one of:
  - **DONE** — no open-issues file remains and nothing is unresolved. The verbal language is
    complete.
  - **CLOSING** — the owner's answers resolve everything, but the companion is dirty, so this run
    was the first closing touch and changed nothing (the loop, step 4; Step 3's companion rule).
    Nothing is left to answer; the one ask is — commit the companion, then re-run, and that re-run
    is the close.
  - **OPEN** — something is still unanswered. Give a count per bucket, under the bucket names the
    companion on disk carries (its shape is `content_open_issues_template.md`'s, so read the names
    there, never from a name remembered here), name where they live, and name the next move: the
    owner answers inline, commits, and re-runs product-content.

Do not enumerate downstream steps; authoring the verbal language is this skill's whole job.
