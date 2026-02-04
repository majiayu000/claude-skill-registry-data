---
name: dnevni-summary
description: Creates STRUCTURED summary.md in each daily folder. Analyzes chat conversations and generates actionable summaries with "Što je uradio" and "Što bi trebao da uradi" sections per person. Use for daily reports and activity tracking.
---

# Dnevni Summary

## Overview

Kreira STRUKTURIRANI `summary.md` u svakom dnevnom folderu - analizira razgovore i generiše akcione summaries.

**Što radi:**
- Učitava `chat.md` iz dnevnog foldera
- Učitava prethodne taskove (iz prošle sedmice i prethodnih dana)
- **Claude analizira razgovore i generiše strukturirani summary**
- Kreira `summary.md` sa:
  - Uvodni sažetak razgovora
  - Po osobama: "Što je uradio" i "Što bi trebao da uradi"
- Fokus na akcije, taskove i odluke (ne samo lista poruka!)

**Output:**
- `summary.md` u svakom dnevnom folderu
- Lokacija: `{odjel}/{sedmica}/{datum}/summary.md`
- Organizovan po osobama sa kondenzovanim aktivnostima

## When to Use This Skill

User says:
- "Make daily summary"
- "What happened today"
- "Daily report"
- "Summary for 24.10"
- "What did everyone do today"

**Default behavior:** Uses today's date, analyzes all departments

## Workflow

IMPORTANT: **This is a Claude-driven skill.** The Python script only loads data, Claude does the analysis and writing.

### How It Works

**Step 1: User requests summary**
```
"Make daily summary for 25.10"
"Generiši dnevni summary"
```

**Step 2: Python script učitava podatke**
- Pronalazi foldere za datum
- Čita `chat.md` iz svakog foldera
- Čita prethodne sedmične summaries (za taskove)
- Čita prethodne dnevne summaries (za taskove)
- Vraća podatke kao output

**Step 3: Claude analizira razgovore**
- Čita output od script-a (chat poruke + prethodni taskovi)
- Razmatra kontekst i relevantnost
- Ekstraktuje ključne informacije:
  - Šta je ko uradio (akcije, postignuća)
  - Šta bi ko trebao da uradi (planirani taskovi, obaveze)
  - Ključne odluke i dogovori
- **KORISTI extended thinking ako je potrebno za kompleksne razgovore**

**Step 4: Claude generiše strukturirani summary**
- Kreira uvodni paragraf sa sažetkom razgovora
- Za svaku osobu kreira sekcije:
  - "Što je uradio:" - konkretne akcije
  - "Što bi trebao da uradi:" - budući taskovi
- Fokus na AKCIJE i TASKOVE, ne samo prepričavanje poruka

**Step 5: Claude zapisuje summary.md**
- Koristi Write tool da kreira `summary.md` u odgovarajućem folderu
- Format: Strukturirani markdown sa jasnim sekcijama

## Summary Format

IMPORTANT: **Format treba biti STRUKTURIRAN i AKCIONI, ne samo lista poruka!**

```markdown
# Sazetak razgovora (DD.MM.YYYY)

[Uvodni paragraf - 2-3 rečenice koje sažimaju glavne teme razgovora i ključne akcije]

---

## **Ime Prezime**

### Što je uradio:
- Konkretna akcija 1
- Konkretna akcija 2
- Postignuće / završen zadatak

### Što bi trebao da uradi:
- Planirani task 1
- Obaveza 2
- Follow-up akcija

---

## **Ime Prezime**

### Što je uradio:
- ...

### Što bi trebao da uradi:
- ...
```

**Primjer dobrog summary-ja:**

```markdown
# Sazetak razgovora (25.10.2025)

Razgovor se vrti oko pracenja Life Plast kontakta, trazenja IT opreme u Sarajevu, i masine za pakovanje secera. **Haris** je pokusao kontaktirati Life Plast ali voditelj je dostupan tek u ponedjeljak. **Mahir** trazi IT opremu (polovna/nova + servis) u Sarajevu. **Seval** je pronasao dobavljaca za industrijske masine za pakovanje.

---

## **Haris Grupacija**

### Što je uradio:
- Pozvao voditelja firme Life Plast ali nije bio dostupan
- Kontaktirao proizvodnju i saznao da je voditelj dostupan tek u ponedjeljak u 8:00
- Identificirao moguce IT kontakte u Sarajevu (braca u IT sektoru - programeri)

### Što bi trebao da uradi:
- Ponedjeljak u 8:00 - Ponovo kontaktirati voditelja Life Plast
- Kontaktirati poznanike iz IT sektora za IT opremu i servis

---

## **Mahir**

### Što je uradio:
- Trazio poznanike za IT opremu u Sarajevu (polovna ili nova)
- Ima kontakte u Zenici ali preferira Sarajevo jer je blize

### Što bi trebao da uradi:
- Sacekati preporuke od tima za IT kontakte u Sarajevu
- Provjeriti servise za IT opremu

---

## **Seval Grupacija**

### Što je uradio:
- Pronasao dobavljaca industrijskih strojeva za pakiranje: **Studio Plus**
- Dostavio link: https://studioplus.ba/industrijski-strojevi-za-pakiranje/
- Dostavio kontakt broj: +387 39 703 607
- Specificno nasao masinu za pakovanje secera

### Što bi trebao da uradi:
- Sacekati potvrdu da li je masina za pakovanje jos potrebna
- Ako jeste, kontaktirati Studio Plus za detalje i cijene
```

