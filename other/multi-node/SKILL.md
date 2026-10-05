---
name: multi-node
description: Attach, secure and operate additional 3x-ui panels as nodes of a master panel — probe before saving, choose a TLS trust mode (verify/skip/pin/mTLS), select which inbounds sync, and monitor health and per-node traffic. Use when asked to add a server to a cluster, set up mTLS between panels, work out which node is serving whom, or update the panels on every node.
---

# Multi-node

A node is another 3x-ui panel this one drives: inbounds and clients are pushed to
it, and its traffic and online state are pulled back. Most of these calls reach the
node itself over the network, not just the local panel, so failures here are as
often connectivity as configuration.

Node tools need panel **v3.5.0+**; `reload_node_mtls_client` needs **v3.7.0+**.

## Adding a node, in the right order

1. **Probe before saving.** `test_node` takes the same connection parameters as
   `add_node` and reports whether they work, without writing anything:

```
test_node address="node1.example" port=2053 scheme="https" api_token="…" tls_verify_mode="verify"
```

2. **Save it.** `add_node` probes again as part of the write and refuses
   parameters it cannot reach, so a successful call means the link works.
3. **See what it offers.** `list_node_inbounds id=<id>` lists the inbounds that
   exist on the node — the input for selective sync.
4. **Choose the sync mode.** `inbound_sync_mode="all"` pushes everything;
   `"selected"` with `inbound_tags=[…]` pushes only the named tags. Selective sync
   is the right default for a mixed cluster, where one node is not meant to carry
   every customer.

`allow_private_address` must be set for a node on a private or loopback address —
otherwise the probe rejects it as unroutable, which is the intended protection
against pointing a node at yourself by accident.

## TLS trust modes

`tls_verify_mode` decides what the master accepts from the node:

| Mode | Meaning | When |
|---|---|---|
| `verify` | Standard chain validation | The node has a real certificate for a real domain |
| `skip` | No validation at all | Never, outside a lab — it removes the only defence against interception |
| `pin` | The certificate must match a recorded fingerprint | Self-signed certificates, which is most private clusters |
| `mtls` | Both sides present certificates | The strongest option, and the one to grow into |

For `pin`, read the fingerprint from the node and store it in the node's
`pinned_cert_sha256` (base64 SHA-256 of the leaf certificate):

```
get_node_cert_fingerprint id=<id>
update_node id=<id> tls_verify_mode="pin" pinned_cert_sha256="<that value>"
```

`get_remote_cert_hash server="node1.example:2053"` gets the same value from the
outside, which is the honest way to check the two agree before pinning. Re-pin
after every certificate renewal — a renewed certificate has a new fingerprint and
the node goes unreachable the moment the old one is replaced.

A node that is not reachable directly can be dialled through the cluster: set
`outbound_tag` and the master reaches it through that Xray outbound instead of
straight out.

## mTLS

Two panels, two calls, in this order:

1. On the **master**: `get_node_mtls_ca` — the node-auth CA, minted on first call.
2. On the **node's** panel: `set_node_mtls_trust_ca ca_cert="<that CA>"` — this is
   the panel acting as a node, declaring which CA it trusts.
3. Back on the master, set the node's `tls_verify_mode="mtls"`.

After rotating a client certificate, `reload_node_mtls_client` applies it without a
panel restart. That is the difference between a rotation and an outage.

## The API token is write-only

From **v3.6.0** the panel reports only `hasApiToken`, never the value. Two
consequences:

- `update_node` sends `apiToken` **only when you supply one**; its absence means
  "keep the stored token". Updating a node's port does not silently wipe its
  credentials.
- `clear_api_token=true` is the explicit way to drop it — for a node that has moved
  to mTLS and no longer needs a token. It is mutually exclusive with `api_token`;
  passing both is a contradiction the panel rejects.

If a token is lost, it cannot be read back from either side. Mint a new one on the
node and set it with `update_node`.

## Operating the cluster

```
list_nodes                    # health, counts, last heartbeat
probe_node id=<id>            # re-check one now and refresh cached health
get_node_history id=<id> metric="cpu" bucket=360
```

`list_nodes` is the daily view; a node whose heartbeat has stopped is still serving
whatever configuration it last received, which is why a stale node looks fine to
its users right up until something changes.

`get_node_history` takes a bucket in **seconds** and always returns 60 samples, so
the bucket also chooses the window: 360 gives six hours. Valid values are 2, 30,
60, 180, 360, 720, 1440, 2880 and 10080.

Per-node client views: `get_online_clients_by_node`, `get_client_ips_by_node`, and
`get_active_inbounds` for the inbound tags that actually carried traffic.
`get_node_descendants` shows the nodes below this panel when the cluster is more
than one level deep.

`set_node_enable id=<id> enable=false` pauses sync without deleting anything — the
right move for maintenance on a node, since re-enabling resumes where it left off.

## Destructive edges

`delete_node` removes the node and **does not migrate its inbounds**. Clients
served there lose their route; move them first or accept the outage knowingly.

`update_node_panels ids=[…]` runs the 3x-ui self-updater on those nodes. They
restart, traffic on them drops, and a node that fails to come back needs hands on
it. Update one node first, confirm it returns in `list_nodes`, and only then do the
rest. Take a backup (`backup_to_telegram`) before starting.
