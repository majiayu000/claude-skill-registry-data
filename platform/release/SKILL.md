---
name: release
description: Use once your change is on main, to put it live on the network by the smallest path it needs, or to see what is live. Whoever makes a change releases it.
---

Release from `main` as it is now, never an older commit, and only what your change touched.

Check `one builds` first: if the build for your part is from a commit that has yours, you're live and run nothing.
`tooling/release` checks the same before it builds, and a release of a commit that a build the network has, or the
release holding the machine's lock, already contains ends on its own with exit status 0, saying which build to follow
with `one builds`. Only a release whose commit nothing covers waits, one release of a kind at a time.

A release is part of your change: it isn't done until it's live.

## Versions

The platform (One Core's server, the UI library, the edge, the clients and what they say to each other) has one
version, and each app one of its own, Semantic Versioning's. `tooling/version` says the platform's, and
`tooling/version apps/<name>` an app's, from the Conventional Commits that touch that part's paths, as
release-please's manifest mode does: a breaking change (`type!:` or a `BREAKING CHANGE:` footer) takes the next
minor, a `feat` or a `fix` the next patch, and a commit touching two parts moves each. Before 1.0 a minor is
breaking, as Cargo, npm and Hex read 0.x. A build is that version with its commit's count and hash as build
metadata, `0.18.2+2974.febd37350abc`. Nothing decides a bump but how commits are marked and what they touch: `!`
marks what breaks whoever uses the part the commit changes. A version names a release and refuses nothing: an app's
`!` moves only that app, and the platform's whether parts talk is their protocol's. One that wasn't marked is marked by a commit after it
that touches the same part, `fix!: <what broke>`, before it's released.

Exactly two rules hold at runtime:

- Parts talk where the protocols they speak overlap (`OneCore.Protocol`, `core/protocol.json`), whatever their
  versions. A server refuses a request of a part that speaks none it does (`OneCore.Mcp`), saying why; a server asks
  one like that nothing, as if it were off; the relay passes the edge's calls only to servers that speak one it does
  (`core/edge/relay/relay.ts`), apart from whether they're ready. What updates a part that's behind, `tools/list`,
  `builds`, `download`, `update` and its task's `tasks/get`, is answered whatever it speaks, so a client of any
  version can always update. `one builds` says each part's `protocol`, the `edge_protocol`, each device's
  `last_seen`, whether each server is `connected` now (if not, its update as it last said it is under `last_said`, as of its
  `last_seen`), and `why` a server doesn't talk.
- An app runs on a server on its `requires`' `"core" => ">= 0.16.0"` or newer (`OneCore.Apps.Version.platform/1`,
  worked out from the two versions, never kept): `runs`, or `waiting_for_server` on an older one (deploying it there
  is refused, saying so). `one apps` and `one builds` say which, and a server that can't run one says why in
  telemetry.

## Order

