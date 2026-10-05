---
name: diagnose-connectivity
description: Work out why a 3x-ui client cannot connect, in the order that finds the cause fastest — scope the outage, check the core, the inbound, the client's own limits, routing and outbounds, then the node. Use whenever someone reports "it stopped working", a client cannot connect, a site is unreachable through the proxy, or traffic works for some users and not others.
---

# Diagnosing a connection failure

Work from the cheapest, most common cause outward. Most reports resolve in the
first two steps, and every step below is a read-only call.

## Step 0 — scope it

Ask, or determine from the panel, which of these it is:

- **Everyone, everywhere** → the core or the box (step 1)
- **Everyone on one inbound** → the inbound (step 2)
- **One client** → that client's limits (step 3)
- **Everyone, but only for one destination** → routing or an outbound (step 4)

`get_online_clients` answers this immediately: a normal-looking list means the
core is up and serving, so skip straight to step 3.

## Step 1 — the core and the box

```
server_status
get_xray_logs count=100
```

The single most common panel-wide outage is a template that Xray refuses to load:
the panel saves it happily, the core then fails to start, and every client drops.
`get_xray_logs` names the offending field. Confirm by comparing what is running
with what is saved — `get_xray_config` reports the running core, `get_xray_template`
the saved document; if the config call fails while the template reads fine, the
core is down.

Fix the template and `restart_xray`. If the panel itself is unreachable, nothing
here will answer at all — that is a host or firewall problem, not a config one.

## Step 2 — the inbound

```
get_inbound id=<id>
```

Check, in this order: `enable` is true; `port` is what clients are actually
dialling and nothing else took it; `expiryTime` (Unix **milliseconds**, 0 = never)
has not passed; `total` (bytes, inbound-wide quota) is not exhausted. A disabled
or expired inbound looks exactly like a network failure from the client side.

For a REALITY inbound whose settings are unchanged but which stopped getting
through, the camouflage target is the suspect — see the `reality-inbound` skill.

## Step 3 — the client

```
get_client email="alice"
get_client_traffic email="alice"
get_last_online
```

Five things disable a client that is otherwise correctly configured:

| Field / tool | Failure |
|---|---|
| `enable: false` | Disabled by hand or by a bulk operation |
| `expiryTime` in the past | Expired. Milliseconds, not seconds — a value that looks absurdly small is a seconds value written by mistake |
| `totalGB` reached | Quota spent. The field is **bytes** despite the name |
| `limitIp` exceeded | Too many simultaneous IPs; further connections are refused and the IP may get banned |
| HWID slots full | `list_client_devices` — a new device is rejected when every slot is taken |

`get_last_online` distinguishes "never connected since we changed something"
(configuration or credentials) from "was connected until an hour ago" (limit,
expiry, or a network event).

### Flow mismatches, read straight off the log

When the client is enabled and within every limit but still cannot connect,
`get_xray_logs` usually names the cause verbatim. These four come from the VLESS
inbound and each has exactly one meaning:

| Log line | Cause |
|---|---|
| `XTLS only supports TLS and REALITY directly for now.` | `xtls-rprx-vision` on a ws/grpc/xhttp inbound. Vision is TCP+TLS/REALITY only — clear the client's `flow` |
| `account … is rejected since the client flow is empty` | The server expects Vision but the client's link has no `flow`. Reissue the link with `flow=xtls-rprx-vision` |
| `xtls-rprx-vision doesn't support UDP` | UDP over a Vision client; expected, not a fault to fix on the server |
| `failed to use xtls-rprx-vision, found outer tls version …` | The outer TLS is not 1.3 |

If `limitIp` is the cause, `get_client_ips` shows what the panel counted and
`clear_client_ips` resets it. Check `get_fail2ban_status` too: where fail2ban is
active, exceeding the IP limit bans the address, so the client stays broken after
the limit itself is fixed. Where it is absent, the opposite confusion applies —
the limit is recorded but never enforced, so `limitIp` cannot be the explanation
at all and something else is going on.

The IP-limit job reads the core's online-stats API on current cores and falls back
to parsing the Xray access log on older ones. On an older core with the access log
disabled it has nothing to read, so IP limits and bans silently do nothing.

## Step 4 — routing and outbounds

When connection succeeds but a destination does not load, ask the router what it
would do. No traffic is sent:

```
test_route domain="www.example.com" port=443 network="tcp" email="alice"
```

`matched: false` means no rule applied and the default outbound was used.
A wrong `outboundTag` points at the rule list — `get_routing_rules` shows the
rules in evaluation order, and order is the usual culprit: a broad rule above a
narrow one swallows it.

Then check the outbound actually works: `test_outbound` for one, `test_outbounds`
for all, `get_xray_observatory` for the latency and health the core has been
recording. A balancer that has pinned itself to a dead outbound shows up in
`get_balancers`; `set_balancer_override` releases it, but the override is
runtime-only and is forgotten on restart.

If routing depends on `geosite:`/`geoip:` tokens, a stale or partial geo database
makes rules silently miss — `validate_geodata_tokens` reports tokens that do not
resolve, and `update_geofile` refreshes the data.

Domain rules also need sniffing enabled on the inbound. Without it the router only
ever sees IP addresses, and every domain rule misses.

## Step 5 — the node

On a multi-node panel, confirm the client is being served where you think:

```
list_nodes
get_online_clients_by_node
```

`list_nodes` carries health and last heartbeat; a node that stopped heartbeating
serves stale config. `probe_node id=<id>` re-checks it now. `get_client_ips_by_node`
shows which node actually saw the user.

## Step 6 — blocked rather than broken

If the panel is healthy, the client's limits are clean, and the link works from
another network but not from the user's, the problem is upstream filtering rather
than configuration. For REALITY, re-scan the current `dest` (`scan_reality_target`)
and consider rotating it. For CDN-fronted transports, see `cdn-fallback`.

## Do not, while diagnosing

`reset_all_traffics`, `reset_all_client_traffics`, `delete_depleted_clients` and
`delete_orphan_clients` are panel-wide and destructive. They are cleanup tools, not
diagnostic ones, and running one to "reset things" destroys the evidence and the
accounting along with it.
