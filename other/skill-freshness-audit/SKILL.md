---
name: skill-freshness-audit
description: >
  Systematic skill freshness auditing with verification anchors, volatility classification,
  staleness detection, and upstream lineage tracking across every Agent Skill in the
  repository (data_product_accelerator/, genai-agents/, apps_lakebase/). Fetches official
  documentation URLs embedded in skills, compares patterns against live docs, tracks lineage
  to databricks/databricks-agent-skills (the single upstream registry), and reports
  drift. Use when auditing skill currency, verifying skills against latest Databricks/MLflow
  docs, checking for stale skills, syncing with the upstream registry, or after a platform
  release. Triggers on "audit skills", "check freshness", "stale skills", "verify skills",
  "skill audit", "update check", "Databricks released", "new MLflow version", "upstream
  sync", "databricks-agent-skills lineage", "upstream lineage".
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Read/report meta-skill — audits skill currency and reports drift; no deployed resource and no deploy verb. Client-agnostic. On Genie Code it audits the skill tree under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`); fetching upstream docs uses the Genie Code web tools (see `skills/genie-code-environment`)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "3.0.0"
  domain: admin
  role: utility
  standalone: true
  last_verified: "2026-04-27"
  volatility: low
  upstream_sources: []  # This audit system (self-referential)
---

# Skill Freshness Audit

Ensures all Agent Skills stay current with official Databricks, MLflow, and platform documentation through systematic verification, staleness detection, and drift reporting.

## When to Use

- Periodic skill audits (recommended: monthly for high-volatility, quarterly for medium)
- After a Databricks or MLflow platform release
- When a skill produces incorrect patterns during implementation
- When user says "audit skills", "check freshness", or "verify skills"
- Before major implementations to ensure skill accuracy

---

## Freshness Metadata Schema

Every skill's frontmatter should include these three fields:

```yaml
metadata:
  last_verified: "2026-02-07"          # ISO date when skill was last verified against docs
  volatility: high                      # high | medium | low — how often the underlying APIs change
  verification_sources:                 # URLs to check for drift (optional, for skills with external refs)
    - url: "https://docs.databricks.com/aws/en/metric-views/yaml-ref"
      check_for: "YAML syntax, supported field types"
    - url: "https://mlflow.org/docs/latest/genai/serving/responses-agent"
      check_for: "ResponsesAgent API, predict() signature"
  upstream_sources:                     # Repo-level lineage tracking (tracks upstream dependencies)
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-agent-bricks/SKILL.md"
      relationship: "extended"          # derived | extended | inspired | reference
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
```

`verification_sources` checks live documentation URLs for API drift. `upstream_sources` tracks structured repo-level lineage for systematic upstream sync audits. Both are complementary.

**Template:** See [assets/templates/verification-metadata.yaml](assets/templates/verification-metadata.yaml) for a copy-paste starter.

---

## Volatility Classification

| Volatility | Stale After | Description | Example Skills |
|---|---|---|---|
| **high** | 30 days | APIs change frequently, new features added often | GenAI agents, MLflow 3.x, Genie APIs, metric views |
| **medium** | 90 days | Features evolve but core patterns are stable | DLT, monitoring, dashboards, asset bundles |
| **low** | 180 days | Stable patterns, rarely change | ERD diagrams, naming standards, merge patterns, documentation |

**Full classification:** See [references/volatility-classification.md](references/volatility-classification.md)

---

## Audit Workflow

### Quick Audit (5 minutes) — Find Stale Skills

```
1. Run scan script to find all skills with stale last_verified dates
2. Report stale skills grouped by volatility
3. Prioritize high-volatility skills for verification
```

**Script:** See [scripts/scan_skill_freshness.py](scripts/scan_skill_freshness.py)

### Full Audit (per skill) — Verify Against Live Docs

```
1. Read the skill's verification_sources from frontmatter
2. For each verification URL:
   a. WebFetch the URL
   b. Compare key patterns (API signatures, SQL syntax, SDK methods)
   c. Check for deprecated features still recommended in skill
   d. Check for new capabilities missing from skill
3. Report drift as a list of specific updates needed
4. Update last_verified date after verification (even if no changes needed)
```

### Platform Release Audit — After Databricks/MLflow Release

```
1. Identify affected domain (e.g., "MLflow 3.2 released" → genai-agents domain)
2. Find all skills in affected domain using volatility-classification.md
3. Run Full Audit on each affected skill
4. Update skills with new patterns / deprecation warnings
5. Update last_verified dates
```

### Upstream Source Audit — Check Lineage Across Both Registries

Skills track their lineage to the single authoritative upstream registry via
`upstream_sources` metadata:

| Upstream registry | Repo | Manifest | Use for |
|---|---|---|---|
| Databricks Agent Skills | [`databricks/databricks-agent-skills`](https://github.com/databricks/databricks-agent-skills) | [`manifest.json`](https://raw.githubusercontent.com/databricks/databricks-agent-skills/main/manifest.json) | All canonical Databricks-platform and accelerator skills (apps, lakebase, model-serving, agent-bricks, pipelines, dabs, unity-catalog, metric-views, genie-agents, mlflow-evaluation, synthetic-data-gen, and more) |

The scanner is registry-agnostic and just parses `upstream_sources` entries.
Skills should pick **one** of these styles:

- **Structured `upstream_sources`** — for skills that genuinely derive from or
  extend an upstream skill. Scanner audits this for sync drift.
- **Lightweight `## See Also` footer** — for skills that merely point at an
  upstream registry as an authoritative reference. Not tracked by the scanner.

