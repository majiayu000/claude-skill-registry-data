---
name: apple-foundation-models-production
description: Build and review reliable Apple Foundation Models features. Use when native apps need guided output, image input, model tools, privacy, or fallbacks.
license: MIT
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-31"
  last-reviewed: "2026-08-31"
  apple-docs-reviewed: "2026-08-30"
---

# Apple Foundation Models Production

Build a bounded generative subsystem, not a source of truth. Establish the task, authoritative inputs, data boundary, output contract, and deterministic fallback before editing code.

## Invariants

1. **The model never owns authoritative state.** It may propose text, interpretations, or actions. Deterministic code validates and commits every state transition.
2. **Every path has a deterministic outcome.** Unavailability, cancellation, refusal, guardrail failure, timeout, capacity errors, and invalid output end in a declared fallback or recoverable UI state.
3. **Generated shape is not truth.** Validate domain rules, evidence, permissions, and freshness after `@Generable`, `@Guide`, or schema decoding. Supply application-owned source IDs, reject unknown IDs, and reconstruct citations from authoritative records.
4. **Privacy precedes convenience.** Minimize prompt and attachment data. Do not log raw prompts, transcripts, images, tool results, or output by default. Treat remote tools and alternate providers as separate data boundaries.
5. **Requests are admitted and cancellable.** Never overlap responses on one `LanguageModelSession`. Choose queue, latest-wins, or reject-while-busy; cancel with the owning feature and discard stale results.
6. **Model-selected tools grant no authority.** Validate arguments, enforce permissions in normal code, and confirm consequential effects immediately before execution.
7. **Image attachments preserve an explicit transform contract.** Validate source, type, orientation, and lifecycle before attachment; either supply the source orientation or normalize/redact to a new owned representation and pass `.up`.

Prefer Foundation Models for bounded summarization, extraction, classification, rewriting, image understanding, and grounded dialogue. Do not use the model as a calculator, rules engine, database, policy authority, or source of current facts.

## References

- Before adopting or changing APIs, use Xcode `DocumentationSearch` with `FoundationModels`, then read [apple-documentation.md](references/apple-documentation.md) for reviewed sources and the freshness boundary.
- For availability and capabilities, session admission, error mapping, guided generation, evidence validation, attachments, tools, or privacy controls, read [production-contracts.md](references/production-contracts.md).
- For prompt or schema changes, runtime measurement, regression review, or release qualification, read [evaluation.md](references/evaluation.md).

## Review

- Last updated: `2026-08-31`
- Last reviewed: `2026-08-31`
- Apple documentation reviewed: `2026-08-30`

Foundation Models system and Private Cloud Compute availability, errors, sessions, guided generation, tools, attachments, and privacy were reviewed using Xcode MCP `DocumentationSearch`; attachment-contract behavior was re-reviewed with a live Codex evaluation.

[Apple documentation evidence](references/apple-documentation.md)
