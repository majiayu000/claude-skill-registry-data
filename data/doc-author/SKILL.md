---
name: doc-author
description: Guide a user through authoring a new document using the GoodDocs template and validation rules.
---

# Skill: doc-author

## Purpose
Guide a user through authoring a new document using the GoodDocs template and validation rules.

## Behavior
1. If `repo.config.json` exists, use `defaultDocTypeKey` and `defaultOwners` automatically.
2. Ask the user for:
   - Title
   - Motivation
   - Proposed solution
   - Alternatives/open questions
3. Determine the next numeric ID by scanning `docs/<docRoot>` for `####-*.md` and incrementing the max value.
4. Set frontmatter `id` to `DOC-####` and generate `####-<kebab-title>.md` using `templates/doc-template.md`.
5. Update `docs/README.md` to include a link to the new document.
6. Run `python3 scripts/validate_docs.py` and fix issues before finishing.
