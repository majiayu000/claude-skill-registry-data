---
name: ansible-specialist
description: Ansible playbooks, roles, inventory management, and configuration automation
  for Linux/Unix infrastructure. Use when asked to write a playbook, create an Ansible
  role, manage server configuration, set up dynamic inventory for AWS/Azure/GCP, encrypt
  secrets with Ansible Vault, run ad-hoc commands against a fleet, or integrate Ansible
  with CI/CD pipelines.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: infrastructure-iac
  tags:
  - ansible
  - configuration-management
  - devops
  - iac
  - automation
---

# Ansible Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `write a playbook`, `Ansible role`, `configure servers`.
- The requested work fits this skill's lane: Writing playbooks, Ansible roles, dynamic inventory, Ansible Vault, fleet config management.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Cloud resource provisioning (use aws/azure/gcp-specialist); container builds (use docker-specialist).

## First actions
1. `Glob('**/*.yml', '**/*.yaml')` — find existing playbooks, roles, and inventory files
2. `Read` the main playbook or site.yml if found; read inventory files to understand host structure
3. Identify target OS (Ubuntu, CentOS, RHEL, etc.) — this affects module choices and package names
4. Confirm whether Ansible Vault is in use (look for `!vault` tags in vars files)

## Decision rules
- If task involves secrets or credentials: use Ansible Vault; never store plaintext secrets in vars files
- If the playbook touches more than one role's responsibilities: split into separate roles
- If task is idempotency-sensitive: use `state:` parameters and check mode (`--check`) before applying
- If dynamic inventory is needed: identify the cloud provider and use the appropriate inventory plugin (aws_ec2, azure_rm, gcp_compute)
- If scope requires cloud resource provisioning: that belongs to aws-specialist / azure-specialist / gcp-specialist, not here

## Steps

### Step 1: Assess current state
Read existing playbook structure. Identify: hosts/groups being targeted, roles already defined, variable files in use, and any Vault-encrypted content.

### Step 2: Design the solution
Determine whether to write a top-level playbook, a new role, or extend an existing one. If a new role: scaffold it with `ansible-galaxy init roles/<name>` structure.

### Step 3: Write the playbook or role
Follow these ordering rules: handlers go in `handlers/main.yml`; defaults (overridable) go in `defaults/main.yml`; non-overridable vars go in `vars/main.yml`; templates go in `templates/` as `.j2` files.

### Step 4: Validate
Run syntax check: `ansible-playbook --syntax-check site.yml`
Run dry-run: `ansible-playbook --check --diff site.yml`
If Molecule is configured: `molecule test`

### Step 5: Document
Add a README to each new role explaining: purpose, variables (name, default, description), dependencies, and example usage.

## Output contract
- Primary artifact: `.yml` playbook or role directory tree
- Required: all tasks use `name:` fields; all variables are documented in `defaults/main.yml` or `vars/main.yml` with comments
- Validation: playbook passes `--syntax-check` and `--check` before being handed back

## Constraints
- NEVER store plaintext passwords, tokens, or keys in any var file — use Ansible Vault
- NEVER write non-idempotent tasks without explicitly flagging them with a comment explaining why
- Scope boundary: cloud resource provisioning (EC2, VMs, GKE) belongs to cloud specialist skills, not here

## Examples

### Example 1: New role request
User says: "Write an Ansible role to install and configure Nginx with SSL on Ubuntu 22.04"
Actions:
1. Glob for existing roles directory
2. Create role scaffold at `roles/nginx/`
3. Write tasks/main.yml with apt install, config template, service handler
4. Write templates/nginx.conf.j2 with SSL block
5. Write defaults/main.yml with `nginx_port: 443`, `nginx_ssl_cert_path: /etc/ssl/certs/`
Result: Complete role directory with README, passes --syntax-check

### Example 2: Dynamic inventory
User says: "Set up dynamic inventory for our AWS EC2 fleet"
Actions:
1. Read existing ansible.cfg and inventory/ directory
2. Write `inventory/aws_ec2.yml` using `amazon.aws.aws_ec2` plugin
3. Document required IAM permissions and env vars
Result: Working dynamic inventory config with tag-based grouping

## Troubleshooting
**"MODULE FAILURE" or unreachable hosts**
Cause: SSH connectivity, become privileges, or Python interpreter mismatch
Fix: Test with `ansible -m ping all`; verify `ansible_python_interpreter` is set correctly for target OS

**Vault decryption failure**
Cause: Wrong vault password or missing ANSIBLE_VAULT_PASSWORD_FILE
Fix: Confirm vault ID matches; export ANSIBLE_VAULT_PASSWORD_FILE or use --vault-password-file flag

## Reference
- `references/legacy-agent.md`: deep domain knowledge — variable precedence, module reference, Molecule testing, Galaxy patterns
- `references/examples/`: reusable playbook and role snippets
