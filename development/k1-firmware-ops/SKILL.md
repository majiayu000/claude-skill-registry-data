---
name: k1-firmware-ops
description: Build selected K1.node2 pattern(s), upload firmware to the ESP32-S3 over LAN, verify the web API/UI, capture artifacts, and draft release notes.
---

# K1 Firmware Ops

## Purpose
Create a repeatable, end-to-end flow for K1.node2: **codegen → compile → OTA → API/UI QA → release notes**.

## Prerequisites
- PlatformIO CLI (`pio`) installed and on PATH.
- Node.js 18+ and npm installed.
- Playwright runtime installed (the steps below run `npx playwright install`).

## Config
Edit `tools/k1.config.json` in the repo root to match your setup:
```json
{
  "device_ip": "192.168.1.50",
  "ota_method": "arduino",
  "dashboard_path": "/",
  "pattern": "Twilight",
  "upload_port": "3232"
}
```

## Procedure (follow these steps in order)
1. **Build & Upload** (uses existing project scripts and/or PlatformIO):
   ```bash
   bash tools/k1_firmware_ops.sh --pattern "<PATTERN_NAME>" --ip "<DEVICE_IP>" --qa false
   ```
   - Artifacts land under `artifacts/<timestamp>/` (build log and metadata).

2. **Install QA deps** once:
   ```bash
   cd tools/qa/playwright
   npm ci
   npx playwright install
   cd ../../..
   ```

3. **Run API + UI tests** (captures JSON report + screenshots):
   ```bash
   bash tools/k1_firmware_ops.sh --pattern "<PATTERN_NAME>" --ip "<DEVICE_IP>" --qa true
   ```

4. **Generate release notes** (Markdown summary with links to artifacts):
   ```bash
   node tools/release/generate_release_notes.mjs
   ```

## Examples
- Rebuild and upload **Twilight** to `192.168.1.50` and run QA:
  ```bash
  bash tools/k1_firmware_ops.sh --pattern "Twilight" --ip "192.168.1.50" --qa true
  ```

- Build only (no QA), using `tools/k1.config.json` defaults:
  ```bash
  bash tools/k1_firmware_ops.sh
  ```

## Guardrails
- Treat IPs and Wi‑Fi credentials as secrets; do not commit secrets.
- Prefer ArduinoOTA unless an HTTP OTA endpoint is **documented and reachable**.
- If `/api/params` POST semantics differ from the tests, update `tools/qa/params.sample.json` and the tests accordingly.
