---
name: run-ircx
description: Build, run, and drive ircx. Use when asked to start ircx, run its tests, build it, take a screenshot of its UI, click through the app, or check that a frontend change works in the running client.
---

ircx is a Tauri 2 desktop client: a React frontend in a WebKitGTK window, a Rust
core behind it. There are two ways to drive it and the first is the one to
reach for.

**The frontend in headless Chrome**, via `scripts/run-ircx/driver.mjs`,
which starts Vite, launches Chrome, and takes commands on stdin. It needs no npm
package and no display. Almost everything a change touches is reachable that
way: the shell, the command palette, every sheet, themes, the timeline. A
selector reaches an element, `text` and `count` answer questions about it, and a
failure points at a line of your code.

**The assembled app in a real window**, via
`scripts/run-ircx/window.mjs`, which starts `Xvfb`, seeds a profile,
launches the app against a server and takes the same kind of commands. Use it
only for what the frontend alone cannot show — a live socket, the delivery
states behind it, and anything the Rust side decides. It is slower, it has no
selectors, and what it tells you is a screenshot.

## Prerequisites

`google-chrome` and the Node version pinned by the project (the driver uses the
built-in `WebSocket`, so there is nothing to install). Verified Chrome:

```bash
google-chrome --version   # Google Chrome 151.0.7922.71
```

`window.mjs` needs five more, all present here: `gcc` and `libXtst` to build the
input helper, `Xvfb` to put the window somewhere, `xprop` to tell when it
arrived, and ImageMagick's `import` to photograph it.

## Setup

Each git worktree needs its own `node_modules`:

```bash
npm ci
```

## Run (agent path)

Pipe commands in, read one `ok`/`err` line back per command:

```bash
mkdir -p /tmp/shots
printf 'goto /\nss /tmp/shots/shell.png\ntext body\nquit\n' \
  | node scripts/run-ircx/driver.mjs
```

Opening a sheet from the command palette — this is the flow most UI work needs:

```bash
printf 'goto /
key ctrl+k
type Plugins
wait 400
key Return
wait 600
text [role=dialog]
ss /tmp/shots/plugins.png
key Escape
count [role=dialog]
quit
' | node scripts/run-ircx/driver.mjs
```

That prints the sheet's text, writes the screenshot, and ends with `ok 0`
confirming Escape closed it.

### With a conversation on screen

By default every `invoke` rejects, so the app has no networks and no
conversations. Anything needing one — the timeline, the composer, the panes, the
roster, the archive and upload sheets — has to be driven with `--seeded`, which
answers from `seed.mjs` instead:

```bash
printf 'goto /
wait 1500
click [aria-label="#ircx"]
wait 900
click textarea
type hello
key Return
wait 600
ss /tmp/shots/channel.png
quit
' | node scripts/run-ircx/driver.mjs --seeded
```

The seed holds one network, `#ircx`, `#rust`, a 300-message `#long` to park in
the middle of, a `#band` whose sixty lines are one block tall enough to scroll
its own author off the top — which is what draws the sticky author band — and a
query. `#ircx`'s members are picked for the roster's width
arithmetic: a voiced one, an away one, and `wallabywombat` to reach the ceiling.
A line typed into the composer is kept, so `ArrowUp` brings it back.

**`click` is not a pointer.** It calls `el.click()`, so nothing moves and no
`pointerdown` sequence happens — anything driven by pointer events, such as the
pane divider with its `setPointerCapture`, cannot be worked by it. `drag` and
`dragxy` go through the DevTools Protocol instead, which is a real pointer as
far as the page is concerned. `dragxy` is the one that answers "can this be
hit": a selector always lands dead centre, which is the question nobody is
asking.

**This is where the layout defects are.** jsdom lays nothing out, so a whole
class of bug — a name truncated by a sub-pixel shortfall, a header wrapping into
a row of fixed height, a scroller clamped before it was measured, a four-pixel
target lying entirely to one side of the line it draws — cannot be caught by
`vitest` at all. #299, #300, #301 and #307 were each found here, and
none of them had a failing test until a browser had shown the defect first.

