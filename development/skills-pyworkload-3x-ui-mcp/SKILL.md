---
name: 3x-ui-panel-operations
identifier: pyworkload-3x-ui-panel-operations
description: Operate a 3x-ui (Xray/V2Ray) proxy panel through its MCP server — set up VLESS-REALITY inbounds and pick a camouflage target, diagnose why a client cannot connect, harden the panel, front a transport with a CDN, run client billing and cleanup, build and verify routing, and manage multi-node clusters. Use for any task against a 3x-ui panel, including "it stopped working", "add a user", "make it undetectable", "route this through Warp", or "add a server to the cluster".
---

# 3x-ui panel operations

Seven procedures for running a 3x-ui panel through the
[3x-ui MCP server](https://github.com/pyworkload/3x-ui-mcp), which exposes the
panel's API as 166 tools. This file routes to the right one; each carries the
operating knowledge a tool schema cannot hold — the order to do things in, and
what the panel will not warn you about.

Rules here are verified against the Xray-core and 3x-ui sources rather than
third-party guides, and quote the error text the logs actually produce.

## Pick the procedure

| Read | When the task is |
|---|---|
| [`reality-inbound/SKILL.md`](reality-inbound/SKILL.md) | Creating a VLESS-REALITY inbound, choosing or rotating a `dest`/SNI, or a REALITY inbound that stopped getting through |
| [`diagnose-connectivity/SKILL.md`](diagnose-connectivity/SKILL.md) | "It stopped working", one client or everyone cannot connect, a destination is unreachable through the proxy |
| [`panel-hardening/SKILL.md`](panel-hardening/SKILL.md) | Securing or auditing the panel, rotating credentials, scoped API tokens, fail2ban, certificate pinning, backups |
| [`cdn-fallback/SKILL.md`](cdn-fallback/SKILL.md) | Putting a transport behind Cloudflare, hiding the origin IP, or sharing port 443 between inbounds via fallbacks |
| [`client-lifecycle/SKILL.md`](client-lifecycle/SKILL.md) | Creating users, handing over subscription links, bulk renewals, usage reports, deleting dead accounts |
| [`smart-routing/SKILL.md`](smart-routing/SKILL.md) | Routing some destinations differently, geo tokens, provider outbounds (Warp/Nord/PIA), balancers, debugging a rule that does not match |
| [`multi-node/SKILL.md`](multi-node/SKILL.md) | Adding a node, TLS trust modes and mTLS, selective inbound sync, cluster monitoring |

## Things true across all of them

- **Clients are keyed by `email`**, not UUID, and one client can be attached to
  several inbounds. `update_client` overlays only the fields you pass and
  preserves the rest — never delete and recreate a client to change one field,
  because that reissues the UUID and breaks the user's app.
- **`update_inbound` and `update_outbound_sub` follow the same read-modify-write
  contract.** `set_inbound_fallbacks` does **not**: it replaces the whole list.
  From panel v3.9.0 `update_inbound` silently keeps the inbound's clients and
  `enable` flag — switch an inbound with `set_inbound_enable` and edit clients
  with the client tools.
- **Units bite.** Expiry is Unix **milliseconds** (0 = never, negative = a
  duration that starts on first use); stored `totalGB` is **bytes** despite the
  name, while tool parameters called `total_gb` take GB.
- **Routing rules are edited through the whole Xray template**, so the rule tools
  rewrite it; `update_xray_template` replaces it outright.
- **A balancer override lives in the running core only** and is forgotten on
  restart.
- **"Subscription" means two different things**: outbound subscriptions pull
  remote outbound lists *into* this panel, while `get_subscription_links` returns
  what this panel *serves to* its own users.
- **Every tool is annotated** with its effect. The ones marked destructive delete
  data, zero counters, or drop live connections — several are panel-wide with no
  undo, so enumerate what you are about to remove and show it first.

## Panel versions

Baseline is 3x-ui **v3.3.0+**. REALITY scanning needs **v3.4.2**, node, token and
host-group tools **v3.5.0**, and geodata plus several maintenance calls **v3.7.0**.
Below those the panel answers 404; the server's README carries the full table.