This audit checks whether upstream sources have changed since the skill was
last synced.

```
1. Run scan script to find skills with stale last_synced dates
2. For each skill with upstream_sources:
   a. Read the skill's upstream_sources from frontmatter
   b. For each upstream path, WebFetch the raw GitHub URL:
      https://raw.githubusercontent.com/{repo}/main/{path}
   c. Compare key patterns against the skill's current content
   d. Check for new patterns, deprecated approaches, or API changes in upstream
3. Report upstream drift grouped by relationship type (derived > extended > reference)
4. After syncing, update last_synced date and sync_commit in the skill frontmatter
```

**Lineage Map:**

- [references/databricks-agent-skills-lineage-map.md](references/databricks-agent-skills-lineage-map.md) — all skills mapped to their upstream `databricks/databricks-agent-skills` sources.

**Priority by relationship type:**

| Relationship | Sync Priority | Reasoning |
|---|---|---|
| `derived` | High | Skill directly draws from upstream; changes likely require updates |
| `extended` | Medium | Skill extends upstream; check for new base patterns |
| `inspired` | Low | Heavily customized; check for major direction changes only |
| `reference` | Low | Original content; check for API/pattern accuracy only |

### Upstream Drift Report Format

When upstream drift is detected, report in this format:

```markdown
## Upstream Drift Report: {skill-name}

**Skill:** `data_product_accelerator/skills/{domain}/{skill-name}/SKILL.md`
**Upstream:** `{repo}` → `{path}`
**Relationship:** {derived|extended|inspired|reference}
**Last Synced:** {date} (commit: {hash})
**Status:** UPSTREAM DRIFT DETECTED

### Changes in Upstream:
1. **{Pattern Name}** — {description of what changed upstream}
   - **Our skill says:** {current pattern in our skill}
   - **Upstream says:** {new pattern in upstream}
   - **Impact:** {high|medium|low} — {why this matters}

### Recommended Actions:
- [ ] Update {section} to align with upstream {pattern}
- [ ] Add new {capability} from upstream
- [ ] Update `last_synced` and `sync_commit` in frontmatter
```

---

## Critical Rules

### 1. Always Update `last_verified` After Verification

Even if no changes are needed, update the date. This proves the skill was checked:

```yaml
# Before verification
metadata:
  last_verified: "2025-11-15"

# After verification (no changes needed)
metadata:
  last_verified: "2026-02-07"
```

### 2. Verification Sources Are Verification Anchors, Not Auto-Updaters

The URLs don't automatically update the skill. They give the agent a **ground truth** to compare against when prompted. The agent must:
- Fetch the URL content
- Compare key patterns against the skill's instructions
- Report differences
- Wait for human approval before updating skill content

### 3. Prioritize High-Volatility Skills

When time is limited, always audit high-volatility skills first. A stale GenAI agent pattern can cause implementation failures; a stale ERD pattern is cosmetic.

### 4. Report Format for Drift

When drift is detected, report in this format:

```markdown
## Drift Report: {skill-name}

**Skill:** `data_product_accelerator/skills/{domain}/{skill-name}/SKILL.md`
**Last Verified:** {date}
**Volatility:** {high|medium|low}
**Status:** DRIFT DETECTED

### Changes Found:
1. **{Pattern Name}** — {description of what changed}
   - **Skill says:** {current pattern in skill}
   - **Docs say:** {current pattern in docs}
   - **Impact:** {high|medium|low} — {why this matters}

### Recommended Updates:
- [ ] Update {section} with new {pattern}
- [ ] Add deprecation warning for {old pattern}
- [ ] Add new {capability} section
```

---

## Scanning for Stale Skills

### Using the Scan Script

The scanner walks the entire repository by default, discovering every `SKILL.md`
under the supplied root and grouping skills by domain (`data_product_accelerator/<sub>`,
`genai-agents/<sub>`, `apps_lakebase`, etc.). Reference / asset / build / vendored
subtrees are excluded automatically.

```bash
# Repo-wide scan from the repo root
python data_product_accelerator/skills/admin/skill-freshness-audit/scripts/scan_skill_freshness.py

# Override the root or add custom excludes (fnmatch globs against the relative path)
python data_product_accelerator/skills/admin/skill-freshness-audit/scripts/scan_skill_freshness.py \
    --root /path/to/repo \
    --exclude '*/sandbox/*' --exclude '*tmp*'
```

