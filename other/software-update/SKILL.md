---
name: software-update
description: Read when the network's edge is behind its servers' build, when Software Update says the edge went back, before setting up a network's edge to update itself, to choose which devices get dev builds, or to publish the network's installers.
metadata:
  title: "Software Update"
  subtitle: "Keeps your network's edge current"
  about: "Updates your network's web address, sign-in pages and web app to the build your servers run, by itself, after every update. Choose which of your devices get dev builds."
  category: Admin
---

The network's update takes its servers to each build. Once they're all up to date on one, it has one of them deploy
that build's edge, the part of the network at its address (`core/edge/updater/updater.ts`): the edge's own update,
`edge_update` in `one builds`, which never holds the servers'. This app is what deploys it there: with it installed for
the network, a server says it deploys the edge (`deploys_edge`), and one ready server on the build is told to. The
deploy checks Cloudflare says the edge is live as that build and rolls every Worker back if not. It's tried once a build, and Update
Now tries again: `edge_update` says `needs_setup` where this app can't use the token, and `failed`, with why, where
the deploy went back.

It deploys with the network's Cloudflare API token: the field `api_token` of the item `Cloudflare edge deploy` in the
network's Vault, switched on for this app, a token that can edit Workers and read the zone of the network's address.
Only a server that opens the network's Vault reads it, and it never leaves that server. To set it up, keep the token
there (`vault set`, as a plain tool on a device, `ONE_SUBJECT=network`, `secret: true`), and ask its person to switch
it on for this app with `vault request` (`app: "software-update"`), whose link they open and Allow.

## Dev builds

`dev_builds` lists your devices (Sign-In's apps), each with whether it gets dev builds, and `set_dev_build` switches
one: the network's one setting, which each person changes for their own devices. A device is on until it's switched
off, so a new one starts on. The Home Screen widget Dev Builds shows the same, a row to press for each device.
`tooling/release client` reads it and builds only for the devices that are on, saying which targets it skipped and why;
a device that's off keeps its build and gets the next release once it's on again. Servers and the edge always get every
release, so a device that's one of the network's servers isn't one of these: its target's `one` is built whenever a
server needs it, and it's no row to switch.

## Installers

The network's own installers, its app as a person installs it the first time on a Mac, Windows, Linux or Android, are
kept here: `installers` lists them, and `tooling/release client` publishes each (`publish_installer`, the file sent as
an upload: `one software-update publish_installer --platform mac --name "the PTC App.dmg" --build <build> --file-from
<path>`), in place of the one before. The Downloads app offers them on the network's download page, <address>/download,
and `installer` gives one with a link that downloads it. From then on the app updates itself: a Mac's from its disk
image, and Windows' from its program, `windows-program`, published beside its installer with its SHA-256, which the
page doesn't offer.
