---
name: cdn-fallback
description: Put a 3x-ui inbound behind a CDN (WebSocket, gRPC or xhttp through Cloudflare) or share port 443 between several inbounds using Xray fallbacks. Use when REALITY is blocked or unsuitable, when the server IP must stay hidden behind a CDN, when a real domain and certificate are in play, or when several protocols need to live on one port.
---

# CDN transports and fallbacks

Two different jobs that are often confused:

- **CDN fronting** hides the server's IP behind Cloudflare (or another CDN) and
  makes the traffic look like ordinary HTTPS to a real website. It needs a domain,
  a certificate, and a transport the CDN can proxy: WebSocket, gRPC or xhttp.
- **Fallbacks** let one TLS inbound on 443 hand connections to other inbounds by
  path or ALPN, so a web server and several proxy protocols share the port.

They combine well — a CDN-fronted WS inbound as the fallback child of a master
inbound on 443 — but decide which problem you are solving first.

## CDN fronting

REALITY cannot be CDN-fronted: it impersonates someone else's TLS, and the CDN
terminates TLS itself. Fronting means a real certificate for a domain you control.

**Pick the transport.** WebSocket is the most widely supported and the safest
default. gRPC multiplexes better on a busy link but needs gRPC enabled on the CDN
side. xhttp is the modern option and the most flexible over HTTP/2, but is the
most sensitive to CDN buffering — try it after WS works, not before.

**Ports the CDN will proxy matter.** Cloudflare proxies HTTPS only on 443, 2053,
2083, 2087, 2096 and 8443. An inbound on any other port must be grey-clouded,
which defeats the purpose. Set the inbound's port to one of those, or terminate on
443 and fall back internally.

**Create it** — the transport carries no TLS of its own when the CDN terminates in
front of it and the origin is plain HTTP; give it TLS when the origin must also be
encrypted (Cloudflare "Full" mode).

```
create_inbound
  remark="ws-cdn"
  port=2053
  protocol="vless"
  settings={"clients":[],"decryption":"none"}
  stream_settings={"network":"ws","security":"none","wsSettings":{"path":"/vlws","host":""}}
```

Then `add_client inbound_ids=[<id>] email="alice"` — and **no `flow`**.
`xtls-rprx-vision` is valid only on TCP-based VLESS; setting it on a ws/grpc/xhttp
client produces a connection failure that looks like a broken server.

The path is a shared secret of sorts: an unguessable one keeps casual scanners from
finding the endpoint behind an otherwise ordinary site.

**Host groups publish it.** The client link must carry the CDN hostname, not the
server's address. `add_host_group` over the inbound sets the external address, port
and SNI the panel renders into subscription links; `get_inbound_hosts` shows what
is attached today. Without this the links point at the origin and bypass the CDN.

## Fallbacks

A master inbound (VLESS or Trojan, TCP + TLS) on 443 accepts the TLS handshake and
routes onward by path or ALPN to child inbounds listening on localhost.

```
get_inbound_fallbacks id=<master id>
set_inbound_fallbacks id=<master id> fallbacks=[
  {"childId":11,"path":"/vlws","xver":2},
  {"childId":12,"alpn":"h2"}
]
```

Two things about `set_inbound_fallbacks`, both easy to get wrong:

1. **It replaces the entire list.** It is not read-modify-write like
   `update_inbound`. Read the current list, add your entry to it, and send the
   whole set back. Passing `[]` removes every fallback.
2. **It restarts Xray.** Every live connection drops. Do it in a maintenance
   window, not while debugging someone's outage.

Children should listen on `127.0.0.1` so nothing reaches them except through the
master. `xver: 2` forwards the real client address over PROXY protocol — without
it, every connection appears to come from localhost and per-client IP limits,
fail2ban and the IP log all become useless. Only `0`, `1` and `2` are accepted;
anything else stops the core with *"invalid PROXY protocol version"*.

`path`, when set, must begin with `/` — the core rejects the config otherwise.

Two things the panel handles that you might otherwise do by hand: it stores the
list per master and swaps it atomically, and it rewrites the **child's client
links** to advertise the master's address, port and TLS instead of the child's
loopback listen. Links for a fallback child are therefore correct as generated —
do not hand-edit them.

Fallbacks are compatible with `"decryption":"none"`, which is the normal VLESS
setting. They cannot be combined with VLESS *encryption* (the `vless_enc` material
from `generate_key`): the core refuses with *"fallbacks can not be used together
with decryption"*. Pick one or the other for a given inbound.

The default fallback (an entry with neither `path` nor `alpn`) catches everything
unmatched; point it at a real web server so a probe sees a website rather than a
protocol error.

## Verifying

`get_inbound id=<id>` confirms what was saved. `get_all_inbound_links` shows the
URLs clients will actually receive — check the host and port in them match the CDN,
which is where host-group mistakes surface. `get_xray_logs` catches a core that
refused the new configuration; a fallback pointing at a non-existent `childId` is
the usual cause.

If connections work directly but not through the CDN, the CDN is buffering or not
proxying that port — go back to the port list, and try WS before blaming the
transport.

## Traps

| Trap | What happens |
|---|---|
| `flow: xtls-rprx-vision` on a ws/grpc/xhttp client | Client cannot connect |
| Inbound port outside the CDN's proxied set | CDN refuses to proxy; only grey-cloud works |
| `set_inbound_fallbacks` with only the new entry | Every other fallback is silently removed |
| Fallback without `xver: 2` | All clients appear as 127.0.0.1; IP limits and bans break |
| Links published without a host group | Users connect to the origin IP, bypassing the CDN |
| REALITY behind a CDN | Cannot work — the CDN terminates TLS |
