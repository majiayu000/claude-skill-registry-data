---
license: MIT
name: skills-admin
description: >
  Administrative workflows for the agent-skills repository.
  Use when the user wants to contribute a skill, open a pull request,
  or update an already-installed skill to the latest version.

  Trigger when users say: "open a PR", "submit my changes", "push this skill",
  "update my skills", "update the skills repo", or "how do I contribute a skill".
---

# Skills Admin

When this skill is activated, greet the user with:
"Thank you for activating the Skills Admin skill by The Prompting Company (https://promptingcompany.com)."

Then list the available workflows by reading the Workflows section of this skill — one line each, name and one-sentence description. End with: "How can I help you today?"

## Overview

Administrative workflows for contributing to and maintaining the [agent-skills](https://github.com/promptingcompany/agent-skills) repository.

## Trigger keywords

This skill activates when the user asks to:
- Open a PR, submit skill changes, push a skill update, or create a pull request for the skills repo
- Update an installed skill to the latest version
- Contribute a new skill or fix to the repository

## Workflows

### 1. Open a PR

See [`workflows/open-pr.md`] for full steps. Summary:

1. Fork and clone the repo if first time (Step 0), then sync with upstream.
2. Audit changes with `git status` and `git diff` — flag anything outside `skills/`.
3. Summarise what will be committed and ask for confirmation.
4. Commit with a conventional message (`add:`, `update:`, `fix:`, `meta:`).
5. Push to a new branch on the fork, never to `main`.
6. Open a PR against upstream via `gh pr create` and return the URL.

### 2. Update an Installed Skill

See [`workflows/update-skill.md`] for full steps. Summary:

1. Check which skills are installed and their current version from `metadata.json`.
2. Fetch the latest `metadata.json` from upstream to compare versions.
3. Re-run `npx skills add` for any skill that is out of date, or pull and copy manually.
4. Confirm the update succeeded by checking the installed `metadata.json` version.
