---
name: semantic-commits
description: Write semantic commit messages with concise, informative high-level subjects and keep fuller detail in the pull request. Use when preparing commits for project repos so commit history stays readable while PRs carry the broader implementation narrative.
---

# Semantic commits

## Rules
- Use semantic commit prefixes
- Keep commit subjects concise and informative
- Prefer high-level intent over low-level diff narration
- Put fuller reasoning and implementation detail in the PR
- Configure Git author identity per agent in the format `<Name> (<Archetype>) <bot-<archetype-slug>@<operator-email-domain>>`

## Preferred format
`type(scope): summary`

Examples:
- `feat(auth): add password reset flow`
- `fix(api): handle missing session token`
- `docs(spec): clarify onboarding constraints`
- `test(queue): cover race condition on retry`
- `chore(ci): run integration harness in docker`

## Subject guidance
- use imperative mood
- keep it readable in `git log --oneline`
- make the primary change obvious
- avoid vague subjects like `updates` or `work in progress`

## PR relationship
The commit should say what changed at a high level.
The PR should explain the why, assumptions, validation, and reviewer guidance in full.