Publishing is all a release does: as the core's release, `builds` on GitHub, which every network takes its builds
from, its edge telling it within five minutes (`core/edge/updater/core.ts`), so no release names a network. Each
network's update takes every server to the latest build by itself (`core/edge/updater/updater.ts`): each awake server
prepares it, then each restarts on it, one at
a time, never the last ready one. A build published while another is under way takes its
place; a server asleep or gone is caught up once it's back; one that goes back holds it, saying which and why, until
a newer build or Update Now (the `update` tool). A server behind the network's build with none prepared, as a laptop
that slept through releases, steps aside until it's on it (`OneCore.Servers.Aside`): it takes no calls and runs no
services or jobs, so what only it runs (a Mac's iMessage, Remote Shell there) waits for its update. Run no
`one update` for a release. `one builds` says how far it is
(`network`: its `network_update_status`, the servers `behind` it, and when each step was reached, in `timings`).
Nothing is watched after a release: each server verifies a build before it keeps it, and a bug found later is fixed
forward.

Any release mixes with what's live, a breaking one too, since a release that changes the wire speaks the protocol
before beside its own. Release the servers first, then the edge from the commit they run, then the clients. `tooling/release` refuses a build that speaks
no protocol a server, the edge or a device that talks with them does, naming which: drop an old protocol only
once none of them speaks only it. Devices are otherwise not waited for, since their people update them.

| Changed | Release |
| --- | --- |
| One of this repo's apps (`apps/<name>/`) | `tooling/release server`: every network's servers take the core's apps to the commit of the build they start on (`OneCore.Apps.Lifecycle.update_core_apps/0`), each whose folder changed, as a new version every install of it takes, so no release names a network |
| An app of a network's own repo | `ONE_SUBJECT=network one deploy --name <name> --files-from apps/<name>`, from that repo, into its network (about 12 s). Refused, someone else's newer change is live: rebase and deploy again, never `--force` |
| An app with a NIF (`server/nif/`) | `tooling/nifs` first. A Mac's NIF whose inputs haven't changed is the one last published (or cached here); one that changed is built on a Mac (a few minutes): GitHub's macOS runner, or the Mac `ssh mac` reaches when GitHub has no runner for it within 5 minutes (`tooling/on-mac`) |
| An app's native code (`server/nif/`, `server/bin/`) | Also `tooling/publish-nifs` once it's on `main`: it publishes the new builds to a GitHub Release and pushes their `server/checksums.json`, from which every network updating the app from git gets them. A Mac's are built on a Mac (`tooling/on-mac`) |
| The UI library (`core/ui/`) | The server, which ships it and builds every app again against it, then the edge, which serves it to browsers |
| The edge (`core/edge/`, an app's `edge/`, `clients/web/`, and the app's window page `clients/app/page/`, which every app on a build it runs on loads from its next start, phones too) | `bun install && flock ~/.cache/the-one-app/release-server.lock bun edge.js deploy https://<the network's host>` in `core/edge/`; it reads that network's Cloudflare token from 1Password itself (the item "Cloudflare edge deploy" tagged `vault/<host>`, or `CLOUDFLARE_API_TOKEN`), deploys to the account of the zone the host is on, and refuses, deploying nothing, where the token can't see that zone or where the edge there is a newer build than this one (`--allow-downgrade` goes back on purpose) |
| The server (`core/server/`, or Rust it builds with) | `tooling/release server`, which reads the build signing key from 1Password itself, as every `tooling/release` does. Each server restarts on it in turn (a few seconds each), never the last ready one; a server whose `one` is new restarts on that `one` too, so no device's server runs an old `one` |
| The desktop app or CLI (`core/client/`, `clients/`, an app's `client/native/`) | `tooling/release client`. Every device takes it by itself: a server's `one` as the network's update takes it (restarting each server on it, one at a time), and a desktop app as it hears of it, starting again on it (`clients/app/src/updater.rs`). `client` includes the Mac's build, made on GitHub's macOS runner and the owner's Mac at once, whichever is first (`tooling/on-mac`; about 2 minutes, 8 with nothing cached: run `client` with your harness's longest timeout; a second release of the kind waits for the first only when its commit isn't in the first's), and only when what it's built from changed since the network's latest `one/macos-aarch64` (so is every client: one that didn't keeps its build, and `one --version` says which that is); Linux's alone is `tooling/release one/linux-x86_64 one-cli/linux-x86_64` (about 4 min). Once it's ended, published or covered, it publishes every network's installers from its latest builds, which its download page offers (`tooling/installers`, for each repo `tooling/networks` lists, each as this machine's client of that network; a Mac's notarised by Apple, about 2 min each) |
| A phone's app | Every network's iPhone app goes to its own TestFlight with `tooling/release client`, where its native code changed (`tooling/testflight`, from each network's repo, `tooling/networks`), and its testers' phones take it; its page and its apps reach it without one. Only Andre's own devices (the internal group) get each build: a network's people get one at a milestone, `tooling/testflight --milestone <the network's repo>`, which Andre calls. Android's plain APK, `one/android-aarch64`, is built here by `tooling/release client` (`cargo tauri android build --apk`), and each network's own made from it and published by `tooling/installers` (`tooling/android-apk`), which its phones install by themselves (`clients/app/src/updater.rs`) |
| Docs, `tooling/`, `.agents/` | Nothing |

Windows' builds, `server/windows-x86_64`, `one/windows-x86_64`, `one-cli/windows-x86_64` and the app's installer,
`one-setup/windows-x86_64` (NSIS's `makensis`, `apt install nsis`), are made on Linux like the others, and are
built only for a network with a Windows server or device. The owner's Surface is one, a server of the live network
since 18 Nov.

An app change that uses something new in `core/server/` says so in its `requires`, `"core" => ">= 0.16.0"`: a
server still on an older build has it `waiting_for_server` until its update.

This repo's apps are the network's own trusted apps, deployed from git at the commit of the build each network's
servers run: by a new network's first server (`found/1`), and by each server that starts on the network's latest
build (`update_core_apps/0`), never taking one deployed from a newer commit back. A network being built
(`tooling/network`) deploys them from the checkout, and a change to one reaches it as its code reloader says.

On a device that is also a server, `one update` is the network's Update Now. What a server did is in the log of the
program keeping it running (`one serve run`), `journalctl --user -u one-server-<key's first 12>` on Linux.

Run an edge deploy only while no server release publishes on the machine, by taking its lock, which waits for one that
does: `flock ~/.cache/the-one-app/release-server.lock bun edge.js deploy https://<host>`. A network's address is in
Agent Memory, not the repo.

## Secrets

1Password is the source of truth for secrets. What a release or a signature needs is read from it where it's used
(`op read`). What a network's apps use at runtime is kept in 1Password too, as an item tagged `vault/<the network's
host>` (or `vault/<host>/groups/<name>` for a group's), titled and with fields named as its Vault item, in the
network's own 1Password vault: `ptc-nosudo` for PTC's, `van-tonder-nosudo` for Andre's, `shared-nosudo` for one both
use. `tooling/vault-sync` puts each into its network's Vault, one way: change a secret in 1Password, then run it. A
new runtime secret goes into 1Password first. A person's own items (their sign-ins, Chrome profiles) and recovery keys
are never synced.

## What is live

- `one builds` gives the network's update (`network`), each server's `build` as `<version>+<count>.<commit>`, and the
  `edge`'s.
- `git diff --stat <commit> origin/main` is what isn't live on the server.
- `ONE_SUBJECT=network one code --name <app>` is an app's files as deployed.

## Mistakes already made

- A breaking release that apps' code can't run on (the plugin-to-app rename, 17 Nov) leaves sign-in not running on
  each server it reaches, so nobody is signed in there and nothing can be deployed to it: keep sign-in's new version
  first with the new build's own `OneCore.Apps.Store.keep/8` on a server's machine (as the bucket is reached without
  the node) and restart that server.
- Releasing everything when one app changed. A server release is minutes and restarts every server; an app is
  seconds.
- Releasing a server build onto storage whose stored names it had renamed. A rename of anything kept (a blob prefix,
  a database, a table) needs a one-time rename of what's stored first; say so in the commit and do it before
  `one update`.
- Releasing from a worktree behind `origin/main`: a build the network has from a newer commit covers it, so `tooling/release` publishes none of it.
- Releasing a server from a tree with changes not committed: the build is `.dirty`, and every server refuses it
  ("says it's ….dirty, not what was published").
- Changing what servers ask each other (`hooks/call`, `apps/call`, what a call passed on says in `_meta`) so the
  version before reads it wrongly while the release reaches them (`This device isn't signed in here`, 240 times in
  three minutes): keep it compatible for one release, the new beside the old. A server that can't take its update
  (`permissions couldn't decide it`) is taken by hand, as its program would: download the build `one download --target <kind>` links, unpack it in its
  `server/builds/<build>` past `bin/one_core eval "OneCore.Release.check()"` saying that build, set `next` to
  `{"build": <it>, "program": <its one --version>}` and `server_update_status` to `verifying` in `server/state.json`,
  and restart its unit (`systemctl --user restart one-server-<key's first 12>`, or on a Mac
  `launchctl kickstart -k gui/$(id -u)/app.theone.server.<key's first 12>`); it goes back by itself if it doesn't
  answer.
- Deploying the edge before the servers, from a commit they don't run: its relay took them all for gone and server
  updates went back (17 Nov). It now sends nothing only to those that speak no protocol it does; the edge still
  goes after the servers.
- A breaking release that removed two app categories (17 Nov), when parts talked only on one 0.minor and apps
  pinned one with `~>`: the network split in two and six apps waited for updates. Now apps say a minimum.
- Refusing parts by how many 0.minors apart they were (until 19 Nov): three `!`s that changed nothing on the wire
  took the platform from 0.24 to 0.26, and phones on 0.24 that spoke exactly what 0.26 does were refused. Now parts
  talk by their protocol.

## Report

What you released, by which command, and the minutes from your commit reaching `main` to `one builds` (or
`one code`) showing it live: for a server, its `network.timings`.
