---
name: unifi-wifi
description: >-
  Use when UniFi Wi-Fi is slow, unstable, or being tuned: "my wifi is slow but
  speedtest on the router is fast", "great signal, terrible speed", "should I
  use 80MHz or 40MHz", "channel planning", "co-channel interference", "DFS
  channels", "my APs keep picking the same channel", "audit my SSIDs", "hidden
  SSID", or diagnosing throughput that collapses under load. Also roaming: "my
  phone stays stuck on the far AP", "sticky clients", "improve roaming", "should
  I enable fast roaming", "minimum RSSI", "TX power tuning". Covers the
  diagnostic ladder for slow Wi-Fi, channel width and DFS tradeoffs, safe radio
  writes, cell sizing and roaming persuasion, SSID hygiene, and the in-wall AP
  port trap. Assumes unifi-connect.
  Not for firewall policy between networks (unifi-firewall), wired port and
  client operations (unifi-clients).
compatibility: >-
  UniFi Network with adopted UniFi APs. Channel and DFS specifics below are US
  regulatory domain. Verified on Network 10.4.57 with AC and WiFi 6 hardware.
---

# UniFi Wi-Fi

Most "slow Wi-Fi" is not slow Wi-Fi. It is a WAN problem, a backhaul problem, a
client problem, or a bandwidth cap somebody set two years ago. The diagnostic
ladder below exists to find that out cheaply, in that order, before touching
radios. Radio changes are the most disruptive and the most often wrong.

## The diagnostic ladder

Run it top to bottom. Each rung eliminates a layer, and the failure that motivated
this skill was only visible at the last rung.

**1. Rule out the WAN.** Trigger a gateway-side speedtest, which measures the
gateway to the internet with no Wi-Fi involved:

```bash
udm raw POST /proxy/network/api/s/default/cmd/devmgr '{"cmd":"speedtest"}'
# wait, then read the RESULT from stat/device, not stat/health
udm devices --json | python3 -c '
import json,sys
for d in json.load(sys.stdin):
    s = d.get("speedtest-status")
    if s: print(d.get("name"), s.get("xput_download"), s.get("xput_upload"),
                "status_summary=", s.get("status_summary"))'
```

The result lands on the **gateway's** device object, under the hyphenated key
`speedtest-status` (not `speedtest_status`), with throughput in the nested
`xput_download` and `xput_upload` fields. `status_summary` tells you whether the
run finished; a fresh gateway that has never run one reports zeros. `stat/health`
is a different number entirely and will send you in circles.

**2. Check the AP's uplink.** An AP on a 100 Mbps link, or meshed rather than
wired, caps every client behind it:

```bash
udm devices --json | python3 -c '
import json,sys
for d in json.load(sys.stdin):
    up = d.get("uplink") or {}
    print(d.get("name"), d.get("type"), up.get("speed"), up.get("type"))'
```

**3. Check the client's own view.** Signal, negotiated rate, satisfaction:

```bash
udm clients --json | python3 -c '
import json,sys
for c in json.load(sys.stdin):
    print(c.get("hostname"), c.get("signal"), c.get("tx_rate"), c.get("satisfaction"))'
```

This rung is where the interesting case appears. A client at **-57 dBm with an
866 Mbps PHY rate** has an excellent link. If it measures 32 Mbps, the radio is
fine and something is contending. Signal is not throughput, and confusing the
two is why people replace working access points.

**4. Rule out a bandwidth cap.** Somebody, possibly you, may have set one:

```bash
udm raw GET /proxy/network/api/s/default/rest/usergroup
udm wlans --json    # check per-SSID rate limits
```

**5. Compare every AP's channel, width, and channel utilization.** The last rung,
and the one that finds co-channel contention:

```bash
udm devices --json | python3 -c '
import json,sys
for d in json.load(sys.stdin):
    for r in d.get("radio_table_stats") or []:
        print(d.get("name"), r.get("radio"), "ch", r.get("channel"),
              "bw", r.get("bw"), "cu_total", r.get("cu_total"),
              "sat", r.get("satisfaction"))'
```

