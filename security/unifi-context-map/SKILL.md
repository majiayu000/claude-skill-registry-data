---
name: unifi-context-map
description: >-
  Use when an agent keeps guessing wrong about a UniFi network, when starting
  recurring agent work against a gateway, or when asked to "map my network",
  "document my UniFi setup", "build a network inventory", "what's on my
  network", "why does the agent keep using the wrong AP", or "audit my
  reservations against reality". Covers writing and maintaining the site map
  file: networks, devices, SSIDs, reservations, zones, an append-only Gotchas
  list, provenance checks that keep it honest, and the security rules for a file
  that is a burglary aid if it leaks. Assumes unifi-connect. Not for making
  changes to any of it (unifi-firewall, unifi-wifi, unifi-clients).
compatibility: Any UniFi gateway reachable per unifi-connect.
---

# UniFi Context Map

This repo deliberately ships no network inventory, because the useful one is
yours. This skill is how the agent builds it.

An agent working a UniFi network without a map guesses: which AP is the one in
the back bedroom, whether `10.x.x.50` is the NAS or a decommissioned print
server, whether that camera reservation reflects where the camera actually is.
UniFi answers with MAC addresses and machine names, and it is confidently wrong
in a specific way: **the config is not the operational reality.** A reservation
exists whether or not the device honors it. A port override is stored whether or
not the hardware enforces it.

One markdown file, one human pass, fixes this.

## Read this before you write anything down

**A complete UniFi map is a burglary aid.** Not being dramatic: assembled in one
file it contains camera names and their physical placements, which cameras are on
which segment, your WAN address, the MAC address of every device in the building,
your alarm panel's IP, and which SSID is the trusted one. That is a casing
document with a network diagram attached.

So, before the first line:

- **Never commit it to a public repo.** Not "scrub it later". Git history is
  forever and the scrub is always harder than you think.
- **`.gitignore` it by name** in whatever repo you do network work from. A
  suggested pattern is in this repo's `.gitignore`.
- **Never paste it into a shared or third-party context** you do not control.
- **The API key never goes in it.** Env var, always, same as `unifi-connect`.
- If you do keep it in a repo, keep that repo private, and assume any file an
  agent reads freely is a file that can end up somewhere you did not intend.

This warning exists because the private skill this repo was distilled from could
not be published as-written. Roughly seventy percent of it was exactly the
inventory described above.

## Where to keep it

Wherever your agent reads context from and nowhere else: the private repo you do
network work from, or a local notes directory. Keep it in one place so there is
one thing to protect.

## Skeleton

Every section dated. The date is what tells a future agent how much to trust it.

```markdown
# <Site> network map (snapshot YYYY-MM-DD)

## Gateway
- Host: <UDM_HOST>, web UI https://<UDM_HOST>
- Model, UniFi OS version, Network controller version
- Auth: X-API-Key, key name "agent", stored in env var; NOT in this file
- SSH: open/closed

## Networks and VLANs (as of YYYY-MM-DD)
| Name | Purpose | VLAN | Subnet | DHCP |

## Firewall zones (as of YYYY-MM-DD)
- Zone name, id, and in one line what it is allowed to reach
- Which networks belong to it

## Devices (as of YYYY-MM-DD)
| Name | Type | Model | IP | Firmware |
- Flag which have DHCP reservations and which hold dynamic leases:
  the dynamic ones drift, so pull `devices` before targeting one

## SSIDs (as of YYYY-MM-DD)
| SSID | Band | Security | Network | Enabled |

## Reservations (as of YYYY-MM-DD, N total)
| Name | IP | MAC |

## Port forwards (as of YYYY-MM-DD)
| Name | Protocol | External port | Destination |

## Reservation vs reality
The section that earns the file. See below.

## Gotchas (append-only, dated)
- YYYY-MM-DD: <thing that cost you an hour>
```

## Building the inventory

The commands produce candidates. The human pass produces meaning.

