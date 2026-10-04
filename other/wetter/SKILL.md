---
name: wetter
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: Answers weather questions for a location or coordinates via wttr.in (free, no API key). Current weather + 3-day forecast. Location comes from the user request or preferences; optional short cache.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [wetter, wttr, vorschau, assist]
language: de
status: active
visibility: public
dependencies: {'tools': ['wetter_core.py'], 'services': [], 'protocols': [], 'python': ['urllib', 'json']}
provenance: {'origin': 'bach', 'origin_path': 'system/hub/_services/weather/weather_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---
<img src="banner.png" width="100%" alt="wetter banner">

# Wetter

Schnelle, schluesselfreie Wetterauskunft fuer den Alltag.

## Zweck

Beantwortet „Wie wird das Wetter?"-Fragen ohne API-Key (Datenquelle: wttr.in).
Liefert aktuelles Wetter (Temperatur, gefuehlt, Wind, Luftfeuchte, UV) plus eine
kompakte 3-Tage-Vorschau. **Userneutral:** kein fester Standort im Code — der Ort
kommt aus der Anfrage oder aus `assist/prefs.json` (`wetter_default_location`),
die das LLM interaktiv mit dem Nutzer fuellt.

## Trigger

| Nutzereingabe | Aktion |
|---|---|
| „Wetter fuer Potsdam?" / „Wie wird das Wetter in Hamburg?" | `wetter_core.py "<Ort>"` |
| „Wetter morgen?" (ohne Ort) | `wetter_core.py --default` (Ort aus prefs) |
| „Mein Standard-Wetterort ist Potsdam" | `wetter_core.py --set-default "Potsdam"` |
| Koordinaten bekannt | `wetter_core.py <lat> <lon>` |

## Workflow

```
1. Ort bestimmen: aus Anfrage; sonst prefs.json (wetter_default_location);
   sonst Nutzer interaktiv fragen + optional als Default speichern.
2. wetter_core.py abfragen (wttr.in, 2 Versuche, 30-min-Cache).
3. Lesbaren Wetter-Text + 3-Tage-Vorschau praesentieren.
```

## CLI-Einstieg (wetter_core.py)

```bash
python wetter_core.py "Potsdam"          # Ort
python wetter_core.py 52.6789 13.5878   # Koordinaten
python wetter_core.py --default         # Ort aus prefs.json
python wetter_core.py --set-default "Potsdam"
```

## Store (optional)

- **Kein Pflicht-Store.** Optionaler Kurz-Cache `assist/wetter/.cache.json`
  (TTL 30 min, best-effort) — vermeidet wiederholte Netzabrufe.
- Standortpraeferenz in `assist/prefs.json` (`wetter_default_location`).

## Haltung

Wir nutzen wttr.in als schluesselfreie Default-Quelle, sind aber offen fuer
andere Wetter-Backends (z.B. DWD/OpenWeather), falls der Nutzer das wuenscht.

## Datenschutz

- Nur der Ortsname/die Koordinaten gehen an wttr.in (noetig fuer die Abfrage).
- Keine Telemetrie, kein Konto. Cache + Praeferenz bleiben lokal.

## Verwandte Ressourcen

- `assist/AGENTS.md` — Umbrella-Router
- `assist/reiseroute/` — nutzt Wetter ggf. fuer Reiseplanung (geplant)

## Changelog

### 0.1.0 (2026-06-22)
- Initiale Version. Portiert aus BACH `hub/_services/weather/weather_service.py` (MIT).
- Erweitert: Ortsname-Support (nicht nur Koordinaten), 3-Tage-Vorschau,
  optionaler Cache, prefs-basierter Standard-Ort. Userneutral.
