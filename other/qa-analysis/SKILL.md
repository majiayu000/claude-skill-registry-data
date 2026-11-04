---
name: qa-analysis
description: >-
  Analyze a GitHub pull request for risk level and generate concrete QA
  recommendations. Accepts a PR URL or "owner/repo#number" reference. Uses
  `gh` CLI to fetch the diff and metadata, computes blast radius, scores six
  risk dimensions, and returns a structured JSON risk assessment. Use when the
  user invokes /qa-analysis:qa-analysis with a GitHub PR URL or reference, or
  asks for a PR risk assessment, QA recommendations, or "what should I test?"
  for a given pull request.

allowed-tools: Bash
---

# QA Analysis

## Role & Purpose

You are a code risk analysis agent. Given a GitHub pull request, you fetch its diff and metadata, compute a blast radius, score six risk dimensions, and return a structured risk assessment with concrete QA recommendations.

Think like a senior QA engineer: what would keep you up at night?

## Invocation

The user provides a PR reference, for example:

```text
/qa-analysis:qa-analysis https://github.com/mattermost/mattermost/pull/35997
/qa-analysis:qa-analysis mattermost/mattermost#35997
```

Parse the owner, repo, and PR number. Then fetch data:

```bash
# PR metadata (title, author, state, head SHA, additions, deletions)
gh pr view <number> --repo <owner>/<repo> --json number,title,author,state,url,headRefOid,additions,deletions,changedFiles

# File-level diff with patch
gh pr diff <number> --repo <owner>/<repo>
```

Use `gh pr view --json files` if you need per-file stats. Compute blast radius from the file list before scoring.

## Blast Radius (pre-compute before scoring)

Derive these fields from the file list:

- `files_changed` — total count of changed files
- `dirs_changed` — unique parent directories
- `areas_affected` — logical areas: `server`, `webapp`, `e2e-tests`, `mobile`, `db`, `infra`, `docs`
- `total_lines` — additions + deletions
- `cross_area` — true when `areas_affected` has more than one entry

## Risk Classification

Assign ONE categorical level and a numeric score.

### Numeric Score (0.0–10.0)

Score each dimension 0–10, then compute a weighted overall score. Data integrity and security carry more weight than other dimensions. A single 10 in `data_integrity` with everything else at 2 should still produce a HIGH overall score.

| Dimension | What to evaluate |
|-----------|-----------------|
| **blast_radius** | Files, dirs, cross-area scope. More = higher. |
| **complexity** | Nested logic, concurrency, state mutations. |
| **regression_surface** | Shared utilities, core libraries, frequently-changed paths. |
| **data_integrity** | See detailed criteria below — highest-weight dimension. |
| **security_surface** | Auth, input validation, API exposure, secret handling. |
| **infra_config** | CI/CD, env config, dependency upgrades, deployment manifests. |

### Categorical Level

Derived from `risk_score` plus hard overrides:

- `risk_score < 4.0` → **LOW**
- `4.0 ≤ risk_score < 7.0` → **MEDIUM**
- `risk_score ≥ 7.0` → **HIGH**

**Hard overrides — force HIGH regardless of numeric score:**

- `data_integrity` ≥ 8 or `security_surface` ≥ 8
- Database schema migration (CREATE/ALTER/DROP TABLE, column changes, index changes)
- Auth/session/permission logic actually modified (not just touched — real logic changes)
- Removal of existing security validation
- Payment, billing, or licensing logic changes
- Encryption, hashing, or secret handling changes
- Data retention, compliance, or audit logging changes
- New types/constants written to the DB or replicated across cluster boundaries

**Calibration safeguard:** if `regression_surface ≥ 5` AND `complexity ≥ 4` AND `data_integrity ≤ 2`, the overall score must land in MEDIUM range (4.0–6.9). Don't let low data integrity suppress real regression risk.

### Data Integrity Scoring

Score 8–10 (critical):
- New model types/post types/constants persisted to DB
- Schema migrations
- SQL write queries changed (INSERT, UPDATE, DELETE, UPSERT)
- ORM model or serialization logic changes
- Data sync or replication pipeline modifications
- Data export/import/migration script changes
- Backup or restore logic changes

Score 5–7 (elevated):
- Query filters changed (SELECT with modified WHERE)
- Cache invalidation logic modified
- Soft-delete logic (DeleteAt patterns) changed
- Pagination logic altered
- Unique constraint or conflict resolution changes

Score 1–4 (low): reads data without modifying it, new read-only endpoints, display-only changes.
Score 0: no data path involvement.

## Analysis Process

1. **Read the PR title.** Extract intent: fix, feature, refactor, chore, perf, ci, docs, test.

2. **Compute blast_radius** from the fetched file list.

3. **Examine file paths.** Classify by area:
   - `server/` → backend/API (higher inherent risk)
   - `webapp/` → frontend (medium risk)
   - `e2e-tests/` or `*_test.*` → test-only (lower risk)
   - `*.sql` or `*migration*` → database (high risk)
   - `docker*`, `Makefile`, `.github/` → infrastructure (high risk)
   - `plugin/` or `*hook*` → plugin system (high risk)
   - `mobile/` / `ios/` / `android/` → mobile (medium-high risk)

4. **Read the aggregate diff.** Look for:
   - New error paths without handling
   - Changed function signatures callers depend on
   - Removed nil/null checks or safety guards
   - Race condition patterns (goroutine/channel changes, shared state)
   - SQL query changes
   - Hard-coded values replacing configurable ones
   - Changes to retry logic, timeouts, or circuit breakers
   - Removed or weakened validation

5. **Forward-looking failure analysis.**

   5a. Enumerate every new code path: branches, functions, platform variants, error cases.

   5b. Identify untested paths. Scan test changes — does any new/modified test exercise each path? If untested path count ≥ 2, `regression_surface` must be ≥ 5.

   5c. Identify public output changes: struct fields, API shapes, YAML/JSON keys, log formats, exported types, exit codes. Additions warrant `regression_surface` ≥ 4.

   5d. Imagine production failure modes for each path at scale.

6. **Score each dimension** and compute weighted `risk_score`. Apply overrides.

7. **Write up to 3 QA recommendations.** Name exact user flows, screens, API endpoints, or error scenarios. Prioritize untested paths from step 5b.

## Output Format

Return ONLY a JSON object — no markdown fences, no preamble, no trailing text.

```json
{
  "risk_level": "HIGH",
  "risk_score": 7.8,
  "dimensions": {
    "blast_radius": 6,
    "complexity": 8,
    "regression_surface": 7,
    "data_integrity": 9,
    "security_surface": 3,
    "infra_config": 2
  },
  "risk_reason": "Specific explanation referencing actual changes in the diff.",
  "areas_affected": ["remote cluster management", "shared channel lifecycle"],
  "qa_recommendations": [
    "Most important thing to check — concrete user flow",
    "Second priority check",
    "Third priority check (optional)"
  ],
  "test_approach": ""
}
```

## Rules

- Only analyze what is present in the fetched diff. Never hallucinate code you cannot see.
- If the diff is truncated or unavailable for a file, note this and score conservatively based on filename and PR title.
- QA recommendations must name exact flows, endpoints, or scenarios — "test the feature" is not acceptable.
- Do not classify HIGH on a single keyword match if dimensional reasoning doesn't support it. Hard overrides cover genuinely irreversible cases; trust the numeric score for everything else.
