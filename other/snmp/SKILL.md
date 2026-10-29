---
name: snmp
description: Use when enumerating SNMP services on authorized targets,
  typically UDP 161. Covers finding SNMP hosts, testing default and common
  community strings, walking MIB trees with snmpwalk and snmpbulkwalk for
  system info, interfaces, routes, users, and running processes, probing
  SNMP write access safely, and handling SNMPv3 auth. Use when a network
  device, printer, or server exposes SNMP and you need configuration,
  credential, or topology data before deeper testing.
version: 1.0.0
domain: network
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [nmap-methodology, recon-active]
tools:
  - name: Net-SNMP
    version: 5.9.4
  - name: nmap
    version: "7.98"
  - name: Python
    version: "3.12"
---

SNMP (Simple Network Management Protocol) lets administrators monitor
network gear, and it is still deployed with the default community strings
`public` and `private` far too often. A readable SNMP service can hand you
hostnames, interface tables, routing tables, ARP tables, running processes,
installed software, and sometimes usernames. A writable one can change device
configuration. This skill covers authorized SNMP enumeration on UDP 161:
finding services, guessing community strings, walking the MIB tree for
useful data, and testing write access without breaking the device. All
testing targets systems you have written permission to test.

## Quick Workflow

1. Find hosts with UDP 161 open on the target range.
2. Identify the SNMP version and test the default community strings.
3. Brute force a short list of common community strings if defaults fail.
4. Walk the standard MIB branches: system, interfaces, IP, and processes.
5. Extract hostnames, routes, ARP entries, users, and software lists.
6. Test SNMP write access with a harmless read-back write, only in scope.
7. Note SNMPv3 targets for credentialed testing later.

## 1. Find SNMP services

SNMP runs over UDP, so scans are slower and less reliable than TCP scans.
Use a targeted UDP sweep on port 161 and confirm with an actual SNMP query
rather than trusting the port state alone.

```bash
# UDP sweep for SNMP across the subnet (slow, be patient)
nmap -sU -p 161 --open -T4 192.168.1.0/24 -oG /tmp/snmp-sweep.gnmap

# Faster alternative: nmap SNMP discovery scripts
nmap -sU -p 161 --script snmp-info,snmp-sysdescr 192.168.1.0/24 \
  -oN /tmp/snmp-info.txt
```

The `snmp-info` script tries the `public` community string by itself, so a
hit there already tells you the string works. Confirm manually:

```bash
# Basic query with the public community string (SNMPv2c)
snmpwalk -v2c -c public 192.168.1.10 1.3.6.1.2.1.1.1.0

# The .1.0 at the end is sysDescr: a free text device description
# Example answer: STRING: "Cisco IOS Software, C2900 Software ..."
```

If `snmpwalk` prints `Timeout: No Response`, either the community string is
wrong, the version is wrong, or SNMP is filtered. Work through each in
order.

## 2. Test community strings

Community strings are cleartext passwords. Vendors ship `public` for
read-only and `private` for read-write, and many devices keep them.

```bash
# Try the classic defaults against one target
for c in public private community manager admin default; do
  echo "=== community: $c ==="
  snmpget -v2c -c "$c" -t 2 -r 1 192.168.1.10 1.3.6.1.2.1.1.1.0 2>&1 \
    | grep -v "Timeout" | head -2
done
```

```bash
# nmap brute force script with a custom community list
nmap -sU -p 161 --script snmp-brute \
  --script-args snmp-brute.communitiesdb=/tmp/communities.txt \
  192.168.1.10
```

Keep the list short and sane: `public`, `private`, plus vendor defaults
for the gear you fingerprinted (`cisco`, `tivoli`, `Dell`, `HP`, empty
string). A good starter file:

```bash
cat > /tmp/communities.txt <<'EOF'
public
private
community
manager
admin
default
cisco
tivoli
password
snmp
EOF
```

