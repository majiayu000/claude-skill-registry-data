---
name: pr-workflow-skills
description: >
  PR lifecycle management: creating PRs with repo templates, addressing GitHub PR review comments,
  running asynchronous background PR reviews and checks, and finishing/merging development branches.
---

# PR Workflow

Meta-skill consolidating pull request workflow expertise. Each sub-skill below is a
full standalone skill with its own instructions, scripts, and references.
Match the user's intent to the most specific sub-skill, then read its
SKILL.md and follow its instructions completely.

## Sub-Skills

### pr-creator
- **Description:** Use this skill when asked to create a pull request (PR). It ensures all PRs follow the repository's established templates and standards.
- **Path:** `.subSkills/pr-creator/SKILL.md`

### pr-address-comments
- **Description:** Use this skill if the user asks you to help them address GitHub PR comments for their current branch. Requires `gh` CLI tool.
- **Path:** `.subSkills/pr-address-comments/SKILL.md`

### async-pr-review
- **Description:** Trigger this skill when the user wants to start an asynchronous PR review, run background checks on a PR, or check the status of a previously started async PR review.
- **Path:** `.subSkills/async-pr-review/SKILL.md`

### finishing-dev-branch
- **Description:** Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
- **Path:** `.subSkills/finishing-dev-branch/SKILL.md`

## Routing Instructions

1. Read the user's request carefully.
2. Match their intent against the sub-skill descriptions above.
3. Read the matched sub-skill's SKILL.md at the given path and follow its instructions completely.
4. If the intent clearly spans multiple sub-skills, start with the primary match and note the others for follow-up.
5. If no specific sub-skill matches but the request is clearly in this domain, use the default sub-skill.
6. **Default sub-skill:** pr-creator

## Disambiguation

- "PR" without context -> pr-creator (most common entry point)
- "address comments" / "fix review feedback" -> pr-address-comments
- "review this PR" (async/background) -> async-pr-review
- "I'm done, how do I merge" / "finish this branch" -> finishing-dev-branch
