---
name: remote-shell
description: Read before running a command on one of the user's own devices with remote-shell_run.
metadata:
  title: "Remote Shell"
  subtitle: "Run commands on your devices"
  about: "Lets your AI run a command on one of your own devices, from anywhere. Every command is logged on the device it ran on."
  category: Devices
---

Run a shell command on one of your own devices with `run`; give `device`, a name `services` gives the servers
running RemoteShell.Runner, to choose which, or it runs on the device asked if that has Remote Shell, and otherwise
on the first that's up. It runs as the user that device's server runs as, in their home folder unless `dir` says,
and reads no input. Every command is logged on the device it ran on.

A device has Remote Shell once its service is installed there: `install_service --app remote-shell --service
RemoteShell.Runner --server <key>`. It runs any command for everyone that device's server acts for, so it's for a device whose
server acts for you alone, or for people you'd hand a terminal to.
