---
name: reviewen
description: Start de rapport_reviewen workflow. Gebruik dit wanneer de gebruiker een rapport of sectie wil laten nakijken op taal, APA, humanisering en structuur. Activeer proactief bij vragen als "check dit rapport", "nakijken", "review", "klaar voor inlevering?", "controleer mijn tekst".
model: sonnet
---

Je voert de `rapport_reviewen.md` workflow uit.

## Uitvoering

1. Lees `workflows/rapport_reviewen.md` volledig met de Read tool
2. Volg ALLE stappen en domeinen uit die workflow in volgorde — sla GEEN stap over
3. Bij twijfel over een stap: lees de workflow opnieuw

## Constraints (altijd van kracht)

- Lees ALLE gidsen die in de workflow genoemd worden met de Read tool — "raadpleeg" is niet voldoende
- Alle vier reviewdomeinen zijn VERPLICHT bij een volledige review
- Domein 5 (Inlevereisen & Beoordelingscriteria) is OPTIONEEL — wordt alleen uitgevoerd als config-bestanden bestaan voor de actieve vakcode
- Tools gemarkeerd als [VERPLICHT] MOETEN worden uitgevoerd via Bash
- Een tool die een fout geeft: rapporteer de fout, maar sla de tool NIET over
- De verificatiechecklist aan het einde MOET volledig worden doorlopen
- `history_writer.py` + `generate_report_pdf.py` zijn ALTIJD de laatste stappen
- Output gaat naar `.tmp/reviewen/<titel>.pdf`
- Presenteer een korte samenvatting in de chat (NIET het volledige rapport)
- Werkbestanden in `.tmp/` root worden na afloop opgeruimd

## Verificatiechecklist [VERPLICHT]

Bevestig intern dat ALLE stappen zijn uitgevoerd:

- [ ] Alle 5 gidsen gelezen met Read tool (taal, apa, humanize_nl, academische_stijl, schrijfstijl)
- [ ] Domein 1: grammar_check.py uitgevoerd + taalcheck handmatig
- [ ] Domein 2: apa_checker.py uitgevoerd + APA-check handmatig
- [ ] Domein 3: humanizer_nl.py + readability_nl.py + tekst-analist uitgevoerd
- [ ] Domein 4: structuurcheck handmatig uitgevoerd
- [ ] Domein 5: quick scan + beoordelingscriteria gecontroleerd (indien geladen)
- [ ] generate_review_chart.py + generate_report_pdf.py uitgevoerd
- [ ] history_writer.py uitgevoerd → .tmp/reviewen/<titel>.pdf
- [ ] Korte samenvatting in de chat gepresenteerd
- [ ] Werkbestanden in .tmp/ root opgeruimd
