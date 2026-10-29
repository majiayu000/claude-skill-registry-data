---
name: personal-knowledge-architect
description: >-
  Extracts connected, reusable methods, scenarios, and entities from source texts. Use when organizing personal knowledge: confirm a deduplicated skeleton, then enrich it with source-grounded steps and relations.
metadata:
  version: "0.4.0"
  language: en
  translation_of: personal-knowledge-architect-cn
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills/tree/main/skills/en/personal-knowledge-architect
---

# Personal Knowledge Architect — Build Connected, Reusable Knowledge

Input is a batch of linear source texts. Output `sce-scenes.yaml`, `sce-concepts.yaml`, and
`sce-entities.yaml` in the user-selected directory, with progress in `_sce-round1-progress.md`. The
value is reuse: one scene can directly invoke a concept established elsewhere.

## Principles

1. **Source first** — `define` and IPO come from the source and stay within 50 words. Leave
   unsupported content empty rather than inventing it.
2. **Concepts are the hub** — Establish concepts first, attach entities to concepts, and let scenes
   invoke only established concepts and entities.
3. **Prefer omission** — A candidate without its own IPO or decomposition is not a concept. Merge
   abstractions into their parent and demote fragments to steps.
4. **Bound references** — Keep two to six relations per concept and only the strongest relation for
   a knowledge-element pair.
5. **Stop for confirmation between rounds.** Never start round two before approval.

## Round One: Skeleton

Process five to ten texts per batch and update `_sce-round1-progress.md`.

1. Read the complete batch and record progress.
2. Extract candidates with only `id + define + sources`: scenes answer “how do I…”, concepts can
   express an IPO, and entities answer “did I use X?”
3. Deduplicate globally: merge at 80% or greater semantic overlap, normalize synonymous IDs, and
   return overly fine steps to their parent. Record every `X → Y` merge.
4. Write the three YAML files and mark remaining fields `TODO`.
5. Stop and present deduplication and concept coverage for confirmation.

## Round Two: Content

Use `sources` to return to the original text. Sequence words indicate steps; requirement and input
words indicate IPO inputs.

1. Fill from the hub outward: concepts first with complete IPO or decomposition, entities in
   parallel, then scenes with trigger, goal, and three to six progressive assembly stages.
2. Read `references/relations.md`; add entity hierarchy and concept–entity invocation relations.
3. Run completeness checks and write `updated_at`.

Completion requires a skeleton-only round one with a merge log; every concept has IPO or
decomposition; every entity passes “I used X” and has hierarchy depth at most three; every scene
invokes established concepts/entities in three to six stages; all references resolve; every
definition has a source and stays within 50 words; there are no isolated concepts; and every concept
has two to six relations.

| Layer   | Meaning                                                          | Question                   | Valid form                                                                                          |
| ------- | ---------------------------------------------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------- |
| Concept | Class: executable action                                         | Which method should I use? | IPO preserves independent logic; decomposition records stages, sub-concepts, and why each is needed |
| Entity  | Instance: identifiable person, tool, product, or named framework | What did I use?            | “I used X,” where X is not an action                                                                |
| Scene   | Assembly: problem plus orchestration                             | How do I…?                 | Trigger, goal, three to six stages, invocations, and constraints                                    |

During round two, read `references/relations.md` for the direction and selection order of the eight
relation types.
