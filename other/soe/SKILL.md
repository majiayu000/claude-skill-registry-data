---
name: soe
description: Orchestrates the Linux Standard Operating Environment domain roles across ansible/configure_rhel.yml (general host baseline) and the purpose-built playbooks (connect_linux.yml, load_balancer_setup.yml, nfs_client_setup.yml, nfs_server_setup.yml, update_rhel.yml) to audit or remediate a RHEL-family host, and summarizes the results. Use when asked to check, audit, or bring a system into compliance with "the SOE" or "the standard operating environment" as a whole, rather than a single domain.
---

# soe

Top-level orchestrator for the domain skills, each of which maintains one
Ansible role under `ansible/roles/`. Unlike the single-playbook design this
repo used to have (`ansible/site.yml`, running every domain role
unconditionally), the roles are now spread across **six playbooks**, each
scoped to a specific host role or task. This skill picks the right
playbook(s) for what's being asked, runs it (directly, or filtered by
`--tags`), and summarizes the result. See `docs/ARCHITECTURE.md` for the
shared conventions these roles follow and the rationale for the
multi-playbook split.

## Policy & workload awareness (repo-wide)

`docs/POLICY.md` and `docs/WORKLOAD.md` capture org-wide policy items and
the workloads this SOE actually hosts. Every domain skill checks its own
role for staleness against these two docs individually (see
`docs/ARCHITECTURE.md`'s "Policy & workload awareness"); this skill can run
the same check across all 54 in-repo roles at once, as part of (or
alongside) a full SOE audit:

```
policy_ts=$(git log -1 --format=%ct -- docs/POLICY.md docs/WORKLOAD.md)
for d in ansible/roles/*/; do
  name=$(basename "$d")
  role_ts=$(git log -1 --format=%ct -- "$d")
  if [ -n "$role_ts" ] && [ "$policy_ts" -gt "$role_ts" ]; then
    echo "$name: stale (role last touched $(git log -1 --format=%cI -- "$d"))"
  fi
done
```

Report the resulting list of stale domains alongside the normal audit
summary — don't silently fold it in or omit it, and don't treat "stale"
as "broken"; it only means that domain hasn't been read against the
current `docs/POLICY.md`/`docs/WORKLOAD.md` yet, not that anything is
actually wrong. For each stale domain the user asks about (or all of
them, if asked to do a full re-assessment), read both docs and hand off
to that domain's own skill for the relevance judgment and any proposed
change.

## The six playbooks

| Playbook | Purpose | Roles it triggers |
|---|---|---|
| `configure_rhel.yml` | **General host baseline** — the closest equivalent to the old `site.yml`. All 43 in-repo domains it can run are gated by a single `configure_rhel_domains` list variable (`when: "'<name>' in configure_rhel_domains"`) rather than being commented in/out of the file — see `.claude/skills/configure_rhel/SKILL.md`. | 20 in `configure_rhel_domains` by default; 23 more present, fully wired, off by default (enable via `-e`, no file edit needed) |
| `connect_linux.yml` | **Pre-flight connectivity/access check** — no roles at all, just ad hoc tasks confirming SSH reachability and that `become` actually gets root. Run this first against a new/unfamiliar host before anything else. See `.claude/skills/connect_linux/SKILL.md`. | none (raw tasks only) |
| `load_balancer_setup.yml` | Configures a host as an haproxy + keepalived load balancer. See `.claude/skills/load_balancer_setup/SKILL.md` — note that skill documents a verified gap: the templates it needs don't currently exist in this repo. | `packages_install`, `files_copy`, `sebooleans`, `service_state` (haproxy/keepalived-specific vars) |
| `nfs_client_setup.yml` | Configures a host as an NFS client (mounts one export). See `.claude/skills/nfs_client_setup/SKILL.md`. | `packages_install`, `files_create`, `service_state`, `mount_setup` |
| `nfs_server_setup.yml` | Configures a host as an NFS server (exports one directory). See `.claude/skills/nfs_server_setup/SKILL.md`. | `packages_install`, `files_create`, `files_copy`, `sebooleans`, `firewall`, `service_state` |
| `update_rhel.yml` | Reports pending dnf updates (and, opt-in, applies them). See `.claude/skills/update_rhel/SKILL.md`. | `system_update_report_pre` active; `system_update` commented out |

**`--tags <domain>` works correctly against all six playbooks** — every
role entry in all five role-bearing playbooks now carries an explicit
`tags: ["<name>"]`. This wasn't always true: bare role names in a
`roles:` list get no implicit tag matching their own name, so
`--tags <domain>` previously matched nothing anywhere in this repo,
silently, regardless of what any `SKILL.md` claimed — verified directly,
fixed as part of adding `configure_rhel_domains` (see
`.claude/skills/configure_rhel/SKILL.md`'s "Notes"). Trust `--tags` now;
don't add defensive caveats about it not working, that's fixed.

`ansible/site.yml` is **no longer this repo's entrypoint** — don't suggest
it, don't run it, and treat any lingering mention of it elsewhere as stale
documentation to flag for a fix. (The file may still physically exist in
the repo; that isn't the same as it being in use.)

**Important:** `packages_install`, `files_copy`, `files_create`,
`sebooleans`, `service_state`, `firewall`, and `mount_setup` are
low-level, list-driven building-block roles reused across multiple
playbooks above with *different, playbook-specific variables* — e.g.
`packages_install` installs a general utility package set under
`configure_rhel.yml` but installs `haproxy`/`keepalived` under
`load_balancer_setup.yml`. Always confirm which playbook actually matches
the host's role before running one of these — see each such role's own
`SKILL.md` ("Wiring into the SOE" section) for specifics.

**Before proposing or validating any role edit**, check whether
`myllynen.rhel_ansible_roles` is installed as a collection on the machine
you're running `ansible-playbook` from. It's fine if it is — none of the
six playbooks above declare a play-level `collections:` keyword for it
(deliberately; see `docs/ARCHITECTURE.md`'s "Collections vs. local roles"),
so they always resolve roles from this checkout's own `ansible/roles/`
regardless. But if you're ever handed a *different* playbook, or a
modified copy of one of these six that reintroduces that `collections:`
line, treat that as a reason to stop and confirm which role copy is
actually running before trusting any `--check --diff` output — a role
edit can otherwise validate cleanly while silently exercising old,
previously-installed code.

## Domain roles — general baseline (`ansible/configure_rhel.yml`)

In `configure_rhel_domains` by default (see
`.claude/skills/configure_rhel/SKILL.md` for the mechanism):

| Skill / role | Domain |
|---|---|
| `audit_setup` | auditd install + config/rules deployment; can fail or reboot on locked-rules conflicts |
| `boot_parameters` | GRUB/kernel command-line via grubby — **remediates and can reboot by default**, not audit-only |
| `certificates` | CA trust store (anchors/blocklist/extended-format) via update-ca-trust |
| `etc_hosts` | Full, exclusive rewrite of `/etc/hosts`; rebuilds initramfs on change |
| `firewall` | Basic firewalld enable/zone/ports (also invoked separately by `nfs_server_setup.yml`) |
| `guest_agent` | Guest agent for the detected hypervisor (role dir is `guest_agent`, not `vm_guest_agent` — see that skill's note) |
| `ipv6_setup` | IPv6 enable/disable via sysctl + grubby + NM — **reboots on change, no opt-out flag** |
| `packages_install` | Baseline dnf package set (also invoked, with different packages, by `load_balancer_setup.yml`/`nfs_client_setup.yml`/`nfs_server_setup.yml`) |
| `packages_remove` | dnf package denylist removal |
| `performance_tuning` | Active `tuned` profile |
| `resolver_configuration` | How `/etc/resolv.conf` is populated |
| `root_password` | Root account password — no-op until `root_password` is set (vault) |
| `sebooleans` | SELinux boolean enable/disable (also invoked by `load_balancer_setup.yml`/`nfs_server_setup.yml`) |
| `security_hardening` | Secure Boot/FIPS verification (audit-only, can fail run), kernel lockdown, SELinux mode, crypto policy |
| `service_state` | systemd mask/unmask/enable/disable/restart by list — `sshd` is hard-protected (also invoked by all three composite playbooks) |
| `sshd_configuration` | Declarative sshd_config options, validated with `sshd -t` before applying |
| `system_init` | Post-install cleanup — **now active by default here, unlike the old `site.yml`; reboots the host** (see that skill's `SKILL.md`) |
| `system_locale` | System locale — restricted to `C.UTF-8`/`en_US.UTF-8`/`auto`, **reboots by default** on change |
| `timesync` | Thin wrapper around the external `redhat.rhel_system_roles.timesync` collection role |
| `watchdog` | systemd hardware/software watchdog timeouts |

Present in the `roles:` list, fully wired, but **off by default** — not
in `configure_rhel_domains`'s default value. Enable via `-e` for a given
run (see `.claude/skills/configure_rhel/SKILL.md`); no file edit needed:

| Skill / role | Domain |
|---|---|
| `accounts_local` | Local (non-domain) user/group create/delete, passwords, sudoers, SSH keys |
| `accounts_policy` | Local account/login/PAM/authselect config |
| `cron_setup` | cron service, cron.allow/cron.deny, and declarative crontab entries |
| `dns_cache` | Local DNS caching via dnsmasq/systemd-resolved/nscd |
| `domain_ad` | AD domain join/leave via realmd/adcli + sssd/authselect |
| `ima_evm_setup` | IMA/EVM file-integrity appraisal — RHEL 9.7+ only |
| `motd_issue` | `/etc/motd(.d)` and `/etc/issue.d`/`/etc/issue.net` banners |
| `mount_setup` | Mounts a configured filesystem — off here by default; the same role is active by default in `nfs_client_setup.yml` instead, see that skill |
| `multipath_setup` | device-mapper-multipath config — **reboots by default** when enabled |
| `packages_verify` | rpm-level package verification (missing/modified files) |
| `repository_setup` | yum.repos.d files + RHSM registration/repo enablement |
| `rescue_image` | Kernel rescue image generation toggle |
| `scap_compliance` | OpenSCAP oscap scan — remediates whenever `scap_compliance_remediate: true`, **regardless of `--check`** |
| `shell_profile` | System-wide shell profile template |
| `splunk_forwarder` | Splunk universal forwarder deployment-server + local user config |
| `system_coredump` | systemd-coredump enable + size cap |
| `system_hostname` | `/etc/hostname` |
| `system_keyboard` | Virtual console keymap + font |
| `system_update_report_pre` | Reports pending dnf updates — off here by default; active by default in `update_rhel.yml` instead, see that skill |
| `system_update` | Applies dnf updates — off by default in both `configure_rhel.yml` and `update_rhel.yml`, see that skill |
| `timezone` | System timezone via `community.general.timezone` |
| `troubleshooting_tools` | Baseline troubleshooting package set + optional PCP metrics |
| `usbguard_setup` | USBGuard device authorization — **enables enforcement (`policy: reject`) the moment it actually runs**, not a separate opt-in flag on top of `configure_rhel_domains` |

## Domain roles — composite playbooks

| Skill / role | Playbook | Purpose in that playbook |
|---|---|---|
| `mount_setup` | `nfs_client_setup.yml` | Mounts the configured NFS export. Also present (off by default) in `configure_rhel.yml`'s `configure_rhel_domains` toggle — see `.claude/skills/configure_rhel/SKILL.md`. |
| `files_create` | `nfs_client_setup.yml`, `nfs_server_setup.yml` | Creates the mount point / export directory (not in `configure_rhel.yml` at all) |
| `files_copy` | `load_balancer_setup.yml`, `nfs_server_setup.yml` | Deploys haproxy/keepalived config, or the `/etc/exports.d` file (not in `configure_rhel.yml` at all) |
| `system_update_report_pre` | `update_rhel.yml` | Lists pending updates without applying them. Also present (off by default) in `configure_rhel.yml`'s `configure_rhel_domains` toggle. |
| `system_update` | `update_rhel.yml` | Applies updates — off by default in both `update_rhel.yml`'s `roles:` list (still a commented line there, not part of the `configure_rhel_domains`-style toggle) and `configure_rhel.yml`'s `configure_rhel_domains` default. |

## Domain roles — not wired into any playbook

These roles exist under `ansible/roles/` and have a `SKILL.md`, but no
playbook in this repo currently references them (not even commented out).
`--tags <domain>` against any of the six playbooks reports "did not match
any tags." See each role's own `SKILL.md` for how to wire it in (add to
`configure_rhel.yml`, or write a small dedicated playbook) via the branch +
PR workflow:

`files_acl`, `files_fetch`, `files_get`, `files_properties`, `files_remove`,
`files_unarchive`, `scap_satellite`

## Domain roles — deliberately excluded from every playbook

`system_reboot` and `system_unregister` are **not referenced anywhere**,
by design — each acts unconditionally with no guard variable (reboots or
de-registers the host outright), so neither should ever run as a side
effect of a routine playbook run. Invoke either only by adding it to a
playbook's `roles:` list yourself for that specific run, per its own
`SKILL.md`.

(`system_init` used to be in this category under the old `site.yml` — it
no longer is. See the baseline table above and `system_init`'s `SKILL.md`
for that behavior change.)

## What to do

**To run the pre-flight check** on a host you haven't touched before or
aren't sure is reachable:

```
ansible-playbook ansible/connect_linux.yml
```

This has no `--check` mode of its own (it's read-only already) — it
reports Ansible version/config, resolves the actual connection
user/port, waits for SSH, pings, and confirms `become` actually reaches
root. A failure here means don't bother running anything else against
that host yet.

**To audit the general baseline** (read-only, safe):

```
ansible-playbook ansible/configure_rhel.yml --check --diff
```

Summarize per-role: which roles reported no diff (compliant vs. current
variable settings — note several roles do nothing at all until their
variables are set), which showed diffs (drift found, not yet applied), and
which failed a task outright. Remember this only covers the roles in
`configure_rhel_domains` today (see the table above and
`.claude/skills/configure_rhel/SKILL.md`) — roles outside that list are
skipped and report nothing at all, which is different from "compliant."

**To audit one domain**: add `--tags <domain>` to whichever playbook
actually contains that role — e.g.
`ansible-playbook ansible/configure_rhel.yml --tags timesync --check --diff`,
or `ansible-playbook ansible/nfs_client_setup.yml --tags mount_setup --check --diff`
for an NFS client. Check the tables above (or the domain's own `SKILL.md`)
before picking a playbook — running the wrong one either matches no tags
or applies the wrong variables. Against `configure_rhel.yml` specifically,
`--tags` alone isn't enough if the domain isn't in `configure_rhel_domains`
— see `.claude/skills/configure_rhel/SKILL.md`.

**To set up a load balancer or NFS host**: use the matching composite
playbook directly rather than trying to reconstruct its role list against
`configure_rhel.yml`:

```
ansible-playbook ansible/load_balancer_setup.yml --check --diff   # or --tags <domain>
ansible-playbook ansible/nfs_client_setup.yml --check --diff
ansible-playbook ansible/nfs_server_setup.yml --check --diff
```

**To check for or apply pending RHEL updates**:

```
ansible-playbook ansible/update_rhel.yml --check --diff   # reports pending updates only, by default
```

`system_update` (the role that actually applies updates) is commented out
in this playbook by default — see that role's `SKILL.md` before uncommenting
it for a real fleet-wide patch run.

**To remediate**: never run a full playbook without `--check` across all
its domains unless the user has explicitly asked to apply fixes — this
touches auth, boot config, and device policy in one pass (high blast
radius), and several of these roles can act immediately and disruptively
on their own:

- `usbguard_setup` enables and starts enforcement **the moment it
  actually runs** (`policy: reject`, no separate opt-in flag on top of
  being in `configure_rhel_domains`) — see that skill's `SKILL.md` before
  remediating any host with only physical console access.
- `boot_parameters` and `system_locale` both **reboot the host by
  default** (`boot_parameters_reboot` / `system_locale_reboot`) when they
  change something — get explicit confirmation before a real remediate
  run, or pass `-e boot_parameters_reboot=false -e system_locale_reboot=false`.
- `system_init` — now active by default in `configure_rhel.yml` — reboots
  the host as part of a routine, untagged `configure_rhel.yml` run because
  `reboot` is in its default action list. This is a genuine behavior
  change from the old `site.yml`, where this role was excluded entirely;
  flag it clearly.
- `audit_setup` can also reboot the host if
  `audit_setup_update_lock: reboot` is set and the current rules are
  locked.
- `ipv6_setup` **reboots on change with no opt-out flag**.
- `multipath_setup` reboots by default (`multipath_setup_reboot: true`)
  once it's actually included in `configure_rhel_domains` and applies a
  change, rather than reloading `multipathd` in place.
- `scap_compliance` remediates (not just audits) whenever
  `scap_compliance_remediate: true` is set, **regardless of whether
  `--check` is passed**, once it's in `configure_rhel_domains`.
- `system_update`, once uncommented in `update_rhel.yml` (a literal
  commented-out line there, not part of the `configure_rhel_domains`-style
  toggle — see that skill), can update dozens of packages and reboot the
  host per `system_update_reboot_policy`.

Prefer remediating one domain at a time
(`ansible-playbook ansible/<playbook>.yml --tags <domain>`) with the user's
confirmation of what will change, per `docs/ARCHITECTURE.md`.

**To target real hosts**: add them to `ansible/inventory/hosts.ini` (or
pass `-i <path>`); all six playbooks default to `hosts: all`.

**To propose a change spanning multiple roles or more than one playbook**:
this is the one case that doesn't belong to a single domain skill. Same
rules as every domain's "propose a change" workflow apply — never commit
directly, branch as `soe/<short-desc>` (no domain prefix, since it's
cross-cutting), validate locally, push, open a PR titled
`[soe] <what changed>`, then stop for human review. Don't fold a
cross-cutting change into a single domain's PR — see
`docs/ARCHITECTURE.md`'s "Contribution workflow".

## Adding a domain

Follow "Adding a new domain skill" in `docs/ARCHITECTURE.md`, then add a
row to the appropriate table above (general baseline, a composite
playbook, not-wired-in, or deliberately-excluded).
