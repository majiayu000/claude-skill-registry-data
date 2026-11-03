---
name: product-prd
description: CPO-posture skill that authors a project's PRD — the product source of truth and the head of the definition sequence. Requires CPO posture (halts if invoked outside a cpo session or the cpo agent). Non-interactive by design — it drafts the whole PRD best-effort from the project's inputs and a product diagnostic, and instead of interviewing live it surfaces everything it can't settle into a companion open-issues file (open issues, choices to confirm, directives) for the owner to answer async. On re-run it consumes both files, retires the owner's answered file whole to a permanent trail, folds their answers into the PRD, and when nothing is left unresolved it clears the companion — its absence means the PRD is done. The skill resolves where the files land from the project's Product path. Use when authoring, continuing, or revising a product's PRD. Do not use for per-change specs (development-specs), the project's Agari (project-agari), or downstream documents (SRS / SDD / Delivery Plan / FDR / ADR / NFDR).
license: MIT
metadata:
  author: Eyal Golan
  version: "4.16.0"
  created: "2026-07-09"
  category: product-definition
  tags: prd, cpo, product-definition, product-source-of-truth, upstream-chain
  risk: safe
---

# product-prd

## Purpose

Author a project's **PRD**: the product source of truth — the product-facing **what and
why** that engineering, design, and architecture build on. It is the **head** of the
definition sequence (`<CORE>/doctrine/setup/setting_up_a_project.md`, which owns that
sequence and is not restated here); the CTO derives the SRS from it and the CDO the UXD,
both written off it in parallel.

This file is the **orchestrator**: posture, the file loop, and the commit mechanics. **How to
author** — the diagnostic, the tag contract, and the twelve authoring principles — is the
authoring prompt **`prompts/rich.md`**, applied at Step 2; a principle
referenced below by number lives there. The PRD's **section shape** is the template
**`<CORE>/templates/product-templates/prd_template.md`**. Neither is restated here.

## Posture

**CPO role required.** If invoked outside CPO posture (neither a `cpo:` session nor the
`cpo` subagent), stop and say: *"product-prd requires CPO posture. Switch? (Open a session
with the `cpo:` prefix, or run the `cpo` subagent.)"* Do not shed the role. Take care not to
confuse the CPO with the delivery-tier **Product Owner**, who writes per-change specs
downstream — a different role that only shares the word "product".

**Non-interactive.** Throughout, **the owner** is the person whose product this is — the one
who directed the project and whose taste calls the PRD is settling. You work *with* them, but
through files, not a live interview:

- **Draft, don't ask.** Draft the whole PRD best-effort from the inputs. Never open a
  blank-page interview; never block waiting.
- **Surface, don't interrogate.** What the inputs can't settle goes to the **open-issues
  file** in one of three buckets:
  - **Open issues** — a product question you have no basis to decide.
  - **Choices to confirm** — a decision you drafted that is the owner's to sign off.
  - **Directives** — an action outside your own reach to perform (open a file elsewhere,
    change something outside the product, get a reply only a person can give). **Routing test
    against the prompt's principle 11, first:** can your own tools settle this — the vendor's
    own docs, a web search, a research query? If yes, it was never a directive — principle 11
    owns it: open the source now and fold the fact into the PRD, tagged by what you found, and
    it never reaches this bucket. Only what your tools genuinely can't reach — a private
    negotiation, a number no published source carries, an answer that needs a specific person's
    reply — is a directive. **A directive is a gate, not a blocker.** The owner may not be able
    to take the action now, and the product doesn't wait on the *action* to be *defined* — so
    the deferred **action** never blocks DONE. The **directive itself** does, until confirmed:
    an unconfirmed gate is an OPEN item like any other (Step 4) — confirming it, not performing
    it, is what clears it. Surface it *as a gate to confirm*: name the action, who performs it,
    and **what it gates** — what it blocks / when it is "reached" (before v1 listing, before a
    Phase-2 commitment). The owner **confirms the gate** — a light sign-off that this is a real
    gate worth recording, **not** the performing of the action, which stays deferred. On the
    run after it is confirmed, the gate moves into the PRD body under the recorded-gates
    heading the prompt's principle 9 names and drops from here; whether the owner has *started*
    the action makes no difference — the only gate into the body is the confirmation, and you
    never move it on your own initiative. "Ask the vendor's account rep for their unpublished
    SLA terms" is the directive (their docs don't carry it, so principle 11's tools can't); it
    is recorded as a gate on "the rep's SLA terms" the moment the owner confirms it, whether or
    not they have picked up the phone.

  Never a bare menu: a choice leads with your drafted answer and why; an open issue leads
  with your reasoning and what would settle it; a directive names the action, who performs it,
  and what it gates, and asks the owner to confirm it. If you have a lean, it's a choice — the
  buckets split on whether you have a basis, not on how sure you feel.
