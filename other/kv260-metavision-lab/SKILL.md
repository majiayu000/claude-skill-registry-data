---
name: kv260-metavision-lab
description: Use when setting up, operating, debugging, or documenting the AMD Kria KV260 Prophesee Metavision lab, including PetaLinux desktop launchers, custom event viewer, native metavision_viewer behavior, headless recording API, Windows X11 control center, file transfer GUI, and event-camera recovery workflows.
---

# KV260 Metavision Lab

Use this skill when the task involves the AMD Kria KV260 + Prophesee event-camera workstation that was built around:

```text
/home/petalinux/Projects/kria-kv260-starter
```

The lab includes:

- Prophesee event camera on KV260, usually `/dev/video0`.
- Custom KV260 event viewer and recorder.
- Native `metavision_viewer` launcher/toggle for SDK smoke tests.
- Local PetaLinux X11/Matchbox desktop launchers.
- Windows SSH X11 control center and file transfer panel.
- Headless HTTP recording API for experiments.
- Recovery scripts for stale viewers and `/dev/video0` ownership.

## First Checks

Run the bundled probe before changing viewer, desktop, or recording state:

```sh
skills/kv260-metavision-lab/scripts/kv260_metavision_probe.sh
```

If running from outside LazySkills, pass the repo path:

```sh
KV260_PROJECT_DIR=/home/petalinux/Projects/kria-kv260-starter \
  /path/to/kv260_metavision_probe.sh
```

## Core Rules

1. Run KV260 commands directly on the board. Do not SSH to the KV260 from a KV260-local session.
2. Only one process can own `/dev/video0`: custom viewer, native `metavision_viewer`, validation tools, or headless API.
3. Stop stale viewers before recording or switching display targets.
4. Prefer the headless recording API when recording correctness matters more than preview smoothness.
5. Keep raw recordings outside git, usually `/home/petalinux/event_recordings`.
6. Keep private session mirrors under ignored `private/` folders.
7. Commit and push durable docs, launchers, and scripts after repo edits when the project policy says so.

## Main Workflows

### Setup The Board

Read `references/setup-and-install.md`.

Main setup command in the Kria repo:

```sh
cd /home/petalinux/Projects/kria-kv260-starter
KV260_SUDO_PASSWORD=<password> ./scripts/kv260-full-setup.sh
```

Dry run first on unknown images:

```sh
./scripts/kv260-full-setup.sh --dry-run
```

### Operate Viewers

Read `references/viewer-and-recording.md`.

Common commands:

```sh
./scripts/kv260-event-camera-switch.sh --status
./scripts/kv260-event-camera-switch.sh --board
./scripts/kv260-event-camera-switch.sh --windows
./scripts/kv260-event-camera-switch.sh --stop-all
./scripts/kv260-metavision-viewer-toggle.sh
```

### Record Without GUI

Read `references/viewer-and-recording.md`.

Start/check the API:

```sh
./scripts/kv260-event-camera-api.sh start
./scripts/kv260-event-camera-api.sh status
```

Remote clients use:

```text
http://192.168.1.250:8765
```

### Desktop And Windows Control Center

Read `references/desktop-and-control-center.md`.

Important scripts:

```text
scripts/kv260-metavision-control-panel.py
scripts/kv260-file-transfer-gui.py
scripts/windows/Install-KV260WindowsShortcuts.ps1
scripts/windows/Open-KV260EventCamera.ps1
```

### Recover Stuck State

Read `references/troubleshooting.md`.

Common recovery commands:

```sh
./scripts/kv260-event-camera-switch.sh --stop-all
./scripts/kv260-recover-event-viewer.sh
./scripts/kv260-camera-viewer.sh --status
fuser -v /dev/video0 2>/dev/null || true
```

## Reference Navigation

- `references/setup-and-install.md`: Prophesee/PetaLinux setup, desktop packages, launchers, rootfs expansion.
- `references/viewer-and-recording.md`: custom viewer, native viewer, recording API, file formats, preview-vs-recording priority.
- `references/desktop-and-control-center.md`: local desktop launchers, Windows SSH X11, control center, file transfer GUI.
- `references/troubleshooting.md`: black/stalled preview, duplicate launchers, stale GUI, RDP/VNC limits, SFTP/SCP limits.
- `references/repo-map.md`: important scripts and docs in `kria-metavision-lab`.

## Related Skills

Use `kv260-windows-arduino` when Arduino light modulation or Windows-triggered recording is involved.

Use `aginti-agentlink` when coordinating multiple Codex/agent sessions across Windows, KV260, GitHub, and private history mirrors.

