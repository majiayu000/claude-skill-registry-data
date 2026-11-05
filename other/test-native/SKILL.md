---
name: test-native
description: Reproduce and measure Claude Desktop behavior in a Linux session that is not the host's - a nested sway/wlroots compositor (native Wayland, XWayland, hidden workspaces, another XDG_CURRENT_DESKTOP) driven by scripted input and screenshots, plus run-time probes injected into the Electron client when the needed data is not in any log. Use when a report comes from Wayland/sway/Hyprland/GNOME/KDE and the host runs something else, when X11 vs Wayland must be compared, when a window must be hidden/occluded/on another workspace, or when a renderer or main-process value must be measured in the running app.
argument-hint: "<what to reproduce or measure, and in which session type>"
---

# test-native - nested compositor + in-app probes

Goal: **$ARGUMENTS**

Two tools, used together or alone:

1. A **nested sway** gives a real Wayland session with workspaces, focus and
   frame callbacks, on any host (X11 desktop, Wayland desktop, or no display at
   all), with scripted mouse/keyboard and screenshots. It is not a substitute
   for GNOME/KDE-specific behavior (portals, KWin, mutter); for those use the
   VMs in AGENTS.md ("Test VMs").
2. **Probes injected into the app** measure what no log shows (frames,
   observers, focus, timers, IPC shapes) and let several candidate fixes ship
   in ONE debug build, switched by environment variables, so each variant is a
   relaunch, not a rebuild.

Read `/linux` for the session/DE routing the launcher does; this skill is
about producing those sessions and reading the app from inside.

## 1. Nested sway

sway is packaged everywhere (`sway`; `grim` for screenshots and `wtype` for
typing are small extras worth installing). Pick the backend by host:

| Host | Start | Notes |
|---|---|---|
| X11 desktop (XFCE, i3, ...) | `WLR_BACKENDS=x11 sway` | a 1024x768 window; resize with `swaymsg output X11-1 resolution 1600x1000` |
| Wayland desktop (KDE, GNOME, sway) | `WLR_BACKENDS=wayland sway` | a nested window inside the host compositor |
| none / CI | `WLR_BACKENDS=headless WLR_LIBINPUT_NO_DEVICES=1 WLR_RENDERER=pixman sway` | no window; screenshots via `grim` |

Always start it with a minimal config (`-c`) so the host's `~/.config/sway`
bindings do not interfere, and talk to it through its own socket:

```bash
printf 'output * resolution 1600x1000\ndefault_border none\n' > /tmp/sway-test.conf
WLR_BACKENDS=x11 sway -c /tmp/sway-test.conf &
export SWAYSOCK=$(ls -t /run/user/$(id -u)/sway-ipc.*.sock | head -1)
swaymsg -t get_outputs | jq -r '.[].name'            # X11-1 / HEADLESS-1 / WL-1
ls /run/user/$(id -u)/wayland-*                        # the nested display, e.g. wayland-1
```

`-c` replaces `~/.config/sway/config` entirely, so host bindings and outputs
never apply. The nested instance also starts its own XWayland (`:1` when the
host owns `:0`); check with `ss -xlp | grep X11-unix`.

### Launch the app INTO the nested session

A plain `claude-desktop` inherits the host's `XDG_SESSION_TYPE`/`DISPLAY` and
opens on the host desktop. Set the session variables explicitly; the launcher
tests `XDG_SESSION_TYPE` first:

```bash
# native Wayland, sway routing
swaymsg exec 'env -u DISPLAY WAYLAND_DISPLAY=wayland-1 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=sway claude-desktop'
# XWayland comparison (same compositor, X11 code path)
swaymsg exec 'env DISPLAY=:1 WAYLAND_DISPLAY=wayland-1 XDG_SESSION_TYPE=wayland CLAUDE_USE_XWAYLAND=1 claude-desktop'
# pretend to be another desktop for the launcher's routing (CU bridges, tray, portals)
...  XDG_CURRENT_DESKTOP=KDE  ...     # see /linux for what each value changes
```

Only one instance per profile runs at a time: quit the host's Claude first
(`pkill -f '^/usr/lib/claude-desktop/claude --enable'`, wait for the process
to go). Confirm where it landed: `swaymsg -t get_tree | jq -c '.. | objects |
select(.pid?) | {id,name,shell}'` lists the app's windows with `xdg_shell`
(native) or `xwayland`. Confirm the ozone platform with `pgrep -af claude |
grep -o 'ozone-platform=[a-z]*'`.

`--remote-debugging-port` and other debugging switches make the app refuse
to start; DevTools come from `developer_settings.json` instead (section 2).

### Windows and workspaces

```bash
swaymsg '[title="^Test$"] move container to workspace 2'; swaymsg workspace 2   # hide everything else
swaymsg '[title="^Claude$"] focus'
swaymsg '[title="^Test$"] floating enable, resize set 1400 850, move position 50 60'
swaymsg -t get_workspaces | jq -c '.[] | {name,visible}'
```

