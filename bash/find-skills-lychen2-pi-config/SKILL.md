---
name: find-skills
description: Find and install agent skills when the user explicitly asks for reusable capabilities, workflows, or skill recommendations. Specialized tasks do not require skill discovery.
---

# Find Skills

Find skills that fit the requested task and available environment. Check already
installed capabilities first; a new package is useful only when it adds something
the user needs.

## Search and select

1. Identify the requested capability and constraints from context. Ask only when a
   missing requirement changes the candidates.
2. Use available skill discovery or `npx skills find <query>`. A marketplace or
   repository search can fill a gap; visiting a leaderboard is not a prerequisite.
3. Read the promising skill's instructions, dependencies, and supported workflow.
   Judge fit from its content and maintenance; stars and installation counts are
   supporting signals, not minimum thresholds or proof of quality.
4. Present the best matches with their purpose, source, and installation command.
   Mention a dependency or compatibility limit when it affects use. Avoid a search
   diary, quality checklist, or stock disclaimer. If no candidate fits, state that
   directly and give a workable next action.

## Install within the requested scope

When installation is requested, inspect unfamiliar package instructions and scripts
at that external-code boundary. Use the host's supported skill location and preserve
existing user skills. Do not run a global update to install one skill.

Common commands, when the Skills CLI is appropriate:

```bash
npx skills find <query>
npx skills add <owner/repo@skill>
npx skills check
```

Use global or noninteractive flags only when they match the authorized installation
scope. Reuse that authorization for the installation and its focused verification.

## Delivery

Return the requested recommendations or the installed skill's path and invocation.
Keep necessary installation/review notes in native comments when producing a saved
artifact; if comments are unavailable, use the conversation outside it. Omit routine
process notes. Do not copy the skill's operating instructions into an unrelated
deliverable.
