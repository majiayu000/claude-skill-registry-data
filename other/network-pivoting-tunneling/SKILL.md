---
name: network-pivoting-tunneling
description: >
  Pivot into internal networks from a foothold — tunnels, port-forwards, and proxychains. Load
  when a host has a second NIC / reaches an internal subnet you can't hit directly, on
  "pivot", "internal network", "double-hop", after a foothold in a multi-host lab.
domain: network
type: technique
stability: learning
modes: [pentest]
severity: high
mitre: [T1090, T1572]
tools: [ligolo-ng, chisel, sshuttle, proxychains, socat]
schema_version: 1
---

# Pivoting & tunneling

## When it applies
You have a foothold on host A, and the objective (or the next host B) is only reachable from
A's network. You need to route your tools through A.

## Why it works
The foothold sits inside the trust boundary. A tunnel turns that host into a router/proxy so
your attack host can reach internal services as if it were on that subnet.

## Method
1. **Discover internal reach** from the foothold: `ip a`/`ipconfig`, `arp -a`, and scan the
   internal range for live hosts/ports (upload a static scanner or use built-ins).
2. **Pick a tunnel**:
   - **ligolo-ng** (preferred): agent on the target, add a route to the internal CIDR; you get
     a clean interface — all tools work natively, no proxychains.
   - **chisel**: `chisel server --reverse` on you, `chisel client ... R:socks` on target → SOCKS.
   - **sshuttle**: if you have SSH creds — `sshuttle -r user@A 10.10.0.0/16` (VPN-like, simple).
   - **ssh -L/-D**: local/dynamic forwards for one-off ports or a quick SOCKS proxy
     (`-L 8080:internal:80`, `-D 1080` for SOCKS, `-R` to expose your listener to the target).
   - **socat relay**: on the foothold, `socat TCP-LISTEN:9999,fork TCP:internal:80` forwards a single
     internal port — handy when only socat is present.
   - **Windows foothold, no SSH**: built-in `netsh interface portproxy add v4tov4 listenport=8080
     connectaddress=<internal> connectport=80`, or `plink.exe -D 1080 user@$LHOST` for SOCKS.
   - **DNS/ICMP egress only**: when TCP is fully filtered, tunnel over DNS (`dnscat2`, `iodine`).
3. **Route tools**: with ligolo, just target the internal IP; with SOCKS, prefix `proxychains`
   (set the port in `/etc/proxychains4.conf`) — note UDP/ICMP don't traverse SOCKS.
4. **Chain hops**: repeat from B to reach a third subnet (double pivot). `ssh -J` chains jump hosts;
   ligolo just adds another route.

## Gotchas
- proxychains + nmap: use `-sT` (TCP connect) and skip ping (`-Pn`); SYN scans won't tunnel.
- Match the agent binary's arch/OS to the target; static builds avoid dependency pain.
- Note every route/tunnel in `state.md` so you can tear them down and reproduce for the report.

## Verify success
Your attack host reaches an internal-only host/service through the tunnel (a scan or login that
was impossible directly now works).

## References
ligolo-ng & chisel docs; `ad-pivot-arsenal` (this library) for the AD-focused arsenal.
