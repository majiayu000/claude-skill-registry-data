---
name: ss-references
description: A library of shared templates that other ss-* skills read at runtime — subagent dispatch prompts, the technical-proposal template and its quality checklist, the OpenSpec directory skeleton, and the multi-repo detection rules. Not invoked directly by users; skills like ss-coding, ss-proposal, ss-write-spec, and the workflows read the file they need before producing an artifact.
---

# Shared References

This skill is a template library, not a workflow. It has no standalone "run"
behavior. Other skills read one of the files below at the exact point where they
need to dispatch a subagent, generate an artifact, or make a routing decision.

## What's Here

| File | Covers | Read When |
|---|---|---|
| `implementer-prompt.md` | The dispatch prompt shape for implementer subagents | Before dispatching an implementer (`ss-coding`) |
| `proposal-template.md` | Section-by-section structure of a technical proposal | Before writing a proposal (`ss-proposal`) |
| `proposal-writing.md` | Quality-standards checklist a proposal must pass | During a proposal's self-review (`ss-proposal`) |
| `openspec-skeleton.md` | The `openspec/` directory skeleton for a project that has none | Before writing specs into a project without an `openspec/` tree (`ss-write-spec`, `ss-reverse-spec`) |
| `multi-repo-detection.md` | Rules for deciding whether a requirement spans repositories | At a workflow's entrance, and after a proposal records its repository list |

## How Other Skills Reach It

Skills reference these files by sibling relative path — `../ss-references/<file>.md`
— which resolves both in this repository and after an install flattens every skill
directory into the same parent (`~/.agents/skills/`). This directory is a skill, and
not a bare folder, precisely so that installers carry it along: the `skills` CLI only
copies directories that contain a `SKILL.md`.

Because of that, the skills here must be installed as a bundle. Installing a single
skill on its own (for example `--skill ss-coding`) leaves its `../ss-references/…`
reads dangling.
