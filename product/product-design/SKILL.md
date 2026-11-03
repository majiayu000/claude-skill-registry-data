---
name: product-design
description: CDO-posture skill that authors a project's design language — the visual source of truth in Google's DESIGN.md format, written off the settled UXD's design-system direction and read cold by implementing agents to style the product. Requires CDO posture (halts if invoked outside a cdo session or the cdo subagent). Non-interactive by design — it grounds every value in the evidence where evidence exists (the product's own source, its brand assets, the UXD's constraints) and designs the rest itself, and instead of interviewing live it surfaces its load-bearing calls into a companion open-issues file for the owner to sign off async. It runs the format's own linter before committing and never reports a design language finished on a file that has not met the prompt's bar. On re-run it consumes both files, retires the owner's answered companion whole to a permanent trail, folds their answers into the design language, and when nothing is left unresolved it clears the companion — its absence means the design language is done. The skill resolves where the files land from the project's Product path. Use when authoring, continuing, or revising a product's design language. Do not use for the experience definition (product-uxd), per-change specs (development-specs), the PRD (product-prd), the SRS (product-srs), the project's Agari (project-agari), or downstream documents (SDD / Delivery Plan / FDR / ADR / NFDR).
license: MIT
metadata:
  author: Eyal Golan
  version: "0.11.5"
  created: "2026-08-04"
  category: product-definition
  tags: design-language, design-tokens, cdo, product-definition, upstream-chain
  risk: safe
---

# product-design

## Purpose

Author a project's **design language** (`DESIGN.md`): the visual source of truth — the tokens
that are normative and the prose that applies them — read cold by implementing agents to style
the product. It is written **off the UXD's design-system direction call**: that call names the
system and the constraints, and this document holds every value — a token value carried in both
is a defect of whichever document copied it. The sequence is
`<CORE>/doctrine/setup/setting_up_a_project.md`, which owns it and is not restated here.

The format is **external and machine-checked** — Google's DESIGN.md, linted by
`@google/design.md`. The schema's authority is the vendor, not this skill and not the template;
which invocation is pinned and what a clean result means are the prompt's.

This file is the **orchestrator**: posture, the file loop, path resolution, the machine-gate
step, staging, and the commit. **How to author** — the design-language completeness lens, the
evidence gate, the anti-default discipline, the provenance gate, the machine gate's bar, the
stability rule, and the tone — is the authoring prompt
**`prompts/rich.md`**, applied at Step 2; a rule referenced below by name
lives there. The design language's **section shape and token schema as stamped** are the template
**`<CORE>/templates/product-templates/design_template.md`**; the companion's shape is
**`design_open_issues_template.md`** beside it. None of them is restated here.

**Non-interactive.** The run never blocks on the owner: it derives the whole design language
best-effort, writes its load-bearing calls into a companion open-issues file the owner signs off on
their own time, and a re-run folds those answers in. That is what lets it run headless (as the
`cdo` subagent) as well as in an interactive `cdo:` session.

---

## Posture

**CDO role required.** If invoked outside CDO posture (neither a `cdo:` session nor the `cdo`
subagent), stop and say: *"product-design requires CDO posture. Switch? (Open a session with
the `cdo:` prefix, or run the `cdo` subagent.)"* Do not shed the role. Where the CDO ends and the
delivery-tier **Architect** begins is a posture fact the CDO loader stack already owns — the two
share the word "design" and nothing else, and the boundary comes from there, never from a
restatement here.

---

## The files and the loop

product-design produces the files below under the product's `docs/` — the skill resolves the
locations (next section); a caller names the **project**, never the paths.

