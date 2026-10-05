---
name: cua-macos-lume-sandbox
description: Provision a macOS VM as a cua computer-use sandbox with lume on Apple Silicon — pull or APFS-clone an image, size it, ensure autologin, install cua-driver plus a LaunchAgent, grant TCC unattended when SIP is off, set the guest resolution, and verify with a real screen capture. Use when asked to set up, rebuild, or repair a cua or computer-use sandbox VM, to register the cua-driver MCP server, or when cua-driver reports a daemon in "unknown" state, TCC grants that will not stick, or screenshots at the wrong resolution.
---

# Provision a macOS cua sandbox VM with lume

Turns a [lume](https://github.com/trycua/cua)-managed macOS guest on Apple Silicon into a working
[cua](https://cua.ai) computer-use sandbox: `cua-driver` running under a LaunchAgent, Accessibility
and Screen Recording granted, and a verified screen capture at the resolution you asked for.

**On `macos-tahoe-cua` the run is unattended** — Accessibility, Screen Recording, and full-display
capture all come up without anyone at the VM's screen. That hinges entirely on the image; see the
decision rule below. One leftover needs a single click: **Tahoe raises a separate "direct capture"
consent** that does not live in TCC.db and so cannot be scripted — see
[REFERENCE.md §3](REFERENCE.md). Capture works without answering it; the dialog just sits on the
desktop, where it will get in the way of UI automation until dismissed.

Validated end to end on a Mac Studio M3 Ultra / macOS 26.6.1 host, guest macOS 26.4 (25E246),
lume 0.5.3, cua-driver 0.20.0. Every trap the scripts work around is documented in
[REFERENCE.md](REFERENCE.md).

## Prerequisites

- Apple Silicon Mac; `lume` 0.5.3+ and `jq` on `PATH`
- ~50 GB free per sandbox: lume's cache keeps the ~21 GB image **in addition to** the ~26 GB VM
- Only 2 macOS guests may run at once (XNU limit), counting any VM already running

## Decision rule: which image

This is the only choice that matters, because it decides whether provisioning can be unattended.

| | `macos-tahoe-cua:latest` | `macos-tahoe-vanilla:latest` |
|---|---|---|
| SIP | **disabled** | enabled |
| Autologin (real Aqua session) | **yes**, first boot | **no** — boots to the login window |
| Xcode Command Line Tools | yes | no |
| `CuaDriver.app` / `cua-computer-server` | **no** — you still install them | no |
| TCC grants pre-applied | no | no |
| Default disk | 150 GB | 100 GB |
| **TCC grants scriptable?** | **yes** (SIP off ⇒ TCC.db writable) | **no** — one manual sitting |

**Use `macos-tahoe-cua:latest` unless you have a specific reason not to.** "Pre-provisioned" means
the *environment*, not the cua software — the driver install is still yours to run. What it actually
buys you is SIP-off and autologin, and SIP-off is what removes the manual step.

## Quick start

```bash
VM=my-sandbox SHARED_DIR="$HOME/work/sandbox" bash scripts/provision.sh
```

`VM` is required. Everything else is optional:

| Variable | Default | Notes |
|---|---|---|
| `VM` | — | **required**; the lume VM name |
| `IMAGE` | `macos-tahoe-cua:latest` | ignored when `GOLDEN` is set |
| `GOLDEN` | — | clone this VM instead of pulling (APFS CoW, ~2 s) |
| `SHARED_DIR` | — | host dir to share `:rw`; omitted entirely when unset |
| `CPU` / `MEMORY` | `8` / `16GB` | |
| `DISK_SIZE` | — | unset means don't resize; **increase-only** |
| `DISPLAY_RES` | `1920x1080` | applied *inside* the guest, see traps |
| `INSTALL_COMPUTER_SERVER` | `0` | `1` also installs Path B (HTTP API) |
| `INSTALL_TERMINFO` | `1` | export the host's terminfo into the guest user's `~/.terminfo` |
| `TERMINFO_TERMS` | `$TERM` | space-separated entries to export; skips ones the guest has |

`--recreate` destroys an existing VM of that name first.

## What `provision.sh` does

1. **Acquire** — clone from `GOLDEN` if set, else pull `IMAGE`. Skipped if the VM already exists.
2. **Size** — `lume set` with the VM stopped; resizes only when it's a genuine increase.
3. **Boot**, wait for IP and SSH.
4. **Check `/dev/console`** — the one precondition everything rests on. If it's owned by `root`
   there is no GUI session; the script applies `lume setup --unattended tahoe` and reboots.
5. **Install `cua-driver`** and a LaunchAgent pointing at the **in-bundle** binary.
6. **Grant TCC** directly in `TCC.db` when `csrutil` reports SIP disabled; otherwise print the
   manual instructions.
7. **Export terminfo** — compiles the host's `$TERM` entry into the guest user's
   `~/.terminfo`, which ncurses already searches, so SSHing in from Ghostty/kitty/WezTerm
   doesn't hit "unknown terminal type".
8. **Set guest resolution** with `displayplacer`.
9. **Verify** — SIP, `doctor`, permissions booleans, and a real `get_desktop_state` capture.

It is idempotent: re-running is also the health check.

## Verify

```bash
lume ssh "$VM" "stat -f '%Su' /dev/console"     # -> lume   (root = no GUI session)
lume ssh "$VM" "/Applications/CuaDriver.app/Contents/MacOS/cua-driver permissions status --json"
# -> "accessibility": true, "screen_recording": true
lume ssh "$VM" "/Applications/CuaDriver.app/Contents/MacOS/cua-driver call get_desktop_state '{}'" \
  | grep -E 'screen_width|screenshot_png_b64'
```

Booleans flipping is not proof — only a returned `screenshot_png_b64` is.

## Snapshot a golden image

`lume clone` is APFS copy-on-write: ~2 seconds, ~0 bytes. Do this once and never re-download:

```bash
lume stop "$VM" && lume clone "$VM" "${VM}-golden"
GOLDEN="${VM}-golden" VM="$VM" bash scripts/provision.sh --recreate   # future rebuilds
```

lume's cache keeps only the **current manifest per image**, so a `:latest` that moves upstream costs
a full re-download even with caching on. A golden clone is the only durable protection.

## Register the MCP server

Never bake the VM's IP into the registration — a NAT guest's IP drifts across reboots and the MCP
server then fails silently. Install the wrapper, which re-resolves at connect time:

```bash
install -m 755 scripts/cua-mcp-wrapper.sh ~/.local/bin/cua-${VM}-mcp
claude mcp add --scope user cua-driver-vm -- ~/.local/bin/cua-${VM}-mcp
```

The wrapper reads `CUA_VM` (default: the name baked in at install time). **stdout is the JSON-RPC
channel** — any diagnostic printed there breaks the transport.

## Traps worth knowing up front

- **SSH working is not evidence of a GUI session.** A vanilla image has working SSH *at the login
  window*. `stat -f '%Su' /dev/console` is the only reliable test — `root` means no Aqua session,
  and then `cua-driver` cannot launch, LaunchAgents never load, and permissions read `unknown`.
- **`lume set --display` never reaches the guest.** It only offers the mode to the virtual GPU;
  macOS keeps rendering at its previous resolution and cua-driver screenshots at *that*. `lume ls`
  will confidently report a resolution the guest is not using.
- **`lume stop` is unreliable** — it can no-op silently or fail with `Cannot modify <vm>: the VM is
  running. Stop it first.` from `stop` itself. The script falls back to terminating the process.
- **`take_screenshot` does not exist** in cua-driver 0.20.0; capture is `get_desktop_state`. The old
  name fails with `no reviewed risk classification`, which reads like a TCC error but is the
  driver's own tool-manifest gate.
- **Don't rename the `lume` guest account.** cua hardcodes `/Users/lume`, and every lume convenience
  command defaults to it. Change the password instead.

Full diagnosis of each, plus the Path B HTTP API and the version history, is in
[REFERENCE.md](REFERENCE.md).
