---
name: location-suche
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: Location, restaurant and hotel search via OpenStreetMap (Nominatim + Overpass API). Returns POIs (Points of Interest) near a location or searches by free text.

tags: [location, openstreetmap, poi, nominatim, overpass, restaurant, hotel]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['urllib.request', 'urllib.parse', 'urllib.error', 'json', 'time']}
runtime: python3
entry_point: location_suche_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/location_search.py', 'origin_version': '1.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (save_location, list_locations, _ensure_table, _get_db). Kein Store. Userneutral (keine privaten Pfade). Headless, nur Stdlib.\n'}
language: de
visibility: public
---
<img src="banner.png" width="100%" alt="location-suche banner">

# Location-Suche

**Ort-, Restaurant- und Hotelsuche via OpenStreetMap**

---

## Überblick

Sucht nach Restaurants, Hotels, Cafés und anderen Orten mithilfe der
OpenStreetMap-Dienste Nominatim (Geocoding) und Overpass (POI-Suche).
Kein API-Key erforderlich. Kein persistenter Store.

---

## Trigger

| Phrase | Aktion |
|---|---|
| „Such ein Restaurant in München" | POI-Suche: category=restaurant, near=München |
| „Hotels in der Nähe von Wien" | POI-Suche: category=hotel, near=Wien |
| „Wo ist der Eiffelturm?" | Nominatim-Freitext-Suche |
| „Finde Cafés in Berlin" | POI-Suche: category=cafe, near=Berlin |
| „Suche Apotheke nahe Potsdam" | POI-Suche: category=pharmacy, near=Potsdam |

---

## Workflow

1. **Trigger erkennen:** Enthält die Anfrage eine Kategorie (Restaurant, Hotel usw.)
   und einen Ort → Schritt 2. Sonst Freitext → Schritt 4.
2. **Ort geocodieren:** Nominatim liefert Koordinaten für den genannten Ort.
3. **POIs suchen:** Overpass-API sucht Einrichtungen der Kategorie im Umkreis.
4. **Ergebnis anzeigen:** Liste mit Name, Adresse, Entfernung (m) ausgeben.
5. **Freitext-Suche (Fallback):** Nominatim-Freitext liefert direkte Treffer.

---

## CLI

```bash
# POI-Suche (Kategorie + Ort)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py restaurant München

# Ort geocodieren
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --geocode "Brandenburger Tor Berlin"

# Radius anpassen (Standard: 1000 m)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py hotel Wien --radius 2000

# Hilfe
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --help
```

---

## Store

Kein persistenter Store. Ergebnisse werden nur angezeigt, nicht gespeichert.

---

## Unterstützte Kategorien

restaurant, cafe, bar, pub, fast_food, hotel, hostel, guest_house, supermarket,
pharmacy, hospital, bank, atm, fuel, parking, bus_stop, train_station, museum,
cinema, theatre, library, school, university, church

---

## Haltung

- Immer den Nutzer nach dem Ort fragen, wenn keiner genannt wurde.
- Bei mehr als 10 Ergebnissen nur die 5 nächsten anzeigen, Rest auf Anfrage.
- Entfernung in Metern angeben, ab 1 km in km (1 Dezimalstelle).
- Datenschutz: Keine Standortdaten werden gespeichert oder übertragen außer an
  die öffentliche Nominatim/Overpass-API (openstreetmap.org).

---

## Datenschutz

Suchanfragen gehen an `nominatim.openstreetmap.org` und `overpass-api.de`.
Keine Anmeldung, kein API-Key, keine persistente Datenspeicherung.
User-Agent wird gemäß Nominatim-Policy gesetzt.

---

## Verwandte Ressourcen

- `reiseroute` — Routenplanung von A nach B (nutzt ebenfalls Nominatim für Geocoding)
- `wetter` — Wetter am aktuellen Ort

---

## Changelog

| Version | Datum | Änderung |
|---|---|---|
| 1.0.0 | 2026-06-22 | Erstellt aus BACH location_search.py v1.1.0; Store entfernt |
