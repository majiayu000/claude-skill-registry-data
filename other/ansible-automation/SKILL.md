---
name: ansible-automation
description: >
  Design, author, harden, and validate Ansible playbooks, roles, and automation workflows.
  Use when writing Ansible tasks, structuring reusable roles, enforcing task idempotency,
  managing inventory and variables, encrypting secrets with Ansible Vault, implementing
  resilient block/rescue error handling, or complying with ansible-lint standards.
compatibility: >
  Agent Skills-compatible coding agents with access to ansible, ansible-playbook, or ansible-lint tooling. Tooling is required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "ansible, automation, playbooks, roles, idempotency, vault, ansible-lint, devops"
  topics: "devops"
---

# Ansible Automation and Role Engineering

Ansible delivers agentless, declarative configuration management and orchestration over SSH or WinRM. Production-grade Ansible automation demands strict task idempotency, structured role architecture, deterministic variable scoping, robust error handling with block/rescue constructs, and secret encryption via Ansible Vault.

## Purpose & Overview

This skill establishes engineering standards for authoring reliable, reproducible Ansible playbooks and roles. Adhering to these standards ensures:
- Playbooks produce idempotent results: re-running a playbook against an unchanged system results in zero changed tasks (`changed=0`).
- Operational tasks isolate secrets and sensitive values using Ansible Vault.
- Roles follow standard directory anatomy and variable precedence rules.
- Workflows adhere to `ansible-lint` production rules without warnings or syntax errors.

---

## Core Principles & Rules

1. **Strict Idempotency Across All Tasks**:
   - Always prefer built-in declarative modules (`ansible.builtin.template`, `ansible.builtin.package`, `ansible.builtin.copy`) over generic `ansible.builtin.command` or `ansible.builtin.shell`.
   - When `command` or `shell` is unavoidable, you must define `changed_when` and either `creates` or `removes` to prevent false "changed" states on successive runs.

2. **Trigger Side-Effects Exclusively via Handlers**:
   - Never restart services directly in sequential tasks. Emit notifications via `notify: Restart <service>`.
   - Handlers execute once at the end of the play (or when explicitly flushed with `ansible.builtin.meta: flush_handlers`), preventing redundant restarts during multi-step configuration changes.

3. **Standardize Role Directory Anatomy**:
   - Structure roles strictly: `defaults/main.yml` (overridable defaults), `vars/main.yml` (constant role variables), `tasks/main.yml` (task execution), `handlers/main.yml` (notified handlers), `templates/` (Jinja2 files), `meta/main.yml` (dependencies and metadata).

4. **Never Store Plaintext Secrets**:
   - Encrypt passwords, API keys, and certificates with `ansible-vault` (either full files or via `!vault |` inline encrypted strings).
   - Set `no_log: true` on tasks that process sensitive parameters to prevent secret leakage in CI logs and standard output.

5. **Defensive Error Handling with `block` / `rescue` / `always`**:
   - Avoid blanket `ignore_errors: true`. It masks fatal defects and creates indeterminate host states.
   - Use `block` to group transactional operations, `rescue` to execute remediation or rollback tasks, and `always` to clean up temporary artifacts.

6. **Tag Every Task for Granular Execution**:
   - Apply contextual tags (`tags: [install, config, service, security]`) so operators can execute targeted phases (e.g. `ansible-playbook -t config site.yml`) without executing the entire stack.

---

## Standard Workflows & Procedures

### Workflow: Production Role Engineering

1. **Scaffold Role Structure**:
   ```bash
   ansible-galaxy role init roles/app_service
   ```
2. **Define Defaults and Types**:
   - Place baseline configurable variables in `defaults/main.yml`.
   - Use explicit typing and sensible defaults (e.g., `app_service_port: 8080`, `app_service_enabled: true`).
3. **Implement Declarative Tasks**:
   - Use fully-qualified collection names (FQCN) such as `ansible.builtin.systemd` or `ansible.posix.firewalld`.
   - Keep tasks focused on single discrete state declarations.
4. **Wire Handlers**:
   - Place service restarts and reload actions in `handlers/main.yml`.
5. **Static Linting & Syntax Verification**:
   - Validate syntax: `ansible-playbook --syntax-check site.yml`.
   - Lint with ruleset: `ansible-lint roles/app_service`.
6. **Execution Dry Run**:
   - Test changes with `--check` and `--diff` flags before committing:
     ```bash
     ansible-playbook -i inventory/staging site.yml --check --diff
     ```

---

## Real-World Examples & Patterns

### 1. Production Role Task Definition (`roles/nginx_proxy/tasks/main.yml`)

```yaml
---
- name: Install Nginx package
  ansible.builtin.package:
    name: "{{ nginx_package_name }}"
    state: present
  tags:
    - install
    - packages

- name: Deploy hardened Nginx configuration
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: "0644"
    validate: /usr/sbin/nginx -t -c %s
  notify:
    - Reload nginx
  tags:
    - config

- name: Configure TLS private key from Ansible Vault
  ansible.builtin.copy:
    content: "{{ nginx_tls_private_key }}"
    dest: /etc/ssl/private/app.key
    owner: root
    group: root
    mode: "0600"
    no_log: true
  notify:
    - Reload nginx
  tags:
    - config
    - security

- name: Ensure Nginx service is enabled and started
  ansible.builtin.systemd:
    name: nginx
    state: started
    enabled: true
  tags:
    - service
```

### 2. Handlers Definition (`roles/nginx_proxy/handlers/main.yml`)

