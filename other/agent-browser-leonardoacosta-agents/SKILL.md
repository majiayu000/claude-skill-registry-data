---
name: agent-browser
description: Use agent-browser for direct CLI browser automation, inspection, web-app testing, screenshots, sessions, and approved profile or CDP control. Trigger when a task names agent-browser or requires its CLI/session controls.
compatibility: Requires the installed agent-browser CLI. Read its version-matched bundled skill before issuing commands.
---

# agent-browser

The installed CLI is authoritative. Before browser work, run:

```bash
command -v agent-browser
agent-browser --version
agent-browser --help
agent-browser skills get core
```

If the CLI or requested skill is missing or unsupported, stop and report it. Do
not substitute stale instructions or invent flags. Load complete references only
when needed with `agent-browser skills get core --full` and
`agent-browser skills path core`.

Load a specialized installed skill when required, such as `electron` or
`dogfood`; fail closed if it is unavailable.

An explicit agent-browser request authorizes its managed Chromium runtime. Ask
for approval only for an explicit external executable, private profile, or CDP
endpoint. Use a task-unique session prefix, one stable named session per task,
and only owned-resource cleanup. With shared CDP, pin the session to its tab
using the upstream `--pin-tab` behavior.

Load `agent-browser-policy` with this skill. It supplements upstream core with
consent, privacy, profile, harness-versus-CLI, CDP, and cleanup rules.