## Script Usage

**The script ONLY loads data - it does NOT generate the summary!**

```bash
# Read data for specific date
python .claude/skills/dnevni-summary/scripts/read_daily_data.py --date 25.10

# Read data for specific folder
python .claude/skills/dnevni-summary/scripts/read_daily_data.py --folder "gastrohem whatsapp/svaštara/20.10 - 27.10/25.10"
```

**Script output:**
- Učitava i prikazuje chat.md sadržaj
- Učitava i prikazuje prethodne taskove iz sedmičnog summary-ja
- Lista prethodnih dnevnih summaries (za dodatni kontekst)
- **NE** generiše summary.md (to radi Claude!)

## Example Workflow

**User:** "Generiši dnevni summary za 25.10"

**Claude steps:**

1. **Učitava podatke:**
   ```bash
   python .claude/skills/dnevni-summary/scripts/read_daily_data.py --date 25.10
   ```
   Output prikazuje za svaki folder:
   - Chat.md sadržaj (sve poruke)
   - Taskove iz prošle sedmice (Plan za narednu sedmicu sekcije)
   - Listu prethodnih dnevnih summaries (za kontekst)

2. **Analizira razgovore (za svaki folder):**
   - Čita chat poruke koje je script prikazao
   - Identifikuje akcije, postignuća, taskove
   - Koristi extended thinking za kompleksne/duge razgovore
   - Kreira strukturirani summary prema prescribed formatu:
     - Uvodni sažetak (2-3 rečenice)
     - Po osobama: "Što je uradio" / "Što bi trebao da uradi"

3. **Zapisuje summary.md (za svaki folder):**
   - Koristi Write tool
   - Path: `gastrohem whatsapp/{odjel}/{sedmica}/{dan}/summary.md`
   - Format: Strukturirani markdown sa jasnim sekcijama
   - Fokus na AKCIJE i TASKOVE (ne samo prepis poruka!)

4. **Potvrđuje:**
   "✅ Kreirani dnevni summaries za 25.10: 3 foldera procesirana"

## Script Reference

### read_daily_data.py

**Purpose:** Load chat data and previous tasks for Claude analysis (does NOT generate summaries)

**Usage:**
```bash
# Read data for specific date
python scripts/read_daily_data.py --date 25.10

# Read data for specific folder
python scripts/read_daily_data.py --folder "gastrohem whatsapp/svaštara/20.10 - 27.10/25.10"

# Today's date (default)
python scripts/read_daily_data.py
```

**Arguments:**
- `--date DD.MM` - Date to read (default: today)
- `--folder PATH` - Process specific folder only
- `--base-path PATH` - Base path (default: "gastrohem whatsapp")

**What it does:**
1. Finds all daily folders for the specified date
2. Reads chat.md from each folder
3. Finds and reads previous weekly summary (for tasks)
4. Lists previous daily summaries (for context)
5. Displays all data on stdout

**What it does NOT do:**
- Does NOT analyze conversations
- Does NOT generate summaries
- Does NOT write summary.md files

**Claude does:** Analysis, summary generation, and writing summary.md files

## Important Notes

- **Fokus na AKCIJE:** Ne samo prepričavati poruke, već ekstraktovati šta je KO URADIO i šta BI TREBAO DA URADI
- **Kontekst je bitan:** Koristi prethodne taskove da vidiš šta je bilo planirano
- **Jasna struktura:** Svaka osoba ima svoje dvije sekcije (uradio / trebao)
- **Uvodni sažetak:** 2-3 rečenice koje kažu o čemu se razgovara
- **Extended thinking:** Koristi ga za kompleksnije razgovore gdje je teško ekstraktovati akcije
- **Per-folder summaries:** Svaki odjel dobija svoj summary.md u svom folderu
- **Natural language:** Summaries treba da budu čitljivi i prirodni, ne suvi bullet pointi

## Best Practices

1. **Process end-of-day** - Generiši summaries na kraju radnog dana dok je kontekst svjež
2. **Read previous summaries** - Ako je potrebno više konteksta, pročitaj prethodne dnevne summaries
3. **Focus on actions** - Izvuci konkretne akcije i taskove, ne samo prepričavaj poruke
4. **Be specific** - "Kontaktirao Life Plast" umjesto "Nešto radio oko Life Plast"
5. **Include details** - Imena firmi, brojevi telefona, linkovi - sve relevantno
6. **Use extended thinking** - Za duge razgovore sa mnogo informacija
