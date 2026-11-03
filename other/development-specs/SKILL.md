---
name: development-specs
description: |
  Product Owner-posture skill for ongoing work. Takes a casual change request for an existing project and expands it into a structured change_spec.md. Uses docs/fdr.md when it exists and never requires it — a project with no FDR yet is the normal case. On a product with code, a line in the language's packet that fixes how a language-level fact renders decides the rule over the request's own rendering. States every test or check the product's nfdr.md, SDD.md or adr/ require of the change, even one the request leaves out or defers. Hands on, rather than specifying, a behaviour a product document states that the product does not have today and the request does not ask for, or that the request explicitly rules out. Halts with a report instead of asking questions when it cannot proceed.
  Use when: an existing project needs a scoped, single change — not a new app or full rewrite.
  Do not use for: new projects or first-time specs (use product-fdr instead), or changes that require updating FDR, ADR, or NFDR decision files.
  Trigger phrases: "add X to the project", "change how Y works", "update the spec for Z", "the spec needs to reflect X", "run development-specs".
license: MIT
metadata:
  version: "1.34.1"
  category: product
  risk: safe
---

# Development Specs

## Purpose

For ongoing work on an existing project: formalize a casual change request into a structured `change_spec.md` the architect can consume in `development-design`.

**Produces:** `change_spec.md` (success) or `halt_report.md` (blocked)

**The language packet is read for meaning.** On a product with code, the packet for each of the product's languages is resolved every run (Step 2). A line that fixes how the language renders a fact can decide a rule; how it says to write code cannot, and the product's own records outrank it.

**The records above the change bind it.** A test or check the product's `nfdr.md`, `SDD.md` or an ADR requires of this change is stated as a rule, even where the request leaves it out or defers it (Step 2, Step 5, Step 6). It is never left out of scope and never a halt.

**A record's unbuilt behaviour is handed on, not taken on.** A product document may state a behaviour the product does not have today. In changing mode, where that behaviour binds nothing this change adds or alters, and the request does not ask for it, the spec does not take it on: it is an `## Out of Scope` line and a `deferred_decisions.md` record gap, for `shukuba-refine` to place (Step 5, Step 6). The test is the requirement's subject. One that binds something this change adds or alters — its new or altered field, page, action or output — is a rule, as above, even where the product meets it nowhere yet, unless the request explicitly rules that behaviour out: then it is handed on too. A test or check a record requires is never handed on that way — it folds in even against the request.

## Input

**Product Owner role only.** If invoked outside a product-owner session, stop immediately, halt `wrong-posture`, and say: "development-specs requires product-owner posture. Switch? (Open a new session with the `product-owner:` prefix.)" Write `halt_report.md` carrying that reason, where § *Outputs* sends a pre-worktree halt. The refusal is a halt like every other one here, and a halt that leaves only a spoken sentence leaves nothing its caller or a later reader can check.

The invocation must supply:
- **Project name** `<project>` — the `system/projects/<project>/` folder (passed as the invocation argument). The
  product is resolved from `system/projects/<project>/project.md` → `Product path:`; `docs/fdr.md` lives
  under that path. Whether the product is its own repo is the path tool's answer (Step 4), never read off
  the value's shape.
- **Change request** — the **Request** in the `change_request.md` of the single **active** change folder
  under `system/projects/<project>/journey/tobiishi/`, discovered by the command below. The
  change key is that folder name; the project is the invocation argument — `change_request.md` carries no
  `Project:` field.

If no project name is supplied, halt with `missing-project-context`.

From the instance root, run the chain's read-only discovery command:

```bash
python3 "<CORE>/tools/chain_development.py" --list-open-changes --instance-root "$PWD" --project <project>
```

Use its JSON array as the active-key set, not a directory listing. If the command fails, report the
error and stop; never interpret failure as no active change. An empty array halts with
`no-active-change`; more than one key halts with `ambiguous-active-change`, naming every key.
Exactly one key supplies the request. Leave other files and folders untouched. This skill never
opens a change folder: `tobiishi-open` places the request before the chain runs.

## Workflow

### Step 1 — Locate project docs (fdr optional)

Read `system/projects/<project>/project.md` and take its `Product path:`, `Test command:` and `Languages:` fields — the second says whether this is a product with no code (`none`), which Step 5's preserving mode branches on, and the third is where Step 2's language resolution starts. Resolve `docs/fdr.md` under
it — `<Product path>/docs/fdr.md` (a relative `Product path` resolves from the instance root; an absolute
one is read as written, and a leading `~/` is the home directory). **Note whether it exists — its presence is optional** (see *FDR is optional* below); a
project that has not run `product-fdr` yet has no FDR, and that is the normal starting case.

**This stage resolves the product-docs path for its own reads, and each later step resolves it the
same way rather than re-deriving it from a stamped header** — the downstream stages
(`development-design` / `development-plan` / `development-implementation`) each apply this same rule
from `project.md` on their own entry. `projectDocs` is the **absolute** directory holding `fdr.md` /
`adr/` / `nfdr.md` / `SDD.md`, and it is taken from the path tool's contract once Step 4 has created the
worktree(s) — never composed from `Product path:` by hand:

```bash
python3 "<CORE>/tools/development_path.py" resolve --format json \
  --worktree "$WORKTREE" --project <project> --key <key>
```

A non-zero exit is a halt,
written on the branch as Step 6's are, with the tool's `message` in `halt_report.md`. From its output:

- `<sub>`, where the product sits inside its repository — the contract's `product_path` when that is
  relative, else `product_path` relative to `product_repo` (`.` when they are the same directory);
- `projectDocs = <product_worktree>/<sub>/docs`.

