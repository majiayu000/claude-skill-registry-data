---
name: tib-report
description: Create TIB (Tjänsteperson i Beredskap) incident reports. Auto-triggers on phrases like "skapa TIB-rapport", "ny händelserapport", "TIB report", "dokumentera händelse".
allowed-tools: Bash, Read, Write
---

# Skill: tib-report

## Purpose

Provides quick creation of standardized TIB (Tjänsteperson i Beredskap) incident reports in the required format. Reports are saved as markdown files in the PKM structure and follow the organizational template with sections for Tidpunkt, Händelse, Åtgärd, Beslut, and Reflektion.

## Required Context (gather BEFORE starting workflow)

1. PKM path via `bun run src/aida-cli.ts paths getPkmRoot` → for saving location
2. Current date/time via `bun run src/aida-cli.ts time getTimeInfo` → for default tidpunkt

**How to gather context:**
```bash
# Get PKM path for saving report
bun run src/aida-cli.ts paths getPkmRoot

# Get current date/time
bun run src/aida-cli.ts time getTimeInfo
```

## Workflow Steps

### Step 1: Parse Input & Identify Missing Sections

- **Action:** Check if user provided complete report info in initial message
- **Look for:**
  - Title/subject of incident
  - Tidpunkt (date/time)
  - Händelse (what happened)
  - Åtgärd (actions taken by TIB)
  - Beslut (decisions made)
  - Reflektion (reflections/lessons learned)
- **Output to user:** None (internal processing)
- **Wait for:** Continue immediately

### Step 2: Gather Missing Information

**Required fields:**
- Title (for filename)
- Tidpunkt
- Händelse

**Optional but prompted:**
- Åtgärd
- Beslut
- Reflektion

- **Action:** Ask user for any missing required fields
- **Output to user:**
  ```
  Jag skapar en TIB-rapport. Jag behöver följande information:

  📅 Tidpunkt: [if missing, ask]
  📝 Händelse: [if missing, ask]
  ⚙️ Åtgärd: [if missing, ask]
  ⚖️ Beslut: [if missing, ask]
  💭 Reflektion: [if missing, ask]
  ```
- **Wait for:** User provides missing information

### Step 3: Determine Report Format

- **Action:** Detect if incident is single-event or multi-day based on tidpunkt or händelse content
- **Format:** See [REPORT-FORMAT.md](REPORT-FORMAT.md) for formatting rules
- **Output to user:** None (internal processing)
- **Wait for:** Continue immediately

### Step 4: Generate Report Content

- **Action:** Use template from `templates/tib-report.md` and populate with user data
- **Language style:** Follow professional language guidelines in [REPORT-FORMAT.md](REPORT-FORMAT.md) - always use formal, concrete language
- **Template variables:**
  - `{{title}}` - Title/heading of the report
  - `{{tidpunkt}}` - Date/time of incident
  - `{{händelse}}` - What happened (with timeline if multi-day)
  - `{{åtgärd}}` - Actions taken by TIB
  - `{{beslut}}` - Decisions made by TIB
  - `{{reflektion}}` - Reflections and lessons learned
- **Output to user:** None yet
- **Wait for:** Continue immediately

### Step 5: Determine Filename and Save

- **Action:** Create filename in format `YYYY-MM-DD [Title].md`
- **Extract date:** From tidpunkt field (use first date if multi-day)
- **Save location:** `<pkm>/04-TIB/03-REPORTS/YYYY-MM-DD [Title].md`
- **CLI call:**
  ```bash
  # Write report file to PKM location
  # Use Write tool with full path
  ```
- **Output to user:** None yet
- **Wait for:** Continue immediately

### Step 6: Confirm Creation

- **Output to user:**
  ```
  ✅ TIB-rapport skapad!

  📄 Fil: YYYY-MM-DD [Title].md
  📁 Plats: 04-TIB/03-REPORTS/

  Rapporten innehåller:
  • Tidpunkt: [datum/tid]
  • Händelse: [sammanfattning]
  • Åtgärd: [ja/nej/text]
  • Beslut: [ja/nej/text]
  • Reflektion: [ja/nej/text]

  Vill du öppna filen för granskning?
  ```
- **Wait for:** User may request to view or edit

## Output Format

- **Language:** Swedish (default)
- **File format:** Markdown (.md)
- **File location:** `<pkm>/04-TIB/03-REPORTS/`
- **Filename:** `YYYY-MM-DD [Title].md`

See [REPORT-FORMAT.md](REPORT-FORMAT.md) for complete format specification and examples.

## Error Handling

- **If `paths getPkmRoot` fails:** Show error "Kan inte hitta PKM-sökvägen. Kontrollera att config/aida-paths.json finns och är korrekt konfigurerad."
- **If PKM path not accessible:** Show error "Kan inte komma åt PKM-mappen: [path]. Kontrollera behörigheter."
- **If `04-TIB/03-REPORTS/` doesn't exist:** Create directory automatically (with user confirmation)
- **If file already exists:** Ask user "En rapport med detta namn finns redan. Vill du: 1) Skriva över, 2) Ändra filnamn, 3) Avbryt"
- **If user provides no title:** Use generic format `YYYY-MM-DD TIB-rapport.md`
- **If required field missing after prompting:** Ask again or offer to save as draft

## Anti-patterns

- **NEVER create report without Tidpunkt and Händelse** - these are required minimum
- **NEVER modify existing reports** - only create new ones
- **NEVER save outside PKM structure** - always use `<pkm>/04-TIB/03-REPORTS/`
- **NEVER use database** - TIB reports are standalone markdown files
- **NEVER create task or journal entry** - this is not integrated with AIDA task system
- **NEVER skip filename date prefix** - format must be `YYYY-MM-DD [Title].md`
- **NEVER use direct SQL** - not applicable (no database interaction)
- **NEVER overwrite without asking** - confirm with user first

## Tool Contract

**Allowed CLI Operations:**
- **time:** getTimeInfo (for current date/time defaults)
- **paths:** getPkmRoot (to get PKM path for saving)

**File Operations:**
- **Read:** `templates/tib-report.md` (template file)
- **Write:** `<pkm>/04-TIB/03-REPORTS/YYYY-MM-DD [Title].md` (final report)

**Forbidden Operations:**
- No task creation
- No journal entries
- No profile updates
- No database operations
- No modifications to existing reports (without explicit user request)

**File Access:**
- **Read:** `templates/tib-report.md`
- **Write:** `<pkm>/04-TIB/03-REPORTS/` (new reports only)
- **No writes to:** Database, system files, config files, other PKM locations

## Supporting Documentation

- [REPORT-FORMAT.md](REPORT-FORMAT.md) - Report format specification (single source of truth)

## Design Principles

1. **Standardized format** - Ensure all reports follow the same structure
2. **Flexible input** - Accept complete info or gather interactively
3. **Clear confirmation** - Always show what was created and where
4. **Non-invasive** - Don't integrate with task system (standalone files)
5. **Multi-day support** - Handle both simple and complex timeline events
