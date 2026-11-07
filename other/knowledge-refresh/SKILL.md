---
name: knowledge-refresh
description: Use after a release, to compare the knowledge Claude Code reads, CLAUDE.md, the standards, the source pages and the incident log, with the code and the data, and propose what is stale, missing or wrong.
argument-hint: "[area]"
---

# Knowledge refresh

The job: keep the knowledge that Claude Code reads true to the project: CLAUDE.md and the knowledge folder. It proposes, and after the data engineer's yes it writes the approved changes. The runbook and the how-to guides belong to the docs skill.

Input: none, or the area to check.

## Steps

1. CLAUDE.md: every folder it names exists, every skill is listed, every path is right.
2. The standards against the code: naming, layers, code style.
3. The sources against the contracts and the files: one page per source, current.
4. The business: the glossary and the stakeholders against the documents.
5. The architecture and the core model against what is built.
6. The known issues and the incident log: what a run has proven since. The incident skill adds the entries, this skill checks them.
7. The decision log: what is decided, what is still open.
8. A document nobody has read yet: what it adds to the knowledge.
9. Keep it short: what repeats another file is cut and linked.
10. Report every finding as a proposal: the file, what it says, what is true.

## Output

A list of proposals, one per finding: the file, what it says, what is true, and the change. After the yes, the approved changes in the knowledge files.

## Reads

- the knowledge, the code, the data contracts, the documents, the run records

## Writes

- nothing until the yes, then only the knowledge files the data engineer approved

## Never

- Never applies a change without the yes.
