---
name: project-config
description: >
  Shows and changes what this project configures in its own `.claude/` — which skills and
  agents the audit trail records, the plan-window budget of the audit reports, whether a
  compose service stopped on purpose blocks the end of a turn — through `ArchHook.jar config`,
  the only writer, which validates every value before it writes. Explicit invocation only.
argument-hint: "[empty to list | <setting id> | <what to change, in plain words>]"
disable-model-invocation: true
allowed-tools: AskUserQuestion, Bash(java:*)
model: sonnet
effort: low
---

# `project-config` — the project's own settings, listed and changed through one writer

## Current settings

!`java -jar "${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/ArchHook.jar" config list 2>&1`

---

The block above is one JSON line from `config list`: every file this project may write for
itself, each key with its type, its allowed `values`, its `default`, its current `value`, what
it changes (`effect`), `fixed: true` when upstream owns it, `available: false` when the audit
trail is off, `in_force` and `problems` as `doctor` would print them. Where it did not expand —
a host with no `` !` `` injection, such as the GitHub Copilot CLI — run the same command first:

```bash
java -jar .claude/hooks/ArchHook.jar config list
```

## Why this is a skill (Form 2) and not an agent

A short procedure over one command's output, typed by hand because it changes a versioned
file (axes 2 and 3 of decision 0187). An agent was rejected: no context to preserve, no tool to
restrict beyond what `config` itself refuses, the same model — none of invariant 5's reasons.
The validation is not here either: it lives in `ArchHook.jar config`, so a person, this skill,
another agent and a later mod reach the same rule.

## Contract

**Class:** ops — the territory is `skill_classes.ops` in `@.claude/schemas/extensions.json`,
and it is **empty**: this skill writes no file with a tool. Every change is
`java -jar .claude/hooks/ArchHook.jar config set|unset`, which writes the file itself after the
validator `doctor` runs passes. `guard` refuses a Write, an Edit or a shell redirect into a
registered path, so editing the JSON by hand from here is not a way around it.

**Reads:** the `config list` output above. Which settings exist, their keys, values, defaults
and the decision behind each are data in `project_config` of `@.claude/schemas/extensions.json`;
this skill never restates them.

**Writes:** nothing directly. Through `config`: the files `project_config` lists, and only those.

**Out of reach:** a key marked `fixed` (today `arch-adopt` in `audited`, never audited); a
setting whose file is `available: false` (the audit trail is off — `.claude/audit-usage/`
missing — and writing a setting of it would switch the trail on); anything in
`.claude/settings.json`, `settings.local.json` or `extensions.json` itself, which `/arch-adopt`
overwrites.

## Procedure

### 1 · Show

No argument: render the block as one table per file — `path`, `summary`, then the keys whose
`value` is not null and every key whose `in_force` mentions it — and the `problems`, if any,
first. For `audited`, list only the pieces whose `value` differs from `default`; the full list
of skills and agents is noise until asked for. End with the decision of each file
(`decision`), cited by path, for whoever wants the reason.

`problems` not empty → say so before anything else: `doctor` reports the same line red, and a
gated one (`doctor.gate.labels`) fails CI. The way out is `config unset <id> <key>` for each key
it names.

### 2 · Decide what to change

An argument or a request names a change → map it to `<id> <key> <value>` from the block. A key
not in the block does not exist: say which keys do, never invent one. Ambiguous (which skill,
which value) → one `AskUserQuestion` with the candidates from the block, each option carrying
its `effect`; when a value differs from the `default`, say what that default protects — the
`effect` text and the decision record hold it.

### 3 · Confirm, then write

State the command and the line of the file it changes, and ask once. On yes:

```bash
java -jar .claude/hooks/ArchHook.jar config set <id> <key> <value>
java -jar .claude/hooks/ArchHook.jar config unset <id> <key>      # back to the default
```

Exit 0 prints the change. Exit 2 wrote nothing and printed why — relay it as printed and offer
the valid values from the block; never retry with a guessed value. Exit 1 is a usage error.

### 4 · Report

The file and the line changed, that it is versioned (commit it with the change it serves), and
the `doctor` line that now validates it (`doctor_label`). `/arch-adopt` never touches these
files: the setting survives every update.

## Failure modes

- **The block is a stack trace or `Unknown mode: config`.** The project's `ArchHook.jar` predates
  decision 0187. Tell the person to run `/arch-adopt`; do not edit the JSON instead.
- **`config: no project_config`.** Same cause, `extensions.json` side — `/arch-adopt`.
- **A guard refusal naming `config set`.** Something tried to write the file directly. Use the
  command it names.
- **`available: false` and the person wants a setting of the audit trail.** Creating
  `.claude/audit-usage/` switches the whole trail on; that is `/audit-usage`'s subject, not a
  setting. Say so and stop.