Field names matter here and are not the obvious ones. Channel width is **`bw`**,
not `channel_width`. The names are per object, not global: on a *client* record
the same value really is `channel_width`. Check the object you are reading rather
than carrying a field name across from another endpoint. `cu_total` is **channel utilization**, the percentage of
airtime in use, and it is the closest thing to a direct measurement of the
problem this skill is about. `cu_self_tx` and `cu_self_rx` break out how much of
that is this AP's own traffic: **high `cu_total` with low `cu_self_*` means
somebody else is using your airtime**, which is either a neighbor or, more often,
your own AP two rooms away on the same channel.

`satisfaction` reports `-1` when a radio has no clients on it. That is "no data",
not "terrible".

Read `radio_table_stats`, the operational state, not `radio_table`, the config.
They disagree more often than you would like.

## The 80 MHz trap

The failure that motivated this skill, because it is a change that looks free.

Setting every 5 GHz radio to 80 MHz doubles the theoretical per-client rate, so
it reads like a pure upgrade. It is not, because **width is bought with
channels.** In the US regulatory domain, 80 MHz with DFS channels disabled leaves
exactly **two** non-overlapping blocks:

- UNII-1: channels 36 / 40 / 44 / 48
- UNII-3: channels 149 / 153 / 157 / 161

Two blocks. If you have more than two 5 GHz APs with overlapping coverage, some
of them are sharing an 80 MHz block and taking turns transmitting. Wi-Fi degrades
gracefully in signal terms and catastrophically in contention terms: everything
looks healthy right up until two clients are busy simultaneously.

The observed case: four APs, three of them in-wall units on adjacent walls, all
piled into UNII-1 after a global switch to 80 MHz. Result was roughly **32 Mbps
on a gigabit connection**, with an 866 Mbps PHY link at -57 dBm and a confirmed
1276 Mbps gateway speedtest. Neither ISP, backhaul, nor signal was the cap.

**Do not disable DFS channels when auditing a channel plan.** It is the change
that creates the pileup. DFS is the difference between two usable 80 MHz blocks
and six.

### Pick a block, not a channel

At 80 MHz a radio occupies its whole block, so two APs on *different* channels in
the *same* block are fully co-channel with each other. This is the mistake to
avoid when spreading APs out: moving an AP from 48 to 104 accomplishes nothing if
another AP already sits on 100.

US 80 MHz blocks:

| Block | Channels | DFS? |
|---|---|---|
| UNII-1 | 36, 40, 44, 48 | no |
| | 52, 56, 60, 64 | yes |
| | 100, 104, 108, 112 | yes |
| | 116, 120, 124, 128 | yes, and see below |
| | 132, 136, 140, 144 | yes |
| UNII-3 | 149, 153, 157, 161 | no |

Map what you have to blocks before choosing a target, because the channel numbers
hide the collision:

```bash
udm devices --json | python3 -c '
import json,sys
B=([36,40,44,48],[52,56,60,64],[100,104,108,112],[116,120,124,128],[132,136,140,144],[149,153,157,161])
blk=lambda c: next(("%d-%d"%(b[0],b[-1]) for b in B if c in b), "?")
for d in json.load(sys.stdin):
    for s in d.get("radio_table_stats") or []:
        if s.get("radio")=="na" and s.get("channel"):
            print(d.get("name"), "ch", s.get("channel"), "-> block", blk(s["channel"]))'
```

**Prefer 52-64, 100-112, and 132-144 when you need free blocks.** The 116-128
block overlaps terminal doppler weather radar (TDWR, 5600-5650 MHz) in the US,
where a CAC can run ten minutes instead of one, and the channels are sometimes
unavailable outright. An 80 MHz block anchored at 116 spans 116/120/124/128 =
5570-5650 MHz, so it swallows the whole TDWR sub-band: at 80 MHz you cannot
sit near 116 without sitting *in* it.

### If an AP keeps falling off a DFS channel, stop restarting it

