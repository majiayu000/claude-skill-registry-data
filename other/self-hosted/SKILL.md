---
name: self-hosted
description: Use for local LLM fallback, failover, and Ollama health.
category: system
---

# Self-Hosted Independence — Local LLM Fallback + Auto-Failover

Erkennt lokale LLM-Provider (Ollama, llama.cpp), generiert Fallback-Config,
überwacht Health von primary + fallback, und schaltet bei 3× Fehlschlag
automatisch auf local um.

## Verfügbare CLI-Befehle

```bash
# Alle Provider prüfen
python scripts/self-hosted.py --check

# Status + Config anzeigen
python scripts/self-hosted.py --status

# Manuell umschalten
python scripts/self-hosted.py --switch-to local
python scripts/self-hosted.py --switch-to primary
python scripts/self-hosted.py --switch-to auto

# Benchmark (Latenz remote vs local)
python scripts/self-hosted.py --bench

# JSON-Report
python scripts/self-hosted.py --report

# Setup: Ollama installieren + Modelle laden
python scripts/self-hosted.py --setup
```

## Wichtige Pfade

| Pfad | Beschreibung |
|------|-------------|
| `~/.self-hosted/config.json` | Konfiguration (primary, fallback, failover) |
| `~/.self-hosted/state.json` | Laufender State (active_provider, failures, history) |
| `~/scripts/self-hosted.py` | Hauptscript |
| `~/scripts/self-hosted-cron.py` | Cron-Wrapper (alle 5 Min) |

## Auto-Failover

- Prüft primary (OpenRouter/Remote) alle 60s
- Wenn 3× hintereinander fehlschlägt → automatisch auf local (Ollama)
- Wenn primary wieder da ist → automatische Recovery (nach 3 erfolgreichen Checks)
- History der letzten 100 Health-Checks in state.json

## Fallback-Plan

1. **Ollama** mit qwen3.5:latest (oder phi4-mini:latest)
2. **CPU-Modus** mit qwen3:1.7b (tiny model) falls kein GPU-Modell verfügbar
3. **llama.cpp** auf localhost:8080 (OpenAI-kompatibel) wird ebenfalls erkannt

## Auto-Detection

Das Script erkennt beim Start automatisch das beste verfügbare Ollama-Modell:
- Bevorzugt deepseek-coder-Modelle, dann qwen3.5, phi4-mini
- Wählt automatisch einen kleinen CPU-Modus (qwen3:1.7b / phi4-mini)
- Die Config wird nur einmal generiert und kann manuell editiert werden

## Setup (Erstinstallation)

```bash
python scripts/self-hosted.py --setup
```

Das lädt automatisch (abhängig von Verfügbarkeit):
- deepseek-coder (falls vorhanden)
- qwen3.5:latest (Standard)
- phi4-mini:latest (Fallback)
- qwen3:1.7b (CPU-Modus)

## Exit-Codes

- `0` = alles OK (primary aktiv)
- `1` = Fallback aktiv (local läuft, primary down)
- `2` = kein LLM verfügbar