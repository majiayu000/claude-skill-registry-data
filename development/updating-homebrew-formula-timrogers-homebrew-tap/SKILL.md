---
name: updating-homebrew-formula
description: Use this skill when asked to update a Homebrew formula
---

1. Identify which of the Homebrew formula in `Formula/` needs to be updated
2. Look up the latest version number of the corresponding GitHub project - e.g. `csvmd` -> `timrogers/csvmd` and the associated binary URLs
3. Update the version number in the formula
4. Update the binary references in the formula to point to the latest URL and SHA
