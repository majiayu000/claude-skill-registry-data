---
name: nixpi-firmware-provision
description: >
  Provision the nixpi Raspberry Pi 4 SD card via the FAT FIRMWARE partition — the
  Cloudflare connector token and Wi-Fi credentials that a fresh flash needs. Use when
  asked to "reflash nixpi", "flash the Pi", "plant the tunnel token", "update the
  connector token", "rotate the tunnel key", "set up / change nixpi Wi-Fi", or "nixpi
  can't reach the tunnel after a reflash". Everything is an all-Nix flake app
  (`nix run .#nixpi-*`) on the macOS host; pairs with
  the in-tree firmware-secrets capsule, hosts/nixpi.nix, and
  docs/nixpi-sd-flashing-runbook.md.
---

# nixpi firmware provisioning

nixpi reads two operator-planted files off the SD card's FAT `FIRMWARE` partition at
boot (`local.firmwareProvisioning`, the in-tree
`modules/features/firmware-secrets/` capsule),
copying each into a root-only `/run` file before its consumer starts:

| Planted file (`/boot/firmware/…`) | → `/run/…` | Consumer |
|---|---|---|
| `cloudflared-token` (`TUNNEL_TOKEN=…`) | `cloudflared-token` | `cloudflared-connector` |
| `wpa_supplicant.conf` (`country=` + `network={}`) | `wpa_supplicant-firmware.conf` | `supplicant-wlan0` (upstream `networking.supplicant`) |

## Why not agenix (read this first)

agenix encrypts to nixpi's SSH **host key**, but a NixOS SD image ships none, so every
fresh flash mints a new random host key — after which the agenix ciphertext no longer
decrypts, the tunnel never comes up, and (the tunnel being the only remote path in)
there is no way back in. The FAT partition is the one thing macOS can write, so
host-key-independent secrets live there. `secrets/cloudflared-token.age` stays the
operator-only **vault** of the token; the operator decrypts it to plant, the Pi never
decrypts it on-device.

## The tools (all macOS flake apps)

- `nix run .#nixpi-flash -- --disk /dev/diskN [--release | --image FILE.img.zst] [--ssid NAME | --wifi-conf FILE]`
  — fresh reflash: acquire the image → verified `dd` (byte-count checked) → auto-plant
  token + Wi-Fi. Image source, in precedence: `--image` (local file); `--release`
  (download the latest CI-built image off the `installer-latest` GitHub release — needs
  `gh` auth, but **no Nix build and no aarch64-linux builder**, so this is the Mac path);
  default = `nix build` the sdImage (Cachix-warms the kernel, but the final assembly still
  needs an aarch64-linux builder). Wi-Fi is auto-detected unless you pass
  `--ssid`/`--wifi-conf` (needed on a band-split network — see gotchas).
- `nix run .#nixpi-provision [--all|--token|--wifi]` — plant onto an already-mounted card.
- `nix run .#nixpi-wifi-creds [--ssid S [--psk P]]... [--country CC]` — emit a
  `wpa_supplicant.conf` from this Mac's current Wi-Fi (SSID + keychain PSK + locale country).
  **`--ssid` is repeatable**: each one opens a `network={}` block, the `--psk` after it
  belongs to it, and the blocks are ranked by a descending `priority=` — first is the
  AP nixpi prefers, the rest are fallbacks it drops to when that one is gone. A
  non-ASCII SSID (an emoji one is real) is emitted as a **hex** `ssid=` plus a decoded
  comment, because a quoted UTF-8 literal has to survive the pipe, FAT and
  wpa_supplicant's parser intact.
- `nix run .#nixpi-vault-token` — re-encrypt a new token (stdin/`$TUNNEL_TOKEN`) into the vault.

Run them from the repo root (they read the vault at `secrets/cloudflared-token.age`).

## Scenarios

1. **Fresh reflash** → `nix run .#nixpi-flash -- --disk /dev/diskN --release`, then insert +
   boot. (`--release` downloads the CI-prebuilt image; drop it to `nix build` locally instead —
   only works where an aarch64-linux builder exists. The image is secret-free, so the public
   release artifact is safe.)
2. **Update the tunnel token** (rotation): `CLOUDFLARE_API_TOKEN=… nix run .#cf-tunnel-apply`
   prints a new token → pipe it to `nix run .#nixpi-vault-token` → commit the vault →
   `nix run .#nixpi-provision -- --token` on a mounted card (or reflash), reboot.
3. **Update Wi-Fi** → `nix run .#nixpi-provision -- --wifi` on a mounted card, reboot.

## Gotchas

- **Re-plant every flash** — `dd` wipes the FAT partition. `nixpi-flash` does it for you.
- **Wi-Fi needs `country=`** — the Pi 4 radio is rfkill-blocked without a regulatory domain.
- **Band-split SSID** — if the Mac is joined to `<name>-5G` but the keychain stores the
  base `<name>` PSK, Wi-Fi auto-detect (used by `nixpi-flash`/`nixpi-provision` with no
  Wi-Fi args) fails ("no saved password"). Pin it:
  `nix run .#nixpi-flash -- --disk /dev/diskN --ssid <name>` (the 2.4 GHz `<name>` also
  gives a headless Pi better range), or plant separately —
  `nix run .#nixpi-wifi-creds -- --ssid <name> > wpa.conf` then
  `nix run .#nixpi-provision -- --wifi --wifi-conf wpa.conf`. Verified 2026-07-15 on `BELL044`.
- **The token is plaintext on the FAT partition at rest** — accepted tradeoff for
  unattended first-boot; mitigate with physical security + rotate on card loss. The
  `/run` copy is root-only (0600).

## Full runbook

`docs/nixpi-sd-flashing-runbook.md` (§4b = the plant step; §1 = the verified-write golden rule).
