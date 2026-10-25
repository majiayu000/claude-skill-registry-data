---
name: dependency-upgrade
description: Plan and execute a dependency or framework upgrade with migration notes, isolated changes, full verification and a rollback path.
---

# Dependency upgrade: move versions without breaking the runtime

- Read the release notes and migration guide before changing the lockfile. Identify breaking changes, dropped runtime support and security fixes.
- Upgrade one dependency family at a time. Keep application changes and lockfile churn in separate commits when possible.
- Use the project's package manager and lockfile exactly; do not mix managers or hand-edit generated files.
- Run the full test and build matrix, including type checks and the oldest supported runtime. Fix deprecations rather than suppressing them.
- Check transitive changes and peer constraints. A green install is not proof that the runtime path still works.
- For a security upgrade, identify the vulnerable range, the fixed version and whether the vulnerable path is actually reachable.
- Record the version delta, migration steps, test evidence and rollback plan.

---

_NullByte skill pack. Original guidance for this tool; no third-party skill text is bundled._
