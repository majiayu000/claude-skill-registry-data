---
name: reiseroute
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: Route planning from A to B via OSRM (Open Source Routing Machine). Supports car, bicycle and pedestrian. No API key required.

tags: [routing, navigation, osrm, openstreetmap, reise]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['urllib.request', 'urllib.parse', 'urllib.error', 'json']}
runtime: python3
entry_point: reiseroute_core.py
provenance: {'origin': 'BACH hub routing-service', 'origin_path': 'system/hub/_services/routing/routing_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'urllib.parse-Import an den Kopf verschoben (war im Original nur im else-Zweig). geocode_place (Nominatim) integriert. Keine Origin-DB. Kein Store. Userneutral, headless, nur Stdlib.\n'}
language: de
visibility: public
---
<img src="banner.png" width="100%" alt="reiseroute banner">

# Reiseroute

**Routenplanung via OSRM (Open Source Routing Machine)**

---

## Überblick

Plant Routen zwischen zwei Orten (Namen oder Koordinaten) über den öffentlichen
OSRM-Dienst (`router.project-osrm.org`). Gibt Distanz, Fahrzeit und Verkehrsmittel
aus. Kein API-Key, kein Konto erforderlich.

---

## Trigger

| Phrase | Aktion |
|---|---|
| „Plan die Route von Berlin nach Hamburg" | Auto-Route, Ortsnamen geocodieren |
| „Wie lange dauert die Fahrt von München nach Wien mit dem Auto?" | Auto-Route + Zeitangabe |
| „Route mit dem Fahrrad von Potsdam nach Berlin" | Fahrrad-Modus |
| „Zu Fuß von Kreuzberg nach Mitte Berlin" | Fußgänger-Modus |
| „Strecke von 52.52,13.41 nach 53.55,9.99" | Direkt-Koordinaten |

---

## Workflow

1. **Start- und Zielort extrahieren** aus der Nutzereingabe.
2. **Modus erkennen:** Auto (Standard), Fahrrad, Fuß.
3. **Geocodieren:** Ortsnamen → Koordinaten via Nominatim.
4. **OSRM anfragen:** Gibt Distanz (km) + Dauer (formatiert) zurück.
5. **Ergebnis ausgeben:** Übersichtliche Textzusammenfassung.

---

## CLI

```bash
# Auto-Route zwischen zwei Orten
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Berlin" "Hamburg"

# Fahrrad
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Potsdam" "Berlin" --modus fahrrad

# Zu Fuß
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Kreuzberg, Berlin" "Mitte, Berlin" --modus fuss

# Koordinaten direkt (lat,lon)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "52.5200,13.4050" "53.5500,9.9937"

# JSON-Ausgabe
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "München" "Wien" --json

# Hilfe
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py --help
```

---

## Modi

| Modus | Alias | OSRM-Profil |
|---|---|---|
| auto (Standard) | car, pkw, fahren | driving |
| fahrrad | bike, rad, radfahren | cycling |
| fuss | foot, laufen, gehen, zu fuss | foot |

---

## Store

Kein persistenter Store. Routen werden nicht gespeichert.

---

## Haltung

- Immer Start und Ziel vor der Berechnung benennen.
- Klarstellen wenn ein Ort mehrdeutig ist (z.B. „Wien" = Österreich oder gleichnamige Stadt?).
- Hinweis: OSRM liefert die schnellste Route ohne Echtzeit-Verkehr.
- Bei sehr langen Fußgänger-Routen (> 20 km) einen Hinweis ausgeben.

---

## Datenschutz

Anfragen gehen an `nominatim.openstreetmap.org` (Geocoding) und
`router.project-osrm.org` (Routing). Keine Anmeldung, kein API-Key,
keine persistente Datenspeicherung.

---

## Verwandte Ressourcen

- `location-suche` — POI-Suche (nutzt ebenfalls Nominatim)
- `wetter` — Wetter am Reiseziel

---

## Changelog

| Version | Datum | Änderung |
|---|---|---|
| 1.0.0 | 2026-06-22 | Erstellt aus BACH routing_service.py v1.0; Geocoding integriert |
