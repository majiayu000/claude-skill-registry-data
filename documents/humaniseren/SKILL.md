---
name: humaniseren
description: >-
  Maakt tekst die als AI klinkt menselijker, in de stem van de gebruiker, zonder de inhoud te veranderen. Haalt
  de AI-patronen van 2026 eruit, in het Nederlands en het Engels: woordkeus per modelgeneratie, clusters,
  niet-X-maar-Y, formules, gelijk of overgecorrigeerd ritme, LinkedIn-formules. Een feitencontrole bewaakt dat
  geen feit, getal, citaat of bron verandert. Kan ook alleen analyseren (scan). Gebruik bij
  /dutchquill:humaniseren, of als de gebruiker vraagt een tekst menselijker of natuurlijker te maken, minder als
  AI te laten klinken, of op AI-patronen te checken ("klinkt dit als ChatGPT?", "maak dit menselijker",
  "humanize this", "does this sound like AI").
argument-hint: "[tekst of pad] [scan | herschrijf]"
when_to_use: >-
  Gebruik deze skill ook als de gebruiker DutchQuill niet noemt: bij elke vraag of een tekst als AI of ChatGPT
  klinkt, of hij door AI geschreven lijkt, of de vraag een tekst natuurlijker, menselijker of minder robotachtig
  te maken. Ook in het Engels ("does this sound like AI", "humanize").
---

# Humaniseren

Opdracht: $ARGUMENTS

Elk `dq`-commando draai je via Bash met dit voorvoegsel; hieronder staat het als `DQ`:

```bash
CLAUDE_PLUGIN_DATA="${CLAUDE_PLUGIN_DATA}" "${CLAUDE_PLUGIN_ROOT}/scripts/dq"
```

## Stand

!`DQ_NIET_INSTALLEREN=1 CLAUDE_PLUGIN_DATA="${CLAUDE_PLUGIN_DATA}" "${CLAUDE_PLUGIN_ROOT}/scripts/dq" config toon --kort 2>&1 | tail -10 || true`

## Stappen

1. **Lees de werkwijze** (`${CLAUDE_PLUGIN_ROOT}/gidsen/werkwijze/basis.md`) en de humaniseergids van de taal
   van de tekst: `DQ gids pad nl/humaniseren` of `DQ gids pad en/humanize`. Lees de gids helemaal; die is het
   eigenlijke werk.
2. **Modus.**
   - **scan**: als de gebruiker vraagt of iets als AI klinkt, of om een check. Je analyseert en verandert niets.
   - **herschrijf**: de standaard als er om "menselijker maken" wordt gevraagd.
3. **Tekst en genre.** Geplakt, een pad (`DQ extraheer` voor .docx of .pdf), of uit de werkmap. Bepaal het
   genre; dat bepaalt de drempels. Sla het origineel op als `origineel.md` (`.dutchquill/tmp/` of de versiemap).
4. **Stem.**
   - Lees het stemprofiel als het er is (`DQ gids voor` toont `stemprofiel` en `stem_json`).
   - Staan er teksten in `mijn-stijl` maar is er nog geen `stem.json`: draai `DQ stem analyse`.
   - Is er niets van de gebruiker zelf, dan volg je genre en toon. Zeg dat in één regel: met een paar eigen
     teksten in `mijn-stijl` wordt het resultaat persoonlijker.
5. **Analyse:** `DQ tells --input <origineel> --genre <genre>`. Meldt het een korte tekst (onder 100 woorden),
   zeg dan in de chat dat de score weinig zegt en oordeel vooral op wat je zelf leest. Lees daarna zelf de
   categorieën uit de gids na die het script niet ziet:
   - een gezegde dat diep klinkt;
   - opgeblazen belang;
   - de verkeerde lezer;
   - tekst over de tekst;
   - of het specifiek genoeg is.
6. **Scan: rapporteer, log en stop.** Log de scan: `DQ historie log --actie humaniseren --titel "<titel>"
   --tekst <origineel> --meta '{"modus": "scan", "niveau": "<niveau>"}'`. Geef het niveau, de vijf belangrijkste patronen met een voorbeeld uit de tekst
   en een alternatief, en wat goed is aan de tekst. Bij een document mag dit ook als bestand
   (`2-output/humaniseren/<titel>/vN/`): maak eerst het overzichtsbeeld met `DQ reviewgrafiek --input <origineel>
   --genre <genre> --titel "<titel>" --output <map>/overzicht.png`, zet het als `![Overzicht](overzicht.png)`
   bovenaan `bron.md`, en exporteer met `DQ export --bron <map>/bron.md --naam "Scan <titel>" --template review`.
7. **Herschrijf.**
   - Werk volgens sectie 1 van de gids: sterke patronen eerst, en verander niet meer dan nodig.
   - Respecteer "Wanneer niet ingrijpen".
   - Maak specifiek met wat in de tekst of het materiaal staat. Verzin niets; zet `[voorbeeld nodig]` waar
     een concreet detail de tekst beter zou maken.
8. **Controle**, verplicht:
   - `DQ tells --compare <origineel> <concept> --genre <genre>`
   - `DQ feiten --origineel <origineel> --nieuw <concept>`: herstel elk verloren of nieuw feit.
   - Controleer of je niet overgecorrigeerd hebt (alleen korte zinnen, alles met punten).
   - Hooguit drie rondes.
9. **Uitvoer** (werkwijze 6 en 7).
   - Chat: de nieuwe tekst, plus één regel met de score voor en na.
   - Document: een nieuwe versie in `2-output/humaniseren/<titel>/` (komt de tekst uit `2-output/`, dan met
     `DQ versie volgende --van "<pad>"` als vN+1 in dezelfde titelmap), en in `wat-is-er-veranderd.md` per
     patroongroep wat er aangepast is.

## Klaar als

- [ ] De gids is gelezen, en de stem is gebruikt als die er is.
- [ ] De feitencontrole is schoon of elk verschil is verklaard.
- [ ] Het niveau is laag, of het restant is uitgelegd (bijvoorbeeld vaktermen of de eigen stijl van de gebruiker).
- [ ] Niets verzonnen, niets binnen citaten veranderd.
- [ ] De taalronde (werkwijze 5) is gedaan, als laatste stap; citaten blijven zoals ze zijn.