An AP assigned a DFS channel can run there for a week or two, hit a radar
detection (real or false), quietly move to a non-DFS channel, and **keep reporting
the assigned channel in its config the whole time**. Nothing alarms, nothing logs
it, and `rest/device` echoes back whatever you last wrote. One deployment sat like
this for **twelve days**: config said 116, the radio was on 149, stacked on top of
two APs already sharing the 149-161 block, at 33% and 30% channel utilization
while every other AP sat at 1-2%. Every check had read the config.

Restarting puts it back and buys another week or two, which is treating the
symptom. If a radio keeps getting pushed off the same block, the block is wrong
for that site. **Retire it and take an extra co-channel share instead.** Moving
that AP to a non-DFS block took it from 33% to 7% utilization and its neighbour
from 21% to 12%. A share you chose beats a channel the AP cannot hold, so pair
whichever APs are furthest apart physically: different floors beats different
rooms.

**Audit live-vs-config, not either one alone,** on a schedule rather than only
after a write. A radio that drifts once will drift again.

```bash
udm devices --json | python3 -c '
import json,sys
for d in json.load(sys.stdin):
    cfg={r["radio"]:r for r in d.get("radio_table") or []}
    for s in d.get("radio_table_stats") or []:
        c=cfg.get(s["radio"],{}).get("channel")
        if s.get("channel") and str(c)!=str(s["channel"]) and c!="auto":
            print("DRIFT", d.get("name"), s["radio"], "cfg", c, "live", s["channel"])'
```

The tradeoff is real and worth stating honestly: DFS channels require radar
detection, cost a ~50-60 second silent scan when a radio moves onto one, and some
older or cheap client devices will not associate on them at all. Weigh that
against four APs sharing one block. In a dense deployment, **40 MHz on
non-overlapping channels beats 80 MHz on shared ones**, every time.

## Changing a radio channel safely

**Read and write are different endpoints.** This one costs people an hour:

```
GET  /proxy/network/api/s/default/stat/device/<MAC>       # the object
PUT  /proxy/network/api/s/default/rest/device/<DEVICE_ID> # the write
```

`GET rest/device` **returns an empty list** on Network 10.4.57, with or without a
device id appended, exactly like `rest/firewallrule` in `unifi-firewall`. It is
not broken and your key is fine: reads live on `stat/device`. An agent that GETs
`rest/device`, sees `[]`, and concludes the controller has no devices is on the
wrong endpoint.

The write body that works is the radio table alone, sent complete:

```bash
# GET the device, edit ONLY the target field inside radio_table,
# then PUT the WHOLE radio_table array back:
udm raw PUT /proxy/network/api/s/default/rest/device/<DEVICE_ID> \
  '{"radio_table": [ <every radio, every field, one value changed> ]}'
```

Verified on Network 10.4.57: this preserves the radio you did not touch. You do
not need to send the entire device object back, and you should not, because
`stat/device` hands you a pile of read-only operational fields along with the
config.

**Send the full `radio_table` array.** A partial write drops the fields you
omitted, including transmit power and width on the other radio.

**`channel` may read `auto` in config while `radio_table_stats` shows a real
number.** Those are both correct: the AP is auto-selecting and has landed
somewhere. Writing a concrete channel silently opts that radio out of automatic
selection, which is usually what you want for a deliberate plan, but it is a
second change riding along with the first. Know you are making it.

**Moving onto a DFS channel triggers a CAC (channel availability check)** and the
radio goes silent for it. Two moves observed on Network 10.4.57 took roughly **45
and 105 seconds**, so budget more than a minute and do not conclude the write
failed at the 60-second mark. Clients drop and reconnect once. Do it when nobody
is on a call.

**The two directions are not equally hard.** Moving *off* a DFS channel onto a
non-DFS one is easy: one observed move settled about **75 seconds** after a
force-provision, no restart, clients reassociating on their own. Moving *onto* a
DFS channel is where it sticks, and a force-provision can leave the radio on its
old channel indefinitely; an AP restart (`cmd/devmgr` `restart`, ~2.5 minutes
offline) is what finally lands it after CAC. If a *non*-DFS move needs a restart,
something else is wrong. Go look rather than power-cycling.

