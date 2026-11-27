---
name: deploy-node
description: Deploy or converge a HomeLab node safely from inventory using Ansible and validate the live result.
---
# Deploy/converge node
Resolve the node and its groups from inventory; discover current runtime roles (PostgreSQL primary, Redis master) rather than trusting names; confirm dependencies and run order (ansible/README.md, site.yml). Run syntax-check, then the smallest playbook that covers the change, with --check/--diff first where the role supports it. Read the role's own assertions; then verify the live state independently: systemd/Docker health, listening addresses (never 0.0.0.0), overlay guard, replication/quorum for stateful roles. For disruptive steps (data-node restarts, failover) stop and get the owner's go-ahead. Report evidence, residual risk and rollback.
