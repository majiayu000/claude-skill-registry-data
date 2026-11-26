---
name: snx-run
description: "Run a recompiled game unattended and judge the result: scripted button input, timed exit, screenshots, reading the log, and repeat runs for intermittent crashes. Use when verifying a runtime change, reproducing a bug, checking a scene renders, measuring a crash rate, or when the user asks to run or test the game."
---

# Run the game

## One command

```bash
tools/run_game.py <id> --dump work/<Game>                 # 60 s with the default script
tools/run_game.py <id> --runs 5 --dump work/<Game>        # crash rate
tools/run_game.py <id> --seconds 20 --script "" --out "$SCRATCH/boot"  # boot only, no input
```

`<id>` is the game's folder in `recompiled/`, or in `games/` for one an older version made there: its title ID, or the
name it was recompiled under (`scarletnx -r work/<Game> NAME`). `work/<Game>` is the extracted dump.

`$SCRATCH` stands for the session's scratchpad directory: keep `--out` there, never in `/tmp` or the repo (without
`--out` it makes a new folder in `/tmp`). It runs the game from its folder, `recompiled/<id>/`, writes `runN.log` and
`runN.png` (the last frame, converted from the runtime's `.ppm` when Pillow is installed, otherwise `runN.ppm` stays
and it says so once) per run, and prints one line per run: the exit code (or `timeout`), then `ok`, the crash site (the signal from the
`*** Crash` header and the faulting thread's `pc`/`lr` after it, named with `--dump`) or the `svcBreak` reason, then
the frame count with the average FPS over `--seconds`. Options it doesn't know (`--fps_limit=0`, `-v`...) go to the
runtime. Look at the picture with the Read tool: a frame that "rendered" can still be black or garbage, and only the
picture shows it.

The runtime options behind it, for a run by hand from `recompiled/<id>/` (`./<id> --seconds=60 ...`):

| Option | Effect |
| --- | --- |
| `--seconds=N` | Exit after N seconds, printing `frames=N hash=...` (the last frame's hash) and writing `--shot`. They count from the game's start, after the shader loading screen (`prepare_shaders=2`), which ends after N seconds itself. The first run after a rebuild translates the game's shaders again there (seconds, or a minute in a big game) |
| `--frames=N` | Exit after N presented frames |
| `--shot=PATH` | Screenshot to `PATH.ppm` at exit |
| `--shot_every=N` | Also a numbered screenshot every N frames (`PATH_0000.ppm`, ...), needs `--shot` |
| `--script=ms:hex,...` | Press buttons at those times, each held 300 ms (`--press_len=ms` changes it). `Nf:hex` presses at the Nth presented frame instead. One press is a script of one entry: `--script=5000:1` |
| `--swkbd_text=TEXT` | The software keyboard answers TEXT instead of opening a dialog |
| `-v` | Log every IPC call (`IPC <interface> cmd N`, `nn::audio::detail::IAudioOut` for an audout): huge, grep it |
| `--fps_limit=0` | Unlimited frame rate |
| `--game=PATH` | Run the game PATH names (`recompiled/<id>`, the folder, runs `recompiled/<id>/<id>_code.so`) instead of the one the runtime is named after. Its log, caches and captures still go to that game's folders |

The timing, screenshot, press and script options are `platform/unattended.c`'s, shared by the SDL3 and headless
backends, so a headless build takes `--script` too. With `--seconds` or `--frames` the window doesn't go fullscreen. The SDL3 backend runs on Wayland
when the desktop has it. `SDL_VIDEO_DRIVER=x11` runs it on X11 instead: test a platform change on both.

Buttons (hex): A 1, B 2, X 4, Y 8, L 40, R 80, ZL 100, ZR 200, Plus 400, Minus 800, Left 1000, Up 2000, Right 4000,
Down 8000. Combine by adding. The values are 64-bit, and bits 40 to 47 push the sticks all the way: 40 left stick
left (`10000000000`), 41 up, 42 right, 43 down, then 44 to 47 the same for the right stick (`800000000000` is right
stick down).

`run_game.py`'s default script was written for one game's boot to its first cutscene: Plus at 15 s, A at 16 s, Plus
at 18 s, then A at 21, 31, 36, 40 and 44 s. Any other game needs its own `--script`. With save data from earlier runs the screens come
in a different order, so check the screenshots before trusting a script.

## Reading the log

The game's log, `recompiled/<id>/<id>.log` in a checkout (a data folder keeps it in its state folder, `docs/USAGE.md`
"Folders"), and the run log grow to megabytes. Never print it whole.

- `grep -n "Crash\|svcBreak\|FATAL" run1.log`: the failure, then `sed -n` around it.
- The log has no FPS line. `frames=N` at the end of a `--seconds` run, divided by the seconds, is the average frame
  rate (`run_game.py` prints it).
- `grep "vulkan:" run1.log | tail -3`: every 600 presents, the draws and skipped draws, compute dispatches and
  batches with the time spent waiting on them, and skipped dispatches. `WARN` lines with `vulkan: shader ... didn't
  compile` or `untranslated instructions` are rendering bugs.
- `video:` lines: NVDEC and VIC jobs. `romfs:` lines: files the game opened (movies are `.usm`).
- `threads.txt`, next to the game's log: every guest thread's state and wait, rewritten every 15 s. A hang is read from here.
- `diag=1` in the game's `.ini` saves the QMD and program of each new compute shader (the first 32) to
  `recompiled/<id>/captures/compute/`. F5 writes every game thread's state to the log at any time.
- RenderDoc (installed by the user): `--renderdoc=$SCRATCH/cap --renderdoc_frames=500,800` captures those
  presents (one guest frame each; `45s` is the first frame after 45 s on the `--script` clock, steadier on a loaded machine) to `$SCRATCH/cap_capture*.rdc`, and the log says `renderdoc: captured present N`.
  Run it with `SDL_VIDEO_DRIVER=x11`: RenderDoc has no Wayland surface, and on Wayland `vkCreateInstance` fails with
  VK_ERROR_EXTENSION_NOT_PRESENT. The capture layer slows the game (to about 20 fps in one test), so pick presents the run
  reaches, and expect a few hundred MB per capture. Captures hold the game's textures and buffers: they stay local.
  A capture stops the GPU thread for seconds. A game that waits only 1 s for its frame fences and then goes on can
  crash a little after a capture (one test game's arena deleter lists were overwritten): that crash is the capture's.
  Replay from scripts with RenderDoc's Python module (not in the Arch package): build it from the same tag with
  `-DENABLE_QRENDERDOC=OFF -DENABLE_PYRENDERDOC=ON` outside the repo and put its `lib/` on `sys.path`.
  With 1.46 on Arch, `-DENABLE_GL=OFF -DENABLE_GLES=OFF -DENABLE_EGL=OFF -DENABLE_WAYLAND=OFF` configures and the
  module builds in about 10 minutes (it fetches its own SWIG). Run scripts with `PYTHONPATH` and `LD_LIBRARY_PATH` both
  set to that `lib/`. `ReplayController` lists actions (`GetRootActions`), saves targets (`SaveTexture`), reads buffers
  (`GetBufferData`), and has `PixelHistory`, `DebugPixel` with `ContinueDebug`, and `GetPostVSData`: a pixel trace
  of a pass's samples finds which input is wrong faster than reading its SPIR-V. Under the layer a game runs about 3x
  slower, so a scene comes later on both the `s` clock and in presents: capture a few points across a long run.

Crash reports are handled with the `snx-crash` skill.

## Intermittent bugs

- One clean run proves nothing. Measure the rate before the fix with the same script and run count, then after, and
  put both in the commit message (for example "crashed 4 of 6 runs before, 0 of 20 after").
- Save data from earlier runs (`recompiled/<id>/<id>_data/save/`) changes what the game does at boot. A rate measured with
  one save state is not comparable with one measured with another. To start fresh, move the save folder aside
  (outside `recompiled/`), never delete it without asking.
- Don't build or run anything heavy while measuring: timing changes the rate.
- Runs are sequential. Two games at once share the GPU and the saves.

## Stopping a game

`pgrep -a` with the title ID's first 15 characters (Linux keeps 15 of a process name), then `kill PID`. Never `pkill`, which matches the shell running it.
