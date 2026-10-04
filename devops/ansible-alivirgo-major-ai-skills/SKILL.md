---
name: ansible
description: "Write idempotent Ansible playbooks, inventories, and roles; use check mode and ansible-vault for controlled infrastructure automation."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["ansible", "playbooks", "roles", "automation", "vault", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Ansible Configuration Management AI Skill Guide

## Overview & Engine Architecture

Ansible pushes desired configuration to hosts (SSH, WinRM, or APIs) using **playbooks** and **roles**. Tasks should be idempotent: re-running converges without drift. Agents prefer modules over raw `shell`/`command`, name every task, and keep vault passwords out of repositories and chat transcripts.

```
inventory + group_vars/host_vars
        |
        v
playbook.yml  ->  roles/ tasks handlers templates
        |
        v
managed nodes (SSH) / cloud APIs
```

## When to use this skill

- Bootstrapping packages, users, and services on VMs
- Writing reusable roles for app deploy glue
- Encrypting secrets with ansible-vault
- Dry-running changes with check mode

## Operational directives

1. Prefer modules (`apt`, `yum`, `copy`, `template`, `service`, `user`) over shell.
2. Use `handlers` for restarts; notify only on change.
3. Run `--check` (and `--diff` for templates) before production.
4. Store secrets in vaulted files; never commit plaintext vault passwords.
5. Keep inventories environment-split (`inventories/prod`, `inventories/dev`).

## Playbook sketch

```yaml
- name: Configure web hosts
  hosts: web
  become: true
  roles:
    - role: common
    - role: nginx
      vars:
        nginx_worker_processes: auto
```

Role task example:

```yaml
- name: Ensure nginx is installed
  ansible.builtin.package:
    name: nginx
    state: present

- name: Deploy nginx site config
  ansible.builtin.template:
    src: site.conf.j2
    dest: /etc/nginx/sites-available/app.conf
    mode: "0644"
  notify: Reload nginx

- name: Enable site
  ansible.builtin.file:
    src: /etc/nginx/sites-available/app.conf
    dest: /etc/nginx/sites-enabled/app.conf
    state: link
  notify: Reload nginx
```

## Commands

```bash
ansible-playbook -i inventories/prod site.yml --check --diff
ansible-galaxy init roles/nginx
ansible-vault encrypt group_vars/prod/vault.yml
ansible-vault edit group_vars/prod/vault.yml
ansible-playbook -i inventories/prod site.yml --ask-vault-pass
```

## Failure patterns

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Unreachable | SSH key/bastion | `-vvv`, ProxyJump |
| Changed every run | Non-idempotent shell | Switch to module |
| Template wrong | Variable undefined | `ansible-inventory --list`, defaults |
| Vault decrypt fail | Wrong password/file | Confirm vault id |

## Best practices

- Pin collections in `requirements.yml`.
- Use `serial` / `max_fail_percentage` for rolling host updates.
- Tag tasks (`--tags`) for partial runs during incidents.
- Document required privilege (become) per play.

## Limitations

- Network devices and Windows need specialized collections and remoting setup.
- Extremely large fleets may need AWX/Tower or Execution Environments.
- Check mode cannot always simulate every module accurately.

## Related skills

- `@terraform` - provision machines Ansible configures
- `@docker` - when configuration moves into images
- `@packer` - golden images with Ansible provisioners
