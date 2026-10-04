---
name: bilingual-audit
description: Scan data/ fixtures for English-without-Malayalam parity gaps (titleMl, definitionMl, nameMl, summaryMl). Use when reviewing data changes, before PR, or when asked about bilingual coverage.
---

# Bilingual audit

Reports every record in `data/` where an English field is filled but its
Malayalam (`*Ml`) counterpart is missing or empty. The product promise is
bilingual parity — `*Ml` fields are typed as optional, so the type system won't
catch gaps.

## Fields to audit

| File                  | EN field          | ML field            |
| --------------------- | ----------------- | ------------------- |
| `data/kpis.ts`        | `title`           | `titleMl`           |
| `data/kpis.ts`        | `meta.definition` | `meta.definitionMl` |
| `data/departments.ts` | `name`            | `nameMl`            |
| `data/ministers.ts`   | `name`            | `nameMl`            |

(If new fields with `Ml` siblings appear — e.g. `summary`/`summaryMl` — add them
to the table.)

## How to run

Quick grep pass:

```bash
# Find KPIs missing titleMl
grep -nE '^\s*title:' data/kpis.ts | while read line; do
  lineno=$(echo "$line" | cut -d: -f1)
  # check next ~3 lines for titleMl
  if ! sed -n "$((lineno+1)),$((lineno+3))p" data/kpis.ts | grep -q 'titleMl:'; then
    echo "data/kpis.ts:$lineno missing titleMl"
  fi
done
```

For a structured pass, read each fixture file end-to-end and inspect every
record object — grep misses nested `meta.definition` cases. The fixture files
are short (<100 records each); a full read is fine.

## Output format

Group findings by file. For each gap, report:

```
data/kpis.ts: id=fiscal.revenue-deficit missing meta.definitionMl
data/departments.ts: id=dept.tourism missing nameMl
```

End with a one-line summary: `N gaps across M records`.

## What to do with findings

This skill _reports_ — it does not patch. Translations need a Malayalam speaker
(or vetted glossary), not a guess. Flag the gaps and let the user decide whether
to:

1. File translation requests
2. Mark the record `dataStatus: "tbd"` until the translation lands
3. Remove the EN-only field if it was added prematurely

Never machine-translate Malayalam government terminology — wrong term = wrong
meaning, and this dashboard is read by journalists.