Adding a handler to `seed.mjs`: key it off the **Rust** parameter names, not the
TypeScript ones. `submit_input` takes `input`, not `text`, and a wrong name
throws inside the seed and reads exactly like a frontend bug. A command with no
handler rejects by name, so a walk that reaches past the seed says so.

| command | what it does |
|---|---|
| `goto <path>` | navigate, default `/` |
| `ss <file>` | screenshot to `<file>` (PNG) |
| `eval <expr>` | evaluate, print the JSON result |
| `text <sel>` | `textContent` of the first match |
| `count <sel>` | how many match — `0` is how you assert something closed |
| `click <sel>` | click the first match |
| `drag <sel> <dx> <dy>` | press at its centre, move in steps, release |
| `dragxy <x> <y> <dx> <dy>` | the same from a point, for asking what a target catches |
| `size <w> <h>` | set the viewport, for what a layout does when narrow |
| `fill <sel> <value>` | set an input's value the way React notices |
| `filllabel <label> <value>` | the same, finding the field by its visible label |
| `type <text>` | insert text at the focus |
| `key <combo>` | `ctrl+k`, `Escape`, `Return`, `a` |
| `wait <ms>` | |
| `quit` | stop Chrome and Vite |

The driver picks a free port and prints it as `ok ready http://localhost:<port>/`.
It kills both children on `quit`, on EOF, and on a closed stdin.

## Run (the assembled app)

`window.mjs` starts `Xvfb`, seeds a profile with the network you name, launches
the app twice — once to let it create and migrate its archive, once with the
network in it — and hands you the window. With #344 the app then opens the
channel by itself, so a walk starts with a conversation on screen.

```bash
mkdir -p /tmp/shots
printf 'wait 2000
ss /tmp/shots/joined.png
click 657 723
type hello from the harness
key Return
wait 1500
ss /tmp/shots/said.png
quit
' | node scripts/run-ircx/window.mjs --join '#harness'
```

| command | what it does |
|---|---|
| `type <text>` | insert text at the focus, a keystroke at a time |
| `key <combo>` | `Return`, `Escape`, `ctrl+k`, `shift+Return` |
| `click <x> <y>` | window coordinates, the window being at the origin |
| `move <x> <y>` | put the pointer there and press nothing, for anything drawn on hover |
| `wheel <x> <y> <n>` | scroll there, `n` notches, up when negative |
| `ss <file>` | screenshot the display to `<file>` |
| `wait <ms>` | |
| `quit` | stop the app, Vite and Xvfb, and delete the profile |

| option | |
|---|---|
| `--server <host:port>` | default `127.0.0.1:6667` |
| `--nick <nick>` | default `walker` |
| `--join <#channel>` | seeded as a connect command, repeatable |
| `--tls` | the seeded network uses TLS, off by default |
| `--sasl <account:password>` | the seeded network logs in with SASL PLAIN |
| `--release` | drive the release app instead of a debug build against Vite |
| `--keep` | leave the profile behind and print where it is |
| `--profile <dir>` | launch on a profile a `--keep` run left, as it stands |

**`--sasl` is how a walk becomes two sessions of one account**, which is what
`MARKREAD` is relayed between and what a bouncer-shaped question needs. The
password does not go in the seed: the app reads it from the OS keyring, so the
flag writes it there — the `ircx` service, keyed by the network's id — and
clears it again on the way out unless `--keep` was asked for. `ergo` merges a
second connection into an existing client when it authenticates, so a socket
script with the same credentials is the second session.

**`--profile` is how "does it survive a restart" is asked.** A run seeds a fresh
profile, so a draft, a pane layout, a theme and its edits are all gone by the
next one. Keep a profile, do the thing, quit, and launch again on the same
directory; nothing is seeded the second time.

