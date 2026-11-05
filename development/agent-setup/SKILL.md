---
name: agent-setup
description: "Use when inventorying, unifying, installing or synchronizing local Claude Code, Codex, Cursor or Antigravity skills and setup."
capability: "Use when inventorying, unifying, installing or synchronizing local Claude Code, Codex, Cursor or Antigravity skills and setup."
side_effect_level: local_write
approval_required: false
requires_tools: "Project-documented tools; see body."
output_schema: "Evidence, changes and verification report."
risk_class: medium
---

# agent setup

Use the framework's stdlib setup CLI. Read [references/usage.md](references/usage.md) for arguments, native paths, inventory boundaries, backups and conflict handling.
Inventory and plan first. Review destination eligibility and conflicts; preserve project contracts and provider-managed packages. Use Jev only for bounded semantic routing with sanitized evidence; deterministic validation and user authority decide writes.
Apply an exact reviewed plan. Check its receipt, run applicable validation and rerun plan to identify drift. Roll back only exact writes whose current hashes still match. Never replace credentials, permissions, models or .git/config.
Installation is explicit. Do not add startup self-update hooks.


Resolve helper paths from this skill directory. Run project commands from the target workspace.
