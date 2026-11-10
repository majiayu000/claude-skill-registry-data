---
name: uptime
description: Uptime monitors for public sites and the org's Hosting apps.
---

# Uptime

Use it to see whether a site or app is up, and to add or change monitors.

## Flow

1. `uptime.list` for every monitor with its state and percent up.
2. `uptime.get` for one monitor's recent checks.
3. `uptime.check` runs a check now and waits for it.
4. `uptime.save` adds or changes a monitor. For an app, call `uptime.targets` first and set `target_kind` to app.

## Watch out

- A target is a public https URL or an app name.
- `expected_status` is a class such as 2xx or a code such as 204.