**`--release` is what a figure has to be measured on**, and the build for it is
`npm run tauri build -- --no-bundle` — **not** `cargo build --release`. What
decides whether the frontend is inside the binary or fetched from the dev server
is the tauri CLI rather than the cargo profile, and both land on
`target/release/ircx`. A window driven against the cargo one comes up white with
`Could not connect to localhost`, and a measurement taken there is a measurement
of an error page. Nothing can tell them apart from outside — the embedded assets
are compressed — so the first screenshot is the check.

**A Tailwind `hover:` rule cannot be walked at all, and says nothing about it.**
Tailwind v4 wraps every `hover:` and `group-hover:` utility in
`@media (hover: hover)`, and WebKitGTK on `Xvfb` answers that query `hover:
none` — there is no pointer device on that display, whatever `move` does with
XTEST. So a control drawn `hidden group-hover:block` is invisible for the whole
of a walk and reads as a control the app does not have. The same engine on a
real pointer session answers `hover: hover`.

Reach such a control by its focus twin instead — `group-focus-within:` is not
inside the media query, so clicking anything focusable in the same group draws
it. `move` still photographs a bare `:hover` rule, one written without the
Tailwind variant, which is the only kind this harness can see.

**A timeline can only be scrolled with `wheel`.** The scroller is a `div`
nothing focuses, so no key sent to the window moves it, and `click` lands on a
message rather than dragging a bar. **How far a notch goes is not a constant.**
It has been about a third of a message and as much as three whole messages, so a
coordinate read off one screenshot is stale after a single notch. Measure it
in the pane being walked before counting them, and take the screenshot the
coordinate comes from after the last one.

**Two frames with nothing between them is how the app is caught moving on its
own.** Send an input, photograph, wait, photograph again — any difference is the
app rather than you, and `md5sum` on the pair is the whole test, since a still
pane is byte-identical. What the difference *is* takes a real measurement:
`shift.py` slides a band of one frame over the other and answers in pixels.

**Two things it cannot do**, and both bite quietly:

- **No selectors.** Nothing answers for WebKitGTK the way the DevTools Protocol
  answers for Chrome, so the window is read by screenshot and clicked by
  coordinate. Assertions are your eyes on a PNG, the archive under `--keep`, or
  a second client on the socket.
- **A coordinate goes stale.** The fourth run's first `Retry` click missed
  because a reconnect drew two rows and pushed the control up the pane between
  the screenshot and the click. Take the shot, click, and let nothing arrive in
  between.

**Read the wire from a second client, not from ircx.** Its timeline draws local
copies the moment Enter is pressed and its raw log records the queue rather than
the socket, so neither is a clock. A small socket client joined to the same
channel reads what the server received.

## Measure startup

`startup.mjs` times exec to each of the four marks in the *Startup* section of
`docs/measurements.md`, over profiles it seeds: empty, an archive, networks that
dial. `quickserver.mjs` is what they dial — registration answered immediately,
so the figure is ircx's rather than a server's.

```bash
node scripts/run-ircx/startup.mjs --messages 100000 --networks 3 --runs 3
```

It drives the **real compositor**, not `Xvfb`: the marks are read off
`WAYLAND_DEBUG` and a frame commit is not something an X server reports, so a
window appears on the operator's screen once per run. `--seed-only` builds one
of the profiles and stops, for `window.mjs --profile <dir> --release` to open
somewhere less intrusive.

**Seeding an archive by hand is where this goes wrong quietly.** Three columns
in `messages` hold JSON rather than what their names suggest — `kind` is a
quoted camelCase string, `delivery` is internally tagged, `tags` is an array —
and `open_targets.kind` must be lowercase `channel` or the conversation reopens
as a query. Rows that get any of it wrong insert perfectly well and count
towards the file size, then fail to deserialise: the archive looks populated,
the timeline comes up empty, and nothing says so. The first version of this
harness measured exactly that. **Check a seeded profile with a screenshot before
believing a number taken on it.**

`networks.sasl_mechanism` is a fourth, and it fails wider: the bare word `PLAIN`
where the column wants `"PLAIN"` fails one row's deserialisation and takes the
whole network list with it, so the app comes up saying it has no networks
configured while the row sits in the table.

