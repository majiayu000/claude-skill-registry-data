---
name: grading
description: "Systematisk bedömning av poängprov enligt etablerad metodik. Guidar genom hela processen från förberedelser till kvalitetskontroll. Använd denna skill när du behöver rätta prov, bedöma elevsvar, sammanställa poäng, eller när användaren frågar om provbedömning eller rättning."
allowed-tools: []
---

# Poängprovsbedömning med rättningsmall

Systematisk bedömning av poängprov enligt etablerad metodik. Denna Skill guidar dig genom hela bedömningsprocessen från förberedelser till slutlig kvalitetskontroll.

## KRITISK PRINCIP

**Bedöm ALLA elever för EN fråga åt gången - ALDRIG alla frågor för en elev.**

Detta säkerställer:
- Rättvis bedömning (du ser hela variationen samtidigt)
- Konsekvent standard (direkt jämförelse mellan svar)
- Undvikande av drift (bedömningen blir inte strängare/mildare)
- Kalibrering (du ser skillnaden mellan olika poängnivåer)

## Steg 1: Förberedelser

### 1.1 Läs provinstruktioner
```
Read: medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/provinstruktion.md
```

**Kritiska punkter att notera:**
- Hur många frågor ska besvaras i varje del?
- Finns det specialfall (t.ex. "5 av 6 frågor")?
- Vad krävs för full poäng i essäfrågor?
- Ordgränser och strukturkrav?

### 1.2 Läs bedömningskriterier (facit)
```
Read: medier-samhälle-och-kommunikation-1/prov-radio-tv-i-sverige/facit.md
```

**För varje fråga, dokumentera:**
- Maxpoäng
- Krav för full poäng
- Krav för godkänt
- Gränser för underkänt
- Nyckelelement som MÅSTE finnas

### 1.3 Verifiera parsern
```
Bash: pdm run python scripts/grading/verify_parser.py
```

**Kontrollera att:**
- Alla elever parsas korrekt
- Antalet besvarade frågor stämmer
- Inga tekniska fel uppstått

## Steg 2: Systematisk bedömning fråga för fråga

### 2.1 Starta graderingsassistenten
```
Bash: pdm run python scripts/grading/manual_grading_assistant.py
```

Detta verktyg visar alla elevsvar per fråga så du kan jämföra direkt.

### 2.2 Bedömningsprocess för varje fråga

**KRITISKT: För VARJE FRÅGA (A1, A2, ..., B, C):**

#### Fas 1: Förberedelse
1. Läs bedömningskriterierna från graderingsassistenten
2. Identifiera nyckelelement för full poäng
3. Notera skillnader mellan olika poängnivåer (t.ex. 6p vs 5p vs 4p)

#### Fas 2: Första genomläsningen
1. Läs ALLA elevsvar på denna fråga
2. Anteckna preliminära intryck:
   - Vilka svar är tydligt starka (full poäng)?
   - Vilka är i mittenområdet?
   - Vilka är svaga?

#### Fas 3: Detaljerad bedömning
För varje elev:

1. **Checklista mot kriterier:**
   - [ ] Komponent 1 finns?
   - [ ] Komponent 2 finns?
   - [ ] Förklaringar tydliga?
   - [ ] Exempel/konkretisering?

2. **Tilldela poäng:**
   - Jämför mot andra elevsvar du precis läst
   - Använd kriterierna strikt
   - Motivera varje poäng

3. **Dokumentera:**
   ```
   [Elevnamn] ([poäng]p): [Kort motivering]
   ```

#### Fas 4: Kvalitetskontroll för frågan
- Har du använt hela poängskalan?
- Är poängen konsekvent med kriterierna?
- Kan du försvara varför elev X fick mer/mindre än elev Y?

## Steg 3: Specialfall

### Del A: "Välj 5 av 6 frågor"
- Om eleven besvarar färre än 5: Förlorade poäng för obesvarade
- Om eleven besvarar alla 6: Rätta alla 6, summera totalt
- Maxpoäng Del A kan överstiga teoretisk max om eleven besvarar extra frågor

### Del B: "ALLA tre aspekter krävs för full poäng"
**Kontrollera noggrant från provinstruktion:**
- Hur många aspekter krävs för full poäng?
- Räcker det med "minst två" för godkänt?

**Bedöm metodiskt:**
- Identifiera vilka aspekter eleven behandlat
- Kontrollera orsakssamband och djup
- Tilldela poäng enligt facit

### Del C: Essäfråga med struktur
**Bedöm i fyra dimensioner:**
1. **Inledning**: Historisk kontext, bakgrund
2. **Huvuddel**: För- OCH nackdelar, balanserad diskussion
3. **Avslutning**: Syntes, koppling mellan historia och nutid
4. **Struktur**: Tydlig essästruktur, språkkvalitet

