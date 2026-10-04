---
name: file-issues
description: Use when the user asks in plain words to file, open, write or split GitHub issues. Not for a brief spec stores, closing or editing an existing issue, a plan, or a repository the working directory does not point at.
argument-hint: <what the issue or issues should cover>
allowed-tools: Bash(gh issue *), Bash(gh label *), Bash(gh project *), Bash(gh pr list *), Bash(git log *), Bash(node *repo-fields.mjs*)
model: opus
effort: high
---

# File issues that read as specs

An issue states what must become true, so a later plan can be written against
it. The enemy is the story issue: the occasion that prompted it, a quote from
the prompt, and a background paragraph repeating the labels, type and parent
that GitHub already shows beside the body. The overcorrection is the one-line
issue that never says when it is done, which pushes the whole spec into the
plan.

A plain request to file, open, write or split issues authorizes creating them,
with their labels, type, project fields, relations and milestone, and creating
the default labels `references/fields.md` names when the repository defines
none of its own. It never closes an issue, never deletes one, and never edits
an existing one, except to add a relation to a parent or a blocker the user
named.

## Steps

1. **Intake.** Turn the request into one goal sentence per issue, each tied to
   the part of the request it came from.
   - Never invent an issue the request does not ask for.
   - A goal sentence that needs an "and" for two unrelated outcomes is too
     big: propose a parent plus sub-issues, listing the split, and ask once.

2. **Read the repository, invent nothing.** Run
   `node "${CLAUDE_SKILL_DIR}/scripts/repo-fields.mjs"` and pick the vocabulary
   from its JSON, as `references/fields.md` says.

3. **Ground the references.** Send the `exo:locate-code` agent the paths and
   symbols the goal sentences name, so `References` carries real paths.
   Skip this step for an issue that names no code.

4. **Create in dependency order**, in the same turn and with no approval
   question first: a parent before its children, a blocker before what it
   blocks, with the commands and field settings in `references/fields.md`.

5. **Read back.** Read each created issue back with
   `gh issue view <n> --json number,title,labels,milestone,url` and report its
   URL, title and one metadata line.

## The body

Write it in the language of the existing issues, which the script's `titles`
shows. When there are none, follow the language of the recent pull requests and
commits
(`gh pr list --limit 5 --json title --jq '[.[].title]'`,
`git log -5 --format=%s`). The skill's own text stays English.

A brief or any feature work takes the Spec shape in `references/fields.md`; a
bug, a regression, a chore or a documentation fix takes the Report shape below.

- `### What happens`: one sentence naming the current behavior, in the present tense.
- `### Expected`: what should happen instead.
- `### Steps`: the prompts or commands that produce it, in order.
- `### Environment`: the versions and the platform the repository's own bug template asks for, one per line; where it has no template, the tool versions and the operating system.
- `### Evidence`: the output, transcript or log lines that show it, the relevant ones only and with secrets removed.

## References

| File | Read it when |
|---|---|
| `references/fields.md` | Steps 2 and 4, and before writing a Spec body. |

## Judgment

- Explicit user instructions outrank this skill, including a body section it
  forbids: say once that the metadata already shows it, then write it.
- A request to change or close an existing issue leaves this skill: report it
  and let the user run the `gh` command.
- A repeated request for one issue after a proposed split is the decision.
