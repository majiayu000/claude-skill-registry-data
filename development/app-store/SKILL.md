---
name: app-store
description: Read before showing a person which apps they could install, or answering what's in the network's marketplace.
metadata:
  title: "App Store"
  subtitle: "Find, install and manage apps"
  about: "Every app your network can install, by what it's for, and what's installed for you, everyone and your groups: install, update, uninstall and bring back."
  category: Utilities
---

The App Store is the app a person installs and removes apps with, as VS Code's Extensions view is: Marketplace, every
app the network can install, and Installed, what's installed for each owner they see. `marketplace` lists the
first: every app anyone in the network deployed, then the app directory's (one.ptcau.dev/apps) that aren't
among them, each with what it requires and why. Installing and the rest are One Core's own tools (`install`,
`uninstall`, `apps`, `apps_update`, `apps_retry`, `apps_trust`), which an agent calls itself. An uninstalled app
is restored, with what it kept, in Recently Deleted (`soft-delete restore`), as everything deleted is.

An app only the directory has is a stranger's code, not yet in the network: the skill installing-apps says how
to check it for the person and install it (`one install <source> --app <name>`), which the app leaves to their AI.
