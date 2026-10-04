---
name: gardener
description: >
  Monthly catalog hygiene audit for Claude Code plugin marketplaces. Inventories
  every skill and agent, scores each against a 7-dimension rubric via parallel
  Opus Agents, detects description collisions via Bedrock Cohere v4 embeddings
  with pairwise cosine, and writes a delta report vs. the prior audit. Proposes
  resolutions; does not auto-apply. Use when the user asks to audit the catalog,
  run the gardener, find skill collisions, check plugin hygiene, generate a
  monthly audit report, or mentions catalog drift.
arguments:
  - name: scope
    description: Optional scope — plugin name (e.g., personal-plugins) or 'all'. Defaults to 'all' in the current marketplace.
    required: false
context: fork
user_facing: true
---

## Contents

| Reference                            | When to load                            |
| ------------------------------------ | --------------------------------------- |
| `references/orchestrator.md`         | Running `/gardener` — the 4-phase flow  |
| `../../references/rubric.md`         | Scoring dimensions (shared)             |
| `../../references/write-protocol.md` | Copied verbatim into every Agent prompt |
| `templates/inventory-skeleton.md`    | Inventory output file                   |
| `templates/scorecard-skeleton.md`    | Per-skill scorecard output file         |
| `templates/collisions-skeleton.md`   | Collisions output file                  |
| `templates/clusters-skeleton.md`     | HDBSCAN taxonomy output file            |
| `templates/report-skeleton.md`       | Final audit report                      |

# Gardener

Monthly catalog hygiene. Orchestrator runs inside a forked subagent. Walks every skill and agent across the marketplace, scores them in parallel, detects collisions via Bedrock Cohere v4 embeddings, runs an HDBSCAN taxonomy check, and composes a delta report against the prior audit. Proceeds autonomously — planning is reversible. Gates only at the point of writing fixes back to SKILL.md files, which it does not do: it proposes.

## How it works

Read `references/orchestrator.md` and follow its phases. Short version:

1. **Inventory** — walk the marketplace, extract frontmatter and file stats, write `audit/YYYY-MM/inventory.md`.
2. **Collide** — run `scripts/embed-catalog.py` once (Bedrock Cohere v4), then `scripts/pairwise-collisions.py` and `scripts/cluster-taxonomy.py`. One interpreter Agent opens the flagged SKILL.md files, verifies the collisions by reading, and writes `audit/YYYY-MM/collisions.md` + `audit/YYYY-MM/clusters.md` with recommended actions.
3. **Score** — launch one parallel Opus Agent per skill. Each Agent reads the skill's SKILL.md, references/, and templates/ in full, applies the shared rubric, and cites file:line evidence in every rationale. Collision and cluster data from Phase 2 are passed in as cross-reference context — *where to look*, not substitute for reading.
4. **Report** — one foreground critic Agent reads inventory + all scorecards + collisions + clusters + the prior month's report, writes `audit/YYYY-MM/report.md` with health score, delta, quarantine list, and top-5 action items.

## Output layout

```text
plugin-gardener/audit/
  YYYY-MM/
    inventory.md
    scores/
      <skill-name>.md         # one per skill
    vectors.npz               # cached Cohere v4 embeddings
    collisions.csv            # raw pairwise output
    collisions.md             # interpreted, ranked, with actions
    clusters.md               # HDBSCAN clusters, outliers, straddlers
    report.md                 # the deliverable
```

Each month's audit is a standalone artifact; deltas are computed by reading the prior-month report inline.

## What it does not do

The gardener proposes. It does not:

- Edit SKILL.md or agent files.
- Open pull requests.
- Delete files.
- Change marketplace.json.
- Publish to skills.sh or any external registry.

Those actions are the user's to approve. Every suggestion in `report.md` includes the exact file path and the proposed change, ready for you to apply manually or via a follow-up `/rewrite-descriptions` invocation.

## Cost note

One monthly run against 40–50 skills: ~50 parallel Opus Agents for scoring, 1 embedding call (single Bedrock invocation, all descriptions fit under the 96-item cap), 1 critic Agent for the report. Significant — budget for it as a monthly line item, not a casual run.
