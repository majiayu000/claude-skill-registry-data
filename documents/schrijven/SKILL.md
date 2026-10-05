---
name: schrijven
description: Start de rapport_schrijven workflow. Gebruik dit wanneer de gebruiker nieuwe academische tekst wil schrijven (inleiding, methode, resultaten, discussie, conclusie of volledig rapport). Activeer proactief bij vragen als "schrijf een...", "maak een sectie over...", "stel een inleiding op...".
model: sonnet
---

Je voert de `rapport_schrijven.md` workflow uit.

## Uitvoering

1. Lees `workflows/rapport_schrijven.md` volledig met de Read tool
2. Volg ALLE stappen uit die workflow in volgorde — sla GEEN stap over
3. Bij twijfel over een stap: lees de workflow opnieuw

## Constraints (altijd van kracht)

- Lees ALLE gidsen die in de workflow genoemd worden met de Read tool — "raadpleeg" is niet voldoende
- Tools gemarkeerd als [VERPLICHT] MOETEN worden uitgevoerd via Bash
- Een tool die een fout geeft: rapporteer de fout, maar sla de tool NIET over
- De verificatiechecklist aan het einde MOET volledig worden doorlopen
- `history_writer.py` + `md_to_docx.py` zijn ALTIJD de laatste stappen
- Output gaat naar `.tmp/schrijven/<titel>.docx`
- Werkbestanden in `.tmp/` root worden na afloop opgeruimd

## Verificatiechecklist [VERPLICHT]

Bevestig intern dat ALLE stappen zijn uitgevoerd:

- [ ] Alle 5 gidsen gelezen met Read tool (apa_nl, academische_stijl, taal, humanize_nl, schrijfstijl)
- [ ] grammar_check.py + apa_checker.py uitgevoerd
- [ ] humanizer_nl.py --suggest + readability_nl.py uitgevoerd
- [ ] tekst-analist subagent aangeroepen (of fallback bij falen)
- [ ] generate_review_chart.py uitgevoerd
- [ ] Risicobeoordeling laag, of tekst herschreven bij gemiddeld/hoog
- [ ] history_writer.py + md_to_docx.py uitgevoerd → .tmp/schrijven/<titel>.docx
- [ ] Werkbestanden in .tmp/ root opgeruimd
