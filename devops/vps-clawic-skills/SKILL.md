---
name: VPS
slug: vps
version: 1.0.2
description: 'Runs rented virtual private servers end to end: picking a provider and plan, first boot, snapshots, resizing, IP addresses, and moving between hosts. Use when choosing between Hetzner, DigitalOcean, Vultr, or Linode, when a box is unreachable and it is unclear whether the fault is the provider or the machine, when SSH refuses and the only way in is the web console or rescue mode, when the disk filled, the plan has to change, or a snapshot has to be restored, when a firewall rule looks correct but is ignored, when the provider sends an abuse notice or suspends the server, when outbound mail is rejected or blacklisted, or when bandwidth overage or IPv4 charges make the bill jump. Covers provider firewalls, private networking, and restorable backups. Not for Linux internals (`linux`), container runtime problems (`docker`), reverse-proxy/TLS configuration (`nginx`), DNS record design (`dns`), or managed platforms with no server to administer (`hosting`).'
homepage: https://clawic.com/skills/vps
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🖧
    os:
    - linux
    - darwin
    - win32
    displayName: VPS
    configPaths:
    - ~/Clawic/data/vps/
    - ~/Clawic/data/servers/
    - ~/Clawic/data/domains/
    - ~/Clawic/data/finances/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/vps/
      - ~/Clawic/data/servers/
      - ~/Clawic/data/domains/
      - ~/Clawic/data/finances/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/vps/config.yaml` (what the user declared) and `~/Clawic/data/vps/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file that `## Boxes` names when the condition written on its line applies — that index *is* the list of files; never work from a fixed list of names, because most boxes get created after this skill was written. Read `~/Clawic/data/servers/servers.md` before any sizing, cost, access, or "what do I have" question. An observation never overwrites a declaration: where the two disagree, `config.yaml` wins and the observation is recorded as an observation. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a host created, rebuilt, resized, discovered, or destroyed; a port opened or closed; a provider account and how it is paid; a snapshot policy; a restore that was actually timed; a spend number; or something the user will want to read again — a recovery runbook, a cutover plan, the reason one provider was chosen over another. `memory-template.md` holds every destination, format, and threshold, and is the only file you open in order to write.

**Hosts go to the shared inventory `~/Clawic/data/servers/servers.md`**, not into this skill's folder: the same file holds machines from every provider, so "what servers do I have" answers itself whoever created them. One row per host, identified by `Name` + `Provider` — read the file first and update your own row in place, never append a second one. VPS-only attributes that inventory has no column for (image, snapshot policy, private-network membership, what it serves) go to `## Hosts` in `memory.md`, keyed by the same `Name`.

**A domain that points at a host** goes to the shared `~/Clawic/data/domains/domains.md` — registrar, expiry, and where it points — because a migration is a DNS operation as much as a server one, and the TTL is what sets the cutover window.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `file:~/.ssh/id_ed25519`, `keychain:hetzner-api`, `1password:Infra/root-password`, `env:RESTIC_PASSWORD`.

A VPS is a machine someone rents you and can take away. Two things decide every outcome: whether you can get back in when SSH stops working, and whether the data exists somewhere the provider account cannot reach. Everything else is tuning. Quote the monthly price with its currency, say what happens if the box dies tonight, and prefer a cheaper plan plus a rebuild script over a bigger plan. Work from defaults immediately: never open with questions about their provider, their budget, or their distro. The one exception to silence is `provider` — while it is unset, name which provider's console and plan names you are assuming before giving steps (Rule 8). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale, country) → the Configuration table default.

## When To Use

