---
name: review-checklist
description: Review a change against this project's blocking gates and quality bar — government sources, SEED_VERSION bump, deno check, translation provenance (machine-draft flags), KPI defensibility. Use before opening a PR or when asked to review the current diff or a PR for this repo.
---

# Review checklist

The project-specific review standard. The full rubric lives in
[`docs/code-review-guidelines.md`](../../../docs/code-review-guidelines.md);
this skill is the actionable pass. (For generic diff review use the built-in
`/code-review`; this one adds the kerala-gov-mission-control rules.)

## Run the gates first

```bash
deno task check          # fmt --check + lint + type-check  (blocking)
deno task check:sources  # government-source policy          (blocking)
deno task check:ml       # foreign-script glyphs in data/    (blocking, in CI)
deno task test           # unit tests (lib/)                 (blocking, in CI)
```

All must be green. These are the same gates the pre-commit hook and CI run.

## Blockers — fail the review if any are true

- [ ] A published figure (KPI / GO / Status Paper) cites a **non-government**
      source, or is missing `sourceUrl`. → `docs/data/source-policy.md`
- [ ] A `data/*.ts` fixture changed but `SEED_VERSION` in `data/db.ts` was
      **not** bumped.
- [ ] `deno task check` fails (type error / lint / formatting drift).
- [ ] An LLM-drafted `*Ml` string lacks `translationStatus: "machine-draft"` on
      its record. Machine translation is allowed **only** as a flagged draft
      (spec Rule 2.4); unflagged machine Malayalam is a blocker. (Missing
      entirely is OK with `dataStatus: "tbd"`.)
- [ ] A new KPI is missing a defensibility field (`ownerDeptId`, `target`, ≥1
      external comparator, `meta.definition`+`definitionMl`, `source`,
      `sourceUrl`, `owner` designation, `lastRefreshed` with `+05:30`).

## Quality — request changes

- [ ] EN field added without a `*Ml` counterpart — human-verified or flagged
      `machine-draft` (`/bilingual-audit`).
- [ ] New island where a server component would do.
- [ ] Reinvents an existing type/helper/CSS token instead of reusing it.
- [ ] A visual without visible provenance (source + retrieval/refresh date).
- [ ] Conflicting official figures picked silently instead of disambiguated in
      `meta.definition`.

## Escalate to an agent

- `kpi-data-reviewer` — for any `data/kpis.ts` change.
- `governance-data-reviewer` — for `unverified`/`tbd` Department/Minister/
  Secretary records.

Report findings as `file:line — issue (severity)`, or "No blocking issues."
