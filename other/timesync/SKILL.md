---
name: timesync
description: Maintains the ansible/roles/timesync Ansible role that wraps the redhat.rhel_system_roles.timesync collection role with a list of NTP servers as input, and flushes handlers so time updates immediately, on RHEL-family systems as part of the Linux SOE. Use when checking, configuring, or fixing NTP/chrony time sync, clock drift, or "system clock not synchronized" issues.
---

# timesync

This skill's deliverable is `ansible/roles/timesync/`. See
`docs/ARCHITECTURE.md` for the shared conventions (role layout, audit vs.
remediate via `--check --diff`, safety rules).

`ansible/roles/timesync/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/timesync/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/timesync/policy-<short-desc>` or
  `soe/timesync/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/timesync/defaults/main.yml`:

- `timesync_ntp_servers` (default: a list of 5 entries —
  `0.rhel.pool.ntp.org` through `3.rhel.pool.ntp.org` plus
  `time.cloudflare.com`, all with `iburst: true`): each entry is a dict
  with at least `hostname` and any options the
  `redhat.rhel_system_roles.timesync` collection role's `timesync_ntp_servers`
  var accepts (e.g. `iburst`, `pool` vs. plain server, `nts`).
- The role itself is a thin wrapper: it migrates a legacy single-string
  `ntp_servers` list (if `timesync_ntp_servers` isn't set but `ntp_servers`
  is) into the new dict form, then `include_role`s
  `redhat.rhel_system_roles.timesync`, then flushes handlers so the time
  update takes effect immediately rather than at end-of-play.
- **All actual config-file management (which package, which service,
  `/etc/chrony.conf` layout, RHEL-vs-Debian path differences) lives inside
  the `redhat.rhel_system_roles.timesync` collection role, not in this
  wrapper.** That collection role is an external dependency — it isn't
  vendored in `ansible/roles/`, so it must be resolvable (Galaxy
  collection install) for this role to do anything at all.

## What to do

**To audit** (read-only, safe to run any time):

```
ansible-playbook ansible/configure_rhel.yml --tags timesync --check --diff
```

Summarize the diff output and any failed tasks in plain language. Because
most of the actual work happens inside the external system role, an
accurate audit also depends on that collection being installed and
behaving correctly under `--check` — this wrapper doesn't add its own
`assert`-based checks on top.

**To remediate** (modifies the system — only after the user explicitly
asks): first summarize what will change from the `--check --diff` output,
then run the same command without `--check`:

```
ansible-playbook ansible/configure_rhel.yml --tags timesync
```

**To propose a change to the role itself** (e.g. changing the default
server list): never edit and commit directly. On a branch named
`soe/timesync/<short-desc>`, edit `ansible/roles/timesync/defaults/main.yml`
(this wrapper has very little in `tasks/main.yml` to change), validate
locally (`--syntax-check`, `ansible-lint roles/timesync/`, and
`--check --diff` against a real/test host if available), then push and
open a PR titled `[timesync] <what changed>` with the `--check --diff`
output in the body. Then stop — a human reviews and merges; see
`docs/ARCHITECTURE.md`'s "Contribution workflow".

## Notes

- Unlike most roles in this repo, `timesync` does **not** assert
  `ansible_os_family == "RedHat"` itself — any OS-family guarding happens
  (or doesn't) inside the external collection role.
- `timesync_ntp_servers` defaults to public NTP pools; point it at the
  org's own internal NTP servers via `group_vars`/`host_vars` or `-e` if
  it has them.
- This role has no dependency on the `redhat.rhel_system_roles` collection
  declared in `meta/main.yml` — if a fresh environment fails with a
  "role not found" error for `redhat.rhel_system_roles.timesync`, that's
  why; install the collection (or fix the missing dependency declaration)
  rather than assuming the role itself is broken.

## Standalone audit/remediate scripts

`scripts/audit.sh` and `scripts/remediate.sh` are a **separate, Ansible-independent**
sanity check — useful for a quick one-host check without an Ansible run,
but they check chrony directly (package installed, `chronyd` enabled/active,
a `server`/`pool` line present in `/etc/chrony.conf`, `timedatectl`
sync status) and are not driven by `timesync_ntp_servers` or aware of
the collection role's actual config layout. Treat them as a
lightweight, independent smoke test, not a substitute for
`--check --diff` against the real role, and note that `remediate.sh`'s
fallback pool (`2.rhel.pool.ntp.org iburst`) is only one entry from the
role's actual 5-entry default list — it exists purely so the script has
*something* to append if `/etc/chrony.conf` has no server/pool line at
all, not to mirror the full baseline.
