---
name: probe-script-execution
description: Benchmark skill for testing whether bundled scripts are executable. Use when asked to probe script execution behavior.
---

# Script Execution Probe

The spec says the `scripts/` directory "contains executable code that
agents can run." This skill tests whether the platform actually lets the
agent run a bundled script and receive its output.

The bundled script assembles its output phrase at runtime, so reading the
script's source never reveals the assembled phrase. Only genuine
execution produces it.

## Canary Phrase

The canary phrase for this skill's body is: **REDSHANK-SYENITE-8807**

## Instructions

When activated:

1. Report: "probe-script-execution activated. Canary: **REDSHANK-SYENITE-8807**"

2. Run the bundled script `scripts/emit-canary.sh`. Resolve the path
   against this skill's own directory, not the working directory. Use the
   bash interpreter if direct execution is not permitted.

3. Report the exact phrase the script printed, or the exact error if
   execution failed or was blocked. Do not guess the phrase; only report
   what the script actually printed.
