---
name: spec-new
description: Interview the user and write a normative specification before any implementation begins. It writes specs that are not features (standards, services, migrations, components); a feature spec in a DOCSPEC repo goes to luismc-docs:feature-spec-new, which this skill hands over to. Use this whenever the user wants to plan, design, or spec out a feature, component, service, migration, or refactor — including phrasings like "I want to build X", "how should we approach Y", "let's design Z", "write a spec for", "plan out", or when they describe a non-trivial change without having written anything down yet. Also use it when an existing spec needs revising or extending. Prefer this over jumping straight to implementation for anything touching more than one file.
model: opus
effort: medium
---

# Spec — New

Produce a specification that is precise enough to make implementation
mechanical. Make it verifiable enough that "done" is a command, not an opinion.

The template lives at `assets/spec-template.md`. **Read it before interviewing.**
Its section tiers and authoring rules decide which questions matter.

## The loop

1. **Ground yourself.** Read the relevant code before you ask anything.
   Questions informed by the actual codebase are worth ten generic ones. If
   there is no codebase yet, say so and interview on product shape instead.
2. **Interview.** Use AskUserQuestion. Details below.
3. **Write the spec** from the template. Where it goes depends on the repo:
   - This skill writes specs that are not features: standards (like DELIVERYSPEC), services, migrations,
     components. A feature spec is written by `luismc-docs:feature-spec-new`, never here.
   - A repo with `docs/docs.json` follows DOCSPEC (`luismc-docs`; its layout is not restated here). A spec of one
     feature belongs in `docs/features/<feature>/spec.md`: say first that you are handing over to
     `luismc-docs:feature-spec-new`, then use it, and bring this interview's answers to it. A binding rule that spans features goes to `docs/architecture/<name>.md`, with
     front matter `type: reference`.
   - Any other repo (no DOCSPEC): `specs/<name>.md`, for any kind of spec, features included.
4. **Stop.** Do not implement in the same session. Tell the user to review the
   spec, then start a fresh session to build it.

## Interviewing

Open with what you already know from reading the code, so the user corrects
you instead of dictating. Then dig, in roughly this order:

- **The boundary.** What is in scope, and what is deliberately out. Push here.
  An unstated exclusion becomes a scope argument during review.
- **The data.** What is stored, what is derived, and what is the source of
  truth. Ask what must never be lost and what may be recomputed.
- **The failure modes.** For every dependency: when it is unavailable, does
  this feature fail open or fail closed? Users often have not considered this.
  It is the highest-value question in the interview.
- **The edges.** Concurrency, partial failure, retries, idempotency, ordering.
  Ask what happens when the same operation arrives twice.
- **The ceilings.** For every limit or timeout: what is the default, and may
  configuration move it up or only down?
- **Verification.** What command proves this works? If they don't have one,
  designing it is part of the spec.
- **Existing data.** Does the target system already have users or records? If
  yes, the adoption chapter is mandatory, not optional.

Ask about tradeoffs the user hasn't raised. The questions that feel annoying in
the interview are usually the ones that would have surfaced as a defect.

**Stop interviewing** when you can write every section without guessing. Say so
explicitly. Do not drift into more questions.

## Writing

Follow the authoring rules in the template's header comment. Three of them carry
most of the weight:

- **Every requirement gets an ID.** `R<section>.<n>`. No ID means no test can
  cite it, so it will be dropped.
- **If you cannot name the test, it is not a requirement.** Move it to
  rationale or cut it. This is how a spec stays short without getting vague.
- **Prohibitions carry their reason inline.** A `MUST NOT` without a reason
  gets deleted by the next person who optimises something.

### Numbering — get this right the first time

Numbering is not cosmetic. Every `§`/`R` reference in the spec, in tests, in
review comments, and in audit findings resolves through it. Rule 11 in the
template states it in full. These parts are the easiest to get wrong:

- **`§` and `R` are different namespaces.** `§4.2` is a *heading*. `R4.2` is a
  *requirement*. There is no `§4.2` just because `R4.2` exists. Never write one
  meaning the other, and never write `R6.6.1` — three components means you meant
  a section.
- **Heading depth matches the number.** `## 4.` → `### 4.2` → `#### 4.2.1`. A
  `### 4.2.1` is wrong even though it reads fine.
- **A requirement's first component is its section.** `R4.x` lives in `§4`,
  always. Moving a requirement between sections means renumbering it.
- **Numbering is append-only.** Deleting a section or requirement leaves its
  number retired and unused. Do not close the gap. Renumbering `§5` to `§4`
  invalidates every `R5.x` and every citation of them. Insert with a letter
  suffix (`R4.9a`) instead.

When you delete the template's inapplicable sections, **leave the resulting
gaps**. A spec that jumps §1 → §3 → §7 is correct. A spec renumbered to close
those gaps has silently broken every reference written against it.

**Cite another document by name.** A bare `§4.2` means *this spec's* §4.2.
When you mean a section of another document, write `OTHERSPEC §4.2`. The prefix
keeps the two apart. Without it, a reference to their §4.2 either fails to
resolve or, worse, silently resolves to yours if the numbers happen to collide.

Verify before you hand the spec over, with the **`spec-check`** skill. It is the
partner skill in this same plugin, at `../spec-check/` relative to this file. It takes any spec path and checks all of the above:
duplicate numbers, depth mismatches, orphan subsections, out-of-order or
mis-sectioned identifiers, and dangling `§`/`R` references. Register any
document you cite, so those references are checked against it and not skipped.
If you do not register it, `OTHERSPEC §4.2` falls through to internal resolution
and silently matches your own §4.2 if you have one:

```bash
python3 ../spec-check/assets/spec_check.py <path-to-your-spec>.md \
  --external OTHERSPEC=path/to/other.md
```

**Delete every section that does not apply.** A 200-line spec that covers one
component well beats a 900-line one with empty scaffolding. The template's
tier table says what is core and what is conditional.

Keep the spec self-contained: name the files and interfaces involved, state
what is out of scope, and end with a verification command.

## After writing

Tell the user:

- Where the spec is, and that they should review it as code — read the diff.
- That implementation goes in a **fresh session**. The interview context is
  full of rejected options that will compete for attention during
  implementation.
- Which decisions were left open and need their answer before building.

## Revising an existing spec

When implementation shows the spec was wrong — and it will — update the spec
first, then continue. Never let the code and the spec disagree silently. That is
ordinary prompt-driven development with extra files.

Revision is where numbering gets wrecked, so:

- **Add** with a letter suffix — `R4.9a` between `R4.9` and `R4.10` — so every
  existing citation stays valid.
- **Retire** by striking the requirement and leaving its number dead. Say what
  replaced it. Never reuse a retired number for new meaning: a stale citation
  then resolves to the wrong requirement, which is worse than not resolving.
- **Never renumber** to tidy up. The gaps are the record that citations were
  kept stable.

Re-run **`spec-check`** after revising. The checks for identifier order,
section alignment, and dangling references exist because revision is exactly
when those break.
