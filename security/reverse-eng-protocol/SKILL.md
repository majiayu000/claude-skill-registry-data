---
name: reverse-eng-protocol
description: >
  Reverse a custom network protocol from captured traffic or the client binary: recover the
  frame layout, message-type dictionary, field meanings, and state machine. Load for custom
  TCP/UDP binary protocols, Protobuf/gRPC without reflection, FlatBuffers/MessagePack,
  WebSocket/MQTT/private RPC framing, PCAP-driven format recovery, length-prefixed or TLV
  frames, magic bytes, CRC/checksum fields, or encrypted frame headers.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: medium
cwe: [CWE-319]
tools: [tshark, wireshark, python3, blackboxprotobuf, kaitai-struct, imhex]
schema_version: 1
---

# Custom protocol reverse engineering

## When it applies
The target speaks something that isn't plain HTTP/JSON: a custom binary TCP/UDP protocol,
Protobuf/gRPC with no reflection, FlatBuffers/MessagePack, WebSocket or MQTT frames, or a
private RPC format — and you have a PCAP, a proxy export, client logs, or the client binary.
(For pure HTTP parameter signing in JS, use `reverse-eng-js`; for gRPC's HTTP/2 attack surface
itself, `api-grpc`.) Target and any replay testing must be in `scope.txt`
(`tradecraft-scope-roe`) — replay only against systems you're authorized to touch.

## Why it works
Protocols are machines, and machines are regular: fixed headers, magic bytes, length fields,
monotonic sequence numbers, and repeated type-length-value structures. Align many samples of
the same message type and the invariant bytes identify themselves; the variable ones are your
fields. Serialization formats like Protobuf are self-describing enough to decode blind — field
numbers and wire types survive even without the `.proto`.

## Method
1. **Capture and triage.** Pull raw payloads and label each sample by direction (C→S / S→C);
   note handshake, heartbeat, and reconnect patterns:
   ```bash
   tshark -r cap.pcap -Y "tcp.port==4433" -T fields -e frame.number -e ip.src -e tcp.payload | head
   ```
   First questions: fixed header? magic bytes? a length field? TLV or fixed-size records? Any
   compression (zlib/gzip/lz4) or per-frame encryption (AES/ChaCha)?
2. **Recover the frame layout.** Align several messages of the same kind and diff the bytes:
   invariant regions = header/constants; counters = sequence numbers; a field whose value
   matches the remaining byte count = length (check endianness, and whether it includes the
   header). Locate integrity fields last — CRC16/32, checksums, HMAC slots. Sketch the state
   machine (`Connect → Auth → Ready → Request/Response → Close`). Encode the layout as a
   Wireshark Lua dissector, an ImHex/010 Editor template, or a Kaitai Struct `.ksy`.
3. **Tackle serialization and crypto.** Protobuf: `protoc --decode_raw < msg.bin` for a quick
   read, `blackboxprotobuf` or `pbtk` to rebuild a usable `.proto`. gRPC is HTTP/2 headers plus
   a protobuf body. Encrypted frames: the key derivation lives in the client — pull it with
   `reverse-eng-binary-triage` (native), `reverse-eng-js` (web), or mobile tooling; look for the
   nonce/IV adjacent to the ciphertext.
4. **Produce the artifacts.** A message-type table (name / opcode / fields), at least one
   reproducible decode command or script, and evidence excerpts (raw hex + decoded result,
   redacted of secrets and third-party data).

## Gotchas
- **Length-field ambiguity** — big- vs little-endian, and header-inclusive vs body-only, are
  the two classic off-by-entire-parse errors; validate against a known sample's byte count.
- **A crash on replay is not proof of a bug** — it may be a checksum/sequence check rejecting
  you; fix your framing first, then judge the response.
- **Compressed-before-encrypted vs encrypted-before-compressed** — high entropy over the whole
  body means encryption; compression headers (`\x78\x9c`, `\x1f\x8b`) mean you can decompress
  directly.
- **Don't fuzz blind against the live service** — replay a captured, harmless message first;
  mutate one field at a time, and only within scope.

## Verify success
Your dissector or script decodes a fresh capture into the correct fields with no manual
fix-ups, and you can state the message-type dictionary and state machine. Bonus proof: a
replayed (in-scope) message with one mutated field is accepted by the server — the layout is
right, and the protocol is now fuzzable.

## References
Wireshark/tshark docs; Kaitai Struct gallery; blackboxprotobuf; `api-grpc`, `web-websocket`,
`reverse-eng-binary-triage` in this library.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