## Run (human path)

```bash
npm run tauri dev   # → the real window, Rust backend and all. Ctrl-C to stop.
```

The same window on your own display, for looking at rather than driving. It
needs a display, and it will refuse to start if another dev server holds port
5183 (see Gotchas).

## Test

```bash
npm run typecheck && npm run lint && npx vitest run
cargo test --workspace
```

Do not set `CARGO_TARGET_DIR`. The default is `<checkout>/target`, which is
already one directory per worktree — see Gotchas for what sharing one costs.

## Gotchas

- **The frontend throws without Tauri, and the failure looks like CSS.**
  `onFileDrop` in `src/lib/ipc.ts` calls `getCurrentWindow()` unguarded the
  moment `<DropToUpload>` mounts. Outside a Tauri webview that throws
  synchronously and React unmounts the whole tree, leaving a window that is the
  right dark colour and **completely empty** — it reads like a stylesheet
  problem, not a crash. `vite.browser.config.mjs` injects a
  `window.__TAURI_INTERNALS__` stub to get past it. `TitleBar.tsx` guards for
  this properly with `"__TAURI_INTERNALS__" in window`; that call site does not.
- **`npm run tauri dev` cannot run twice.** `vite.config.ts` pins port 5183 with
  `strictPort: true` so the Rust side's `devUrl` cannot drift, so a second one —
  or another agent's worktree — fails outright. `driver.mjs` asks for port 0
  instead and is unaffected; `window.mjs` needs 5183 and is not. If `npm run
  dev` dies with "Port 5183 is already in use", that is another session, not
  you: leave it alone and use `driver.mjs`.

  It bites twice. A dev server left over from your own earlier run holds the
  port too, and the app then refuses it by name — *`http://localhost:5183/` is
  serving another checkout* — which is #233 working. `window.mjs` reports what
  the app said rather than only that no window arrived, but the fix is to find
  the stale `vite` and kill it.
- **A window opens on your real desktop instead of on `Xvfb`.** GTK prefers
  Wayland when `WAYLAND_DISPLAY` is set, so `DISPLAY=:98` alone is not enough:
  the app appears on the operator's actual screen, the `Xvfb` root stays black,
  and nothing anywhere says why. `window.mjs` unsets it and sets
  `GDK_BACKEND=x11`. Driving the app by hand, do the same — and
  `xprop -name ircx` against the display is what answers "did it map here".
- **`pkill -f` matches the shell running it.** A pattern like
  `pkill -f target/debug/ircx` appears in the `bash -c` wrapper's own command
  line, so it kills the shell before the app. Kill by exact name (`pkill -x
  ircx`) or by the pid you started.
- **A second ircx on the machine used to make every launch a timeout.** The
  single-instance plugin hands a launch off to the ircx already running and
  exits 0, so nothing maps on `Xvfb` and the run dies on `timed out waiting for
  the app to create its profile` with nothing on stderr underneath it — the app
  did what it was built to do. `window.mjs` builds with the `walk` feature,
  which drops the plugin, and builds on every run because a binary an earlier
  run left may not carry it. Launching the app by hand, build the same way:
  `cargo build --manifest-path src-tauri/Cargo.toml --no-default-features
  --features walk`.
- **Two checkouts must not share one target directory.** This entry used to say
  the opposite — that a fresh worktree rebuilds ~51G, so point
  `CARGO_TARGET_DIR` at another checkout's `target/`. Both halves were wrong.

  Sharing is unsafe. Cargo will run a test binary the *other* checkout built:
  on 2026-08-09 `cargo test --workspace` failed four `ircx-plugin` tests on a
  `CARGO_MANIFEST_DIR` baked in at compile time, naming a worktree that had
  since been deleted. That failure at least announced itself. The same
  mechanism with a binary that still passes tells you a tree is green when
  nothing in it was tested, and `window.mjs` had a whole extra build step
  bolted on for the same reason — the app binary belonged to whichever checkout
  built it last.

  And the 51G was an accumulated directory, not a build. A fresh worktree's
  full test build is **84 seconds and 7.1 GB** (`docs/measurements.md`); the
  81 GB in a long-lived checkout is mostly `incremental/` grown over months.

  So build into the default and leave `CARGO_TARGET_DIR` unset. If you do need
  to name one, put it outside the checkout: `.gitignore` and
  `eslint.config.js` both ignore `target` by that exact name, so a directory
  inside the checkout called anything else gets picked up by lint and by git.
