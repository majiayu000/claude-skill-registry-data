---
name: docs
description: Use after a change or a release, to write and refresh the runbook and the how-to guides of the project, so the runbook and the guides match the code.
argument-hint: "[change]"
---

# Docs

The job: the runbook and the how-to guides, matching the code every time. It writes the docs, never the code. The standards and the source pages are checked by the knowledge-refresh skill, and the incident log gets its entries from the incident skill.

Input: none, or the change to document.

## Steps

1. List what changed since the docs were last written: the diff, the new files, the renamed things.
2. The runbook: every command, in order, as it runs today. Check that each command exists and that its flags parse, with --help or a dry run. Never run a command that writes data or starts a job.
3. The how-to guides: one per repeated task of the project, the steps as a new colleague would follow them.
4. Check every guide against the code: every path exists, every name is the name in the code.
5. Link the facts instead of copying them. A source, a business term or a rule links to its page in the knowledge, and a repeated passage becomes a link.
6. Report what was out of date and what is now written.

## Output

The runbook and the how-to guides as Markdown files in the docs folder, every command and every path checked against the code.

## Reads

- the code, the scripts, the run records, the existing docs, the knowledge

## Writes

- the runbook and the how-to guides

## Never

- Never changes the code to match the docs.
- Never invents a fact: where the code says nothing, write "unknown".