- Choosing a provider, region, and plan, and sizing the first box — or its replacement
- Taking a rented server from first boot to something you would point a domain at
- Locked out or unreachable: SSH refuses, the web console is the only way in, the provider suspended the server or sent an abuse notice
- Operating what is already live: disk filling, snapshots and restores, resizes, kernel reboots, IP changes, bandwidth overage, outbound mail rejection
- Moving a live server to another provider, or shutting one down without leaving billable pieces behind
- Not for Linux internals and systemd debugging (`linux`), container runtime problems (`docker`), reverse-proxy and TLS configuration (`nginx`), DNS record design (`dns`), or managed platforms where there is no server to administer (`hosting`) — this covers the rented-machine side of all five

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "Which provider and how big?" | Price the binding constraint (usually RAM), then compare egress allowance and IPv4 charge, never vCPU count | `choosing.md` |
| Provider-specific quirk, or "is Contabo fine?" | The per-provider table: what each one is genuinely good and bad at | `providers.md` |
| Fresh box, nothing done yet | The First Hour in the exact order below — the order is what prevents lockout | `provisioning.md` |
| SSH refuses, hangs, or the key stopped working | Classify first: refused (nothing listening / firewall), timeout (routing / provider firewall), or auth (key, permissions, config) | `access.md` |
| Locked out completely | Web console → rescue mode → mount and chroot; never rebuild before reading the disk | `access.md` |
| A firewall rule that looks right is ignored | Which layer is deciding — provider firewall, nftables/ufw, or Docker's own chain | `firewall.md` |
| Abuse notice, suspension, or the box is sending traffic you did not ask for | Assume compromise, take it off the network first, respond inside the provider's window | `security.md` |
| Backups, snapshots, "am I covered?" | 3-2-1 with one copy the provider account cannot delete, then time a real restore | `backups.md` |
| Disk full, out of memory, load high, box crawling | The four killers, in the order they actually occur: disk, inodes, memory, steal time | `operations.md` |
| IPv6, private networking, floating IPs, reverse DNS | Address plan, what the private network does and does not protect, PTR rules | `networking.md` |
| Mail from the server is rejected or lands in spam | Port 25 policy, PTR/HELO match, IP reputation — usually the answer is a relay | `email.md` |
| Too small, too big, or "do I need a second server?" | Vertical first, and the disk-is-a-one-way-door rule; horizontal only for isolation or availability | `resizing.md` |
| Moving to another provider, or shutting a server down | The cutover choreography and the teardown list that stops the billing | `migration.md` |
| Box unreachable and nothing changed | Split the fault: provider status, network path, then the machine | `incidents.md` |
| Bill went up, or spend has to come down | The five line items that are not the server price | `costs.md` |
| What to actually run on the box and how to lay it out | One box, several sites, containers or not, panel or not, isolation model | `hosting.md` |
| Anything else about a rented server | Answer directly, then state the monthly cost with currency and what happens if this box dies tonight | — |

Coverage map: `choosing.md` provider and plan selection · `providers.md` per-provider quirks · `provisioning.md` first boot to production · `access.md` SSH and lockout recovery · `firewall.md` the two filtering layers · `security.md` exposure, intrusion, abuse · `backups.md` snapshots and restores · `operations.md` day-to-day and the four killers · `networking.md` addresses and private links · `email.md` outbound mail · `resizing.md` scaling decisions · `migration.md` provider moves and teardown · `incidents.md` the box is down · `costs.md` the bill · `hosting.md` what runs on it.

## Core Rules

