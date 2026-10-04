---
name: mvp-agent
description: New agent in a fleet from zero to operational
argument-hint: <agent-name> [fleet-path]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: max
---

# MVP — Agent

Chain: scaffold-subagent → foundation-config → feature-implement (agent logic) → feature-test → ops-deploy

Produces a new agent inside a fleet project, configured, tested, and ready to operate.