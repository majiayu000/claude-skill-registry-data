---
name: infer-research-from-code
description: For every domain in the upstream domain-selection proposal, derive a product-scoped research Markdown file from scan-index.json evidence plus the canonical domain KB, carrying the five KB-extension sections with inline knowledge_gap markers wherever code evidence is absent.
version: 0.1.0
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# infer-research-from-code

Called by `product-keeper` during `/codify`, strictly after
`infer-domain-selection-from-code` has produced `specification/domain-selection.yaml`.
Produces one `research/{domain}.md` per selected domain at
`{stm_base}/{issue}/evidence/codify/proposals/research/{domain}.md`.

## Purpose

In greenfield, `research/{domain}.md` is copied from the canonical KB during
`/specify` Stage 3 and extended by research agents. In `/codify` the codebase
is the evidence surface — no prior product LTM, no web research. This skill
derives each domain's research document from scan-index.json signals attributed
to that domain, the canonical KB entry (when one exists), and any ADR / README
material matching the domain's search patterns. Every output carries the five
KB-extension sections from `core/components/memory/standards/rules/kb-extension.md`;
where scan evidence cannot populate a section, it is emitted with an inline
`knowledge_gap: true` marker so `/garura:enrich` surfaces the gap rather than silently
resolving it. Tier-2 inference, `learning_category: domain`, `sub_category: null`.

## Input

Receive from the /codify play orchestrator via JSON contract. All paths absolute.

| Field | Required | Description |
|-------|----------|-------------|
| `scan_index_path` | yes | `scan-index.json` produced by `scan.py`. |
| `stm_base` | yes | STM root from `stm.base-path` in `.garura/core/config.yaml`. |
| `issue` | yes | Issue number (STM namespace). |
| `related_proposal_paths` | yes | MUST contain the absolute path to `specification/domain-selection.yaml`. Missing → `missing_related_proposal`. |
| `kb_domain_dir` | yes | `core/components/memory/knowledge/domain/`. Missing → `kb_domain_dir_missing`. |
| `output_dir` | yes | `{stm_base}/{issue}/evidence/codify/proposals/research/`. One `{domain}.md` per selected domain lands here. |
| `decision_manifest_path` | yes | `{…}/proposals/research/decision-manifest-infer-research.yaml`. |
| `resolution_trace_path` | yes | `{…}/proposals/research/resolution-trace-infer-research.yaml`. |
| `ltm_context` | yes | Resolution Protocol context (`product_base`, `kb_base`, resolved LTM paths). |

## Process

### 1. Validate inputs

- `scan_index_path` exists and parses as JSON with `manifests`, `patterns`,
  `config_files`, `docs`, `git`. Missing → `scan_index_missing`.
- `related_proposal_paths` includes an existing `domain-selection.yaml`.
  Missing → `missing_related_proposal`.
- `kb_domain_dir` exists with ≥1 non-underscore `.md` file. Missing →
  `kb_domain_dir_missing`.
- `output_dir` is creatable. Failure → `output_path_unwritable`.

### 2. Resolution Protocol walk (R1–R3, R4 skipped)

Per `core/components/memory/standards/rules/resolution.md`. Write every probe
to `resolution_trace_path` with `source`, `path`, `outcome`, payload.

- **R1 — STM.** Skipped (codify bootstrap). Record reason `"codify-bootstrap"`.
- **R2 — Product LTM.** Probe `{product_base}/research/{domain}.md` per
  selected domain. If present AND LOCKED, propose only when scan evidence
  materially conflicts; non-conflicts emit `alignment_confirmed: true` in
  frontmatter and skip the body.
- **R3 — KB.** Per selected_domain in `domain-selection.yaml`:
  `inferred_domain_new: false` → read `{kb_domain_dir}/{domain}.md` to inherit
  canonical feature IDs, search patterns, and five-section structure.
  `inferred_domain_new: true` → no KB base; structure directly from
  `kb-extension.md` and emit `knowledge_gap: true` on every section without
  a code signal.
- **R4 — Web.** Not invoked. Gaps route through `/garura:enrich` to a human.

### 3. Attribute scan evidence per domain

Replay the signal → domain mapping used by `infer-domain-selection-from-code`,
persisting per-signal evidence under the owning domain:

- `patterns.framework_idioms` tagged for this domain (express → `backend-api`).
- `patterns.naming_suffix_counts` whose suffix is typical for the domain
  (`*Controller`/`*Service` → `backend-api`; `*Screen`/`*Page` → `frontend-web`).
- `patterns.test_framework_signals` whose test files sit under paths
  implicated by the domain's source files.
- `config_files.*` associated with the domain (Dockerfile → containerized
  runtimes; `.github/workflows` → `engineering-experience`; helm → `deployment`).
- `docs.adrs` whose title contains the domain's search-pattern tokens (from
  KB base for canonical domains; derived from slug + triggering readme
  excerpt for new domains).
- `docs.readme_preview` sections whose heading or surrounding paragraph
  matches the domain's search patterns — record matched span and line.
- `manifests` deps mapped to the domain (Stripe → `payments`; Auth0/Clerk
  → `user-management`; etc.).
- `git.churn_top` is used ONLY for `Experiential`; never as membership evidence.