- **The owner owns the taste calls.** Scope, target users, what "done enough" means. Your
  job is the draft, the diagnostic, the reasoning, and the honest recommendation.

## What the PRD is

The product-facing what and why — the **how** (architecture, system requirements, delivery
sequencing) belongs downstream. Updated in place with a version bump; never forked. **Read
cold**: every statement stands alone, and what is out of scope is as load-bearing as what
is in.

## The files and the loop

Resolve the product from the directed project's `system/projects/<name>/project.md`
`Product path:` — a caller names the *project*, never the paths. (Relative → inside the
instance repo; absolute → the product's own repo.) If `Product path:` is still an unfilled
placeholder, stop and say so — everything below resolves from it, including where an open issue
would be written, so there is nowhere to record the problem and nothing to author against.
Never invent the path.

| File | What it is |
|---|---|
| `<Product path>/docs/PRD.md` | The PRD. Permanent. |
| `<Product path>/docs/what_left.md` | The product's what-left list. |
| `<Product path>/docs/PRD_open_issues.md` | The companion — *open issues*, *choices to confirm*, *directives*. Transient. |
| `<Product path>/docs/trail/prd/cycle-<N>.md` | The owner's answered files, retired whole. Permanent. |

**Cycle numbering:** `N` is one higher than the **highest** `cycle-<N>.md` already in
`trail/prd/` — list the directory and take the max, so a removed or renamed cycle can't make
you collide with an existing one. The first is `cycle-1.md`; create `trail/prd/` if it isn't
there. Never overwrite an existing cycle.

**The loop, repeated until clean:**

1. You draft/update the PRD and write the open-issues file with what you couldn't settle.
2. The **owner answers inline** and re-runs the skill.
3. You **copy their answered file whole to the next trail cycle**, fold the answers into the
   PRD, and rewrite the open-issues file with only what's still unresolved. This is the
   ordinary cycle — something survives the fold. A run where nothing would is step 4's, and
   step 4 alone says what it may touch.
4. When the answers resolve everything, the run is the close: one run that folds, copies the
   answered file to the trail, and **removes** the open-issues file instead of rewriting it.
   **Its absence is the done signal.** The close has a precondition the ordinary cycle does
   not: the owner's answers must already be committed (Workflow Step 3 owns the rule and
   why). Re-entry is inline answers, so the first closing touch normally finds them
   uncommitted — and then it **changes nothing at all**: no fold, no trail copy, no rewrite,
   no commit; the companion survives intact, answers and all, for the owner to commit. It
   reports the state and asks for that commit; the re-run after it is the close, start to
   finish, in one run. That stop is a report with an ask, not a live interview. What
   "unresolved" means for a directive is the confirmation, not the action — Posture, above,
   owns that distinction and where a confirmed gate goes.

Step 3 is why the trail exists. Folding rewrites the open-issues file, and the close removes
it — so without the trail the owner's answers are destroyed twice, and their reasoning for a
decision survives only in git history. The trail costs one flag on the same commit and makes
every owner answer permanently citable. It is the skill's job; the owner never manages it.

## Workflow

### Step 1 — Identify the project, intake, read current state

Resolve the directed project's real product before considering a what-left addition. Expand a home-relative binding before resolving it. Establish which repository will receive the PRD commit. Express the PRD and what-left destinations relative to that repository, including the product's subpath when the product is nested. A nominal binding must receive no list write. Preserve the existing stop for an unresolved binding. If the list is absent, leave it absent. First PRD authoring must not create or update a what-left list through this revision capability.

```sh
git -C "<expanded Product path>" rev-parse --show-toplevel
```

