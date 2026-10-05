---
name: ima_evm_setup
description: Maintains the ansible/roles/ima_evm_setup Ansible role that enables or disables IMA/EVM file-integrity appraisal via a signed policy file, as part of the Linux SOE. Use when checking or fixing IMA/EVM state. Only applies on RHEL 9.7+; no-ops (with a gathered-fact check) on older releases.
---

# ima_evm_setup

Maintains `ansible/roles/ima_evm_setup/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/ima_evm_setup/README.md` documents this role's full
configuration surface (every `defaults/main.yml` variable, with its
original inline comments, rendered as a single reference). Read it
before proposing or explaining how to configure this role — it
reflects the role's actual current defaults even if a variable summary
elsewhere in this file has drifted out of sync with the role.

## Policy & workload awareness

`docs/POLICY.md` and `docs/WORKLOAD.md` capture org-wide policy items and
the workloads this SOE actually hosts — either can gain a new or changed
item that this role should reflect. Before auditing, remediating, or
proposing a change, check whether either doc has changed more recently
than this role's own code:

```
git log -1 --format='%cI %h %s' -- docs/POLICY.md docs/WORKLOAD.md
git log -1 --format='%cI %h %s' -- ansible/roles/ima_evm_setup/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/ima_evm_setup/policy-<short-desc>` or
  `soe/ima_evm_setup/workload-<short-desc>`), same branch + PR workflow as
  any other role change (see "What to do" above and
  `docs/ARCHITECTURE.md`'s "Contribution workflow"). Don't wait to be
  asked.
- **Not relevant** — say so explicitly (e.g. "checked against
  `docs/POLICY.md` and `docs/WORKLOAD.md` as of `<date>`, nothing affecting
  this domain") rather than silently skipping the check.

This check is informational, not a gate — it runs alongside a normal
audit/remediate, never blocks one; surface the staleness note alongside
the normal output.

## What the role actually does

Encoded in `ansible/roles/ima_evm_setup/defaults/main.yml`:

- `ima_evm_setup_enable: null` (default) leaves current IMA/EVM state
  untouched — same null-means-noop pattern as `firewall_enable`.
- Only takes effect when `ansible_facts.distribution_version | float >= 9.7`
  (gathered if not already present); silently does nothing on 9.6 and earlier.
- `ima_evm_setup_policy_config_file` (default:
  `/usr/share/ima/policies/01-appraise-executable-and-lib-signatures`, part of
  `ima-evm-utils`) must already exist **on the target** — this is not a local
  file copied by the role.
- `ima_evm_setup_verify_policy` (default `true`) validates the new policy
  before applying; because the mechanism *appends* to the current policy
  rather than replacing it, the combined policy is only actually in effect
  after a reboot.
- `ima_evm_setup_reboot` (default `false`) — disabling IMA fully requires a
  reboot to complete per the role's own note.

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/ima_evm_setup`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

> **This role is off by default** in `ansible/configure_rhel.yml` — every
> role there (active or not) is gated by a single `configure_rhel_domains`
> list variable (`when: "'<name>' in configure_rhel_domains"`), and `ima_evm_setup`
> isn't in the default value of that list. Nothing needs editing in the
> playbook itself to turn it on: pass the *full* desired domain list via
> `-e`, e.g.
> `-e '{"configure_rhel_domains": [...the default 20..., "ima_evm_setup"]}'`
> (see `.claude/skills/configure_rhel/SKILL.md` for the current default list
> to extend, and why it has to be the full list, not just the addition —
> `-e` replaces the variable's value, it doesn't merge into it). `--tags ima_evm_setup`
> alone is **not** enough — the domains list and `--tags`/`--skip-tags` are
> separate, ANDed gates, both verified independently: a role only runs if
> it's in `configure_rhel_domains` *and* matches the requested tags. Some
> roles (this one — check its `defaults/main.yml` and task file) also have
> their own internal enable flag or required variable on top of that, which
> still needs setting the same as before. Flag all of this to the user before
> assuming the commands below will do anything.

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/configure_rhel.yml --tags ima_evm_setup --check --diff
```

Summarize the diff output and any failed tasks in plain language.

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the same command without `--check`:

```
ansible-playbook ansible/configure_rhel.yml --tags ima_evm_setup
```

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/ima_evm_setup/<short-desc>`, edit `ansible/roles/ima_evm_setup/`, validate
locally (`--syntax-check`, `ansible-lint roles/ima_evm_setup/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[ima_evm_setup] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes

- A bad or overly strict appraisal policy can block executables/libraries
  from running after reboot — this is a boot-risk change in the same class as
  `boot_parameters`; treat proposed policy-file changes with the same caution
  and confirm before a real remediate run that reboots.

## Wiring into the SOE

This role has a row in `.claude/skills/soe/SKILL.md`'s domain table. It's
present (not commented out) in `ansible/configure_rhel.yml`'s `roles:` list,
gated by `configure_rhel_domains` — off by default, on via `-e` — see the
caveat at the top of "What to do" above and
`.claude/skills/configure_rhel/SKILL.md`. It is not referenced by any of the
other playbooks (`load_balancer_setup.yml`, `nfs_client_setup.yml`,
`nfs_server_setup.yml`, `update_rhel.yml`, `connect_linux.yml`) either. This
repo no longer uses `ansible/site.yml`; see `docs/ARCHITECTURE.md`.
