---
name: code-review-skills
description: >
  Code quality lifecycle: reviewing PRs and local changes, requesting and receiving review feedback, detecting duplication and reinvented wheels, and auditing user-facing strings for clarity and style.
---

# Code Review Skills

Meta-skill consolidating code quality and review expertise. Each sub-skill below
is a full standalone skill with its own instructions, scripts, and references.
Match the user's intent to the most specific sub-skill, then read its
SKILL.md and follow its instructions completely.

## Sub-Skills

### code-reviewer
- **Description:** Use this skill to review code. It supports both local changes (staged or working tree) and remote Pull Requests (by ID or URL). It focuses on correctness, maintainability, and adherence to project standards.
- **Path:** `.subSkills/code-reviewer/SKILL.md`

### requesting-review
- **Description:** Use when completing tasks, implementing major features, or before merging to verify work meets requirements
- **Path:** `.subSkills/requesting-review/SKILL.md`

### receiving-review
- **Description:** Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
- **Path:** `.subSkills/receiving-review/SKILL.md`

### review-duplication
- **Description:** Use this skill during code reviews to proactively investigate the codebase for duplicated functionality, reinvented wheels, or failure to reuse existing project best practices and shared utilities.
- **Path:** `.subSkills/review-duplication/SKILL.md`

### string-reviewer
- **Description:** Use this skill when asked to review text and user-facing strings within the codebase. It ensures that these strings follow rules on clarity, usefulness, brevity and style.
- **Path:** `.subSkills/string-reviewer/SKILL.md`

## Routing Instructions

1. Read the user's request carefully.
2. Match their intent against the sub-skill descriptions above.
3. Read the matched sub-skill's SKILL.md at the given path and follow its instructions completely.
4. If the intent clearly spans multiple sub-skills, start with the primary match and note the others for follow-up.
5. If no specific sub-skill matches but the request is clearly in this domain, use the default sub-skill.
6. **Default sub-skill:** code-reviewer

## Disambiguation

- "review" without qualification → code-reviewer (most general)
- "review my strings" / "review copy" → string-reviewer
- "I got review feedback" → receiving-review
- "review before merge" / "verify work" → requesting-review
- "check for duplication" / "reinvented wheel" → review-duplication
