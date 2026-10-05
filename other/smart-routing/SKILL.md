---
name: smart-routing
description: Build and verify Xray routing on a 3x-ui panel — split traffic by domain or geo token, send some destinations through Warp/NordVPN/PIA, block what should not leave, and confirm each rule with the router before trusting it. Use when asked to route certain sites differently, bypass the proxy for local traffic, block ads or torrents, add a VPN provider outbound, or debug a rule that is not matching.
---

# Routing

Routing rules live in the saved Xray template, and every rule tool
(`add_routing_rule`, `update_routing_rule`, `remove_routing_rule`) rewrites that
whole template read-modify-write. Two consequences: back up before a session of
edits, and do not interleave rule edits with `update_xray_template`, which replaces
the document outright and will discard rules added in between.

## Before anything else

**Sniffing must be enabled on the inbound.** Without it the router sees only IP
addresses and every `domain` rule misses — silently, with no error anywhere. The
default `sniffing` this server sends on `create_inbound` has it on; an inbound
created elsewhere may not. Check `get_inbound` first when domain rules "do nothing".

## Rule order is the whole game

```
get_routing_rules
```

Rules are evaluated top to bottom and the first match wins. The classic failure is
a broad rule above a narrow one — `geosite:category-ads` above a specific
`domain:ads.example.com` exception means the exception never runs.
`add_routing_rule` appends by default; pass `index` to place a rule where it will
actually be reached.

`get_routing_rules` also returns the balancer definitions, because a rule's
`balancerTag` is meaningless without them.

## Validate geo tokens before saving

`geosite:` and `geoip:` tokens that do not exist do not error — they just never
match:

```
validate_geodata_tokens tokens="geosite:category-ads-all,geoip:private" kind="domain"
```

`list_geodata_files`, `list_geodata_categories` and `list_geodata_entries` browse
what the server's databases actually contain, which is the reliable way to find the
right category name rather than guessing from a blog post. `update_geofile`
refreshes the databases; stale geo data is a common cause of rules that used to
work.

## Common shapes

Direct for local traffic, so it never leaves through the proxy:

```
add_routing_rule rule={"type":"field","outboundTag":"direct","ip":["geoip:private"]} index=0
```

Block a category:

```
add_routing_rule rule={"type":"field","outboundTag":"blocked","domain":["geosite:category-ads-all"]}
add_routing_rule rule={"type":"field","outboundTag":"blocked","protocol":["bittorrent"]}
```

Send a set of domains through a provider outbound:

```
add_routing_rule rule={"type":"field","outboundTag":"warp","domain":["geosite:openai","domain:example.com"]}
```

Rules can also match `inboundTag`, `port`, `network` and the client's `user`, which
is how one inbound gets different routing per customer.

## Provider outbounds

Warp, NordVPN and PIA each have a read tool and a write tool, so inspecting is
annotated differently from erasing:

```
get_warp_data action="data"        # account state; "config" returns the WireGuard config
manage_warp action="reg"           # register; then changeIp / license / interval / del
```

NordVPN and PIA follow the same shape (`get_nordvpn_data`, `manage_nordvpn`,
`get_pia_data`, `manage_pia`) and take a token or credentials. All of these reach a
third party, not the panel — `manage_*` with `action="del"` erases stored
credentials and cannot be undone from here.

Once registered, the provider appears as an outbound: `get_outbounds` shows its
tag, and that tag is what a routing rule targets.

## Verify with the router, not by trying it

```
test_route domain="www.example.com" port=443 network="tcp" email="alice"
```

The running core answers with what it *would* do — `matched` (false means no rule
applied and the default outbound was used), `outboundTag`, and `groupTags` for the
balancer chain the decision passed through. No traffic is sent. Test the rule you
just added and one destination that must **not** be affected; a rule that is too
broad is invisible until someone complains.

`test_route` needs panel **v3.3.1+**.

Then confirm the chosen outbound is actually alive — `test_outbound` for one,
`test_outbounds` for all, `get_xray_observatory` for the latency and health history
the core has been recording.

## Balancers

`get_balancers` merges two sources: the definitions saved in the template (`tag`,
`selector`, `fallbackTag`, `strategy`) and the live state from the running core
(`running`, `override`, `selected`). When the core cannot be reached you get the
definitions plus a `live_status_error` — that is a core problem, not a balancer
problem.

`set_balancer_override` pins a balancer to one outbound, or releases it back to its
strategy. **The override lives in the running core only and is forgotten on
restart** — it is an incident tool ("pin off the flapping exit until morning"), not
a configuration change. Anything that must survive a restart belongs in the
template.

Balancer status and override need panel **v3.3.1+**.

## After changing rules

Rule changes take effect through the template; if the core will not load the new
document, every client drops. Check `get_xray_logs` after a batch of edits, and
remember `get_xray_config` reports the *running* core while `get_xray_template`
reports what was *saved* — a difference between them means the core rejected the
save.