The scanner exits with a non-zero status if any skill is stale, making it CI-friendly.

### Domain attribution

Domains are derived from the path:

- `apps_lakebase/skills/<id>/SKILL.md` → `apps_lakebase`
- `genai-agents/<group>/<id>/SKILL.md` → `genai-agents/<group>` (e.g. `genai-agents/foundation`)
- `data_product_accelerator/skills/<domain>/<id>/SKILL.md` → `<domain>` (e.g. `ml`, `silver`, `admin`)

### Manual Scan Pattern

If you prefer to scan manually:

```
1. Glob all SKILL.md files repo-wide: **/SKILL.md
   Exclude: .git, node_modules, dist, build, .venv, presentations,
            retrospectives, assets, references
2. For each, read the frontmatter metadata section
3. Extract last_verified, volatility
4. Calculate days_since_verified = today - last_verified
5. Compare against threshold: high=30, medium=90, low=180
6. Report any skill where days_since_verified > threshold
```

---

## Verification Source Patterns

### What to Check For Each Domain

| Domain | Key Verification Points |
|---|---|
| **GenAI Agents** | ResponsesAgent API signature, tracing span types, OBO auth flow, Lakebase API, evaluate() parameters |
| **Semantic Layer** | Metric view YAML syntax, TVF parameter types, Genie API endpoints, Conversation API schema |
| **Monitoring** | Monitor creation API, custom metric syntax, dashboard JSON schema, alert API v2 |
| **Silver** | DLT expectation decorators, expectation patterns URL, DQX version/API |
| **Gold** | Constraint syntax (PK/FK), MERGE statement patterns, CLUSTER BY AUTO syntax |
| **ML** | MLflow experiment API, model registry API, Feature Store API, LoggedModel API |
| **Infrastructure** | Asset Bundle YAML schema, job task types, serverless config |

**Full verification source mapping:** See [references/verification-sources.md](references/verification-sources.md)

---

## Integration with Self-Improvement

This skill complements `admin/self-improvement`:

- **Self-Improvement** = reactive (triggers on errors during implementation)
- **Skill Freshness Audit** = proactive (triggers on schedule or platform release)

When this audit finds drift, use the self-improvement workflow to apply the updates:
1. This skill **detects** the drift
2. Self-improvement skill **applies** the fix (update existing skill > create new)

---

## Validation Checklist

Before marking a skill as "verified":

- [ ] All `verification_sources` URLs fetched and compared
- [ ] API signatures in skill match current documentation
- [ ] No deprecated features still recommended without warnings
- [ ] No new major capabilities missing from skill
- [ ] Code examples still compile/run correctly
- [ ] `last_verified` date updated in frontmatter
- [ ] If skill has `upstream_sources`, check upstream for changes since `last_synced`
- [ ] If upstream changes found, update skill content and `last_synced` / `sync_commit`
- [ ] Version history entry added if changes were made

---

## Additional Resources

- [Verification Sources Master List](references/verification-sources.md) — All skills mapped to their verification URLs
- [Databricks Agent Skills Lineage Map](references/databricks-agent-skills-lineage-map.md) — All skills mapped to their upstream `databricks/databricks-agent-skills` sources
- [Volatility Classification](references/volatility-classification.md) — Complete volatility ratings for all skills
- [Verification Metadata Template](assets/templates/verification-metadata.yaml) — Copy-paste frontmatter template (includes `upstream_sources`)
- [Scan Script](scripts/scan_skill_freshness.py) — Automated staleness and upstream sync scanner (repo-wide, multi-domain)

## Version History

| Date | Changes |
|---|---|
| Aug 30, 2026 | Consolidated to a single upstream registry: `databricks/databricks-agent-skills` (32-skill manifest) now covers all accelerator + platform lineage. Retired the `databricks-solutions/ai-dev-kit` lineage map and remapped every `upstream_sources` entry (slug renames: `databricks-genie`→`databricks-genie-agents`, `databricks-asset-bundles`→`databricks-dabs`, `databricks-synthetic-data-generation`→`databricks-synthetic-data-gen`, `databricks-spark-declarative-pipelines`→`databricks-pipelines`, `databricks-config`→`databricks-core`) |
| Apr 27, 2026 | Repo-wide scanner extension (`--root` / `--exclude`, multi-domain attribution); `databricks/databricks-agent-skills` registered as an authoritative upstream registry (later consolidated as the single registry) |
| Feb 9, 2026 | Added upstream_sources lineage tracking: initial lineage map, upstream source audit workflow, upstream drift report format, scan script upstream sync support |
| Feb 7, 2026 | Initial creation: audit workflow, verification anchors, volatility classification, scan script |
