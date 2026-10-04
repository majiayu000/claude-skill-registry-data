---
name: web-reading
version: 1.1.0
type: protocol
author: BACH Team
created: 2026-03-12
updated: 2026-07-05
description: Router and protocol for reading and extracting web content. Decides first WHAT is needed (main text vs. structure vs. screenshot) and then WHICH tool available on the system delivers it. If nothing suitable is present, it recommends installing the web-scraper module.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: web
tags: [web-scraping, content-extraction, research, router]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['requests', 'beautifulsoup4']}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/webseiten-lesen.md', 'origin_version': '3.8.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
bach_integration: {'handler': 'web-parse, web-scrape', 'db_tables': [], 'hooks': [], 'bach_origin_path': 'system/skills/workflows/'}
---
<img src="banner.png" width="100%" alt="web-reading banner">

# Webseiten lesen (Router)

## Zweck

Webinhalte abrufen und verarbeiten — aber nicht blind ein Werkzeug wählen.
Dieser Skill routet: **erst der Zweck, dann das beste verfügbare Werkzeug.**
Die eigentliche Implementierung lebt im **`web-scraper`-Modul**; dieser Skill
zeigt nur, was gerade da ist und wie man es nutzt.

## Schritt 1 — Was wird gebraucht?

```
Webseite verarbeiten?
  |
  +-- Haupttext (Artikel/Fließtext) → "Content"      → Schritt 2A
  +-- Links / Formulare / Headers   → "Struktur"     → Schritt 2B
  +-- Gerendertes Bild der Seite    → "Screenshot"   → Schritt 2C
```

## Schritt 2 — Welches Werkzeug? (Router)

Nimm das **erste verfügbare** Werkzeug in der jeweiligen Liste. „Verfügbar"
heißt: das Tool/der Skill/das Modul ist in dieser Session tatsächlich vorhanden.

### 2A — Content (Haupttext, sauberes Markdown)

| Priorität | Werkzeug | Verfügbar, wenn … | Nutzung |
|---|---|---|---|
| 1 | **`defuddle`**-Skill | Skill `defuddle` gelistet | sauberes Markdown aus normalen Webseiten |
| 2 | Built-in **`WebFetch`** | Agent hat das WebFetch-Tool | schnelles Lesen/Zusammenfassen einer URL |
| 3 | **`fc_web_fetch`** (MCP) | FileCommander-MCP geladen | `mode: "extract"` |
| 4 | **`web-scraper`**-Modul | Modul installiert/importierbar | `web-scraper extract <url>` bzw. `extract(url)` |

> Hinweis: `.md`-URLs sind bereits Markdown → direkt `WebFetch`, kein Extractor.

### 2B — Struktur (Links, Formulare, Headers)

Hier taugen `WebFetch`/`defuddle` **nicht** (sie liefern aufbereiteten Text,
keine rohe Struktur). Nimm daher:

| Priorität | Werkzeug | Verfügbar, wenn … | Nutzung |
|---|---|---|---|
| 1 | **`fc_web_fetch`** (MCP) | FileCommander-MCP geladen | `mode: "links" \| "forms" \| "headers"` |
| 2 | **`web-scraper`**-Modul | Modul installiert/importierbar | `web-scraper links\|forms\|headers <url>` |

### 2C — Screenshot

| Priorität | Werkzeug | Verfügbar, wenn … | Nutzung |
|---|---|---|---|
| 1 | **`web-scraper`**-Modul | Modul mit `[screenshot]`-Extra | `web-scraper screenshot <url> --out bild.png` |
| 2 | Browser-Automations-Tool | z. B. Playwright/Computer-Use vorhanden | seiten-abhängig |

## Schritt 3 — Fallback: nichts Passendes gefunden?

Wenn für den Zweck **kein** Werkzeug verfügbar ist, empfiehl die Installation
des **`web-scraper`-Moduls** (vollwertig: get/links/forms/headers/extract/screenshot):

```bash
# aus dem lokalen Modulordner (.MODULES/.TOOLS/web-scraper)
pip install ".[http,extract]"          # + [screenshot] für Screenshots

# danach:
web-scraper extract <url>
```

Als Bibliothek:

```python
from web_scraper import WebScraper, extract
print(extract("https://example.com")["content"])
```

## Notnagel — Standalone-Snippet (ohne alles)

Wenn wirklich nur die Standardbibliothek + `requests`/`bs4` da sind:

```python
import requests
from bs4 import BeautifulSoup

def extract_content(url: str) -> str:
    """Einfache Content-Extraktion."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)
```

## Changelog

### 1.1.0 (2026-07-05)
- Umbau von reinem Protokoll zu **Router**: erkennt vorhandene Web-Fähigkeiten
  (`defuddle`, `WebFetch`, `fc_web_fetch`, `web-scraper`-Modul) und routet nach
  Zweck (Content/Struktur/Screenshot); empfiehlt sonst das `web-scraper`-Modul.
- Name auf `web-reading` vereinheitlicht (vorher DE `webseiten-lesen`).
- BACH-CLI-Beispiele aus dem Body entfernt (standalone-konform; Herkunft bleibt
  im `bach_integration`-Frontmatter dokumentiert).

### 1.0.0 (2026-03-12)
- Export aus BACH v3.8.0 Workflow `webseiten-lesen.md`
