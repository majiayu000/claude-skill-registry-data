---
name: github-issues-prs
description: >
  Draft reproducible GitHub issues, structured pull request descriptions,
  technical responses to code reviews, and cross-referenced issue discussions.
  Use when opening new issues with reproduction steps, composing PR descriptions
  linked to issues, summarizing changes for reviewers, or responding constructively
  to review feedback.
compatibility: >
  Agent Skills-compatible coding agents interacting with GitHub repository
  collaboration workflows.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "github, pull-requests, issues, bug-reports, code-review, collaboration"
  topics: "version-control, devtools"
---

# GitHub Issues and Pull Requests

Clear, structured communication on GitHub accelerates code review, prevents regressions, and creates a durable technical record. High-quality issues provide minimal reproducible examples; high-quality pull requests clearly articulate **why** a change was made, **how** it was implemented, and **how** it was validated.

## Core Rules

1. **Bug reports require minimal reproduction steps**: Never file a bug report with just "it crashed". Provide exact input, actual output, expected output, and environment details.
2. **Pull requests must link related issues**: Use standard GitHub closing keywords (`Fixes #123`, `Closes #456`) so issues close automatically on merge.
3. **Include before/after context and verification**: PR descriptions must detail how the changes were verified and what tests were added.
4. **Keep PRs focused and reviewable**: Avoid massive multi-concern PRs. Separate refactorings from new features.
5. **Treat GitHub integrations as read-only by default**: Agents should draft issue and PR descriptions for user review. Never submit or push without authorization.

---

## 1. Canonical Bug Report Template

```markdown
### Summary
When parsing a YAML frontmatter containing an unquoted date value (e.g. `updated: 2026-10-15`), `load_skill_dir()` raises an unhandled `AttributeError` instead of normalizing the string.

### Reproduction Steps
1. Create a `SKILL.md` with the following frontmatter:
   ```yaml
   ---
   name: sample-skill
   description: Sample description
   metadata:
     updated: 2026-10-15
   ---
   ```
2. Run `owl validate ./sample-skill`.

### Expected Behavior
The validator normalizes the date object into an ISO 8601 string and completes validation successfully.

### Actual Output
```text
AttributeError: 'datetime.date' object has no attribute 'strip'
Traceback (most recent call last):
  File "owl/parsing.py", line 102, in load_skill_dir
    ...
```

### Environment
- OWL Version: `0.4.1`
- Python Version: `3.11.8`
- OS: macOS 14.5 (Sonoma)
```

---

## 2. Canonical Pull Request (PR) Template

```markdown
## Description
Resolves an unhandled `AttributeError` when frontmatter fields contain parsed YAML dates or numeric types instead of strings. Normalizes date and numeric metadata fields to strings during dictionary loading in `parsing.py`.

Fixes #142

## Type of Change
- [x] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Key Changes
- `src/owl/parsing.py`: Added type-coercion helper `_coerce_string()` to ensure YAML-parsed scalar types (dates, ints) are safely converted to string before string stripping.
- `tests/test_parsing.py`: Added regression test `test_load_skill_with_date_metadata()` verifying unquoted date handling.

## How Has This Been Tested?
- [x] Unit test suite: `pytest tests/test_parsing.py -k date` passes.
- [x] Full regression test: `pytest` passes with 100% green.
- [x] Linting & Typing: `ruff check .` and `mypy src/` report 0 errors.

## Checklist
- [x] My code follows the code style of this project.
- [x] I have updated the `CHANGELOG.md` under `[Unreleased]`.
- [x] I have added unit tests covering my changes.
```

---

## 3. Responding to Review Comments

When addressing reviewer feedback:
- Acknowledge the feedback constructively.
- Reference the specific commit that resolved the comment.
- If proposing an alternative design, explain the trade-offs clearly.

Example:
> *"Great catch on the potential memory leak when parsing large streams. In commit `7f2a1b`, I refactored `read_all()` to stream chunks with an explicit 64KB buffer. Let me know if that aligns with your expectation!"*

---

## 4. Verification Checklist

- [ ] Issue title summarizes the observable symptom concisely.
- [ ] Bug report includes complete stack trace and environment specifications.
- [ ] PR description links the target issue (`Fixes #...`).
- [ ] Before and after behavior is documented.
- [ ] Review responses are professional, specific, and cite exact commit hashes.