- **Assigning `.value` to an input does nothing React can see.** React installs
  its own setter and listens for the event after it, so a plain assignment
  updates the DOM while React's state keeps the old value — the field looks
  edited and nothing else reacts. `fill` goes through the prototype's setter and
  then dispatches `input`. Use it rather than `eval`.
- **Form fields have no stable selector.** `src/components/onboarding/fields.tsx`
  labels its inputs with a React `useId`, so the id is generated per render and
  nothing in CSS reaches a field by the name a person sees. Everything built on
  those fields — onboarding, the plugin permissions form — needs `filllabel`,
  which goes through the `<label for>`. `fill` only works where a selector
  genuinely exists.
- **`key` cannot type punctuation.** It maps a character to a US-layout key code,
  so `(` and `)` are unreachable through it. Use `type`, which goes through
  `Input.insertText` and is layout-independent. This matters for anything
  pasting a CSS value like `rgb(...)` or `url(...)`.
- **`window.mjs`'s `type` cannot type an emoji, and the failure is sticky.**
  That `type` is not `driver.mjs`'s: it goes through XTEST a keystroke at a
  time, so a character with no keysym stops it dead — `err no keycode for
  keysym 0xf0` is what a 👍 gets. Run 36 lost two attempts to it. Worse, the
  characters typed *before* the failure are already in the field, so the next
  attempt appends to them and sends something nobody wrote: a `/react` that
  died on its emoji left ircx sending a reaction whose value was a msgid.
  Clear the field (`ctrl+a`, `BackSpace`) after any `type` that errors. A
  reaction's value has no restriction on it, so a word tests the same path.
- **Do not type a path into GTK's *folder* chooser.** Its location bar (`ctrl+l`)
  duplicates injected characters: `/tmp/notaplugin` arrived as
  `/tmp/nootaplugin`, and a longer one as `claude-aude-1000` for `claude-1000`.
  Shortening the path does not help — a four-character prefix mangled too — and
  it is not the dropped-keystroke fault #349 fixed, because characters are being
  *added*. The save dialogue's Name field takes a typed path perfectly well; this
  is the folder chooser specifically.

  Navigate it by clicking instead. Put the folder somewhere the chooser already
  lists — the app's own working directory is where it opens — then click its row
  and click Open.
- **Backend-dependent UI is empty, not broken.** Without `--seeded` every
  `invoke` rejects, so the network list, plugins, uploads and themes installed on
  disk show their backend-absent state — the plugins sheet renders "no backend:
  the frontend is running in a browser" where the list would be. The two built-in
  themes still load, being compiled in rather than read from disk. `--seeded`
  answers instead; anything that must exercise the Rust side itself still needs
  `npm run tauri dev`.
- **`scripts/run-ircx/**` is excluded from application lint** in
  `eslint.config.js`. The harness runs in Node and is not application source.

## Troubleshooting

- **`ok ready` never prints, `timed out waiting for the Vite dev server`**: run
  `npm ci` — a fresh worktree has no `node_modules`.
- **`err no element matching <sel>`**: the sheet had not rendered yet. Add
  `wait 400` after the `key Return` that opens it.
- **Blank screenshot, no error**: the Tauri stub did not load. Check the driver
  was started with `--config scripts/run-ircx/vite.browser.config.mjs`
  — it is, unless you launched Vite yourself.
- **`process exited with 1 before Chrome's debugger`**: another Chrome is using
  the profile directory. The driver makes a fresh one under `/tmp` per run, so
  this means a stale process; `pkill -f ircx-chrome-` and retry.
