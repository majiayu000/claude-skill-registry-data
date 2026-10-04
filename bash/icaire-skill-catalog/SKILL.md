---
name: icaire-skill-catalog
description: Show the ICAIRE workbench catalog from README.md and install additional role-specific skills from this repo. Use when the user asks what ICAIRE skills exist, wants to see the skills catalog, wants to add more ICAIRE skills later, or wants role-specific skill recommendations.
---

# ICAIRE Skill Catalog

Show the ICAIRE skill catalog and install additional skills from this repo after
the initial general-purpose install. ICAIRE Cortex is remote; this workflow
does not require a BigBrain CLI or local brain runtime.

## Contract

- Treat `README.md` in the ICAIRE workbench repo as the source of truth for the
  catalog.
- Do not maintain a separate hardcoded list of departments or skills in this
  skill.
- General-purpose skills should already be installed by
  `INSTALL_FOR_AGENTS.md`; use this skill to inspect the catalog and add
  role-specific skills later.
- Ask before installing or removing skill symlinks.
- Use `CODEX_HOME` when it is set. Otherwise use `~/.codex`.
- Prefer `scripts/install_icaire_skills.py` from the workbench when it is
  available so catalog parsing and safe backups use one implementation.

## Workflow

1. Locate the ICAIRE workbench repo:
   - Prefer `~/projects/ICAIRE/icaire-workbench` when it exists.
   - Otherwise use `~/projects/ICAIRE/icaire-skills` when present and rename it
     to `~/projects/ICAIRE/icaire-workbench`.
   - Otherwise use `~/projects/icaire-skills` when present and rename it to
     `~/projects/ICAIRE/icaire-workbench`.
   - If neither exists, ask the user for the repo path or tell them to run
     `INSTALL_FOR_AGENTS.md` first.
2. Read the repo `README.md`.
3. Parse the `Skill Catalog` section:
   - `### General Purpose Skills`
   - `### Role Specific Skills`
   - nested `####` function sections
   - table rows whose first column is a backticked skill name
4. If the user only wants to see the catalog, summarize it by section and show
   the skill names with short purpose text from the README table.
5. If the user wants recommendations, ask what they do at ICAIRE and what
   workflows they expect Codex to help with. Match their answer to the
   role-specific function headings from the README.
6. Before installation, show:
   - general-purpose skills already expected to be installed
   - selected role-specific function headings
   - skill names that will be added
7. After explicit confirmation, symlink the selected skill directories into
   `$CODEX_HOME/skills`.
8. Verify every selected installed `SKILL.md` resolves under the ICAIRE workbench
   repo.

## Install Command

Use this command after the user confirms the role-specific sections to install:

```sh
cd ~/projects/ICAIRE/icaire-workbench
python3 scripts/install_icaire_skills.py \
  --runtime codex \
  --role-section "Comms" \
  --role-section "Research / Policy"
```

Use `--runtime claude` for Claude Code. Replace the example sections with exact
`####` headings from `README.md`.

## Output Requirements

- When showing the catalog, group skills under the same headings as the README.
- When recommending installs, explain which README headings matched the user's
  role and why.
- When installing, report installed skill names and verification results.
- If no role-specific skills match, ask the user to choose from the README
  headings instead of guessing.

## Guardrails

- Do not invent skills that are not listed in `README.md`.
- Do not install all role-specific skills by default.
- Do not edit skill files during catalog or installation work.
- Do not remove non-ICAIRE skills from `$CODEX_HOME/skills`.