Every item carries a concrete evidence path (JSON pointer or file path) and,
where applicable, a literal excerpt ≤ 200 chars.

### 4. Author `research/{domain}.md` — five required sections

Per selected domain emit Markdown: YAML frontmatter (Section 5), short prose
preamble, five KB-extension sections in order. Each section states
`inferred: true` and emits inline `knowledge_gap: true` bullets rather than
fabricating content when evidence is absent.

- **Inclusion** — MUST cite scan evidence (e.g., "Express middleware + 
  `*Controller` suffix present → backend-api included"). `knowledge_gap: true`
  is NOT permitted here; a domain without inclusion justification would not
  be in `selected_domains`.
- **Success Criteria** — derived from detected test patterns and assertion
  counts where attributable. Otherwise emit one bullet: `- knowledge_gap:
  true — no measurable success criteria observable from scan; defer to /garura:enrich`.
- **Failure Scenarios** — derived from try/catch clusters, error-taxonomy
  modules, or ADRs naming failure modes. Usually absent; emit
  `knowledge_gap: true` with pointers to insufficient-but-present signals
  (ADR titles, churn clusters) as leads.
- **Cross-Tree Refs** — derived from co-change clusters in `git.churn_top`
  and cross-domain imports in `manifests` / `entry_points`. If no cross-tree
  signal exists, emit `- (none observed)` — a valid finding, NOT a
  knowledge_gap.
- **Experiential** — ADR titles matching search patterns, README notes under
  the domain's umbrella, and long-lived churn clusters (`git.churn_top`
  entries with earliest commit > 180 days old). `Usage count` bootstraps to
  0; `Last promoted: never`. If no ADR / README / churn match, emit
  `knowledge_gap: true` on Scenarios-observed and Common-mistakes sub-bullets.

### 5. YAML frontmatter meta block

Every file begins with:

```yaml
---
source_type: "inferred_from_code"
evidence:
  - "<scan-index JSON pointer or file path>"
  - "..."
confidence: "high" | "medium" | "low"
learning_category: "domain"
sub_category: null
tier: 2
domain: "<slug>"
inferred_domain_new: <bool>
alignment_confirmed: <bool>   # true only when R2 hit LOCKED with no conflict
knowledge_gap_sections:       # explicit catalog of gap-marked sections
  - "Success Criteria"
  - "Failure Scenarios"
---
```

Confidence uses the same tiers as `infer-domain-selection-from-code`, computed
per-domain from the signal count in THIS research file.

### 6. Write artifacts + decision manifest

Write every `research/{domain}.md` first, then the decision manifest, then the
resolution trace. The manifest lists every section-level inference — one entry
per (domain, section) derived from evidence AND one entry per (domain, section)
emitted as `knowledge_gap: true`. Per Decision Surfacing Discipline each entry
carries `decision_id`, `decision_type`, `tier` (low for knowledge_gap, mid/high
for evidenced), `grounding_source`, `recommendation`, `alternatives`,
`chosen_reason`. Nothing silently resolved.

## Output

**Primary artifacts — `research/{domain}.md` (one per selected domain):**
YAML frontmatter meta block + prose preamble + five KB-extension sections
(Inclusion, Success Criteria, Failure Scenarios, Cross-Tree Refs, Experiential).
Sections with no code evidence carry inline `knowledge_gap: true` markers;
sections with evidence cite concrete scan-index pointers or file paths.

**Decision manifest — `decision-manifest-infer-research.yaml`:** standard
Garura shape (`schema_version`, `skill`, `generated_at`, `decisions[]`); one
entry per (domain, section) inference or knowledge_gap.

**Resolution trace — `resolution-trace-infer-research.yaml`:** R1..R3 probes
with `source`, `path`, `outcome`, payload. R4 omitted.

### Return contract

```yaml
status: success
artifact_paths: [ "<output_dir>/<domain>.md", "..." ]
decision_manifest_path: "<decision_manifest_path>"
resolution_trace_path: "<resolution_trace_path>"
research_file_count: <int>
knowledge_gap_section_count: <int>
overall_confidence: "high" | "medium" | "low"
alignment_confirmed_count: <int>
```

## Failure Modes

Emit `status: failure` with `what_failed`, `detail`, and `evidence` (offending
path / field). Codes:

- `missing_related_proposal` — `related_proposal_paths` lacks an existing
  `domain-selection.yaml`.
- `kb_domain_dir_missing` — `kb_domain_dir` absent or empty.
- `scan_index_missing` — `scan_index_path` absent or not valid JSON.
- `insufficient_signal` — domain-selection declares domains but every
  per-domain evidence bundle is empty; would produce pure knowledge_gap
  stubs. Fall back to /garura:enrich.
- `output_path_unwritable` — `output_dir` cannot be created.

## Boundaries

- Read-only against `scan_index_path`, `kb_domain_dir`, and `related_proposal_paths`.
- Emits proposals, never canonical LTM. Promotion from STM proposals to
  `.garura/product/research/` is handled downstream by `/garura:enrich`.
- Does NOT re-run `scan.py`, consult the web, or modify the canonical KB even
  when `inferred_domain_new: true` — new canonical entries are created only
  after human promotion.
