---
name: proxychains
description: "Route a TCP client through SOCKS/HTTP proxies with the host's proxychains4 config (dynamic_chain, proxy_dns, 127.0.0.1:1080) and the pp alias. Use when a tool has no proxy flag but must egress through a pivot; Not for UDP, ICMP or static binaries (use ligolo-ng) or for intercepting and rewriting traffic (use mitmproxy)."
---

# proxychains

proxychains4 is an `LD_PRELOAD` shim: it replaces `connect()` in a dynamically linked binary so that every TCP connection goes to a proxy instead. On this host it is version 4.17-1, configured at `/etc/proxychains4.conf`, with `pp` aliased to `proxychains4 -q`. It is the cheapest way to make a stubborn tool egress through a SOCKS listener, and it fails silently in several situations that matter.

## When to use

| Situation | Use proxychains | Better alternative |
| --- | --- | --- |
| CLI tool has no `--proxy` flag | yes | - |
| Quick one-off request through a pivot | yes | `curl -x socks5h://...` is simpler |
| Whole subnet reachable through a pivot | no | ligolo-ng TUN routing |
| UDP, ICMP, or SYN scans | no | ligolo-ng |
| Statically linked or setuid binary | no | ligolo-ng, or a proxy-aware client |
| Intercept, replay, rewrite HTTP | no | mitmproxy |
| Browser with its own proxy settings | no | `--proxy-server` on Chrome |

## Prerequisites

- `/usr/bin/proxychains4` and `/usr/bin/proxychains` (same binary), library `/usr/lib/x86_64-linux-gnu/libproxychains.so.4`.
- A live SOCKS listener at the address in `[ProxyList]`. Fresh boxes have none: `ss -ltnp | grep -E ':1080|:9050'` is empty until chisel, ligolo or `ssh -D` starts one.
- `pp` is a zsh alias in `~/.zshrc` (`alias pp='proxychains4 -q'`), so it exists only in interactive zsh.
- The target binary must be dynamically linked; check with `ldd <binary> | head -1`.

## Core invocations

```sh
# 1. no arguments prints the two flags it actually takes
proxychains4

# 2. smoke test: preload works, no network involved
proxychains4 -q id                 # uid=0(root) gid=0(root) groups=0(root)

# 3. the alias form used in this environment
pp id

# 4. is anything listening on the configured proxies?
ss -ltnp | grep -E ':1080|:9050'

# 5. prove egress through the chain; 000 with rc 7 means the proxy chain is dead
proxychains4 -q curl -s -m 5 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:80/

# 6. compare against the direct path (a local listener answers 308 here)
curl -s -m 5 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:80/

# 7. TCP connect scan through the pivot; -sT is mandatory, SYN scans bypass the shim
pp nmap -sT -Pn -n -p 22,80,443,445 10.0.0.5

# 8. shell, ssh and git all inherit the preload
pp ssh -o ConnectTimeout=8 user@10.0.0.5
pp bash -c 'curl -s -o /dev/null -w "%{http_code}\n" http://10.0.0.5/'

# 9. per-run config: strict single-proxy chain, nothing skipped
cat > /tmp/pc-strict.conf <<'EOF'
strict_chain
quiet_mode
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5 127.0.0.1 1080
EOF
proxychains4 -f /tmp/pc-strict.conf curl -s http://10.0.0.5/

# 10. debugging: drop -q so the library prints the chain it picked
proxychains4 curl -s -m 5 -o /dev/null http://10.0.0.5/

# 11. confirm the binary is even eligible for preloading
ldd /opt/tools/chisel | head -1        # "not a dynamic executable" -> shim cannot work
file /usr/bin/curl | cut -c1-80        # dynamically linked -> eligible

# 12. run through tor's listener when it is the only one alive
ss -ltnp | grep 9050
proxychains4 -q curl -s --socks5-hostname 127.0.0.1:9050 http://10.0.0.5/
```

## Flags that matter

CLI flags:

| Flag | Effect | Note |
| --- | --- | --- |
| `-q` | quiet: no chain logging | hides the diagnostics you need while debugging |
| `-f <file>` | alternate config | the only two options it accepts |
| `-h` | not a flag | parsed as the program name: `can't load process '-h'` |

Config directives in `/etc/proxychains4.conf`:

| Directive | Here | Meaning |
| --- | --- | --- |
| `dynamic_chain` | on | use proxies in order, skip dead ones; if all are dead the call fails |
| `strict_chain` | off | all proxies must be alive, in listed order |
| `random_chain` / `round_robin_chain` + `chain_len` | off | rotate per connection |
| `quiet_mode` | on | same as `-q`, always on here |
| `proxy_dns` | on | resolve names through the proxy via the `224.x.x.x` mapping |
| `remote_dns_subnet 224` | on | synthetic range used for that mapping |
| `tcp_read_time_out` / `tcp_connect_time_out` | 15000 / 8000 ms | raise for slow links, not for timeouts you want to see |
| `localnet ...` | all commented | nothing is excluded, including `127.0.0.1` and RFC1918 |
| `dnat` | commented | rewrite destination host/port |
| `[ProxyList]` types | `socks4`, `socks5` | also `http`, `raw`; numeric IPv4 only |

