---
name: vm-lab
description: "Parallels macOS VM lab: GUI automation, Peekaboo, TCC, Ghostty."
---

# VM Lab

Use this when the task needs a clean macOS VM to test GUI automation, TCC prompts, screenshot capture, clicking, typing, performance, or "two-way validation" of Peekaboo-like tools.

Core idea: run the tool under test inside the guest, but verify it from outside the guest with Parallels screenshots and host-side observations. Do not close apps you do not own.

## Safety Rules

- Treat the VM snapshot as disposable, not the host.
- Never print secrets. If `op` is needed, follow the 1Password skill and run it only inside `tmux`.
- Prefer fresh app windows you create yourself: TextEdit, a local HTML test page, or a small test app.
- Avoid modifying host state except temporary screenshots under `/tmp`.
- For git repos inside the VM, use HTTPS remotes and normal branch discipline.

## VM Discovery

List VMs:

```bash
prlctl list --all
```

Get VM status/IP:

```bash
prlctl list --info "macOS Tahoe"
```

Run guest commands as Peter:

```bash
prlctl exec "macOS Tahoe" \
  'sudo -u steipete -H /bin/zsh -lc '\''source ~/.zprofile 2>/dev/null || true; uname -a'\'''
```

Capture an independent host-side screenshot:

```bash
prlctl capture "macOS Tahoe" --file /tmp/vm-reference.png
sips -g pixelWidth -g pixelHeight /tmp/vm-reference.png
```

## TCC / GUI Attribution

For macOS Screen Recording and Accessibility, the responsible process matters.

- `prlctl exec` is headless and can fail to produce useful Screen Recording attribution.
- Launch the test command from a visible terminal app in the guest when Screen Recording is involved.
- Ghostty works as a GUI terminal if installed.
- After a first failed capture, check `System Settings > Privacy & Security > Screen & System Audio Recording`.
- `permissions status` run through `prlctl exec` may still report Screen Recording false after Ghostty is allowed; validate Screen Recording by rerunning the capture from Ghostty.

Open the Screen Recording pane:

```bash
prlctl exec "macOS Tahoe" \
  'sudo -u steipete -H open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"'
```

Open Ghostty:

```bash
prlctl exec "macOS Tahoe" 'sudo -u steipete -H open -a Ghostty'
```

## Running Commands Through Ghostty

Best path: create a guest script with `prlctl exec`, open/focus Ghostty, then type only a short launcher path into the visible terminal.

Guest script pattern:

```bash
prlctl exec "macOS Tahoe" 'sudo -u steipete -H /bin/zsh -lc '\''cat > /tmp/run-vm-lab.zsh <<EOF
#!/bin/zsh
source ~/.zprofile 2>/dev/null || true
cd ~/Projects/Peekaboo || exit 1
Apps/CLI/.build/debug/peekaboo image --path /tmp/peekaboo-vm.png --json
rc=$?
echo "EXIT:$rc"
[ -f /tmp/peekaboo-vm.png ] && sips -g pixelWidth -g pixelHeight /tmp/peekaboo-vm.png
echo "Press return to close..."
read _
exit $rc
EOF
chmod +x /tmp/run-vm-lab.zsh
ln -sf /tmp/run-vm-lab.zsh /tmp/r
open -a Ghostty'\'''
```

Then link the launcher into Ghostty's home directory and type `./r` with `scripts/parallels_type.py`. This avoids unreliable path characters in Parallels key injection.

```bash
prlctl exec "macOS Tahoe" \
  "sudo -u steipete -H /bin/zsh -lc 'ln -sf /tmp/run-vm-lab.zsh ~/r'"
python3 skills/vm-lab/scripts/parallels_type.py "macOS Tahoe" $'./r\n'
```

Avoid long command typing. Parallels key injection uses its own key-code table and can be layout-sensitive.

## Known Pitfalls

- macOS clipboard APIs may fail from `prlctl exec`; `pbcopy`, AppleScript clipboard, and Peekaboo paste can all fail in headless guest context.
- `open -na Ghostty.app --args -e ...` may only focus an existing Ghostty window on macOS; do not assume it runs the command.
- `prlctl exec` may re-join argv through a guest shell; for complex payloads, pass one fully shell-quoted command string or create the file with a tiny Python writer.
- Parallels `send-key-event --key` uses Parallels key values, not macOS virtual key codes.
- For normal typing, send `prlctl send-key-event <vm> --key <key>` with no `--event`; explicit `press`/`release` can repeat or stick. Return is an exception: use press then release.
- Prefer one `prlctl send-key-event --json` batch over many separate `send-key-event` processes; separate calls can drift under focus/latency.
- Use `PRL_KEY_ENTER = 36`, `PRL_KEY_SLASH = 61`, `PRL_KEY_R = 27`, `PRL_KEY_T = 28`, `PRL_KEY_M = 58`, `PRL_KEY_P = 33`.
- If keystrokes produce garbage, send Return to clear the line, create a shorter launcher, then retry.
- If Peekaboo permission probes hang with Screen Recording missing and emit `SWIFT TASK CONTINUATION MISUSE`, record it as a product bug; do not confuse it with the VM harness.

## Two-Way Validation

For each GUI action, verify through two independent signals:

- Tool-under-test output: JSON, screenshot file, AX result, or app state.
- External verifier: `prlctl capture`, host-side image inspection, file content in guest, or process/window state.

Examples:

- Screenshot: compare Peekaboo image dimensions/content against `prlctl capture`.
- Click: use Peekaboo to click a test button, then verify both guest app state and host screenshot.
- Type: use Peekaboo to type into a controlled text field, then verify AX value and host screenshot.
- Performance: wrap commands with `/usr/bin/time -p`; repeat cold/warm runs; keep outputs in `/tmp`.

## Peekaboo VM Baseline

Inside guest:

```bash
cd ~/Projects/Peekaboo
git pull --recurse-submodules
swift build --package-path Apps/CLI
Apps/CLI/.build/debug/peekaboo --version
Apps/CLI/.build/debug/peekaboo permissions status --json
```

Host-side reference capture:

```bash
prlctl capture "macOS Tahoe" --file /tmp/vm-prlctl-reference.png
```

Guest-side Peekaboo capture through Ghostty:

```bash
/tmp/r
```

Compare:

```bash
prlctl exec "macOS Tahoe" \
  'sudo -u steipete -H /bin/zsh -lc '\''sips -g pixelWidth -g pixelHeight /tmp/peekaboo-vm.png'\'''
sips -g pixelWidth -g pixelHeight /tmp/vm-prlctl-reference.png
```

## Reporting

When handing off, include only:

- VM name and OS build.
- repo commit tested.
- permission state.
- commands that passed/failed.
- independent verifier result.
- product bugs discovered.
