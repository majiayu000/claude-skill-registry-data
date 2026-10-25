---
name: cachyos"
description: Maintain and diagnose CachyOS-specific optimized repositories, kernels, chwd hardware profiles, sched-ext scheduling, and packaged system settings. Use for these components on CachyOS or an explicitly configured Arch host, not generic Arch administration or every desktop edit.
---

# CachyOS system work

Establish the actual distribution and installed CachyOS components. Read
`/etc/os-release`, kernel identity, configured pacman repositories, and relevant
package versions. A CachyOS kernel on Arch does not prove the full distribution is
installed. A CachyOS desktop does not imply Omarchy.

Keep [arch-linux](../arch-linux/SKILL.md) for generic package/configuration ownership
and [arch-update-recovery](../arch-update-recovery/SKILL.md) for transactions and
boot recovery. Add this skill's evidence only where CachyOS changes the decision.
Preserve the current task and existing authority through those handoffs.

## Repositories and CPU compatibility

Compare `/etc/pacman.conf` and its included mirror files with the installed
repository packages and current [optimized repository guidance](https://wiki.cachyos.org/features/optimized_repos/).
Inspect CPU features exposed to the actual host or VM before selecting an ISA tier.
Do not infer support from a marketing CPU name or copy another machine's v3/v4/Zen
repository configuration. Repository order determines package selection.

Keep signatures, keyrings, and distribution priority intact. Installing CachyOS
repositories on another distribution is a repository migration, not an incidental
performance fix. Do not run an online repository-conversion script for diagnosis.

## Hardware and kernel changes

Read [hardware profiles](https://wiki.cachyos.org/features/chwd/chwd/) and inspect
the installed `chwd --help` before choosing flags. List relevant hardware and
profiles first. Auto-configuration and profile install/remove operations change
packages and drivers; they are not diagnostic commands.

For a kernel or GPU change, match the running and installed kernels, headers,
module packages or DKMS state, firmware, boot entries, and Secure Boot requirements.
Use the installed kernel manager's supported interface, checking current
[kernel-manager guidance](https://wiki.cachyos.org/features/kernel_manager/).
Keep a known-working boot option until the replacement actually boots and exercises
the device. Do not promise recovery from a package build or module file alone.

## Tuning and packaged defaults

Read [settings and tuning](references/settings-and-tuning.md) when changing
sched-ext, power policy, sysctl, udev, or game-specific wrappers. Inspect the
current effective value and its owner before proposing an override. Package
defaults are a baseline, not proof that a change helps this workload.

For each experiment, change one relevant policy, hold workload conditions steady,
and compare latency/throughput plus heat, power, and stability where relevant.
Restore the baseline if the evidence does not support the change. Do not install
another scheduler manager or replace a desktop merely to try a setting.

## Verification and handoff

For authorized changes, record the affected profile/package/configuration and
recovery path, validate it, then test the original failure or workload. Separate
installed kernel, running kernel, configured scheduler, and observed scheduler.
Report missing graphical, hardware, reboot, or benchmark evidence directly.

Keep diagnostics local. Inspect a bug-report helper before execution and decline
its upload path unless sharing was requested. A request to fix the machine does
not authorize sending its logs to a paste service. Use
[omarchy](../omarchy/SKILL.md) only when Omarchy itself owns the affected surface.
