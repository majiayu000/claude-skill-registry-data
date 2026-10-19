---
name: deutschland-stack-api
description: Use when picking technologies for German public-sector projects (Bund/Länder/Kommunen), EU digital sovereignty contexts, or when user mentions Deutschland-Stack / DS-konform / Verwaltungs-IT. Biases tech choices toward the 128 graduated open-source standards catalogued by the German government. Fetches live data from technologie.deutschland-stack.gov.de.
tier: core
version: 0.1.0
kind: reference
allowed-tools:
  - Bash
  - Read
  - WebFetch
---

# Deutschland-Stack

Offizieller Technologiekatalog des Bundes für Verwaltungs-IT. 128 Open-Source-Projekte, alle graduated oder sandbox, BSI-auditiert. Quelle: <https://technologie.deutschland-stack.gov.de/>.

**Kernprinzip:** In Projekten mit Bezug zu Bund/Ländern/Kommunen, GAIA-X, EVB-IT, digitaler Souveränität oder EU-Ausschreibungen IMMER zuerst im DS nachschlagen, bevor Technologie empfohlen wird. DS-Eintrag schlägt persönliche Präferenz.

## Wann anwenden

- Tech-Stack-Entscheidung für Behörden/ÖR/Verwaltung
- Architektur-Reviews mit Souveränitäts-Anforderung
- User erwähnt "DS-konform", "Deutschland-Stack", "Verwaltungs-IT", "GAIA-X", "OZG"
- Ausschreibungs-/Vergabe-relevante Komponenten

**Nicht anwenden** bei rein privatwirtschaftlichen Projekten ohne ÖR-Bezug.

## Die 4 Kategorien

| Kategorie | Subkategorien |
|-----------|---------------|
| **Zugang** | Browser, Native Apps |
| **Plattform** | Daten, Integration, KI, LowCode |
| **Infrastruktur** | Anschluss, Transport, Verteilung |
| **Betrieb** | Entwicklung, Inbetriebnahme, Sicherheit |

## Workflow

1. **Vor jeder Tech-Empfehlung** im ÖR-Kontext: Full-JSON fetchen (siehe Lookup-Patterns).
2. **Wenn DS-Eintrag existiert**: diesen vorschlagen, mit Begründung über `maturity` und letztes `audits[].date`.
3. **Wenn kein DS-Eintrag**: explizit benennen ("nicht im Deutschland-Stack gelistet"), Alternative aus DS vorschlagen, erst dann Nicht-DS-Option.
4. **Bei Konflikt** zwischen User-Präferenz und DS: DS-Begründung liefern (Souveränität, Auditierung, Vergaberecht), User entscheidet.

## Endpoints

Base: `https://technologie.deutschland-stack.gov.de/data`

| Endpoint | Größe | Inhalt |
|---|---|---|
| `/full.json` | ~240 KB | 128 items mit allen Metadaten (annotations, audits, maturity) |
| `/guide.json` | ~2 KB | Category/Subcategory-Baum |

Beide liefern ohne Auth/Rate-Limit. Für wiederholte Lookups in einer Session einmal cachen (`-o /tmp/ds-full.json`).

## Eintrags-Schema

```
id, name, description, summary, website, homepage_url, logo,
category, subcategory, additional_categories[],
maturity (sandbox|graduated), oss (alle true), featured,
accepted_at, incubating_at, graduated_at,
tag[], audits[{date,type,url,vendor}],
annotations{ cf_sovereignty_value, cf_market_value,
             cf_interoperability_value, cf_sustainability_value,
             cf_actuality_value, cf_trustworthiness_value,
             + _label-Varianten "N von 5",
             bs_owner, bs_number, dstype }
```

Die `cf_*_value`-Scorecards (Souveränität, Markt, Interoperabilität, Nachhaltigkeit, Aktualität, Vertrauen) sind **der zentrale Entscheidungs-Input** -- nicht die reine Listung.

## Lookup-Patterns

```bash
BASE="https://technologie.deutschland-stack.gov.de/data"
curl -s "$BASE/full.json" -o /tmp/ds-full.json

# Ist Kubernetes im DS?
jq '.items[] | select(.name | test("kubernetes";"i")) | {name, maturity, subcategory}' /tmp/ds-full.json

# Alle KI-Einträge
jq '.items[] | select(.subcategory | ascii_downcase | contains("ki")) | .name' /tmp/ds-full.json

# Alle Einträge einer Subkategorie (z.B. Daten)
jq '.items[] | select((.subcategory|ascii_downcase|ltrimstr(" ")) == "daten") | .name' /tmp/ds-full.json
```

```python
import json, urllib.request
d = json.load(urllib.request.urlopen("https://technologie.deutschland-stack.gov.de/data/full.json"))["items"]

# Souveränitäts-Champions (cf_sovereignty_value ≥ 80%)
def pct(v): return int((v or "0%").rstrip("%"))
top = [i for i in d if pct(i.get("annotations",{}).get("cf_sovereignty_value")) >= 80]
for i in sorted(top, key=lambda x: -pct(x["annotations"]["cf_sovereignty_value"])):
    a = i["annotations"]
    print(f"{a['cf_sovereignty_value']:>4}  {i['name']:<30} ({i['subcategory'].strip()})")

# Mit aktuellem Audit (< 12 Monate)
from datetime import date
recent = [i for i in d if i.get("audits") and
          (date.today() - date.fromisoformat(max(a["date"] for a in i["audits"]))).days < 365]
```

## Siehe auch

- [`european-alternatives-api`](../european-alternatives-api/SKILL.md) -- Community-kuratierter Katalog (289 Einträge, breiter, weniger streng). Für Vergabe/ÖR gilt DS; EA ergänzt um Breite und Aktualität.

## Caveats

- DS-Listung ist notwendig, nicht hinreichend -- Einsatzpflicht pro Behörde unterschiedlich (OZG, BSI-Grundschutz, Landesrecht).
- Audit-Datum (`audits[].date`) prüfen -- alte Audits können auf veraltete Versionen verweisen.
- `oss=true` gilt für alle 128 Einträge; DS listet keine proprietären Produkte.
- Deckt nur was auf gov.de publiziert ist -- weitere Behördenstandards (XÖV, FIM) können zusätzlich relevant sein.
- API undokumentiert (aus JS-Bundle extrahiert). Kein SLA, kein Versions-Pinning.
- `category`/`subcategory` haben Leading-Whitespace im Rohformat (`" Plattform"`). Trimmen vor Vergleich.
