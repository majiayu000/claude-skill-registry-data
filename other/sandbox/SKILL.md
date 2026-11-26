---
name: sandbox
description: Read when an untrusted app can't reach something, or before deciding whether to install an app trusted or untrusted.
metadata:
  title: "Sandbox"
  subtitle: "Apps you don't know, kept apart"
  about: "Runs apps you don't fully trust walled off from your machines, with only what you let them have."
  category: Admin
---

An untrusted app runs behind this machine's own sandbox (bubblewrap on Linux, Seatbelt on a Mac, an AppContainer
on Windows): it reaches only what One Core hands it, and the tools and hosts its `permissions/0` names. When one
can't reach something, it's that its permissions don't name it; deploying it trusted (`--trusted`), which only someone
who may install for whoever it's for may do, runs it with its server's full access instead.

A server whose machine can't make that sandbox (no bubblewrap or prlimit on Linux, or one that doesn't allow it)
says what it lacks, in `services` and in Device Activity, and runs untrusted apps once it has it.
