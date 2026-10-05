---
name: frame-initiative
description: Create a parent initiative packet under `.initiatives/<initiative-slug>/` with the canonical file tree, seeded shared-context docs, placeholder-owned files, and initial routing fields before split work begins.
---

# frame-initiative

Use when discovery shows the work needs a parent initiative packet before healthy child task packets can exist.

## Read first
- `../references/initiative-packet-contract.md`
- `../references/initiative-workflow-contract.md`
- `../references/final-state-authoring-policy.md`
- `../../references/communication-mode.md`
- relevant tracked `AGENTS.md` chain

## Goal
Create the parent initiative packet exactly once and leave every later phase updating existing canonical files rather than inventing ad hoc packet structure.

## Do
1. Choose the initiative slug and create `.initiatives/<initiative-slug>/`.
2. Create every required top-level file from the initiative packet contract.
3. Seed `INDEX.md`, `BRIEF.md`, `DECISIONS.md`, `INVARIANTS.md`, `REPO_MAP.md`, `CONTRACTS.md`, and `OPEN_QUESTIONS.md` with the best current discovery facts.
4. Create explicit placeholder stubs in `UBIQUITOUS_LANGUAGE.md`, `TASK_GRAPH.md`, and `SYNC_LOG.md`.
5. Seed `INDEX.md` with:
   - `Status: discovery` during bootstrap
   - `Next durable distill: later`
6. Exit bootstrap with `Status: framed`.
7. Leave unknowns explicit instead of inventing certainty.

## Writing rule
Write the packet as the initiative’s current working model.
Do not explain how this packet differs from some earlier workflow shape.
Do not leave transitional notes in canonical files.

## Do not
- split child tasks yet
- write a delivery plan inside the initiative packet
- duplicate giant prose that belongs in later child packets

## Output bar
A fresh agent must be able to open the initiative packet and immediately see the problem, invariants, contracts, open questions, and the canonical files later phases own.

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
