---
name: tageszeitung
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: Creates a personalised daily newspaper from RSS feeds and web sources. Ported from the BACH news system (news.py + newspaper_generator.py). Own SQLite store (no Origin-DB). feedparser optional — XML fallback via stdlib. PDF export via Edge Headless (msedge.exe).

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [zeitung, news, rss, feed, pdf, tageszeitung]
language: de
status: stable
visibility: public
dependencies: {'tools': [{'name': 'msedge.exe', 'optional': True, 'purpose': 'HTML → PDF (Edge Headless); without Edge: HTML output only'}], 'services': [], 'protocols': [], 'python': [{'name': 'feedparser', 'optional': True, 'install': 'pip install feedparser', 'purpose': 'RSS parsing (main backend). Fallback: defusedxml → regex'}, {'name': 'defusedxml', 'optional': True, 'install': 'pip install defusedxml', 'purpose': 'XXE-safe XML parser as fallback when feedparser is missing. Without defusedxml a regex fallback is used (no ET.fromstring on network data).'}]}
provenance: {'origin': 'bach-port', 'origin_path': 'BACH/system/hub/news.py + hub/_services/newspaper/newspaper_generator.py', 'origin_version': 'news.py v1.x, newspaper_generator.py v1.x', 'origin_repo': 'ellmos-ai/bach (privat)', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'notes': 'Schema (news_sources + news_items) 1:1 aus BACH news.py portiert. BaseHandler-Abhängigkeit entfernt. Origin-DB-Pfad entfernt. DB-Pfad konfigurierbar. newspaper_generator.py-Logik (HTML-Render + Edge-PDF) userneutral übernommen.\n'}
---
<img src="banner.png" width="100%" alt="tageszeitung banner">

## Zweck

Aus konfigurierten RSS-Feeds und Web-Quellen Artikel abrufen, nach Kategorien
sortieren und als HTML/PDF-Tageszeitung rendern. Artikel werden lokal in
`tageszeitung/store.db` gespeichert und als gelesen markiert.

---

## Trigger

| Phrase | Aktion |
|---|---|
| „Erstell meine Tageszeitung" | Artikel abrufen + PDF rendern |
| „Tageszeitung für heute" | Heutige Zeitung rendern |
| „Füge Feed hinzu [URL]" | RSS-Quelle registrieren |
| „Zeig meine Quellen" | Quellen-Liste ausgeben |
| „Fetch News" | Alle Quellen abrufen (kein Render) |

---

## Workflow

1. **Quellen prüfen**: Alle aktiven Quellen aus `news_sources` lesen.
2. **Fetch**: RSS via feedparser (oder xml.etree-Fallback), Web via urllib.
3. **Deduplizierung**: UNIQUE(source_id, url) verhindert Duplikate.
4. **Render**: Ungelesene Artikel nach Kategorie gruppieren → HTML → PDF.
5. **Liefern**: HTML/PDF im Ausgabe-Ordner ablegen (konfigurierbarer Pfad).

---

## CLI-Einstieg

```bash
# Quelle hinzufügen
python tageszeitung_core.py add-source "Heise" rss https://www.heise.de/rss/heise-atom.xml --category tech

# Alle Quellen abrufen
python tageszeitung_core.py fetch

# Tageszeitung rendern (HTML + PDF wenn Edge verfügbar)
python tageszeitung_core.py render [--date 2026-06-22] [--out /pfad/]

# Quellen auflisten
python tageszeitung_core.py sources

# Ungelesene Artikel
python tageszeitung_core.py items [--limit 50] [--category tech]

# Artikel als gelesen markieren
python tageszeitung_core.py read <item_id>

# Alternativer Store (z.B. für Tests)
python tageszeitung_core.py --store /tmp/t.db sources --dry-run
```

---

## Store

| Eigenschaft | Wert |
|---|---|
| Typ | SQLite |
| Pfad (Standard) | `skills/assist/tageszeitung/store.db` |
| Override | `--store <pfad>` oder Env `TAGESZEITUNG_STORE` |
| Tabellen | `news_sources`, `news_items` |

### Schema (aus BACH news.py portiert)

```sql
CREATE TABLE IF NOT EXISTS news_sources (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    type         TEXT NOT NULL DEFAULT 'rss',  -- rss | web
    url          TEXT NOT NULL UNIQUE,
    category     TEXT DEFAULT 'Allgemein',
    schedule     TEXT DEFAULT 'daily',
    is_active    INTEGER DEFAULT 1,
    last_fetched TEXT,
    fetch_count  INTEGER DEFAULT 0,
    error_count  INTEGER DEFAULT 0,
    last_error   TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS news_items (
    id           TEXT PRIMARY KEY,
    source_id    TEXT NOT NULL REFERENCES news_sources(id),
    title        TEXT NOT NULL,
    content      TEXT,
    summary      TEXT,
    url          TEXT,
    author       TEXT,
    published_at TEXT,
    fetched_at   TEXT NOT NULL,
    is_read      INTEGER DEFAULT 0,
    category     TEXT,
    UNIQUE(source_id, url)
);
```

---

## Haltung

- feedparser wird bevorzugt; ohne feedparser greift ein xml.etree-Fallback für einfache RSS 2.0-Feeds.
- PDF-Erzeugung erfordert `msedge.exe` im System-PATH oder `MSEDGE_PATH`-Env. Ohne Edge wird nur HTML gerendert.
- Maximale Artikel pro Kategorie: konfigurierbar via `assist/prefs.json` (`tageszeitung_max_per_category`, Standard: 5).

---

## Datenschutz

- Artikel-Inhalte bleiben lokal in `store.db`.
- Keine externen Analyse-Dienste — nur die konfigurierten RSS-/Web-Quellen werden aufgerufen.

---

## Verwandte Ressourcen

- BACH `hub/news.py` — Origin (read-only)
- BACH `hub/_services/newspaper/newspaper_generator.py` — Origin (read-only)

---

## Changelog

| Version | Datum | Änderung |
|---|---|---|
| 0.1.0 | 2026-06-22 | Erstanlage — BACH-Schema portiert, eigener Store, feedparser optional |