Current list: `socks4 127.0.0.1 9050` (tor) then `socks5 127.0.0.1 1080` (chisel/ligolo listener). With `dynamic_chain`, a dead 9050 is skipped and 1080 is used; if both are dead every connection fails.

## Workflow

1. **Start the listener first.** chisel, ligolo or `ssh -D 1080`; confirm with `ss -ltnp | grep 1080`.
2. **Smoke test before the real tool.** `pp curl -m 5 -o /dev/null -w '%{http_code}\n' http://<reachable-internal>/`. `000` means the chain, not the target.
3. **Run with `-q` off once.** The library's line `1<--socks5--127.0.0.1:1080<--163.5.1.1:80` tells you whether the destination is being proxied at all.
4. **Watch for silent bypass.** Confirm the binary is dynamic (`ldd`), not setuid, and not doing its own networking (DoH, QUIC, raw sockets).
5. **Limit the tool.** One connection per second through a pivot is normal; `nmap -sT -T3` and `--max-rate 50`, not a `/16` sweep.
6. **Escalate to ligolo-ng** as soon as you need UDP, ICMP, many hosts, or a statically linked binary.
7. **Clean up** the config edits; `/etc/proxychains4.conf` is a system file.

## OPSEC and telemetry

- The proxy sees every destination, hostname and payload in clear text unless the application encrypts it. A third-party SOCKS relay is a full observer.
- `proxy_dns` maps names to `224.x.x.x` addresses; an application that caches or re-resolves those can emit odd traffic.
- With no `localnet` entries, connections to `127.0.0.1` and RFC1918 also go to the proxy. That breaks local API calls (for example a DevTools endpoint on 9222) and can leak internal addresses to the relay.
- proxychains does not change timing or volume: a scan through a tunnel is still a scan, now visible to both the pivot owner and the target.
- SOCKS credentials in `[ProxyList]` are stored in plain text in a world-readable file.
- A setuid binary drops `LD_PRELOAD`; if you expected a proxy and got a direct connection, nothing warned you.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `000` and curl rc 7, direct request works | no live listener; `dynamic_chain` skipped all proxies | start the SOCKS listener, re-check `ss -ltnp` |
| `can't load process '-h'` | `-h` is not a flag, it is taken as the program name | run `proxychains4` with no arguments for usage |
| Tool connects directly, ignores the proxy | statically linked binary (`/opt/tools/chisel` and most Go tools) | use ligolo-ng, or the tool's own proxy flag |
| Same, for a setuid binary | loader drops `LD_PRELOAD` for setuid | run as a non-setuid path, or route with ligolo-ng |
| `pp` not found | alias lives in interactive zsh only | `proxychains4 -q ...` in scripts |
| Localhost calls fail under proxychains | no `localnet` entries, so 127.0.0.1 is proxied too | add `localnet 127.0.0.0/255.0.0.0` or run that call unproxied |
| Every connection times out but the proxy is up | proxy expects no auth, or the wrong SOCKS version | match the `[ProxyList]` type; test with `curl -x socks5h://` |
| DNS still leaks | app uses DoH/DoT or a static resolver | disable DoH, or use a tool that resolves proxy-side (`socks5h`) |
| Gateway/ICMP unreachable through the tunnel | proxychains is TCP-only | ligolo-ng |

## Verification

```sh
proxychains4                          # Usage: proxychains4 -q -f config_file program_name [arguments]
proxychains4 -q id                    # uid=0(root) gid=0(root) groups=0(root)
grep -E '^(dynamic_chain|quiet_mode|proxy_dns)' /etc/proxychains4.conf   # three lines
tail -6 /etc/proxychains4.conf        # socks4 127.0.0.1 9050, then socks5 127.0.0.1 1080
ss -ltnp | grep -E ':1080|:9050'      # empty until you start a listener
proxychains4 -q curl -s -m 5 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:80/   # 000, rc 7
```

A working chain shows a non-`000` status. The `000` above is the documented dead-proxy behaviour on this box, not a config error.

## Related skills

- [chisel](../chisel/SKILL.md) for the SOCKS5 listener this config points at
- [ligolo-ng](../ligolo-ng/SKILL.md) when TCP-only proxying is not enough
- [segfault-cli](../segfault-cli/SKILL.md) for `PROXY`/`TOR`, which print addresses for `curl -x`
- [mitmproxy](../mitmproxy/SKILL.md) for rewriting HTTP instead of forwarding it
- [toolchain-router](../toolchain-router/SKILL.md) to choose between proxy and route