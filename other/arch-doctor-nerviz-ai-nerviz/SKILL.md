---
name: arch-doctor
description: >
  Diagnoses the AI setup and architecture enforcement on this machine: active hooks,
  loaded boundary rules, Maven wrapper, `java` on PATH, which `.claude/` this project
  was written from and what has been edited since, and whether every docker-compose
  service is actually running with no foreign container on its ports and no image tag
  disagreeing with the one the test suite pins. Explicit invocation only.
disable-model-invocation: true
allowed-tools: Read, Bash(java:*), Bash(find:*), Bash(sort:*)
model: sonnet
effort: high
---

## Diagnosis

!`java "${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/ArchHook.java" doctor 2>&1`

## AI files

!`find "${CLAUDE_PROJECT_DIR:-.}/.claude" -maxdepth 2 -type f | sort`

---

Interpret the result above and tell the user, in two or three sentences, whether the
setup is operational. If something is marked with ❌, give the concrete command that
fixes it — don't describe the problem in general terms.

The `Provenance` line is the one exception to "give the command": when it lists files
edited locally, say which ones and that an update would overwrite them. Don't offer to
run the update — losing a hand-edited norm is the user's call, not a fix to apply.

Don't fix anything without the user asking.

## Why this is a manually-invoked skill

Form 2: the whole body is two shell injections plus how to read them, so it is a
procedure (axis 5) fired by a person who wants a verdict (axis 2 — `/arch-doctor`). Form 1
was rejected because a diagnostic the model reaches on its own runs a JVM and a `find` on
every session that mentions a hook; Form 3 was rejected because there is nothing to isolate —
the output is the report, and it is what the user asked to see.

Runs on `sonnet` with `effort: high`: the report is computed, but naming the cause and the
command that fixes it is judgment (`@.claude/decisions/0080-procedural-skills-on-sonnet.md`).

The name is not `doctor`: `/doctor` is a native command, and a skill folder with that name
shadows it silently — `@CLAUDE.md` § Known pitfalls.

## Contract

**Class:** observer — the territory is `skill_classes.observer` in
`@.claude/schemas/extensions.json`, and it is **empty**: this skill writes no file. It
reports, and the fix is the user's call. `ArchHook.java guard` enforces it.

**Reads** the output of `ArchHook.java doctor` (which folds in `compose`) and the listing of
`.claude/`, both injected above. Nothing else: an injection that lied about the setup would
be worse than no report.

**Writes** nothing, ever. Leaves no audit report either — its class, `observer` in
`skill_classes` of `@.claude/schemas/extensions.json`, declares `audited: false`, because an
observer that records its own observation makes the trail mostly about reading it.
