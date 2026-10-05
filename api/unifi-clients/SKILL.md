---
name: unifi-clients
description: >-
  Use when operating on UniFi clients, devices, switch ports, or DHCP: "block a
  device", "kick a client off wifi", "restart an access point", "power cycle a
  PoE port", "move a device to a different VLAN", "my device is on the wrong
  subnet after I changed the port", "set a DHCP reservation", "change DHCP DNS
  servers", "forget an old client", "why did my PUT reset all the other ports",
  or reading UniFi events and alarms. Covers full-object PUT discipline, the
  wired VLAN migration trap, and where events moved. Assumes unifi-connect. Not
  for firewall policy between zones (unifi-firewall), radios and SSIDs
  (unifi-wifi).
compatibility: >-
  UniFi Network with adopted devices. Verified on UniFi OS 5.1.19 / Network
  10.4.57. Port and DHCP object shapes are version-sensitive.
---

# UniFi Clients and Devices

Day-to-day operations, and the two ways they go wrong: **partial writes that
silently destroy config**, and **VLAN changes that appear to work and do not.**

## Full-object PUT discipline

The rule that prevents most damage on this API:

> `rest/*` endpoints replace the object. GET it, modify the one field, PUT the
> whole thing back.

A partial PUT does not merge. It writes what you sent and drops the rest. The
consequences scale with the object:

- `rest/networkconf`: PUT `{"dhcpd_dns_1": "..."}` and you can lose the network's
  DHCP range, domain name, and VLAN assignment.
- `rest/wlanconf`: you can lose the passphrase, the network binding, the band
  settings.
- `rest/device` `port_overrides`: **PUT the complete `port_overrides` list.**
  Sending one port's override resets every other port on the switch to defaults.
  On a 24-port switch carrying a segmented network, that is the whole afternoon.

```bash
# Correct shape, every time
udm raw GET /proxy/network/api/s/default/rest/networkconf/<NETWORK_ID> > /tmp/net.json
# edit /tmp/net.json, changing only what you mean to change
udm raw PUT /proxy/network/api/s/default/rest/networkconf/<NETWORK_ID> "$(cat /tmp/net.json)"
```

Then re-read and diff. The PUT response is not proof.

## The wired VLAN migration trap

You change a switch port's native VLAN. The controller accepts it. The device
behind that port is now **stranded**, and nothing tells you.

**Changing `native_networkconf_id` in `port_overrides` does not bounce the link.**
The device never sees a carrier drop, so it never re-runs DHCP. It keeps its
old-subnet lease, sits on a segment where that address has no gateway, and looks
completely healthy until it needs to route somewhere. Then it fails in a way that
looks like a firewall problem, which is where the afternoon goes.

Completing the move requires the device to issue a fresh DHCP **DISCOVER**, which
means a real reboot. Lease expiry technically works and is useless: 24 hours.

**PoE devices: force it cleanly over the API.**

```bash
# Confirm the port actually draws power first
udm devices --json | python3 -c '
import json,sys
for d in json.load(sys.stdin):
    for p in d.get("port_table") or []:
        if float(p.get("poe_power") or 0) > 0:
            print(d.get("name"), p.get("port_idx"), p.get("poe_power"))'

udm devices power-cycle <SWITCH_MAC> <PORT_IDX>
```

`poe_power` is a **string** (`"0.00"`, `"6.42"`), not a number, so a truthiness
test passes on an unpowered port. Cast it. The field is only present on switch
(`usw`) port tables; APs and the gateway do not have it.

Full reboot, fresh DISCOVER, device lands on the new VLAN. Verify by reading its
new address, not by assuming.

**Self-powered devices cannot be force-renewed remotely.** A link bounce makes
them re-REQUEST their *old* lease (INIT-REBOOT), and when the new VLAN's DHCP
server stays silent, they keep the stale address. There is no API path around
this. The only reliable sequence:

1. Flip the port to the target VLAN
2. Physically power-cycle the device, unplug about ten seconds, replug

Zero-stranding variant, better if you are already standing there: unplug first,
flip the port while it is off, replug. The device boots straight onto the new
VLAN and is never stranded at all.

**`forward: 'disabled'` is a no-op for disabling a port.** Verified on UniFi OS
5.1.19 / Network 10.4.57: the controller accepts it, and the port stays UP. Do
not build a "disable the port to force a renegotiation" plan on it.

**Cosmetic, not a failure:** after a non-default native assignment the controller
normalizes `forward` from `'all'` to `'customize'` in the read-back. The port
still passes native-VLAN traffic. Do not chase this.

