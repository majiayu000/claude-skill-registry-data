---
name: load_balancer_setup
description: Runs ansible/load_balancer_setup.yml to configure a RHEL-family host as an haproxy + keepalived load balancer, as part of the Linux SOE. Use when asked to set up, check, or fix a load balancer host, haproxy, or keepalived — as distinct from the general host baseline covered by configure_rhel.yml.
---

# load_balancer_setup

Runs `ansible/load_balancer_setup.yml`, a purpose-built playbook that
configures haproxy + keepalived on a host, by reusing four generic,
list-driven domain roles with load-balancer-specific variables set directly
in the playbook (not those roles' own `defaults/main.yml`). See
`docs/ARCHITECTURE.md` for the six-playbook layout this fits into, and each
role's own `SKILL.md` (`packages_install`, `files_copy`, `sebooleans`,
`service_state`) for what it does in the general case.

## Policy & workload awareness

This playbook doesn't own an `ansible/roles/<name>/` directory of its
own — it reuses `packages_install`, `files_copy`, `sebooleans`, `service_state`, each of which already carries its own
policy/workload staleness check in its own `SKILL.md` (see
`docs/ARCHITECTURE.md`'s "Policy & workload awareness"). What's specific to
*this* playbook is the `load_balancer_setup.yml`-specific variables set directly
there rather than in any role's own `defaults/main.yml` — check whether
those need updating too:

```
git log -1 --format='%cI %h %s' -- docs/POLICY.md docs/WORKLOAD.md
git log -1 --format='%cI %h %s' -- ansible/load_balancer_setup.yml
```

If the docs are newer than the playbook file, re-read both docs with this
specific workload in mind (not just the general-baseline case each
underlying role's own check considers) before assuming nothing needs to
change.

## What the playbook actually does

Encoded directly in `ansible/load_balancer_setup.yml`'s `vars:` block:

- `packages_install: [haproxy, keepalived]` — installs both packages via
  the `packages_install` role, **overriding** that role's own default
  baseline utility package list entirely (this playbook's `vars:` replace
  the role's `defaults/main.yml` value, they don't add to it).
- `files_copy` deploys `keepalived-notify-haproxy` to
  `/usr/local/sbin/keepalived-notify-haproxy` (mode `0755`).
- `files_copy_templates` renders three Jinja templates:
  `haproxy-global.cfg.j2` → `/etc/haproxy/haproxy.cfg`,
  `haproxy-app.cfg.j2` → `/etc/haproxy/conf.d/app.cfg`, and
  `keepalived.conf.j2` → `/etc/keepalived/keepalived.conf`.
- `service_state_enable: [keepalived]` — only `keepalived` is enabled
  directly; the comment in the playbook notes keepalived manages haproxy
  itself (via the notify script above), so haproxy isn't separately
  enabled here.
- A second `service_state` role invocation conditionally reloads haproxy
  and restarts keepalived, but **only** `when: copy_templates is changed
  and start_services is not changed` — i.e. only if the templates actually
  changed on this run and the initial enable didn't already restart
  something, avoiding a redundant double-restart.
- `sebooleans` is in the `roles:` list but its `vars:` (`sebooleans_enable:
  [haproxy_connect_any]`) is commented out by default — see "Notes" below.

> **Known gap, verified against this checkout**: the four assets this
> playbook references — `keepalived-notify-haproxy`, `haproxy-global.cfg.j2`,
> `haproxy-app.cfg.j2`, `keepalived.conf.j2` — do **not exist anywhere in
> this repository** (no `ansible/files/`, no `ansible/templates/`, nothing
> under `roles/files_copy/`). `files_copy`'s `ansible.builtin.copy`/
> `template` tasks resolve `src:` by searching the playbook directory's
> `files/`/`templates/` subdirectories (and the current role's, when one
> applies) — none of those exist here. Running this playbook today fails
> with "could not find src" on both the `files_copy` and
> `files_copy_templates` tasks, both under `--check` and for real. Don't
> tell a user this playbook works end-to-end without flagging this; the
> package install, `sebooleans`, and `service_state` steps are unaffected
> and will still run.

## What to do

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/load_balancer_setup.yml --check --diff
```

Summarize the diff output and any failed tasks in plain language. To audit
just one piece (e.g. only the package install), add `--tags packages_install`
etc.

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the same command without `--check`:

```
ansible-playbook ansible/load_balancer_setup.yml
```

**Propose a change to this playbook or its templates**: never edit and
commit directly. On a branch named `soe/load_balancer_setup/<short-desc>`,
edit `ansible/load_balancer_setup.yml` and/or the referenced templates,
validate locally (`--syntax-check`, `--check --diff` against a real/test
host if available), then push and open a PR titled
`[load_balancer_setup] <what changed>` with the `--check --diff` output in
the body. Then stop — a human reviews and merges; see
`docs/ARCHITECTURE.md`'s "Contribution workflow". If the change is really
to one of the underlying roles' general behavior (not this playbook's
specific use of it), scope the branch/PR to that role instead, per its own
`SKILL.md`.

## Notes

- **Before anything else**: this playbook can't currently deploy the
  haproxy/keepalived config (see the gap noted above) — create
  `ansible/files/keepalived-notify-haproxy` and
  `ansible/templates/{haproxy-global.cfg,haproxy-app.cfg,keepalived.conf}.j2`
  (or wherever `files_copy`'s search path actually needs them for this
  playbook) before relying on it for a real load balancer build-out, and
  propose that addition via the branch + PR workflow below like any other
  change.
- `sebooleans_enable: [haproxy_connect_any]` is present in the playbook
  but **commented out** — SELinux may block haproxy from connecting out
  to backend servers on a non-standard port until this is enabled. If
  haproxy fails to reach its backends and SELinux is enforcing, check
  `ausearch`/`sealert` for `haproxy_connect_any` denials and uncomment
  this before assuming the haproxy config itself is wrong.
- This playbook doesn't open any firewalld ports/services for haproxy —
  unlike `nfs_server_setup.yml`, it has no `firewall` role invocation at
  all. If the load balancer needs firewalld rules, that's a change to
  propose to this playbook (or handle via `configure_rhel.yml`'s
  `firewall` role for that host/group), not something this playbook does
  today.