```bash
udm networks --json | python3 -c '
import json,sys
for n in json.load(sys.stdin):
    print(n.get("name"), n.get("vlan","-"), n.get("ip_subnet"))'

udm devices --json | python3 -c '
import json,sys
for d in json.load(sys.stdin):
    print(d.get("name"), d.get("type"), d.get("model"), d.get("ip"), d.get("version"))'

udm wlans --json | python3 -c '
import json,sys
for w in json.load(sys.stdin):
    print(w.get("name"), w.get("enabled"), w.get("security"))'

udm reservations --json | python3 -c '
import json,sys
r=json.load(sys.stdin); print(len(r),"reservations")
for u in r: print(" ", u.get("name") or u.get("hostname"), u.get("fixed_ip"))'

udm zones --json | python3 -c '
import json,sys
for z in json.load(sys.stdin): print(z.get("_id"), z.get("name"))'

udm portforward --json | python3 -c '
import json,sys
for p in json.load(sys.stdin):
    print(p.get("name"), p.get("dst_port"), "->", p.get("fwd"), p.get("fwd_port"))'
```

What no query can tell you is that the AP named `U7PG2-a3f4` is the one in the
back bedroom, or that a given reservation belongs to hardware you threw out in
2023. Do that pass once, write it down, mark it verified.

## Reservation vs reality

Give this its own section. It is the highest-value thing in the file and it is
never what you expect.

A DHCP reservation applies only if the device asks that DHCP server. Devices that
join over a different SSID, sit behind an unmanaged switch, or were re-cabled at
some point get an address from wherever they actually are, and the reservation
sits dormant looking authoritative. In one real audit, of seven cameras with
reservations on a dedicated camera VLAN, exactly **one** was actually on it. The
rest had joined over Wi-Fi to an IoT SSID and held dynamic leases on a completely
different subnet. Every one of them looked correctly segmented in the reservation
table.

Check the live client list against the reservation list and record every mismatch
with the reason:

```bash
udm clients --all --json | python3 -c '
import json,sys
for c in json.load(sys.stdin):
    print(c.get("hostname") or c.get("name"), c.get("ip"), c.get("mac"), c.get("network"))'
```

Then write lines like: *"dormant reservation, device actually joins over the IoT
SSID and lives on that subnet"*, or *"permanent exception, behind an unmanaged
switch, cannot be segmented"*. That is the knowledge the API cannot give back.

## The Gotchas list

The highest-value section and the one nobody writes. Every network accumulates
local traps no vendor doc can predict. The shape:

- "The printer is behind an in-wall AP data port, so it cannot be VLAN-jailed.
  Permanent exception, do not retry."
- "The basement camera shares an unmanaged switch with another device, so both
  are stuck on the trusted network."
- "Two APs hold dynamic leases and their addresses drift. Pull `devices` before
  targeting either."
- "The guest SSID was disabled in March and was found enabled again in July.
  Check its state on every wlanconf touch."
- "That reservation belongs to hardware removed last year. Left in place
  deliberately so the address stays parked."

Append with a date, never rewrite history. **When something costs more than five
minutes, the fix is not finished until the gotcha is in the map.**

## Provenance: keeping it honest

A map that rots silently is worse than no map, because the agent trusts it. Two
rules.

**1. Date every snapshot section.**

**2. Ship a re-verify one-liner beside every volatile claim, with an expected
value.** Then any session can re-check cheaply:

```markdown
## Provenance
Last full verification: YYYY-MM-DD

- Controller version: `udm status`, expect Network <VERSION>
- Networks: `udm networks --json | python3 -c '...'`, expect N, including <VLANs>
- Devices: `udm devices --json | ...`, expect N devices
- Reservations: `udm reservations --json | python3 -c 'import json,sys;print(len(json.load(sys.stdin)))'`, expect N
- Port forwards: `udm portforward --json | ...`, expect <names>
- SSIDs: `udm wlans --json | ...`, <SSID> must show enabled=False
```

That last line is the pattern worth copying: encode the *invariant you care
about*, not just the count. "This SSID must be disabled" is a check that catches
a real regression. "There are six SSIDs" is a check that catches nothing.

If a check disagrees with the map, **trust the live output**, fix the map, re-date
the section. That loop is the entire maintenance burden: a couple of minutes,
only when a check fails.

## What not to put in it

- The API key, admin passwords, or any credential.
- Wi-Fi passphrases. The SSID list needs names and security modes, not secrets.
- Full policy or config dumps. Keep the index and the gotchas; snapshot the raw
  JSON to a separate gitignored file if you want a rollback artifact.
- Anything the agent can derive fresh more cheaply than you can maintain it. Live
  client lists change hourly; the map holds meaning, not state.
