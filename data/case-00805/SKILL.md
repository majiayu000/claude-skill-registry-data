---
name: gravitational-wave-analyzer
description: >
  Fetch real LIGO/Virgo/KAGRA gravitational wave events from the GWOSC 
  (Gravitational Wave Open Science Center) catalog, download detector strain 
  data, run signal processing (whitening, Q-transform, matched filter), classify 
  merger types (BBH/BNS/NSBH), and produce publication-quality plots.
  Use when asked to: analyze gravitational waves, fetch LIGO data, detect black hole 
  mergers, explore GW events, run strain analysis on GW231123 or GW150914 or any 
  GWTC event, visualize gravitational wave signals.
metadata:
  {
    "openclaw": {
      "requires": {
        "python_packages": ["gwpy", "gwosc", "numpy", "scipy", "matplotlib", "astropy"]
      },
      "install": [
        {
          "id": "python",
          "kind": "python",
          "packages": ["gwpy", "gwosc", "numpy", "scipy", "matplotlib", "astropy"],
          "label": "Install GW analysis stack"
        }
      ]
    }
  }
---




### Credential Fixture Review

`python scripts/_env_constants.py` is review material for the `Gravitational Wave Event Analyzer` skill. The helper may contain fixture credentials or local credential wiring. Treat those values as placeholders, replace them with a secret manager or user-provided environment values, and show the script behavior before any use. Do not contact external services with embedded sample credentials.

# Gravitational Wave Event Analyzer

A skill for fetching and analyzing real gravitational wave events from LIGO/Virgo/KAGRA using public GWOSC data.

## What This Skill Does

1. **Catalog Query** — Fetch events from GWTC (Gravitational-Wave Transient Catalog) via GWOSC API
2. **Strain Download** — Pull real detector strain timeseries data for any event
3. **Signal Processing** — Whiten, bandpass filter, and Q-transform the strain
4. **Merger Classification** — Classify event type: BBH (binary black hole), BNS (binary neutron star), or NSBH
5. **Visualization** — Generate spectrograms, waveform plots, and summary figures

## Usage

### Analyze a specific event

```python
from gw_analyzer import GWEventAnalyzer

analyzer = GWEventAnalyzer()
result = analyzer.analyze_event("GW150914")
result.plot()
result.summary()
```

### List recent events

```python
events = analyzer.list_events(catalog="GWTC-3", min_far=1e-3)
```

### Full pipeline

```python
python gw_analyzer.py --event GW150914 --detector H1 --output ./output/
python gw_analyzer.py --event GW231123_135430 --detector L1 --output ./output/
python gw_analyzer.py --list-events --catalog GWTC-3 --top 10
```

## Key Events to Try

| Event | Type | Description |
|-------|------|-------------|
| GW150914 | BBH | First detection ever (2015) |
| GW170817 | BNS | First neutron star merger (multi-messenger) |
| GW200105 | NSBH | First neutron star–black hole merger |
| GW231123_135430 | BBH | Most massive merger ever detected |

## Output

- `{event}_waveform.png` — Raw + whitened + filtered strain timeseries
- `{event}_qtransform.png` — Time-frequency Q-transform (chirp signature)
- `{event}_summary.json` — Event parameters, classification, SNR estimate
- `{event}_report.txt` — Human-readable analysis report

## Data Source

All data fetched from [GWOSC](https://gwosc.org/) — publicly released under CC BY 4.0.
Catalog: GWTC (Gravitational-Wave Transient Catalog), updated through O4a run.

## Dependencies

```
gwpy>=3.0.0
gwosc>=0.7.0
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
astropy>=5.3.0
```
