---
description: "Check licenses of all dependencies and detect prohibited licenses"
user-invokable: true
---

# /license-check

A skill for checking the licenses of all project dependency libraries.

## License Policy

### Allowed

MIT, BSD-2-Clause, BSD-3-Clause, Apache-2.0, ISC, MPL-2.0

### Prohibited

GPL-2.0, GPL-3.0, LGPL-2.1, LGPL-3.0, AGPL-3.0 and other GPL variants

## Steps

1. List all dependencies with `go list -m -json all`
2. Check the LICENSE file of each dependency's repository/package
3. Compare licenses against the policy
4. Display results in a table:
   - Dependency | Version | License | Status (OK / PROHIBITED / UNKNOWN)
5. Warn if any prohibited or unknown licenses are found

## Notes

- For UNKNOWN licenses, recommend manual verification
- Include transitive dependencies (indirect) in the scope
