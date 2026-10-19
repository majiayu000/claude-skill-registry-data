---
name: european-alternatives-api
description: Use when picking software for EU customers, GDPR-driven replacements, digital-sovereignty contexts, or when user asks for the European / open-source version of a US product (Google Drive, Dropbox, Slack, …). Biases tech choices toward the 289 community-curated alternatives at european-alternatives.cloud. Fetches live data. Complements deutschland-stack-api (community-curated vs. government-graduated).
tier: core
version: 0.1.0
kind: reference
allowed-tools:
  - Bash
  - Read
  - WebFetch
---

# European Alternatives

Community-kuratierter Katalog unter <https://european-alternatives.cloud/en>. 289 Einträge über 46 Kategorien, überwiegend DE/CH/FR/NL. Quelle: <https://github.com/TheMorpheus407/european-alternatives>.

**Kernprinzip:** Wenn für ein US-Produkt eine europäische oder Open-Source-Alternative gesucht wird, zuerst hier nachschlagen. Für Behörden-/Vergabe-Kontexte hat [`deutschland-stack-api`](../deutschland-stack-api/SKILL.md) Vorrang; EA ergänzt um Breite und Aktualität.

## Wann anwenden

- User fragt nach einer EU-/OSS-Alternative zu einem konkreten US-Produkt
- Tech-Stack-Pick mit GDPR- oder EU-Data-Residency-Anforderung
- Cross-Check des Deutschland-Stack mit Community-View (DS = staatlich graduated; EA = community, breiter, weniger streng)
- Audits der Form "was ersetzt X, und wer ersetzt es noch"

**Nicht anwenden** für reines Web-Scraping der Seite -- die API liefert dieselben Daten strukturiert.

## Endpoints

Base: `https://european-alternatives.cloud/api/catalog`

| Endpoint | Größe | Inhalt |
|---|---|---|
| `/categories` | ~9 KB | 46 Kategorien mit `usGiants` und `alternativeCount` |
| `/entries?status=alternative` | ~1.9 MB | 289 Alternativen (full database) |
| `/entries?status=us` | ~700 KB | 109 US-Originale, die ersetzt werden |
| `/entries?status=denied` | ~50 KB | 18 abgelehnte Einträge mit Begründung |
| `/landing-groups` | ~1 KB | Kategorie-Cluster (privacy-security, communication-work, …) |
| `/further-reading` | ~1 KB | Weitere Verzeichnisse (european-alternatives.eu, Privacy Guides, PRISM Break) |

Alle liefern `{"data": [...]}`. Keine Pagination, keine Auth. Für wiederholte Lookups in einer Session einmal cachen (`-o /tmp/ea-alts.json`).

## Eintrags-Schema (Alternativen)

```
id, name, description, website, logo, country (ISO-2 / "oss"),
category, replacesUS[], isOpenSource, pricing (free|freemium|paid),
tags[], openSourceLevel, openSourceAuditUrl, sourceCodeUrl,
headquartersCity, license, dateAdded, localizedDescriptions{},
reservations[], positiveSignals[], trustScore (0-100),
trustScoreStatus, trustScoreBreakdown{}
```

US-Einträge lassen OSS-Felder weg; denied-Einträge haben zusätzlich `deniedDecision`.

## Lookup-Patterns

```bash
BASE="https://european-alternatives.cloud/api/catalog"

# 1. List all categories with counts
curl -s "$BASE/categories" | jq -r '.data[] | "\(.alternativeCount)\t\(.name)\t\(.usGiants | join(", "))"'

# 2. Find what replaces a specific US product (by id, e.g. "google-drive")
curl -s "$BASE/entries?status=alternative" \
  | jq '.data[] | select(.replacesUS | index("google-drive")) | {name, country, website, isOpenSource, trustScore}'

# 3. All alternatives in a category (e.g. "email")
curl -s "$BASE/entries?status=alternative" \
  | jq '.data[] | select(.category=="email") | {name, country, pricing, trustScore}'

# 4. Open-source only, filtered by country
curl -s "$BASE/entries?status=alternative" \
  | jq '.data[] | select(.isOpenSource==true and .country=="de") | .name'

# 5. Cache the full alternatives JSON locally (re-fetch occasionally -- community catalog grows)
curl -s "$BASE/entries?status=alternative" -o /tmp/ea-alts.json
```

For richer filtering (multi-field, sort by trustScore, joins with categories), use Python:

```python
import json, urllib.request
B = "https://european-alternatives.cloud/api/catalog"
alts = json.load(urllib.request.urlopen(f"{B}/entries?status=alternative"))["data"]
cats = {c["id"]: c for c in json.load(urllib.request.urlopen(f"{B}/categories"))["data"]}

# Top-trust EU-hosted LLM alternatives
llm = [a for a in alts if a["category"] == "large-language-models" and a["country"] != "us"]
for a in sorted(llm, key=lambda x: -(x.get("trustScore") or 0))[:5]:
    print(f"{a['trustScore']:>3}  {a['name']:<25} ({a['country']}) -- {a['website']}")
```

## Siehe auch

- [`deutschland-stack-api`](../deutschland-stack-api/SKILL.md) -- Staatlich graduated/auditiert, enger Scope, Vergabe-relevant. Bei ÖR-Kontext hat DS Vorrang; EA ergänzt um Breite und Aktualität.

## Caveats

- API ist undokumentiert (aus JS-Bundle extrahiert). Kein SLA, kein Versions-Pinning.
- `country` nutzt ISO-2 plus den Literal `"oss"` für vendor-neutrale OSS-Projekte.
- `trustScore` ist Community-abgeleitet -- `trustScoreBreakdown` lesen, bevor er zitiert wird.
- Für Sessions mit vielen Filter-Queries die Alternativen-JSON einmal cachen -- 1.9 MB pro Call summiert sich.
- Community-Katalog wächst -- gelegentlich neu fetchen.