**Kontrollera ordgränser:**
- Notera om eleven är under/över gränsen
- Bedöm enligt facit om detta påverkar poäng

## Steg 4: Sammanställning

### 4.1 Skapa CSV-fil
Skapa `scripts/grading/output/grades.csv` med struktur:
```csv
Elev,Email,A1,A2,A3,A4,A5,A6,B,C,Total
[Elevnamn],[Email],[poäng],...,[totalsumma]
```

### 4.2 Skapa detaljerad bedömningsfil
Skapa `scripts/grading/output/detailed_assessment.md`:

```markdown
# DETALJERAD BEDÖMNING - [Provnamn]

## Fråga A1 (alla elever):
- [Elev 1] ([poäng]/[max]p): [Motivering]
- [Elev 2] ([poäng]/[max]p): [Motivering]
...

## Fråga A2 (alla elever):
...

## Sammanfattning per elev:

### [Elevnamn] (Total: [X]p)
Del A: [poäng per fråga] = [summa]p
Del B: [poäng]p ([kort motivering])
Del C: [poäng]p ([kort motivering])
```

## Steg 5: Kvalitetskontroll

### 5.1 Verifiera maxpoäng
- Stämmer maxpoäng per del med provinstruktion?
- Är totalpoängen korrekt för varje elev?
- Har någon fått mer än max (acceptabelt om extra frågor besvarats)?

### 5.2 Kontrollera att varje elev har:
- Alla obligatoriska frågor bedömda
- Obesvarade frågor markerade (0p eller "Ej besvarad")
- Korrekt totalsumma

### 5.3 Dubbelkolla gränsvärden
- **Full poäng (6p/10p/15p)**: Motivera varför full poäng gavs
- **0 poäng**: Kontrollera att inget svar verkligen finns
- **Gränsvärden för Del B**: Om full poäng, verifiera att ALLA kriterier uppfylls

## Steg 6: Slutliga filer

**Spara två filer:**
1. `scripts/grading/output/grades.csv` - Poängöversikt för import
2. `scripts/grading/output/detailed_assessment.md` - Detaljerad motivering per fråga

**Båda filerna MÅSTE:**
- Vara kompletta för alla elever
- Ha korrekta summor
- Följa bedömningskriterierna strikt

## CHECKLISTA före avslut

**Förberedelser:**
- [ ] Läst provinstruktion
- [ ] Läst alla bedömningskriterier från facit
- [ ] Verifierat att parsern fungerar

**Bedömning (ALLA elever per fråga):**
- [ ] Bedömt ALLA elever för A1 samtidigt
- [ ] Bedömt ALLA elever för A2 samtidigt
- [ ] Bedömt ALLA elever för A3 samtidigt
- [ ] Bedömt ALLA elever för A4 samtidigt
- [ ] Bedömt ALLA elever för A5 samtidigt
- [ ] Bedömt ALLA elever för A6 samtidigt
- [ ] Bedömt ALLA elever för B samtidigt
- [ ] Bedömt ALLA elever för C samtidigt

**Kvalitetskontroll:**
- [ ] Kontrollerat maxpoäng per del
- [ ] Kontrollerat totalsumma för varje elev
- [ ] Verifierat gränsvärden (0p, full poäng, specialkrav)

**Output:**
- [ ] Skapat `scripts/grading/output/grades.csv`
- [ ] Skapat `scripts/grading/output/detailed_assessment.md`
- [ ] Verifierat att båda filerna är kompletta och korrekta

## Verktyg

### Manual Grading Assistant
Visar alla svar fråga för fråga:
```bash
pdm run python scripts/grading/manual_grading_assistant.py
```

### Verify Parser
Kontrollera att parsern fungerar:
```bash
pdm run python scripts/grading/verify_parser.py
```

### Interactive Grading
För manuell interaktiv rättning (kräver input):
```bash
pdm run grade
```

## VIKTIGA PRINCIPER

1. **Konsistens**: Använd samma standard för alla elever
2. **Transparens**: Motivera varje poäng tydligt
3. **Systematik**: Följ processen exakt, inga genvägar
4. **Kvalitet**: Dubbelkolla allt innan avslut
5. **Fråga-för-fråga**: Rätta ALDRIG alla frågor för en elev innan du rättat samma fråga för alla

---

**När denna Skill används:**
Påbörja med Steg 1.1 och arbeta metodiskt genom alla steg. Använd TodoWrite för att tracka progress genom checklistan. Kommunicera tydligt med användaren vid varje steg och be om bekräftelse vid osäkerhet kring bedömningskriterier.
