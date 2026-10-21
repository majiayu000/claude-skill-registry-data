---
name: planted
owner: baseline
description: Fixture SKILL.md that intentionally contains a dev-tree runtime reference inside a bash fence. Used by tests/shipped-skill-md-shippability.test.mjs to verify scan-shipped-skills.mjs emits a BLOCKER DEV_TREE_RUNTIME_REF finding.
---

# planted — fixture skill (DO NOT USE IN PRODUCTION)

This fixture exists solely to exercise scan-shipped-skills.mjs's C1 check. It pretends to be a baseline skill whose procedure invokes a dev-only path.

## Procedure

1. The skill nominally does something. To trigger the marker writer it runs:

   ```bash
   node -e "import('./src/foo.js').then(m => m.run())"
   ```

   This invocation references `src/foo.js`, which would not exist in a consumer install.