```yaml
---
- name: Restart nginx
  ansible.builtin.systemd:
    name: nginx
    state: restarted

- name: Reload nginx
  ansible.builtin.systemd:
    name: nginx
    state: reloaded
```

### 3. Idempotent Command with `changed_when` and `failed_when`

```yaml
---
- name: Initialize application database schema
  ansible.builtin.command:
    cmd: /opt/app/bin/app-migrate --check-only
  register: migration_check
  changed_when: false
  failed_when: migration_check.rc not in [0, 2]

- name: Run database migration when pending migrations exist
  ansible.builtin.command:
    cmd: /opt/app/bin/app-migrate --execute
  when: migration_check.rc == 2
  register: migration_result
  changed_when: "'Applied' in migration_result.stdout"
  failed_when: migration_result.rc != 0
```

### 4. Transactional Block, Rescue, and Always Pattern

```yaml
---
- name: Safely apply application release
  block:
    - name: Download release tarball
      ansible.builtin.get_url:
        url: "https://artifacts.corp.internal/app-{{ app_version }}.tar.gz"
        dest: "/tmp/app-{{ app_version }}.tar.gz"
        mode: "0640"
        checksum: "sha256:{{ app_sha256 }}"

    - name: Extract release payload
      ansible.builtin.unarchive:
        src: "/tmp/app-{{ app_version }}.tar.gz"
        dest: "/opt/app/releases/{{ app_version }}"
        remote_src: true

    - name: Switch current release symlink
      ansible.builtin.file:
        src: "/opt/app/releases/{{ app_version }}"
        dest: "/opt/app/current"
        state: link
      notify: Restart application

  rescue:
    - name: Log deployment failure
      ansible.builtin.debug:
        msg: "Deployment failed for version {{ app_version }}. Initiating rollback."

    - name: Roll back symlink to previous release
      ansible.builtin.file:
        src: "/opt/app/releases/{{ app_previous_version }}"
        dest: "/opt/app/current"
        state: link

  always:
    - name: Clean up temporary download archive
      ansible.builtin.file:
        path: "/tmp/app-{{ app_version }}.tar.gz"
        state: absent
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Operational Risk | Production Resolution |
| :--- | :--- | :--- |
| **Using `shell` / `command` indiscriminately** | Breaks idempotency; every run marks tasks as "changed"; triggers unnecessary handler reloads. | Use native declarative modules (`template`, `copy`, `apt`, `systemd`). Add `changed_when` if commands are mandatory. |
| **Plaintext passwords in playbooks** | Credentials leak into Git repositories, shell logs, and pull request histories. | Use `ansible-vault encrypt_string` and load values dynamically. Mark tasks with `no_log: true`. |
| **Relying on blanket `ignore_errors: true`** | Conceals critical failures; hosts proceed with incomplete configurations, creating split-brain states. | Replace with explicit `failed_when` conditions or `block`/`rescue` recovery routines. |
| **Restarting services inside task bodies** | Multiple tasks in a play trigger repeated service disruptions instead of a single coordinated reload. | Decouple actions using `notify` to call handlers defined in `handlers/main.yml`. |
| **Missing `mode` on file and template tasks** | Target files receive unpredictable permissions based on remote umask, leading to security breaches. | Explicitly specify `mode: "0644"`, `mode: "0600"`, or `mode: "0755"` on all file operations. |
| **Polluting root namespace with host variables** | Unstructured variables in playbooks collide across groups and environments. | Organize inventory with `group_vars/<group_name>.yml` and role defaults in `defaults/main.yml`. |

---

## Verification Checklist

When creating or maintaining Ansible code, verify every standard before merging:

- [ ] **Syntax Verification**: `ansible-playbook --syntax-check -i inventory/hosts site.yml` succeeds without error.
- [ ] **Linting Quality**: `ansible-lint` returns 0 violations across all plays and roles.
- [ ] **Idempotency Check**: Running `ansible-playbook site.yml` twice consecutively shows `changed=0` on the second run.
- [ ] **Secret Masking**: All tasks receiving secrets specify `no_log: true` and load values from encrypted Vault storage.
- [ ] **FQCN Usage**: All tasks reference Fully Qualified Collection Names (e.g., `ansible.builtin.*`).
- [ ] **File Permissions**: Every `copy`, `template`, `file`, and `get_url` task explicitly defines `owner`, `group`, and `mode`.
- [ ] **Template Validation**: Configuration file deployments utilize the `validate:` directive where binaries support config testing.
- [ ] **Handler Efficiency**: Side effects (restarts/reloads) are handled strictly via notified handlers.
- [ ] **Tag Coverage**: Key tasks declare appropriate tags (`install`, `config`, `service`) for targeted runs.

---

## Tooling & Reference Guides

- **Syntax & Linting Commands**:
  ```bash
  ansible-playbook -i inventory/hosts site.yml --syntax-check
  ansible-lint site.yml roles/*
  ```
- **Idempotency Dry Run**:
  ```bash
  ansible-playbook -i inventory/hosts site.yml --check --diff
  ```
- **Vault Management**:
  ```bash
  ansible-vault encrypt_string --name 'db_password' 'supersecret'
  ansible-vault encrypt group_vars/all/vault.yml
  ansible-vault decrypt group_vars/all/vault.yml
  ```
- **Official Documentation**:
  - [Ansible Documentation](https://docs.ansible.com/ansible/latest/index.html)
  - [Ansible Role Directory Structure](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)
  - [Ansible-Lint Rules Documentation](https://ansible.readthedocs.io/projects/lint/)