**Verify from `radio_table_stats`, never the PUT echo**, and read `state` rather
than just `channel`:

| `state` | Meaning |
|---|---|
| `RUN` | on air and serving |
| `DFS_WAIT` | mid-CAC, silent, this is the normal DFS transition |
| `INIT` | not on air |

A radio still reporting the old channel with `state: RUN` has not moved yet. One
in `DFS_WAIT` is moving and needs more time.

```bash
udm devices --json | python3 -c '
import json,sys
for d in json.load(sys.stdin):
    for s in d.get("radio_table_stats") or []:
        print(d.get("name"), s.get("radio"), s.get("channel"),
              s.get("state"), "clients", s.get("num_sta"))'
```

## Roaming

**Nothing here makes a client roam.** The client decides, every time, using logic
its vendor did not document and you cannot change. Every setting below either
changes what the client sees or takes the current AP away from it. Read that again
before spending an evening on thresholds: this is lobbying, not commanding.

A sticky client is usually not a roaming problem. It is a cell-size problem. An AP
loud enough to be heard comfortably three rooms away gives a client that walks
that far a perfectly good signal and no reason to move. Fix coverage overlap
first. The persuasion knobs compensate for a cell plan, they do not replace one.

### What the controller exposes, and where

Two different objects, which is the first thing that trips people up.

Per SSID, in `rest/wlanconf`:

| Field | What it is |
|---|---|
| `fast_roaming_enabled` | 802.11r fast transition |
| `wpa3_fast_roaming` | the WPA3 equivalent, tracked separately |
| `bss_transition` | 802.11v, lets the AP *suggest* a better AP |
| `roaming_assistant_na_enabled` / `roaming_assistant_na_rssi` | disconnect a 5 GHz client below a threshold |
| `roaming_assistant_6e_enabled` | same for 6 GHz |
| `minrate_na_enabled` / `minrate_na_data_rate_kbps` | minimum 5 GHz data rate |
| `minrate_ng_enabled` / `minrate_ng_data_rate_kbps` | minimum 2.4 GHz data rate |

Per radio, in each device's `radio_table`:

| Field | What it is |
|---|---|
| `min_rssi_enabled` / `min_rssi` | signed dBm floor, e.g. `-75` |
| `tx_power_mode` | `low`, `medium`, `high`, `auto`, `disabled` |
| `tx_power` | integer dBm |
| `min_txpower` / `max_txpower` | hardware bounds for this radio |

Every field name above was read off a live controller on Network 10.4.57.
**There is no 802.11k neighbor-report toggle in either object on this version.**
If a guide tells you to enable 11k in UniFi, confirm it is not describing a
different controller generation.

### Order of operations

Work down. Each step is cheaper to undo than the one after it.

**1. Size the cells with transmit power.** The most effective fix and the least
clever one. In a dense deployment, turning power *down* improves roaming: a
smaller cell means the client runs out of signal while a better AP is already well
within range.

**Set every AP covering the same area to the same mode.** One AP left on `auto`
among manual neighbors resizes its own cell on its own schedule while everything
around it holds still, so the overlap you designed drifts without you touching
anything.

```bash
udm devices --json | python3 -c '
import json,sys
for d in json.load(sys.stdin):
    for r in d.get("radio_table") or []:
        print(d.get("name"), r.get("radio"), r.get("tx_power_mode"),
              r.get("tx_power"), "range", r.get("min_txpower"), r.get("max_txpower"))'
```

Two things observed on real mixed hardware:

- **`min_txpower` and `max_txpower` differ per radio and per model.** Ranges of
  `6..22`, `6..26`, and `4..20` were seen across three AP models on one network. A
  single dBm value applied network-wide is not portable, and a value outside a
  radio's range is not a setting.
- **`tx_power` does not track `tx_power_mode`.** Radios reporting mode `low` were
  observed carrying `tx_power` values of both `6` and `20`. When the mode is a
  named preset, read `tx_power` as a leftover, not as effective radiated power.

