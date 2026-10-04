---
name: synology-dsm
description: >
  Administer Synology DSM NAS over SSH: shares, packages, storage pools, crashed volumes, and btrfs recovery.
license: MIT
compatibility: "Requires SSH access to a Synology NAS running DSM 7, with an admin account for sudo. DSM 6 differences are noted but not covered in depth"
metadata:
  source: iuliandita/skills
  date_added: "2026-07-27"
  effort: high
  argument_hint: "[task-or-host-or-volume]"
---

# Synology DSM: Administration and btrfs Recovery

Operate Synology NAS appliances over SSH: package and service control, storage stack
inspection, snapshots and backups, and recovery of btrfs volumes that will not mount.

DSM is a Linux appliance with a heavily modified btrfs and a userspace that regenerates its own
config. Two facts drive most of this skill: **DSM's btrfs on-disk format is newer than the
btrfs-progs DSM ships and diverges from mainline**, so stock tools report healthy volumes as
corrupt; and **DSM regenerates `/etc/fstab` and package state at boot**, so hand edits do not
survive.

**Target versions** (October 2026):
- DSM 7.4.1-90080 - current release (7.4 GA was 90075, 2026-06-16)
- DSM 7.3 (released 2025-10-08) - Long-Term Support line, maintained to October 2027. Patch
  floor is **7.3.2-86009-4 or above** ([SA-26:13](https://www.synology.com/en-global/security/advisory/Synology_SA_26_13),
  critical, 2026-09-18). `-2` carries the SA-26:06 fixes but not SA-26:03 (CVE-2026-32746);
  `-3` predates SA-26:13
- DSM 7.2 - end of maintenance December 2025, yet it still received fixes in SA-26:06 (April
  2026). Treat continued patching as unreliable rather than as policy, and plan an upgrade
- Advisories: Synology-SA-26:03 (CVE-2026-32746, telnetd buffer overflow, CVSS 9.8, unauthenticated
  RCE - keep Telnet off), Synology-SA-26:06 (multiple DSM CVEs, 2026-04-15), Synology-SA-26:11 (MailPlus Server)
- [SA-26:11](https://www.synology.com/en-global/security/advisory/Synology_SA_26_11):
  critical MailPlus Server CVE-2026-13136 and CVE-2025-15660; fixed in
  4.0.1-31663+ for DSM 7.3 or 4.0.1-21663+ for DSM 7.2.2/7.2.1. Update the
  package separately from DSM; the advisory lists no mitigation.
- [SA-26:03](https://www.synology.com/en-global/security/advisory/Synology_SA_26_03)
  also fixes affected DSM 7.2.2 at 7.2.2-72806-8+ and DSM 7.2.1 at
  7.2.1-69057-11+. These advisory floors do not establish ongoing lifecycle support.

- Userspace `btrfs` on the appliance is old (v4.0 on DSM 7.1 avoton). Check with `btrfs --version`
  before assuming a subcommand exists

DSM 7.1.x and earlier do not appear in current advisories' fixed-version lists; treat them as
unpatched. That is a reason to plan an upgrade, not to run one on a unit with a broken volume.

Verify the actual build before quoting any of this: `cat /etc.defaults/VERSION`.

## When to use

- Any task on a Synology NAS over SSH: shares, packages, services, users, storage pools
- A volume that will not mount, shows "Volume Crashed", or has gone read-only
- btrfs work on a Synology volume, including snapshots, subvolume flags, and offline recovery
- Deciding whether a DSM warning is real damage or a stock-tool false positive
- Planning disk replacement, RAID repair, or a migration between Synology units
- Hardening DSM: SSH, admin accounts, firewall, package exposure

## When NOT to use

- Generic Linux administration on a normal distro - use **debian-ubuntu**, **arch-linux**,
  **rhel-fedora**, **nixos**
- Mainline btrfs on a normal Linux host - Synology's format divergences do not apply there
- Docker Compose authoring, image builds, registry work (Container Manager runs stock Docker) -
  use **docker** for the container content, this skill only for DSM-side paths and permissions
- Router, VLAN, DNS, or reverse proxy design around the NAS - use **networking**
- OPNsense/pfSense appliances - use **opnsense-pfsense**
- Kubernetes storage that happens to point at a Synology CSI target - use **kubernetes**
- Application security review or dependency scanning - use **security-audit**
- Localizing a live outage across an unknown stack - use **debug-triage** first, then come back here
- Proxmox, libvirt, or generic hypervisor work - use **virtualization**

## AI Self-Check

Before returning any DSM command, verify. When no SSH session exists yet - the common case when
answering a question - the appliance-state items convert into the first commands the user runs,
in this order, rather than being skipped:

- [ ] DSM major version confirmed (`cat /etc.defaults/VERSION`) - DSM 6 and DSM 7 differ in
  service control, root login, and available tools
- [ ] No command from the hard-refusal list below
- [ ] Destructive storage operations run against a dm-snapshot overlay, not the live device
- [ ] Any `mount`, `mdadm`, `dmsetup`, or `btrfs` write path stated with its blast radius
- [ ] `cd /` before anything that unmounts `/volume1` (SSH sessions land in the home dir on it)
- [ ] Shell syntax is ash-compatible (`/bin/sh` is ash - no process substitution, no bashisms)
- [ ] Long-running jobs wrapped in `setsid nohup ... < /dev/null &`, not attached to the SSH session
- [ ] Binaries deployed to `/root/` or a package dir, never `/tmp` (`noexec`)
- [ ] Tool presence checked, not assumed - `lsof`, `fuser`, `mountpoint`, `modinfo` are absent
- [ ] Config edits target files DSM does not regenerate, or the regeneration is accounted for
- [ ] Backup or snapshot state verified before any repair, not after
- [ ] **Hidden state identified**: DSM version, model, package dependencies, mounted volumes, and prior repair attempts are made explicit before acting
- [ ] **Verification is real**: checks exercise the actual mount, service, or filesystem rather than reading a DSM banner
- [ ] **Spec claims verified**: claims about DSM behavior are checked against the appliance or Synology's GPL kernel source, not recalled
- [ ] Cross-cutting agent hygiene applied - see `references/agent-hygiene.md`

---

## Hard refusals

These are rules, not suggestions. Each one has destroyed a real volume.

1. **Never run `btrfs check --repair --init-extent-tree` on a Synology volume.** Observed
   behavior: full scan completes, then it writes a zero-entry node into the chunk tree, hits
   `BUG_ON` in `btrfs_try_chunk_alloc`, and leaves the filesystem permanently unmountable
   (`open_ctree failed`). There is no recovery from this short of restore or a data recovery lab.
2. **Never `mount -o clear_cache` on a damaged volume.** Unconditional, because proving the free
   space tree is *not* the damaged structure is exactly what a damaged filesystem prevents.
   Clearing the tree requires freeing its own blocks, which requires the damaged block. The
   transaction aborts during mount and the filesystem then fails `open_ctree` entirely - strictly
   worse than before.
3. **No repair of any kind without a dm-snapshot overlay in place.** One named exception: when
   there is no usable backup, a single read-only mount attempt on the bare origin is permitted
   to reach evacuation, accepting that the mount replays the log tree and is therefore a write.
   Everything after that attempt goes through the overlay. See `references/btrfs-recovery.md`.
4. **Never click "Repair" in DSM on a crashed volume before identifying which layer failed.**
   The banner does not distinguish mdadm degradation from btrfs read-only. Repair at the wrong
   layer writes to every disk in the pool.
5. **Never run `mdadm --assemble --force` or `--create` as a first move on a suspect array.**
   Force-assembly with stale event counts silently picks a wrong parity generation.
6. **Never enable Telnet, including as an SSH workaround.** CVE-2026-32746 is an unauthenticated
   RCE in DSM's telnetd (CVSS 9.8). If SSH is unusable, use the console or DSM's UI.

Confirm with the user before any RAID repair, volume delete, DSM update, disk removal,
package uninstall, or reboot of a production unit. All of these are outward-facing or
irreversible. When running unattended with no one to ask, stop and report what needs approval -
never proceed on a default.

---

## Environment facts

Observed on a DS415+ running DSM 7.1.1 (avoton). The mechanisms hold broadly, but re-check any
row that a decision rests on - `scp -O`, in particular, follows from DSM's SFTP service being
off, which is a toggle rather than a fixed property.

| Fact | Consequence |
|---|---|
| `/tmp` is `noexec` | Deploy binaries to `/root/` or a package dir |
| sftp subsystem disabled | `scp` needs `-O` (legacy protocol) or it fails with `subsystem request failed` |
| User homes live on the data volume (`/volume1/homes/<user>`) | If the volume is down, key auth breaks (`authorized_keys` unreadable) and login prints `Could not chdir to home directory` |
| Every SSH session lands in the home dir | `umount /volume1` fails with "target is busy". Always `cd /` first |
| `/bin/sh` is ash | No bashisms, no process substitution `<(...)` |
| Missing tools | `fuser`, `mountpoint`, `modinfo`, `lsof` absent - read `/proc` directly |
| Present tools | `python3`, `mdadm`, `dmsetup`, `losetup`, `truncate`, `blockdev`, `btrfs`, `systemctl`, `smartctl` |
| Root login | DSM 7 disables direct root SSH. Log in as an admin user and `sudo -i` |
| `/etc/fstab` is regenerated at boot | Hand-edited mount options do not persist |
| `syno_poweroff_task` | Exists on DSM 6, **not** on DSM 7.1+. Stop packages and services individually |
| Defaults live in `/etc.defaults/` | Edits there survive DSM updates better than `/etc/`; both can be overwritten by a major upgrade |

Read `references/dsm-cli.md` for the command reference (packages, services, shares, users,
indexing, logs, SMART, notifications).

---

## Workflow

Copy this checklist and track progress (an unmountable volume follows "Recovery first moves"):

```markdown
- [ ] Step 1: DSM version, build, and platform recorded
- [ ] Step 2: Storage stack read bottom-up (disks, md, LVM, btrfs)
- [ ] Step 3: Symptom routed to the matching reference
- [ ] Step 4: Blast radius and rollback stated before any write
- [ ] Step 5: Result verified on the runtime (on failure, return to Step 2)
```

### Step 1: Identify the appliance before anything else

```sh
cat /etc.defaults/VERSION                  # productversion, buildnumber, majorversion
grep unique /etc.defaults/synoinfo.conf    # platform, e.g. synology_avoton_415+
uname -a                                   # kernel (3.10.x or 4.4.x on most models)
synopkg list --name                        # installed packages
```

Model and build determine which GPL kernel source to read, which btrfs features exist, and
whether DSM 6 or DSM 7 semantics apply. Do not skip this step to save a round trip - almost
every later decision depends on it.

### Step 2: Establish the storage picture

```sh
cat /proc/mdstat                           # all md arrays, degraded state, resync progress
sudo vgs; sudo lvs                         # LVM layer
sudo btrfs filesystem show                 # filesystems and devices
sudo btrfs filesystem usage /volume1       # data vs metadata allocation
df -h /volume1
mount | grep volume                        # actual mount options in force
```

The stack is `/dev/sdX3 -> mdN (RAID) -> vgN/volume_N -> cachedev_N (flashcache shim) -> btrfs`.
`md0` (system, ~8 GB) and `md1` (swap, ~2 GB) are RAID1 across **all** disks and are commonly
found degraded and ignored for months. Check them; repair is a plain `mdadm --add` and an 8 GB
RAID1 resync finishes in under a minute.

Read `references/storage-and-backup.md` for SHR, disk replacement, compatibility database,
snapshots, and backup verification.

### Step 3: Route on symptom

| Symptom | Route |
|---|---|
| Volume mounts, DSM is healthy, routine task | `references/dsm-cli.md` |
| Degraded array, disk replaced, pool repair | `references/storage-and-backup.md` |
| Volume read-only, "Volume Crashed", will not mount | `references/gotchas.md`, then `references/storage-and-backup.md` section 4 **first** - the banner does not say which layer failed. Only once the array and LV are confirmed healthy does it become `references/btrfs-recovery.md` |
| Stock `btrfs` reports corruption but the volume mounts and reads fine | Likely a Synology format divergence, not damage. `references/btrfs-recovery.md`, section on private trees |
| Package keeps restarting after being disabled | Dependency resurrection - `references/dsm-cli.md` |

### Step 4: Change with a stated blast radius

Before any write: state what is affected, whether it is reversible, and what the rollback is.
For storage operations, the rollback is the overlay or a verified backup - nothing else counts.

### Step 5: Verify against the runtime, not the UI

DSM's banners lag reality and its health status is derived. Verify the thing itself:

```sh
mount | grep /volume1                          # actually mounted, and rw or ro?
sudo btrfs filesystem usage /volume1           # metadata headroom
sudo dmesg | tail -100                         # kernel truth about the mount
synopkg status <Pkg>                           # package state as JSON
# damage survey: hours on a large share, so detach it and keep stderr
sudo sh -c 'setsid nohup find /volume1/SHARE -size +0 > /dev/null 2> /root/survey.log < /dev/null &'
```

Replace `SHARE` with the confirmed share path, quoting it inside the elevated shell if needed.
The elevated shell opens the log and detaches the survey; inspect that log for errors.
`find <dir>` alone performs readdir only and reads no inodes, so it reports a badly damaged
filesystem as clean. **`-type f` does not fix that**: `find` answers `-type` from the `d_type`
that `readdir` already returned and skips the `stat` entirely. Use a predicate that needs inode
data - `-size +0`, `-printf '%s\n'`, `-newer <ref>` - and let stderr through instead of
discarding it, since the EIO lines are the finding. If verification fails, return to Step 2.

---

## Recovery first moves

**Establish the goal before the sequence.** With a verified backup, the goal is repair. Without
one, the goal is **evacuation**: get the data off a read-only mount first, and treat repair as a
later, optional problem. Buying destination disks is cheaper than a recovery lab. Ask which
situation the user is in; do not assume.

When a volume will not mount, do these in order. Details in `references/btrfs-recovery.md`;
read `references/gotchas.md` before the first write of any kind.

**The branch that decides the order:** with a verified backup, build the overlay first and run
every mount attempt against it. Without one, take the named exception in hard refusal 3 - one
read-only mount attempt on the bare origin, accepting the log-replay write, because evacuation
beats purity. After that attempt, everything goes through the overlay.

1. **Stop writing.** Do not repair, do not reboot repeatedly, do not let DSM auto-repair. Do not
   update DSM on a unit with a broken volume.
2. **Identify version and platform** (Step 1 above), and confirm the failure is above the RAID
   layer (`references/storage-and-backup.md` section 4).
3. **Try the cheap read-only mount options**, cheapest first, reading `dmesg` after each failure.
   `-o ro,no_quota_tree` alone recovers a common class of Synology mount failure. Note that a
   read-only mount still replays the log tree, which is a write - the reference explains when
   that forces the overlay first.
4. **If a read-only mount succeeds and there is no backup, evacuate now.** Repair decisions get
   easier once the data is elsewhere.
5. **Build a dm-snapshot overlay and fingerprint the origin** before any write attempt. The
   overlay and a mounted origin are mutually exclusive, so this is a branch point, not a step
   that stacks on top of step 3.
6. **Read the GPL kernel source** for the nearest published release family when the cheap options
   fail (the archive carries families such as `7.4-90080`, `7.3-86009`, `7.2-72806`, `7.1.1-42962`,
   not every build; the full list is in `references/btrfs-recovery.md` section 8):
   `https://archive.synology.com/download/ToolChain/Synology%20NAS%20GPL%20Source/<VER>-<BUILD>/`
   Extract `fs/btrfs/` and read `ctree.h`, `disk-io.c`, `super.c`, `usrquota.c`. It converts a
   black box into a documented system, and twenty minutes there beats hours of probing.
7. **Only then** consider offline tools, and only a patched btrfs-progs build, against the overlay.

---

## Packages and services

```sh
synopkg list --name                  # installed packages (no --started on 7.1)
synopkg status <Pkg>                 # JSON status
synopkg stop|start <Pkg>
synopkg enable|disable <Pkg>         # autostart marker in /var/packages/<Pkg>/enabled
systemctl stop pkgctl-<Pkg>.service  # the underlying unit
```

**Package dependencies resurrect packages.** `synopkg disable` is not enough if another
installed package declares the target in `install_dep_packages`:

```sh
grep -h install_dep_packages /var/packages/*/INFO
```

Synology Drive declares SynoFinder, so SynoFinder restarts within a minute of being disabled.
When the goal is "stop indexing this share", use the indexer's own control tool rather than
fighting the package manager - see `references/dsm-cli.md`.

---

## Security

- Keep Telnet disabled (CVE-2026-32746, CVSS 9.8, unauthenticated RCE in DSM's telnetd)
- Disable the default `admin` account; use a named admin with 2FA
- Move SSH off 22 only as noise reduction, not as a control; restrict by firewall rule instead
- Do not expose DSM's web UI directly to the internet. QuickConnect and DDNS both widen exposure;
  prefer a VPN into the LAN
- Patch level matters more than version line: 7.3 LTS with current patches is a supported
  posture, 7.2.1 without them is not
- Snapshots are not backups until they are replicated off the unit. Immutable (WORM) snapshots,
  introduced in DSM 7.2, resist an admin-account compromise; ordinary snapshots do not
- Package exposure is the real attack surface: MailPlus, Photos, and Drive carry most advisories.
  Uninstall what is unused

## Restore drills

Restore representative files and application data to a separate destination, never over live data for a drill. Verify contents, permissions, encryption-key access, and application readability; measure recovery time and data loss against the required RTO/RPO. Record the backup selected, checks, and cleanup. A healthy backup task alone does not prove recovery.

## Performance

- Check `btrfs filesystem usage` metadata headroom before blaming disks. A metadata-full btrfs
  behaves like a failing filesystem while every disk is healthy
- Indexing (`synoindexd`, `synoelasticd`) and Photos face-recognition dominate CPU on small units;
  pause per share rather than disabling packages
- `synoindexd` and snapshot deletion both spike I/O; do not benchmark during either
- SHR/RAID5 resync and btrfs balance are both throughput killers - check `/proc/mdstat` before
  investigating "slow NAS" complaints

---

## Reference Files

- `references/dsm-cli.md` - DSM command surface: packages, services, shares, users, network,
  indexing, logs, notifications, SMART, DSM API. Read for any routine administration task.
- `references/storage-and-backup.md` - SHR and the RAID/LVM/btrfs stack, disk replacement,
  drive compatibility database, snapshots, Hyper Backup, restore verification. Read when the
  task touches disks, pools, snapshots, or backups.
- `references/btrfs-recovery.md` - Synology's btrfs divergences (private root flags, private
  trees, private mount options, the usrquota mount trap), dm-snapshot overlay procedure, mount
  escalation ladder, tool matrix, btrfs-progs bugs, subvolume flag ioctls. Read when a volume
  will not mount or when stock tools report corruption.
- `references/gotchas.md` - footguns, diagnostic hygiene, ash shell traps, behavior of a
  damaged volume. Read before any repair attempt.

## Output Contract

See `references/output-contract.md` for the full contract.

- **Skill name:** SYNOLOGY-DSM
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** an existing
  system (health review, recovery post-mortem, hardening audit), emit the full contract and
  write the deliverable to `docs/local/audits/synology-dsm/<YYYY-MM-DD>-<slug>.md`. When invoked
  to answer a question, run a routine command, or explain behavior, respond freely.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract).

## Related Skills

- **docker** - Container Manager on DSM is stock Docker plus a GUI. That skill owns the compose
  file and image; this one owns `/volume1` paths, DSM permissions, and package lifecycle.
- **networking** - DNS, VPN, reverse proxy, and VLAN work around the NAS. This skill stops at
  the appliance's own interfaces.
- **debug-triage** - localizes an unknown failing layer during a live incident. Use it first when
  "the NAS is down" could be network, power, or storage; this skill takes over once it is DSM.
- **debian-ubuntu** - DSM 7 is Debian-derived, so some package intuitions carry over, but DSM's
  own package manager and config regeneration do not behave like apt.
- **security-audit** - reviews application code and dependencies. This skill covers appliance
  hardening and DSM-specific exposure.
- **virtualization** - Virtual Machine Manager on DSM runs QEMU/KVM underneath; that skill covers
  the guest and hypervisor concepts, this one the DSM package around them.

## Rules

The hard refusals above are rules too; this list adds the constraints they do not cover.

1. **Read Synology's GPL kernel source for the exact build before deep recovery work when it is
   published.** If no exact drop exists, the closest lower published release family may guide
   read-only investigation only; treat every constant and behavior as provisional, do not use it
   to justify a write or repair, and stop for the exact source or recovery-lab advice when it
   disagrees with observed DSM behavior.
2. **Treat mainline-tool corruption reports as unverified.** Synology's private root flags and
   trees are rejected by mainline's tree-checker. Confirm damage against the DSM kernel's own
   behavior before acting on a stock-tool verdict.
3. **Suspect the diagnostic first when it returns nothing.** Empty output on a damaged system is
   usually a broken check, not a clean result.
4. **Snapshots are not backups.** Verify a restore path off the unit before touching storage.
5. **Detach long jobs from a script file, not an inline command,** so `pkill -f` cannot match
   your own shell (`references/dsm-cli.md`).
