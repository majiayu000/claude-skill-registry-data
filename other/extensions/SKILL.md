---
name: neatcontext-extensions
description: Report which extensions the connected NeatContext context expects, and whether this machine provides them. Use when the user asks what a context can reach, why an extension tool is missing, or how to connect one here.
---

# Context extensions

The bundled CLI path and Kimi session id below are expanded by Kimi Code at skill activation. Run:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" extensions
```

Relay the report. Two separate things are being reported, and the difference matters:

- What the **context** expects — the extension it declares and the capability that provides. This travels with the context and is the same on every machine it reaches.
- What **this machine** provides for it. That is local, hand-written, and lives in the bindings file the report names. Nothing configures it automatically, and nothing inside a shared context can configure it.

If something is reported as not configured, show the example binding from the report and say where the file goes. Tell the user to keep credentials in the environment and name them under `envFrom` rather than writing them into the file.

If an extension is reported as unavailable or failed, relay the reason exactly as given — a command that is not there, a server that did not answer — and do not guess at a fix beyond what the report says.

Say plainly that the context still works: its profile and knowledge folder are served whether or not any extension is configured.

To record that this context expects something new:

```text
KIMI_PLUGIN_ROOT="${KIMI_SKILL_DIR}/../.." kimi __plugin_run_node "${KIMI_SKILL_DIR}/../../src/kimi/neatcontext-cli.mjs" -- --session-id "${KIMI_SESSION_ID}" extensions add <id> --capability "<what it lets this context do>"
```

Add `--tools a,b` to narrow it to specific tools, and `--important` when the context leans on it. That records what the context wants; it connects nothing on its own. `extensions remove <id>` drops the declaration and leaves any local binding alone, and `extensions test <id>` starts one on purpose and names the tools it really offers.