For an **in-repo** product `product_worktree` is `$WORKTREE` — the worktree is a full nested checkout, so
the instance root *inside it* is `$WORKTREE` and `projectDocs` is `$WORKTREE/<sub>/docs`. For an
**external** product it is the **product-repo worktree** Step 4 opened, **not** the product's primary
checkout; when `Product path:` *is* the product repo root (the common case — e.g.
`/Users/.../<product>`), `projectDocs` is `<product_worktree>/docs`. Anchoring `projectDocs` inside the
product worktree is what makes every downstream stage **read and write the external product on its own
isolated branch** (`PROJECT_ROOT=$(dirname "$PROJECT_DOCS")` falls inside the product worktree). Never
resolve an external `projectDocs` to the product's primary checkout, and never `$WORKTREE`-prepend it
(the instance worktree has no external code).

Compute `projectDocs` after the worktree(s) exist (Step 4) for this stage's own reads. The presence
check here runs against the product's **primary** checkout root
(`<Product path>/docs` for external, `<instance-root>/<Product path>/docs` for in-repo) — pre-worktree —
which holds the same content the branch worktree will. It records **whether** `fdr.md` is available; its
absence is not a halt.

**FDR is optional.** `<Product path>/docs/fdr.md` may be absent — a project that has not run `product-fdr`
yet is the normal starting case, not an error. When it is present, read and use it (Step 2); when it is
absent, **proceed without it** and fall back to the change request + the product's public export surface (on a product with no code, what its documents state).
Never halt on a missing `fdr.md`.

**Halt condition:** `system/projects/<project>/project.md` missing → halt `missing-project-context`. Stop
immediately, write `halt_report.md` only, where § *Outputs* sends a pre-worktree halt. Do not write any other file — not a change spec, not a flow
spec, not a placeholder. Do not infer or invent content from the change request alone. (A missing
`fdr.md`, by contrast, is **not** a halt — see *FDR is optional* above.)

### Step 2 — Read context

- Read `docs/fdr.md` fully **when it exists** (read-only — do not modify). When it is absent, skip this: the
  change request itself is the primary context, and the product's public export surface stands in for the
  behavioural baseline — or, on a product with no code, what its documents state. Never halt on its absence.
  For every requirement a product document states that bears on the change — `fdr.md`, the SRS
  where a record points to it, `nfdr.md`, `SDD.md`, an ADR — note two things: whether it binds
  something this change adds or alters, and whether the product does it today. Step 5's *A record's unbuilt
  behaviour is handed on* reads both notes. On a product with no code (`Test command: none`) its
  documents are the product, so the second note does not arise and that paragraph does not apply.
- **Read the records above the change** — `nfdr.md`, `SDD.md` and every ADR under `adr/`, each **when it
  exists** (read-only), from the same `docs/` directory as `fdr.md`. Note every test or check one of them
  requires of this change — e.g. a check that binds every new text field, or every action at the slice
  that lands it, binds this change when it adds such a field or action. Where a check's reach is stated by reference to another document — "every action SRS NFR-1 lists" — read
  that document's item to decide whether this change is inside it. Step 5 states each as a rule. An
  absent record is skipped, never a halt.
- **Resolve the language packet** — on a product with code (`Test command:` other than `none`). Walk
  `<CORE>/doctrine/engineering/languages/README.md` § *The resolution chain* from Step 1's `Languages:`
  (a stamped placeholder such as `<blank>` reads as absent), for each language the chain resolves; where it falls to inference, infer from the product's own tree at
  `Product path:`, because no worktree exists yet. Open each resolved packet's `README.md` and read every
  concern it routes. Record each language on the header's `Language resolution:` line. No packet, or no
  language resolved, is never a halt: proceed, and say so on that line.
  **What the packet may decide (changing mode).** One test, whichever packet file the line sits in: a
  packet line decides a rule only where it **fixes the rendered output itself** — how the language
  shows a type, or a value the runtime supplies, as it is shown. Where a rule pins output that renders a language-level
  fact, consult the packet of the language that fact belongs to. A line that fixes that rendering, where the request (its rule or its example) states the rendering otherwise,
  makes the rule state the packet's rendering, with the
  departure logged in `## Locked Answers`. Every other line — one saying what a value can hold, or what
  a construct does, without fixing how it is shown — decides nothing, and the request stands;
  so does a silent packet, a resolved language with no packet, or a fact from a language the chain did
  not resolve (its packet is not opened). A **language-level fact** is one the language itself determines — an annotation as written, a value the runtime supplies where the code supplies none, what a construct does — never a value or format the product chooses. A request stating such a fact's rendering does not make it product-chosen; a format is product-chosen only where the request says the product transforms the fact. An output the change asks the code to produce — an exit status, a message, the stream it goes to — is product-chosen however the code would produce it; "what a construct does" covers only a fact the rule renders from code the product already has. A packet instruction for how to write, lay out,
  build, check, test or log code never decides a rule: that is the developer's, and the PO altitude
  fence (Step 5) keeps it out. An output the rule pins (a message, its stream, an exit status) is never
  such an instruction, even where a packet line prescribes the same output; the leak is a rule naming
  how the code produces it. Step 5's `nfdr` clause admits only a mechanism an ADR, the NFDR or the SDD already
  fixes, and the packet is never that record. The product's own records outrank the packet (README
  § *Precedence*): where `docs/fdr.md` or an ADR, the NFDR or the SDD locks the rendering, the record wins. In
  preserving mode the packet is resolved and recorded, and never the source of an invariant.
