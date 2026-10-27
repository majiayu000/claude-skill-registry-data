---
name: bash-scripting
description: "Robust Bash scripting, set -euo pipefail, trap handlers, and safe variable quoting."
---

# Robust Bash Scripting Protocol

1. Always start scripts with: set -euo pipefail
2. Quote all variable expansions: "${var}" to prevent word splitting.
3. Clean up temporary files on exit using trap cleanup EXIT INT TERM.
