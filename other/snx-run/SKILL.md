---
name: snx-run
description: "Run a recompiled game unattended and judge the result. It covers scripted button input, a timed exit, screenshots, the log, and repeat runs for intermittent crashes. Use it when you verify a runtime change or reproduce a bug. Use it also to check that a scene renders or to measure a crash rate. Use it when the user asks to run or test the game."
---

# Run the game

## One command

```bash
tools/run_game.py <id> --dump work/<Game>                 # 60 s with the default script
tools/run_game.py <id> --runs 5 --dump work/<Game>        # crash rate
tools/run_game.py <id> --seconds 20 --script "" --out "$SCRATCH/boot"  # boot only, no input
```

`<id>` is the folder of the game in `recompiled/`. For a game that an older version made in `games/`, it is the folder
there. The folder name is the title ID, or the name of the recompile (`scarletnx -r work/<Game> NAME`). `work/<Game>`
is the extracted dump.

`$SCRATCH` is the scratchpad directory of the session. Keep `--out` there, never in `/tmp` or in the repo. Without
`--out`, the script makes a new folder in `/tmp`.

The script runs the game from its folder, `recompiled/<id>/`. For each run, it writes `runN.log` and `runN.png`, which
is the last frame. The script converts `runN.png` from the `.ppm` of the runtime when Pillow is on the machine. If
Pillow is not there, `runN.ppm` stays and the script says so one time.

For each run, the script prints one line with these items:
- The exit code (or `timeout`).
- `ok`, the crash site or the `svcBreak` reason. The crash site is the signal from the `*** Crash` header and the
  `pc`/`lr` of the thread with the fault after it. `--dump` gives names to these addresses.
- The frame count with the average FPS over `--seconds`.

The script gives the options that it does not know (`--fps_limit=0`, `-v`...) to the runtime. Look at the picture
with the Read tool. A frame that "rendered" can still be black or garbage, and only the picture shows it.

These are the runtime options behind the script, for a run by hand from `recompiled/<id>/` (`./<id> --seconds=60 ...`):

| Option | Effect |
| --- | --- |
| `--seconds=N` | Exit after N seconds. At exit, the runtime prints `frames=N hash=...` (the hash of the last frame) and writes `--shot`. The seconds count from the start of the game, after the shader load screen (`prepare_shaders=2`). That screen also ends after N seconds. The first run after a rebuild translates the shaders of the game again on that screen (seconds, or a minute in a big game). |
| `--frames=N` | Exit after N presented frames |
| `--shot=PATH` | Write a screenshot to `PATH.ppm` at exit |
| `--shot_every=N` | Also write a numbered screenshot every N frames (`PATH_0000.ppm`, ...). It needs `--shot`. |
| `--script=ms:hex,...` | Press buttons at those times. The runtime holds each press for 300 ms (`--press_len=ms` changes it). `Nf:hex` presses at the Nth presented frame instead. One press is a script of one entry: `--script=5000:1` |
| `--swkbd_text=TEXT` | The software keyboard answers TEXT and does not open a dialog |
| `--pause=at:len,...` | Pause the whole game at `at` ms for `len` ms. Each pause logs if guest memory and guest time stayed unchanged (`grep "pause:"`). |
| `--state_save=at:slot,...`, `--state_load=at:slot,...` | Save the game to a save state slot, or load a slot, at `at` ms (`grep "state:"`). A later run can load a slot that an earlier run saved. A slot that names a file (`0:/path/x.snxstate`) is that file. |
| `--state_check=at,...` | A save state round trip at `at` ms. The runtime saves, loads the state again immediately, and logs `state: check:`. The log tells if guest memory and guest time came back the same. |
| `-v` | Log every IPC call (`IPC <interface> cmd N`, `nn::audio::detail::IAudioOut` for an audout). The log gets very large, so use grep on it. |
| `--fps_limit=0` | No limit on the frame rate |
| `--game=PATH` | Run the game that PATH names, not the game that gives the runtime its name. `recompiled/<id>`, the folder, runs `recompiled/<id>/<id>_code.so`. The log, caches and captures still go to the folders of the game that gives the runtime its name. |

The time, screenshot, press and script options come from `platform/unattended.c`. The SDL3 and headless backends
share that file, so a headless build also takes `--script`. With `--seconds` or `--frames`, the window does not go
fullscreen. The SDL3 backend runs on Wayland when the desktop has it. `SDL_VIDEO_DRIVER=x11` runs it on X11 instead.
Test a platform change on both.

The buttons have these hex values: A 1, B 2, X 4, Y 8, L 40, R 80, ZL 100 and ZR 200. Plus is 400, Minus 800,
Left 1000, Up 2000, Right 4000 and Down 8000. Combine buttons with addition.

The values are 64-bit. Bits 40 to 47 push the sticks all the way. Bit 40 pushes the left stick to the left
(`10000000000`), 41 up, 42 right and 43 down. Bits 44 to 47 do the same for the right stick (`800000000000` is right
stick down). Bit 48 (`1000000000000`) is Home. It opens the menu of the game, and closes it.

