---
name: bundle-author
disable-model-invocation: true
description: 'Scaffolds ycc skills and agents for ycc maintainers only. Use when adding a ycc skill, adding a ycc agent, or extending bundle source.'
argument-hint: '<skill-name> [--skill-only] [--with-agent] [--dry-run]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash(ls:*)
  - Bash(test:*)
  - Bash(mkdir:*)
  - Bash(chmod:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/bundle-author/scripts/*.sh:*)'
---

# ycc Bundle Author

This skill scaffolds new source-of-truth surfaces under `ycc/` — skills and optional
agents. Skills themselves provide slash invocation. It is a contributor workflow scoped
strictly to this repo's `ycc/` tree. It writes nothing under `.cursor-plugin/` or `.codex-plugin/` (those are
regenerated), and it emits the exact follow-up commands needed to sync the derived
bundles after scaffolding completes.

## Arguments

Parse `$ARGUMENTS`:

- **skill-name** (required, first positional) — kebab-case identifier, no leading or
  trailing hyphens.
- **--skill-only** — stamp `user-invocable: false` into skill frontmatter for
  passive guidance that should not appear in the slash menu. Model invocation
  remains available. Otherwise the skill is user-invocable as a native slash command.
- **--with-agent** — also scaffold `ycc/agents/<skill-name>.md`.
- **--dry-run** — preview only; writes nothing.

The older `--with-command` flag is accepted as a legacy no-op. It never creates
a wrapper or overrides `--skill-only`.

**Questions:** class `clarify` (Phase 0 anti-pattern match "proceed?"): headless (no question tool or chat turn), print the matched anti-pattern and stop; scaffold nothing. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

## Phase 0: Guards

Before scaffolding, verify all of the following. If any check fails, abort immediately
with a clear, specific message.

1. `skill-name` matches the regex `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`. Reject names with
   uppercase letters, leading/trailing hyphens, or consecutive hyphens.
2. None of the target paths already exist:
   - `ycc/skills/<skill-name>/`
   - If `--with-agent`: `ycc/agents/<skill-name>.md`
     Use `test -e` for each path and abort if any returns true.
3. Name does not collide with an existing skill or agent. Use `ls` on
   `ycc/skills/` and `ycc/agents/` to confirm.
4. Re-read `${CLAUDE_PLUGIN_ROOT}/skills/bundle-author/references/when-not-to-scaffold.md`
   and check whether any anti-pattern applies to the user's request. If a match is
   detected, surface it explicitly and ask whether to proceed before continuing.

## Phase 1: Preview

Read `${CLAUDE_PLUGIN_ROOT}/skills/bundle-author/references/surface-map.md`. Present the
user with the full list of files that will be created:

- `ycc/skills/<skill-name>/SKILL.md` (with `user-invocable: false` stamped in the
  frontmatter when `--skill-only` is set)
- `ycc/skills/<skill-name>/references/` (directory, no files created by default)
- If `--with-agent`: `ycc/agents/<skill-name>.md`

Note that `scripts/` subdirectories are not created by default. If the skill will need
bash helpers, the contributor adds `ycc/skills/<skill-name>/scripts/` manually after
reviewing the scaffolded output.

## Phase 2: Dry-run check

If `--dry-run` was passed: print the file list from Phase 1, then print the exact
post-scaffold commands from Phase 4 (substituting the real skill name), and STOP. Do not
invoke the helper script.

## Phase 3: Scaffold

Invoke the helper:

```
${CLAUDE_PLUGIN_ROOT}/skills/bundle-author/scripts/scaffold-skill.sh <skill-name> [--skill-only] [--with-agent]
```

The helper copies templates from
`${CLAUDE_PLUGIN_ROOT}/skills/bundle-author/references/templates/` and substitutes
`{{NAME}}` and `{{DESCRIPTION}}` placeholders (`references/templates/skill-template.md`,
run when scaffolding any skill in Step 1). `--with-agent` also renders
`references/templates/agent-template.md`; read it only to check the rendered agent file. If the helper exits with a non-zero
status, STOP and surface its stderr verbatim — do not attempt to repair or work around
the failure.

## Phase 4: Post-scaffold steps

Always emit the following block to the user after a successful scaffold, substituting
`<skill-name>` with the actual name. Omit line 2 unless `--with-agent` was passed.

```
Next steps:
1. Edit ycc/skills/<skill-name>/SKILL.md to replace TODOs.
2. If --with-agent: edit ycc/agents/<skill-name>.md.
3. If you added scripts under ycc/skills/<skill-name>/scripts/: chmod +x them.
4. Regenerate derived bundles: ./scripts/sync.sh
5. Validate: ./scripts/validate.sh
```

## Evals

A new skill ships with **3 eval cases** under `ycc/evals/`: two prompts that
must load the skill and one near-miss that must load a sibling or nothing (under
`trigger/`), each graded with `tool_used: Skill`. Manual-only skills
(`disable-model-invocation: true`) replace the two positive cases with
no-autoinvoke cases under `ycc/evals/policy/` (`min: 0`, `max: 0`). Skills with a hard gate (confirmation, dry-run,
no-write default) also get a case under `ycc/evals/behavior/` with deterministic
graders. Copy an existing case, run it with `./scripts/eval.sh --case <name>`,
and keep descriptions fixed until it passes. See `ycc/evals/README.md`.

## Important Notes

- Never writes under `.cursor-plugin/` or `.codex-plugin/` — those are regenerated by
  `./scripts/sync.sh` from sources in `ycc/`.
- Never edits `ycc/.claude-plugin/plugin.json` or `.claude-plugin/marketplace.json` —
  those are maintained by the `bundle-release` workflow.
- Refuses generic scaffolding for external repos — see
  `${CLAUDE_PLUGIN_ROOT}/skills/bundle-author/references/when-not-to-scaffold.md`.
- Prefer extending an existing skill over adding a near-duplicate. Run `ls ycc/skills/`
  to confirm no existing skill covers the same domain before proceeding.
