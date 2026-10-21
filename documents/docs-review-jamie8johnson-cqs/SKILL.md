---
name: docs-review
description: Review project docs for staleness. Checks lib.rs, Cargo.toml, README, CONTRIBUTING, SECURITY, PRIVACY, and GitHub repo metadata.
disable-model-invocation: false
---

# Docs Review

Check all project documentation for staleness and fix what's drifted.

## Process

1. **Scope the review**:
   - Run `git log vLAST_TAG..HEAD --stat` to see what changed since last release
   - Focus on docs affected by those changes
   - If no tag exists, review everything

2. **Check each item**:

   | File | What to check |
   |------|---------------|
   | `src/lib.rs` doc comment | Language count, feature list, API examples compile, Quick Start accuracy |
   | `Cargo.toml` | `description` (crates.io one-liner), `keywords`, `categories` |
   | `README.md` | Hardcoded versions (schema, install), feature list, usage examples, badge URLs |
   | `CONTRIBUTING.md` | Architecture Overview matches current file layout — any files added/moved/renamed? |
   | `SECURITY.md` | Threat model current, dependency notes, any new attack surfaces? |
   | `PRIVACY.md` | Data handling claims still accurate? |
   | `CLAUDE.md` | Skills list matches `.claude/skills/`; Project Conventions accurate (MSRV, feature names); WSL/CI guidance not contradicting current practice |
   | GitHub repo | Description and topics — `gh repo view`, update with `gh repo edit` if needed |

3. **Fix and report**:
   - Fix stale docs directly
   - Report what was updated and what was already current
   - If unsure about a claim, flag it rather than guessing

## When to run

- Before releases (`/release` references this)
- After significant feature PRs
- Before audits
- When you suspect drift

## Rules

- Don't rewrite docs for style — only fix factual staleness
- Don't add content — only correct what exists
- Check numbers against code: grep for hardcoded counts (languages, tests, dimensions) and verify
- If CONTRIBUTING.md Architecture Overview lists files, glob to confirm they exist
