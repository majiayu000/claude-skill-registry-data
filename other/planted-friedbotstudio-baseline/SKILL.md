---
name: planted
owner: baseline
description: Fixture SKILL.md that intentionally invokes a .claude/-prefixed helper that is NOT in the shipped manifest. Used by tests/shipped-skill-md-shippability.test.mjs to verify scan-shipped-skills.mjs emits a BLOCKER UNSHIPPED_MODULE_IMPORT finding.
---

# planted — fixture skill (DO NOT USE IN PRODUCTION)

This fixture exercises C3: a `.claude/`-prefixed runtime invocation that the manifest does not list.

## Procedure

1. Run the helper:

   ```bash
   node .claude/skills/notinmanifest/helper.mjs run
   ```
