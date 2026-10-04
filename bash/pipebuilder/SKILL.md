---
name: pipebuilder
description: Build, inspect, verify, and maintain PipeBuilder PipeSpaces and PipeBuilder-managed Agent Skills. Use when creating or editing a Skill, changing pipespace.json, resolving Skill Providers or generated-artifact drift, running PipeBuilder commands, or updating the installed PipeBuilder CLI.
license: MIT
compatibility: Requires Python 3.7 or newer. Git is required only for Git Skill Providers.
---

# PipeBuilder

`pipebuilder.py` in this Skill directory is the complete standalone CLI. The
Skill provides Agent guidance; the Python file remains usable without an Agent.

## Locate the inputs

Before changing a PipeSpace, run:

```bash
python3 <skill-root>/pipebuilder.py explain <space> --format json
```

Use the report and `.pipebuilder/lock.json` to distinguish:

- `.pipebuilder/skills/<name>/`: PipeSpace-local source, highest priority.
- `pipespace.json.skillProviders[]`: shared folder or Git Provider source.
- `.agents/skills/`, `.cursor/skills/`, `.codebuddy/skills/`,
  `.claude/skills/`, `AGENTS.md`, and `.pipebuilder/lock.json`:
  Builder-owned outputs; do not edit them directly.

Same-name Skills shadow lower-priority candidates; their contents are not
merged.

## Build and verify

Run the following sequence from the target PipeSpace:

```bash
python3 <skill-root>/pipebuilder.py check . --format json
python3 <skill-root>/pipebuilder.py explain . --format json
python3 <skill-root>/pipebuilder.py build . --dry-run --require-no-post-commands --format json
python3 <skill-root>/pipebuilder.py build . --require-no-post-commands --format json
python3 <skill-root>/pipebuilder.py verify . --format json
```

Stop if `check` or the dry run fails. A build is complete only when `verify`
reports no input drift, digest drift, or orphaned output.

`--require-no-post-commands` is the default Agent-safe build mode: it fails
before the first write if any selected Provider declares a post command. If it
reports `PB018`, inspect the commands in `explain`; run ordinary `build` only
after their executable, arguments, working directory, and side effects are
approved. Do not treat the flag as a way to silently skip required commands.

If generated directories are protected by the host sandbox, request the
narrowest persistent permission for the exact PipeBuilder safe-build command
or installed `pipebuilder` executable. Never request a blanket Python, shell,
workspace-write, or approval-bypass rule. Keep `clean` separately approved
because it deletes lock-proven outputs. See
[references/build-permissions.md](references/build-permissions.md) for the
cross-Agent permission SOP.

Use `clean` to remove generated files proven by the lock. Never recursively
delete an Agent configuration directory.

For a Git Provider without network access, use `build . --offline`; this
requires a matching lock and immutable cache.

## Create or edit a Skill

1. Find the Provider source with `explain`; never edit an installed output.
2. Keep one coherent responsibility per Skill.
3. Create `<skill-name>/SKILL.md` with a matching lowercase kebab-case `name`
   and a `description` that states both what it does and when to use it.
4. Put deterministic executables in `scripts/`, detailed material in
   `references/`, and templates or resources in `assets/`.
5. Select the Skill explicitly in `pipespace.json.skills[]` or through
   intentional tag matching.
6. Run the complete build and verification sequence.

Test at least three prompts that should trigger the Skill, three adjacent
prompts that should not, one successful workflow, and one failure/recovery
path. If `skills-ref` is installed, also run:

```bash
skills-ref validate <provider-root>/<skill-name>
```

PipeBuilder verification remains the final workspace gate.

## Update the installed Skill

Preview and then synchronize the installed Skill directory from the latest
GitHub Release:

```bash
python3 <skill-root>/scripts/update.py --dry-run
python3 <skill-root>/scripts/update.py
```

Use `--tag vX.Y.Z` to pin an update to a release tag. The updater validates the
ZIP checksum and package manifest, restricts content to the portable Skill
directories, and then adds, replaces, or removes managed files as one update.
The package recursively includes `agents/`, `scripts/`, `references/`,
`assets/`, and `.pipe-agents/`; adding a resource there does not require an
updater file-list change.
