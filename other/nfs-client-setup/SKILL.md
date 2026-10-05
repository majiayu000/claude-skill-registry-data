---
name: nfs_client_setup
description: Runs ansible/nfs_client_setup.yml to configure a RHEL-family host as an NFS client mounting one export, as part of the Linux SOE. Use when asked to set up, check, or fix an NFS client mount — as distinct from the general host baseline (configure_rhel.yml) or an NFS server (nfs_server_setup).
---

# nfs_client_setup

Runs `ansible/nfs_client_setup.yml`, a purpose-built playbook that mounts
one NFS export on a host, by reusing four generic domain roles with
NFS-client-specific variables set directly in the playbook. See
`docs/ARCHITECTURE.md` for the six-playbook layout this fits into, and
each role's own `SKILL.md` (`packages_install`, `files_create`,
`service_state`, `mount_setup`) for what it does in the general case.

## Policy & workload awareness

This playbook doesn't own an `ansible/roles/<name>/` directory of its
own — it reuses `packages_install`, `files_create`, `service_state`, `mount_setup`, each of which already carries its own
policy/workload staleness check in its own `SKILL.md` (see
`docs/ARCHITECTURE.md`'s "Policy & workload awareness"). What's specific to
*this* playbook is the `nfs_client_setup.yml`-specific variables set directly
there rather than in any role's own `defaults/main.yml` — check whether
those need updating too:

```
git log -1 --format='%cI %h %s' -- docs/POLICY.md docs/WORKLOAD.md
git log -1 --format='%cI %h %s' -- ansible/nfs_client_setup.yml
```

If the docs are newer than the playbook file, re-read both docs with this
specific workload in mind (not just the general-baseline case each
underlying role's own check considers) before assuming nothing needs to
change.

## What the playbook actually does

Encoded directly in `ansible/nfs_client_setup.yml`'s `vars:` block:

- `nfs_mount_src` (default `192.168.122.130:/export`) and `nfs_mount_dir`
  (default `/mnt/remote`) — the two values everything else derives from.
  **Always override both** for a real host; the defaults point at an
  example lab address.
- `packages_install: [nfs-utils]`.
- `files_create` creates `nfs_mount_dir` as a directory, owned
  `nobody:nobody`, mode `0755`.
- `service_state_enable: [nfs-client.target]`.
- `mount_setup_enable` mounts `nfs_mount_src` at `nfs_mount_dir`,
  `fstype: nfs`, `opts: _netdev,hard`, `state: mounted` — `_netdev` marks
  it as a network filesystem for systemd's mount ordering, `hard` means
  I/O blocks and retries indefinitely on an NFS outage rather than
  returning an error (the opposite of `soft`).

`gather_facts: false` and `become: true` at the play level.

## What to do

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/nfs_client_setup.yml --check --diff
```

Summarize the diff output and any failed tasks in plain language. To limit
to one piece, add `--tags <role>` (`packages_install`, `files_create`,
`service_state`, or `mount_setup`).

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the same command without `--check`, with `nfs_mount_src`/`nfs_mount_dir`
overridden for the real host via `-e` or group_vars/host_vars:

```
ansible-playbook ansible/nfs_client_setup.yml \
  -e nfs_mount_src=<server>:<export> -e nfs_mount_dir=<local-path>
```

**Propose a change to this playbook**: never edit and commit directly. On a
branch named `soe/nfs_client_setup/<short-desc>`, edit
`ansible/nfs_client_setup.yml`, validate locally (`--syntax-check`,
`--check --diff` against a real/test host if available), then push and
open a PR titled `[nfs_client_setup] <what changed>` with the
`--check --diff` output in the body. Then stop — a human reviews and
merges; see `docs/ARCHITECTURE.md`'s "Contribution workflow". If the
change is really to one of the underlying roles' general behavior (not
this playbook's specific use of it), scope the branch/PR to that role
instead, per its own `SKILL.md`.

## Notes

- `mount_setup_enable`'s `opts: _netdev,hard` means a hung/unreachable NFS
  server can make processes touching this mount block indefinitely
  (that's what `hard` is for — it favors data consistency over
  availability). If the host needs the mount to time out instead, that's a
  variable override (`opts: _netdev,soft,timeo=...`), not a playbook bug.
- This playbook has no `firewall` role invocation — client-side NFS
  generally doesn't need inbound firewalld rules the way the server does
  (see `nfs_server_setup.yml`), but if the host's outbound policy is
  restrictive, that's out of scope for this playbook today.
- Mounting the wrong `nfs_mount_dir` on a host that already uses that path
  for something else silently overwrites what's there once mounted
  (the prior contents become inaccessible, not deleted, until unmounted) —
  confirm the target path is dedicated to this mount before remediating.
