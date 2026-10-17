---
name: repo-next-steps-review
description: Reviews a repository's current state and recommends prioritized next steps. Use when the user asks to review a repo, assess project health, identify gaps, suggest next actions, create a practical improvement plan, or decide what to work on next.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: repo-readiness
  task_type: review
  audience: repository-maintainers
  tags:
    - repo-review
    - project-health
    - next-steps
    - planning
  status: draft
  side_effects: none
---

# Repo Next Steps Review

## Purpose

Review a repository's current state and produce a prioritized, evidence-backed set of next steps that help maintainers decide what to improve first.

## When to use this skill

Use this skill when:

- The user asks to review a repository and suggest what to do next.
- The user wants a project health check, gap analysis, or readiness assessment.
- The user asks for a practical improvement plan across docs, tests, CI, code quality, packaging, demos, or maintenance.
- The task is advisory and should not change files unless the user separately asks for implementation.

Do not use this skill when:

- The user asks for a narrow review covered by a more specific skill, such as npm publishing, accessibility, SEO, or bundle size.
- The user already specified a concrete code change to implement.
- The task requires current external data, rankings, pricing, or market research without permission to use web or registry sources.
- The repository cannot be inspected and the user has not provided enough files or context to support evidence-backed findings.

## Inputs to inspect

Inspect the smallest useful set of repository inputs before expanding scope:

- `README.md`, `docs/`, examples, demos, and screenshots
- `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or other project manifests
- Build, test, lint, formatting, and type-check configuration
- `.github/workflows/`, CI configuration, issue templates, and pull request templates
- `src/`, `lib/`, `app/`, `tests/`, `test/`, `spec/`, and `examples/`
- `CHANGELOG.md`, `LICENSE`, release notes, roadmap files, and contribution docs
- Existing command output from tests, linters, type checks, builds, or repository status

## Workflow

1. Identify the repository type, primary audience, likely maturity stage, and stated goals from manifests and docs.
2. Inventory the visible project surface: documentation, setup path, runnable commands, tests, CI, release process, code organization, examples, and maintenance signals.
3. Run only safe local inspection commands when appropriate, such as file listing, manifest parsing, tests, linting, type checks, or builds. Avoid network access and remote side effects unless the user explicitly requests them.
4. Separate observations into strengths, blockers, important improvements, and nice-to-have polish.
5. Tie every finding to concrete evidence: a file, missing file, config field, command result, or observed repository structure.
6. Prioritize next steps by impact, effort, and dependency order. Put foundational fixes before polish.
7. Recommend implementation sequencing: immediate fixes, short-term improvements, and later enhancements.
8. If evidence is incomplete, state the assumption and name the file, command, or context that would reduce uncertainty.
9. Do not edit files unless the user explicitly asks for changes after the review.

## Output format

Return the result using this structure:

```md
## Summary

Briefly describe the repository's current state and the highest-leverage next step.

## Strengths

- Evidence-backed positive observations.

## Findings

| Priority | Area | Finding | Evidence | Recommended next step |
|---|---|---|---|---|
| P0/P1/P2 | docs/tests/ci/code/release/etc. | Specific issue or gap | File, missing artifact, or command result | Actionable recommendation |

## Suggested roadmap

### Now
- Highest-impact tasks to do first.

### Next
- Follow-up improvements after blockers are resolved.

### Later
- Lower-priority polish or strategic options.

## Validation checklist

- [ ] Commands or checks to run after implementing the recommendations.
- [ ] Files or docs to verify.
```

If the repository is very small, combine sections but keep priorities and evidence.

## Quality bar

The task is complete only when:

- The review is specific to the inspected repository, not generic advice.
- Each finding includes evidence from files, missing artifacts, repository structure, or command output.
- Recommendations are prioritized and actionable.
- The roadmap distinguishes immediate work from later improvements.
- The output notes uncertainty instead of overstating unsupported claims.
- No files are modified unless the user explicitly requested implementation.

## Edge cases

- If there is no README or manifest, start with repository structure and recommend a minimal project identity document.
- If the repo contains multiple apps or packages, identify each workspace and call out cross-cutting versus package-specific next steps.
- If tests or builds fail because dependencies are unavailable, report the environment limitation separately from project issues.
- If the repo is already mature, focus on risk reduction, release confidence, contributor experience, and maintenance automation.
- If the user asks for a scored review, provide a lightweight rubric and explain that scores are directional rather than objective.

## Related skills

- `release-readiness-review`
- `github-pages-readiness`
- `npm-publish-readiness`
- `bundle-bloat-review`
