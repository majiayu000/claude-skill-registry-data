---
name: write-docs
description: Write or edit documentation - service utilities, project, code, service, SOP or known-issue notes - in a lint-clean, runbook-first house style. Use whenever documentation is created, restructured or reviewed.
---

# Write Docs

Pick the document type first, obey the general rules, and lint the result
before reporting it as done. One document may hold several types as
sections - a service description followed by an SOP and its known issues is
one document, not three. Where a repository states its own convention, that
convention wins over the defaults here.

## General rules

- **Format** - Markdown. Every fenced block carries a language tag (`bash`,
  `text`, `yaml`, ...).
- **Charset** - ASCII only. No smart quotes, em dashes, non-breaking spaces
  or box drawing.
- **Graphics** - ASCII art only.
- **Lint** - the document passes
  [markdownlint](https://github.com/DavidAnson/markdownlint) without edits:
  blank line around every heading, list and fenced block, one H1, no
  duplicate heading text, no trailing punctuation in headings, no trailing
  whitespace, no hard tabs, file ends with a single newline.
- **Language** - English, unless the user asks for another language.
- **Table of contents** - required once a document has more than three H2
  headings: a bullet list of links to the H2 headings, placed under the
  intro paragraph. Service utilities are the exception - see below.
- **Size** - one item is at most one paragraph, three to four sentences.
  Prose that overflows becomes its own section. Lists, tables and code
  blocks do not count against it.
- **Style** - the simplest language that is still accurate: short sentences,
  active voice, second person in procedures. Link every external product on
  first mention.
- **Runbooks** - examples, tests and procedures are copy-pasteable: one
  command per line, no `$` prompt inside the block, expected output shown
  separately.

## Document types

Pick the type before writing. If the request fits none of them, ask the user
instead of guessing.

### Service utilities

Skills, agent instructions, memory and plans - documents an agent reads, not
a person.

- No table of contents, whatever the heading count.
- No runbooks: state the rule, do not demonstrate it.

### Project description

- Why the project exists, which tasks and goals it serves.
- How it implements those goals.

### Code description

- What the code does.
- Its main classes and methods.
- Two or three usage examples.

### Service description

- Why the service is needed.
- How it is implemented.
- How to install it.
- How to integrate it.
- Examples.

### SOP

- What the procedure covers.
- The procedure itself, as a copy-paste runbook.
- How to test that it worked.

### Known issues

- The problem: symptom, trigger, blast radius.
- A runbook that fixes it.

## Workflow

1. Identify the type, asking the user when it is ambiguous.
2. Read the repository's own conventions - `CLAUDE.md`, `GEMINI.md`,
   `CONTRIBUTING.md`, `docs/README.md` - before drafting. A
   repository-specific template is a contract: keep its headers, field
   lines and numbering.
3. Extend a document that already covers the topic rather than adding a
   second one.
4. Draft against the general rules and the type's required content.
5. Add or refresh the table of contents when the type allows one and the
   document has more than three H2 headings.
6. Validate, fix, revalidate.
7. Commit through the repository's commit flow.

## Validation

Markdown linters are rarely on `PATH`: they live in a project virtualenv, in
`node_modules`, or behind `pre-commit`. Find the one this repository uses,
then run it on the file. These two checks close the gap the linter leaves -
the first must print nothing, the second must show no stale link to a
document you renamed.

```bash
grep -nP '[^\x00-\x7F]' "docs/my-note.md"
grep -rn "old-basename" --include='*.md' .
```
