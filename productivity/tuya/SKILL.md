---
name: Tuya Smart
slug: tuya
version: 1.0.0
description: Control and automate Tuya Smart devices with official cloud APIs, secure request signing, region-aware routing, and safe command execution.
homepage: https://clawic.com/skills/tuya
changelog: Initial release with end-to-end Tuya Smart workflows for authentication, account linking, device control, diagnostics, and safe rollout playbooks.
metadata:
  clawdbot:
    emoji: T
    requires:
      bins:
      - curl
      - jq
      - openssl
      env:
      - TUYA_ACCESS_ID
      - TUYA_ACCESS_SECRET
    primaryEnv: TUYA_ACCESS_SECRET
    os:
    - linux
    - darwin
    - win32
    displayName: Tuya Smart
---

## Setup

On first use, read `setup.md` and align activation boundaries, cloud region context, and write-safety defaults before sending Tuya commands.

## When to Use

Use this skill when the user needs practical execution across the Tuya ecosystem: cloud API authentication, device discovery, DPS-based command control, account linking, or automation orchestration.
Use this instead of generic IoT advice when outcomes depend on Tuya Smart API behavior, regional endpoints, request signing, and command validation.

## Architecture

Memory lives in `~/Clawic/data/tuya/`. See `memory-template.md` for structure and status values.

```text
~/Clawic/data/tuya/
|-- memory.md                 # Core context and activation boundaries
|-- environments.md           # Region, project, app-account, and endpoint mapping
|-- devices.md                # Device inventory, capabilities, and command mappings
|-- automations.md            # Cross-device orchestration plans and safeguards
`-- incidents.md              # Error signatures, fixes, and verification evidence
```

## Quick Reference

Use the smallest file needed for the current task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory and workspace templates | `memory-template.md` |
| Cloud auth and signing reference | `auth-signing.md` |
| User account and home/device linking | `account-linking.md` |
| Device commands and state workflows | `device-operations.md` |
| Multi-device rollout patterns | `orchestration-playbooks.md` |
| Diagnostics and recovery | `troubleshooting.md` |

## Requirements

- Tuya IoT Platform project credentials: Access ID and Access Secret
- Environment variables: `TUYA_ACCESS_ID` and `TUYA_ACCESS_SECRET`
- Correct regional OpenAPI endpoint for the project data center
- Device permissions enabled in the project (Cloud Authorization and required API groups)
- For account-based device binding: configured user permission package and app account flow

Never ask users to paste production secrets into chat logs. Prefer local environment variables and redacted examples.

## Data Storage

Keep local operational notes in `~/Clawic/data/tuya/`:
- environment and endpoint mappings
- device command dictionaries by product/device id
- approved automation policies and rollback plans
- incident signatures and validated remediations

## Core Rules

### 1. Resolve Region and Project Scope Before Any API Call
- Confirm project environment, app type, and region endpoint first.
- Block execution if region and project are ambiguous because token and device calls will fail or target the wrong tenant.

### 2. Build and Verify Tuya Signature Inputs Exactly
- Sign every request with Tuya's documented HMAC-SHA256 process.
- If `sign`, `t`, nonce, body hash, or signed headers are inconsistent, treat the request as invalid and rebuild before retrying.

### 3. Discover Device Capabilities Before Sending Commands
- Read device details and function schema before writes.
- Generate commands only from supported `code` values and valid data types/ranges.

### 4. Use Read-Before-Write and Read-After-Write Control Loops
- Capture baseline status before command execution.
- After each write, verify resulting state and stop rollout on mismatch.

### 5. Apply Explicit Safety Gates for Real Device Writes
- Start with read-only inspection and dry-run command plans.
- Require explicit confirmation before high-impact actions (power, heating, locks, alarms, or bulk updates).

### 6. Keep Account Linking and Device Ownership Consistent
- Match app account model, cloud project permissions, and user-device binding flow.
- If device list and control APIs disagree, reconcile account linkage before troubleshooting commands.

### 7. Design Automations as Idempotent, Observable Sequences
- Use deterministic run ids, bounded retries, and clear stop conditions.
- Track each step with expected state checks to avoid duplicate or partial actions across device fleets.

### 8. Preserve Security and Privacy Boundaries
- Use least-privilege credentials and only declared endpoints.
- Read credentials from environment variables and never write raw secrets to local notes.
- Treat project tokens as short-lived runtime data and avoid persisting them unless the user explicitly requests it.

## Common Traps

- Choosing the wrong regional endpoint -> valid credentials fail and device lookup appears empty.
- Sending commands without checking function schema -> invalid `code/value` pairs and rejected writes.
- Mixing app-account and cloud-account assumptions -> users appear linked but device control fails.
- Retrying signed requests with stale timestamps/nonces -> repeated signature errors.
- Running bulk commands without staged verification -> large-scale bad state transitions.
- Treating online status as control success -> command accepted but target state not achieved.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://openapi.tuyaus.com | Signed API headers, device ids, command payloads, and project-scoped metadata | Tuya OpenAPI access for US region projects |
| https://openapi-ueaz.tuyaus.com | Signed API headers, device ids, command payloads, and project-scoped metadata | Tuya OpenAPI access for US West region projects |
| https://openapi.tuyaeu.com | Signed API headers, device ids, command payloads, and project-scoped metadata | Tuya OpenAPI access for Europe region projects |
| https://openapi-weaz.tuyaeu.com | Signed API headers, device ids, command payloads, and project-scoped metadata | Tuya OpenAPI access for Europe West region projects |
| https://openapi.tuyacn.com | Signed API headers, device ids, command payloads, and project-scoped metadata | Tuya OpenAPI access for China region projects |
| https://openapi.tuyain.com | Signed API headers, device ids, command payloads, and project-scoped metadata | Tuya OpenAPI access for India region projects |
| https://developer.tuya.com | Documentation query terms | Validate API behavior, limits, and integration requirements |

No other data is sent externally.

## Security & Privacy

Data that leaves your machine:
- signed Tuya API requests that contain selected device identifiers and command payloads
- optional account-linking payloads required by Tuya user/device binding APIs

Data that stays local:
- environment mapping, command dictionaries, and automation runbooks under `~/Clawic/data/tuya/`
- incident notes and risk decisions

This skill does NOT:
- use undeclared third-party endpoints
- request bypass or evasion techniques
- store `TUYA_ACCESS_ID` or `TUYA_ACCESS_SECRET` in local skill files
- execute bulk writes without user confirmation and verification strategy

## Trust

This skill sends operational data to Tuya cloud services when execution is approved.
Only install if you trust Tuya and your credential handling model with your IoT control data.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/<slug> (install if the user confirms):
- `iot` - Device connectivity and system-level IoT integration guidance
- `smart-home` - Home automation architecture and reliability practices
- `api` - API contract design, auth workflows, and error handling discipline
- `mqtt` - Messaging patterns for device telemetry and event-driven orchestration
- `zigbee` - Local network device planning and Zigbee ecosystem troubleshooting

## Feedback

- If useful, star it: https://clawic.com/skills/tuya
- Latest version: https://clawic.com/skills/tuya
