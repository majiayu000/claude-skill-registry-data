---
name: mac-menu-bar-app
description: Ship a real, double-clickable macOS app — a menu bar utility, a background daemon that starts at login, a local tool you can find in Spotlight. Use when you say "i need an executable", "make it a mac app", "build me something for my mac", "put it in my menu bar", "make it run at login", "i can't find it on my mac", or when a local tool has outgrown `python3 -m thing` in a terminal. Covers the Swift + launchd + install-script pattern with zero runtime dependencies, and the four macOS traps that each produce a SILENT failure.
---

# Shipping a local Mac app

**"An executable" means something you can find in Spotlight and click.** A Python
module in a terminal is not that, and neither is a thing that runs but shows
nothing when clicked.

A finished app in this shape is four files: `YourApp.swift`, `makeicon.swift`
(draws the icon), `build.sh`, `install.sh`. The four traps below are what the
first build of one hit.

## The architecture that worked

    /Applications/YourApp.app        signed, IMMUTABLE Swift binary + .icns
    ~/Library/Application Support/YourApp/   the Python package (mutable)
    ~/Library/LaunchAgents/<id>.plist        launchd owns the daemon
    ~/.local/bin/<name>                      CLI shim
    ~/Library/Logs/YourApp.log               the app's log
    /tmp/<name>-daemon.log                   the daemon's log (launchd writes it)

**Zero runtime dependencies.** `/usr/bin/swiftc` ships with Command Line Tools
(Swift 6.3 as of 2026-08), so a native menu bar app needs no PyObjC — which is
usually not installed on the system python3. The daemon is Python
stdlib only.

**launchd owns the daemon, never the app.** `RunAtLoad` + `KeepAlive` gives one
instance, restarted on crash, started at login. Letting the app spawn it produced
orphans that were alive but not listening. Verify with `kill -9` and check it
comes back.

---

## The four traps. Each one fails SILENTLY.

### 1. `~/Desktop` is TCC-protected — a LaunchAgent there hangs forever

This is the expensive one. Terminal holds a Desktop grant, so `python3 -m thing`
works perfectly by hand. **A LaunchAgent has no grant and no way to show a
consent prompt, so the interpreter blocks in startup** — inside `os_listdir`,
before it can even load `encodings`. The symptom is a process that is **alive,
silent, and not listening**, with an empty log.

**Never run a LaunchAgent's code out of `~/Desktop`, `~/Documents` or
`~/Downloads`.** Stage it into `~/Library/Application Support/<App>/`. The repo
can still live on the Desktop; the install script copies out of it.

### 2. Nothing may be written inside a signed `.app`

Python wrote `__pycache__/*.pyc` into the bundle on first run, breaking the code
signature — `codesign` reports *"a sealed resource is missing or invalid"* — and
the app stopped launching from Finder while still launching from a terminal.

Keep the bundle immutable (binary, `Info.plist`, `.icns`, `_CodeSignature` and
nothing else). Set `PYTHONPYCACHEPREFIX=~/Library/Caches/<app>`. Verify after a
full run:

    codesign -vvv --strict /Applications/YourApp.app     # must say "valid on disk"
    find /Applications/YourApp.app -name "__pycache__"   # must be empty

`spctl -a` saying **"rejected" is fine** — that only means ad-hoc signed, not
notarized. Locally built apps carry no `com.apple.quarantine` flag, so Gatekeeper
does not block them. **Check the quarantine xattr, not `spctl`.**

### 3. `contentTintColor` does nothing on a menu bar button

macOS forces template images monochrome and ignores the tint, so an "amber"
alarm renders **black**. A coloured menu bar icon must be **drawn** as a
non-template `NSImage`:

```swift
let dot = NSImage(size: NSSize(width: 12, height: 12), flipped: false) { rect in
    amber.setFill(); NSBezierPath(ovalIn: rect.insetBy(dx: 2, dy: 2)).fill(); return true
}
dot.isTemplate = false      // template == monochrome, always
```

Keep the *resting* icon a template SF Symbol so it adapts to light/dark bars.
Breaking the monochrome convention only for the alarm is what makes it catch the
eye without being read.

### 4. `HTTPServer.server_bind()` calls `socket.getfqdn()`

A reverse-DNS lookup: instant in a shell, can stall indefinitely under launchd.
Subclass and skip it:

```python
class _Server(ThreadingHTTPServer):
    def server_bind(self):
        socketserver.TCPServer.server_bind(self)   # not HTTPServer's
        self.server_name, self.server_port = HOST, PORT
```

---

## Findability — it must be findable in Spotlight

- **Install to `/Applications`, not `~/Applications`.** Spotlight and Launchpad
  largely ignore the home one. `/Applications` is writable without `sudo`.
- **Run `lsregister` after writing the bundle**, or it stays invisible even
  sitting in `/Applications`:

      /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f /Applications/YourApp.app
      mdimport /Applications/YourApp.app

  Confirm with `mdfind "kMDItemFSName == 'YourApp.app'"`.
- **Give it an icon.** Without one it is a blank generic square and invisible to
  the eye even when Spotlight finds it. Draw the `.iconset` with AppKit in Swift
  (see `makeicon.swift`), then `iconutil -c icns`, then `CFBundleIconFile`.
  **Design the 16pt case deliberately** — drop detail below 64px and draw the one
  element that survives. An icon illegible at 16pt is not a smaller icon, it is a
  worse one.

## An `LSUIElement` app MUST acknowledge being launched

A menu bar agent has no window and no Dock icon, so clicking it in Spotlight
produces **no feedback at all** — and none whatsoever if it is already running.
Users report this as "clicking it, nothing happens" when the app is running
perfectly.

**Open the menu yourself** on launch and on reopen:

```swift
DispatchQueue.main.asyncAfter(deadline: .now() + 0.7) { self.item.button?.performClick(nil) }

func applicationShouldHandleReopen(_ s: NSApplication, hasVisibleWindows: Bool) -> Bool {
    item.button?.performClick(nil); return true
}
```

This is not a nicety. Silence is indistinguishable from failure.

## Log, always, and never to /dev/null

Sending a spawned daemon's output to `FileHandle.nullDevice` hid a startup
failure through two debug rounds. Log to a file, and pass **`-u`** to Python or
the log stays empty from buffering when stdout is not a tty.

Log state *transitions*, not every poll, or the file becomes unreadable and
nobody will open it.

## Debugging a process that is alive and doing nothing

**Take the stack before forming another theory.** Three rounds of hypotheses
were beaten by one command:

    sample <pid> 2 -file /tmp/s.txt && sed -n '/Call graph/,/Binary Images/p' /tmp/s.txt

That is what identified the TCC hang, unambiguously, in seconds. Also useful:
`lsof -p <pid>` (if only dyld and the binary are mapped, it never finished
starting) and `launchctl print gui/$UID/<label>`.

## The install script is the deliverable

One script, idempotent, with `--uninstall`. It should: stage the package out of
the repo → build and sign the app → write and bootstrap the LaunchAgent →
`lsregister` → write the CLI shim → **verify the daemon actually answers** and
say so. Print where each surface lives.

## Ask vs. decide yourself

- **Decide:** language, install paths, launchd config, log format, the traps above.
- **Ask:** the visual design of anything the user will look at daily. Show live
  prototypes rather than descriptions (`beautify`).
- **Don't add CI** to a tool that is only meant to run locally unless asked.

## Forward references

- Reading Claude Code's own state → `claude-usage-mining`
- Prototyping the UI before building it → `beautify`
- Remote/hosted services instead of local → `build-remote-mcp-server`
