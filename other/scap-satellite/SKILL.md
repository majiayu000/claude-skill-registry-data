---
name: scap_satellite
description: Maintains the ansible/roles/scap_satellite Ansible role that runs foreman_scap_client against Satellite/Capsule-defined compliance policies, as part of the Linux SOE. Use when checking OpenSCAP compliance reported through Satellite rather than run locally (see scap_compliance for a standalone oscap run).
---

# scap_satellite

Maintains `ansible/roles/scap_satellite/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/scap_satellite/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/scap_satellite/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/scap_satellite/policy-<short-desc>` or
  `soe/scap_satellite/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/scap_satellite/defaults/main.yml`:

- Requires the host already registered to Satellite/Capsule, and
  Satellite/Capsule itself already configured with the referenced policies —
  this role only runs the client-side scan.
- `scap_satellite_server`/`_port`/`_timeout` point at the Capsule; unlike
  `scap_compliance`, the actual profile selection lives in Satellite's own
  Compliance Policies, referenced here by `scap_satellite_policies` (list of
  `id`/`profile`, optionally `tailoring_id`/`tailoring_profile`).
- `scap_satellite_refresh_policy_files` (default `false`) — reuses cached
  policy files unless forced.
- `scap_satellite_fetch_remote_resources` (default `false`) — passed to oscap;
  enabling lets the scan pull remote SCAP content, an outbound-network and
  supply-chain consideration.

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/scap_satellite`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

This role is **not referenced by any playbook in `ansible/`** right now —
not `configure_rhel.yml` (not even commented out), not
`load_balancer_setup.yml`/`nfs_client_setup.yml`/`nfs_server_setup.yml`/
`update_rhel.yml`. There is currently no `ansible-playbook` command that will
invoke `scap_satellite` in this repo. Before running it, either:

1. **Add it to an existing playbook** — most often
   `ansible/configure_rhel.yml`'s `roles:` list (uncomment-style, with a
   `vars:` entry for `scap_satellite` set to what's actually needed), if what's wanted is
   a permanent, repeatable part of the host baseline; or
2. **Write a small ad hoc playbook** for the one-off task, same shape as
   `ansible/load_balancer_setup.yml`/`ansible/nfs_client_setup.yml` (a
   `vars:` block plus a `roles: [scap_satellite]` list), if it's a one-time or
   host-class-specific job that doesn't belong in the general baseline.

Either way, propose it via the branch + PR workflow below rather than running
an untracked local playbook against a real host. Once wired in, audit/remediate
the same way as any other role — `--tags scap_satellite` against whichever playbook now
contains it, `--check --diff` first:

```
ansible-playbook ansible/<playbook>.yml --tags scap_satellite --check --diff   # audit
ansible-playbook ansible/<playbook>.yml --tags scap_satellite                  # remediate
```

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/scap_satellite/<short-desc>`, edit `ansible/roles/scap_satellite/`, validate
locally (`--syntax-check`, `ansible-lint roles/scap_satellite/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[scap_satellite] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes

- This role reports compliance status to Satellite; it does not remediate —
  don't conflate a clean run here with `scap_compliance`'s remediation
  capability when summarizing results to the user.

## Wiring into the SOE

This role has a row in `.claude/skills/soe/SKILL.md`'s domain table, but (see
"What to do" above) is not currently included in any playbook in this repo —
neither the general baseline (`ansible/configure_rhel.yml`) nor any of the
composite playbooks. This repo no longer uses `ansible/site.yml`; see
`docs/ARCHITECTURE.md`.
