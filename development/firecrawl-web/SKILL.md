---
name: firecrawl-web
description: >-
  Web-Scraping, Screenshots, strukturierte Daten-Extraktion, Web-Search und Crawling via Firecrawl API. Nutzen bei aktuellen Web-Infos, URL-Scraping, Screenshots oder Framework-Dokumentation.
metadata:
  author: BexTuychiev
  version: 1.0
lane: worker-flash
reasoning_effort: high
agent: Researcher
routing_hint: |
  **Agent-Scope:** Deep-research, fact-checking, paper-search, knowledge-base. Off-scope: code-building, visual design, writing — return to Yuno.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# Firecrawl Web Skill

Web-Zugriff via Firecrawl API — Screenshots, Markdown-Extraktion, strukturierte Daten, Crawling.

## Script

Das Skill bringt `fc.py` mit:
```

set -euo pipefail
~/.hermes/.agents/skills/firecrawl-web/fc.py
```

## Commands

```bash

set -euo pipefail
# Webseite als Markdown
python3 ~/.hermes/.agents/skills/firecrawl-web/fc.py markdown "https://example.com"

# Nur Main-Content (ohne Nav/Footer)
python3 ~/.hermes/.agents/skills/firecrawl-web/fc.py markdown "https://example.com" --main-only

# Screenshot
python3 ~/.hermes/.agents/skills/firecrawl-web/fc.py screenshot "https://example.com"

# Strukturierte Daten extrahieren
python3 ~/.hermes/.agents/skills/firecrawl-web/fc.py extract "https://example.com"

# Web-Search
python3 ~/.hermes/.agents/skills/firecrawl-web/fc.py search "query"

# Dokumentation crawlen
python3 ~/.hermes/.agents/skills/firecrawl-web/fc.py crawl "https://docs.example.com"
```

## Hinweis für Hermes

Firecrawl braucht einen API-Key. Ohne Key nutze die eingebauten Hermes-Tools:
- `web_extract` für Webseiten → Markdown
- `web_search` für Suche
- `browser` für interaktive Seiten
- `browser_get_images` für Screenshots

Das Firecrawl-Skill ist primär für OpenCode gedacht. Für Hermes reichen die Built-in-Tools in den meisten Fällen.
