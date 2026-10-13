---
name: hardware-radio-sdr
description: >
  Authorized RF/SDR security research on non-Wi-Fi radio signals — identify a signal's frequency
  and modulation receive-only, demodulate and reverse the protocol, and assess replay feasibility
  in a shielded lab. Load for wireless remotes, key fobs, sensors, telemetry, ISM-band devices,
  ADS-B, or any sub-GHz/RF protocol outside classic Wi-Fi. Signals: unknown RF device in scope,
  315/433/868/915 MHz, OOK/ASK/FSK captures, RTL-SDR/HackRF work.
domain: hardware
type: methodology
stability: learning
modes: [pentest]
severity: medium
tools: [rtl-sdr, hackrf, gnuradio, urh, inspectrum, gqrx]
schema_version: 1
---

# RF / SDR signal analysis (non-Wi-Fi radio)

## When it applies
The scope includes a radio device that isn't Wi-Fi — a wireless remote, key fob, alarm sensor,
telemetry link, or ISM-band gadget — and you need to know whether an attacker can eavesdrop on,
forge, or replay its traffic. **Spectrum use and transmission are heavily regulated**: load
`tradecraft-scope-roe` and make `scope.txt` state the exact devices, frequency bands, and whether
**transmitting is permitted at all — the default is receive-only**. Classic Wi-Fi attacks belong to
the wireless domain (`wireless-wpa2-attacks`, `wireless-evil-twin`); this skill is generic SDR RF.

## Why it works
Cheap SDR hardware (RTL-SDR for receive, HackRF for transmit) turns a wide slice of spectrum into
raw I/Q samples. Most low-cost remotes and sensors use simple, unauthenticated modulation
(OOK/ASK/2-FSK) with fixed or rolling codes, so the entire protocol is recoverable from a capture:
demodulate to symbols, read the bit pattern, and you know exactly what a receiver trusts. Replay
and forgery feasibility then falls out of whether the code is fixed, rolling, or challenge-response.

## Method
1. **Confirm the legal envelope before powering anything on.** Note the licensed bands, protected
   services (aviation, emergency — stay far away), and the authorization reference for any TX.
   Receive-only is the default; transmitting happens only in a shielded room (Faraday cage) with
   written permission.
2. **Survey receive-only.** Sweep the expected band in `gqrx` (or `rtl_power` for a wide passive
   sweep) and note the center frequency, bandwidth, and duty cycle of the target signal. ISM
   defaults worth checking first: 315 / 433.92 / 868 / 915 MHz.
3. **Capture I/Q.** Record the raw signal for offline work:
   `hackrf_transfer -r capture.cs8 -f 433920000 -s 2000000` (`-r` = receive to file, `-f` Hz,
   `-s` sample rate; 2 Msps covers most narrowband remotes).
4. **Analyze the capture.** Open it in **Inspectrum** to see the symbol timing and modulation
   visually, then demodulate and decode in **URH** (Universal Radio Hacker) — it auto-detects
   OOK/ASK/FSK, slices symbols to bits, and lets you diff transmissions to separate the fixed
   preamble/address from the counter/button fields. GNU Radio flowgraphs handle protocols URH
   can't.
5. **Classify the code scheme.** Fixed code (identical bits every press) = trivially replayable.
   Rolling code = replay fails but look for rollback/jam-and-replay weaknesses and predictable
   counters. Document which class you observed with capture evidence.
6. **Assess replay/transmit only under the lab rules**: shielded room, written TX authorization,
   the target device as the only receiver. `hackrf_transfer -t replay.cs8 -f 433920000 -s 2000000`
   retransmits a capture — outside a shielded environment this can be a criminal offense regardless
   of engagement scope.
7. **Report the control question, not the capture.** The finding is "an unauthenticated attacker
   can open / arm / spoof this" plus hardening advice (rolling codes, encryption, RX timeouts), not
   a dump of RF trivia.

## Gotchas
- **Default to RX and write the legal boundary into your notes** — which bands, which devices, TX
  yes/no, and the authorization reference. If it's not written, it's receive-only.
- **Never jam or interfere with public communications**, and never transmit outside the shielded
  lab — including "just a quick replay test" on the bench.
- **Sanitize evidence**: don't publish unsanitized frequency + location combinations where the
  pairing itself is sensitive (site layouts, alarm frequencies).
- **Rolling codes defeat naive replay** — don't report "replayable" from a single capture; diff
  several transmissions first.
- **Sample rate too low aliases the signal away** — if you can't find a known transmitter, widen
  the sweep and raise `-s` before concluding it's absent.

## Verify success
From receive-only analysis you can state the center frequency, modulation, symbol rate, and code
scheme (fixed/rolling/encrypted) of the target signal, backed by labeled captures — and a clear
verdict on whether unauthorized control is possible, with any transmit/replay test done strictly
inside the authorized shielded setup.

## References
URH and GNU Radio documentation; Inspectrum; the wireless domain skills for Wi-Fi targets.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