| File | What it is | Lifecycle |
|---|---|---|
| `<Product path>/docs/DESIGN.md` | The design language — best-effort complete on every run. | Permanent; one document, revised and versioned in place (the bump-on-revision rule is the template's own header note), never forked. |
| `<Product path>/docs/DESIGN_open_issues.md` | The companion, holding the calls awaiting the owner's sign-off and the few things the run could not settle, in the buckets `design_open_issues_template.md` defines — kept distinct, never blurred. Which bucket an item lands in is the prompt's. | Transient — exists only while something is unresolved. **Its absence is the done signal.** |
| `<Product path>/docs/trail/design/cycle-<N>.md` | Each answered companion, retired whole. | Permanent. |

**Cycle numbering:** `N` is one higher than the **highest** `cycle-<N>.md` already in
`trail/design/` — list the directory and take the max, so a removed or renamed cycle can't make
you collide with an existing one. The first is `cycle-1.md`; create `trail/design/` if it isn't
there. Never overwrite an existing cycle.

**The loop, repeated until clean:**

1. The run derives/updates the design language and writes the companion with what it couldn't
   ground.
2. The **owner answers inline** — filling the companion's answer slots, whose names and shape are
   `design_open_issues_template.md`'s, stated there and not here — and re-runs the skill.
3. The run **copies the answered companion whole to the next trail cycle**, folds the answers
   into the design language, and rewrites the companion with only what is still unresolved — an
   answer the fold leaves unsettled still drops, its residue re-raised as a fresh unanswered
   item. This is the ordinary cycle — something survives the fold. A run where nothing would is
   step 4's, and step 4 alone says what it may touch.
4. When the answers resolve everything, the run is the close: one run that folds, copies the
   answered companion to the trail, and **removes** the companion instead of rewriting it —
   through the builder, Step 4's `--rm`, never a hand-`rm`. **No open-issues file = the design
   language is done.** The close has a precondition the ordinary cycle does not: the owner's
   answers must already be committed (Workflow Step 4 owns the rule and why). Re-entry is inline
   answers, so the first closing touch normally finds them uncommitted — and then it **changes
   nothing at all**: no fold, no trail copy, no rewrite, no commit; the companion survives
   intact, answers and all, for the owner to commit. It reports the state and asks for that
   commit; the re-run after it is the close, start to finish, in one run. That stop is a report
   with an ask, not a live interview.

Step 3 is why the trail exists. Folding rewrites the companion and the close removes it — so
without the trail the owner's answers are destroyed twice, and their reasoning for a decision
survives only in git history. The trail costs one `cp` on the same commit and makes every owner
answer permanently citable. It is the skill's job; the owner never manages it.

---

## Inputs and where the files land

- **The UXD** — your primary input; read it in full. Its location is `product-uxd`'s to name —
  that skill wrote it, and its own file table owns where the UXD lands under the product's
  `docs/`; resolve the path from `<CORE>/../skills/cdo/.claude/skills/product-uxd/SKILL.md`, never from a path
  remembered here. It must exist: if nothing is at the resolved path, halt and report — the
  design language is authored off the UXD's direction call, so there is nothing to derive one
  from. What the UXD's content means for the derivation — the direction call it seeds from, the
  accessibility requirements that bind the values — is the prompt's rule.
- **The product's own source** — locate and read whatever holds the product's existing visual
  decisions; what counts as that evidence is the prompt's § *Inputs you work from*. For an
  existing product this is the evidence base, and finding nothing is itself a finding the prompt
  says how to route — never a halt.
- **The PRD** — beside the UXD under the product's `docs/`; its location is `product-prd`'s to
  name, resolved from `<CORE>/../skills/cpo/.claude/skills/product-prd/SKILL.md`. Read it if it is there; what it
  feeds is the prompt's § *Inputs you work from*. **Its absence does not halt the run** — the
  state reaches the owner through the companion like any other input gap.
- **`system/projects/<name>/agari.md`** — the project's 上がり Agari, beside the card below. Read it
  in full; what the terminus bounds is the prompt's rule. **Absence does not halt the run**, nor
  does an unfilled placeholder — the state reaches the owner through the companion.
- **`system/projects/<name>/doctrine/`** — the project's own doctrine, if the folder holds anything.
  Read what is there; what it binds is the prompt's rule. Empty or absent is silence, not a halt.
- **The product's `docs/` folder** — read it by **listing the directory**, not by recalling a
  set of filenames. Beyond the files named here and the loop files above, whatever else the
  folder holds is input the run is entitled to: brand material, the product request, the UXD's
  and PRD's own trails of owner answers. What each carries, and which supersedes which, is the
  prompt's § *Inputs you work from*. Skip binary assets. Enumerating rather than naming is
  deliberate — a list of filenames kept here goes stale the day the product gains a document,
  and the run would never know what it had missed.
- **Context and constraints** — whatever the owner hands you, or the docs it points at. What
  counts as one is the prompt's § *Inputs you work from*; read the list there, it is not
  restated here.
- **`system/projects/<name>/project.md`** — the directed project's card. Its `Product path:`
  field resolves where every output lands; the field is the card template's
  (`<CORE>/templates/project_template.md`, the shape `project-stamp` stamps the card from),
  so read it from the card in hand. Every later `Product path:` in this file means that field.

**Path resolution.** A relative `Product path:` is inside the instance repo; an absolute one is
outside it, in whatever repo holds the product (which need not be its root — Step 1 resolves
that repo as `<repo>`). Every instance-relative path this file names (`system/…`, `.claude/…`)
resolves from the instance repo root — the directory the session opened in; no step `cd`s away
from it. If `Product path:` is a placeholder or awaits an owner value, halt and report: both
outputs resolve from it, so there is nowhere to write even an open issue recording the gap.
Never invent one.

---

## Workflow

### Step 1 — Identify the project, read current state

Identify the target project and read:

- `system/projects/<name>/project.md` — the binding. Resolve the file locations from
  `Product path:`, and resolve **`<repo>`** with it — the repo the commit lands in: the instance
  repo (`.`) for a relative path; for an absolute one,
  `git -C "<Product path>" rev-parse --show-toplevel`, because a product with its own repo need
  not sit at that repo's root. If more than one project exists and the target is ambiguous, halt
  and report the candidates — nothing can be resolved or filed without a project.
- the UXD, at the path resolved under *Inputs and where the files land* — in full. **It must be
  on the record:** run `git -C <repo> status --porcelain -- <the resolved UXD path>`; any output
  halts the run, naming the file, for the owner to commit or discard it before re-running.
  Settled design-language content is derived from the UXD and then held stable against
  re-derivation (the prompt's *stability rule*), so deriving from an uncommitted UXD can leave
  settled token values sourced to text the owner later discards — settled output whose source
  was never on the record. One path, one question: this asks about no other file, and the UXD's
  existence is established above, so the only states left to tell apart are clean and not-clean.
- `<Product path>/docs/DESIGN.md` — the existing design language, if any. It is the settled
  baseline the prompt's *stability rule* reproduces; no design language here means this run is a
  first authoring.
- `<Product path>/docs/DESIGN_open_issues.md` — the existing companion, if any. **This is the
  loop's re-entry point,** and it holds two kinds of thing. The owner's inline answers are read
  here — and so is a **pointer item**, which another actor writes into the companion to name a
  **design-run** output produced away from this loop (the pointer is written there, never executed
  there). Read both, and open what a pointer names. Whether what you find may be folded, and how
  narrowly, is the prompt's *stability rule*, which carries it as a permitted delta; this file only
  tells you to read it. A pointer naming something you cannot open is an item for the owner, not a
  fold.
- `<Product path>/docs/trail/design/` — every answer the owner has already given, and their
  reasoning. Read it: a value the owner set in an earlier cycle is authorized, and changing it
  needs a fresh authorization (the prompt's *stability rule*). The prompt's *provenance gate*
  cites these files by path, and a citation you have not opened is not one. It also gives you
  the next cycle number.
- the product's own source — locate and read whatever holds its existing visual decisions, per
  *Inputs and where the files land*.
- the rest of `<Product path>/docs/` — **list the directory** and read what the bullets above
  have not already named. Skip binary assets.
- `system/experience/visual_direction.md` — the instance's **visual direction**, and the one input
  this run *inherits* from rather than derives from. It supplies three things: the **values** every
  product under this instance holds, the **markers** that say how each value is held, and
  § Overview's **direction** — how a design run decides when no value and no limit covers the case.
  An inherited value is not yours to re-choose; what a marker permits, and how an inherited value
  carries its why, are the prompt's.
- `system/experience/visual_restrictions.md` — the instance's **visual fence**: the visual limits
  every product under this instance holds, and which no product may relax. The design language is
  written inside it, and a value that breaks a fence entry is not a value you may write.

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
bar to consult beside it. Step 3's machine gate is read by the opposite rule and says so there; do
not carry that rule to this one.

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
  took one. It is explicitly **not** answering companions — no companion was read, and pointing the
  owner at open questions here sends them to a file that may not exist.

Both halts stop the run where it stands: no `DESIGN.md`, no companion, no trail copy, no commit.
Steps 2 through 5 do not run — the run's whole report is the gate's own output plus the recovery
named above, the same shape as the two halts earlier in this step.

Gather any context and constraints the owner handed you, and read them.

### Step 2 — Derive/revise the design language and write the companion (no interview)

**Gate first — detect the first closing touch before you write anything.** When a companion
existed at intake, its inline answers would resolve everything unresolved, and the file is
uncommitted (check the companion's git cleanliness in `<repo>`), this run is the first closing
touch and **writes nothing**: no derivation or fold, no trail copy, no companion rewrite. Skip
the rest of this step and Steps 3–4, and report CLOSING at Step 5. Why the close needs committed
answers is Step 4's (`--rm` mechanics); the two touches are the loop's, step 4. Everything below
runs only when this gate passes.

Derive or revise `<Product path>/docs/DESIGN.md` by applying the authoring prompt
**`prompts/rich.md`** (how to think — the design-language completeness
lens, the evidence gate, the anti-default discipline, the provenance gate, the machine gate's
bar, the stability rule, and the tone) and the template
**`<CORE>/templates/product-templates/design_template.md`** (the section shape and the token
schema as stamped). Write the companion from
**`<CORE>/templates/product-templates/design_open_issues_template.md`** (its bucket and slot
shape). The prompt's *stability rule* reads its baseline where that baseline lives — the design
language on disk at the DESIGN path, which Step 1 has already read; none there is a first
authoring, and the rule does not bind it. This step restates none of the prompt's thinking.

Set the template's `Status:` line from Step 5's DONE condition — the companion's absence — not
from your tally of answers: **Settled** only when this run ends with no companion on disk (it
removed one, or a first run grounded everything from its inputs and never wrote one); **Draft**
otherwise. Two of the three ways a run can end are settled here: the close folds every answer and
ends with the companion removed, and the first closing touch writes nothing at all — design
language included — so neither can stamp Settled beside a companion still on disk (the loop,
step 4). The third is Step 3's, and it is why this line is not final until the gate has run: the
gate can raise an open issue against a run that had nothing unresolved, and it **corrects this
line to Draft when it does**. That correction only ever runs one way, because the gate adds
residue and never resolves any — so what you write here stands unless Step 3 says otherwise.
Leave **Locked** alone — ratification is the owner's act, not yours. Bump the template's
`Version:` line on any run that changes the design language's content.

Do **not** interview. When anything lands in any bucket, write/update the companion from its
template. When nothing is unresolved, write none — an empty companion would read as OPEN and
invert the done signal: if none existed at intake, **this step** creates nothing; if one existed,
Step 4's `--rm` removes it. This step, not this run — Step 3's gate can still raise an open issue
against a run that reached it clean, and it writes the companion itself when it does.

**Consuming an answered companion.** A companion that existed at intake with at least one answer
slot filled is **consumed** — what counts as an answer slot is the companion template's, read
from its current shape, never from a name remembered here, so a template rename cannot make
filled answers read as unfilled. Consuming is three moves, in this order: copy the companion
whole (an ordinary `cp`) to the next trail cycle, *before* the fold rewrites it; fold the
owner's answers into the design language; then drop every **answered** item from the companion.

**An answered item never survives the drop.** Where the answer settles its item, the item is
resolved and gone. Where the answer leaves something unsettled, the item still drops and the
residue **re-enters as a fresh item with an empty answer slot** — a new item this run raises,
never the old one surviving. Whether an answer settles its item is the prompt's rule; this step
only moves the files that rule implies. What the drop buys is the invariant the rest of the loop
keys on: a filled slot in a surviving companion is always the owner's writing, never this run's,
so a run's own rewrite can never re-fire this detection at the next intake.

A companion with no slot filled is not consumed — no trail cycle, nothing to fold. And when the
drop resolves **every** item, the *write none* rule above owns the disk: leave the companion as
intake read it (the trail copy already holds it) and let Step 4's `--rm` remove it. No state of
this run — a halt between Step 2 and Step 4 included — ever leaves an empty companion behind.

### Step 3 — Run the machine gate

Run the format's linter against the design language this run wrote, and hold the result to the
bar in the prompt's **§ The machine gate** — the pinned invocation, and what counts as clean,
are stated there and nowhere else. **Do not read the exit code as the verdict**; the prompt owns
why. Step 4 builds no commit until this gate has run and every remaining diagnostic is routed.

Route every diagnostic this run did not fix as the prompt directs: where it allows a warning to
be accepted, the record it prescribes; otherwise an item in the companion. A run whose remaining
diagnostics are all accepted that way **meets the bar** — it carries no residue on their account,
and its status follows the companion like any other run's.

**A diagnostic routed to the companion is written here, not back at Step 2.** Where one existed,
add the item to it. Where none did — Step 2 had nothing unresolved and created none — this step
creates it from its template and **corrects Step 2's `Status:` line to Draft**. Step 4 stages it
as an `--add` like any other run's companion; the *neither* branch is not this run's.

A result that still does not meet the bar is not a reason to report finished — and not a reason
to strand the run's work either: proceed to Step 4 with the companion carrying the residue, and
report **OPEN** at Step 5.

A run that wrote no design language — Step 2's gate fired, or nothing changed — has nothing to
lint and skips this step.

### Step 4 — Commit through the builder

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and
supply its variables (`<repo>` from Step 1, the `--add`/`--rm` paths, the actor, subject/body,
the directional). The builder stages, derives `Role:`, and lays the whole trailer block; this
step never hand-writes a `git commit`, spells a trailer, `cd`s into the repo, or resolves the
directional *shape*. What follows is only the values product-design feeds it.

**A run that changes nothing builds no commit — and touches no disk.** If this run folded no
answer, changed no design-language content, and has nothing to stage, make no file change at
all: don't copy to the trail, don't rewrite the companion. (This is *not* the recipe's
`--allow-empty` marker case — product-design makes no commit at all on an empty run.) Report
the state (Step 5) and stop.

**The stage list — compose it from what this run actually did.** Pass every qualifying path in
**one** `--add` (and the companion as the one `--rm` path, when removed) — the recipe's flag
rule owns why. `<D>` below is the resolved docs directory, `<Product path>/docs` expressed
relative to `<repo>` (plain `docs` when the product *is* the repo's root; the subpath when it
sits deeper; the instance-relative path when `<repo>` is `.`).

- `--add <D>/DESIGN.md` — always, on any run that builds a commit.
- The companion, exactly one of: `--add <D>/DESIGN_open_issues.md` (something is unresolved —
  including an item Step 3's gate raised, whether it wrote the file or added to it) ·
  `--rm <D>/DESIGN_open_issues.md` (nothing unresolved *and* one existed at intake — its removal
  is the done signal) · **neither** (nothing unresolved and none existed — so nothing is on disk
  to stage either way). The owner answers *inside* the companion, so the close needs their
  answers already committed — git won't remove a dirty file, and their words aren't yours to
  commit. A dirty companion when everything would resolve marks the first closing touch: Step 2's
  gate stopped that run before any write, so it never reaches this step.
- `--add <D>/trail/design/cycle-<N>.md` — only if this run consumed an answered companion. The
  trail copy rides the same commit as the fold it precedes; neither fires without the other.

**Actor:** `--actor cdo --skill product-design` when running as the `cdo` agent (the usual
path — the subagent, or a `--bg` run launched `--agent cdo`); from an interactive `cdo:` session
with no agent named, `--role CDO --skill product-design` instead. Both derive `Role: CDO`;
why `--skill` is explicit is the recipe's to say. Subject/body, the directional, and the surface
/ co-author trailers are the recipe's variables — fill them per the recipe, not from an example
copied here.

**And `--prompt product-design/rich`**, naming the body this skill is the carrier for. A thin skill over a fat prompt is recorded by both lines and neither implies the other (`<CORE>/doctrine/governance/commit_format.md` § *`Prompt-Version:` trailer*); it takes the bare name, never a path.

### Step 5 — Close / report

Report:

- the DESIGN.md path, and the commit SHA (or that the run changed nothing and built no commit);
- on any run that ran Step 3, the **machine gate's result as counts**, read as the prompt's
  § The machine gate reads them;
- on any run that consumed an answered companion, the **trail cycle path** —
  `<Product path>/docs/trail/design/cycle-<N>.md`, the copy Step 2 made. The loop (its step 4)
  owns why that copy is the surviving record of the owner's answers; the report names it so the
  owner can verify their answers survived without opening the commit;
- the **loop status**, exactly one of:
  - **DONE** — no open-issues file remains and nothing is unresolved; on a run that ran Step 3,
    its bar is met too. The design language is complete.
  - **CLOSING** — the owner's answers resolve everything, but the companion is dirty, so this
    run was the first closing touch and changed nothing (the loop, step 4; Step 4's companion
    rule). Nothing is left to answer; the one ask is: commit the companion, then re-run — that
    re-run is the close.
  - **OPEN** — something is still unanswered, or the machine gate's bar is not met. Give a
    count per bucket, under the bucket names the companion on disk carries (its shape is
    `design_open_issues_template.md`'s, so read the names there, never from a name remembered
    here), name where they live, and name the next move: the owner answers inline, commits, and
    re-runs product-design.

Do not enumerate downstream steps; authoring the design language is this skill's whole job.
