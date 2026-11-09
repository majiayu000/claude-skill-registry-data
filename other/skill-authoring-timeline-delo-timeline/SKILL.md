---
name: skill-authoring
description: Use when a lesson must become a skill, here or in a profile.
version: 1.0.0
author: TimeLine
license: MIT
platforms: [macos, linux]
metadata:
    hermes:
        tags: [skills, documentation, placement, anonymisation, contract]
---

# Skill Authoring

A procedure that worked is written into this repository, not into the agent's own profile. The
failure this prevents is invisible while it happens: a session learns how this tree builds or
publishes, saves the lesson under a profile directory, and every clone of this repository starts
without it. The person who owns the tree then watches their own tooling forget.

Nothing tracked may name a person or a machine path. This skill governs where a lesson lives and
what shape it takes.

## When to Use

- A procedure worked and the next session would have to rediscover it.
- A lesson exists in an agent profile and describes this repository rather than a method.
- A skill directory, its frontmatter, its index or its citation disagrees with the tree.
- Deciding whether a lesson belongs here or in the agent's profile.

## Where a skill lives

```
Documentation/Skill/<Name>/SKILL.md              the rules
Documentation/Skill/<Name>/Reference/            the worked instances and the tools
Documentation/Skill/<Name>/Reference/Index.md    what that directory holds
```

`.agents/skills` is a symlink to `Documentation/Skill/`, so a tool that looks for `.agents/` finds
the same files rather than a copy. Git stores the link; a checkout with `core.symlinks=false` writes
a small text file whose content is `../Documentation/Skill`, and the long path still works.

The repository root `AGENTS.md` carries the task → skill table. It is the index: a skill nobody is
pointed at is not loaded. `Documentation/README.md` carries the reader-facing list of the same
directories, and both are read together, because a skill the loader finds and the reader does not is
a folder nobody opens.

## The naming

- The directory is `PascalCase-Kebab`: `Tool-Archive`, `Timeline-Site-Build`, `RFC-Board`.
- The frontmatter `name` is that directory lowercased: `tool-archive`, `timeline-site-build`.
- The `description` is one sentence beginning `Use when`; it names the trigger, not the topic.
- The body carries its claims in a `## Claim → test` table, or in a `## Verification` table under
  the same rule. A `## References` list may follow the table.

## What belongs here, and what does not

The test is one question: **would this be wrong for a different repository?**

- Wrong elsewhere - this tree's build, storage, transport, board, conventions - belongs here.
- Right anywhere - how to write a skill, how to split work between agents, how a browser tab is
  driven - belongs in the agent's profile, where every repository gets it.
- A lesson that is both goes in both: the method in the profile, the instance here. Patching only
  the profile leaves this clone starting from zero, and the next session re-learns what this one
  already proved.

A skill that ships inside a repository is boilerplate: it describes the class of repository, never
one instance. A project id, an account handle, an absolute path or a token belongs in `.env` or
`Maintain/Configuration/Local/`, never in a tracked file - `Documentation/Reference/Configure.md`
states where each one goes.

## What the body holds

- Rules in `SKILL.md`; a worked instance in `Reference/` behind a one-line pointer.
- `Reference/Index.md` lists every file in that directory, including the ones with no tool at all -
  a directory that archives nothing says so and why.
- A script that ran belongs to a skill (`Documentation/Skill/Tool-Archive/SKILL.md`). A tool that
  names a machine cannot be archived: `archive_tool.py --audit` is the gate, and it covers Markdown
  as well as code, so a skill's prose is held to the same rule as its scripts.
- Every rule that asserts behaviour carries the command that proves it, or is marked as intent. A
  rule that names nothing is `open` in the record header, and reads as unsettled to anyone who
  checks.

## Pitfalls

- **A profile skill is shadowed, not merged.** A repository skill with the same name wins in a
  session started inside the repository, so the profile copy is read by nobody and drifts silently.
- **A skill written here is invisible to the session that wrote it.** The index is built when a
  session starts; the file is found by the next one. Write it now, and do not conclude from its
  absence that it was not saved.
- **A directory with no `Reference/Index.md` is a half-written skill.** The reading order refuses
  it: the index is where a reader learns what sits beside the prose.
- **A name typed in two places drifts.** The directory and the frontmatter `name` are one fact, and
  they are changed together, because a rename that misses one leaves a skill nothing can address.
- **A formatter rewrites prose.** Prettier reflows these files at 100 columns with tabs. Run it on
  the files you touched, never across the tree, and never on a generated artifact.
- **A `Reference/` test that no root script runs never gates.** Nothing in this tree runs a test
  suite, so a test written beside a tool is hand-run only and a regression in that tool passes
  review unless someone runs it. Name the raw invocation in the skill's claim table, and run it with
  `python3 -B` so the run writes no `__pycache__` beside the tool.

## Claim → test

| Claim                                            | Test                                                                                   |
| ------------------------------------------------ | -------------------------------------------------------------------------------------- |
| Every skill has a body and an index              | the directory holds `SKILL.md` and `Reference/Index.md`                                |
| The frontmatter name matches its directory       | the directory name lowercased is the header's `name`                                   |
| Every skill is cited from `AGENTS.md`            | `grep -c '<Name>/' AGENTS.md` returns at least one                                     |
| Every skill appears in `Documentation/README.md` | `grep -c '<Name>/' Documentation/README.md` returns at least one                       |
| Every reference file is listed in its `Index.md` | `ls Reference/` and the index table name the same set                                  |
| Every skill states a testable claim              | the body carries a claim table or a `## Verification` table                            |
| The skill tree names no machine path             | `python3 .../archive_tool.py --audit` prints `clean: no home paths`                    |
| The tracked tree carries no identifier           | review the diff: no tracked file names a person, a handle or a home path               |
| The repository's skills load for a session       | `hermes skills trust <absolute repository root>` prints `N project skill(s) will load` |
