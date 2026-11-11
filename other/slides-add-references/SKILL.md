---
description: Enrich slides with references to academic papers and books
model: sonnet
---

# Goal
- Review the passed slides file `<FILE>.smd`, and add references to books and
  technical papers

# Workflow

## Find References
- If `<FILE>` already has references to technical papers, give them priority
  (e.g., in the `* References` slide at the end)

- Do not add references as `//` comments: add them to the `* References` slide,
  following `.claude/skills/slides.rules.md` "References Slide"

- Add supporting references, following the source types and retrieval methods in
  `.claude/skills/references.rules.md` `# When Searching for References`

## Add Citations
- Find text in `<FILE>` that can take a citation, and add it
- Be sure the citation is correct. If unsure, do not add it

- Citations:
  - Are in the typst format (e.g., `[@su2024dualformer]`)
  - Correspond to entries in `refs.bib` in the same dir as `<FILE>`

# Conventions
- Follow the role in `.claude/skills/role.ai_researcher.md`
- Follow the reference format and conventions in
  `.claude/skills/references.rules.md`

# Verification

- [ ] Check that each paper reference exists
- [ ] Make sure the document still runs, e.g., `gen_slides.py` or
  `notes_to_pdf.py` with `--skip_action open_pdf`. The goal is to confirm it runs,
  not to render it
  ```bash
  > gen_slides.py -i book.Agentic_AI/12.1 --notes_to_pdf_args="--skip_action open_pdf"
  ```
  - Too many references on one page (e.g., more than 4) can cause errors like:
    ```text
    warning: layout did not converge within 5 attempts
     = hint: check if any states or queries are updating themselves

    error: cannot format citation in isolation
        ┌─ @preview/touying:0.7.4/src/magic.typ:175:8
        │
    175 │         cite(it.key, form: "full")
        │         ^^^^^^^^^^^^^^^^^^^^^^^^^^
        │
        = hint: check whether this citation is measured without being inserted into the document
    ```
    which requires bisection to find the problematic reference
