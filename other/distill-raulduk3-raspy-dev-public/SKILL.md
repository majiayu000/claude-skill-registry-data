---
name: distill
description: Turn a raw record (meeting transcript, message, email, notes) into ranked, color-coded candidate requirement statements appended to one HTML file, `docs/incoming.html`, for people to read, discuss and edit by hand. Each candidate is ranked for congruency with the specification and for complexity. Nothing is filed, edited or opened; a person promotes a candidate by pasting its block into an `intake` session.
---

# distill

Turn a raw record (meeting transcript, message, email, notes, stored in the owner's notes and never in a repository) into candidate requirement statements, each ranked against the repository's specification for congruency and for complexity, and append them as one dated batch to `docs/incoming.html`. People read, discuss and edit that file by hand. When a person decides a candidate is worth acting on, they copy its block and paste it into an `intake` session, and `intake` does what it already does. Nothing else reads the file: the loop, workers and hooks never reference it. The skill files no issue, edits no specification and opens nothing.

## Procedure

1. **Source.** Any raw record. It stays in the owner's notes; it is never copied into a repository.
   The HTML receives derived statements and a source reference by date and type only, for example
   `stakeholder call, 2026-09-17`. No raw quotes and no names of private individuals.
2. **Extract** candidate statements. Each is one sentence in `MUST`, `MUST NOT` or `SHOULD` form,
   with a kind: `bug`, `amendment`, `feature` or `question`.
3. **Read the repository.** Read `docs/spec/SDD.md`, `docs/spec/TDD.md`, the other documents under
   `docs/`, and the code the TDD `code:` comments name. When those files are absent or empty, say
   so in the report. Every candidate is `brand new` except one that cannot be acted on at all,
   which is still `nonsense`.
4. **Rank** each candidate on two axes.
   - Congruency: `already satisfied`, `clarifies`, `amends`, `contradicts`, `brand new` or
     `nonsense`. Cite the specification item ids it touches (`SDD-XX-nn`, `TDD-x.y.z`); a
     `brand new` candidate may cite none.
   - Complexity: `S`, `M`, `L` or `XL`, judged from the specification items touched, the files
     likely in scope, external provider effects and data migrations. One line of rationale that
     names what drove the size.
5. **Append** the candidates to `docs/incoming.html` as one dated batch, creating the file from
   the `incoming.template.html` that sits beside this skill file when it is absent. Copy the
   example batch in the template, place the new batch directly under the
   `batches below, newest first` marker, and never rewrite, reorder or delete an existing block:
   people edit them by hand. Escape `&`, `<` and `>` in every statement and rationale. Candidate
   ids are `C-YYYY-MM-DD-n`; n starts at 1 and continues within the day across batches, so search
   the file for the day's highest n first. Set the `class` of each block to the congruency class:
   `satisfied`, `clarifies`, `amends`, `contradicts`, `new` or `nonsense`.
6. **Stop.** Report the batch as a short table: id, statement, kind, congruency, complexity. Do not
   file issues, edit the specification or open anything. Promotion is a person pasting a block
   into `intake`.

## Plain reading

An easy patch is `clarifies` or `amends` at `S`. A hard change is `amends` or `contradicts` at `L`
or `XL`. `already satisfied` and `nonsense` need no work; they stay in the file so the discussion
can confirm that.
