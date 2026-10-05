---
name: unifi-firewall
description: >-
  Use when working on UniFi firewall rules, zones, or network segmentation:
  "my firewall rules are empty", "rest/firewallrule returns nothing", "isolate
  my IoT devices", "block cameras from the internet", "create a firewall zone",
  "VLAN isolation", "zone-based firewall", "my IoT devices lost DNS after I
  segmented them", or auditing what a zone actually permits. Covers the
  zone-based firewall model, where policies live, the block-by-default trap on
  new zones, and lockout safety. Assumes unifi-connect. Not for assigning
  devices to VLANs or switch ports (unifi-clients), Wi-Fi and SSID-to-network
  mapping (unifi-wifi).
compatibility: >-
  UniFi Network 9.x and later, where the zone-based firewall replaced classic
  rule groups. Verified on Network 10.4.57. On older controllers the legacy
  rest/firewallrule model still applies and this skill does not.
---

# UniFi Firewall

Modern UniFi Network replaced the old LAN-IN / LAN-LOCAL / WAN-IN rule groups
with a **zone-based firewall**. Every network belongs to a zone, and policies
govern traffic between zone pairs rather than between interfaces. This is a
better model and a worse migration, because the old API endpoint still exists and
still answers.

## Why your firewall rules look empty

```bash
udm raw GET /proxy/network/api/s/default/rest/firewallrule
# []
```

An empty array. The endpoint is alive, authenticated, and lying by omission: on a
zone-based controller your rules are not there. They are here:

```bash
udm policies    # GET /proxy/network/v2/api/site/default/firewall-policies
udm zones       # GET /proxy/network/v2/api/site/default/firewall/zone
```

An agent that reads `rest/firewallrule`, sees `[]`, and concludes the network is
unfirewalled will confidently propose rebuilding rules that already exist. If a
gateway reports zero firewall rules and it is clearly not wide open, you are on
the wrong endpoint.

**The zone endpoint is singular.** `/firewall/zone` works, `/firewall/zones`
404s. There is no reason for this; just remember it.

## The trap: new zones default to BLOCK against Internal

The single most expensive thing to learn the hard way.

**Creating a new custom zone auto-generates default policies, and the
Internal↔zone pair defaults to BLOCK in both directions.** External and Gateway
pairs default to allow, and custom→External allows, so the new zone reaches the
internet fine. What it loses, instantly and completely, is the trusted LAN: DNS
resolvers, the media server, the home-automation hub, the NAS.

The failure mode is nasty because it is partial. Devices still have internet.
They still associate, still pull DHCP, still look healthy in the controller.
They just cannot resolve names against your internal resolver, so everything
degrades ten seconds later in a way that reads like a DNS outage.

**Stage the allow policies before you create the zone.** Have the payloads
written and ready to POST, create the zone, then immediately POST the allows.
Do not create a zone at the end of a session, and do not create one for a segment
containing anything you or your household will notice going down.

If you are already in the hole: the zone exists, its devices are cut off, and the
fix is POSTing allow policies to `firewall-policies` for the Internal→zone and
zone→Internal directions.

## A worked segmentation: IoT and cameras

The common goal. Two custom zones, each with a deliberately small hole punched
back into the trusted network.

**IoT zone.** Cheap devices with vendor cloud dependencies. They need the
internet, they need the gateway, and they need a very short list of internal
services:

- zone → External: allow (they phone home, that is what they do)
- zone → Gateway: allow (DHCP, DNS to the gateway itself)
- zone → Internal: **allow only specific destination+port pairs**
  - DNS, tcp/udp 53, to your internal resolvers
  - your media server's port, to that host only
  - your automation hub's UI port and MQTT broker port, to that host only
- zone → Internal: block everything else, explicitly, as the last rule
- Internal → zone: allow all (you want to reach them; they should not reach you)

**Camera zone.** Cameras are the segment most worth isolating and the easiest,
because a locally-recorded camera needs almost nothing:

- zone → Gateway: allow
- zone → External: **block**, with an explicit named policy. This is the whole
  point. A camera that cannot reach the internet cannot be recruited into a
  botnet, cannot phone a vendor cloud, and still records perfectly to a local NVR.
- Internal → zone: allow all

Order matters within a zone pair, same as any firewall. Put the narrow allows
above the broad block.

If you also run per-device rules (a smart TV blocked from ad domains, a bedtime
schedule on a game console) note that rules written against the Internal zone do
**not** follow a device when you move it to a custom zone. Mirror them into the
new zone, or the schedule you set up last year quietly stops applying.

## Writing policies

```bash
# List, and find the one you mean
udm policies --json | python3 -c '
import json,sys
for p in json.load(sys.stdin):
    print(p["_id"], p.get("action"), p.get("name"))'

# Create
udm policies create '{...}'

# Update: GET the policy, modify, PUT the whole object back
udm policies update <POLICY_ID> '{...full object...}'

udm policies delete <POLICY_ID>
```

Build a payload by reading an existing policy of the same shape and editing it.
The schema is undocumented and version-specific; a policy the controller wrote
itself is the most reliable template you will find.

**v2 PUTs may return HTTP 201 instead of 200. That is success.** Do not retry.

**Verify from a fresh GET, never from the PUT response.** Re-read the policy list
and confirm the rule is present, enabled, in the position you expect, and in the
zone pair you expect.

## Lockout safety

You are configuring the device your management traffic flows through. A firewall
mistake here does not throw an error, it removes your ability to fix the error.

- **Know your out-of-band path before the first write.** Physical console access,
  a directly-cabled port, the recovery procedure for your model. If your answer
  is "I'd just SSH in", check that SSH is even enabled: on many UniFi OS gateways
  port 22 is closed by default.
- **Never apply a default-deny to the zone holding your workstation.** Obvious
  until the moment you are auditing zones and one of them is quietly the one you
  are sitting in.
- **Write allow policies before restrictive ones**, not after. The window between
  "zone created" and "allows applied" is a live outage.
- **One change, one verification.** Batching six policy writes and then testing
  means the failure is in one of six places, and you may not be able to reach the
  controller to find out which.
- **Snapshot first.** `udm policies --json > policies-$(date +%F).json` costs
  nothing and is the difference between a rollback and an archaeology project.
- Prefer **scheduled maintenance windows for segmentation work**, for the same
  reason you would on any other network: the recovery involves walking to the
  device.
