---
name: rseng-maintenance-sustainability
description: >-
  Covers keeping research software alive and responsible over time: ongoing
  maintenance practice, tracking and paying down technical debt, reducing the
  bus factor, and deprecating or archiving honestly. Use when the user asks
  how to maintain or sustain a project, stop it rotting, schedule CI to catch
  breakage from external change, track or pay down tech debt, plan maintenance
  funding or shared ownership, or retire or deprecate software. (Energy and
  carbon footprint of computing is rseng-green-computing; dependency updating
  and auditing detail is rseng-dependency-management; archiving mechanics are
  rseng-archiving.)
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Maintaining and sustaining research software

Use this skill when the goal is to keep software usable over time rather
than to ship a first version: setting up maintenance habits, managing
dependencies and technical debt, deciding whether to keep, deprecate, or
archive a project, and keeping its sustainability story honest.
Unmaintained software degrades even with no code changes - dependencies
age, environments shift, and the knowledge to run it erodes - so treat
maintenance as a recurring cost, not a one-off.

## Establish maintenance habits early

Calibrate effort to the user base, but build the habits before the
software is widely used:

- Write a test suite and check coverage with a language-appropriate tool
  (pytest-cov for Python, covr for R). Without tests, every dependency or
  environment update carries unknown regression risk.
- Set up a CI pipeline that runs tests on every commit and on a schedule
  (e.g. weekly). Scheduled runs catch breakage from external changes even
  when nobody is actively developing. See the rseng-ci-cd and
  rseng-testing skills for the mechanics.
- Keep documentation current as part of maintenance, not after it. If you
  cannot install and run the software from scratch using only its README
  and install guide, the docs need updating. See rseng-documentation.
- Maintain a visible issue tracker (GitHub/GitLab Issues) so the
  maintenance backlog is shared, not held in one person's head.

## Manage dependencies deliberately

Every dependency is a liability as well as an asset - it can change,
deprecate, or introduce a security issue:

- Prefer a small, well-understood dependency tree drawn from already
  well-maintained projects over a large one.
- Pin exact versions with a management tool for the language (pip + venv,
  pip-tools, uv, or Poetry for Python; renv for R) so updates are
  deliberate and auditable. See the rseng-reproducible-environments skill.
- Automate update pull requests with Dependabot or Renovate so security
  and version bumps surface as reviewable changes rather than silent drift.

## Communicate change clearly

- Use Semantic Versioning (MAJOR.MINOR.PATCH) so users can tell a breaking
  change from a feature from a bug fix and decide when to upgrade. See the rseng-publishing-releasing skill.
- Keep a CHANGELOG and update it with each release: a record of what
  changed, when, and why serves both users and your future self.

## Reduce the bus factor

If only one person understands the software, it becomes unmaintainable the
moment they are unavailable:

- Document key decisions, architecture, and operational knowledge in the
  repository itself, not just in someone's head.
- Share ownership with at least one other person who can act if the primary
  maintainer is away.
- Use regular code review to spread understanding of the codebase (see the
  rseng-version-control-review skill).
- Recruit community help: label low-barrier issues (`good first issue`),
  run maintenance sprints, and make contributing easy.
- Apply for maintenance-specific funding where it exists (funders
  increasingly recognise maintenance as a distinct cost).

## Deprecate or archive honestly

When you can no longer sustain a project, say so. A prominent README
notice, a repository archive, or an explicit deprecation statement is more
helpful to users than silent abandonment.
See the rseng-publishing-releasing skill for archiving mechanics.

## Track and pay down technical debt

Technical debt is often unavoidable in research code written quickly to
test a hypothesis; the danger is that it compounds until change becomes
slow and risky:

- Distinguish intentional debt (a known, documented workaround) from
  unintentional debt (unclear code, missing tests, hardcoded values). The
  latter is more dangerous because it is harder to reason about.
- Record debt where it is visible: create issues or a `tech-debt` label,
  and add `TODO`/`FIXME` comments at the point of the problem with enough
  context for a future reader. Debt held only in memory is forgotten.
- Allocate protected time for maintenance and refactoring - a maintenance
  sprint, a fixed fraction of each cycle, or scheduled calendar time. Debt
  does not reduce itself.
- Refactor incrementally, not with a big rewrite: small, individually
  reviewable improvements (rename for clarity, extract a function, add a
  missing test). Ensure tests cover current behaviour before restructuring,
  or you cannot tell whether a refactor introduced a regression.
- Use static analysis (Ruff or lintr, SonarQube) to surface quality issues
  automatically and track metrics over time. See the rseng-code-quality
  skill for readability and structure guidance.

## Reduce environmental impact

Environmental sustainability of computing is its own practice with
its own skill: rseng-green-computing covers measuring energy and carbon
(CodeCarbon, the SCI metric), reducing footprint in payoff order and
carbon-aware scheduling. From the maintenance perspective, two habits
matter here: include the compute footprint in the project's
sustainability story (long-running services and repeated pipelines
dominate), and revisit it at the same cadence as dependency and debt
reviews - then follow rseng-green-computing for the how.

## Working with this skill

The generated references.md beside this file lists the source
material and pointers:

- references.md - verified Learn more pointers


Learn more (verified):
  - https://opensource.guide/best-practices/ - best practices for
    open source maintainers
  - https://www.software.ac.uk - Software Sustainability Institute
  - https://chaoss.community/kb-metrics-and-metrics-models/ - CHAOSS
    community health metrics
  - https://endoflife.date - end-of-life dates for dependencies


<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-archiving - retiring software needs archival deposit
- rseng-ci-cd - scheduled runs catch external breakage
- rseng-code-quality - incremental refactoring and static analysis
- rseng-contributor-onboarding - recruiting community maintenance help
- rseng-dependency-management - dependency update and audit mechanics
- rseng-green-computing - footprint review at maintenance cadence

<!-- related-skills:end -->
