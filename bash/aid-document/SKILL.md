---
name: aid-document
description: >
  Write a general document in one pass -- a Diataxis how-to, reference page or explanation,
  or a status or progress report. Use this skill when the document you need does not fall
  into one of the named genres and you want it drafted now. It is grounded in, and accuracy-
  checked against, the Knowledge Base (`.aid/knowledge/`) and the project source; aid-tech-
  writer produces it and aid-reviewer verifies it. It resolves nothing: it drafts, you
  approve, and only then is the document placed. It never writes into `.aid/knowledge/`. A
  thin kind-sibling of `/aid-create-document`, which defines its full behavior. To settle a
  document's direction as a reusable design seed first, use `/aid-design-document`.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit Agent
argument-hint: "<subject> -- what to document"
---

# Document (general kind-sibling of /aid-create-document)

`/aid-document` is a thin **kind-sibling** of **`/aid-create-document`**
(`.agents/skills/aid-create-document/SKILL.md`) -- not an alias: it is its own catalog
row (`alias_of: null`, its own `{verb: document, artifact: ""}`), `repurpose: true`
(skipped by `build-shortcut-skills.py`; hand-authored). It carries **no logic of its own.**

Execute `.agents/skills/aid-create-document/SKILL.md` exactly as written, with the
document **genre bound to general** (structure: a Diataxis how-to / reference /
explanation, or a status/progress report) and the **format = markdown**. Substitute only
the invocation name in any printed usage example (`/aid-document` instead of
`/aid-create-document`). Deeper genre structures:
`.aid/runtime/templates/shortcut-scaffolding/document.md`.