**2. Raise the minimum data rate.** `minrate_na_enabled` plus
`minrate_na_data_rate_kbps` sets a floor. Slow frames from a distant client consume
airtime far out of proportion to the data they carry, and a client that cannot meet
the floor has to go find an AP where it can. Gentler than a disconnect, and it
attacks the contention problem from earlier in this skill at the same time.

**3. Enable 802.11r and 802.11v.** `fast_roaming_enabled` shortens the
reassociation handshake; `bss_transition` lets the AP nominate a neighbor. Neither
forces anything, and 11v suggestions are routinely ignored. 802.11r has a long
history of breaking older clients, so turn it on for one SSID and watch what stops
connecting rather than flipping it everywhere at once.

**4. Only then consider a minimum RSSI.** Read the next section first.

### The min RSSI trap

**Minimum RSSI is not a handoff. It is a disconnect.** The AP stops answering a
client below the floor, and what happens next is entirely the client's choice.
That includes immediately reassociating to the same AP, which is a disconnect loop
wearing a roam costume.

Two thresholds exist and they are not the same knob: `min_rssi` is per radio in
`radio_table`, `roaming_assistant_na_rssi` is per SSID in `wlanconf`. Both can be
active simultaneously. **Which one wins when they disagree is not established
here**, because settling it means writing to a live network and watching clients
drop. Read both before changing either.

**`min_rssi` and `min_rssi_enabled` are independent, so read the flag, not the
number.** A radio will happily report `min_rssi: -79` with `min_rssi_enabled:
False`, and that threshold is doing nothing. Observed on Network 10.4.57 with the
flag `True` on every 5 GHz radio and `False` on every 2.4 GHz radio of the same
APs. Auditing the values alone tells you a story that is half wrong.

Before changing a floor, find out who it will evict. A tighter number is only
free if nobody is living in the gap:

```bash
udm clients --json | python3 -c '
import json,sys
for c in json.load(sys.stdin):
    s=c.get("signal") or 0
    if c.get("radio")=="na" and s and s <= -75: print(c.get("hostname"), s)'
```

Set it too aggressive and you have built a coverage hole out of software. A client
evicted at `-70` that sees nothing better than `-72` has nowhere to go, and the
symptom is not poor roaming, it is a device that will not stay on the network at
all. Anything tighter than roughly `-75` needs a specific reason.

**Keep the floor consistent across APs covering the same space.** Values drifting
between `-70` and `-79` on one network is the pathological case: the AP with the
tightest floor evicts clients that every neighbor around it is perfectly happy to
serve.

### Checking whether any of it worked

The controller will not tell you. Client records carry **`roam_count`**, and
comparing it across a few days is a far better signal than reading it once:

```bash
udm clients --json | python3 -c '
import json,sys
for c in json.load(sys.stdin):
    print(c.get("hostname"), c.get("ap_mac"), c.get("signal"),
          c.get("tx_rate"), "roams", c.get("roam_count"))'
```

Run it, walk the building, run it again. `ap_mac` changing is a roam. `signal`
improving after it changed is a *good* roam. A `roam_count` that climbs while the
device sits still is thrash, and usually means a threshold is too tight.

**Check `fixed_ap_enabled` and `fixed_ap_mac` before diagnosing anything.** A
client pinned to a specific AP will not roam no matter what you tune, and the
setting is easy to apply once and forget:

```bash
udm clients --json | python3 -c '
import json,sys
for c in json.load(sys.stdin):
    if c.get("fixed_ap_enabled"):
        print("PINNED", c.get("hostname"), c.get("fixed_ap_mac"))'
```

### Applying the change

`wlanconf` and `radio_table` are both full-object PUTs, so the discipline from
`unifi-connect` applies unchanged: GET the whole object, change one field, PUT the
whole thing back, re-read to confirm. Roaming work is the easiest place in this API
to lose a passphrase or an entire transmit-power plan to a partial write.

