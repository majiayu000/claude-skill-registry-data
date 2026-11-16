---
name: bittorrent-client-from-scratch
description: "Use when building a BitTorrent client or any peer-to-peer file-sharing protocol from first principles — not when integrating an existing torrent library. Triggers on: 'build a torrent client', 'implement bittorrent protocol', 'peer wire protocol', 'bencode parser', 'write a torrent tracker client', 'piece selection algorithm'. Covers bencode encoding, tracker HTTP/UDP protocol, the peer wire protocol, and piece-selection strategy."
origin: yana-ai — synthesized from public BitTorrent protocol specification (BEP 3, BEP 15, BEP 5) and community from-scratch tutorials indexed in codecrafters-io/build-your-own-x
license: Apache-2.0
version: 1.0.0
compatibility: yana-ai >= 0.43.2
---

# /bittorrent-client-from-scratch

## When to Use

- Building a minimal BitTorrent client (download-only or full peer) to understand the protocol, not to ship a production downloader.
- Implementing bencode (BitTorrent's serialization format) for a `.torrent` file parser.
- Writing tracker communication (HTTP/UDP announce) or a bare peer-wire-protocol handshake.
- Teaching or learning piece-selection strategy (rarest-first), choke/unchoke algorithms.

## Do NOT use for

- Production file transfer — use an existing library (libtorrent, aria2, WebTorrent) instead of hand-rolling protocol code for a real product.
- General P2P networking unrelated to BitTorrent's specific wire format (see `wamp-pubsub-patterns` or `raft-consensus-patterns` for other distributed patterns).
- DHT-only (trackerless) discovery as a first implementation — build the tracker-based path first (see Step 4), DHT is a documented extension, not the starting point.

---

## Protocol Layers (build in this order)

```
1. Bencode        — the serialization format everything else is written in
2. .torrent file  — bencoded dict describing the download (info hash, piece hashes, tracker URL)
3. Tracker         — HTTP/UDP request that returns a peer list
4. Peer wire       — TCP protocol between two peers: handshake, message framing, piece exchange
5. Piece manager    — tracks which pieces you have/need, drives requests
6. (Optional) DHT  — trackerless peer discovery, BEP 5 — add only after 1-5 work
```

## Step 1: Bencode

Four types only — no schema needed, all self-describing:

```
Integer:      i<number>e              → i42e = 42
Byte string:  <length>:<bytes>        → 4:spam = "spam"
List:         l<items>e               → l4:spami42ee = ["spam", 42]
Dictionary:   d<key><value>...e       → d3:cow3:mooe = {"cow": "moo"}, keys sorted by raw byte order
```

Write both `decode(bytes) -> value` and `encode(value) -> bytes` — you need `encode` to re-derive the info hash (see Step 2) and to build tracker announce requests.

## Step 2: Parse the .torrent File

A `.torrent` file is a bencoded dict with keys: `announce` (tracker URL), `info` (dict containing `name`, `piece length`, `pieces` — a concatenated string of 20-byte SHA-1 hashes, one per piece, `length` for single-file or `files` for multi-file torrents).

The **info hash** — the torrent's unique identifier everywhere in the protocol — is `SHA1(bencode(info_dict))`, computed over the *raw bencoded bytes* of just the `info` value, not a re-serialization from a parsed struct (re-encoding can silently reorder or reformat and produce the wrong hash — keep the raw byte range from the original decode).

## Step 3: Talk to the Tracker

HTTP GET to the `announce` URL with query params: `info_hash` (20 raw bytes, URL-encoded), `peer_id` (your 20-byte client ID), `port`, `uploaded`, `downloaded`, `left`, `compact=1`. Response is a bencoded dict with `interval` (seconds until re-announce) and `peers` — with `compact=1`, a byte string where every 6 bytes is one peer (4 bytes IP + 2 bytes port, big-endian).

UDP tracker protocol (BEP 15) exists for trackers that don't support HTTP — it's a separate connect/announce handshake, implement it only if a tracker in practice requires it.

## Step 4: Peer Wire Protocol

Handshake (fixed 68 bytes): `\x13BitTorrent protocol` + 8 reserved bytes + 20-byte info hash + 20-byte peer ID. Both sides send this first; a peer that returns a different info hash is not serving your torrent — drop the connection.

After the handshake, all messages are length-prefixed (4-byte big-endian length, then 1-byte message ID, then payload). Core message IDs:

```
0  choke            5  bitfield   (which pieces this peer has)
1  unchoke          6  request    (index, begin, length)
2  interested       7  piece      (index, begin, block data)
3  not interested    8  cancel
4  have (piece idx)
```

State machine per connection: you start `choked` + `not interested`. Send `interested`. Wait for the peer to `unchoke` you — only then can you `request` blocks. A zero-length message (just the 4-byte length field, no ID) is a keep-alive.

## Step 5: Piece Manager

- Track piece state as a bitfield (have / don't have / in-flight).
- Split each piece into blocks (commonly 16KB) — `request` messages are per-block, not per-piece.
- **Rarest-first**: track which peers have which pieces; request pieces that fewest peers have first — this keeps piece availability balanced across the swarm and avoids everyone racing for the same common piece.
- On receiving a full piece, verify its SHA-1 against the hash from the `.torrent` file's `pieces` field before writing to disk or announcing `have` — a mismatched hash means a corrupt/malicious peer, discard and re-request from someone else.

## What NOT to Do

- Don't reorder or reformat the `info` dict before hashing it — you'll compute the wrong info hash and every tracker/peer will reject you.
- Don't request whole pieces in one message — the wire protocol requests blocks (~16KB); requesting a multi-MB piece in one `request` message is invalid per spec and most peers will drop you.
- Don't skip piece-hash verification "to save time" — an unverified piece can poison the rest of the download since later pieces may depend on file layout assumptions from earlier ones.
- Don't build DHT before the tracker path works end-to-end — DHT is a strictly harder distributed-hash-table problem layered on top of a protocol you should already understand.