- **Classify the change:** read `Category` and `Behaviour` from the request. The two-axis vocabulary is **closed** (`<CORE>/doctrine/flow/change_classification.md`; `<CORE>` is resolved at session start by the hook): `Behaviour ∈ {preserving, changing}`, `Category ∈ {feature, bug, refactor, nfdr}`. Validate before stamping:
  - **Category or Behaviour absent / unstated** → **halt** `invalid-behaviour-classification`. Never default either. Both labels are the PM's, set at `tobiishi-open` every time, so a request without one did not come through it — and a filled-in `changing` would run a preserving change in the wrong mode.
  - **`Category: refactor` with `Behaviour: changing`** → **halt** `invalid-behaviour-classification`. Refactoring preserves behaviour by definition (`change_classification.md` § *Category notes*), so the pair contradicts itself; the PM, who set it, fixes it at source.
  - **`Category: feature` with `Behaviour: preserving`** → **halt** `invalid-behaviour-classification`. A feature adds behaviour, and adding to the contract is `changing` even where nothing existing is touched (`change_classification.md` § *Behaviour-preserving — definition*). For a product with no code, a new document is that addition. The PM fixes it at source.
  - **Behaviour present and in-vocabulary** → use it.
  - **Behaviour present but out-of-vocabulary** (e.g. `additive`, `new`, `enhancement`, `breaking`) → **halt** `invalid-behaviour-classification`. Do **not** silently coerce — the producer (the PM, through `tobiishi-open`) emitted an invalid value and must fix it at source. A `feature` is `changing` by definition; "additive" describes *blast radius* (new surface, touches nothing existing), which development-design computes in §2 — it is **not** a Behaviour. This halt is pre-worktree (Step 4 hasn't run): write `halt_report.md` on the main checkout and stop, same as `missing-project-context`.

  Both axes stamp into the `change_spec.md` header; `Behaviour` selects the Step-5 drafting mode.

### Step 3 — Pre-draft checks

Before drafting, check:

1. **Multiple changes:** read and apply `<CORE>/prompts/pm_right_size.md` § *Right-size to one honest merge*, the shared sizing test used at intake. Record the sizing decision that test requires before deciding whether to halt; use it again for the drafting review in Step 6.
2. **FDR conflict** (only when `fdr.md` is present): does the request contradict a decision locked in `fdr.md`? Skip this check when no `fdr.md` exists. A request that is silent on an FDR behaviour the product lacks does not contradict it — Step 5 hands that on.

Halt if either condition is met. Write `halt_report.md` where § *Outputs* sends a pre-worktree halt, and stop. Use the template at `references/halt_report_template.md`.

### Step 4 — Create the change worktree(s)

The **change key** `<YYYY-MM-DD>_<slug>` (e.g. `YYYY-MM-DD_task-multiple-assignees`) is the active change-folder name discovered at intake — it already names the change-work folder `system/projects/<project>/journey/tobiishi/<key>/` (which holds the `change_request.md` you read). Run the create-only command with the main checkout's top level, the project and the key:

```bash
python3 "<CORE>/tools/create_change_worktree.py" \
  --instance "$(git rev-parse --show-toplevel)" --project <project> --key <key>
```

It prints one JSON object and exits `0` on success. It creates branch `<key>` and the **instance** worktree `<repo>/.worktrees/<key>` (inside the repo, so this session can write to it). `$WORKTREE` is the `worktree` of the `repos` entry whose `role` is `instance`, taken as printed: the command reads each identity back from git rather than echoing a computed path.

**External product.** The command asks the path tool (`<CORE>/tools/development_path.py`) whether the product is its own repo. If it is, the command checks **both** repositories before it changes either, then opens the **second** worktree in the product repo itself, and reports it as the `repos` entry whose `role` is `product`. Compute `projectDocs` per Step 1, from the contract's `product_repo` and `product_worktree` — the same paths that worktree was opened at. For an in-repo product there is a single worktree, and the same rule gives `projectDocs` under `$WORKTREE`.

**A non-zero exit is a halt, `worktree-not-created`.** Write `halt_report.md` where § *Outputs* sends a pre-worktree halt, using the template at `references/halt_report_template.md`, and stop. The report carries the command's `error`, `message`, `changed` and `repos` as printed. Do not retry, and do not create the branch or worktree by hand: the command's `repos` says what exists and what does not, and the operator acts on that.

**From here on, the instance worktree is this skill's working root:** every file this skill writes (`change_spec.md`, `halt_report.md`, `deferred_decisions.md`) goes under `$WORKTREE/`, and every commit runs with `git -C "$WORKTREE"` — development-specs only produces pipeline-side artifacts, which always live with the instance. The whole change arc lands on the branch, never on `main`. (Steps 1–3 ran before the worktree existed; their halts, if any, already stopped the run on `main`.)

### Step 5 — Draft change_spec.md

Write `change_spec.md` to `$WORKTREE/system/projects/<project>/journey/tobiishi/<key>/change_spec.md`.

**Drafting mode depends on `Behaviour` (Step 2):**

- **`changing`:** expand the casual request into structured content. Rules are additive/delta — state only what changes relative to `docs/fdr.md` (the current behaviour — except where it states a behaviour the product does not have, which Step 2 noted and *A record's unbuilt behaviour is handed on* decides) **when it exists**; when no `fdr.md` exists, state what changes relative to the product's current public behaviour as given by the request + the public export surface. Do not re-state the full system spec. **Hold PO altitude** (see *Hold PO altitude — changing mode* below). Template: `references/change_spec_template.md`.
- **`preserving`:** do **not** mint new CP-rules — the change adds no new behaviour. **On a card reading `Test command: none`** (a product with no code) there is no suite, no export surface and no module body, so the three sub-bullets below do not apply. Use `references/change_spec_template.preserving_docs.md` instead. Every statement the change touches is an invariant, quoted from the documents with its before-place and after-place, as `<CORE>/doctrine/flow/change_classification.md` § *A product with no code* sets out. Write a **characterization contract**: an `## Invariants` section + a `## Structural Goal` section. Template (code): `references/change_spec_template.preserving.md`. The diagnosis is already in the request — carry it; do not reverse-engineer it from code. Hold PO altitude:
  - **Characterize from four inputs only:** (1) the request/diagnosis, (2) `docs/fdr.md` **when it exists**, (3) the public export surface (the symbols each `__init__.py` re-exports), (4) a check a record above the change requires of it (Step 5, *A check a record above the change requires*). The language packet (Step 2) is resolved and recorded on the header, never the source of an invariant. When no `fdr.md` exists, characterize from (1), (3) and (4) alone. **Do not source an invariant from implementation module bodies.** Sourcing from implementation is what leaks mechanism — how a write is made atomic, internal counter names, on-disk file formats — invariants the doctrine explicitly frees (`change_classification.md`: "on-disk format internals may all change") and that over-constrain the change. This binds where an invariant comes *from*, not what may be read to check one: verifying an invariant against the tree, bodies included, is Step 6's *Claims about existing code (both modes)* pass, and it is required.
  - **Invariants = the thin fence.** Normally two lines: "the existing test suite passes unchanged" (the primary invariant — the suite *is* the contract; do not re-transcribe the scenarios it already guards) and "the public import surface is identical." Add a further invariant only if the request itself names a specific behaviour to protect, or a record above the change requires a check of it (Step 5, *A check a record above the change requires*).
  - **Structural Goal names the target, not the layout.** State the fix direction from the request (e.g. "move implementation out of `__init__.py`; `__init__.py` re-exports only"). Module/file names are development-design's decision — do not propose them, even illustratively.

**Every rule carries an identifier (changing mode).** Each rule under `## Rules` opens with a `CP-<n>` label — the name every downstream artifact cites that rule by, in `change_design.md`'s test rows, in `tl_instruction.md`'s tasks, in test assertions, and in the product's own code comments. A group heading carries no identifier; the rules under it do. A preserving spec mints no rules, so it mints no identifiers.

**The series belongs to the project, not to the change (changing mode).** Numbering continues across change units and never restarts. Take the highest `CP-<n>` already in use anywhere in the project's record — its sealed change specs under `system/projects/<project>/journey/tobiishi/trail/`, and the product `project.md` `Product path:` points at — and start one above it. A project whose record holds none starts at `CP-1`. **A number is never reused**, including one whose rule was later withdrawn. A citation already written into shipped code cannot be re-read to find out which rule it meant, so a reused number leaves that citation permanently ambiguous.

**Hold PO altitude (changing mode).** A changing spec pins *what the user observes*, never *how the code produces it*. For CLI / observable changes the line is:

- **Spec-able — pin it directly.** The observable output contract: the literal lines printed, their order, and exit codes. State the output **shape itself** — `{id}: {name}`, `— {description}` on the next line when a description is present, `No projects.` when the list is empty. Write the shape; never specify it *by reference* to another command ("same style as the `project create` confirmation").
- **Not spec-able — never anchor a rule to it.** Another command's internals (its print / f-string statement), persistence or bootstrap mechanism ("a read of a not-yet-created store bootstraps an empty store"), internal counters, on-disk file formats, in-memory structures. These are development-design / developer territory; anchoring a spec rule to them leaks mechanism, and when the referenced internal is mis-stated it ships an **inaccurate claim about existing code**.
- **Ordering keys — anchor to the output, not a hidden property.** When a rule pins an ordering, key it to a value the output actually prints (e.g. the displayed `id`), never to a property absent from the output (creation time, insertion order, on-disk row offset). If a *product-semantic* order is genuinely intended, state it **and** name its observable realization — e.g. "oldest first, realized as ascending printed `id`" — so the order is verifiable from output alone and the downstream stage knows how to realize it (rather than satisfying it by an incidental invariant). A bare "creation order" that is only realizable through a hidden property is at the wrong altitude.
- **Rule of thumb.** If a rule names another command, a storage detail, or "how" anything works, rewrite it to state the observable output directly. A spec rule must survive any reimplementation that preserves the observable behaviour.
- **Altitude binds the rationale, too.** The same fence applies to every *justification* you write, not just the rules. A `## Locked Answers` entry must explain its choice in observable terms — never by anchoring to storage or mechanism ("mirrors the natural stored order" leaks the storage model into the justification). If a rationale can only be stated by reference to how the data is stored, the rule it justifies is itself at the wrong altitude — fix the rule, not just the prose.

**Altitude under `Category: nfdr` — in either mode.** An `nfdr` change's observable *is* the toolchain: a command, its exit code, what it writes, and where. The fence above still holds, and under this category it splits on **who fixed the mechanism**:

- **Mechanism this spec would be choosing** — a tool, a flag, an on-disk format or a directory that nothing above the change fixes. Out, exactly as for a product change. State what the command must observably do and leave the choice to development-design.
- **Mechanism a record above the change already fixed** — a decision in the product's `adr/`, `nfdr.md` or `SDD.md` that this change is bound by. In, and the line stating it **names that record in the same sentence** — e.g. "runs `<tool>` in `<mode>` (fixed by ADR-<n>)". The citation is the mark. It is also what makes the naming checkable: a reader opens the record and either finds the mechanism fixed there, or has found a defect.

**A named mechanism carrying no such citation is one this spec invented**, whatever its wording. The survival test above reads against the freedom the change actually has. Where a record above it already removed that freedom, the named tool is part of the contract the change must meet rather than a leak through it — and dropping it to hold the fence would drop an upstream-fixed fact.

**A present defect may be named in any category.** Where a rule exists to remove mechanism the tree exhibits today, that mechanism is the rule's *reason*, not a choice this spec is making — and the altitude fence, which keeps a spec from choosing mechanism, does not reach it. Name it, and name **where the defect is** in the same sentence: the file and line, or the command and what it returns today. The citation is the mark, checkable the way a record citation is — a reader opens the site and either finds the defect or has found one in this spec. Unlike a record, this citation is meant to go stale: the change is what makes it false, and that is the point of stating it. Dropping it to hold the fence leaves the rule standing with its cause unstated. It holds in every category and both modes, because the permission follows from why the rule exists, never from what kind of change carries it.

**A check a record above the change requires is a rule (both modes).** Each test or check Step 2 noted from `nfdr.md`, `SDD.md` or an ADR becomes a `CP-<n>` rule, and the rule names the record and its item in the same sentence. The citation is the mark the `nfdr` clause above asks for — a mechanism a record above the change already fixed, not one this spec chose — and here it holds in every category. This holds where the request is silent on the check **and** where the request explicitly defers it to a later station or change: the rule is written either way, and the departure is logged under `## Locked Answers` as (e) with its reason. An `## Out of Scope` entry never excludes such a check, and none of this is a halt. A preserving spec mints no rules, so there the check is an `## Invariants` line instead, naming its record and item in the same sentence, and the departure is logged under `## Locked Answers` as (e) all the same.

**A record's unbuilt behaviour is handed on (changing mode, a product with code).** Decide each requirement Step 2 noted by its subject. **It binds something this change adds or alters** — a new or altered field, page, action, output or saved value — so it is a rule, whatever the product does elsewhere: the paragraph above, for a check `nfdr.md`, `SDD.md` or an ADR requires; the ordinary delta for an `fdr.md` behaviour. **It binds a behaviour this change leaves as it is** — the start, every existing page, a mode the product never enters — **and the product does not do it today, and the request does not ask for it**, so it is the product's gap, not this change's. Taking it on would make this change carry a second one nobody asked for, and the conflict would first surface as a design halt. Then the spec states **no rule on it either way**: neither builds it nor pins its absence, because a rule pinning the absence contradicts the record and fixes the gap into tests the next unit must break. Write one `## Out of Scope` line naming the record and item and citing where the product does otherwise today (the file and line), and park it in `deferred_decisions.md` as a record gap (the template's second entry shape), so `shukuba-refine` places it after the unit lands. A rule this change states on the same ground covers only what the request asks. **The request's explicit no wins over a behaviour, never over a check.** Where the request explicitly rules a behaviour out — "no feature is added", "keep it exactly as dev has it" — a behaviour a product document states is handed on the same way, whatever it binds: an `## Out of Scope` line quoting the request's words, and a record gap. A missing behaviour leaves the product unfinished, which a later change can schedule; a missing check leaves this change less safe, so a test or check under *A check a record above the change requires* still folds in, whatever the request says. Where the change carries existing code over, *the product today* is what that code does. A change that only widens *when* an existing behaviour happens — new data that now takes the existing refusal — leaves that behaviour as it is. Where the product does it in some places and not others, the subject still decides: extending it to what this change adds or alters is a rule, and the places left as they are the gap. The request *asks for* a behaviour where it states it, or names an outcome that cannot be met without it. A preserving spec mints no rules, and its Invariants follow *A check a record above the change requires* unchanged, so this paragraph does not reach it. It is not a `## Locked Answers` entry, because the spec departs from nothing the request asked. Never a halt.

**Direction ambiguity (changing mode).** A changing request may leave a material direction underspecified — append vs replace, additive vs destructive — where the request states neither. Resolve each such element by **reversibility**, never by guessing the user's intent:

- **Reversible, or a safe additive default exists** → pick the conservative (additive, non-destructive) option, write it into the Rules, and record the assumption under `## Locked Answers` **with its reason**.
- **Destructive / irreversible, or no safe default exists** → do **not** invent a rule. Leave it out of the spec and **park it** in `deferred_decisions.md` (template: `references/deferred_decisions_template.md`), one stage-stamped entry per parked element. The spec covers only what can be responsibly specified.

`deferred_decisions.md` is a **tracking collection** — it is not consumed in this run. Downstream stages append their own deferred items; after the unit lands, `shukuba-refine` reads the collection and acts on the route for each entry that has lost its owner. Create the file only when ≥1 entry is written — a parked direction element here, or a record gap handed on below; never litter an empty file.

**`## Locked Answers` is the divergence record (changing mode).** Beyond the conservative-pick assumptions above, log under `## Locked Answers` — **each with its reason** — every decision where the spec departed from or went beyond the request: (a) **resolving a contradiction** between the request and `docs/fdr.md`, (b) **locking an observable behaviour the request left implicit** (the conservative-pick is the common case), (c) **overriding a recommendation** the request stated, (d) **restating a rule to the rendering a packet line fixes**, where the request (its rule or its example) states the rendering otherwise (Step 2), (e) **stating as a rule a check a record above the change requires** — `nfdr.md`, `SDD.md` or an ADR — where the request left it out or deferred it (Step 5), or (f) **naming an existing test as changing** that the request did not name, with what it keeps asserting (Step 6, *Rules against the existing tests*). A divergence that lands without an entry turns a reviewable decision into an unexamined assumption — the failure mode the record exists to prevent. Omit the section only when the spec adds no decision beyond restating the request. Entry (e) is the one a preserving spec logs as well, for the check it states as an Invariant. This is the PO-stage analog of development-plan's `## TL Review Notes`.

The `change_spec.md` header stamps `Category` + `Behaviour` in both modes, and on a product with code a `Language resolution:` line — for each language, the language (or `none resolved`), the resolution-chain step that answered, and the packet `README.md` opened or the floor it fell to, entries separated by `;` (Step 2). What the header may **not** carry is a `Project:` field — `<CORE>/doctrine/flow/step_outcome_contract.md` § Constraints, *No `Project:` header, on either side*, states the rule for every step and every artifact.

**Out of Scope is mandatory.** For any casual request, explicitly name what the change does not address — never a check a record above the change requires of it (*A check a record above the change requires is a rule*, above). A record's behaviour the product lacks and the request does not ask for is named here (*A record's unbuilt behaviour is handed on*, above).