1. **A second way in exists before you change the first one.** Before disabling password login, moving the SSH port, or enabling a firewall: confirm the fallback works — provider web console (VNC or serial), a second authorized key, or rescue mode. Then keep the current session open and prove the change from a *new* session; only close the first once the new one works. Every VPS lockout story is one session and one confident edit.
2. **The provider account is the real root.** Whoever holds that login can rebuild the machine, mount its disk in rescue mode, and delete every snapshot — none of which SSH hardening touches. 2FA on the provider login, API tokens scoped to what they need and rotated, recovery codes stored offline. A hardened box under an unprotected provider account is theatre.
3. **Two firewalls, and they do not see the same packets.** The provider firewall filters before traffic reaches the machine and keeps working when the machine does not; the host firewall is the one a container runtime walks around. Default-deny inbound at both. `ufw deny 5432` does **not** close a Docker-published 5432, because the runtime inserts its rules ahead of ufw's chain — publish container ports to `127.0.0.1` and let a reverse proxy be the only public listener (`firewall.md`).
4. **A snapshot in the same account is not a backup.** 3-2-1: three copies, two media, one offsite — and for a rented server "offsite" means *restorable with the provider account gone*, because the credential that deletes the server deletes its snapshots in the same click. Time a real restore quarterly (`## Due`); an untimed backup has an unknown recovery time, which is the same as an unknown outage length.
5. **Size from the binding constraint, and treat disk as a one-way door.** RAM is the constraint for almost every web workload, not vCPU count. CPU and RAM resizes are reversible on most providers; **disk growth is not** — once grown you cannot shrink back, so the size you grow into becomes the floor of the bill forever. Start one step below your guess: stepping up costs a reboot of a few minutes, stepping down costs a migration.
6. **After an unknown party had root, rebuild — never clean.** A rootkit, a modified `sshd`, a cron entry you did not find: the only trustworthy state is a fresh image plus data restored from a backup that predates the intrusion. Copy out data, not binaries or configs. Cleaning a compromised box means you now run a machine whose integrity you are guessing at.
7. **The build of the box lives in a file, not in your shell history.** Cloud-init user-data or a single provisioning script, kept with the project. The measure: if you cannot recreate this host from scratch in under 30 minutes, you own a pet, and your worst-case outage is exactly as long as the manual rebuild you have never rehearsed. Cattle is not a scale requirement — it is what makes Rule 6 cheap enough to actually do.
8. **Every price names its provider and its currency.** Identical specs vary roughly 2-4× between budget European hosts and US-based clouds, and the gap widens once egress and IPv4 are counted. "About $20 a month" without a provider is not a number. When `provider` is unset, say which one you are assuming before quoting anything.

## The First Hour

The order is the content: three of these steps can lock you out if done early, and two are irreversible later.

1. Create the box with the SSH key **injected at creation** — never with a root password emailed to you.
2. Confirm the fallback path (console access, or rescue mode) *before* touching anything.
3. Update every package; a stock image is typically weeks to months behind on security fixes.
4. Create the non-root admin user with sudo, and copy the key to it. Log in as that user in a second session.
5. Set hostname, timezone (UTC unless the user declared otherwise), and locale — before logs start accumulating in a timezone you will misread.
6. Swap or zram on anything under 4 GB: without it, one build step OOM-kills the database instead of paging.
7. Host firewall: allow SSH **first**, then enable default-deny inbound.
8. Provider firewall: same policy, one layer out.
9. Disable password authentication and root SSH login, from the second session, with the first still open.
10. Automatic security updates on, with a stated reboot policy (`operations.md`) — unattended upgrades that never reboot leave the kernel unpatched and are the most common false sense of safety.
11. Backups configured and one restore tested before the box carries anything real (Rule 4).
12. Write it down: the host row in `servers.md`, its VPS-only attributes in `## Hosts`, and the provisioning script wherever the project lives.

## Failure Signatures

Decode rule: the *shape* of the failure names the layer. Refused means something answered; timeout means nothing did; auth means you reached the right daemon and it said no.

