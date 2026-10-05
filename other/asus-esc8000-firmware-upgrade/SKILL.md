---
name: asus-esc8000-firmware-upgrade
description: Check and upgrade BMC firmware and BIOS on ASUS ESC8000-E12P (and similar ASMB12/AST2600 AMI-BMC ASUS servers) via Redfish and the BMC's HPM wizard API. Use when asked to check firmware/BIOS versions, update BMC or BIOS on ASUS GPU servers, or recover a BMC stuck in firmware-update/flash mode (login blocked, Redfish 503).
---

# ASUS ESC8000 BMC/BIOS Upgrade

Validated end-to-end on ESC8000-E12P (ASMB12-iKVM, AMI SP-X gen13). BMC updates are host-safe;
BIOS updates require the chassis powered OFF and a host reboot.

## Quick start — check current + latest versions

```bash
export BMC_PASSWORD='...'
scripts/check_versions.sh <BMC_IP>                  # current BMC FW, BIOS, power state
scripts/check_versions.sh <BMC_IP> ESC8000-E12P     # + latest versions from ASUS API
```

Download zips from the URLs the ASUS API returns. BIOS zip → `.HPM` (BMC-flashable) + `.CAP`
(EzFlash only — don't use here). BMC zip → `.hpm`.

## Workflow A — BMC firmware (host keeps running)

```bash
scripts/bmc_update.sh <BMC_IP> <BMC_fw.hpm>
```

Does: preserve-config flags → Redfish multipart push → flash → BMC auto-reboot → version verify.
~10 min. **Warning:** after the BMC reboots, the host may power ON via power-restore policy —
re-check chassis state before any subsequent BIOS work.

## Workflow B — BIOS (chassis must be OFF)

1. Confirm with the operator that the host may go down; gracefully shut it down:
   `POST /redfish/v1/Systems/<id>/Actions/ComputerSystem.Reset {"ResetType":"GracefulShutdown"}`
   and wait for `PowerState: Off`.
2. Flash (script enforces a power-off gate and exits update mode on any failure):
   ```bash
   python3 scripts/bios_update.py --ip <BMC_IP> --file <BIOS.HPM>
   ```
3. Power on: `{"ResetType":"On"}`. First POST takes 5–15 min (memory retraining).
   `BiosVersion` in Redfish flips mid-POST; then verify the OS comes back.

Update BMC first, then BIOS (paired releases). Do not run two flashes concurrently.

## If the BMC is bricked in flash mode (the "3ed" state)

Symptoms: web UI loads but login returns `{"error":"Could not login","code":1348}`
("Firmware update in progress hence login has been blocked"), Redfish 503, SSH/IPMI/KVM
ports closed. No remote fix exists once all sessions are gone — it never times out.

→ **AC drain**: unplug both PSU cords (or PDU outlets) 30 s, replug. BMC boots clean in ~3 min.
Prevention: never abandon the firmware wizard mid-flow; the scripts here always exit update
mode on failure, and `hpm/exitupdatemode {"FWUPDATEID":N}` works from ANY admin session.

## Key gotchas (full details in REFERENCE.md)

- `Managers/Self` & `Systems/Self` are invalid — discover members (`Managers/BMC_0`, `Systems/System_0`).
- BMC reset type is `ForceRestart`; reset bounces the host ON via power-restore policy.
- Redfish multipart needs THREE parts incl. `OemParameters={"ImageType":"HPM"}`.
- The Redfish `UpdateService/upload` path CANNOT flash BIOS (demands an unsatisfiable
  `BiosUpdateMethod`) — use the HPM wizard API (Workflow B).
- After the wizard upload you MUST call `PUT hpm/flash` — without it the flash never starts
  and `upgradestatus` returns 500 `code 1442 "Error in HPM Finish Firmware Upload"`.
- `ipmitool hpm upgrade` does not work: `0xD5` refusal, and ~3 KB/s if it runs at all.
- PreserveConfiguration flags default to FALSE — set them before BMC flash or lose network/users.

See [REFERENCE.md](REFERENCE.md) for the complete API map, payloads, and error-code table.