**Plan the order.** If a batch contains both PoE and self-powered devices, do the
PoE ones over the API and leave the self-powered ones for when you can physically
reach them. Do not flip a self-powered device's port and walk away: leaving a
security device, camera, or alarm component stranded offline is worse than not
having started. Revert the port if the physical trip is not happening today.

## Client operations

```bash
udm clients                       # currently connected
udm clients --all                 # including offline, the full known list
udm clients block <MAC>
udm clients unblock <MAC>
udm clients kick <MAC>            # force reassociation
```

`kick` is the gentle diagnostic: it makes a client re-associate, which re-runs
band steering and AP selection. Useful when a device is stuck on a distant AP.

**Forgetting stale clients.** The known-client list accumulates forever. Old
reservations for decommissioned hardware, VM interfaces, replaced phones:

```bash
udm raw POST /proxy/network/api/s/default/cmd/stamgr \
  '{"cmd":"forget-sta","macs":["<MAC>"]}'
```

Worth a periodic sweep. A reservation table full of dead entries is where a stale
DHCP reservation quietly hands a live device the wrong address, and it makes the
inventory in `unifi-context-map` much harder to keep honest.

**Reservations are not reality.** A fixed-IP reservation only applies if the
device asks that DHCP server. A camera with a reservation on the camera VLAN that
actually joins over Wi-Fi to the IoT SSID gets an IoT address, and the reservation
sits dormant looking authoritative. Always confirm from the live client list where
a device actually is, not from the reservation table.

```bash
udm reservations --json | python3 -c '
import json,sys
for u in json.load(sys.stdin):
    print(u.get("name") or u.get("hostname"), u.get("fixed_ip"), u.get("mac"))'
```

**And "active" is not reality either.** A wired client listed by `stat/sta` means
the switch port has link and the controller has an ARP entry for it. That is layer
2. It is not a statement that the host is up, and the controller will keep
reporting a dead server as an active client indefinitely.

Seen on a NAS that was halfway through a reboot: it appeared in `udm clients` with
its correct IP and a healthy-looking uptime, ARP resolved from another machine on
the LAN, and every single TCP port was closed. Diagnosing "the controller says it
is online" as "the box is fine" wasted the first ten minutes.

The tell is in the traffic counters, because a live host is never at a flat zero:

```bash
udm clients --json | python3 -c '
import json,sys
for c in json.load(sys.stdin):
    if c.get("is_wired") and not (c.get("wired-tx_bytes-r") or c.get("wired-rx_bytes-r")):
        print("no traffic:", c.get("name") or c.get("hostname"), c.get("ip"))'
```

Anything that shows up there is a candidate, not a verdict: an idle printer looks
identical. Confirm from off the controller entirely: probe a port the host should
be answering on. The controller can tell you a cable is plugged in. It cannot tell
you a service is running, and it will not say so.

## Device operations

```bash
udm devices                          # all adopted devices
udm devices restart <MAC>
udm devices provision <MAC>          # force-provision, push config
udm devices power-cycle <MAC> <PORT> # PoE port on a switch
```

`provision` is the right first move when a device's operational state disagrees
with its config. It is also how you confirm a setting genuinely is not applying:
if two force-provisions do not change operational behavior, the hardware does not
support what you are asking. That is how the in-wall AP port limitation in
`unifi-wifi` was established.

## DHCP DNS

Set on the network object, so full-object PUT applies:

```bash
udm raw GET /proxy/network/api/s/default/rest/networkconf/<NETWORK_ID>
# fields: dhcpd_dns_1, dhcpd_dns_2, dhcpd_dns_3
```

Practical notes: **make all your LAN networks agree** unless you have a specific
reason not to, or a device's filtering depends on which VLAN it happens to be on.
If you run a filtering resolver, give clients a second one on different hardware,
because a DNS resolver on a single box is a single point of failure for the entire
network's usability. Pointing the last entry at the gateway gives you an
unfiltered last resort, which is either a safety net or a filtering bypass
depending on what the resolver is for. Choose deliberately.

Clients keep their old DNS servers until their lease renews. Changing this and
testing immediately from an already-connected machine tests nothing.

## Events and alarms

**Legacy `stat/event` 404s on Network 10.4.** Events moved to v2, and it is a POST
with a pagination body:

```bash
udm events              # POST /v2/api/site/default/system-log/all
udm events --pages 5    # page back further
```

```bash
udm alarms                        # unresolved
udm alarms archive <ALARM_ID>
udm alarms archive-all
```

Alarms are worth reading before any change session: an existing alarm about an
adoption failure or a switch uplink explains symptoms you would otherwise blame
on your own change.
