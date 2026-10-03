---
name: clean-comments-and-guidance
description: Audit and reduce low-value code comments, KDoc, docstrings, CLAUDE.md, and AGENTS.md while preserving behavior and durable intent. Use for repository-wide comment cleanup, comment-density reduction, or shortening agent guidance.
disable-model-invocation: true
---

# Clean Comments and Agent Guidance

Reduce noise, not information. Build a tracked-file inventory and review every comment and instruction in scope, including tests, configuration, scripts, SQL, and Web assets.

Delete comments that narrate code, restate signatures or types, duplicate tests or configuration, label obvious sections, preserve implementation history, cite completed plans, record transient counts, or repeat an authoritative source.

Treat recorded plans as historical artifacts only, not as documentation or a source of truth. Never use them to implement other features or as authoritative evidence about current behavior; verify relevant claims against current code, tests, configuration, requirements, and project documentation.

Keep comments concise and only when they preserve non-obvious intent, external constraints, security or concurrency guarantees, platform or compatibility behavior, wire or persistence contracts, deliberate UX trade-offs, or warnings against plausible but unsafe changes.

Prefer clearer code, types, assertions, tests, project documentation, backlog tasks, or reusable skills over comments. Move information to its authoritative home instead of duplicating it. Preserve licenses, attribution, required directives, and generated-file contracts.

For `CLAUDE.md` and `AGENTS.md`, retain only current, repository-specific instructions that materially change agent behavior. Remove tutorials, generic knowledge, stale paths or versions, history, inventories, duplicated documentation, and contradictory rules. Link authoritative documents instead of restating them. Treat imports and generated sections according to their actual consumer semantics.

Do not change program behavior. Keep non-comment token streams unchanged where practical; explicitly prove equivalence when comments participate in syntax.

Validate coverage, inspect the final diff, run `git diff --check`, perform language syntax checks, and run build or tests proportional to risk. Report reviewed scope, removed volume, retained comment categories, semantic-equivalence evidence, and anything left unverified.
