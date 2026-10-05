---
name: stabilize-initiative-language
description: Populate `UBIQUITOUS_LANGUAGE.md` inside an initiative packet with canonical terms, aliases to avoid, flagged ambiguities, and term relationships before decomposition hardens.
---

# stabilize-initiative-language

Use after `frame-initiative` and before split work depends on stable terminology.

## Read first
- `../references/initiative-packet-contract.md`
- `../references/initiative-workflow-contract.md`
- `../references/final-state-authoring-policy.md`
- `../../references/communication-mode.md`
- initiative `BRIEF.md`, `DECISIONS.md`, `INVARIANTS.md`, `REPO_MAP.md`, `CONTRACTS.md`, `OPEN_QUESTIONS.md`

## Goal
Stabilize names before tasks, contracts, statuses, and reviews start depending on them.

## Write into `UBIQUITOUS_LANGUAGE.md`
- canonical terms
- aliases or overloaded words to avoid
- flagged ambiguities that still need a decision
- short term relationships
- rerun guidance for later vocabulary updates

## Status
- first semantic writer of `UBIQUITOUS_LANGUAGE.md`
- exit with initiative `Status: language_stabilized`

## Writing rule
Write one canonical vocabulary.
Do not preserve competing term sets in the glossary just because they appeared earlier in discovery.

## Do not
- bury unresolved ambiguity in prose; flag it explicitly
- rewrite the initiative brief into a giant glossary
- reference outside Atelier skill files for terminology rules

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
