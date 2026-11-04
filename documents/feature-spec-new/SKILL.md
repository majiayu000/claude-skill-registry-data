---
name: feature-spec-new
description: Write a new feature spec to the documentation standard, or revise one. This is the one skill that writes every feature spec (docs/features/<feature>/spec.md); luismc-specs:spec-new covers specs that are not features and hands feature specs here. Use when the user wants to document, spec or describe a feature in docs/features, add a feature folder, or turn a feature artifact's decided work into a lasting spec. Creates docs/features/<feature>/spec.md from the template with front matter, requirement IDs, a Mermaid flow and the test table.
model: opus
effort: medium
---

# Feature spec — new

Produces `docs/features/<feature>/spec.md` from `templates/feature-spec.md` (DOCSPEC §4). Read the template and §4 before you write.

This skill writes every feature spec. `luismc-specs:spec-new` writes only specs that are not features and hands feature specs here. `luismc-artifacts:feature-artifact-new` (promote-to-spec) writes this same file from a feature page and follows this template.

## Loop

1. Read the code the feature touches, and the feature's artifact in the record (`record_dir`) if there is one. Promote its findings and decided choices into the spec (R4.10). Copy the decided entries of its `decisions.json` into section 10.
2. Pick `apps` and `topics` from `docs/docs.json`. Ask the owner only when the lists do not cover the feature.
3. Copy the template into `docs/features/<feature>/spec.md` (folder name: lower-case words with hyphens). Set `id` to the folder name, `status: proposed` (or `building`), `version: 0.1.0`, `code:` globs, `last_verified:` today.
4. Write sections 1 to 4 for every reader: one paragraph, why, a Mermaid flow and the steps in words, screens and states (images in `images/` with alt text, rules cited by design-system ID, never written here). Then 5 to 12 for engineers. Delete any section that does not apply.
5. Every requirement gets an ID and a test in section 9. Mark unbuilt parts `NOT YET IMPLEMENTED`.
6. Run `docs_index.py build` then `docs_check.py`; fix every error.

Never write `version` or the Versions table. The release fold does. For later changes use `docs-note`.
