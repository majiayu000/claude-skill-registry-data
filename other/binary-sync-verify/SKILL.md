---
name: binary-sync-verify
description: Measure and test a gaza-geo-sync integration - payload bytes before/after, round-trip correctness of JSON vs binary, strict decoding, upload request rate - and report honestly. Use after integrating or migrating to the binary position format, or when asked whether the binary sync is actually smaller/faster.
---

# Verify a binary position sync

## 1. Correctness (must pass before any numbers)
- **Round-trip:** for the same server state, `Accept: application/json` and
  `Accept: application/octet-stream` must yield the same records after `fetchPositions`
  (lat/lon equal after `codec.round`, speed within `speedStep/2`, time within 1 s).
  Pattern: `tests/sync.test.ts` → "JSON and binary decode to identical payloads".
- **Strict decoder:** truncated, trailing-byte, wrong-version, wrong-profile and random inputs
  throw `CodecError` and nothing else (`tests/fuzz.test.ts` pattern, 20,000 inputs).
- **Fallback:** a client sending no Accept header gets JSON; a server answering JSON is
  handled by the client; an upload refused with 400 is retried as JSON.
- **Offline:** with the network off, the screens read the cached JSON records unchanged.

## 2. Bytes
```bash
# JSON as most proxies send it (gzip) vs binary. Run against your dev server.
curl -s -o /dev/null -w 'json %{size_download} B\n' -H 'Accept-Encoding: gzip' -H 'Accept: application/json' "$URL"
curl -s -o /dev/null -w 'bin  %{size_download} B\n' -H 'Accept-Encoding: gzip' -H 'Accept: application/octet-stream' "$URL"
curl -s -D - -o /dev/null -H 'Accept: application/octet-stream' "$URL" | grep -i -E 'content-type|vary|content-encoding'
```
Report per refresh **and** per minute (× refreshes/min). Count headers too (`curl -w '%{size_header}'`):
for small uploads headers dominate, so say so.

## 3. Requests
- Uploads per minute moving vs parked, before/after the standing-still throttle
  (`bench/uploads.ts` shows the method on a synthetic trace).

## 4. Time and CPU (optional, for weak links)
- `bench/sim/` in the gaza-geo-sync repo: headless Chromium behind tc-netem profiles
  (Wi-Fi, 4G, 3G, EDGE, lossy). Medians and p90, never single runs.

## Reporting rules
- Label synthetic data as synthetic. Give environment (device/CPU throttle, network profile).
- State where binary did not help (headers, CPU decode cost vs native JSON.parse, tiny payloads).
