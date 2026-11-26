---
name: home-screen
description: Read before putting an app or a widget on a Home Screen page, arranging one, answering what's on someone's, or giving an app's entrypoint a category or the user it's about.
metadata:
  title: "Home Screen"
  subtitle: "Your pages of apps"
  about: "Your Home Screen, everyone's and your groups': pages of apps and widgets, arranged your way, and an App Library of every app you can reach, by category."
  category: Utilities
---

Home Screen is the network's launcher: the app every client opens first, which draws the rest. It keeps how each
owner's pages are arranged: `pages` gives an owner's Home Screen, `arrange` changes its pages, and `add` and `remove`
put an app on them or take it off. A person edits their pages as on a phone: touch and hold, or right-click, then Edit
Home Screen. Apps are installed with the App Store, whose `app-store_marketplace` lists what could be.

Its words:

- **Home Screen**: every owner's pages, then the App Library, one for everyone you can reach.
  An owner is a user, a group, or the network, which a person reads as Everyone. A user sees their pages, everyone's
  and their groups', and moves between them with the owner switcher.
- **Page**: a fixed grid of apps and widgets, four across and six down, which never scrolls: what doesn't fit goes on
  the next. It holds only what was put there. A page can be hidden, kept but not shown, and a page with nothing on it
  goes. An owner's pages are one layout, so arranging everyone's or a group's arranges it for everyone who sees it.
  The user themselves arranges theirs, and a group's or the network's `owner`s theirs (`arranges`).
- **App Library**: every app that runs for an owner, by category: what's installed for them and for each broader
  owner they're within. A user's, the one a person sees, shows theirs, their groups' and everyone's; asked for a group
  (`pages`), its own and everyone's; for everyone, only everyone's. Each app is there once, as the narrowest
  install's, and a group's opens for the group. An app installed lands there, not on a page. An app goes on an
  owner's pages only where it opens for them, installed for them or for everyone (`pages`' `apps`).
- A background app, with no entrypoint, is only in the App Library, under Background Apps, and opens its section in
  Settings (its own page there, or a section of its sidebar); one with no section isn't listed on a computer's or a
  phone's screens, which ask Settings for them (`settings_sections`). `add` refuses it and `arrange` skips it, each
  saying why.
- One about whoever opens it (`subject: "user"`) is only in a user's App Library, wherever it's installed, and opens
  for them.
- Installing an app puts its code on a server, so for the network only its owners and those they let (`installer`,
  see `permissions`) do it, and for a group, its owners. Whoever can't asks one of them themselves.

## Categories

An App Library groups apps by the categories the App Store does, an app's `metadata.category` (the skill
building-apps), in that order. An entrypoint that's for something else than its app says one of them as its own
`category`. Admin, what other apps stand on, shows only to the network's owners.
`launcher` is this one's.

## Who an app is for

An app opens for whoever's Home Screen it's on, or whose App Library it's in. One about whoever opens it, as Settings
and Notifications are, says `subject: "user"`: it's in the user's own App Library and opens for them,
wherever its app is installed.
