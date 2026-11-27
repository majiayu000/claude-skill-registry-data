---
name: plan-change
description: Plan a HomeLab infrastructure change before implementation, especially multi-node, networking, security, database, CI/CD, or disruptive work.
---
# Plan infrastructure change
1. Read docs/PROJECT-CONTEXT.md, the relevant roles, inventory and runbooks — and check the live state.
2. State the outcome and the affected nodes, services and files.
3. Map dependencies and traffic/data flows (overlay vs LAN vs public).
4. Identify stateful data and the backup that must exist first.
5. Identify exposure changes and how they will be tested along the attacker's path.
6. Check the RAM/disk budget against the hardware.
7. Define failure behaviour and the rollback path.
8. Assign the work: installer, Ansible role/playbook, scripts, docs.
9. Define validation, including a reboot where persistence matters.
10. Produce ordered steps with hold points for destructive or disruptive actions that need the owner's go-ahead.