| Signature | Most likely cause | First move |
|---|---|---|
| `Connection refused` on SSH | sshd is down or listening on another port — the packet reached the host | Web console → check the service and the port it bound |
| `Connection timed out` on SSH | Provider firewall, host firewall, or the box is not on the network | Provider firewall first (it is invisible from inside the box) |
| `Permission denied (publickey)` | Wrong key, wrong user, or home/`.ssh` permissions too open | Key perms 600 and `.ssh` 700, then the daemon's log — the reason is written there |
| Worked yesterday, refuses today, nothing changed | Fail2ban banned your own address, or the IP allowlist has your new dynamic IP | Console in and check the ban list before re-editing config |
| Firewall rule added, port still open | A container runtime published the port ahead of the host firewall | Bind the publish to `127.0.0.1`, or filter at the provider layer (`firewall.md`) |
| Box responds to ping, all services down | Disk full or read-only root filesystem | Console: filesystem usage and inode usage; a full disk fails writes silently for hours first |
| Everything slow, CPU shows idle | Steal time — the hypervisor is giving your cycles elsewhere | Sustained steal above ~5% on a shared plan is a noisy-neighbor problem; migrate the instance or move to dedicated vCPU |
| OOM killer took the wrong process | No swap, and the largest resident process is not the guilty one | Swap or zram, then per-service memory limits (`operations.md`) |
| Boot fails after adding a mount | A bad `/etc/fstab` entry stops boot dead | Rescue mode, add `nofail` to non-root mounts — this is why step 2 of the First Hour exists |
| Provider suspended the server | Outbound abuse: spam, scanning, or an open relay | Assume compromise, isolate, respond inside the window (`security.md`) |
| Mail rejected, or silently spam-foldered | Port 25 blocked by policy, or PTR does not match HELO, or the recycled IP is blacklisted | Check reputation of that address before doing any DNS work (`email.md`) |
| Bandwidth bill spiked with flat traffic | Backups egressing to another region, or a scraper | Overage is billed on the total, not the peak — find the direction and destination first (`costs.md`) |
| Anything else | Split provider-side from machine-side before debugging either | `incidents.md` |

## What The Bill Is Actually Made Of

The plan price is rarely the whole bill. Ratios below are stable; absolute prices move, so verify on the provider's page before committing money.

| Line item | Why it bites | Do instead |
|---|---|---|
| Egress / bandwidth overage | Allowances differ by more than an order of magnitude — a budget European host may include 20 TB while a US cloud meters from the first gigabyte | Compare included transfer *and* the overage rate before the plan price; serve heavy assets from object storage or a CDN |
| Dedicated IPv4 | Almost every provider now charges for it separately, attached or not, since address scarcity started being priced in 2024 | Count them; release addresses on destroyed servers, and use IPv6 plus a proxy where the client base allows it |
| Snapshots and the backup add-on | Snapshots bill per GB of disk *size*, and the managed backup add-on is commonly a flat ~20% of the plan price | Keep a retention count, not "keep everything"; prune on a cadence in `## Due` |
| Stopped servers | On most providers a powered-off instance still bills for its disk and its reserved address — "stopped" is not "free" | Snapshot and destroy, or accept it is a parked cost and write it down |
| Servers nobody owns | A box created for a two-week experiment two years ago is the single most common finding of a spend review | Every host has an `Owner` in `servers.md`; anything unowned is a candidate for teardown |
| Annual prepay taken too early | Discounts are typically modest for VPS and lock you to a provider whose prices tend to fall | Right-size first, run two months, then commit only for a workload that is not moving |

## Provider Shortlist

Compact orientation; the full per-provider table, including console paths and known gotchas, is in `providers.md`. Verify current plans and prices before quoting.

| Need | Reach for | Because |
|---|---|---|
| Cheapest solid RAM per unit of money, EU users | Hetzner | Best price/RAM ratio of the mainstream hosts, large included traffic; EU/US locations only |
| Simplest operations, best docs, US-centric | DigitalOcean | Predictable pricing, wide tutorial coverage, an ecosystem of managed add-ons when you outgrow the box |
| Many small regions worldwide | Vultr or Linode | Latency to a specific city usually beats the specs argument (Rule: place by user latency) |
| Very cheap bulk resources, tolerant workload | Contabo | Large specs per euro, but oversubscribed and slow support — never for something with a revenue number attached |
| Existing cloud account, small predictable box | Lightsail or an equivalent | Fixed-price VPS inside the cloud account you already control, at the cost of that cloud's egress rates |
| European jurisdiction, data residency stated | Scaleway, OVH, Hetzner | The requirement is contractual, not technical — check where the *legal entity* sits, not just the datacenter |
| Free tier for a hobby box | Always-free ARM tiers | Genuinely free and genuinely reclaimable — never for anything you would miss |
| Undecided | The one whose console the user can already log into | The recovery path you have used before beats a datasheet |

## Output Gates

Before delivering a plan, a command, or a recommendation:

