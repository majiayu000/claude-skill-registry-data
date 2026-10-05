---
name: connect_linux
description: Runs ansible/connect_linux.yml, a read-only pre-flight check that confirms SSH reachability and that `become` actually reaches root on a RHEL-family host, as part of the Linux SOE. Use before running any other SOE playbook against a host that's new, unfamiliar, or suspected of being unreachable/misconfigured, or when asked to "test connectivity" / "check access" to a host.
---

# connect_linux

Runs `ansible/connect_linux.yml`. Unlike every other playbook in this repo,
this one owns no Ansible role under `ansible/roles/` — it's a small,
self-contained set of ad hoc tasks, not a domain skill's deliverable. See
`docs/ARCHITECTURE.md` for the six-playbook layout this fits into.

## Policy & workload awareness

This playbook owns no Ansible role (see above) and makes no
policy-or-workload-driven decisions of its own — connectivity/`become`
checks don't change based on what `docs/POLICY.md` or `docs/WORKLOAD.md`
say. Nothing to re-assess here.

## What the playbook actually does

`hosts: all`, `become: false`, `gather_facts: false` — deliberately
lightweight, since the point is to check access *before* assuming
`become` or fact-gathering will work:

1. Displays Ansible runtime essentials (version, config file, inventory
   sources, playbook Python interpreter, resolved play hosts) — `run_once`,
   so this appears once per play, not once per host.
2. Resolves the actual connection port in use for each host (checking
   `ansible_<connection>_port`, falling back to `ansible_port`, then `22`)
   and displays it along with the resolved connection user, so what's
   about to be attempted is visible before it's attempted.
3. `wait_for` — confirms the resolved host:port is open and speaking
   OpenSSH (`search_regex: OpenSSH`), delegated to `localhost`, 10s timeout.
4. `ansible.builtin.ping` — confirms an actual Ansible connection succeeds
   (not just an open port).
5. `become: true` + `whoami` — confirms privilege escalation actually
   reaches `root`, failing explicitly (`failed_when`) if it doesn't.

Every task here is inherently read-only — there is no separate
audit/remediate split for this playbook the way there is for domain roles.

## What to do

```
ansible-playbook ansible/connect_linux.yml
```

Add `-i <path>` or make sure the target host is in
`ansible/inventory/hosts.ini` first. Run this against a single host with
`-l <hostname>` when checking one host specifically rather than everything
in inventory.

Summarize the result plainly: which host(s) are reachable over SSH, which
resolved to an unexpected user/port (worth flagging even on success — it
usually means an inventory or `ansible_*` variable is set differently than
expected), and — most importantly — whether `become` reached `root`. A
failure at the `wait_for` step means the host is unreachable at the
network level; a failure at the `ping` step means SSH is up but the
Ansible connection itself is failing (wrong user, missing key, etc.); a
failure at the final `whoami` check means SSH access works but sudo/`become`
doesn't — don't proceed to `configure_rhel.yml` or any other playbook
against that host until this is resolved, since every other playbook in
this repo assumes `become: true` will actually work.

**Propose a change to this playbook**: never edit and commit directly. On a
branch named `soe/connect_linux/<short-desc>`, edit
`ansible/connect_linux.yml`, validate locally (`--syntax-check`), push, and
open a PR titled `[connect_linux] <what changed>`. Then stop — a human
reviews and merges; see `docs/ARCHITECTURE.md`'s "Contribution workflow".
Note this playbook has no `ansible/roles/connect_linux/` directory to
change — all its logic lives directly in the playbook file itself.

## Notes

- This playbook has no equivalent under the old `ansible/site.yml` design —
  it's new to the six-playbook layout, specifically to give a fast,
  low-assumption first check before anything role-based is attempted.
- Because `gather_facts: false` and `become: false` are both set at the
  play level, none of the later, `become: true` tasks accidentally run
  with the wrong assumption baked in from a play-level default — each
  privilege-sensitive task escalates explicitly.
