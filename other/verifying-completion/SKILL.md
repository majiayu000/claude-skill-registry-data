---
name: verifying-completion
description: >-
  Runs a mandatory completion checklist before declaring any worldbuilding task
  finished. Catches missing frontmatter, broken cross-references, unlinked glossary
  terms, and deferral language. Use after writing any content, before reporting task
  complete, or when user says "is this done", "verify", "check my work", or
  "completion check". Does NOT write content — only verifies.
model: sonnet
effort: medium
---

# Verifying Completion

Mandatory checklist before declaring ANY worldbuilding task complete.

## Checklist

For EVERY file created or modified:

1. **Frontmatter** — YAML with title, tags, status
2. **Content** — No TODO, placeholder, TBD, "will flesh out", empty sections
3. **Cross-References** — All links resolve, relative paths correct
4. **Glossary & Timeline** — New terms in GLOSSARY.md, events in MASTER-TIMELINE.md, _index.md updated
5. **Canon Consistency** — Obeys upstream science, naming correct, no contradictions
6. **Writing Standards** — Academic prose in science dirs, no meta-commentary

## Red Flags — DO NOT Declare Complete If:

- Any section heading has no content below it
- Any cross-reference doesn't resolve
- "placeholder" or "TODO" appears anywhere
- A new term was introduced but not added to GLOSSARY.md

## Out of Scope

Does NOT write content. Does NOT audit the full repo.
