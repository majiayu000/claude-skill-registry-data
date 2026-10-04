---
name: sdr-satellite
category: aerospace
description: "Software-defined radio (SDR) and satellite reception toolkit — what to install, what you can hear from space, and how to compose the open-source stack (SatDump, SatNOGS, GNU Radio, rustradio, satkit). Covers hardware abstraction (SoapySDR, rtl-sdr-rs), DSP frameworks (GNU Radio, liquid-dsp, rustradio, radiorust), receiver UIs (SDR++, SDRangel, Gqrx, CubicSDR), satellite decoders (SatDump for NOAA APT, Meteor-M LRPT, GOES HRIT, Inmarsat), ground-station orchestration (SatNOGS network, sgoudelis/ground-station, Hamlib), orbit mechanics (SGP4 in Python + Rust, satkit astrodynamics, dSGP4 differentiable). Use when: (1) the user wants to receive satellite signals — weather imagery, ISS SSTV, telemetry, (2) building a ground station or scheduling observations on SatNOGS, (3) decoding TLEs and computing satellite passes, (4) composing SDR tooling into a Rust pipeline (e.g. for Life Agent OS, Opsis world-state events, or arcan/sensorium), (5) explaining what an RTL-SDR or HackRF actually does, (6) deciding between SatDump vs custom GNU Radio flowgraph vs hand-rolled Rust DSP, (7) user mentions 'SDR', 'RTL-SDR', 'HackRF', 'NOAA', 'NOAA APT', 'Meteor-M', 'GOES', 'satellite reception', 'ground station', 'SatNOGS', 'SatDump', 'Gqrx', 'SDR++', 'SDRangel', 'TLE', 'SGP4', 'orbit propagation', 'Hamlib', 'Doppler correction', 'pass prediction', 'CelesTrak', 'amateur radio satellite', 'weather satellite', 'signal decoding'."
---

# SDR & Satellite Reception

How to hear satellites with a $30 dongle, decode the bits, predict the next pass, and (if we want) wire it into Life Agent OS or Opsis as a real-world-event source.

## What this skill covers

The full open-source satellite reception stack, by layer:

| Layer | What it does | Pick |
|---|---|---|
| **L0** Hardware abstraction | One API across dongles | `SoapySDR`; pure-Rust `rtl-sdr-rs` |
| **L1** DSP framework | Demod, filter, sync | `GNU Radio` (standard), `liquid-dsp` (lean C), `rustradio` (Rust), `radiorust` (Tokio) |
| **L2** Receiver UI | Watch the spectrum, demod live | `SDR++`, `SDRangel`, `Gqrx`, `CubicSDR`, `SigDigger` |
| **L3** Satellite decoders | TLE-aware, multi-protocol | `SatDump` (90+ sats) |
| **L4** Ground-station orchestration | Schedule, rotate, Doppler | `SatNOGS`, `sgoudelis/ground-station` (2026), `Hamlib` |
| **L5** Orbit mechanics | TLE → pass times → az/el | `sgp4` (Python), `neuromorphicsystems/sgp4` (Rust), `satkit` (full astro) |

Detail: [references/tools-by-layer.md](references/tools-by-layer.md).

## Quick start — your first weather image

About a 1-afternoon project, $50 total.

```bash
# 1. Hardware: RTL-SDR v4 ($30) + V-dipole antenna ($20 wire or 3D-printed QFH)

# 2. Software (macOS)
brew install --cask satdump
brew install gpredict     # pass prediction GUI

# 3. Find next NOAA 18/19 pass overhead
gpredict      # add NOAA 18, NOAA 19 from CelesTrak TLEs; watch for AOS

# 4. Decode (SatDump live mode, frequency 137.9125 MHz for NOAA 19)
satdump live_processing noaa_apt_demod baseband.raw \
  --source rtlsdr --frequency 137912500 --samplerate 2400000
```

Output: PNG weather imagery of wherever you are, georeferenced. SatDump handles APT, LRPT, HRPT, HRIT, Inmarsat Aero, and ~85 other satellite formats automatically.

Detail: [references/recipes.md](references/recipes.md).

## Quick start — no hardware (use someone else's)

```bash
# Visit https://network.satnogs.org/observations/new/
# Pick a station that can see the satellite you want
# Schedule an observation; the station records IQ + decodes for you
# Download the resulting waterfall, demod, decoded data via the SatNOGS API
```

SatNOGS is ~600 crowd-sourced ground stations worldwide. Free to schedule, public results.

## Quick start — Rust pipeline (no GUI)

For embedding satellite reception into a Rust service — relevant for Life Agent OS, Opsis world-state events, or arcan sensorium:

```toml
# Cargo.toml
[dependencies]
rtl-sdr-rs = "0.x"          # hardware
rustradio = "0.x"           # DSP block graph (or radiorust for Tokio-native)
sgp4 = "1.x"                # neuromorphicsystems/sgp4 — no_std capable
satkit = "0.16"             # full astrodynamics if needed
```

