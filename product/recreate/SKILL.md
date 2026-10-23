---
name: recreate
description: Use for the first design of a product recreated from its existing code — the /recreate flow on a project seeded from a code-to-spec bundle, whose requirements, domain model and upstream dependency definitions are already in place. Treats the seeded definitions as givens, then walks the design lineup for every feature.
metadata:
  aep:
    kind: platform
    audience: [design]
---

# Recreate

The first design of a product that already exists as code. A developer
skill, `code-to-spec`, read the product's code and wrote what `/start` and
the interviews would have asked a person for; the platform seeded the
project from that bundle (ADR-0053). Your job is the `design` lineup over
that tree, with three facts about the tree that `design` cannot know.

## What the tree holds

- `specs/requirements/`: the requirements in the `prd-contract` shape, derived
  from the code. The source tags name modules and files instead of documents
  (`[backend · service.bal:312]`). A line that closes with `*assumed*` is the
  author's inference about the code; it stands as a requirement unless an
  Open Question on the same page doubts it. A `*blocking*` question keeps its
  feature out of this run, as `prd-contract` says.
- `specs/requirements/sources/`: one coverage file per module and document,
  each line pointing at the requirement it landed on or saying why it was set
  aside. They describe the product as it is built today. Read them for the
  as-is shape when a decision needs it; they are context, never requirements,
  and a rule that lives only there does not reach the build. The requirements
  may have been edited since the seed: a coverage line that points at a story
  now gone or reworded is stale, never a reason to bring the story back.
- `specs/design/domain-model.md`: the data model from the code's own types.
  Converge it as the lineup's step 3 says.
- `specs/design/dependencies/<name>/`: one definition per upstream the recreate
  keeps calling, with its provider, its config keys, a contract derived from
  the product's client code, and an `assumptions.md` naming what that
  derivation relies on. These are the givens below.

## The owner's note

The text after `/recreate`, when there is one, is the owner's note: what
the recreate should keep, drop or change, typed when the project was created
or with the command. It steers this run and is not itself a requirement:
where it changes what the product does, write it into the requirements
first, as a Decision or an Open Question in the owner's words on the feature
it touches, so every later `/design` sees it; then design from the files. No
note means the product as the tree describes it.

## The definitions are givens

Every definition on disk is settled before this run: reference it by its
name from the component that calls it, carry it into `declare_plan` as
reused, and never rewrite, rename or remove it, nor coin a parallel
`<capability>-service` for the same system. `architecture`'s reuse rule, that
every external comes from this turn's `list_external_resources` result,
governs the externals you create this turn; a definition on disk is not one
of them. A definition with no provider is an open need like any other and
goes through `architecture`'s steps.

The design's Dependencies step (the lineup's step 7) has nothing to add to a
seeded definition: its contract and keys are on disk, and its
`assumptions.md` already says what the design relies on. Edit that file only
to add an assumption this design makes beyond it.

## Then design

Load the `design` skill and walk its lineup for every feature, as a bare
`/design` does. There is no design to converge: the tree holds requirements,
a data model and dependency definitions, not a design.

Close as `design` closes, and add one line naming the definitions the design
references, so the user sees that none was reinvented.
