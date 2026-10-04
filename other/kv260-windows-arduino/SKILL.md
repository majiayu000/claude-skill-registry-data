---
name: kv260-windows-arduino
description: Coordinate the KV260 Prophesee event-camera board with the Windows host and its USB Arduino light controller. Use when Codex needs to inspect or operate the KV260 recording API, communicate with Windows 192.168.1.166 / CSG1175-P, reason about Arduino COM-port control, clone/use the four related Windows repos, or document/diagnose port conflicts, /dev/video0 ownership, firewall, phase-sync, and recording workflows.
---

# KV260 Windows Arduino

Use this skill for the lab setup where:

```text
KV260 PetaLinux board -> Prophesee event camera on /dev/video0
Windows host          -> Arduino UNO over USB serial for light modulation
```

Do not assume the Arduino is reachable from the KV260 directly. The Arduino has no IP address. Communicate through Windows when controlled light commands are needed.

This skill is paired with the Windows-side skill:

```text
C:\Users\Administrator\.codex\skills\kv260-arduino-event-control\SKILL.md
```

## Core Topology

Current known LAN identities:

```text
KV260 hostname: xilinx-kv260-starterkit-20222
KV260 IP:       192.168.1.250
Windows host:   CSG1175-P
Windows IP:     192.168.1.166
```

Primary service split:

```text
KV260 event recording API:   http://192.168.1.250:8765
Windows Arduino control API: http://192.168.1.166:8780
```

Use `8780` for the future Windows Arduino API to avoid confusing it with the KV260 event API on `8765`.

## First Checks

From the KV260:

```sh
hostname
ip -4 addr show scope global
ping -c 2 192.168.1.166
cd /home/petalinux/Projects/kria-kv260-starter
./scripts/kv260-event-camera-api.sh status
./scripts/kv260-event-camera-switch.sh --status
```

Bundled helper:

```sh
/home/petalinux/.codex/skills/kv260-windows-arduino/scripts/kv260-lab-status.sh
```

## Operating Rules

1. Prefer Windows as the first controlled experiment master, because the Arduino is physically connected to Windows USB.
2. Use KV260 as the recording device. It records `/dev/video0` into `.pse2.raw` plus `.json`.
3. Only one process can own `/dev/video0`: custom GUI, native `metavision_viewer`, or headless recording API.
4. Use `takeover=true` when starting remote recording so the API can stop viewer processes first.
5. Use autonomous Arduino modulation first if Arduino COM3 is not available or the Windows Arduino API is not implemented.
6. For controlled mode, ensure Windows detects Arduino with `arduino-cli board list` before trying serial commands.
7. Never treat bootloader burn as normal upload. Require explicit confirmation and a selected programmer.

## Main Workflows

### Inspect The Lab

Read `references/topology.md` and run:

```sh
scripts/kv260-lab-status.sh
```

Use Windows SSH only when needed to inspect Windows files or Arduino CLI:

```sh
ssh -i /home/petalinux/.ssh/id_dropbear_rsa -y Administrator@192.168.1.166 "powershell -NoProfile -Command \"hostname; arduino-cli board list\""
```

### Record Events From KV260

Read `references/kv260-recording-api.md`.

Start the board API:

```sh
cd /home/petalinux/Projects/kria-kv260-starter
./scripts/kv260-event-camera-api.sh start
```

Run a short recording:

```sh
scripts/kv260-record-once.sh --seconds 2 --prefix skill_smoke
```

Stop API:

```sh
./scripts/kv260-event-camera-api.sh stop
```

### Coordinate Arduino Light Control

Read `references/windows-arduino-control.md`.

Use direct serial on Windows for real-time light commands. Use `arduino-cli` for firmware/core/library/upload tasks only.

If Windows should orchestrate an experiment, use the repo client from Windows:

```powershell
python .\KV260EventExperimentClient.py --board-url http://192.168.1.250:8765 run --arduino-port COM3 --light-on "ON" --light-off "OFF" --seconds 5 --prefix illumination
```

If KV260 should command Windows later, target:

```text
http://192.168.1.166:8780
```

and confirm firewall access first.

### Use Related Repos

Read `references/repositories.md`.

Board clone paths:

```text
/home/petalinux/Projects/polarizer
/home/petalinux/Projects/DualLampHI
/home/petalinux/Projects/OpenHI3.0
/home/petalinux/Projects/OpenHI2.0
```

The Arduino sketch of current interest is:

```text
/home/petalinux/Projects/DualLampHI/firmware/dual_led_direct_timer1/dual_led_direct_timer1.ino
```

### Diagnose Conflicts

Read `references/conflicts.md` before changing ports or services.

Common issues:

```text
Arduino COM3 missing -> fix Windows USB detection first
KV260 API 8765 vs Windows API 8780 -> keep ports distinct
Windows firewall blocks 8780 -> Windows must allow inbound
/dev/video0 busy -> stop GUI/native viewer/API owner
autonomous modulation -> phase is not locked without sync signal
```

### Recover Cross-Session Memory

Read `references/session-memory.md` when the user asks about Codex conversation history, JSONL files, `AGENTS.md`, or making the Windows and KV260 Codex sessions know each other.

Use `scripts/fetch-windows-codex-session.sh` to pull Windows Codex JSONL into the ignored board cache before targeted inspection.

Do not import raw JSONL into git or skill files. Use the JSONL only to recover targeted facts, then write a sanitized summary.

## Source Repo Docs

Canonical detailed docs live in:

```text
/home/petalinux/Projects/kria-kv260-starter/references/kv260-windows-arduino-situation.md
/home/petalinux/Projects/kria-kv260-starter/references/windows-arduino-codex-handoff.md
/home/petalinux/Projects/kria-kv260-starter/references/kv260-arduino-cli-control-api.md
/home/petalinux/Projects/kria-kv260-starter/references/kv260-remote-recording-api.md
```

Load only the relevant file for the task. Do not paste all docs into context unless the user explicitly asks for a full report.

## Windows Peer Skill

Windows peer skill known by this KV260 skill:

```text
name: kv260-arduino-event-control
installed: C:\Users\Administrator\.codex\skills\kv260-arduino-event-control
repo copy: C:\Users\Administrator\Projects\DualLampHI\skills\kv260-arduino-event-control
repo doc:  C:\Users\Administrator\Projects\DualLampHI\docs\codex_cross_session_memory_cn.md
```

Keep this KV260 skill and the Windows peer skill aligned when IPs, ports, repo paths, scripts, serial protocols, or experiment workflow rules change. Do not import raw Codex history as normal memory; use curated docs and skills.

## Board Codex History Context

If recent board-side conversation context is needed, the local Codex history is:

```text
/home/petalinux/.codex/history.jsonl
```

Use targeted reads only, for example:

```sh
tail -n 80 /home/petalinux/.codex/history.jsonl
grep -iE 'arduino|com3|recording api|duallamphi|v-spice|preview' /home/petalinux/.codex/history.jsonl | tail -n 80
```

Do not treat raw history as canonical state. Confirm with repository files, helper scripts, `/dev/video0` ownership, API status, and Windows Arduino probes.
