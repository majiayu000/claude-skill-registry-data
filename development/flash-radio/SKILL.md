---
name: flash-radio
description: Compile the PhoenixSketch production firmware and flash it to the Teensy 4.1 radio over USB. Use when the user asks to build, compile, upload, flash, deploy, or program the radio / Teensy / Phoenix firmware.
---

# flash-radio

Compiles `code/src/PhoenixSketch/PhoenixSketch.ino` with `arduino-cli` and uploads the resulting `.hex` to the connected Teensy 4.1.

## Build settings — read them, do not retype them

`code/.vscode/arduino.json` is the single source of truth. Do **not** hardcode the FQBN
in a command: this file has drifted from copies pasted into skills before (the CPU speed
and optimisation flags changed), and a stale FQBN silently builds a different binary.

Read the values into shell variables first, and use those for every subsequent command:

```bash
cd /home/oliver/Sync/Ham/T41/Software/Phoenix/code
CFG=.vscode/arduino.json
FQBN="$(jq -r '.board + ":" + .configuration' "$CFG")"
SKETCH="$(jq -r .sketch "$CFG")"
OUTDIR="$(jq -r .output "$CFG")"
PORT="$(jq -r .port "$CFG")"
echo "FQBN=$FQBN  SKETCH=$SKETCH  OUTDIR=$OUTDIR  PORT=$PORT"
```

Echo them so the values used are visible in the transcript. As of 2026-07-30 that yields
`teensy:avr:teensy41:usb=serial2,speed=528,opt=o2lto,keys=en-us`, sketch
`src/PhoenixSketch/PhoenixSketch.ino`, output `../ArduinoOutput`, port `/dev/ttyACM0` —
but read the file, do not trust this paragraph.

`usb=serial2` is Dual Serial: the radio enumerates as two ports. The first
(`/dev/ttyACM0`) is diagnostics and the flashing port; the second (`/dev/ttyACM1`) is CAT
at 38400.

## Steps

1. **Check the board is connected.**
   ```bash
   arduino-cli board list
   ```
   A connected radio shows a `Teensy Ports` row with FQBN `teensy:avr:teensy41`. The
   `/dev/ttyACM*` rows show `Unknown` — that is normal, not a problem. If no Teensy row
   appears at all, stop and tell the user to connect/power the radio.

2. **Compile and upload in one step.** This is the reliable path — see "Why one step"
   below.
   ```bash
   arduino-cli compile --upload -p "$PORT" \
     --fqbn "$FQBN" \
     --output-dir "$OUTDIR" \
     "$SKETCH"
   ```
   Use a generous Bash timeout (600000 ms / 10 min); a cold build takes minutes, a cached
   one is quick. If compilation fails, surface the first error and stop — `--upload` will
   not flash a broken build, but say so explicitly rather than letting the failure look
   like an upload problem.

3. **Confirm the board came back.** A successful flash reboots the Teensy and the ports
   re-enumerate:
   ```bash
   sleep 4 && ls -l /dev/ttyACM*
   ```
   The timestamps should be seconds old. If the radio is meant to be usable afterwards,
   a `printf 'IF;' > /dev/ttyACM1` should answer.

4. **Report.** One or two lines: compile result, upload result, notable warnings. The
   tree builds with many pre-existing `-Wunused-*` warnings — do not report those as new.

## Expected output, and what is not an error

- **`Teensy should be selected from "teensy ports" rather than "Serial ports"`** — a
  harmless warning printed on every upload. Ignore it.
- **`New upload port: /dev/ttyACM0 (serial)`** — success.
- A successful run ends with the memory-usage table and no `Failed uploading:` line.
  Check the exit status rather than eyeballing, since the warning above looks alarming.

## Why one step, and how to re-flash without recompiling

A separate `arduino-cli upload` **fails** on this setup in two different ways, both
verified on 2026-07-30:

| Command | Result |
| --- | --- |
| `upload --input-dir ../ArduinoOutput [sketch]` | `Teensy Loader could not find the file PhoenixSketch.ino` — fails with or without the trailing sketch argument |
| `upload --input-file ../ArduinoOutput/PhoenixSketch.ino.hex` | `Teensy Loader is unable to read your compiled sketch` |
| `upload --input-file /abs/path/.../PhoenixSketch.ino.hex` | **works** |
| `compile --upload -p PORT` | **works** |

The Teensy loader cannot resolve relative paths. So to re-flash an existing build without
recompiling, pass an **absolute** path to the `.hex`:

```bash
arduino-cli upload -p "$PORT" --fqbn "$FQBN" \
  --input-file /home/oliver/Sync/Ham/T41/Software/Phoenix/ArduinoOutput/PhoenixSketch.ino.hex
```

Otherwise prefer step 2 — arduino-cli caches the build, so re-running `compile --upload`
against an unchanged tree costs little.

## If the upload hangs or the board does not reboot

The Teensy's auto-reboot into the bootloader is unreliable. If the upload sits waiting,
ask the user to **press the PROGRAM button on the Teensy**, then re-run the step-2
command. Do not keep retrying without telling them — nothing will happen until the button
is pressed.

## Args

- `compile-only` — run the compile without `--upload`; skip the flash. Useful when no
  board is connected or the user just wants to verify the build.
- `flash-only` — skip the compile and re-flash what is already in `$OUTDIR`, using the
  absolute-path `--input-file` form above. Only valid if that directory holds a recent
  build of this sketch; otherwise fall back to a full compile and say that you did.

## Notes

- Always run from `code/` so the relative paths in `arduino.json` resolve.
- Do **not** use this skill for the unit tests — those are CMake under `code/test/build/`
  and are a separate workflow (`run-tests`).
- `code/build/` is the CMake test build; firmware artifacts go to `ArduinoOutput/` at the
  repo root.
- There is no `code/lib/` in this tree. If a future build needs in-tree forked libraries,
  add `--libraries lib` — but do not pass it while that directory is absent.