- Did I state the monthly cost with its currency and its provider?
- If this change touches SSH, the firewall, or the network: did I name the fallback path and instruct proving it from a second session (Rule 1)?
- Did I say what happens to the data if this box disappears tonight, and is that answer a restore that has been timed?
- Is anything irreversible here — disk growth, image rebuild, address release, snapshot deletion — flagged as irreversible before the step, not after?
- Is any destructive command shipped with its own confirmation step, never inside a copy-paste block of read-only ones?
- Did I write what changed: the host row in `servers.md`, VPS-only facts in `## Hosts`, the event in `changes/<year>.md`, and any runbook or decision in `artifacts/`?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/vps/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| provider | text (provider name) | none | Which console paths, plan names, firewall model, and quirks every step assumes (`providers.md`); while unset, name the assumption out loud (Rule 8) |
| default_distro | debian \| ubuntu-lts \| rocky \| alma \| alpine \| arch | debian | Image chosen at creation and the package-manager syntax in every example |
| cpu_arch | arm64 \| x86_64 \| either | either | Plan shortlist in `choosing.md`; `arm64` forces the binary-compatibility check before any recommendation |
| monthly_budget | number (currency from profile) | 20 | The bar for calling a plan expensive in `choosing.md` and the trigger threshold for a spend review in `costs.md` |
| admin_user | text (username) | none | The non-root account named in provisioning and access steps; unset means examples use `admin` as a placeholder |
| ssh_port | number (1-65535) | 22 | Port used in access, firewall, and provisioning guidance |
| firewall_layer | provider \| host \| both | both | Which of the two layers `firewall.md` configures, and which one an audit checks |
| backup_target | provider-snapshots \| object-storage \| own-host \| none | provider-snapshots | Where `backups.md` sends data, and what the quarterly restore drill actually exercises |
| patch_window | text (weekday + hour, or `anytime`) | anytime | When `operations.md` schedules reboots for kernel updates and how overdue reboots are reported |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — firewall front-end (ufw, firewalld, raw nftables, provider-only), backup tool (restic, borg, rsync, provider), provisioning method (cloud-init, Ansible, a shell script, by hand) — affects every procedure's concrete syntax
- **Conventions** — hostname scheme, private address plan, where projects live on disk, tag and label names in the provider console — affects `provisioning.md` and the inventory rows
- **Platform** — preferred region and its distance to users, IPv6 posture, dedicated versus shared vCPU as the default plan family — affects `choosing.md` and `networking.md`
- **Safety posture** — whether destructive commands are emitted at all, confirmation before rebuild, resize, or address release, deletion protection where the provider offers it — affects Output Gates and `migration.md`
- **Isolation model** — one box per project versus many projects per box, containers versus system services versus a control panel — affects `hosting.md` and the sizing math
- **Data residency and compliance** — jurisdictions that are acceptable, providers that are not, log retention obligations — filters the provider shortlist before price is considered
- **Cost reporting** — review cadence, currency for quotes, whether every answer carries a monthly number — affects `costs.md` and the `## Due` table

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Hardening SSH from a single session | The edit that breaks sshd also removes your ability to fix it, and the console is exactly what nobody set up | Second session, fallback proven first (Rule 1) |
| Moving SSH off port 22 counted as security | It removes untargeted bot noise from your logs and stops zero targeted attacks; it also breaks tooling that assumes 22 | Keys only, no password auth, and rate limiting; change the port for log hygiene if you want, not for safety |
| Provider snapshots treated as backups | They live in the account that can delete them, cannot be restored anywhere else, and are billed per GB of disk size | 3-2-1 with one copy outside the provider account (Rule 4) |
| "Nobody knows this IP" | The entire address space is scanned continuously; a new box gets its first credential attempt within minutes of booting | Default-deny inbound at both layers before the first service goes up |
| Databases bound to `0.0.0.0` behind a firewall | One container publish or one firewall reload and it is public — this is how most open database dumps happen | Bind to localhost or the private interface, then also filter (`firewall.md`) |
| Unattended upgrades with no reboot policy | Security patches install, the running kernel and loaded libraries stay old, and the dashboard says green | A stated reboot policy and a `## Due` line; check the reboot-required marker (`operations.md`) |
| Oversizing on day one "to be safe" | You pay the premium every month and never learn the actual constraint; the disk you grew into cannot shrink | Start one step below the guess, watch two weeks, step up (Rule 5) |
| Restoring for the first time during the incident | Restores fail on details nobody wrote down: encryption passphrase, database version mismatch, missing config outside the data directory | Timed restore drill on a scratch box quarterly, with the gaps written into the runbook |
| Cleaning a compromised server | You are trusting binaries an attacker had write access to | Rebuild from a fresh image, restore data from before the intrusion (Rule 6) |
| Running mail from a fresh VPS address | Port 25 is blocked by default on most providers, and recycled addresses often carry an existing blacklist | Check reputation and PTR before building anything; use a relay for anything transactional (`email.md`) |
| Migrating by changing DNS first | Traffic splits across two servers for the length of the old TTL, and writes land on both | Lower the TTL days ahead, then cut over, then raise it (`migration.md`) |
| Destroying a server without a teardown pass | Reserved addresses, volumes, snapshots, and load balancers keep billing after the instance is gone | The teardown list in `migration.md`, then delete the row from `servers.md` and note the date |

