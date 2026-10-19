---
name: dependency-upgrade
description: Use when upgrading packages, libraries, a framework or a language runtime (React, Next.js, Angular, Spring Boot, Django, Node, Python, Java), fixing outdated or vulnerable dependencies, handling breaking changes after a major version bump, or cleaning up npm audit / Dependabot alerts.
---

# Dependency Upgrade

## Overview

Upgrade in small, verified steps. Read what changed before changing code, keep the app working after each step, and never mix an upgrade with unrelated changes.

## Method

1. **Inventory.** List outdated and vulnerable packages: `npm outdated` / `npm audit`, `pip list --outdated` / `pip-audit`, `mvn versions:display-dependency-updates`, `go list -u -m all`. Note current and target versions.
2. **Plan the order:**
   - Patch and minor updates first, in one batch.
   - Then each major upgrade on its own, starting with the runtime and framework, then libraries that depend on them.
   - Security fixes before feature upgrades.
3. **Read before changing.** For each major upgrade: official migration guide, changelog "Breaking changes" section, deprecation notices from the current version. Check peer dependency requirements.
4. **Run official codemods** when available (for example `npx @next/codemod`, `npx react-codemod`, Angular `ng update`, OpenRewrite for Spring).
5. **Upgrade, fix, verify:** update the version and lockfile, fix compile and type errors, run lint, tests and build, start the app and check the main flows.
6. **Commit per step** with the versions in the message.

## Output

Before changing code:

```
| Package | Current | Target | Type | Breaking changes affecting this project | Effort |
```

After:

```
Upgraded: <list>
Code changes: <what was changed and why>
Verified: <lint, tests, build, manual checks>
Not upgraded: <package — reason, e.g. blocked by peer dependency>
```

## Rules

| Rule | Why |
|---|---|
| Lockfile updated and committed | Reproducible installs |
| One major upgrade per commit or PR | Easy review and revert |
| Search the codebase for every API listed as removed or changed | Breaking changes hide in rarely used code |
| Remove `--force` / `--legacy-peer-deps` workarounds once the tree is consistent | They hide real conflicts |
| Check transitive vulnerabilities with `npm audit` / `pip-audit` after upgrading | A direct upgrade may not fix them |

## Common mistakes

- Upgrading everything at once, then not knowing which package broke the build.
- Changing versions without reading the migration guide.
- Silencing deprecation warnings instead of fixing them.
- Declaring success because it compiles; run the tests and the app.
- Using `npm audit fix --force`, which can jump major versions without notice.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
