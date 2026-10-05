---
name: dependency-upgrade
description: Use when upgrading, adding, or removing a dependency, package, library, or framework version. Enforces reading release notes before bumping, mapping breaking changes to actual call sites, and proving the upgrade with a green suite — "it compiles" is not "it works".
---

# Dependency Upgrade

Goal: the version number is the last thing that changes — after you know what
changed between the versions and proved your code survives it.

## Steps

1. **State why.**
   Security fix, needed feature, or staying current — say which. One
   dependency (or one coherent group, e.g. a framework and its satellites)
   per task. Bulk-upgrading everything at once is banned: when something
   breaks, you won't know what broke it.

2. **Read before bumping.**
   Fetch the release notes / changelog for EVERY version between current and
   target — GitHub Releases page, CHANGELOG.md in the repo, the package
   registry's release feed, or the project's migration guide. You are
   hunting for: breaking changes, deprecations, changed defaults, behavior
   changes, security notes. No changelog anywhere? Evidence hierarchy
   applies — diff the library's source between the two tags.

3. **Map the impact to YOUR code, as a step list.**
   For each change found in step 2, search the codebase for the affected
   APIs. Turn the result into an explicit, ordered upgrade plan:
   "1) bump X 4.2→5.0  2) rename Foo→Bar at 3 call sites  3) new default
   for `timeout` — pin the old value  4) run full suite". That step list IS
   your Plan message — the user should see exactly what will happen and why.

4. **Classify the risk.**
   - Patch/minor of a leaf dependency → L1.
   - Major version, or a core dependency (framework, ORM, auth/crypto,
     serialization) → **L2 minimum** — plan approval before touching anything.

5. **Upgrade on green ground.**
   Confirm the suite is green BEFORE the upgrade — otherwise you can't tell
   old failures from new ones. Then bump, build, run the full suite. If the
   affected call sites from step 3 have no test coverage, add it first.

6. **Watch for silent changes.**
   New deprecation warnings, changed log output, different defaults — note
   them even if tests pass. "Compiles and suite is green" plus "release
   notes mapped to call sites" together are the proof; neither alone is.

7. **Keep it isolated.**
   Never mix an upgrade with features or refactors. Separate change,
   separate commit — reviewable and revertable on its own.

8. **Record.**
   Journal entry: `docs/agent-journal/YYYY-MM-DD-deps-<slug>.md` — from/to
   versions, breaking changes found and how each was handled, what was run
   to verify.

## Do not

- Do not trust "it compiles" — behavior changes don't break builds.
- Do not skip intermediate versions' changelogs on a multi-version jump.
- Do not suppress or ignore new deprecation warnings silently — list them.
- Do not add a new dependency without stating what it's for and what it
  replaces (writing it yourself, or an existing dependency, were the
  alternatives — say why they lost).