## Where Experts Disagree

- **One big box versus several small ones.** Several small boxes buy isolation and blast-radius control at the cost of a fixed per-box overhead (address, backup add-on, patching, and your attention) that is easy to underestimate. Frontier: below roughly three services, one box and good backups usually wins; the moment two services have different uptime expectations or different owners, split them.
- **Containers on a VPS, or system services.** Containers make Rule 7 nearly free and pin dependency versions; they also add a networking layer that walks around the host firewall (Rule 3) and a disk-consumption pattern that surprises people. Frontier: multiple apps or an unfamiliar stack → containers; a single well-understood service on a small box → system services and less to know.
- **Control panels.** They make routine hosting tasks tractable for a non-specialist and are a large privileged attack surface that expects to own the machine's configuration. Frontier: a human who will not be reading logs → panel; anything you will automate → no panel, because the panel will fight your config management.
- **Budget hosts.** Very cheap providers are excellent for build agents, mirrors, and experiments, and reliably disappointing when support or IO consistency matters. The frontier is not price, it is whether there is a revenue number attached to the box.
- **Firewall placement.** One school does everything at the provider layer (survives a broken host, no per-distro syntax); the other does everything on the host (versionable, travels with a migration). Both fail alone: the provider layer cannot see container-published ports, and the host layer cannot help when the host is unreachable. Default to both (Rule 3), and if only one is possible, keep the provider layer.

## Security & Privacy

**Credentials:** this skill works with SSH and provider consoles. It does NOT store, log, copy, or transmit private keys, passphrases, root passwords, or provider API tokens, and never writes any of them into `~/Clawic/data/`. Only pointers are stored, in the form `file:~/.ssh/id_ed25519` or `keychain:<entry>`.

**Local storage:** host inventory, provider accounts, exposure map, spend history, and runbooks stay in `~/Clawic/data/vps/` and the shared boxes on this machine — hostnames, addresses, plan names, and prices only.

**Guardrails:** commands are read-only by default. Anything destructive or irreversible — rebuild, destroy, disk growth, address release, snapshot deletion, firewall enable — is presented with its blast radius and its fallback path, and requires explicit confirmation before running.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/vps (install if the user confirms):
- `linux` — what to do once you are on the box: systemd, permissions, disks, boot failures
- `docker` — container runtime problems, images, and Compose stacks running on the server
- `nginx` — reverse proxy, virtual hosts, and TLS termination in front of your services
- `dns` — record design and propagation, which the migration cutover depends on
- `monitoring` — metrics, logs, and alerting once one server becomes several

## Feedback

- If useful, star it: https://clawic.com/skills/vps
- Latest version: https://clawic.com/skills/vps

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/vps.
