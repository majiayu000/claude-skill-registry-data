---
name: release-and-ops
description: 'Plans and executes release and operational readiness tasks, including versioning, changelogs, deployment and rollback.'
metadata:
  id: ce.skill.release-and-ops
  tags: [reliability, contributing, validation]
  inputs:
    files: [CONTRIBUTING.md, ARCHITECTURE.md]
    concepts: [versioning]
    tools: [toolset:exec]
  outputs:
    artifacts: [ce.task.validate]
    files: []
    actions: [run-task]
  dependsOn:
    artifacts: [ce.task.validate]
    files: [.vscode/tasks.json]
  related:
    artifacts: [ce.prompt.prepare-release]
    files: []
---

# Release and Operations Skill

Use this skill to prepare a project for release and to ensure operational readiness.

## Steps

1. **Define release scope.** Review the changes since the last release. Summarise new features,
   bug fixes and breaking changes. Ensure all work is documented in `PRODUCT.md` and
   `ARCHITECTURE.md` where relevant.

2. **Versioning.** Determine the next version number using semantic versioning (MAJOR.MINOR.PATCH).
   Increment MAJOR for breaking changes, MINOR for new backwards‑compatible functionality and
   PATCH for bug fixes.

3. **Update changelog.** Create or update a changelog (e.g. `CHANGELOG.md`) summarising the
   changes, contributors and any migration steps. Use standard formats like Keep a Changelog.

4. **Validate and test.** Run all validation tasks and the full test suite. Perform performance
   and security checks. Ensure that the build artefacts (e.g. packages, Docker images) are
   reproducible and meet quality criteria.

5. **Deployment preparations.** Review deployment scripts or pipelines. Check environment
   variables, secrets and infrastructure configuration. Prepare rollback procedures and
   health checks.

6. **Communication.** Draft release notes for users. Announce any deprecations or important
   notices. Coordinate with operations or DevOps teams to schedule deployment.

7. **Monitor post-release.** After deployment, monitor logs, metrics and user feedback. Be
   prepared to roll back if critical issues arise. Document lessons learned for future
   releases.

This skill ensures that releases are predictable, transparent and operationally sound.
