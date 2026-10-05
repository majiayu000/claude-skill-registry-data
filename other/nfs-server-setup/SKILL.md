---
name: nfs_server_setup
description: Runs ansible/nfs_server_setup.yml to configure a RHEL-family host as an NFS server exporting one directory, as part of the Linux SOE. Use when asked to set up, check, or fix an NFS server/export — as distinct from the general host baseline (configure_rhel.yml) or an NFS client (nfs_client_setup).
---

# nfs_server_setup

Runs `ansible/nfs_server_setup.yml`, a purpose-built playbook that exports
one directory over NFS, by reusing six generic domain roles with
NFS-server-specific variables set directly in the playbook. See
`docs/ARCHITECTURE.md` for the six-playbook layout this fits into, and
each role's own `SKILL.md` (`packages_install`, `files_create`,
`files_copy`, `sebooleans`, `firewall`, `service_state`) for what it does
in the general case.

## Policy & workload awareness

This playbook doesn't own an `ansible/roles/<name>/` directory of its
own — it reuses `packages_install`, `files_create`, `files_copy`, `sebooleans`, `firewall`, `service_state`, each of which already carries its own
policy/workload staleness check in its own `SKILL.md` (see
`docs/ARCHITECTURE.md`'s "Policy & workload awareness"). What's specific to
*this* playbook is the `nfs_server_setup.yml`-specific variables set directly
there rather than in any role's own `defaults/main.yml` — check whether
those need updating too:

```
git log -1 --format='%cI %h %s' -- docs/POLICY.md docs/WORKLOAD.md
git log -1 --format='%cI %h %s' -- ansible/nfs_server_setup.yml
```

If the docs are newer than the playbook file, re-read both docs with this
specific workload in mind (not just the general-baseline case each
underlying role's own check considers) before assuming nothing needs to
change.

## What the playbook actually does

Encoded directly in `ansible/nfs_server_setup.yml`'s `vars:` block:

- `nfs_export_dir` (default `/export`), `nfs_network` (default
  `192.168.122.0/24`), `nfs_options` (default `rw,sync,root_squash`) — the
  values everything else derives from. **Always override these** for a
  real host/network; the defaults point at an example lab subnet.
- `packages_install: [nfs-utils]`.
- `files_create` creates `nfs_export_dir` as a directory, owned
  `nobody:nobody`, mode `0755`, **with `setype: public_content_rw_t`** —
  this SELinux context is what actually lets NFS clients write to the
  export under a targeted policy; a directory created without it will
  silently deny client writes even though `nfs_options` says `rw`.
- `files_copy` writes the export line itself —
  `{{ nfs_export_dir }} {{ nfs_network }}({{ nfs_options }})` — to
  `/etc/exports.d/ansible.exports` via inline `content:` (not a template
  file, so there's no missing-asset issue here the way there is for
  `load_balancer_setup.yml` — see that skill's `SKILL.md`).
- `sebooleans_enable: [nfs_export_all_rw]` — enabled, not commented out
  (unlike `load_balancer_setup.yml`'s `haproxy_connect_any`), because
  without it the export can silently deny client writes regardless of the
  `public_content_rw_t` context above.
- `firewall_enable: true`, `firewall_default_zone: public`,
  `firewall_open_services: [nfs]` — opens the `nfs` firewalld service. The
  playbook's own comment notes `redhat.rhel_system_roles.firewall` is an
  option for more nuanced firewall configuration if this basic
  enable/service-open isn't enough.
- `service_state_enable: [nfs-server]`.
- A second `service_state` role invocation reloads `nfs-server`, but only
  `when: copy_files is changed and start_services is not changed` — same
  avoid-a-redundant-restart pattern as `load_balancer_setup.yml`.

## What to do

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/nfs_server_setup.yml --check --diff
```

Summarize the diff output and any failed tasks in plain language. To limit
to one piece, add `--tags <role>` (`packages_install`, `files_create`,
`files_copy`, `sebooleans`, `firewall`, or `service_state`).

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the same command without `--check`, with `nfs_export_dir`/`nfs_network`/
`nfs_options` overridden for the real host via `-e` or
group_vars/host_vars:

```
ansible-playbook ansible/nfs_server_setup.yml \
  -e nfs_export_dir=<path> -e nfs_network=<cidr> -e nfs_options=<opts>
```

**Propose a change to this playbook**: never edit and commit directly. On a
branch named `soe/nfs_server_setup/<short-desc>`, edit
`ansible/nfs_server_setup.yml`, validate locally (`--syntax-check`,
`--check --diff` against a real/test host if available), then push and
open a PR titled `[nfs_server_setup] <what changed>` with the
`--check --diff` output in the body. Then stop — a human reviews and
merges; see `docs/ARCHITECTURE.md`'s "Contribution workflow". If the
change is really to one of the underlying roles' general behavior (not
this playbook's specific use of it), scope the branch/PR to that role
instead, per its own `SKILL.md`.

## Notes

- `nfs_options` defaults to `root_squash` (the remote root user is mapped
  to `nobody`, not given root on the export) — don't casually switch to
  `no_root_squash` without the user explicitly asking for it; it's a
  meaningful privilege-escalation surface for any client on `nfs_network`.
- `nfs_network` gates who can mount the export at all — widening it (e.g.
  to `0.0.0.0/0`) exposes the export to any host that can reach this
  server's network, not just the intended client subnet. Confirm the
  actual client network before remediating with a broadened value.
- This playbook writes to `/etc/exports.d/ansible.exports`, not
  `/etc/exports` directly — `exportfs` picks up `/etc/exports.d/*.exports`
  automatically, but if the host has conflicting entries for the same
  path in `/etc/exports` itself or another file under `/etc/exports.d/`,
  the *last* one `exportfs -ra` processes wins; check for pre-existing
  export config before assuming this playbook's line is authoritative.