A window on a non-visible workspace gets **no frame callbacks** - that is the
Wayland behavior sway, GNOME and KDE share and the reason native-Wayland
reports differ from X11 (#280).

### Input

Mouse: sway's own seat, in layout coordinates - this reaches the app exactly
like a real pointer (xdotool clicks on an X11 host only move focus):

```bash
clk() { swaymsg -q "seat - cursor set $1 $2"; sleep 0.2; swaymsg -q "seat - cursor press button1"; sleep 0.1; swaymsg -q "seat - cursor release button1"; }
clk 1100 976
```

Keyboard: `wtype` (virtual-keyboard protocol, works on every host backend):

```bash
WAYLAND_DISPLAY=wayland-1 wtype -M ctrl -M alt i -m alt -m ctrl     # chord
WAYLAND_DISPLAY=wayland-1 wtype -d 15 "$(cat snippet.js)"            # text, 15 ms per key
```

If only `xdotool` is available (X11 host): match layouts first
(`swaymsg input type:keyboard xkb_layout de` to whatever `setxkbmap -query`
says), **verify focus before every key** (`xdotool getwindowfocus
getwindowname` must be the sway window AND `swaymsg -t get_tree | jq '.. |
objects | select(.focused==true) | .name'` the intended app window), never
click to focus, and screenshot before pressing Enter. Text that lands in the
chat composer gets SENT as a prompt to a Code session. Known oddity: single
letters can be swallowed on the X11 backend; `wtype` does not have it. The
host clipboard does not reach the nested session (XWayland's bridge did not
deliver to Chromium); do not plan on Ctrl+V.

### Screenshots

```bash
WAYLAND_DISPLAY=wayland-1 grim shot.png                               # any backend, needs grim
import -window "$(xwininfo -root -tree | awk '/wlroots - X11-1/{print $1}')" shot.png   # X11 host fallback
```

Crop with `-crop WxH+X+Y +repage` (ImageMagick) and read the image, or probe
a pixel region numerically for loops:
`import -window $W -crop 200x150+940+780 +repage -colorspace gray -format '%[fx:mean]' info:`.

### Caveats

- Rendering is software (pixman/llvmpipe) - CPU numbers are not representative
  of a GPU desktop; compare variants against each other, not against the host.
- The nested sway is sway, not the reporter's compositor. KWin/mutter-specific
  behavior (portals, tiling, activation) needs the VMs.
- Keep the user's hands off the window while a scripted loop runs, and say so;
  two sets of clicks produce garbage results.

## 2. Probes inside the Electron client

### Where output goes

| From | Call | Lands in |
|---|---|---|
| main process | `globalThis.__cdbDiag("[tag] ...")` (exists after upstream's `ready`; queue before that - see `js/popout_frames_main.js`) | `~/.config/Claude/logs/claude-patches.log` |
| main view (renderer) | `console.warn/info/error("[tag] ...")` | `~/.config/Claude/logs/claude.ai-web.log` |
| CLI child | `logs/custom-models.log` style files | see AGENTS.md "Logs" |

3P mode uses `~/.config/Claude-3p/`; profiles add `-<name>`.

### DevTools without a rebuild

`~/.config/Claude/developer_settings.json` -> `{"allowDevTools": true}`
(or the Extra -> Community Features "Developer tools" row), then
**Ctrl+Alt+I** on the focused window (undocked). Upstream re-reads the file
on every press. Limits inside the console: the page CSP blocks `eval` and
dynamic `import` of fetched code, XHR to localhost needs CORS; type or paste
the code itself. For anything longer than a line, prefer the debug patch.

### The debug-patch recipe (one build, many variants)

Copy the shape of `patches/linux/fix_popout_menus_wayland.nim` +
`js/popout_frames_main.js` + `js/popout_frames_page.js`:

1. A head-injected main module (`"use strict"` anchor with the prepend
   fallback) that registers `app.on("web-contents-created")` ->
   `wc.on("dom-ready")` -> `wc.executeJavaScript(PAGE_SRC)` for the main-view
   origins (`https://claude.ai/...`, `app://localhost/...` minus
   `setup-desktop-3p`). `executeJavaScript` is not subject to the page CSP.
2. The page script measures and logs every N seconds (template:
   `reference/probe.js`): real `requestAnimationFrame` cadence, ResizeObserver
   latency, `document.visibilityState`, `hasFocus()`, plus the counters of
   whatever shim is under test.
3. Candidate fixes are gated by `process.env.CDB_<FEATURE>_*` read in the
   main module and passed to the page as a JSON config (replace the
   placeholder with `split/join`, not `replace`, if the placeholder string
   also appears in a comment). Each variant is then a relaunch with different
   env vars; the user installs once.
4. Bump `EXPECTED_PATCH_COUNT`, build with `./scripts/build-local.sh`, let the
   user install, relaunch into the nested session, read the two logs.
5. Strip the probe and the losing variant before the real patch ships;
   keep an env escape hatch for the winner if it is cheap.

Remember what the 1P main view is: **remote claude.ai code**. A patch on
`resources/ion-dist` (shipped packed as `resources/ion-dist.asar`) only reaches
3P mode (`app://localhost`); run-time injection reaches both.

### Reading the data

Baseline first (both windows visible), then the condition under test, then
the control (e.g. XWayland). A result is a before/after pair in the same log
with timestamps, not a single number. Quote the lines in the report.
