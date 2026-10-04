---
name: safe-apt-install-evaluation
description: Preview an `apt install` transaction with `--simulate` and flag dangerous removals (kernel, NVIDIA, mesa, DKMS, desktop metapackages, `-common` packages) plus the repository origin before the user actually installs. Use when the user wants to know "what happens if I apt install X" on a shared Ubuntu machine, or asks to evaluate / preview an apt install plan.
argument-hint: <pkg> [<pkg>...]
allowed-tools: Bash(apt:*), Bash(apt-get:*), Bash(apt-cache:*), Bash(apt-mark:*), Bash(dpkg:*), Bash(grep:*)
---

# Safe `apt install` Evaluation

The user is a superuser on a shared Ubuntu machine and has previously had `ubuntu-desktop` / NVIDIA / DKMS torn out by a careless `apt install`. This skill runs the simulation, parses the output, and tells them whether the transaction is safe to proceed with — **never run the real install yourself**.

## Core Recipe

### Step 1 — Simulate the transaction

`-s` / `--simulate` does not need root and does not modify the system:

```bash
apt-get -s install <pkg> [<pkg>...]
```

Use `apt-get` (not `apt`) — its output is stable and machine-parseable; `apt`'s output is intentionally user-facing and can change.

### Step 2 — Check the repository origin

For each package the user named:

```bash
apt-cache policy <pkg>
```

The `500`/`1001`/etc. priority lines and the URI tell you which repo a package will come from. Flag anything coming from a PPA, the NVIDIA CUDA repo, `-proposed`, or `-backports` — those are the usual sources of "shadowing" surprises, especially for `nvidia-*` where mixing providers causes pain.

### Step 3 — Show current holds (context)

```bash
apt-mark showhold
```

Anything in the simulation's **REMOVE** list that is *also* on hold is a strong sign the resolver is fighting the user's intent. Mention it.

### Step 4 — Parse the simulation output

Focus on these blocks from `apt-get -s install` stdout:

| Block | What it means | How to triage |
|-------|---------------|---------------|
| `The following NEW packages will be installed:` | New deps being pulled in | Informational — list briefly |
| `The following packages will be upgraded:` | Version bumps | Informational unless a load-bearing pkg is in here (see danger list) |
| `The following packages will be REMOVED:` | **DANGER** — apt will rip these out | Match every entry against the danger patterns below |
| `The following packages have been kept back:` | Resolver gave up on these | Mention — often signals a conflict |
| `0 upgraded, N newly installed, M to remove` | Summary line | If `M > 0`, treat as suspicious until each removal is justified |

### Step 5 — Match removals against danger patterns

Flag **any** removal matching these patterns as a stop-the-world finding:

- `linux-image-*`, `linux-headers-*`, `linux-generic`, `linux-modules-*`, `linux-hwe-*` — kernel
- `nvidia-*`, `libnvidia-*`, `cuda-*`, `nvidia-driver-*`, `nvidia-dkms-*` — GPU stack
- `mesa-*`, `libgl*`, `libegl*`, `libgles*`, `libdrm*`, `xserver-xorg-*` — graphics stack
- `ubuntu-desktop`, `ubuntu-desktop-minimal`, `gnome-shell`, `gdm3`, `plasma-desktop`, `kde-plasma-*` — desktop metapackages
- Anything ending in `-common` (`xserver-common`, `libreoffice-common`, etc.) — usually the seam that takes a metapackage with it
- Anything containing `dkms` — DKMS-built modules (NVIDIA, ZFS, VirtualBox, etc.)
- `systemd`, `systemd-*`, `init`, `dbus`, `libc6`, `libc-bin` — userspace base; removing these bricks the boot
- The exact same package the user asked to install (sign of a conflict)

If **nothing** in the REMOVE list matches the danger list, the transaction is low-risk — say so explicitly.

### Step 6 — Report to the user

Use this structure. Be concise — the user reads the verdict line first and the evidence only if they care.

```
Verdict: SAFE | CAUTION | DO NOT PROCEED

Command they should run:
  sudo apt install <pkg>           # if safe
  (do not run yet)                 # if caution / unsafe

Removals: <N>
  <pkg>  — [DANGER: kernel | NVIDIA | desktop metapackage | etc.]
  <pkg>  — (benign, obsoleted transitional package)

Repository origin (apt-cache policy):
  <pkg> → <repo URI>  [flag if PPA / CUDA repo / -proposed]

Holds in play:
  <list, or "none">

Other notes:
  - <kept-back packages, if any>
  - <upgrades of load-bearing packages, if any>
```

Verdict rules:
- **DO NOT PROCEED** — any danger-list match in REMOVE.
- **CAUTION** — any non-empty REMOVE list, OR any kept-back package, OR the package comes from a shadowing repo (PPA / CUDA / proposed) the user may not realize.
- **SAFE** — empty REMOVE list, no kept-back packages, origin is the main Ubuntu archive.

If verdict is not SAFE, suggest the recovery levers from the [[apt-best-practices]] context:

- `apt-mark hold <pkg>` to pin the at-risk packages before retrying
- `apt-cache policy` to pick a different origin
- `aptitude install <pkg>` — its solver often proposes a non-destructive alternative path that `apt`'s resolver won't find
- A `timeshift` / `dpkg --get-selections > ~/packages-$(date +%F).list` snapshot before any destructive transaction
- Consider whether the tool could live in a container (CUDA toolkit), `pipx`, `cargo install`, or `~/.local` instead of apt

## Variations

- **Multiple packages at once**: pass them all to one `apt-get -s install` call. Apt's resolver works on the combined set; simulating them one-by-one hides interactions.
- **`full-upgrade` / `dist-upgrade` previews**: `apt-get -s full-upgrade` is fair game with the same parsing rules. Default-recommend plain `apt upgrade` over `full-upgrade` on shared machines (the former is not allowed to remove packages to resolve deps).
- **Reverse — "what depends on this?"**: if you're worried about a removal, `apt-cache rdepends --installed <pkg>` shows what would break.
- **Sanity check the system first**: if `dpkg --audit` returns anything, the system is already in a half-configured state and the simulation may be misleading. Flag this before trusting the plan.

## When Applying This Skill

1. Did the user actually ask to evaluate, or to *install*? This skill only evaluates — never run the real `sudo apt install`. End with a recommended command for the user to run themselves.
2. Did you pass every package the user named in a single `apt-get -s install` call?
3. Did you check `apt-cache policy` for every named package (not just the leaf install)?
4. Did you scan the **REMOVED** block against every danger pattern, not just kernel/NVIDIA?
5. Did you note any kept-back packages? (Resolver giving up is a yellow flag even with an empty REMOVE list.)
6. Did you give a single-word verdict line at the top so the user can decide in two seconds?
