---
name: reality-inbound
description: Stand up (or repair) a VLESS-REALITY inbound on a 3x-ui panel the way the Xray community recommends — choose and verify a camouflage target, generate keys, write streamSettings, attach a client, hand back a working link. Use when asked for a new REALITY inbound, a "stealth" VLESS setup, a better dest/SNI, or when an existing REALITY inbound has stopped getting through.
---

# REALITY inbound

REALITY hides the server by completing a real TLS 1.3 handshake with a third-party
site (`dest`) and stealing its certificate for anyone who is not a genuine client.
There is no domain to register and no certificate to renew — but the whole design
rests on picking a good `dest`, and that choice is not something the panel checks
for you.

## Choosing the target

Four properties are mandatory, and `scan_reality_target` verifies all of them:
TLS 1.3, HTTP/2 in ALPN, X25519 key exchange, and a certificate that chains to a
trusted root. A candidate failing any one of them cannot be used at all.

The rest is judgment the scanner cannot make:

1. **Not fronted by a CDN with nodes in your users' country.** Two separate
   problems: your server becomes a port-forwarder into that CDN for anyone who
   probes it, and a censor sees traffic leaving to a foreign IP for a domain that
   resolves locally — an anomaly that stands out precisely because the domain is
   popular.
2. **Not one of the giants.** `google.com`, `microsoft.com`, `apple.com` and
   friends are the most-analysed SNIs on earth and are usually CDN'd locally.
   Xray-core agrees loudly enough to have hard-coded it: a `serverNames` entry
   containing `apple` or `icloud` logs *"REALITY: Choosing apple, icloud, etc. as
   the target may get your IP blocked by the GFW"* at startup.
3. **Reachable and not itself blocked** where the users are. A blocked SNI is
   worse than no camouflage.
4. **Low RTT from the panel server**, not from you. Every client handshake is
   proxied to `dest`, so its latency is added to connection setup.
   `scan_reality_targets` ranks candidates by feasibility first, then latency.
5. **Plausibly close to the VPS.** A site in the same datacenter or AS as the
   server is both fast and unremarkable.

The trick worth knowing: `scan_reality_targets` accepts CIDR ranges and discovers
candidates by reading the certificates hosts actually serve. Scanning the
neighbourhood of your own VPS finds local, low-latency, unpopular targets that no
published "good dest" list contains — and published lists are exactly the ones a
censor also reads.

```
scan_reality_targets targets="203.0.113.0/24,www.some-vendor.example,cdn.other.example"
```

Then confirm the winner on its own and read the SAN list:

```
scan_reality_target target="www.some-vendor.example"
```

`serverNames` must be names that certificate actually covers. Take them from the
scan's SAN DNS names; if the SAN is a wildcard, use a concrete hostname under it,
not the wildcard itself.

Both scan tools need panel **v3.4.2+**. On an older panel they answer 404 — pick
the target by hand against the same criteria and skip to the next step.

## Building the inbound

1. **Keys** — `generate_key type="x25519"`. The `privateKey` goes in the inbound;
   the `publicKey` is what clients need, so keep it, the panel will not show it
   again in the inbound settings.
2. **shortIds** — hex, even length, at most 16 characters (the core decodes each
   into 8 bytes). The **array itself must not be empty** — Xray refuses to start
   with `empty "shortIds"` — but an empty string `""` inside it is legal and admits
   clients that send no shortId. Use one non-empty value per audience if you want
   to tell them apart later.
3. **Create it** — `dest` is `host:port` (443 unless the target says otherwise);
   `serverNames` are the SNIs clients will send.

```
create_inbound
  remark="reality-de"
  port=443
  protocol="vless"
  settings={"clients":[],"decryption":"none","fallbacks":[]}
  stream_settings={"network":"tcp","security":"reality","realitySettings":{
      "dest":"www.some-vendor.example:443",
      "serverNames":["www.some-vendor.example"],
      "privateKey":"<from generate_key>",
      "shortIds":["0123abcd"]}}
```

Leave the default `sniffing` in place — domain-based routing rules match on
nothing without it.

4. **Client** — `add_client inbound_ids=[<id>] email="alice" flow="xtls-rprx-vision"`.
   Vision is what makes REALITY-over-TCP fast, and it is valid **only** on
   TCP-based VLESS. Never set it on a ws/grpc/xhttp client; the connection will
   fail in a way that looks like a server problem.
5. **Hand it over** — `get_all_inbound_links` for the raw URLs, or
   `get_subscription_links sub_id=…` for a subscription the user's app can refresh.

## When an existing REALITY inbound stops working

The target is the first suspect: sites lose HTTP/2, move behind a CDN, or start
serving a certificate that no longer covers the `serverNames` in use. Re-run
`scan_reality_target` against the current `dest` before touching anything else.
If it now fails, pick a new target and change `dest` and `serverNames` together —
they must stay consistent. Existing clients keep working; only the camouflage
changes.

If the target still scans clean, the inbound is probably fine and the problem is
elsewhere — hand off to the `diagnose-connectivity` skill.

## Traps

| Trap | What happens |
|---|---|
| `serverNames` not in the target's certificate | Handshake fails for every client |
| `dest` behind Cloudflare or a local CDN | Server acts as a port-forward; traffic pattern stands out |
| `flow: xtls-rprx-vision` on ws/grpc/xhttp | Client cannot connect; looks like a server fault |
| Odd-length, non-hex, or empty `shortIds` array | Xray refuses to start — check `get_xray_logs` |
| `decryption` omitted from VLESS settings | Inbound is rejected: *please add/set "decryption":"none" to every settings* |
| Copying a "good dest" from a popular list | The same list is public to everyone, censors included |
