---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: lan-macs
description: >
  Find the other Macs on the user's local network and SSH into them. Lists every Mac
  with Remote Login on (Bonjour _ssh._tcp) plus .local hosts in ~/.ssh/config, checks
  key access, and shows where the sudo password is in Keychain. Use when the user
  mentions another Mac, "the other computer", a Mac by name, ssh into a machine on the
  network, the Kimaki fleet, or running something on a different Mac. Also covers adding
  a new Mac to the network (add-mac.md).
---

# lan-macs

Other Macs on the LAN are reached by SSH on their Bonjour name, `<name>.local`. Never hardcode a host. Always list first:

```bash
bun ~/.config/opencode/skills/lan-macs/list-hosts.ts
```

Output, one block per Mac (this Mac is skipped):

```
studio.local
  ssh:      ssh studio
  status:   ok: "studio", user tommy, macOS 26.1 arm64
  password: in Keychain: security find-generic-password -a tommy -s studio.local -w
  found by: ssh-config, bonjour
```

Then run commands with the `ssh:` line:

```bash
ssh -o BatchMode=yes studio 'uname -a'
```

## Status values

| status | meaning | what to do |
|---|---|---|
| `ok` | key auth works | use it |
| `offline` | `.local` name does not resolve | Mac is off, asleep, or on another network. Tell the user |
| `unreachable` | port 22 times out | Mac is asleep or locked. Ask the user to unlock it once |
| `refused` | port 22 closed | Remote Login is off. See add-mac.md step 2 |
| `no key access` | wrong user or no key | add a `Host` block with `User`, or authorize the key (add-mac.md step 4) |

The SSH user comes from `User` in `~/.ssh/config`. If there is none, the script guesses `tommy`, the admin user on every Mac in the fleet.

A Mac only shows from Bonjour while it is awake with Remote Login on. A Mac in `~/.ssh/config` always shows, even when offline.

## Passwords and sudo

Key auth needs no password. The login password is only for `sudo`. It lives in this Mac's Keychain with service `<name>.local` and account = SSH user.

- Never print the password, never put it in a command argument, never paste it in chat.
- Pipe it straight to `sudo -S` on the other Mac:

```bash
security find-generic-password -a tommy -s studio.local -w | ssh studio 'sudo -S -p "" whoami'
```

If the password is not in Keychain, ask the user to store it (they type it, `-w` prompts):

```bash
security add-generic-password -a <user> -s <name>.local -w
```

## Gotchas

- `ping` works but SSH times out: the Mac is locked or asleep. Unlock once, then disable sleep (add-mac.md step 2).
- SSH over IPv4 timed out once while IPv6 worked. Try `ssh -6 <host>`.
- SSH has no TTY. GUI permission prompts (Accessibility, Screen Recording) and Chrome first run must be done by the user on the Mac's screen.
- To browse Bonjour by hand, stop `dns-sd` with SIGINT, not SIGTERM. SIGTERM loses its buffered output when stdout is a pipe.

## Add a new Mac

Read [add-mac.md](add-mac.md): Remote Login, hostname, SSH key, Keychain password, no-sleep, Homebrew, apps, Kimaki from source.
