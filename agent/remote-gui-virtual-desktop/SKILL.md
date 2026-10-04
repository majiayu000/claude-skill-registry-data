---
name: remote-gui-virtual-desktop
description: Use when launching, controlling, documenting, debugging, or cleaning up remote Linux GUI apps through a clean Xvfb desktop, x11vnc, noVNC/websockify, browser app windows, SSH-local ports, or camera/GUI process isolation. Applies to LabVIEW, KiCad, JLCEDA, FreeCAD, Blender GUI, vendor camera tools, license activation flows, and other agent-controlled desktop apps.
---

# Remote GUI Virtual Desktop

Run GUI applications on an isolated X display that the user and agent can view
without disturbing the physical desktop. Keep VNC and noVNC bound to localhost.

## Default Pattern

1. Allocate a dedicated display and ports, such as X `:98`, VNC `5908`, and
   noVNC `6099`.
2. Start a 24-bit X display and localhost-only transport:

```bash
Xvfb :98 -screen 0 1920x1080x24 -ac
x11vnc -display :98 -localhost -nopw -forever -shared -rfbport 5908
websockify -D --web=/usr/share/novnc 127.0.0.1:6099 127.0.0.1:5908
```

3. Launch the app with explicit X context:

```bash
DISPLAY=:98 XAUTHORITY= /path/to/gui-app
```

4. Default to the full noVNC client with scale-to-view enabled:

```text
http://127.0.0.1:6099/vnc.html?host=127.0.0.1&port=6099&autoconnect=1&resize=scale
```

Do not default to `vnc_lite.html`, `scale=1`, or `resize=remote`. Preserve a
lite-client URL only for an explicitly requested legacy deployment. The full
client keeps the whole remote canvas visible and provides the clipboard panel.

## Default Autofit Contract

Autofit has two required layers:

1. noVNC uses `resize=scale` to fit the remote canvas inside the local browser.
2. The remote app's main window is moved to `(0, 0)` and resized to the X root
   dimensions so it cannot extend beyond that canvas.

Use PID-based window discovery first. Class/name matching is only a fallback on
a dedicated display.

```bash
fit_window_to_display() {
  local display="$1" window="$2" width height
  read -r width height < <(
    DISPLAY="$display" XAUTHORITY= xdotool getdisplaygeometry
  )
  DISPLAY="$display" XAUTHORITY= xdotool \
    windowmap "$window" \
    windowmove --sync "$window" 0 0 \
    windowsize --sync "$window" "$width" "$height" \
    windowraise "$window"
}

window="$(
  DISPLAY=:98 XAUTHORITY= xdotool search --onlyvisible --pid "$app_pid" \
    | tail -n 1
)"
fit_window_to_display :98 "$window"
```

Apply the fit after launch and after restore/unminimize. If an app replaces a
small login/QR dialog with a different main window, run a lightweight guard
every 1-2 seconds while the app is alive. Center fixed-size login dialogs; fit
the main window once it reaches a normal application size. Stop the guard with
the desktop session. Do not spawn duplicate guards for the same display/app.

Before force-resizing, check whether the application implements one logical UI
with several synchronized top-level/layered windows, as WeCom does under Wine.
Moving only one layer fragments that UI. For such applications, preserve native
window geometry, center only the login dialog when safe, and rely on full noVNC
`resize=scale` to fit the complete desktop.

## AgInTi Browser / Xiaoyunque Identity

On Lachlan's workstation, preserve this established browser identity:

```text
X display: :98
VNC: 127.0.0.1:5908
noVNC: http://127.0.0.1:6099/vnc.html?host=127.0.0.1&port=6099&autoconnect=1&resize=scale
AgInTi Browser: http://127.0.0.1:8794
Chrome CDP: http://127.0.0.1:9344
Chrome profile: $HOME/.cache/xyq-chrome
```

This identity belongs to AgInTi Browser and Xiaoyunque. Reuse it when the user
asks for that familiar browser or its download history. Do not substitute an
embedded, temporary, or default virtual-desktop profile. Never delete,
overwrite, expose private state from, or commit the profile. Do not open JLC
tabs in this browser, and do not stop or reopen it while preparing a JLC order.

JLC web ordering has a separate AgenticApp stack:

```text
X display: :104
VNC: 127.0.0.1:5924
noVNC: http://127.0.0.1:6124/vnc.html?host=127.0.0.1&port=6124&autoconnect=1&resize=scale
Chrome CDP: http://127.0.0.1:49237
Chrome profile: $HOME/.cache/jlcpcb-order-shared
Launcher: agentic_tools/jlcpcb_order_agent/scripts/jlc_browser_stack.sh
```

The JLC profile name is historical; it is dedicated to JLC runs. Repeated
launcher calls reuse the existing JLC process and tab. `JLCPCB_TAB_CDP_PORT` is
intentionally unsupported. LCEDA Pro's Electron state and the Books/LibGen
browser remain separate.

## AgenticApp Launcher

When working in AgenticApp, prefer:

```bash
agentic_tools/virtual_desktop/launch_virtual_desktop.sh \
  --name APP_NAME \
  --display :98 \
  --screen 1920x1080x24 \
  --vnc-port 5908 \
  --novnc-port 6099 \
  --open-browser \
  -- /path/to/gui-app
```

The launcher or app-specific wrapper should implement the autofit contract,
including persistent re-fit for applications that recreate their windows.

## Verification

```bash
curl -fsS -o /dev/null \
  'http://127.0.0.1:6099/vnc.html?host=127.0.0.1&port=6099&autoconnect=1&resize=scale'
DISPLAY=:98 XAUTHORITY= xdpyinfo | rg 'dimensions|depth of root window'
DISPLAY=:98 XAUTHORITY= xdotool getdisplaygeometry
DISPLAY=:98 XAUTHORITY= xwininfo -root -tree | head -n 80
ss -ltnp | rg ':5908|:6099'
```

Verify that the main app geometry matches the X root geometry, the noVNC view
shows the complete window without clipping, and the full-client clipboard panel
is available. For a login-to-main transition, verify both centered login state
and full-size main-window state.

## Cleanup and Troubleshooting

- Stop camera viewers without killing the IDE or desktop services.
- Remove stale X sockets only after confirming no matching Xvfb process exists.
- If noVNC is blank, inspect Xvfb, x11vnc, and websockify before relaunching the
  app.
- If the app is clipped despite `resize=scale`, inspect its remote window
  geometry; viewer scaling cannot repair an oversized off-canvas app window.
- If the main window stops fitting after login, the app probably created a new
  window; fix the persistent guard instead of adding a one-time delay.
- Record display, ports, profile, process IDs, URL, fit guard, and stop commands
  after a successful setup.
