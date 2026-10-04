---
name: send-bridgezx
description: Send local files or directories to a ZX Spectrum Classic or ZX Spectrum Next through BridgeZX, using the explicit or last-known IP and honoring an optional remote destination or transfer sequence. Use when the user asks to send, upload, copy, or push artifacts to a ZX or Next with BridgeZX. Do not use for BridgeZX server updates or development of BridgeZX itself.
---

# Send BridgeZX

Complete the named transfer. The request only needs to identify what to send;
an explicit IP, target, remote directory, port, or order overrides the defaults.
Use the bundled executor, which delegates transport, naming, limits, CRC, and
target-specific behavior to the installed BridgeZX Python client.

## Authorization Boundary

A request to send or copy named sources authorizes those network writes to the
selected Spectrum. It does not authorize builds, server/client updates, deletion,
renaming, unrelated artifacts, or retries after an uncertain outcome. Build first
only when the user also requested a build or the named source unambiguously means
the output of the repository's documented build command.

## Resolve Inputs

1. Resolve every requested source to an absolute existing file or directory
   before network access. Preserve the user's explicit selection. If a shorthand
   matches multiple plausible artifacts, ask which one; do not select by mtime
   unless the user asked for the latest artifact.
2. Omit the remote destination unless requested. Pass a requested relative path
   through `--destination`; never convert it into a host path or invent a drive
   prefix.
3. Map an explicit Classic/ZX/divMMC destination to `--target classic`, and an
   explicit Spectrum Next destination to `--target next`. Omit `--target` when
   the user did not distinguish them. The executor probes and locks the detected
   target before sending.
4. Use one logical queue by default. BridgeZX traverses that queue in its own
   deterministic files-first natural order. When the user explicitly requires a
   sequence, pass `--ordered`; the executor sends each named source as a separate
   operation and stops at the first failure. To control order inside a directory,
   enumerate its files individually in the requested order.

## Resolve BridgeZX

Run `scripts/bridgezx_transfer.py` with a host-approved Python 3.10+ interpreter.
The executor imports the official `bridgezx` package; it does not implement the
wire protocol.

Client resolution follows the executor's actual precedence: explicit
`--client-root`, then `BRIDGEZX_CLIENT_ROOT`, then an already importable
`bridgezx` package. A supplied root must contain either
`bridgezx/__init__.py` or `client/bridgezx/__init__.py`. A supplied but invalid
root is an error, not permission to fall through to another installation.
If no root was supplied and the package is unavailable, check only the active
workspace and bounded sibling workspace candidates for a verified client;
pass a discovered checkout as `--client-root`. Do not search the entire
filesystem, clone, install, or modify BridgeZX. Ask for its path only when
these bounded checks find no client.

## Transfer

Invoke the executor once, using absolute source paths and only requested options:

```text
<python> <skill>/scripts/bridgezx_transfer.py [--client-root <root>] [--ip <ip>]
  [--port <port>] [--target classic|next] [--destination <remote-path>]
  [--ordered] <source> [<source> ...]
```

IP selection is owned by BridgeZX configuration: `--ip` wins; otherwise the
executor uses `last_ip`, then the first history entry. It probes only that IP.
Do not fall through to another remembered machine, because a reachable older
host may be the wrong Spectrum. If history is empty, ask for the IP. If the
probe is not ready, tell the user to start the matching `.brzx` or `.brzxn`
server and report the exact probe failure.

The executor validates all named sources before probing, verifies an explicitly
requested target, and locks the detected target during the send. Never replace
it with raw sockets, copied protocol logic, GUI automation, or a separately
maintained IP file.

## Result Contract

- Exit `0`: report IP, detected target, destination (or server directory), and
  the successful BridgeZX summary.
- Ordinary failure: report the failing source/operation and BridgeZX message.
- `uncertain` or interruption after transmission may have started: do not retry.
  State that the remote result must be checked before another send.
- Explicit ordered sequence: report how many operations completed before a
  failure; do not continue with later sources.

Keep the handoff short. Do not emit a command transcript unless diagnostics are
needed.
