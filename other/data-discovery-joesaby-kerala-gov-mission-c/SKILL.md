---
name: data-discovery
description: Find and vet a government source before adding any number to the dashboard. Use when sourcing a new KPI, comparator, Government Order, or Status-Paper figure — turns "I need a number" into "I have an official, linkable source".
---

# Data discovery

Every figure on this dashboard must trace to an **official government source**
(see [`docs/data/source-policy.md`](../../../docs/data/source-policy.md)). This
skill is how you find one and confirm it before writing a fixture.

## Steps

1. **Check what we already catalogued.** Read the per-domain inventory in
   [`docs/data/`](../../../docs/data/) (e.g. `fiscal.md`, `health.md`) and the
   typed registry [`data/sources.ts`](../../../data/sources.ts). The source may
   already be listed.
2. **Go to the primary body, not coverage.** Prefer, in order: the issuing
   department (`*.kerala.gov.in` / `*.gov.in`), a constitutional/statutory body
   (RBI, CAG, ECI, Census, MoSPI), the Legislative Assembly
   (`niyamasabha.org`), then `data.gov.in`. A newspaper or aggregator is only a
   lead to the underlying official document — never the source of record.
3. **Get a resolvable URL** to the exact document/page (a PDF, a table, a
   dataset). Note the precise table/figure number — provenance must be specific
   (`Table 3.1b`, not "the report").
4. **Record retrieval.** Capture the `retrievedAt`/`lastRefreshed` timestamp
   (ISO with `+05:30`).
5. **Verify it passes the gate.** Run `deno task check:sources`. If the host
   isn't on the government allowlist, you have the wrong source — go back to 2.

## Reliability ladder (best → unacceptable)

Issuing department → constitutional/statutory body → Assembly →
national open-data portal → **(stop: below this line is not a source of record)**
→ think-tank / aggregator (PRS, OpenBudgets, Dataful) → newspaper → Wikipedia /
blog / social.

## Output

A `{ source, sourceUrl, retrievedAt }` triple ready to drop into the fixture,
plus the exact table/figure citation. If you cannot find an official source, the
number does **not** ship — open a tracking note instead.

## Related

- [`docs/data/source-policy.md`](../../../docs/data/source-policy.md) · `/add-kpi`
  skill · `kpi-data-reviewer` agent · `deno task check:sources`.