Whether a given roaming change needs a force-provision to take effect was not
established here. If a setting reads back correctly but behaves as though it never
applied, `udm devices provision <MAC>` is the next thing to try.

## SSID hygiene

```bash
udm wlans --json | python3 -c '
import json,sys
for w in json.load(sys.stdin):
    print(w.get("name"), w.get("enabled"), w.get("security"), w.get("networkconf_id"))'
```

- **Re-read `enabled` on every `wlanconf` touch.** An SSID that was deliberately
  disabled can come back: a controller update, a config restore, or somebody in
  the UI. Deliberate disables do not always stay disabled, so make checking the
  state part of the routine rather than assuming your last change held.
- **Never leave an open SSID on the trusted network.** If a device genuinely
  cannot do WPA2, and some old handhelds and IoT gear cannot, rebuild that SSID
  on the guest or IoT network where an open join reaches nothing. An open SSID
  bridged to the trusted LAN is an unauthenticated port on your network with a
  radius of about 40 metres.
- **Hidden SSIDs are not security.** They are broadcast in probe requests by every
  client configured for them. They mainly make life harder for you.
- Confirm each SSID's `networkconf_id` maps to the network you think it does.
  This is how a device ends up on the trusted VLAN despite a careful segmentation
  plan: it joined the SSID that was still pointed at the old network.

## The in-wall AP port trap

Filed here because it is AP hardware behavior, though it bites during wired
segmentation.

**AC-series in-wall APs do not enforce native-VLAN overrides on their pass-through
data ports.** Set a port override on the AP, and the controller accepts it and
echoes `native_networkconf_id` back in `port_table` as though it applied. The
operational `forward` value stays `all`, and untagged traffic from the device
behind that port keeps bridging onto the AP's own network.

Verified with two force-provisions and a `forward:'native'` variant. The device
behind the port stayed reachable on the old subnet throughout, which is the tell:
the config says isolated, the network says otherwise.

**Devices behind in-wall AP data ports cannot be VLAN-jailed.** Not a
configuration problem, so do not burn an afternoon on payload variants. Re-cable
to a real switch port, or accept it and document the exception. Once you know
this, it takes ten seconds to check whether a stubborn device is behind one.

## A disabled radio may not be disabled

Same hardware family, same shape of lie, and this one has an ongoing cost.

Two In-Wall HD APs on Network 10.4.57, both with a 2.4 GHz radio configured off
and parked on channel 11 at 20 MHz. What they were actually doing:

| | config (`radio_table`) | operational (`radio_table_stats`) |
|---|---|---|
| channel | 11 | **1** |
| width | `ht` 20 | `bw` **40** |
| power | `tx_power_mode: disabled` | `state: RUN`, `cu_self_tx` 5-6% |
| clients | | **0** |

Every configured value ignored, and `cu_self_tx` of 5 to 6 percent means each one
was spending real airtime beaconing to nobody, on the channel where a third AP was
serving every 2.4 GHz device in the building.

**`num_sta: 0` does not mean a radio is idle.** A radio with no clients still
beacons, and at 40 MHz from channel 1 it covers most of the band. Judge a radio by
`state` and `cu_self_tx`, never by client count.

Things that did **not** fix it, so you can skip them:

- **Force-provision, twice.** The stored config was not applied either time.
- **`"enabled": false` on the radio entry.** The PUT returns `rc: ok` and the
  controller silently strips the field: it does not survive a read-back and it is
  not part of the `radio_table` schema. A clean illustration of why `rc: ok` is
  not evidence, and why a round-trip read is.

An AC In-Wall on the same site, with the same `tx_power_mode: disabled`, sits at
`state: INIT` with no channel and zero utilization, which is what genuinely off
looks like. Whether that radio is disabled or simply failed to initialize is not
distinguishable from the API, so treat it as a clue rather than a conclusion.

**If you need a radio truly off on this hardware, do it in the UI and then diff.**
GET the device's `radio_table`, toggle the radio in the web interface, GET again,
and compare. That tells you the field the controller actually writes. Do not
invent one: the guess above looked entirely plausible and was silently discarded.
