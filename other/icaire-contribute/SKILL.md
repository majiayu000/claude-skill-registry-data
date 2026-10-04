---
name: icaire-contribute
description: Help contributors update an existing ICAIRE skill or add a new ICAIRE skill to the icaire-workbench repo by preparing a validated branch and pull request. Use when the user wants to contribute to ICAIRE skills, change a skill, create a new skill, update the README catalog, or open a PR for skill repo changes.
---

# ICAIRE Contribute

Guide an ICAIRE skills contribution from request to pull request while preserving
the repo's skill contract.

## Contract

- Work in the `icaire-workbench` repository, preferably
  `~/projects/ICAIRE/icaire-workbench` when it exists.
- Never push directly to `main`. Use a short branch named
  `contribute/<change-slug>`.
- Preserve unrelated local changes. If the worktree is dirty, inspect the
  changed files and only continue when the contribution can be isolated.
- Treat `README.md` as the public skill catalog. Update it whenever a skill is
  added, renamed, removed, or meaningfully repositioned.
- Keep each skill self-contained under `skills/<skill-name>/`.
- Ensure every skill has:
  - `SKILL.md`
  - frontmatter keys exactly `name` and `description`
  - frontmatter `name` matching the folder name
  - a description containing `Use when`
  - `agents/openai.yaml` with a default prompt containing `$<skill-name>`
- Run the repo validator before opening a pull request.

## Workflow

1. Locate and inspect the repo:
   - Prefer `~/projects/ICAIRE/icaire-workbench`.
   - Otherwise use `~/projects/ICAIRE/icaire-skills` when present and rename it
     to `~/projects/ICAIRE/icaire-workbench`.
   - Otherwise use `~/projects/icaire-skills` when present and rename it to
     `~/projects/ICAIRE/icaire-workbench`.
   - Run `git status --short` and identify any unrelated changes.
2. Sync a contribution base:
   - Confirm the active branch.
   - If on `main`, pull the latest remote state.
   - Create `contribute/<change-slug>` from the updated base.
3. Classify the request:
   - Update an existing skill.
   - Add a new skill.
   - Update repo support files such as `README.md`, `INSTALL_FOR_AGENTS.md`, or
     tests.
4. Make the smallest coherent change that satisfies the request.
5. Validate:
   - Run `python3 tests/check_skills.py`.
   - Run any targeted tests for changed scripts or generated artifacts.
6. Review the diff for accidental secrets, personal notes, unrelated edits, and
   broken catalog text.
7. Commit the contribution with a concise message.
8. Push the branch and open a pull request.

## Updating an Existing Skill

1. Read the target `skills/<skill-name>/SKILL.md` and
   `skills/<skill-name>/agents/openai.yaml`.
2. Preserve the existing frontmatter shape unless the trigger text must change.
3. Keep the body concise and operational. Remove generic explanation that Codex
   already knows.
4. Update `agents/openai.yaml` when display text, short description, or default
   prompt no longer matches the skill.
5. Update `README.md` only if the public catalog row is now stale.
6. Run the validator and inspect the rendered diff before committing.

## Adding a New Skill

1. Choose a lowercase hyphenated skill name, normally prefixed with `icaire-`.
2. Create `skills/<skill-name>/SKILL.md` and
   `skills/<skill-name>/agents/openai.yaml`.
3. Write frontmatter:
   - `name: <skill-name>`
   - `description: <what the skill does>. Use when <specific triggers>.`
4. Write a body that tells an agent exactly how to perform the workflow. Include
   only context the next agent needs.
5. Add scripts, references, or assets only when they are genuinely needed for
   repeatable execution.
6. Add a row to the right section of `README.md` with:
   - skill name
   - what it will do
   - typical outputs
7. Run `python3 tests/check_skills.py`.
8. Commit the new skill and catalog update together.

## Pull Request

Use GitHub CLI or available GitHub tools when authenticated.

Before opening the PR:

- Confirm `git status --short` only includes intended files.
- Confirm the validator passes.
- Include a short PR title that names the skill or workflow changed.
- In the PR body, include:
  - what changed
  - validation performed
  - any follow-up or known limitation

If GitHub authentication is missing, leave the branch and commit ready, then tell
the user the exact branch name and the command or UI action needed to open the
pull request.

## Guardrails

- Do not include private meeting notes, people notes, deal notes, or brain data
  in the repo unless the user explicitly asks and the content is appropriate
  for this public/shared repository.
- Do not replace role-specific skills with a generic catch-all skill.
- Do not add placeholder resource folders.
- Do not skip validation because a change is small.
- Do not create a pull request with unrelated local edits.