Shape:
- `rtl-sdr-rs` → raw IQ stream
- `rustradio` flowgraph → APT/LRPT demod → frames
- `sgp4` / `satkit` → georeference each frame against TLE
- Emit as `OpsisEvent { kind: "sat_pass", sat_id, lat, lon, alt, timestamp, payload }`

Detail: [references/composition.md](references/composition.md).

## What you can actually hear

| Satellite class | Band | What you get | Difficulty |
|---|---|---|---|
| NOAA 15/18/19 (APT) | 137 MHz | Live weather imagery, ~15-min passes | ★ easy |
| Meteor-M N2/N2-2 (LRPT) | 137 MHz | Higher-res digital weather imagery | ★★ |
| ISS SSTV / APRS | 145 MHz | Slow-scan images, packet radio | ★★ |
| GOES-16/18 (HRIT) | 1.7 GHz | Full-disk geostationary Earth | ★★★ (needs small dish) |
| Inmarsat Aero (STD-C, EGC) | L-band | Aviation messages, maritime safety | ★★★ |
| Iridium pager telemetry | L-band | Pager metadata; voice is encrypted | ★★★ |
| GPS L1 / Galileo E1 | L-band | Your own position from raw signals | ★★★★ |

## Architectural threads (why this lives in the workspace)

Two non-forced connections to existing Broomva work:

**SatNOGS ↔ Spaces.** SatNOGS's distributed ground-station network has the same pattern as `core/life/spaces`: global registry of nodes, a scheduler that assigns work to nodes with the right capability, observations flow back to a central DB. If we ever want "Life node, but with antennas," SatNOGS already solved the rotator/Doppler/TLE-sync coordination problem on top of an open scheduling API.

**Satellite passes ↔ Opsis.** Opsis is already an AI-native world-state engine with `OpsisEvent` protocol and a CesiumJS globe. Live satellite passes are *literally* georeferenced world-state events. `satkit` (Rust SGP4 + ITRF/Geodetic transforms) → `OpsisEvent { kind: "sat_pass", ... }` → CesiumJS globe already renders it. Zero forced abstraction; the pieces match.

Detail: [references/composition.md](references/composition.md).

## Repository layout (if we build the pipeline)

Speculative — no code shipped yet, this is the skill's compositional seed:

```
~/broomva/experiments/sdr-satellite/         # (proposed)
├── crates/
│   ├── sat-sdr/             # rtl-sdr-rs wrapper, hardware enumeration
│   ├── sat-decode/          # rustradio flowgraphs for APT / LRPT / SSTV
│   ├── sat-orbit/           # satkit-based pass prediction + Doppler
│   └── sat-opsis-bridge/    # decoded frames → OpsisEvent emitter
└── scripts/
    ├── first-image.sh       # The "your first NOAA image" walkthrough
    └── schedule-satnogs.sh  # Submit observation to SatNOGS network
```

## References

- [tools-by-layer.md](references/tools-by-layer.md) — full L0-L5 stack survey with comparison tables
- [recipes.md](references/recipes.md) — concrete recipes: first NOAA APT image, SatNOGS scheduling, GOES dish setup, Meteor-M decode
- [composition.md](references/composition.md) — Rust pipeline composition for Life / Opsis / arcan; SatNOGS ↔ Spaces pattern analysis

## Source list

- [SatNOGS — global ground-station network](https://satnogs.org/) · [Wiki](https://wiki.satnogs.org/Introduction) · [Network](https://network.satnogs.org/)
- [SatDump](https://www.satdump.org/about/) — the decode engine
- [Ground Station orchestrator (sgoudelis/ground-station)](https://github.com/sgoudelis/ground-station) · [RTL-SDR.com writeup](https://www.rtl-sdr.com/ground-station-an-open-source-sdr-orchestration-platform-for-satellite-tracking-and-decoding/)
- [RTL-SDR supported software (the canonical big list)](https://www.rtl-sdr.com/big-list-rtl-sdr-supported-software/)
- [15 Best SDR Software 2026 (OneSDR)](https://www.onesdr.com/best-sdr-software/)
- [rtl-sdr-rs crate](https://crates.io/crates/rtl-sdr-rs) · [rustradio](https://crates.io/crates/rustradio) · [radiorust](https://lib.rs/crates/radiorust)
- [neuromorphicsystems/sgp4 (Rust, no_std)](https://github.com/neuromorphicsystems/sgp4) · [satkit (Rust + PyO3 astrodynamics)](https://github.com/ssmichael1/satkit) · [python-sgp4](https://pypi.org/project/sgp4/) · [heyoka.py differentiable SGP4](https://bluescarni.github.io/heyoka.py/notebooks/sgp4_propagator.html)
