---
name: publishing-agent-skills-safely
description: Use when preparing an agent skill for public distribution and a repeatable safety, packaging, and provenance check is needed.
---

# Publishing Agent Skills Safely

Package a public agent skill only after rebuilding its examples with synthetic data and running the local release checks.

## What this skill does

- Validates a candidate skill with a public-safe leakage scanner.
- Demonstrates an expected failure against an intentionally unsafe temporary fixture.
- Creates a deterministic ZIP package from a valid synthetic fixture.
- Produces a machine-readable publication report for review.

## Required inputs

- A public skill directory containing `SKILL.md`, `skill-release.json`, and `.skillignore`.
- Optional external denylist file held outside the public repository.

## Workflow

1. Run `python scripts/check_prereqs.py`.
2. Run `python scripts/run_demo.py --output-dir demo/output` to verify the synthetic reference fixture.
3. Scan the candidate skill and its ZIP with `python tools/leakscan.py <path>` from the repository root.
4. Review every finding. Do not suppress a finding by masking a name; rebuild the sample with generic terminology and synthetic data.
5. Package only after the source tree, ZIP, and generated report are clean.

## Safety rules

- Use reserved domains such as `example.com` and synthetic identifiers such as `DEMO-100`.
- Keep real organization, customer, ticket, schema, URL, email, screenshot, generated artifact, and credential data out of public fixtures.
- Keep any organization-specific denylist outside version control and pass it with `--private-denylist` during release verification.
- Do not place credentials in configuration, examples, shell history, or package artifacts.

## Demo

The demo validates a clean synthetic fixture, creates a temporary unsafe fixture at runtime to prove detection, packages the clean fixture, and writes `publication-report.json`.

## Validation

Run the skill tests from the repository root:

```powershell
python -m unittest discover -s skills/publishing-agent-skills-safely/tests -t skills/publishing-agent-skills-safely -v
```
