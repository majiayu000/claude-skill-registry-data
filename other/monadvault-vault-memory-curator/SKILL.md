---
name: monadvault-vault-memory-curator
description: "Curate notes, documents, chat excerpts, observations, decisions, and project material into governed MonadVault Vault Memory candidates. Use when a Steward says remember this, save this to memory, clean up my memory, decide what to retain, summarize for long-term recall, add retrieval tags, redact sensitive details, scope memory to a Monad or project, review retention, or identify what should be excluded or deleted."
---

# MonadVault Vault Memory Curator

## Overview

Use this skill to convert raw material into Vault Memory candidates with consent posture, scope, sensitivity, and retrieval value. The output is a memory proposal, not an automatic write to storage.

## Routing

- Use this skill for retention, consent, sensitivity, scope, and retrieval decisions.
- Use `monadvault-codex-keeper` when the main task is organizing source material into a codex entry, protocol, glossary, or index.
- Use `monadvault-privacy-sentinel` for a dedicated exposure or publication-risk audit.

## Workflow

1. Separate raw source from interpretation.
2. Identify whether the material is personal, confidential, sacred/cultural, regulated, third-party, public, or operational.
3. Decide whether memory is appropriate:
   - Retain if the material has durable value and the Steward has consented.
   - Summarize if exact text is too sensitive or too noisy.
   - Redact if only a subset belongs in memory.
   - Exclude if the material is temporary, high-risk, unauthorized, or unrelated.
4. Convert approved material into memory candidates:
   - stable title
   - source type
   - concise memory statement
   - retrieval tags
   - permitted Monad or project scope
   - sensitivity class
   - retention recommendation
   - open consent questions
5. Flag any material that should pass through Privacy Sentinel before storage or publication.

## Output Contract

For each memory candidate, return:

- `Title`
- `Source`
- `Memory statement`
- `Why retain`
- `Scope`
- `Sensitivity`
- `Suggested tags`
- `Redactions`
- `Retention`
- `Consent needed`

Use [memory-entry-template.md](references/memory-entry-template.md) for structured conversion.

## Guardrails

- Do not treat chat history as memory by default.
- Do not retain secrets, credentials, private contact details, payment data, or legal identifiers unless the Steward explicitly asks and the storage system is appropriate.
- Do not include third-party private information without an explicit reason and narrower scope.
- Prefer summaries over verbatim retention when sensitive material is only needed for context.
