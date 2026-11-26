---
name: ansible-conventions
description: "Ansible conventions for check mode safety, dynamic inventory generated from infrastructure outputs, idempotent tasks, pre-flight guards before a destructive run, and the ansible-lint and syntax-check gate in CI. Use when writing, reviewing or running a playbook, a role or an inventory script."
---

# Ansible conventions

Ansible configures a host that already exists and that no declarative tool reaches yet.

## When to use

- Writing or changing a playbook, a role, an inventory script, `group_vars` or `host_vars`.
- Reviewing a change that touches a host outside Kubernetes.
- Deciding whether a step belongs in Ansible or in infrastructure code instead.

## Rules

### Check mode safety

- Hard rule: every play runs clean under `--check` before it ever runs for real.
- A module with check mode support simulates a change under `--check` and reports what it would
  do. A module without support, `command`, `shell`, a custom module, reports nothing.
- A task without check mode support sets `check_mode: false` only when it reads and does not
  change anything, and a later task branches on its registered result. Without that, the result
  is empty under `--check`, and the branch reports nonsense without saying so. A task that
  changes something never gets `check_mode: false`.
- `changed_when` reflects the real result of the task, never a module's default guess.
- `--check --diff` runs before every run against real hosts. Read the diff, then run for real.

### Scope

- Ansible configures a host. A workload that runs in Kubernetes is a Helm release through
  infrastructure code, see `kubernetes-conventions`.
- Cloud resources belong to infrastructure code, not an Ansible module. Ansible starts once the
  machine already exists.
- A host with its own declarative configuration mechanism takes its config through that
  mechanism, not a playbook.

### Layout

- `ansible/` holds `inventory/`, `playbooks/`, `roles/`, `group_vars/`, `host_vars/`.
- One playbook per outcome, named for what it achieves, not for the host it targets.
- A role declares its inputs in `defaults/main.yaml`, one comment per variable. Files end in
  `.yaml`, Ansible reads both spellings.
- `group_vars` holds per-environment values, `host_vars` the per-host ones. Nothing inline in a
  playbook.

### Dynamic inventory

- Inventory is generated, not hand maintained, whenever the hosts already live in infrastructure
  code's state. A committed script under `inventory/` builds it from that state's outputs, with a
  unit test against a fixture file covering its grouping logic.
- The person or the CI job holding the credentials runs `tofu output -json` and hands the script
  that JSON on stdin or from a path. An agent never runs that command, see `opentofu-conventions`:
  outputs can carry secrets. In a session the agent works against the fixture or a file the user
  supplies.
- The script needs no credential and no network. An unapplied module means an empty inventory,
  and the script says so instead of failing.
- A static, hand written inventory still needs a reason in the pull request once the hosts could
  have been generated instead.

### Idempotency and tasks

- Every task is idempotent. A second run changes nothing and reports no change.
- Name every task. An unnamed task is unreadable in output and impossible to target.
- Use the module, not `command` or `shell`. Where shell is unavoidable, set `changed_when` and
  `creates` so it stops claiming a change that did not happen.
- `ansible.builtin.*` fully qualified, so a collection cannot shadow a builtin.
- No `ignore_errors` without a comment saying why the failure is acceptable.
- Handlers for restarts, so a service restarts once, not once per task that touched it.
- Collection and role versions pinned in `requirements.yaml`, updated like any other dependency.

### Pre-flight guards for destructive tasks

- A task that writes a whole disk, drops data, or anything else that cannot be undone gets a
  pre-flight guard that refuses rather than warns.
- The guard checks that the target is not currently mounted and is not the host's own root
  filesystem. That check never has an override.
- A second check makes a re-run a no-op: a target that already carries the expected marker is
  left alone.
- An explicit `force` variable, false by default, may override the idempotency check only. It
  never overrides the check that the target is not live.

### Secrets

- No secret in a vars file, `group_vars`, `host_vars` or a role default, plain or committed. See
  `secrets-handling`.
- A task whose output would contain a secret value sets `no_log: true`.

### Environment and CI

- `ansible-core` and `ansible-lint` are pinned in `mise.toml` like any other tool. `ansible-lint`
  has no short name in the registry, pin it backend qualified: `"pypi:ansible-lint"`.
- A virtualenv built from a separate pinned requirements file is a gap, not a pattern to copy
  forward.
- `--syntax-check` and `ansible-lint` run in CI on every change, against no host.
- CI never runs a playbook against a real host. A real run needs a person at the keyboard.

## Guardrails

- Never run a play against real hosts without `--check --diff` having run first.
- Never run `tofu output` or `tofu state show` to build the inventory. Take the JSON from the
  person or the CI job that ran it.
- Never let a destructive task skip its pre-flight guard, with or without `force`.
- Never put a secret in a vars file. Read it from the secret store at run time instead.
- Never run `ansible-playbook` against real hosts in CI.

## References

- `kubernetes-conventions` for anything that runs inside the cluster instead.
- `secrets-handling` for the secret store and what never enters a vars file.
- `opentofu-conventions` for the infrastructure code an inventory script reads.
