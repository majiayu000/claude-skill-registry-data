---
name: tuya
description: Control Tuya devices via local Home Assistant (tuya-local) or Tuya Cloud using the tuya-hub Go CLI.
metadata: {"clawdis":{"emoji":"🏠","requires":{"bins":["tuya"]}}}
---

# Tuya (tuya-hub)

Use this skill when the user wants to discover, poll, or control Tuya devices.

## Build

```bash
go build -o bin/tuya ./cmd/tuya
```

## CLI

- Use `./bin/tuya` or install to PATH and set `TUYA_BIN`.

## Config

Default config: `~/.config/tuya-hub/config.yaml`

Quick setup (guided wizard):
```bash
./bin/tuya config --backend cloud
```

**Important:** `cloud.userId` must be the UID from **Devices → Link Tuya App Account** (not the token UID).

Find linked app users (helps set the right `userId`):
```bash
./bin/tuya users --try-common
./bin/tuya users --schema smartlife
```

Minimum for Home Assistant backend:
```yaml
backend: ha
homeAssistant:
  url: "http://homeassistant.local:8123"
  token: "YOUR_LONG_LIVED_ACCESS_TOKEN"
```

Minimum for Tuya Cloud backend:
```yaml
backend: cloud
cloud:
  accessId: "YOUR_TUYA_ACCESS_ID"
  accessKey: "YOUR_TUYA_ACCESS_KEY"
  endpoint: "https://openapi.tuyaeu.com"
  schema: ""  # optional; used for user lookup
  userId: ""  # UID from Link Tuya App Account
```

Env overrides:
- `TUYA_BACKEND=ha|cloud`
- `TUYA_HA_URL`
- `TUYA_HA_TOKEN`
- `TUYA_CLOUD_ACCESS_ID`
- `TUYA_CLOUD_ACCESS_KEY`
- `TUYA_CLOUD_ENDPOINT`
- `TUYA_CLOUD_SCHEMA`
- `TUYA_CLOUD_USER_ID`

## Common actions (HA)

- **Discover devices**
  ```bash
  ./bin/tuya discover
  ```

- **Poll temperature sensors**
  ```bash
  ./bin/tuya poll --kind temperature
  ```

- **Get a device state**
  ```bash
  ./bin/tuya get --entity sensor.kitchen_temperature
  ```

- **Turn a device on/off**
  ```bash
  ./bin/tuya set --entity switch.garden_lights --state on
  ```

- **Call any HA service**
  ```bash
  ./bin/tuya call --service light.turn_on --data {"entity_id":"light.patio"}
  ```

## Common actions (Cloud)

- **Discover devices**
  ```bash
  ./bin/tuya discover --backend cloud
  ```

- **Poll temperature sensors (scaled)**
  ```bash
  ./bin/tuya poll --backend cloud --kind temperature
  ```
  Values are auto-scaled (tenths) when detected; raw value is in `value_raw` for JSON output.

- **Get device status**
  ```bash
  ./bin/tuya get --backend cloud --id <device_id>
  ./bin/tuya get --backend cloud --id <device_id> --code <status_code>
  ```

- **Switch / light on-off**
  1) Inspect status codes (look for `switch` / `switch_1` / `switch_2`):
  ```bash
  ./bin/tuya get --backend cloud --id <device_id>
  ```
  2) Send command:
  ```bash
  ./bin/tuya set --backend cloud --id <device_id> --code switch_1 --value true
  ./bin/tuya set --backend cloud --id <device_id> --code switch_1 --value false
  ```

## Notes

- Local control is via Home Assistant (tuya-local integration). HomeKit can be bridged through Home Assistant’s HomeKit integration.
- Cloud backend uses Tuya OpenAPI; devices must be linked to the cloud project.
- If you see `permission deny`, the app account UID is wrong or not linked to the project.
