---
name: local-network
description: Use to run a whole network of your own on this machine, to try a change, call its tools as different users, or open the app against it, without touching the owner's live network.
---

    tooling/network <folder> [--standby] [--owner <name>] [--live-edge]

Its header says what each flag does. It builds what isn't built (the UI library, then the server's `mix compile` as it
starts, which builds the Rust workspace's debug build with `cargo build`), starts the server, and prints how to use it once it's
running. A worktree's first build starts from a copy of the build of a worktree beside it (`tooling/copy-build`, which
`tooling/network` and `mix compile` run; run it yourself before a first `cargo`), so its first network builds only what
differs, and starts in about a minute on the shared Linux machine (23 Nov), its own crates rebuilt.
Run it in the background and let your harness tell you when it ends; put the folder in your scratch folder.

## The fastest loop

- An app, One Core's Elixir, the UI library (`core/ui`) or any Rust changed: just call a tool, or reload the app's
  page. Before a client's request, the network's code reloader (`tooling/code_reloader.exs`) loads what changed into
  every server, as Phoenix's code reloader does: One Core's changed modules, the Rust workspace built again (`one`
  and app NIFs), the UI library built again and served, and an app deployed as `one deploy --files-from` deploys
  it. A build error is that request's error, saying so, as is a changed One Core NIF, which needs a start again.
  What only a start builds (a supervisor's children) stays as it was until then.
- The client's page (`clients/app/page`, `clients/web`) is built as the network starts, minified as a deploy builds it, so
  a change to it takes a start again.
- The edge (`core/edge/`, an app's `edge/`) changed: start it with `--live-edge`, and `wrangler dev` builds each Worker
  again as it's saved. Without it, the edge runs its Workers bundled as they're deployed, which saves about 110 MB,
  and an edge change takes a start again.
- The deps or the config changed, or a request says to: stop it and start it again in the same folder.
- A commit, or a rebase that moves it, builds `one` again once (about 5 s): a build is named by its commit.

## Acting as someone

    export ONE_HOME=<folder>/client ONE_AS=owner
    target/debug/one permissions group --name family
    ONE_AS=alice target/debug/one permissions groups
    ONE_SUBJECT=network target/debug/one deploy --name <app> --files-from apps/<app>

Always set `ONE_HOME`: without it, the installed `one` is the owner's live client on the live network, and a debug
build (yours) is a client of its own that's on no network. `<folder>/client` is `owner`'s device, signed in at the
network's address as any device is; `ONE_AS` picks the user it acts as, which a server of a network being built
believes; `ONE_SUBJECT=groups/<name>` or `ONE_SUBJECT=network` runs a call for a group or the network.

`owner`, `alice` and `bob` start with their encryption set up, their keys on `<folder>/client`'s device, so the
Vault opens at once in `one` and in the app run with that home. Anyone else is set up as a passkey would, from that
device: `ONE_AS=<name> bun tooling/keys.ts make`, then `ONE_AS=<name> one vault list` (which lists their Vault for
its servers) and `ONE_AS=<name> bun tooling/keys.ts servers`. To try the passkey itself, a headless Chromium with
a CDP virtual authenticator that has PRF joins by `one sign-in invite`'s link (type a name in its field first, which
is drawn: click it, then type) and opens `unlock_with_passkey`'s.

## A browser signed in

`<folder>/browser.json` is Playwright's storage state for a browser signed in as `owner`, made as the network starts,
with no passkey (`one sign-in browser`, which only a network being built answers). Load it and open the address:

    const context = await browser.newContext({ storageState: "<folder>/browser.json" })

`ONE_AS=alice one sign-in browser > alice.json` signs one in as anyone else. A new person sees Welcome first;
`one home-screen tip --name welcome --seen true` skips it. Chromium draws the page with WebGPU, so launch it with
`--enable-unsafe-webgpu --enable-gpu --use-angle=vulkan --ignore-gpu-blocklist`.

## Only the edge

A change to an edge page that asks no server (the sign-in page, the web client's files, an app's `edge/`) needs no
network: `cd core/edge && bun install --frozen-lockfile && bun edge.js dev --live --port <port> --persist-to <folder>`
runs the edge alone, in about 10 s. Stop it by its process group (`kill -- -<pgid>`): Wrangler's `workerd` outlives `bun`.

## Signing a device in

A device that isn't `<folder>/client` (a phone, the simulator, another client home) signs in at the network's
address, which it prints. Put `{"address": "<the address>"}` in its home's `network` file (or in its own resources: `clients/app/README.md`),
open it, and it shows a code. Then, as whoever it's to be, one step:

    ONE_AS=alice one sign-in approve --code WDJB-MJHT

The device asks every 5 s whether it's approved, and at once if its `one` is sent SIGUSR1 after the approval
(`kill -USR1 <its pid>`), as a push would tell a phone.

On a network being built anyone may be named, the owner too, with no `--owner` and no passkey. For an emulator,
`adb reverse tcp:<port> tcp:<port>` first, `adb shell run-as app.theone.client sh -c 'cat > network'` writes its
`network`, and `adb shell pm grant app.theone.client android.permission.POST_NOTIFICATIONS` skips Android's question.
The app says its code in `adb logcat -s RustStdoutStderr`, as `this device's session: SignIn { … code: "…" }`. A
device's key is only ever handed over by a passkey (Unlock with Passkey), so to open the Vault there, use one there.

## Looking inside the server

Each server is an Erlang node: `iex --sname dbg-$$ --cookie $(cat <folder>/cookie) --remsh <node>` attaches, with the
node's name as `tooling/network` prints it. `:recon`, `:recon_trace` and `:observer_cli.start()` are there.

## A network path that's open one way

`--standby` gives two servers on this machine, each listening on the UDP port in its home's `port` file. To have one
reach the other only one way on an address, as a firewall or a Mac's local network privacy does, drop that direction
with `sudo iptables -I OUTPUT -p udp --sport <from's port> --dport <to's port> -d <address> -j DROP` (the relay is
TCP, so it's untouched), and remove it with `-D` in place of `-I` when you're done: the machine is shared.

## Faults

What a person's network meets, one server at a time, while the tools you're checking run: with `--standby`, make
the fault in `standby` and call tools as the client does, which asks `server`. Each must answer from the servers
that do, naming the one that didn't in `failed`, or fail fast saying why; never hang or answer nothing. A device's
app is faulted the same way, by its own PID.

- Frozen, as a machine asleep: `kill -STOP $(cat <folder>/standby.pid)`, and `-CONT` after. Its connections go
  silent and are given up in 4 s (`SILENT`, `core/client/src/transport.rs`), so a frozen one is the easy case.
- Stuck, as a server that's connected and says it's still running, but never answers: its apps' process suspended,
  `elixir --sname f$$ --cookie $(cat <folder>/cookie) --rpc-eval <its node> ':sys.suspend(OneCore.Apps)'`, and
  `:sys.resume` after. Nothing below the app gives up on that, so only a deadline does: this is the one that hangs.
- Slow: `cpulimit -p $(cat <folder>/standby.pid) -l 2` (apt's or Homebrew's `cpulimit`), which stops and continues
  it, and leaves it stopped if it's killed, so `kill -CONT` it after.
- Packets dropped: the UDP of its port (`<folder>/standby/port`), both ways, as under A network path that's open one
  way; its relay, over TCP, still carries it.
- Behind a firewall with a far relay, as a laptop after it wakes: it answers the relay, and the edge reaches it, but
  the other servers can't in time. Drop every UDP port it listens on (`ss -uanp`, by its PID), and delay its relay
  connection 1.5 s each way with netem on `lo` for that connection's port alone (a `prio` qdisc with a `u32` filter
  on `sport` and `dport`).
- Its relay connection lost: the relay connection is the one to the edge's port (`gateway` in `<folder>/edge.env`)
  with the most `segs_out` in `ss -tnpi`. Reset it with `ss -K` on that port, or drop it silently, as a sleep or a
  network change does, with iptables `DROP` on `lo` for its port both ways. A new `GET /relay` in `edge.log` is it
  connecting again: within seconds of a reset, and of a silent drop once its pings go unanswered.

## Logs and stopping

Everything is in the folder: `server.log`, `reloader.log`, `edge.log` (and `standby.log` with that flag), the servers'
and the edge's state, and the client's home; but the bucket, which is one of the machine's bucket store's, kept in
`~/.local/state/one-networks` with its `bucket.log`, its bucket named in the folder's `edge.env`. Starting again in the
same folder carries on with what's there; a new network in a folder you emptied has a new bucket, and the old one is
removed. The store is started by the first network that needs it and stops once the last one has: never stop it
yourself, as other agents' networks are in it. What its servers build of its apps (their entrypoints, compiled Elixir
and downloaded NIFs) is every server's on the machine, in `~/.cache/one_core` (`OneCore.BuildCache`), so a new network
beside another builds none of it again; it's safe to delete, and goes by itself once unused for a month.

Start it in the background, however you like (`setsid`, `mise exec`); its PID is then in `<folder>/pid`.
Stop it with `kill $(cat <folder>/pid)`, which stops all of it. Started again in the same folder it keeps its ports,
so a server installed with `one serve on` there reconnects by itself.

## Mistakes already made

- Starting a network with `--owner` and joining it with a virtual passkey just to approve a phone, or to see a page
  signed in: `browser.json` is signed in.
- Starting a whole network to work on an edge page that asks no server.
- Running `iex -S mix` in a fresh worktree, which has no deps: `mix deps.get` in `core/server/` first
  (`tooling/network` does it itself).
- Restarting the network to try a change to an app, rather than deploying it into the running one.
- Starting the app where there's no desktop without `dbus-run-session` (see `qa`'s Screens).
- Setting `CARGO_TARGET_DIR`: `tooling/network` runs `target/debug/one` from the repo, and worktrees sharing one run
  each other's builds.
