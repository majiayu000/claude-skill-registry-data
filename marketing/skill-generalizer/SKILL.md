---
name: skill-generalizer
description: >-
  Generalize a skill beyond its origin: strip names, parameterize case-local
  constants, move domain-locked values to opt-in side files, split oversized
  bodies into load-rule'd routers, enforce ≤50-word descriptions. Use for
  generalize skill, de-specify skill, make skill generic, skill audit for
  specificity, skill consistency review, split region-specific rules into
  reference files.
license: Apache-2.0
compatibility: opencode
metadata:
  harness: "opencode"
category: OpenCode Meta
---

# Skill generalizer

Turn a skill that grew around one project, one source document, or one person into a
transferable method. The test of done: **a stranger with a different project can execute
the document without knowing the origin story, nothing in it names the origin, and
nothing in it assumes a jurisdiction or domain the reader never named.**

The failure it fixes: skills accrete. Each real case leaves an anecdote ("on X's artefact,
the calibration bar sat outside the clip"), a proper noun, a magic number tuned to one
artefact, a path to files that ship with one checkout, and a block of rules that only
hold in one jurisdiction. Every one of those raises the cost of the next reader and
lowers the skill's reach — while the underlying LESSON was general all along.

A second, independent failure: skills gain **weight** as well as specificity. The
entire main document enters the model's context the moment the skill loads — detail
needed at one step is dead weight at every other, and an oversized body costs more
context than it returns. A generalization pass that fixes what a skill says but not
how much of it loads is only half done.

## The audit is a decision tree, not a rewrite

Every pass below is an independent **detector** over the skill document; every finding
gets exactly **one disposition**. Run the detectors in order, then close with the
verification gate. The audit is built for modular enhancement: when a new failure mode
appears in practice, add a detector — signature, mechanism, test, disposition — and
wire its anti-pattern; never special-case content inline.

```mermaid
flowchart TD
    S["scan the document"] --> Q1{"names the origin?"}
    Q1 -- yes --> A["(a) generalize: keep signature + mechanism + test, drop the name"]
    Q1 -- no --> Q2{"true only in one jurisdiction / domain vertical?"}
    Q2 -- yes --> D["(d) modularize: opt-in side file + load rule"]
    Q2 -- no --> Q3{"conventional, travels with a confirm-locally note?"}
    Q3 -- yes --> B["(b) reference pin"]
    Q3 -- no --> C["(c) delete"]
    A --> V["contradiction + cross-reference + verification gates"]
    D --> V
    B --> V
    C --> V
    S --> W{"body weight: would a split benefit the skill?"}
    W -- yes --> E["(e) routerize: contract stays, detail moves behind load rules"]
    W -- no --> V
    E --> V
```

## Workflow — a detector per pass, then verify

1. **Named-entity scan**: grep the document for capitalized proper nouns, people,
   clients, source-document and page/section identifiers, brand and trade names. Each
   hit becomes exactly one of:
   (a) a generalized rule — keep the signature, the mechanism, the detection test; drop
   the name; (b) a conditional domain convention — moved to a "reference pins" section
   with a lead line telling readers to discover local equivalents and record deviations;
   (c) deleted; or (d) modularized into an opt-in side file (pass 3). A proper noun
   survives only in the skill's own identity (name/description).
2. **Anecdote → rule**: "on X's artefact, Y happened" carries three transferable parts —
   the SIGNATURE (what it looked like), the MECHANISM (why it happens), and the TEST
   (how to detect it next time). Rewrite the anecdote as signature + mechanism + test.
   Keep numbers that generalize (ratios, tolerances, order-of-magnitude bounds);
   parameterize or delete numbers that were tuned to one artefact.
3. **Domain-modularization scan**: find blocks whose truth is locked to one jurisdiction,
   market, or domain vertical — regulations, building/fire/electrical codes, tax or
   compliance rules, label glossaries, market conventions ("saleable area includes
   balconies"). Test: would a practitioner outside that jurisdiction or vertical find
   the block wrong or irrelevant? If yes, move it to an opt-in side file —
   `references/<domain>/<code>.md` (e.g. `references/regions/sg.md`) — keeping in the
   main document only (i) the domain-GENERAL principle it instantiates ("exit-route main
   doors are commonly fire-rated self-closing by regulation — values are regional") and
   (ii) a load rule ("when the task's context names this domain, read the file and cite
   it in the ledger; if no file exists, discover locally and consider contributing
   one"). Side-file contract (domain-value files, disposition (d) only): fixed section
   skeleton, every value carrying a citation or a verify-locally note, a header inviting
   contributors to copy the structure for a new code, and NO method content — phase
   files (e) and templates/ carry mechanics and artifacts by design, each behind its own
   WHEN+WHAT load rule. The main document stays trigger-neutral: loading is the
   reader's informed decision, never a side effect of triggering the skill.
4. **Constants audit**: every hard-coded number is one of — universal (schema enums, unit
   conversions, protocol contracts → keep unconditional); domain-conventional (typical
   dimensions, default heights → keep in the conventions/pins section, explicitly
   conditional); case-local (tuned to one artefact → parameterize with its rule, or
   delete).
5. **Path/reference audit**: file paths to worked examples, datasets, fixtures → either
   ship them with the skill or mark them as source-repository artefacts. The skill must
   not promise files it does not carry.
6. **Load-weight audit — routerize when it benefits the skill**: SIGNATURE — inline step
   mechanics, vocabularies, worked-example walkthroughs, or human usage docs in the main
   document; a body near or over ~10KB / ~2.5k estimated tokens. MECHANISM — the whole
   body is injected the moment the skill loads; detail needed at one step is dead weight
   at every other, so an oversized body costs more context than it returns. TEST —
   estimate tokens (words × 1.3 or chars ÷ 4) and grep for section shapes:
   multi-paragraph step mechanics, long command vocabularies, example walkthroughs,
   install/usage documentation. DISPOSITION — restructure into the router pattern, when
   it benefits the skill (judgment first, ceiling second): the main document keeps the
   CONTRACT — identity and ≤50-word description, a one-screen "What I do" summary, a
   side-file load table (`Read | When | Use`, or step | file | mode | skip-when),
   cross-cutting hard rules as one-liners that point at the file carrying the detail,
   and the gates. Step mechanics move to `references/phases/<id>-<name>.md`, read only
   when the current step names that file — never preloaded; topic detail and gotchas
   move to `references/<topic>.md` as lookup-on-miss files; domain-locked values follow
   pass 3; verbatim artifacts move to `templates/`; human usage and extension docs move
   to `README.md`, which is never read at load. A skill whose whole method fits one
   screen needs no split — force-splitting a small skill manufactures indirection. The
   ceiling forces the question; it is never the reason to split. (This document
   itself sits over the ceiling — justified: every section is a detector rule, a gate,
   or a disposition, none is step detail; the ceiling exists to force exactly this
   sentence, not to forbid growth.)
7. **Contradiction pass**: the same rule stated twice with different numbers; ordering
   claims ("run this FIRST") that conflict with another step's claim to be first;
   thresholds in mixed units without a conversion note; a module pointer whose load rule
   contradicts another pass's rule. One rule, one home, one number.
8. **Cross-reference audit**: every section the document points to must exist (including
   every side file named by a load rule); every anti-pattern should trace to a workflow
   step; every workflow step with a failure mode should have its anti-pattern. Orphans
   on either side get wired or dropped.
9. **Verification**: grep the final text for the entity list from step 1 and for path
   strings — every remaining hit is justified in one sentence or fixed. Check the load
   weight: the main document sits under the ceiling (~10KB / ~2.5k tokens) or its size
   is justified in one sentence; every side file named in the load table exists and
   carries WHEN + WHAT; no load rule instructs preloading every side file; the
   description is ≤50 words (hard cap 1,024 chars) with trigger phrases preserved; a
   README, if present, duplicates no router rule — it links. Then re-read the
   decision tree end to end as a stranger: executable without the origin, without the
   unnamed jurisdiction, without the unloaded side files? If any step says "as in the
   case of ...", it is not done.

## Side files — the modularization and router dispositions

- **Naming**: domain values live in `references/<domain>/<code>.md`, one code per file
  (region, market, vertical) — the extension point; new codes copy an existing file's
  skeleton. Load-weight restructures add `references/phases/<id>-<name>.md` (step
  mechanics), `references/<topic>.md` (lookup-on-miss detail), `templates/` (verbatim
  artifacts), and `README.md` (human usage and extension docs — never read at load).
- **Load rule mandatory**: the main document must say WHEN to read the file and WHAT to
  do with it (cite in the ledger, emit as verify-locally annotations; for a phase file:
  run only the current step's file). A side file without a load rule is an orphan
  module.
- **What moves**: values, citations, label glossaries, market conventions — content
  that is true only inside the domain — plus step mechanics, verbatim artifacts, and
  human docs from the load-weight pass: detail that is load-bearing only when a step or
  a context names it.
- **What never moves**: gates, tolerances, schemas, the decision tree — the contract
  never leaves the router, one-liner or not. The router keeps the RULE as one-liners;
  the side files carry the DETAIL and the VALUES.
- **Trigger hygiene**: side files load on the reader's informed decision (context names
  the domain; the current step names the phase file) — never as a side effect of
  triggering the skill, and never "read all references first".

## Output contract

- The rewritten skill file — router-shaped when disposition (e) fired: contract,
  load table, one-liner rules.
- Any created side files, each with its load rule as wired into the main document.
- A weight line: body chars and ~tokens before → after, and description word count
  before → after.
- A change list: what was generalized, what was conditionalized, what was modularized,
  what was deleted — one line each.
- A residual list: items that could not be generalized without losing meaning, flagged
  for the owner.

## Anti-patterns

- Generalizing into vagueness — deleting the numbers that carry the method (tolerances,
  thresholds, conversion factors) instead of the names that carry the story.
- Keeping the origin as a "for example" clause — an example-specific aside is still
  example-specific, however labelled.
- Conditionalizing something universal (schema rules, API contracts, unit conversions) —
  those are unconditional and belong in the method body.
- Over-conditionalizing something conventional until the rule says nothing — a pin with a
  concrete number and a "confirm locally" lead is transferable; "varies by region" is not.
- Modularizing the contract — gates, tolerances, schemas, and the decision tree
  fracture in exile, router one-liner or not; step mechanics may move behind load
  rules only once the router carries their contract (load-table row; hard-rule
  one-liner where the rule is cross-cutting) — a step exiled without its router line
  is the same fracture.
- Side files without a load rule — an orphan module is dead weight the reader never
  finds, and an uncited regulation is worse than none.
- Monolithic load — keeping step detail inline "because it might be needed"; detail
  needed at one step is dead weight at every other. (pass 6)
- Preload instructions — a load rule that says read every side file up front
  re-injects the weight the router removed. (pass 6)
- README mirroring the router — human docs that restate rules drift; link, don't
  duplicate. (pass 6)
- Trimming the description into unfindable — cutting word count by deleting trigger
  phrases; a concise description nothing matches is a lost skill. (pass 9)
- Renaming the skill or its directory as part of generalizing — identity is separate
  from specificity; changing the id breaks every reference to the skill.
