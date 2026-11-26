---
name: schrijven
description: >-
  Schrijft nieuwe tekst in het Nederlands of Engels, in de toon en met de controles die de gebruiker koos:
  hbo-rapporten (APA), onderzoeks- en adviesrapporten, zakelijke rapporten, procesdocumenten (SOP),
  research-notities, memo's, mails, LinkedIn- en andere social posts, README's en korte teksten. Gebruikt het
  materiaal in de DutchQuill-werkmap (notities, rapporten, beelden, bronnen). Mails, posts en korte teksten komen
  in de chat, documenten als bestand met versies. Gebruik bij /dutchquill:schrijven, of als de gebruiker vraagt
  om een tekst te schrijven, op te stellen of te maken ("schrijf een mail aan", "maak een rapport van mijn
  notities", "write a LinkedIn post about", "draft a README").
argument-hint: "[wat je wilt laten schrijven]"
when_to_use: >-
  Gebruik deze skill ook als de gebruiker DutchQuill niet noemt: bij elk verzoek om een tekst voor iemand anders te
  schrijven of op te stellen, hoe kort ook (een mail of antwoord op een mail, een bericht aan een collega, een
  LinkedIn- of social post, een bio, een rapport, een README). Ook in het Engels ("write", "draft", "compose").
  Niet voor code, commit messages of uitleg in de chat zelf.
---

# Schrijven

Opdracht: $ARGUMENTS

Elk `dq`-commando draai je via Bash met dit voorvoegsel; hieronder staat het als `DQ`:

```bash
CLAUDE_PLUGIN_DATA="${CLAUDE_PLUGIN_DATA}" "${CLAUDE_PLUGIN_ROOT}/scripts/dq"
```

## Stand

!`DQ_NIET_INSTALLEREN=1 CLAUDE_PLUGIN_DATA="${CLAUDE_PLUGIN_DATA}" "${CLAUDE_PLUGIN_ROOT}/scripts/dq" config toon --kort 2>&1 | tail -10 || true`

## Stappen

1. **Lees de werkwijze:** `${CLAUDE_PLUGIN_ROOT}/gidsen/werkwijze/basis.md`. Gaat het om een bestand, lees dan
   ook `${CLAUDE_PLUGIN_ROOT}/gidsen/werkwijze/markdown.md`.
2. **Genre, config en uitvoer** (werkwijze 1). Is de opdracht te dun om te schrijven, stel dan in één keer de
   vragen die je echt nodig hebt (doel, lezer, kernboodschap, lengte). Bij een mail of post is de
   opdracht meestal genoeg: schrijf, en zeg wat je aannam.
3. **Gidsen lezen** (werkwijze 2): alles uit `DQ gids voor --genre <genre>`, plus het genre-sjabloon. Werkt `dq`
   niet, lees dan rechtstreeks `${CLAUDE_PLUGIN_ROOT}/templates/genres/<genre>.md` (het sjabloon),
   `${CLAUDE_PLUGIN_ROOT}/gidsen/toon.md` en `${CLAUDE_PLUGIN_ROOT}/gidsen/nl/kern.md` (Engels:
   `gidsen/en/style.md`). Schrijf nooit zonder het genre-sjabloon gelezen te hebben.
4. **Materiaal** (werkwijze 3), als de opdracht erom vraagt of naar de werkmap verwijst.
   **Titelpagina (profiel student, of APA aan, bij een document).** Vraag vóór de opzet in één bericht of de
   gegevens kloppen: "Ik gebruik deze gegevens voor de titelpagina: naam, studentnummer, instelling, opleiding,
   vak, docent(en), opleidingsniveau. Klopt dit voor dit rapport?" Haal ze uit `DQ config toon` (`student`).
   Staan er meer vakken in het profiel, vraag dan welk vak het is (`DQ vak lijst`). Wat de gebruiker kiest of
   verandert, zet je in de frontmatter van `bron.md` (`vak: Naam (CODE)`, `begeleider: ...`, `naam: ...`); de
   frontmatter gaat voor het profiel. Ontbreekt er iets, laat het dan leeg in plaats van het te raden. Het
   opleidingsniveau (`student.niveau`) bepaalt de diepgang: zie de tabel bovenaan `academische-stijl.md`.
5. **Opzet (alleen bij documenten).** Laat een korte opzet zien: koppen met per kop één regel over de inhoud, de
   figuren met hun plek, en wat er nog ontbreekt. Wacht op akkoord of aanpassingen. Bij chat-uitvoer sla je
   deze stap over.
6. **Schrijven.**
   - In de stem van de gebruiker (stemprofiel) en de toon uit de config.
   - Volgens het genre-sjabloon en `kern.md`.
   - Gebruik alleen feiten uit het materiaal of van de gebruiker. Wat ontbreekt, markeer je als `[bron nodig]`,
     `[cijfer nodig]` of `[voorbeeld nodig]`.
   - Ook kleur en sfeer zijn feiten: avonden en weekenden, een tijdstip, wat iemand voelde of dacht, hoe iets ging.
     Staat het niet in de vraag of het materiaal, dan schrijf je het niet. Een korte post mag kort blijven.
   - Ook een persoonlijke les, mening of ervaring is een feit. Leid die niet af uit wat de gebruiker gaf; zet
     `[voorbeeld nodig]` of laat het weg. Moet je een zin als aanname melden, dan hoort hij niet in de tekst.
     (Een conclusie die uit het materiaal volgt, zoals in een rapport, valt hier niet onder.)
   - Beelden uit het materiaal zet je op de plek waar de tekst erover gaat, met een bijschrift en een
     verwijzing in de tekst (markdown.md).
   - Bevat het materiaal cijfers die een grafiek waard zijn, maak er dan een:
     `DQ grafiek --type bar|timeline|comparison|donut --data '<json>' --output <map>/grafiek-1.png`.
     Een proces of architectuur: `DQ diagram --type flow|architecture|layers --data '<json>' --output ...`.
     `DQ grafiek --help` toont het JSON-formaat.
   - Is het document langer dan ± 1500 woorden, schrijf het dan hoofdstuk voor hoofdstuk in `bron.md`. Begin
     met een paar alinea's en voeg toe.
   - **Bronnen (als APA aan staat):** verwerk de bronvermelding tijdens het schrijven, niet achteraf. Heb je de
     gegevens van een bron (auteurs, jaar, titel, uitgever, url) maar nog geen opgemaakte regel, laat
     `DQ apa-bron --input <bronnen.json>` de literatuurregel en de verwijzing in de tekst maken (15 brontypen;
     `DQ apa-bron --help-schema` toont het formaat). Ontbreekt een gegeven, vraag het of zet `[bron nodig]`.
   - Voorwoord, begrippenlijst en reflectie alleen als de opdracht of de gebruiker erom vraagt (zie het
     genre-sjabloon). De verdeling van de woorden per hoofdstuk staat in het sjabloon.
7. **Controles en herstellus** (werkwijze 5).
8. **Opslaan en exporteren** (werkwijze 6), of de tekst in de chat (werkwijze 7).
9. **Bij het profiel student:** een tekst die DutchQuill schrijft is altijd AI-gebruik. Bied daarom bij elk
   document een AI-verantwoording en de bronvermelding van de chat aan, volgens `ai-gebruik.md`. Vul alleen in
   wat de gebruiker en jij echt hebben gedaan.

## Varianten

- **"Geef me drie versies"** (vooral posts en mails): maak versies die echt verschillen in opening, lengte of
  invalshoek, niet drie keer dezelfde tekst.
- **Antwoord op een mail:** de gebruiker plakt de mail. Beantwoord elke vraag, neem de aanspreekvorm over, en
  maak het niet langer dan de mail zelf, tenzij het onderwerp dat vraagt.
- **Een hoofdstuk of sectie** van een bestaand rapport: lees het rapport eerst (`DQ extraheer`), schrijf in
  dezelfde stijl en zet het resultaat als nieuwe versie in `schrijven/<titel>/`.

## Klaar als

- [ ] De werkwijze en alle gidsen uit `DQ gids voor` zijn gelezen.
- [ ] De controles zijn gedraaid. Het tells-niveau is laag, of het restant is uitgelegd.
- [ ] De taalronde (werkwijze 5) is gedaan, als laatste stap.
- [ ] Er is geen verzonnen feit, cijfer, bron of voorbeeld in de tekst; open plekken zijn gemarkeerd.
- [ ] Profiel student: de gegevens voor de titelpagina zijn bevestigd en de AI-verantwoording is aangeboden.
- [ ] Chat: de tekst, de regel "Taalronde: ..." en hooguit twee regels toelichting. Bestand: `bron.md`, de exports,
  `wat-is-er-veranderd.md` en een historieregel.