For many targets, wrap the loop in Python with the standard library calling
`snmpget`, and stop at the first hit per host. Never spray thousands of
strings; SNMP agents on embedded devices crash under brute force, and a
crashed switch is an outage you caused.

## 3. Walk the MIB tree

Once a read community string works, walk the standard MIB-2 branches. These
OIDs exist on almost every SNMP agent and give the most value per query.

```bash
C="public"; T="192.168.1.10"

# System group: description, uptime, contact, hostname, location
snmpwalk -v2c -c $C $T 1.3.6.1.2.1.1

# Interfaces: names, addresses, speeds, status
snmpwalk -v2c -c $C $T 1.3.6.1.2.1.2 | head -60

# IP address table: every configured address on the device
snmpwalk -v2c -c $C $T 1.3.6.1.2.1.4.20

# Routing table: destinations, next hops, interfaces
snmpwalk -v2c -c $C $T 1.3.6.1.2.1.4.21
```

```bash
# ARP / neighbor table: IP to MAC mappings (great for pivoting)
snmpwalk -v2c -c $C $T 1.3.6.1.2.1.4.22

# TCP connections table: who is connected to what
snmpwalk -v2c -c $C $T 1.3.6.1.2.1.6.13

# Full walk saved for offline review (can be large)
snmpbulkwalk -v2c -c $C $T 1.3.6.1.2.1 > /tmp/mib2-walk.txt 2>&1
wc -l /tmp/mib2-walk.txt
```

Use `snmpbulkwalk` instead of `snmpwalk` for full walks: it fetches many
values per packet and finishes far faster. On Windows targets with SNMP
installed, the Host Resources MIB adds gold:

```bash
# Running processes (names and paths)
snmpwalk -v2c -c $C $T 1.3.6.1.2.1.25.4.2.1.2 | head -40

# Installed software
snmpwalk -v2c -c $C $T 1.3.6.1.2.1.25.6.3.1.2 | head -40

# Local users (when the agent exposes them)
snmpwalk -v2c -c $C $T 1.3.6.1.4.1.77.1.2.25
```

The last OID is the LAN Manager MIB user table, present on Windows SNMP
agents. It leaks usernames, which feed password spraying.

## 4. Pull the high value data

Turn the raw walk into findings. These one-liners extract what matters.

```bash
C="public"; T="192.168.1.10"

# Hostname, contact, location (often contains real names and sites)
snmpwalk -v2c -c $C $T 1.3.6.1.2.1.1.4.0 1.3.6.1.2.1.1.5.0 1.3.6.1.2.1.1.6.0

# Interface names mapped to IPs
snmpwalk -v2c -c $C $T 1.3.6.1.2.1.2.2.1.2
snmpwalk -v2c -c $C $T 1.3.6.1.2.1.4.20.1.1

# Config file names on network gear (Cisco: running config location hints)
snmpwalk -v2c -c $C $T 1.3.6.1.4.1.9.9.96.1.1.1.1.2 2>/dev/null | head -10
```

On printers, SNMP often exposes the admin password or the device web
password in vendor MIB branches. Check the vendor branch
(`1.3.6.1.4.1.<enterprise>`) when the device is a printer, UPS, or camera.
Document every credential-looking string, but verify before reporting.

## 5. Test write access carefully

A `private` or custom read-write community string allows SET operations,
which change device configuration. Test write access only when the scope
explicitly allows configuration changes, and use a harmless, reversible
write.

```bash
# Safe write test: set sysContact to a test value, read it back, restore it
ORIG=$(snmpget -v2c -c private 192.168.1.10 1.3.6.1.2.1.1.4.0 | cut -d'"' -f2)
snmpset -v2c -c private 192.168.1.10 1.3.6.1.2.1.1.4.0 s "pentest-probe"
snmpget -v2c -c private 192.168.1.10 1.3.6.1.2.1.1.4.0
snmpset -v2c -c private 192.168.1.10 1.3.6.1.2.1.1.4.0 s "$ORIG"
snmpget -v2c -c private 192.168.1.10 1.3.6.1.2.1.1.4.0
```

