---
name: projektordner
description: >
  Projektordner wechseln in zid (File → Open Folder…, Ctrl+O): In-App-Ordner-Dialog, openProjectFolder, veraltete git-status-Ergebnisse, Ordner ohne Repo, File-Watcher-Thread, Aufwecken des Frame-Loops; dazu die Fenster-Backends Wayland/X11 und die WGPU-Surface. Use when touching src/ui/folder_picker.zig, folder_ops.zig, openProjectFolder/takePendingOpenFolder, UI.updateGitStatus, git_worker.isInsideRepo/repoTopLevel, Scheduler.on_result, the file watcher, src/platform/native_window.zig, Renderer.setWindow, libs/wio, or scripts/e2e_open_folder.py.
---

# Projektordner und Fenster-Backends

## Projektordner wechseln („Open Folder…“)

- Header-Menü **File → Open Folder…** oder **Ctrl+O** öffnet einen modalen Dialog
  (`src/ui/folder_picker.zig`, Logik ohne Clay in `src/ui/folder_ops.zig` mit Tests):
  editierbarer Pfad (`~` wird expandiert), Liste der sichtbaren Unterordner (Klick steigt ab),
  ↑ für den Elternordner, Enter/Open bestätigt, Escape/Cancel schließt.
- Kein nativer Dialog (zenity/kdialog/Portal): der In-App-Dialog ist headless testbar und
  braucht keine Systemabhängigkeit.
- Bestätigt → `UI.pending_open_folder`; `main.zig` holt es per `takePendingOpenFolder` und ruft
  `openProjectFolder` (auch beim Start): Explorer-Root, `current_directory`, Git-Branch/-Status
  und File-Watcher wechseln. Offene Tabs bleiben erhalten.
- **Veraltete git-status-Ergebnisse verwirft `UI.updateGitStatus`:** der Status trägt
  `root:<toplevel>` und wird nur angenommen, wenn das zur Repo-Wurzel des aktuellen Projekts
  passt (`git_worker.repoTopLevel`, `samePath`). Sonst überschreibt ein spät eintreffender Status
  des Start-Projekts den des neuen.
- **Ordner ohne Repo bekommen keine git-Tasks.** `git_worker.isInsideRepo` (unit-getestet) sucht
  `.git` aufwärts; schlägt das fehl, bleibt `git_repo_path` null und weder Branch noch Status
  werden eingereiht. `runGitCwd` loggt bei Fehlern Befehl, Ordner und stderr.
- Der File-Watcher registriert seinen Baum im eigenen Thread (`~/projects` hat tausende Ordner,
  das darf den Frame-Loop nicht blockieren).
- **Jedes Async-Result weckt den Frame-Loop:** `Scheduler.on_result` ist im Fenster-Modus
  `wio.cancelWait` (Worker und Watcher rufen es nach jedem `push`). Ohne Hook schläft der Loop in
  `wio.wait(.{})`, die Result-Queue (256) läuft bei ruhigem Fenster voll und der Watcher loggt
  pro Ereignis „result queue full". Headless braucht keinen Hook (Polling).
- E2E: `python3 scripts/e2e_open_folder.py [ordner]` startet headless, fährt Menü → Dialog →
  Pfad tippen → Enter und prüft den neuen Root; Screenshots in `tmp/e2e_menu.ppm` und
  `tmp/e2e_dialog.ppm`. RPCs dafür: `element_bounds(id)`, `element_bounds_i(id, index)`,
  `folder_picker_state`, `get_state.root`; `key_press` kennt `o`, `up`, `down`.
- Pfadfeld im Dialog (`line_edit`, z-Index, waagrechtes Scrollen): Skill `editor`.

## Fenster-Backends: Wayland und X11

- `build.zig` baut wio mit `unix_backends = "x11,wayland"`. wio wählt beim Start selbst:
  `XDG_SESSION_TYPE` entscheidet, sonst probiert es beide (`libs/wio/src/unix.zig`).
- Die WGPU-Surface braucht je Backend andere Handles. `Platform.nativeWindow` liefert sie als
  `NativeWindow` (`src/platform/native_window.zig`), `Renderer.setWindow` baut daraus den
  Deskriptor: Wayland-Surface, Xlib-Window oder HWND.
- Linken der Backend-Bibliotheken und der wio-GLX-Patch: Skill `packaging`.
- X11 von einer Wayland-Sitzung aus prüfen: `env -u WAYLAND_DISPLAY XDG_SESSION_TYPE=x11
  DISPLAY=:0 ./zig-out/bin/zid --e2e --ai=off <datei>`, dann Screenshot per RPC. Xwayland reicht
  dafür. Headless berührt kein Backend, deckt das also nicht ab; ein Fenster nur nach Rückfrage
  beim User (Skill `grosse-dateien`).
