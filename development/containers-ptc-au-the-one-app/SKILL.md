---
name: containers
description: Read before creating or using a Linux container on the user's machines, as a scratch machine, a dev environment, somewhere to run Chrome or a desktop to look at.
metadata:
  title: "Containers"
  subtitle: "Linux machines when you need one"
  about: "Starts Linux containers on your own machines: somewhere to install, build and try things without touching your devices."
  category: Devices
---

Containers are Linux containers on the user's own machines, run by Podman. Use one when you need a machine of
your own to install, build, run or break things in, instead of the user's device itself. `machines` lists the
machines that run them.

- `create` takes an `image`, a `name`, what it's for in a few words (`description`) and a `size` (small, medium,
  large), and says each stage: pulling an image its machine hasn't got, waiting for `desktop` to be built, starting. A
  shell image such as `docker.io/library/ubuntu:24.04` keeps running with no command. Then `exec` runs commands in it, `read_file`
  and `write_file` move files up to 16 MB, and `logs` reads what its own command printed. `list` shows yours and their
  state, Podman's (an exited one with its exit code); one on a machine that's off is `unknown`, and a machine that doesn't answer is in `failed`, with why, while the others' are still listed. An app's code moves
  a file of any size with `upload` and `download`: to the bucket and back, sealed with a key it's given, a chunk at a
  time.
- `restart` at `create` is Docker's restart policy, which `list` shows: `no` (the default) leaves it stopped once its
  command ends, `on-failure` starts it again when that fails, and `always` whenever it ends and after the machine
  reboots. One stopped by hand, or for going unused, stays stopped until the next reboot. There's no `unless-stopped`.
- `image: "desktop"` is a Linux desktop: a 1280×800 display (Xvnc, `DISPLAY=:99`, which `screen` resizes) with Openbox
  and Google Chrome on it, downloaded from Google as each machine builds the image, as Containers starts there and
  again each week, in the background, so a desktop waits for it only in the minute after that: `machines` says how far
  its build is. A running one is a screen in Computer Use,
  called what the container is: look at it and act on it there. Chrome's DevTools Protocol is on port 9222 inside it
  (`exec` with `curl -s 127.0.0.1:9222/json`), and `playwright-mcp` is Playwright's MCP server, to start on it.
- `commit` makes an image of a prepared container, and `create` from that image's name makes throwaway copies of
  it on the same machine. `remove_image` removes it.
- A container reaches the internet but nothing of the machine's own: no files, no host network, no privileges.
  `ports` at `create` publishes ports on the machine's loopback, and `request` makes an HTTP request to one from
  there. A port can't yet be forwarded to your own device.
- `mounts` puts a folder of the machine itself into a container: it's the machine owner's own files, which the
  container can then change. Use it only when the user asked for that folder.

Containers cost memory and CPU on the user's machine while they run. Stop or remove one when you're done with it.
One left running and unused (no `exec`, file, screenshot or request) for `idle_hours`, 4 unless `settings` says,
is stopped on the hour; `start` brings it back with its files. Yours are yours: nobody else sees them but the
network's owner.

Every server that has Podman (rootless where it can be) runs containers by itself, with nothing installed. One that
can't says what it lacks in `machines` (`lacks`), in Settings and in Device Activity, and runs them once it has it.
