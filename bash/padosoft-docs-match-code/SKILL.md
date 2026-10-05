---
name: padosoft-docs-match-code
description: >-
  Use this skill when writing or reviewing documentation that quotes the code — a README, a CLAUDE.md or
  AGENTS.md, a SKILL.md, an ADR, an onboarding guide, an API doc — and whenever the user reports that a
  documented command, column, env var or flag does not exist, that setup instructions fail on a clean
  machine, that the docs describe an older behaviour, or asks to document a feature. It checks the quoted
  facts against migrations, models, config, command signatures and routes, and prefers a generated or
  pointed-to source over a copied snippet. Do not use it for writing style, for choosing a docs platform, or
  for translating existing documentation.
license: MIT
compatibility: >-
  Language-agnostic. The verification commands assume a POSIX shell and a repository you can read.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: Every fact quoted from the code is verified against the code before merging.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: documentation, readme, drift, schema, env vars, onboarding, adr, api docs
---

# Docs match code

Documentation that quotes the code **is code**: a column name, an env var, a command flag, a route, a
response shape. The difference is that nothing fails when it goes stale — it just quietly starts lying, and
the person it lies to is the one with the least context to notice.

**The rule: every fact quoted from the code is verified against the code before merging.**

---

## 1. What counts as a quoted fact

| In the docs | Verify against |
|---|---|
| A table or column name, a type, a nullability | the migration, the model |
| An environment variable | the example env file, the config that reads it |
| A command and its flags | the command's own signature/help |
| A route, verb or path | the route list |
| A response shape or field | the resource/serializer, or a real response |
| A file path | the filesystem |
| A default value | the code that defines it, not the docs that repeated it |

Prose about *why* is not a quoted fact and does not rot the same way. It is the concrete nouns that drift.

## 2. Verify, do not remember

```bash
# env vars named in the docs but absent from the example file
rg -o "[A-Z][A-Z0-9_]{3,}" README.md docs/ | sort -u > /tmp/doc-vars
rg -o "^[A-Z][A-Z0-9_]*" .env.example | sort -u > /tmp/real-vars
comm -23 /tmp/doc-vars /tmp/real-vars | head

# a column named in the docs, against the migrations
rg -n "column_name" database/migrations/ app/Models/

# a command's real signature
<your-cli> help <command>        # then compare flag by flag
```

The check that matters is the boring one: **open the file the doc is describing**. Most drift is one
renamed thing that nobody grepped for.

## 3. Prefer a pointer or a generator to a copy

A snippet copied into a document is a fork of the truth, and forks diverge. In order of preference:

1. **Generate it.** A section between markers, rebuilt from the source by a script, with CI failing when it
   is stale. This is the only option that cannot rot.
2. **Point at it.** "The full list is in `config/x.php`" beats reproducing the list.
3. **Copy it, and mark it.** If you must copy, say where it came from, so the next person knows what to
   re-check.

The cost of (1) is one script; the cost of (3) is every reader who trusted the copy.

## 4. Onboarding instructions are executable claims

"Clone, copy the env file, run these three commands" is a promise that it works on a clean machine. It is
also the documentation that rots fastest, because the people who write it never run it again.

Test it the only way that counts: a fresh clone, an empty environment, and the steps exactly as written —
nothing from your shell history, no assumed global tool. Whatever you had to do that is not in the file is
the part that was missing.

## 5. Agent instruction files rot the same way, and cost more

`CLAUDE.md`, `AGENTS.md`, skill files and the like quote paths, commands and rules. When one goes stale the
agent does not warn you: it follows the stale instruction confidently, which is worse than having no
instruction. Treat them as documentation with a shorter fuse.

Two specific traps:

- **A rule that names a file, a helper or a flag that has been renamed.** The agent looks for it, does not
  find it, and improvises.
- **Documentation that teaches the pattern you just fixed.** If you correct instances of an anti-pattern and
  leave the example that taught it, the next change reintroduces it — you fixed the symptom and kept the
  cause.

## 5b. State files rot by time, not by drift

A progress ledger, a continuity note, a lessons file: these do not quote the code, they describe **a moment**
— and the moment passes while the file stays. Four rules keep one true:

- **Write memory as a dated historical observation**, not as a present-tense fact. "On <date> the tree was
  untracked" stays true forever; "the tree is untracked" becomes false the day it is committed, and the file
  now lies without anyone editing it.
- **Record the state *after* the action, plus the next gate.** A ledger committed saying "staged, not yet
  committed" is stale in the same commit that carries it. Worse is one saying "amend this commit, then push":
  once that commit is under review, following the instruction rewrites published history.
- **Keep it collaborator-neutral and machine-neutral.** No contributor name, no absolute path from the
  authoring machine. Record the branch identity and the command that *discovers* the path, so the file works
  for the next person and the next clone.
- **Do not promise a tool the reader may not have.** If a check is mandatory it lives in the repository or is
  installed reproducibly; anything environment-owned is labelled supplementary.

The same applies to a lessons file itself: append a fix only once it is confirmed, with the test or rule that
prevents recurrence — otherwise it accumulates hypotheses that read like conclusions.

## 6. When the code changes, the docs are part of the change

Not a follow-up, not a ticket: the same commit. The reviewer who can tell whether the doc is now right is
the reviewer of that diff, and only for as long as the diff is open.

The question at the end of a change: *did I rename, move, add or remove anything a document names?*

---

## Gotchas

- **A doc test that only checks links is measuring nothing about content.** Links resolving does not mean the
  column exists.
- **Copy-paste across projects carries the other project's truth.** A README that started as another repo's
  README describes that repo until every line is checked.
- **The example that is "obviously" right is the one that is wrong**, because nobody re-reads it.
- **Generated sections still need the generator to run in CI.** A `make docs` that only humans run drifts the
  same way, just more slowly.
- **Screenshots are documentation too**, and they are the hardest to keep true. Prefer describing the state
  over showing a UI that will be restyled.

## Checklist

- [ ] Every column, env var, command, flag, route and path in the diff's docs verified against the source
- [ ] Onboarding steps run from a clean clone, exactly as written
- [ ] Copied snippets replaced by a pointer or a generated section, or marked with their source
- [ ] Agent instruction files checked for renamed files, helpers and flags
- [ ] No example left teaching a pattern that was just fixed
- [ ] Docs changed in the same commit as the code they describe

## Final report

```
Docs touched: <files>
Facts verified: <n> (columns, env vars, commands, routes, paths)
Drift found: none | <doc:line → real value>
Copies converted to pointer/generated: <n>
Onboarding steps run clean: yes | no | not applicable
```
