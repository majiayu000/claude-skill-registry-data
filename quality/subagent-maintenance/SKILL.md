---
name: subagent-maintenance
description: "Maintain an existing generated subagent package when its sources, converters, runtime behaviour, or requirements change — detect staleness, re-ingest or re-derive, re-export, and re-validate. Use when an already-authored package needs updating rather than authoring from scratch (Phase 12 of the authoring cycle)."
---

# Skill: subagent-maintenance

**Purpose:** Maintain existing generated subagents when sources, converters,
platform behavior, or requirements change. Phase 12 of the authoring cycle.

---

## Maintenance trigger types

| Trigger | Re-enter at |
|---------|-------------|
| Source content changed materially | Phase 2 (re-interrogate) |
| New source adds a mode or changes quality bar | Phase 2 → multi-source merge |
| Platform adapter format changed | adapter-export only |
| Test failure after platform update | adapter-export → validate |
| Conflict re-opened by new evidence | multi-source merge |
| Profile body became bloated | profile-generation → Phase 8 |
| Rights status changed | Phase 1 — stop distillation if rights withdrawn |
| Authored skill/reference body drifted from its grounding | Step 9 stale check → author-skills re-author |

---

## Steps for adding a new source

1. Run `source-ingestion` for the new source
2. Run `source-interrogation` on new source Markdown
3. Compare interrogation with existing profile
4. Identify conflicts using Phase 7 conflict classes
5. Resolve conflicts, update `profile.yaml`
6. Update `provenance-ledger.md` with new distillation rows
7. Append CHANGELOG entry
8. Re-run `adapter-export`
9. Re-run `validate`

---

## Steps for adapter-only update (platform change)

1. Check `.claude/agents/generated/<slug>.md` against canonical profile
2. Re-run `adapter-export`
3. Re-run `validate`

---

## Steps for stale authored bodies (Step 9)

When a source is re-ingested or principles are re-derived, skill/reference bodies authored from
the old grounding go stale. Detect and refresh them:

```bash
python -m tools.subagent_factory.cli stale <slug>          # report drift (STALE/WARN/INFO)
python -m tools.subagent_factory.cli stale <slug> --mark   # flip drifted ready docs → stale
```

Then re-run `author-skills <slug>` (it re-authors `stale` docs like stubs and re-stamps the
baseline) and re-export. The `validate` gate surfaces stale bodies as an advisory WARN; they do
not hard-block release but should be refreshed before the next one.

---

## Stale source policy

If a source is marked stale in the provenance ledger:
- Adapters generated from it are marked `status: stale`
- Human review required before next release
- Run `cli stale <slug>` to find authored bodies whose grounding the change invalidated
