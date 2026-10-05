---
name: nav2009-development
description: Develop, review, and architect C/AL code and objects for Microsoft Dynamics NAV 2009 (Navision) — Classic client and RoleTailored Client (RTC). Covers C/AL coding patterns and performance idioms (FINDSET/FINDFIRST/ISEMPTY, SETCURRENTKEY, locking, COMMIT discipline), key/SIFT design, code-review checklist, customization architecture (hooks, setup tables, number series), reports (Classic sections and RDLC), integrations (XMLports, Dataports, NAS, web services, MSMQ/COM), and upgrade-friendly patterns toward Business Central. Use for any NAV 2009 / Navision / C/AL task — writing or reviewing code, designing a customization, building a report or integration, or preparing for a BC migration.
license: MIT
metadata:
  version: "1.0.3"
---

# NAV 2009 Development

Expert guidance for **Microsoft Dynamics NAV 2009** (incl. SP1/R2): C/AL, C/SIDE, the 2-tier
Classic client and the 3-tier RoleTailored Client (RTC). This skill is knowledge-only; detailed
pattern tables live in [REFERENCE.md](REFERENCE.md) — consult it before writing or reviewing
non-trivial C/AL.

For **performance problems** (slowness, locking, deadlocks): the C/AL-side rules are below, but
measure the SQL side with the **nav2009-sql-performance** skill — its script collects the DMV
evidence and its REFERENCE maps SQL findings back to C/AL causes. Use both for a complete picture.

## Platform facts (don't guess against these)

- NAV 2009 is **pre-AL, pre-events**: no extensions, no event subscribers, no try-functions, no
  `SETAUTOCALCFIELDS`, no queries, no .NET interop in classic C/AL (DotNet variables arrive in 2009 R2
  RTC service tier only). Customization = direct object modification in C/SIDE.
- Two UIs coexist: **Classic** (Forms, Dataports, classic report sections) and **RTC** (Pages,
  XMLports, RDLC report layouts). Code may run on the Classic client, the RTC service tier, or NAS —
  guard UI calls with `GUIALLOWED` and don't use client-side file dialogs in server-side code.
- Object/field customization ranges: **50000–99999** (licensed range). Standard objects are modified
  in place — every change must carry a version tag in the object's `Version List` and inline markers.
- SQL Server backend: table keys → SQL indexes (`MaintainSQLIndex`), SumIndexFields → **SIFT indexed
  views** (`MaintainSIFTIndex`), FlowFields/`CALCSUMS` read them. NAV owns the physical schema;
  never recommend hand-made SQL indexes as the primary fix.

## Core C/AL rules (write and review against these)

1. **Record loops**: `FINDSET` (or `FINDSET(TRUE)` when modifying) for loops; `FINDFIRST`/`FINDLAST`
   for one record; `ISEMPTY` for existence checks; never bare `FIND('-')` for new code.
2. **`SETCURRENTKEY` must match the filters** (and any `CALCSUMS`) — the single biggest C/AL
   performance lever. Filtering on fields with no supporting key = scans on `G/L Entry`-sized tables.
3. **Transactions**: no `COMMIT` inside posting routines or loops — it breaks NAV's all-or-nothing
   posting (Codeunits 80/90/12...) and multiplies log writes. `LOCKTABLE` before read-then-update;
   acquire locks in a consistent order across code paths to avoid deadlocks.
4. **FlowFields**: `CALCFIELDS` only what you need, outside loops where possible; prefer
   `CALCSUMS` on a SIFT-keyed field over summing in a loop.
5. **Customization architecture**: logic in your own codeunits in the 50000+ range; standard objects
   get only minimal, tagged call-out lines ("hooks"). New modules get their own setup table and
   integrate with No. Series. Mark every standard-object touch:
   `// <TAG> CUSTOMIZATION BEGIN ... // <TAG> CUSTOMIZATION END`.
6. **Naming**: standard NAV abbreviations (`CustLedgEntry`, `GenJnlLine`, `SalesHeader`) — match
   the base application's conventions, not your own.

## Review checklist (when asked to review C/AL)

Walk [REFERENCE.md](REFERENCE.md) § Review checklist. Headlines: key/filter mismatch on large
tables, `FIND` misuse, stray `COMMIT`, missing version tags, customization sprawl in standard
objects, field IDs outside 50000–99999, locking order, RTC/Classic/NAS execution-target bugs
(`GUIALLOWED`, file handling), and upgrade hostility (logic buried in standard objects instead of
hooked-out codeunits).

## Reports, integrations, BC-upgrade posture

- **Reports**: NAV 2009 RDLC reports still run the Classic report's DataItems underneath — keep the
  dataset flat and minimal; `GetData`/`SetData` for document headers. Details + Classic-sections
  guidance in REFERENCE.
- **Integrations**: prefer RTC **SOAP web services** (published Pages/Codeunits, port 7047) for new
  work; XMLports for file exchange; Dataports are Classic-only legacy; NAS + Job Queue for unattended
  processing; MSMQ/COM only when the counterpart demands it.
- **BC-upgrade posture**: keep customizations hook-shaped (one-line call-outs → own codeunits) so
  they translate to event subscribers later; avoid new Dataports/Forms where an XMLport/Page works;
  flag deep standard-table surgery as migration debt.
