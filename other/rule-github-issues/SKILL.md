---
name: rule-github-issues
description: MANDATORY when editing files matching [".github/ISSUE_TEMPLATE/**/*", ".github/PULL_REQUEST_TEMPLATE*", ".github/workflows/**/*.yml", "documentation/**/*.md"]. GitHub issue, PR, and workflow template conventions
---

# GitHub Issues & PR Rules

## Issue Templates

ALWAYS store issue templates in `.github/ISSUE_TEMPLATE/` as YAML forms (`.yml`) with `name`, `description`, `labels`, and structured `body` fields. ALWAYS include required fields for reproduction steps, expected vs actual behavior, and environment. NEVER ship a freeform Markdown template for bug reports.

Correct:
```yaml
name: Bug report
description: Report a defect in simpler-grants-gov
labels: ["bug", "triage"]
body:
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
    validations:
      required: true
```

## Pull Request Template

ALWAYS include in `.github/PULL_REQUEST_TEMPLATE.md`: summary, linked issue (`Closes #...`), testing notes, screenshots for UI changes, accessibility checklist, and a data/privacy impact note. NEVER merge a PR without a linked issue or ADR reference for non-trivial changes.

## Labels and Triage

ALWAYS use the project's canonical label set (`bug`, `enhancement`, `docs`, `a11y`, `security`, `privacy`, `fedramp`, `good first issue`). NEVER invent new labels without updating the label reference.

## Commit and PR Titles

ALWAYS use conventional-commit-style prefixes (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`). Title MUST be imperative and under ~72 characters.

## Security-Sensitive Issues

NEVER file a public issue for a suspected vulnerability — use the private security advisory process documented in `SECURITY.md`. Triage labels MUST NOT leak exploit details.

## Open Source & CC0

ALWAYS verify that all contributed content is compatible with the project's CC0 / public-domain posture. NEVER import code from incompatible licenses via an issue/PR without a license review.

## Automation Workflows

Workflow files in `.github/workflows/` that manage issues/PRs (stale bots, triage, label sync) MUST pin action versions by SHA, run with least-privilege `permissions:`, and fail closed on errors.

---

## Related Rules

- **`ci-cd.mdc`** — build and test workflows
- **`security.mdc`** — security-advisory process
- **`data-privacy.mdc`** — privacy impact assessment in PRs
- **`fedramp.mdc`** — change-management expectations
- **`accessibility.mdc`** — a11y checklist in PR template

## Specialist Validation

**Simple (label tweak, copy edit):** None.
**Moderate (new template, new workflow):** Invoke `codebase-conventions-reviewer`.
**Complex (triage automation, permissions changes):** Invoke `security-sentinel` and `architecture-strategist`.