### Step 6 — Self-review

Re-read `change_spec.md`. Check for blocking conditions:

- **Multiple-change drift:** did drafting reveal this is actually two changes? → halt (multiple-changes). A check folded in under Step 5's *A check a record above the change requires* is never what makes it two.
- **Too vague:** are the rules too ambiguous to derive tests from? → halt (too-vague). **Does not apply when `Behaviour: preserving`** — a preserving change adds no new rules by design; its tests are the existing suite (the invariant), not new ones.
- **Direction ambiguity (changing mode):** for each material UX/behaviour direction the request left open, confirm the Step-5 split was applied — conservative-pickable (reversible/additive) elements are in the Rules and recorded under Locked Answers; un-pickable (destructive/irreversible) elements are parked in `deferred_decisions.md`, **not** invented into rules. If **every** material element is un-pickable so the spec would carry no responsibly-specifiable change → halt (`undecidable-direction`). Partial ambiguity is not a halt — park the un-pickable parts and ship what remains.
- **Ordering observability (changing mode):** does any rule pin an ordering by a property the output does not print (creation time, insertion order, on-disk offset)? Re-key it to the output-observable value (the printed `id`), or — if a product-semantic order is intended — state that order *and* its observable realization. Self-resolvable.
- **Rationale altitude (changing mode):** does any `## Locked Answers` justification anchor to storage or mechanism (e.g. "mirrors the stored order")? Rewrite it in observable terms. If it cannot be — if the only available justification is a storage fact — the rule it justifies is at the wrong altitude; fix the rule. **A justification that diagnoses a present defect is not a breach** — where the mechanism named is the tree's behaviour today that the rule exists to remove, and the line carries the citation Step 5's present-defect paragraph requires, the mechanism is the rule's *cause* rather than its content. Read the rule against the fence; do not rewrite the diagnosis that explains why it is there. Self-resolvable.
- **Claims about existing code (both modes):** open and read every file, test and symbol that a rule, an Invariant or a `## Locked Answers` entry names. Check each claim against the tree, not against the request and not against what drafting assumed. Where the tree contradicts the claim, correct the claim; where the rule stands only on the wrong claim, the rule is what changes. A claim asserted unread is a promise the developer meets as a red test, and the cheapest repair for that red test is to reverse the rule the claim was written to support. **A claim about what a command *decides* is verified by producing that verdict, not by reading the checker.** Where a rule, an Invariant or a Locked Answer asserts that a command passes or fails on a described tree, run it against that tree and record the verdict in `## Verified Claims`. **Run it under the conditions the rule itself fixes.** A harness that swaps out what the rule says must be real — a recording server where the rule demands a real start — produces a verdict about a different system, however faithfully the command ran; record the conditions beside the verdict. **The tree described is commonly one that does not exist yet** — a rule asserting what the *current* check does to a *post-change* tree is the ordinary shape, and it is verified by constructing that tree and running the check against it, never by reasoning about what the check would do to it. Reading the source establishes what the checker inspects, never what it concludes — substring anchors, counts and ordering all behave differently under a widened contract, so every quoted fact about the checker can be correct and the verdict derived from them still false. Nothing about that is particular to a category: a `preserving` spec asserting that a check passes today rests on the same derivation as an `nfdr` one, and running the command is the cheaper move in both. Where the command exists and can be run, reading it instead is the finding. Self-resolvable.
- **Language rendering (changing mode, a product with code):** for each rule that pins output rendering a language-level fact (Step 2 defines it; a value or format the product chooses is not one) — add a `## Verified Claims` row: the rule in *Claim*, and in *Verified by* exactly one of: the packet line that fixes that rendering (file and line, quoted), `packet does not fix it` (also for a resolved language with no packet), `language not resolved` (also for a language the chain did not resolve), or the packet line and the product record that overrides it; and in *What came back*, the rendering the rule now states. A line that does not fix the rendering is recorded as `packet does not fix it` even where it agrees with the request. Only a fixing line, where the request (its rule or its example) states the rendering otherwise, restates the rule (Step 2), logged in `## Locked Answers`. A rule carrying a packet instruction for how to write, lay out, build, check, test or log code is an altitude leak, unless Step 5's `nfdr` clause admits it through an ADR, the NFDR or the SDD named in the same sentence: remove it. An output the rule pins — a message, its stream, an exit status — is never a packet instruction, even where a packet line prescribes the same output; the leak is a rule naming how the code produces it. Where the rendered fact is read from code the product already has, the rule also gets its *Claims about existing code* row; the rendering row does not replace it. A spec with rendering rows and no code-claim row still writes the zero form, beside the rendering rows. Self-resolvable.
- **Rule-to-Example coverage (changing mode):** walk `## Rules` in order and name, for each rule, the `## Examples` row that exercises it. A rule with no row gets one, or gets a stated reason beside it for having none. Walk from the rules and never from the table — a rule the table omits is invisible from the table's side, which is the whole reason this pass exists. The floor is one row per rule, not a claim to have enumerated every edge; `development-design/SKILL.md` walks the rules again for those ("the Examples table is the floor, not the universe"). Self-resolvable.
- **Records above the change (both modes):** walk each test or check Step 2 noted from `nfdr.md`, `SDD.md` and `adr/`, and name the `## Rules` entry — in preserving mode, the `## Invariants` line — that states it with its record cited. One with none gets one, logged under `## Locked Answers` as (e). Then walk `## Out of Scope` and take out any entry that excludes such a check, keeping whatever else the entry excludes. Walk from the records and never from the spec — a check the request never named is invisible from the spec's side. Self-resolvable; never a halt.
- **Unbuilt record behaviour (changing mode, a product with code):** run after *Records above the change*. For each rule that cites a product document, name its subject. A rule whose subject this change adds or alters stays, whatever the product does elsewhere — the pass above put it there — unless it states a behaviour (not a check) the request explicitly rules out, which comes out and is handed on. A rule whose subject this change leaves as it is, standing only on a record's behaviour the product does not have today with the request silent on it, comes out and is handed on per Step 5's *A record's unbuilt behaviour is handed on* — and so does a rule pinning that behaviour's absence. Self-resolvable; never a halt.
- **Rules against the existing tests (changing mode):** run last, after the two passes above. For each rule, search the suite for the tests that assert the observable the rule changes, and ask whether the rule can be met without changing one the spec does not name as changing. Where it cannot, the spec contradicts itself, and the contradiction would first surface at design. Resolve it here. A rule beyond what the request asks, that no record requires, is narrowed to what the request asks. Otherwise — the request asks for it, or a record requires it (a check under *A check a record above the change requires*, or a behaviour on what this change adds or alters under *A record's unbuilt behaviour is handed on*) — the test is named as changing, with what it keeps asserting, and logged under `## Locked Answers` as (f). Self-resolvable. In preserving mode a rule needing a changed test is a behaviour delta: the *Behaviour delta* check below halts it.
- **Predicate membership (changing mode):** for each rule keyed to a *class* of inputs rather than to named values — an origin shape, a path form, a status family — name the class's boundary and confirm that a rule or a stated deferral decides every side of it. This sits in the gap between two checks above: *too vague* passes because the Examples name concrete cases and tests derive cleanly from them, and rule-to-Example coverage walks each rule to a row without asking whether the rows span the rule's domain. **An enumeration is this same check entered from the other end.** A rule that names values — three causes, four states, two origins — reads closed *because* it names them, and is open whenever the domain those values are drawn from is wider than the list. So ask what the named values are values *of*, and whether they span it. The gap is invisible from the list's side, for the same reason the check above walks from the rules and never from the table. **Where the members are not this spec's to fix, close the set by domain rather than by list:** state the domain the set must span and say the members are not fixed here. Suggesting candidate values is fine and often useful; enumerating them as *the* set is this spec deciding something it holds at the wrong altitude. A domain stated this way is a property of the requirement rather than an instruction to a later stage (`<CORE>/doctrine/flow/folder_state_handoff.md` § *A constraint handed down is stated as a property*). A predicate whose membership is undecided reads as specified and reaches the developer as a judgement call.
- **Behaviour delta (preserving mode only):** did drafting reveal the change actually alters or adds to the FDR contract or public interface — or, on a product with no code, drops, weakens or adds a statement (a pointer saying only where moved text now stands is not an addition)? → halt (`behaviour-delta-detected`) — it is not behaviour-preserving and must be reclassified. **No `## Locked Answers` entry keeps a label this contradicts:** the label is the PM's, set at `tobiishi-open`, and this halt is how it goes back. A spec that stays `preserving` over a changed signature has answered the PM's question for it.
- **FDR conflict** (only when `fdr.md` is present): does any new rule contradict a locked decision in `docs/fdr.md`? → halt (fdr-conflict). Skip when no `fdr.md` exists. A behaviour handed on per Step 5 is not a conflict: the spec states no rule on it.
- **Out of Scope empty:** if missing, add at least one explicit boundary — this is self-resolvable
- **Noun-without-verb:** named commands or flags without behavior specified? → resolve in place

Self-resolvable gaps (missing lifecycle verbs, empty Out of Scope, internal inconsistencies): fix in place. No product questions — this is an automatic pipeline.

Halt if blocking conditions remain. Write `halt_report.md` into `$WORKTREE/system/projects/<project>/journey/tobiishi/<key>/` (the worktree already exists from Step 4 — a halt from here on lands on the branch, not `main`) and stop. Use the template at `references/halt_report_template.md`.

### Step 7 — Commit outputs

Commit `change_spec.md` (and `deferred_decisions.md`, if any element was parked or handed on) on the change branch through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply its variables: `<repo>` = `$WORKTREE`, `<staged file(s)>` = `change_spec.md` (+ `deferred_decisions.md` if written), plus subject / body / **`--actor product-owner`** (the agent `launcher.md` launches this skill as — name it, never derive it) / `--skill development-specs` (this skill's own name, so `Skill-Version:` records what ran) / directional. Never hand-write `git commit` or a trailer. This skill does not advance the pipeline inboxes — that baton-pass is handled separately.

The step-outcome message this skill returns carries the standard `{ step, status, key, artifact }` —
see `<CORE>/doctrine/flow/step_outcome_contract.md`. (On a halt, the message carries `status: halt` +
`halt_reason`/`halt_report` as usual.)

The skill is done.

---

## Outputs

Written to `$WORKTREE/system/projects/<project>/journey/tobiishi/<YYYY-MM-DD>_<slug>/` — on the change branch, never `main` (see Step 4) — except a pre-worktree halt, below:

| File | Produced when |
|---|---|
| `change_spec.md` | Success |
| `deferred_decisions.md` | When ≥1 direction element is parked (changing mode), or a record's unbuilt behaviour is handed on (changing mode) |
| `halt_report.md` | Any halt condition |

**Where a pre-worktree halt lands.** The posture gate and Steps 1–3 run before Step 4 creates `$WORKTREE`, so their `halt_report.md` has no worktree path to take. It goes to the **deepest of these directories that already exists**:

| Resolved as far as… | `halt_report.md` goes to | The halts that stop here |
|---|---|---|
| the active change folder | `system/projects/<project>/journey/tobiishi/<key>/` | `invalid-behaviour-classification`, `multiple-changes`, `fdr-conflict`, `worktree-not-created` |
| the project, with no active change folder | `system/projects/<project>/journey/tobiishi/` | `no-active-change` |
| neither | the instance root | `wrong-posture`, `missing-project-context` |

**Never create a directory to hold the report.** The directory that is missing is the finding, and a run that creates one leaves a folder claiming a change is open where none is.

---

## Critical Rules

- **Halt, don't ask.** This is an automatic pipeline skill. When a blocking condition is found, write `halt_report.md` and stop. Do not ask the user for clarification.
- **fdr.md is read-only.** Never edit, append to, or overwrite `docs/fdr.md`. It is input only. All output goes to new files under `system/projects/<project>/journey/tobiishi/<YYYY-MM-DD>_<slug>/`.
- **Exact output filenames are required.** On success: `change_spec.md`. On halt: `halt_report.md`. No other filenames are acceptable (`changes.md`, `change_request.md`, `halt.md`, `flow_specs.md`, etc. are all wrong).
- **Decision files are read-only.** `fdr.md`, `adr/`, `nfdr.md`, `SDD.md` are never modified in the normal flow.
- **Worktree-first.** Step 4 takes the key discovered at intake (the active `<key>/` folder name) and runs `create_change_worktree.py`; from there the instance worktree `<repo>/.worktrees/<key>` is this skill's working root — all of development-specs's outputs (pipeline-side) go under `$WORKTREE/`, all commits run with `git -C "$WORKTREE"`, and the change arc never lands on `main`. It passes `<project>` too, so the command can ask the path tool whether the product is its own repo and, for an **external** product, open the product's own worktree; and anchor `projectDocs` inside it (Step 1) — that is what routes the downstream stages' reads **and** writes onto the product's isolated branch. Every halt before the worktree exists — the posture gate in § *Input*, and Steps 1–3 — stops on the main checkout, in the directory § *Outputs* names. Halts from Step 6 (self-review) onward are written inside the worktree, on the branch.
- **Name the product's path, never paste it.** Where `change_spec.md` refers to the product's location, it cites `project.md` `Product path:` as the field that holds it. An absolute path written into the document is a second copy of a fact that file owns. The copy drifts: a spec that pasted the product root named the product's **primary checkout**, while every stage of that change was reading its worktree under `.worktrees/<key>/`. The header carries no path at all; this rule holds the same single-sourcing in the body, where the fence around the header does not reach.
- **Rules are delta.** `change_spec.md` states only what changes relative to `docs/fdr.md` — and where `fdr.md` states a behaviour the product lacks, Step 5's *A record's unbuilt behaviour is handed on* decides. Do not re-state the full system spec.
- **PO altitude in both modes.** A spec pins observable behaviour, never mechanism. Changing mode: pin the exact output contract directly (literal lines, order, exit codes — e.g. `{id}: {name}`, `No projects.`), but never anchor a rule to another command's internals, persistence / bootstrap mechanism, counters, or on-disk formats, and never specify output *by reference* to another command's print statement ("same style as X"). Hold altitude in the **rationale** too — a `## Locked Answers` justification must not anchor to storage / mechanism ("mirrors the stored order") — and key any **ordering** to an output-observable value (the printed `id`), not a hidden property (creation time, insertion order); if a product-semantic order is intended, state it *and* its observable realization. Preserving mode holds altitude via the characterization-contract rule below. A rule that names "how" leaks mechanism — rewrite it to the observable. Under `Category: nfdr` the toolchain *is* the observable: Step 5's nfdr clause says which mechanism may be named and how naming it is marked. In any category, a test or check a record above the change requires may be named, citing that record — Step 5's *A check a record above the change requires*; and mechanism the tree exhibits today that a rule exists to remove may be named, cited to its site — Step 5's present-defect paragraph.
- **A packet line decides a rule only where it fixes the rendered output.** On a product with code, resolve each language's packet every run (Step 2) and record it on the header's `Language resolution:` line. In changing mode, a packet line that fixes how a language-level fact is rendered, from the packet of the language the fact belongs to, decides the rule where the request (its rule or its example) states the rendering otherwise, logged in `## Locked Answers`; any other line leaves the request standing, and the product's own records outrank the packet. The packet's instructions for writing, laying out, building, checking, testing or logging code stay the developer's; Step 5's `nfdr` clause admits only a mechanism an ADR, the NFDR or the SDD already fixes, never a packet's. In preserving mode the packet is never the source of an invariant. A missing packet is never a halt.
- **Out of Scope is mandatory.** Every change spec must name at least one explicit boundary — and none of them excludes a check a record above the change requires. A record's behaviour handed on per Step 5 is named here.
- **Records above the change bind it (both modes).** Read `nfdr.md`, `SDD.md` and `adr/` when present (Step 2). Every test or check they require of this change is a `CP-<n>` rule citing its record in the same sentence (Step 5), whether the request is silent on it or defers it, with the departure logged in `## Locked Answers` as (e); in preserving mode it is an `## Invariants` line citing its record, logged the same way. An Out of Scope entry never excludes one, and it is never a halt. An absent record is skipped.
- **A record's unbuilt behaviour is handed on (changing mode, a product with code).** The requirement's subject decides. One binding something this change adds or alters is a rule, even where the product meets it nowhere yet — unless it is a behaviour the request explicitly rules out, which is handed on; a check never is. One binding a behaviour this change leaves as it is, that the product does not do today and the request does not ask for, gets no rule either way — an `## Out of Scope` line and a `deferred_decisions.md` record gap instead (Step 5). Not an FDR conflict, not a Locked Answer, never a halt.
- **One change per run.** If the request covers multiple distinct changes, halt with `multiple-changes`.
- **Conservative-pick, park the rest (changing mode).** When a request leaves a material direction open, pick the safe additive option for reversible ambiguity (record in Locked Answers); park destructive/irreversible elements in `deferred_decisions.md` rather than inventing a rule. Halt `undecidable-direction` only when nothing can be responsibly specified — partial ambiguity is never a halt.
- **Record divergences in `## Locked Answers` (changing mode; entry (e) in both).** Every decision that departed from or went beyond the request — resolving a request↔FDR contradiction, locking an observable behaviour the request left implicit (conservative-pick), overriding a stated recommendation, restating a rule to the rendering a packet line fixes, where the request (its rule or its example) states the rendering otherwise (Step 2), stating as a rule a check a record above the change requires where the request left it out or deferred it (Step 5), or naming an existing test as changing that the request did not name (Step 6) — is logged in `## Locked Answers` with its reason. This is development-specs's divergence record (the PO-stage analog of development-plan's `## TL Review Notes`); a silent resolution turns a decision into an unexamined assumption.
- **Two-axis classification, closed vocabulary.** Every change carries `Category` + `Behaviour` (see `<CORE>/doctrine/flow/change_classification.md`). `Behaviour ∈ {preserving, changing}` — nothing else. A missing label, an out-of-vocabulary Behaviour (`additive`, `new`, `enhancement`, …), or a self-contradicting pair (`refactor` + `changing`, `feature` + `preserving`) **halts** `invalid-behaviour-classification` at Step 2; never default it, and never propagate it into the header. `Behaviour: preserving` switches drafting to a characterization contract (invariants + structural goal) — never mint new-behaviour CP-rules for a preserving change. Characterize it from the request + `docs/fdr.md` (when present) + the public export surface + any check a record above the change requires (the language packet is recorded, never the source of an invariant) — or, on a product with no code, from the request and the documents' own statements (`change_spec_template.preserving_docs.md`); never *sourced* from implementation bodies (that leaks mechanism the change is free to alter) — reading them to verify a claim is Step 6's *Claims about existing code (both modes)* pass, and is required.
