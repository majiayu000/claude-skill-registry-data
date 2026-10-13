---
name: wu-input-001f
description: Evaluate WriteUrdu translation, Voice Translator, audio transcription, and dictionary previews for safe activation using live quality, cost, privacy, and device evidence. Do not use for building new input features.
---

# WU-INPUT-001F live activation gate

Read `specs/WU-INPUT-001F-live-quality-activation-gate.md`, then `benchmarks/wu-input-001f/README.md`. Follow their links to current implementations and predecessor contracts. Repository code and tests override stale handoff details.

## Boundaries

- Evaluate existing preview capabilities; do not add another feature.
- Do not change editor, transliteration, current Voice Typing, global navigation, sitemap, audio limits or preview indexability.
- Never commit keys, private text/audio, provider-console exports containing secrets, or production user content.
- Never call live providers without explicit credentials and an intentional operator command.
- Back-translations are context clues, not synonyms. Never invent synonyms.

## Evidence discipline

Use `pass`, `fail`, `unavailable` and `not-run` exactly. Automated tests do not prove language quality. Missing credentials, browser/platform coverage, consented audio or account headroom means activation remains unavailable, not passed.

Run offline checks first:

```bash
node benchmarks/wu-input-001a/validate.js
npm run benchmark:input-activation:check
node tests/input-live-activation-gate.test.mjs
```

Use existing opt-in live runners under `benchmarks/wu-input-001a/`. Keep raw outputs outside source control unless they contain only committed fixtures and have been deliberately sanitized for evidence.

## Activation decision

Update `benchmarks/wu-input-001f/activation-status.json` only from recorded evidence. A `ready: true` row needs all required evidence references and passing prerequisite rows. Shared feature gates must remain off if any exposed direction is unacceptable.

After focused checks, run full repository Quality workflow. Report local results, live-provider results, browser/device evidence, account dependencies, hosted CI and activation recommendation separately. Do not call CI green until GitHub Actions says so.
