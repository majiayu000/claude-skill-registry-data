---
name: verify-clarila
description: "Run this repository's source-bound CLI verification journeys for skill discovery, immutable official guidance and Obsidian maintenance. Use for this Clarila source checkout; this does not establish live provider or product acceptance."
---

# Verify the Clarila tools in this checkout

Read repository instructions and [the feature map](features/README.md). Use the existing Bun executable and Go toolchain; do not install or change dependencies. Inspect `.clarila/verify.json`, then run the bundled `clarila-verify/scripts/project-verify.sh` with `doctor` or `run`, the exact repository root, that config and an evidence directory outside this checkout. Select the relevant mapped features. Keep commands, real results, source and plan hashes from the generated report. A changed source snapshot requires a fresh run for affected journeys.

This adapter launches real CLI invocations and uses disposable temporary repositories/vaults where stated. Its tests assert discovery, filesystem and receipt effects. Browser/native device, authenticated Discord/GitHub/EAS behavior, independent assessment, publication and deployment need their own applicable evidence. An unavailable prerequisite stays explicit.

Evidence survives process cleanup in the external run directory. Never delete unrelated processes or private state. Report the selected feature scope and concrete remaining gaps.
