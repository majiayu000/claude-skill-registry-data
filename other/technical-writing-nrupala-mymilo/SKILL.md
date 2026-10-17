---
name: technical-writing
description: Write documentation that gets used — READMEs, runbooks, API docs, decision records, changelogs, kept close to source.
version: 1
triggers: technical writing, documentation, readme, runbook, api docs, write docs
category: Writing & documents
blurb: Write documentation that gets used — READMEs, runbooks, API docs and decision records.
archetype: knowledge
example: Rewrite this README so a newcomer can actually use it.
---

# Technical Writing — the docs seat

Docs are part of the product. Write for the reader who arrives tired and wants to get something done.

## When to use
- Any deliverable handed to someone else (README, runbook, API docs, guide).
- Behavior changes — docs update in the same change.
- Onboarding friction — fix it in the docs first.

## Method
1. **README skeleton**: what it is (one paragraph) · quickstart (copy-paste, tested) · usage · operations (env vars, ports, defaults) · troubleshooting · where to change things.
2. **Docs-as-code**: docs live with the source they describe; reviewed like code; no wiki-only oracles.
3. **API docs**: generated from or verified against the contracts; one working example per endpoint.
4. **Decision records**: cross-link ADRs from code where behavior is surprising.
5. **Changelog**: continuously kept (see `release-management`), never retro-fitted at release time.
6. **Plain language**: short sentences; define jargon on first use; steps as lists; examples over adjectives.
7. **Test the docs**: run the quickstart from a clean environment; broken docs equal broken trust.

## Artifacts
- README.md, `docs/`, `runbooks/`, changelog entries, tested examples.

## Quality gates
- [ ] Quickstart works verbatim from a clean state.
- [ ] Every config option documented with its default.
- [ ] Docs updated in the same PR as behavior changes.
- [ ] No stale screenshots or commands.

## Red lines
- Never publish private, contact, or financial data in docs — privacy rules apply everywhere.
- No silent "TODO: document" — track it or finish it.

## Related
`release-management` (changelogs) · `architecture-decisions` (ADRs) · `observability-ops` (runbooks).
