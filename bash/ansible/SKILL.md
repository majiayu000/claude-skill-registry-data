---
name: ansible
description: Run Ansible ad-hoc commands and playbook operations
activation_keywords: [ansible, playbook, automation, config, inventory]
execution_mode: client
---

# Ansible Skill

Provides Ansible automation operations via local CLI:
- Run ad-hoc commands (ping, command, shell, setup, etc.)
- Check playbook syntax and dry-run
- List inventory hosts and groups
- Run playbooks

Use `builtin_ansible` tool with fields:
- `operation`: one of "ad_hoc", "playbook_check", "playbook_run", "inventory", "list_hosts"
- `module`: Ansible module name (required for ad_hoc, e.g. "ping", "command", "shell", "setup")
- `args`: module arguments (for ad_hoc)
- `playbook`: path to playbook file (required for playbook operations)
- `inventory`: path to inventory file (default: /etc/ansible/hosts or ./inventory)
- `hosts`: target hosts pattern (default: "all")
- `extra_args`: additional ansible-playbook arguments

Note: Requires Ansible CLI (ansible, ansible-playbook) installed.
Write operations (playbook_run) require user confirmation.
