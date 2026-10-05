---
name: security-baseline
description: Install secure-development basics for non-toy repos. Use when a repo needs secret scanning, dependency vulnerability checks, auth/session conventions, input validation guidance, safe environment variable handling, .gitignore protection, or a security review checklist.
---

# Security Baseline

## Purpose

Add a pragmatic security floor that agents can follow and validate.

## Inspect First

- env files, `.gitignore`, auth/session code, input boundaries, dependency manifests, CI, deployment docs, and existing security docs

## Procedure

1. Protect secrets.
   - Ensure real `.env` files are ignored.
   - Keep `.env.example` complete and non-secret.
   - Add secret scanning guidance or scripts.

2. Define secure coding conventions.
   - Auth/session helpers.
   - Input validation at boundaries.
   - Error handling that avoids leaking secrets.

3. Add checks.
   - Create target repo `scripts/security-check` where useful.
   - Use `scripts/security_baseline_check.py` for lightweight baseline inspection.
   - Coordinate dependency vulnerability checks with `dependency-governance`.

4. Document review.
   - `docs/security/baseline.md`
   - `docs/security/review-checklist.md`

## Validation

- Run `./scripts/security-check` when present.
- Confirm `.env.example` has no real secrets.
- Confirm `.gitignore` protects local env files.

## Completion Criteria

- Security expectations are documented, checkable, and visible in review.
