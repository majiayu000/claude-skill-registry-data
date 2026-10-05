---
name: configure_rhel
description: Runs ansible/configure_rhel.yml, the general RHEL host baseline, letting the user choose which of its 43 domains actually apply for a given run via the configure_rhel_domains variable — without editing the playbook. Use whenever someone wants to audit/remediate "the baseline" with a non-default set of domains, wants to know what's on/off by default, or asks to enable something like usbguard, accounts_local, cron, etc. that isn't active out of the box.
---

# configure_rhel

Runs `ansible/configure_rhel.yml` — the general host baseline playbook (see
`.claude/skills/soe/SKILL.md` and `docs/ARCHITECTURE.md` for how it fits
into the six-playbook layout). This skill is specifically about
**controlling which of its domains apply for a given run.**

## Policy & workload awareness

Each of this playbook's domains carries its own policy/workload staleness
check in its own `SKILL.md` (see `docs/ARCHITECTURE.md`'s "Policy &
workload awareness"). When running a broad `configure_rhel` pass across
many domains at once, prefer `soe`'s repo-wide scan
(`.claude/skills/soe/SKILL.md`) over checking each domain one at a time.
This playbook's own file, and `configure_rhel_domains`'s default list
specifically, can itself need a change when a new workload or policy item
implies a domain should move from off-by-default to on-by-default (or vice
versa) — that's a change to `ansible/configure_rhel.yml` itself, not to any
one role, so it follows the "cross-cutting change" path in
`docs/ARCHITECTURE.md`'s contribution workflow, not a single-domain branch.

## The mechanism

Every one of the 43 in-repo roles this playbook can run is listed as:

```yaml
- role: <name>
  tags: ["<name>"]
  when: "'<name>' in configure_rhel_domains"
```

`configure_rhel_domains` is a single list variable, defined once near the
top of the playbook's `vars:` block. A role's tasks are only considered at
all if its name is in that list — this is the actual on/off switch, not a
comment to remove. `--tags`/`--skip-tags` still work as a *second*,
independent filter on top: a role only runs if it's in
`configure_rhel_domains` **and** matches the requested tags (both are
verified separately, ANDed — confirmed by testing, not just by reading the
YAML). `--tags <domain>` alone, without `<domain>` also being in
`configure_rhel_domains`, does nothing.

**Default value** — reproduces exactly what this playbook applied before
this variable existed:

```
ipv6_setup, etc_hosts, guest_agent, resolver_configuration, timesync,
packages_remove, boot_parameters, system_locale, audit_setup, certificates,
firewall, watchdog, packages_install, performance_tuning, root_password,
security_hardening, sebooleans, service_state, sshd_configuration,
system_init
```

**Available, off by default** — in the `roles:` list, fully functional,
just not in the default `configure_rhel_domains` value:

```
system_hostname, repository_setup, dns_cache, timezone, system_keyboard,
multipath_setup, system_update_report_pre, system_update, accounts_policy,
accounts_local, domain_ad, ima_evm_setup, motd_issue, mount_setup,
rescue_image, packages_verify, shell_profile, troubleshooting_tools,
usbguard_setup, splunk_forwarder, system_coredump, scap_compliance,
cron_setup
```

That's 43 total. See each domain's own `SKILL.md` for what it actually
does — this skill is about turning them on/off, not what each one enforces.

**Not covered by `configure_rhel_domains` at all** (stays commented-out in
the file regardless, needs a direct edit — not a `-e` flag — to ever use):
a handful of `redhat.rhel_system_roles.*`/`community.general.*` entries
interleaved in the `roles:` list (external collection roles, not part of
this repo's own `ansible/roles/`), and one stale reference to `ipaclient`,
which was never an actual role in this repo (no `ansible/roles/ipaclient/`
exists) — don't treat it as a real, selectable domain.

**`-e` replaces the list, it does not merge into it.** To add
`usbguard_setup` to an otherwise-normal baseline run, pass the full 21-item
default list *plus* `usbguard_setup` — not just `["usbguard_setup"]` on its
own (that would run **only** `usbguard_setup` and skip everything else).

**Some domains also gate themselves internally**, independent of
`configure_rhel_domains` — e.g. `shell_profile`'s task still no-ops unless
`shell_profile_file` is set, `packages_verify` still no-ops unless
`packages_verify_enable: true`. Being in `configure_rhel_domains` gets a
role a chance to run; it doesn't override that role's own "do nothing
until configured" defaults. Check the domain's own `SKILL.md`/
`defaults/main.yml` for what else needs setting.

## What to do

**Figure out what the user actually wants applied.** In a live
conversation, this is a good fit for `ask_user_input_v0` rather than
asking the user to hand-write a domain list — e.g. present the 23
available-but-off domains (grouped sensibly: accounts/auth
(`accounts_local`, `accounts_policy`, `domain_ad`), naming/discovery
(`system_hostname`, `dns_cache`, `timezone`, `system_keyboard`),
compliance/hardening (`usbguard_setup`, `ima_evm_setup`, `scap_compliance`,
`packages_verify`), housekeeping (`repository_setup`, `motd_issue`,
`shell_profile`, `cron_setup`, `rescue_image`, `system_coredump`,
`troubleshooting_tools`), storage (`multipath_setup`, `mount_setup`),
updates (`system_update_report_pre`, `system_update`), and
`splunk_forwarder`) and ask which to add to the default 20. On the CLI
with no interactive elicitation available, ask directly in plain text
instead.

**Audit** (read-only, safe to run any time) — default domains:

```
ansible-playbook ansible/configure_rhel.yml --check --diff
```

**Audit with a custom domain selection** — pass the full list (default
20 plus whatever's being added/removed):

```
ansible-playbook ansible/configure_rhel.yml --check --diff \
  -e '{"configure_rhel_domains": ["ipv6_setup","etc_hosts","guest_agent","resolver_configuration","timesync","packages_remove","boot_parameters","system_locale","audit_setup","certificates","firewall","watchdog","packages_install","performance_tuning","root_password","security_hardening","sebooleans","service_state","sshd_configuration","system_init","usbguard_setup"]}'
```

(That example adds `usbguard_setup` to the default set. Swap in whatever
the user actually chose. Removing a normally-active domain for one run
works the same way — leave it out of the list, or use `--skip-tags`
instead if that's clearer for a one-off exclusion without touching the
variable at all.)

**Audit one domain** regardless of whether it's in the default set —
combine `--tags` with a domain list that includes it:

```
ansible-playbook ansible/configure_rhel.yml --tags usbguard_setup --check --diff \
  -e '{"configure_rhel_domains": ["usbguard_setup"]}'
```

(Here it's fine for the `configure_rhel_domains` list to contain *only*
the one domain being audited — `--tags` is already restricting to it, so
the other defaults being absent from the list doesn't additionally narrow
anything.)

**Remediate**: same commands without `--check`, only after the user has
seen the diff and explicitly confirmed. Before remediating with a
newly-added domain, check that domain's own `SKILL.md` for anything that
needs deliberate confirmation first — several of the available-but-off
domains are exactly the ones this repo is most cautious about:

- `usbguard_setup` enables and starts USB enforcement (`policy: reject`)
  the moment it actually runs — confirm the host has console/physical
  access as a fallback, or a reviewed HID allow rule, before remediating.
- `accounts_local` can delete users/groups (including home directories)
  if `accounts_local_users_delete`/`accounts_local_groups_delete` are set.
- `system_update` can update dozens of packages and reboot the host.
- `multipath_setup` reboots by default once it actually applies a change.
- `scap_compliance` remediates (not just audits) whenever
  `scap_compliance_remediate: true` is set, regardless of `--check`.

See each domain's own `SKILL.md` for the full safety detail — this skill
only decides *whether* a domain runs, not what it does once it does.

**Propose a change to the default `configure_rhel_domains` list itself**
(e.g. "usbguard should just be on by default for all hosts now") — that's
a persistent, cross-cutting change, not a one-off `-e` flag. Follow the
same branch + PR workflow as any other change: branch
`soe/configure_rhel/<short-desc>`, edit the default list in
`ansible/configure_rhel.yml`, validate locally, push, open a PR titled
`[configure_rhel] <what changed>`, then stop for human review — see
`docs/ARCHITECTURE.md`'s "Contribution workflow". Don't make this change
unilaterally just because a user asked for one run with a domain enabled;
a single `-e` flag for that run is the right scope unless they explicitly
ask for the default to change.

## Notes

- This mechanism is specific to `configure_rhel.yml`. The other five
  playbooks (`connect_linux.yml`, `load_balancer_setup.yml`,
  `nfs_client_setup.yml`, `nfs_server_setup.yml`, `update_rhel.yml`) are
  each already scoped to one purpose and don't have (or need) an
  equivalent domain-selection variable — see their own `SKILL.md`s.
- `--tags`/`--skip-tags` against `configure_rhel.yml` now work correctly
  for every domain, including ones outside the default
  `configure_rhel_domains` value (as long as the domain list is set to
  include them too — see above). This was verified directly: previously,
  bare role names in the `roles:` list had no implicit tag matching their
  own name, so `--tags <domain>` silently matched nothing for *any*
  domain — a pre-existing bug across this repo's docs, fixed as part of
  adding this toggle (every entry now carries an explicit
  `tags: ["<name>"]`). The same fix was applied to
  `load_balancer_setup.yml`, `nfs_client_setup.yml`,
  `nfs_server_setup.yml`, and `update_rhel.yml` for the same reason.