- `system/projects/<name>/project.md` — the binding. Resolve the paths from `Product path:`,
  then read its input pointers **in this order**, because they do not rank equally:
  - **`Product request (primary input):`** — when present, *this* is what you author from.
    It is the consolidated, checked statement of the product.
  - **`Source material (raw archive):`** — the unedited material behind it. Consult it for
    background, but it is **older than the product request and may be stale in exactly the
    way that matters** — the archive is where a superseded mechanism or an abandoned
    decision still reads as current. Where the two disagree, **the product request wins**,
    and the archive's version is not a fact about the product (see the prompt's
    principle 10).
  - Where a project names only the archive, that is your input — and everything in
    principle 10 applies to it with full force.
  - Where a project names **neither**, you have no stated input. Whatever the owner handed you
    directly is the material; if there is nothing, stop and ask what to author from rather than
    authoring a PRD out of the project card.

  If more than one project exists and the target is ambiguous, ask which — that is the one
  question worth blocking on, because guessing it makes every later answer wrong.
- `<Product path>/docs/PRD.md` — the existing PRD, if any.
- `<Product path>/docs/what_left.md` — the product's what-left list, if any.
- `<Product path>/docs/PRD_open_issues.md` — **the loop's re-entry point**: the owner's
  inline answers are here. An answer marked *(the session's suggestion, accepted by the owner as shown)* or *(the
  session's suggestion, edited by the owner)* came from `project-setup`'s interview: it is the
  session's suggestion, which the owner accepted, so weigh it as that rather than as the owner's
  own words — except that in an edited one, what the owner changed is theirs — and never copy the
  mark into the document. The same marks reach the trail's first cycle; read them there the same
  way.
- `<Product path>/docs/trail/prd/` — every answer the owner has already given, and their
  reasoning. Read it: a value the owner confirmed in an earlier cycle is authorized, and
  changing it needs a fresh authorization (the prompt's principle 7). It also gives you the
  next cycle number.
- `system/projects/<name>/agari.md` — the project's Agari: the product's "done". Read it for
  what you're authoring toward. Whether it has been declared yet decides the commit's
  directional line (Step 3) — if the file is still the unfilled placeholder it shipped with,
  no Agari exists yet.

Retain the prior PRD and the existing what-left list exactly as read. Read the proposed PRD revision and the relevant product code. Retain the owner's answers and earlier confirmations needed to establish authorization. Complete qualification before changing any revision output.

### Step 2 — Draft the PRD and write the open-issues file

**Gate first — detect the first closing touch before you write anything.** When a companion
existed at intake, its inline answers would resolve everything unresolved, and the file is
uncommitted (check the companion's git cleanliness), this run is the first closing touch and **writes nothing**: no PRD draft or fold,
no trail copy, no companion rewrite. Skip the rest of this step and Step 3, and report CLOSING
at Step 4. Why the close needs committed answers is Step 3's (`--rm` mechanics); the two-touch
design is the loop's, step 4. Everything below runs only when this gate passes.

Apply the existing first-closing-touch and empty-run gates to the what-left list as well as the PRD, companion and answer trail. A list addition must not bypass either gate or turn an otherwise empty run into list maintenance. Preserve the existing whole-answer trail and companion lifecycle. When qualifying additions would change an existing list, check the destination against the entry shape and list-state requirements before writing any revision output. If the destination is malformed, report the actual condition and stop without a file write or commit. Do not repair the list through this revision. When no addition qualifies, list validation must not create a repair duty or block an otherwise authorized PRD revision.

Apply the authoring prompt **`prompts/rich.md`** (how to think — the
diagnostic, the tag contract, and the twelve authoring principles;
**The PRD author's revision instructions**) and the template
**`<CORE>/templates/product-templates/prd_template.md`** (the PRD's section shape). Write the
companion from **`<CORE>/templates/product-templates/prd_open_issues_template.md`** (its
bucket and stanza shape). Run the diagnostic as you draft, and sort every product question:

- **Answerable from the inputs** (including answers now in the open-issues file or the
  trail) → resolve it into the PRD body.
- **Anything else** → the matching bucket in the companion file (Posture, above). A choice to
  confirm is drafted into the PRD *and* listed; an open issue is listed only; a directive is
  listed as a gate to confirm — its confirm-then-move-to-body lifecycle is Posture's, not
  restated here.

Set the template's `Status:` line from the Step 4 DONE condition — the companion's absence —
not from your tally of answers: **Settled** only when this run ends with no companion on disk
(it removed one, or a first run settled everything from its inputs and never wrote one);
**Draft** otherwise. The two conditions cannot diverge: the only run that folds every answer
is the close itself, which ends with the companion removed, and the first closing touch writes
nothing at all — PRD included — so no PRD is ever stamped Settled beside a companion still on
disk (the loop, step 4). A **recorded gate in the PRD body does not hold Draft** (it is
resolved: confirmed and moved). Leave **Locked** alone — ratification isn't yours.
Bump the template's `Version:` line on any run that changes the PRD's content.

As you draft, critically review your input itself — don't just author from it (the prompt's
principle 11), using the tools to check what the inputs can't settle. Then run the prompt's
principles over what you've written — the write-time tests as you draft, and its finished-draft
walks after. The principles are the prompt's; this step does not restate them.

**Publishing one or more qualifying additions**

Preserve the list's existing heading and lead sentence. Preserve every existing entry's exact wording, fields, missing-at commit and relative order. Append the qualifying additions after the existing entries. If the list holds only the empty marker, replace only that marker with the additions. Check the proposed result against the entry shape and entries-state requirements before publication. Add no evidence field to an entry.

`<CORE>/templates/product-templates/what_left_template.md`, **The single source of the what-left file's shape**; `<CORE>/doctrine/setup/kensaiapp_structure.md` § *The what-left file*, list-state table.

**The wanted statement of a qualifying addition**

> {wanted statement}

**The source of an addition in a PRD section without a named item**

> PRD § {section heading}

**The source of an addition in a PRD section with a named item**

> PRD § {section heading}, **{item name}**

**Publishing a revision with no qualifying addition**

Leave the what-left list byte-for-byte unchanged when no addition qualifies. Do not include the list in this run's stage set. Report the actual reason for no addition.

### Step 3 — Commit through the builder

Commit through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and
supply its variables (`<repo>`, the `--add`/`--rm` paths, the actor, subject/body, and the
directional). The builder stages, derives `Role:`, and lays the whole trailer block; this step
never hand-writes a `git commit`, spells a trailer, `cd`s into the repo, or resolves the
directional *shape* — the recipe owns all of that. What follows is only the values product-prd
feeds it.

**A run that changes nothing builds no commit — and touches no disk.** If this run folded no
answer, bumped no PRD version, and has nothing to stage, make no file change at all: don't copy to
the trail, don't rewrite the companion. (This is *not* the recipe's `--allow-empty` marker case —
product-prd makes no commit at all on an empty run.) Report the state (Step 4) and stop.

**The stage list — compose it from what this run actually did.** Whatever qualifies below, pass it in
**one** `--add` (and the companion, when removed, as the one `--rm` path) — never a flag per path; the
recipe's flag rule owns why. `<D>` is the resolved docs directory — `<Product path>/docs` expressed
relative to `<repo>`: plain `docs` when the product sits at its repo's root, the subpath down to it when
the product sits deeper inside a larger repo, and the instance-relative path when `<repo>` is `.`. Derive
it from the resolved `<repo>` below; never assume the product is its repo's root. Every path named
must exist (or, for `--rm`, have existed), or the builder halts without committing.

- `--add <D>/PRD.md` — always, on any run that builds a commit.
- `--add <D>/what_left.md` — only when additions were published.
- `--add <D>/trail/prd/cycle-<N>.md` — **only if you consumed an answered companion this run**
  (it existed at intake and you copied it). The trail copy is an ordinary `cp` — made before you
  rewrite or remove the companion, and sharing *one* trigger with this `--add`: neither fires
  without the other. That holds on the close too: the closing run is the only run that copies the
  final answered file — the first closing touch copied nothing, because it changed nothing (the
  loop, step 4). A first run copies nothing.
- The companion, exactly one of: **`--add <D>/PRD_open_issues.md`** (something is unresolved) ·
  **`--rm <D>/PRD_open_issues.md`** (nothing unresolved *and* a companion existed at intake) ·
  **neither** (nothing unresolved and none existed). The owner answers *inside* the companion, so
  the close needs their answers already committed — git won't remove a dirty file, and their words
  aren't yours to commit. A dirty companion when everything would resolve marks the first closing
  touch — Step 2's gate stopped that run before any write, so it never reaches this step: nothing
  to stage, no commit to build (the loop, step 4 owns the two touches).

Include the revised PRD and every published what-left addition in one builder commit in the repository receiving the PRD. Include the companion and answer-trail outputs the revision actually produces. Include the list in the stage set only when additions were published. Use the repository-relative destinations established at intake. Do not commit the PRD first and defer its qualifying list additions. Keep each addition's absence evidence in the revision report and the same commit's body. Keep checking transcripts out of the PRD body.

**The values product-prd supplies:**

- **`<repo>`** — `git -C "<expanded Product path>" rev-parse --show-toplevel` (Step 1).
- **actor + skill** — **`--actor cpo --skill product-prd`** when running as the `cpo` agent (the usual
  path: the `cpo` subagent, or a background run launched `--agent cpo`). From an interactive `cpo:`
  session with no agent named, pass **`--role CPO --skill product-prd`** instead. Both derive `Role: CPO`;
  the explicit **`--skill product-prd`** is required to stamp `Skill-Version:` now that provenance is
  explicit-only — the actor no longer derives it.
- **`--directional`** — the PRD is authored in the executive phase, before any 宿場 station or 上がり
  Agari exists, so it is **`Agari: none — <what this run did>`**. (The recipe's variable #4 owns
  *why*; `Agari: <name>` becomes reachable only on a later *revision* run made after the project's
  Agari has been declared.)

**And `--prompt product-prd/rich`**, naming the body this skill is the carrier for. A thin skill over a fat prompt is recorded by both lines and neither implies the other (`<CORE>/doctrine/governance/commit_format.md` § *`Prompt-Version:` trailer*); it takes the bare name, never a path.

Subject/body and the surface / co-author trailers are the recipe's variables — fill them per the
recipe, not from an example copied here.

### Step 4 — Close and report

Report the PRD path, the loop status, and — on a run that built a commit — its SHA. (A run that
changed nothing built no commit and has no SHA to report; give the path and status only.)

- **DONE** — the companion file is gone. Nothing is unresolved. Recorded gates may live in the
  PRD body — those are resolved (owner-confirmed and moved), not outstanding.
- **CLOSING** — the owner's answers resolve everything, but the companion is dirty, so this run
  was the first closing touch and changed nothing (the loop, step 4; Step 3's companion rule).
  Nothing is left to answer; the one ask is: commit the companion, then re-run — that re-run is
  the close.
- **OPEN** — something is still unanswered: N open issues, M choices to confirm, K gates to
  confirm. Name the counts and where they live; the owner answers or confirms inline and re-runs
  you.

**Report DONE when the companion is gone, even while the PRD records gates whose external
action is still deferred** — per Posture's confirm-not-perform distinction, a recorded gate is
owner-confirmed and openly unperformed, which is the honest state, not a settled PRD stamped
over an action nobody did.

Retain the PRD location, loop status and actual commit reporting. Report the what-left destination when one was resolved. For each addition, report the wanted thing, PRD source, authorization and absence evidence. For each exclusion, report the actual reason. If no addition occurs, report the actual skip or gate condition. Report no revision commit when the run made none. Do not report real-product acceptance without the actual required proof results.

#### The revision report

**DONE after a committing revision**

> PRD: {PRD location}. DONE: no companion remains ({companion check}). Revision commit: {revision commit}.

Variables: `{PRD location}` is the resolved PRD location. `{revision commit}` is the actual builder commit SHA containing the revision. `{companion check}` is the actual companion existence command with its result.

**OPEN after a committing revision**

> PRD: {PRD location}. OPEN at {companion location}: open issues {open issue count}, choices to confirm {choice count}, gates to confirm {gate count}. Answer or confirm inline in {companion location}, then re-run. Revision commit: {revision commit}.

Variables: `{PRD location}`, `{companion location}` and `{revision commit}` are the actual resolved locations and builder commit SHA. `{open issue count}`, `{choice count}` and `{gate count}` are the observed counts for their named buckets.

**DONE on a run that changed nothing**

> PRD: {PRD location}. DONE: no companion remains ({companion check}). No file was changed and no commit was made ({run evidence}).

Variables: `{PRD location}` is the resolved PRD location. `{companion check}` is the actual existence command with its result. `{run evidence}` records the before-and-after output comparison and HEAD check with their actual results.

**OPEN on a run that changed nothing**

> PRD: {PRD location}. OPEN at {companion location}: open issues {open issue count}, choices to confirm {choice count}, gates to confirm {gate count}. Answer or confirm inline in {companion location}, then re-run. No file was changed and no commit was made ({run evidence}).

Variables: `{PRD location}` and `{companion location}` are the actual resolved locations. `{open issue count}`, `{choice count}` and `{gate count}` are the observed counts for their named buckets. `{run evidence}` records the before-and-after output comparison and HEAD check with their actual results.

**CLOSING on the first closing touch**

> PRD: {PRD location}. CLOSING: the owner's answers in {companion location} resolve the remaining items. The answered companion has uncommitted changes ({companion status check}). No file was changed and no commit was made ({run evidence}). Commit {companion location}, then re-run to close the PRD.

Variables: `{PRD location}` and `{companion location}` are the actual resolved locations. `{companion status check}` is the actual cleanliness command and its result. `{run evidence}` records the before-and-after output comparison and HEAD check with their actual results. This state requires the observed first-closing-touch condition.

**One qualifying addition, repeated whole for each addition**

> Added to the what-left list at {list location}: {wanted statement} (revision commit {revision commit}). PRD source: {PRD source}. Authorization: {authorization source}. Missing at: {checked commit}. Absence check: {check command}. Actual output: {check output}. Exit status: {check exit status}. Check conditions: {check conditions}. Main ancestry check: {ancestry command}. Actual output: {ancestry output}. Exit status: 0. The PRD revision and this addition share revision commit {revision commit}.

Variables: `{list location}` is the resolved list destination. `{wanted statement}` is the whole qualified want. `{PRD source}` names the revised PRD section and item, when present. `{authorization source}` identifies the actual authorization and any required confirmation. `{checked commit}` is the product commit used for the absence check. `{check command}`, `{check output}`, `{check exit status}` and `{check conditions}` are the actual command, output, exit status and conditions of the absence check. `{ancestry command}` and `{ancestry output}` are the actual command and output establishing that main carries `{checked commit}`. `{revision commit}` is the actual commit containing both changes. An output with no bytes is rendered as `No output.`; multiline output remains whole.

**A candidate excluded while another candidate is added**

> No entry was added for {wanted statement}: {exclusion reason} ({exclusion evidence}).

Variables: `{wanted statement}` is the assessed candidate. `{exclusion reason}` states the actual reason that candidate was excluded. `{exclusion evidence}` carries the supporting source locator or the actual check command and result. The reason is supplied by qualification, not selected from a fixed menu.

**An existing list receives no addition**

> The what-left list at {list location} was left byte-for-byte unchanged and was not staged ({list checks}). No addition qualified because {skip reason} ({skip evidence}).

Variables: `{list location}` is the resolved list destination. `{skip reason}` covers the actual condition, including multiple exclusions when needed. `{skip evidence}` names the supporting source or actual check result. `{list checks}` records the actual byte comparison and stage-set check with their results.

**No existing list**

> No what-left list exists at {list destination} ({existence command}: {existence result}). No list was created ({list write check}).

Variables: `{list destination}` is the resolved destination that was checked. `{existence command}` and `{existence result}` are the actual existence check and its output or exit status. `{list write check}` is the actual end-of-run existence check and result.

**A nominal product binding**

> The directed project's product binding is nominal ({binding evidence}). No what-left destination was used and no list was written ({list write evidence}).

Variables: `{binding evidence}` is the opened binding source with the actual value and the evidence establishing its nominal role. `{list write evidence}` records the actual publication destinations and unchanged list state.

**An unresolved product binding**

> The directed project's real product could not be resolved ({resolution evidence}). No what-left destination was established and no list was written ({list write evidence}). Resolve the product binding before re-running.

Variables: `{resolution evidence}` is the actual resolution command and result, or the opened binding source showing the unresolved value. `{list write evidence}` records the actual publication destinations and unchanged list state. This message supplements the existing unresolved-binding stop.

**First PRD authoring**

> No what-left addition was attempted because this run first authored the PRD ({intake evidence}). No list was created or updated ({list write evidence}).

Variables: `{intake evidence}` is the actual intake check showing that no prior PRD existed. `{list write evidence}` records the actual publication destinations and unchanged list state.

**A publication gate prevents all changes**

> No what-left addition was published because {gate reason} ({gate evidence}). No file was changed and no commit was made ({run evidence}). Follow the publication gate at {gate source} before re-running.

Variables: `{gate reason}` names the actual publication gate. `{gate evidence}` records the source or actual check result establishing it. `{gate source}` locates the existing gate with a stable anchor. `{run evidence}` records the before-and-after output comparison and HEAD check with their actual results.

**A qualifying revision encounters a malformed list**

> The what-left list at {list location} cannot receive the qualifying additions: {malformed condition} ({shape source}; {state evidence}). No file was changed and no commit was made ({run evidence}). Correct the list's malformed state before re-running this revision.

Variables: `{list location}` is the resolved destination. `{malformed condition}` names the actual shape or state defect. `{shape source}` is the existing shape or state owner with a stable anchor. `{state evidence}` identifies the observed content supporting the finding. `{run evidence}` records the before-and-after output comparison and HEAD check with their actual results.

Authoring the PRD is this skill's whole job — don't enumerate what comes after.