If the SET succeeds, you have proven write access and restored the original
value. Report it as a critical finding: writable SNMP can change routes,
reboot devices, or push configurations. Never write to routing, reboot, or
config-copy OIDs during enumeration.

## 6. Handle SNMPv3

SNMPv3 uses real authentication (username, auth password, privacy password)
instead of community strings. You cannot walk it without credentials, but
you can detect it and note it for credentialed testing.

```bash
# Detect SNMPv3: an auth failure reply still proves the service is there
snmpwalk -v3 -l noAuthNoPriv -u nosuchuser 192.168.1.10 1.3.6.1.2.1.1 2>&1 | head -3

# nmap SNMPv3 discovery
nmap -sU -p 161 --script snmp-info 192.168.1.10
```

With valid SNMPv3 credentials from another phase, walk exactly like v2c:

```bash
snmpwalk -v3 -l authPriv -u monitor -a SHA -A 'authpass' \
  -x AES -X 'privpass' 192.168.1.10 1.3.6.1.2.1.1
```

## Edge cases

- UDP scan says `open|filtered` for everything. That is normal for UDP;
  confirm with a real `snmpget` before calling a host an SNMP service.
- `Timeout: No Response` with the right string. The agent may bind SNMP
  to a management interface or VLAN only, or a firewall drops UDP 161
  from your network. Test from the approved network position.
- The device answers SNMPv1 only. Retry with `-v1`; some old printers and
  UPS units never got v2c.
- The walk returns `No Such Object` for Host Resources OIDs. The agent
  does not implement that MIB; stick to MIB-2.
- Community brute force crashes an old device. Stop immediately, note the
  outage, inform the client contact, and continue with gentler methods.
  This is why you keep the string list short.
- snmpwalk output is enormous. Walk specific branches instead of the full
  tree, and use `snmpbulkwalk` with output redirected to a file.
- Vendor MIBs need translation. Pipe numeric OIDs through `snmptranslate`
  or install the vendor MIB files for readable names.

## Escalation

- Defaults fail and the short list fails. Check the device fingerprint
  for vendor-specific defaults (printer and camera vendors are the worst
  offenders) and try one more targeted round.
- SNMP is filtered from your position. Ask whether a jump host or VPN
  segment with management access is in scope; SNMP often lives on a
  management VLAN you cannot reach directly.
- You find credentials in SNMP output. Feed them into SNMPv3 testing,
  device web interfaces, and SSH/Telnet on the same box.
- Read-write access confirmed. Document it, restore any test value, and
  hand the finding to the reporting phase; do not pivot device
  configuration further without explicit approval.
- The target is a Windows host with SNMP. Prioritize the Host Resources
  and LAN Manager branches for users, processes, and software.

## Detection and defender view

Defenders see SNMP enumeration as bursts of UDP 161 traffic from one
source, failed community string attempts in device logs, and full MIB walks
as sustained query streams. SNMP traps can alert on authentication
failures. The durable fixes: change all default community strings to long
random values, restrict SNMP to read-only where writes are not needed,
migrate to SNMPv3 with authPriv, bind SNMP to the management VLAN only,
and filter UDP 161 at the network edge. Audit devices for community
strings with a scanner on a schedule, because defaults creep back in
after firmware resets and replacements.

## Key references

- MITRE ATT&CK T1046 (Network Service Discovery): SNMP sweeps.
- MITRE ATT&CK T1590.006 (Gather Victim Network Information, Network
  Security Appliances): device config via SNMP.
- CWE-200 (Exposure of Sensitive Information): MIB data leaks.
- CWE-798 (Use of Hard-coded Credentials): default community strings.
- IETF RFC 3411-3418 (SNMPv3 architecture and security).
- Net-SNMP documentation: http://www.net-snmp.org/docs/man/
- nmap snmp NSE scripts: https://nmap.org/nsedoc/scripts/snmp-brute.html