While the menu is open, the scripted A, B and D-pad move in it, as the buttons of a pad do. The Save states page of
the menu holds the game while the page shows.

The default script of `run_game.py` is for the boot of one game to its first cutscene. It presses Plus at 15 s, A at
16 s, Plus at 18 s, then A at 21, 31, 36, 40 and 44 s. Any other game needs its own `--script`. With save data from
earlier runs, the screens come in a different order. Thus check the screenshots before you trust a script.

## Read the log

In a checkout, the log of the game is `recompiled/<id>/<id>.log`. A data folder keeps it in its state folder
(`docs/USAGE.md`, "Folders"). The game log and the run log grow to megabytes. Never print a log whole.

- `grep -n "Crash\|svcBreak\|FATAL" run1.log` finds the failure. Then use `sed -n` to read the lines around it.
- The log has no FPS line. To get the average frame rate, divide `frames=N` at the end of a `--seconds` run by the
  seconds. `run_game.py` prints it.
- `grep "vulkan:" run1.log | tail -3` shows a line for every 600 presents. The line gives the draws and the skipped
  draws. It also gives the compute dispatches and batches, with the time that the runtime waited on them, and the
  skipped dispatches. `WARN` lines with `vulkan: shader ... didn't compile` or `untranslated instructions` show bugs
  in the renderer.
- `video:` lines show NVDEC and VIC jobs. `romfs:` lines show the files that the game opened (movies are `.usm`).
- `threads.txt`, next to the log of the game, gives the state and wait of every guest thread. The runtime writes it
  again every 15 s. Read a hang from this file.
- `diag=1` in the `.ini` of the game saves the QMD and program of each new compute shader (the first 32) to
  `recompiled/<id>/captures/compute/`. F5 writes the state of every game thread to the log at any time.
- RenderDoc (the user installs it): `--renderdoc=$SCRATCH/cap --renderdoc_frames=500,800` captures those presents to
  `$SCRATCH/cap_capture*.rdc`. Each present is one guest frame. `45s` is the first frame after 45 s on the `--script`
  clock, which is steadier on a machine with a high load. The log says `renderdoc: captured present N`.

  RenderDoc has no Wayland surface. On Wayland, `vkCreateInstance` fails with VK_ERROR_EXTENSION_NOT_PRESENT. Thus
  run it with `SDL_VIDEO_DRIVER=x11`. The capture layer slows the game (to about 20 fps in one test). Thus pick
  presents that the run gets to. Expect a few hundred MB for each capture.

  Captures hold the textures and buffers of the game. They stay on this machine. A capture stops the GPU thread for
  seconds. A game can wait only 1 s for its frame fences and then continue. Such a game can crash a short time after
  a capture (one test game found its arena deleter lists overwritten). That crash comes from the capture.

  To replay from scripts, use the Python module of RenderDoc. The Arch package does not include it. Build it from the
  same tag with `-DENABLE_QRENDERDOC=OFF -DENABLE_PYRENDERDOC=ON`, outside the repo. Put its `lib/` on `sys.path`.
  With 1.46 on Arch, the configure works with
  `-DENABLE_GL=OFF -DENABLE_GLES=OFF -DENABLE_EGL=OFF -DENABLE_WAYLAND=OFF`. The module then builds in about
  10 minutes (it fetches its own SWIG).

  Run scripts with `PYTHONPATH` and `LD_LIBRARY_PATH` both set to that `lib/`. `ReplayController` lists actions
  (`GetRootActions`), saves targets (`SaveTexture`) and reads buffers (`GetBufferData`). It also has `PixelHistory`,
  `DebugPixel` with `ContinueDebug`, and `GetPostVSData`. A pixel trace of the samples of a pass finds the wrong input
  faster than a read of its SPIR-V. Under the layer, a game runs about 3x slower. Thus a scene comes later on the `s`
  clock and also in presents.

  Capture a few points across a long run.

For crash reports, use the `snx-crash` skill.

## Intermittent bugs

- One clean run proves nothing. Measure the rate before the fix and after it, with the same script and run count.
  Put both rates in the commit message (for example "crashed 4 of 6 runs before, 0 of 20 after").
- Save data from earlier runs (`recompiled/<id>/<id>_data/save/`) changes what the game does at boot. Do not compare
  a rate from one save state with a rate from another. To start fresh, move the save folder aside (outside
  `recompiled/`). Never delete it before you ask the user.
- Do not build or run a heavy job while you measure. Any change in speed changes the rate.
- Do the runs one after the other. Two games at the same time share the GPU and the saves.

## Stop a game

Run `pgrep -a` with the first 15 characters of the title ID (Linux keeps 15 characters of a process name). Then run
`kill PID`. Never use `pkill`, because it matches the shell that runs it.
