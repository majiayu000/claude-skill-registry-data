---
name: asus-esc8000-gpu-bios-tuning
description: Apply a low-latency GPU-serving + VM-passthrough BIOS profile to ASUS ESC8000-E12P (ASMB12/AMI-BMC, Xeon 6/GNR) servers over Redfish — diff current settings, stage, reboot, verify. Use when asked to optimize/tune BIOS for GPU inference/serving, set performance power profile, enable Resize BAR / SR-IOV / disable SNC, or replicate one server's BIOS config onto another ESC8000.
---

# ASUS ESC8000 GPU-Serving BIOS Tuning

Applies a 10-setting low-latency profile + verifies a 4-setting passthrough baseline, over
Redfish. Validated on ESC8000-E12P (8× RTX PRO 6000 Blackwell, 2× Xeon 6730P, BIOS 0804).
Settings are reversible until you reboot; the tool is **dry-run by default**.

## Quick start

```bash
export BMC_PASSWORD='...'
# 1. Dry-run: show what would change on the target (no writes)
python3 scripts/tune_gpu_bios.py --target <BMC_IP>

# 2. Stage only (reversible, no reboot) — settings pending until next boot
python3 scripts/tune_gpu_bios.py --target <BMC_IP> --apply

# 3. Stage + reboot + verify active (the full apply)
python3 scripts/tune_gpu_bios.py --target <BMC_IP> --apply --reboot
```

## Two source modes (pick one)

- **Profile** (default): targets come from `scripts/gpu_serving_profile.json` (token strings
  validated on BIOS 0804 / registry `S0317.8.4.0`).
- **Template** (most robust): copy the live values from an already-tuned reference server —
  immune to BIOS-version token drift:
  ```bash
  python3 scripts/tune_gpu_bios.py --target <new_BMC_IP> --from-host <tuned_BMC_IP> --apply --reboot
  ```
  Prefer `--from-host` when you have a known-good server (e.g. tuning a second box to match the first).

## The profile (what & why)

10 tuned + 4 baseline-verified. Full rationale table in [REFERENCE.md](REFERENCE.md). Headline:
Resize BAR on, EPP/EPB → Performance, Energy-Efficient-Turbo / C1E-promotion off, Workload →
I/O-sensitive, Latency-Optimized on, **SNC off** (1 NUMA/socket), ASPM-IIO off, AC-loss → Power On.
Baseline (must already hold): Above-4G on, SR-IOV on, **ACS off** (fast GPU P2P — flip to on only
at VM adoption). VT-d has no BIOS toggle on this platform (always exposed; gate it OS-side).

## Workflow checklist

1. Confirm firmware parity first — same BIOS version on source & target, else tokens won't match
   (use the `asus-esc8000-firmware-upgrade` skill). With `--from-host`, mismatched versions are flagged.
2. Dry-run; review the diff with the operator.
3. `--apply --reboot`. The reboot is `GracefulShutdown → poll Off → On` (this build has **no
   GracefulRestart**). POST takes ~5–6 min (SNC change forces full memory retraining).
4. Verify prints `VERIFIED N/N active`. The post-reboot host shows `0/N` mid-POST — that's normal,
   it resolves when the host republishes its BIOS map.

## Gotchas (details in REFERENCE.md)

- PATCH target is `…/Bios/SD`, **not** `/Bios/Settings`; needs `If-Match` etag (else 428).
- PATCH returns **503** ("inventory processing") while the host is mid-boot — wait for it to settle.
- Pace gently / single connection; a freshly-rebooted AMI BMC locks out on rapid auth (`AccessDenied`).
- This only touches BIOS. The `intel_iommu=on iommu=pt` kernel cmdline is a separate OS-side step.

See [REFERENCE.md](REFERENCE.md) for the attribute table, rationale, and the full Redfish API notes.
