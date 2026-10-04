---
name: uvm-timetal
description: "Look up or update UVM minimum weekly hours (vejledende timetal) for Danish schools. USE THIS SKILL when the user asks about UVM timetal, minimumstimetal, mandatory hours, UVM requirements, or how many hours a subject requires for a given grade. Also use when a new school year needs to be added."
---

# UVM Timetal Skill

Retrieves and maintains the UVM vejledende minimumstimetal (weekly hours per subject per grade).

## Authoritative source

UVM publishes the current timetal circular at:
**https://www.uvm.dk/folkeskolen/fag-timetal-og-overgange/timetal**

Fetch that page to get the latest official numbers. The page contains a table showing weekly hours per subject per grade level. Cross-reference with the PDF circular linked on the page for exact values.

For friskoler the rules come from the Friskolelov — UVM minimumstimetal still applies as the baseline, but friskoler set their own curriculum. The `staa-maal-med` feature uses these numbers as the reference target.

## Repository data file

The current data lives at:

```
api/Skoleoverblikket.Api/Data/uvm-timetal/2025-2026.json
```

Keys are `SubjectCategory` enum names. Nested keys are grade level as strings ("0"–"9"), where "0" = børnehaveklasse. Values are **weekly hours** (vejledende).

To read the current file:

```powershell
Get-Content api/Skoleoverblikket.Api/Data/uvm-timetal/2025-2026.json | ConvertFrom-Json | Format-List
```

## Adding a new school year

1. Fetch the authoritative numbers from https://www.uvm.dk/folkeskolen/fag-timetal-og-overgange/timetal
2. Create a new file: `api/Skoleoverblikket.Api/Data/uvm-timetal/<year>-<year+1>.json`
3. Copy the structure from `2025-2026.json` and update values to match the new circular
4. The API (`StaaMaalMedController`, `ReportsController`) auto-picks the newest file (sorted descending by filename) — no code change needed

## Annual hours conversion

Weekly hours × 40 = UVM minimum annual hours (used in the XLSX export in `ReportsController`).

## Enum mapping

The `SubjectCategory` C# enum maps to JSON keys:

```
Dansk, Matematik, Engelsk, Naturfag, Historie, Musik, Idraet,
Kristendomskundskab, Billedkunst, HaandvaerkOgDesign, Tysk, Fransk,
Geografi, Biologi, FysikKemi, Samfundsfag, Fri, Madkundskab
```

`Fri` is excluded from all timetal calculations. 

## If user asks for current values without fetching

Read the file directly:

```powershell
Get-Content api/Skoleoverblikket.Api/Data/uvm-timetal/2025-2026.json
```
