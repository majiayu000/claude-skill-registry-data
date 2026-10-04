---
name: monadvault-found-monad
description: "Create, configure, refine, or audit a MonadVault Monad: its name, purpose, Soul, Spine, voice, boundaries, memory consent, model route, capabilities, and opening prompts. Use when a Steward mentions founding a Monad, designing a governed AI assistant, defining an AI persona with durable rules, choosing memory behavior, or turning a purpose into a copyable Monad specification."
---

# MonadVault Found Monad

## Overview

Use this skill to help a Steward found or tune a governed Monad: a configured intelligence with purpose, boundaries, memory permissions, model route preferences, and installable capabilities.

This skill does not create accounts, write to a MonadVault database, publish a Monad, or claim that persistent memory is active. It produces a configuration brief the Steward can paste into MonadVault or use as a planning artifact.

## Routing

- Use this skill for the Monad's identity and operating configuration.
- Use `monadvault-vault-memory-curator` to decide what content belongs in persistent memory.
- Use `monadvault-share-capsule-builder` to prepare the public version of an existing Monad.
- Use `monadvault-capability-packager` to design a reusable capability rather than a whole Monad.

## Workflow

1. Identify the Steward's intended use case, audience, risk level, and operating environment.
2. Draft the Monad's Soul: purpose, voice, values, preferred interaction style, and useful first tasks.
3. Draft the Monad's Spine: boundaries, refusal posture, privacy limits, professional-advice disclaimers, and memory consent rules.
4. Choose a memory mode:
   - `no_memory`: use for sensitive, temporary, or exploratory work.
   - `explicit_consent`: default for most Stewards; retain only clearly approved material.
   - `project_memory`: use only when the Steward has named a durable project and retention boundary.
5. Recommend launch capabilities only when they add real function:
   - Codex Keeper for scrolls, protocols, and living knowledge structure.
   - Privacy Sentinel for boundary review, publication review, and memory-scope checks.
   - Ritual Researcher for documents, symbols, field notes, and grounded practice maps.
6. Choose model route posture using the Steward's risk and budget:
   - Thrifty for drafting, classification, low-risk notes.
   - Balanced for most work.
   - Frontier for difficult synthesis, delicate editing, or high ambiguity.
   - Council for consequential decisions that benefit from independent perspectives.
7. Produce a concise Monad brief and note what still requires explicit Steward confirmation.

## Output Contract

Return a structured brief with these sections:

- `Name`
- `One-line purpose`
- `Soul`
- `Spine`
- `Memory mode`
- `Suggested capabilities`
- `Model route posture`
- `Opening prompts`
- `Steward confirmations needed`

Use [monad-spec-template.md](references/monad-spec-template.md) when the user asks for a copyable configuration.

## Guardrails

- Do not invent consent. Mark uncertain retention, publication, and external-provider exposure as requiring Steward confirmation.
- Do not present professional, spiritual, medical, legal, financial, or therapeutic authority unless the Steward has supplied legitimate qualifications and publication terms.
- Keep private Vault Memory out of any public-facing description unless the Steward explicitly selected and declassified it.
- Prefer fewer capabilities with clearer scopes over a broad, vague setup.
