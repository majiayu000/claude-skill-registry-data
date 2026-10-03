---
name: cortivex-cross-repo
version: 1.0.0
description: Cross-repository intelligence layer that transfers learned insights between repositories through technology fingerprinting, pattern matching, and privacy-safe sharing
category: learning
tags: [cross-repo, global-insights, fingerprinting, pattern-library, similarity, privacy, sharing]
author: Cortivex
requires: [cortivex MCP server, cortivex-learn]
capabilities: [tech-fingerprinting, insight-promotion, similarity-matching, global-registry, privacy-filtering, pattern-library]
---

# Cortivex Cross-Repository Intelligence

You have access to a cross-repository intelligence system that transfers proven insights between repositories. While `cortivex-learn` records insights scoped to a single repo, this system promotes high-confidence insights to a global registry, matches them to new repositories by technology fingerprint, and applies them as suggestions -- never as overrides.

## Overview

The problem: teams running Cortivex across multiple repositories rediscover the same optimizations independently. A team using Express.js learns that middleware-chain security scanning reduces false positives by 40%. Another Express.js team learns the same thing three weeks later. Cross-repo intelligence eliminates this redundancy by maintaining a global pattern library where anonymized, high-confidence insights are shared across repositories with similar technology profiles.

The system has three layers:

1. **Local insights** (from `cortivex-learn`) -- scoped to a single repository. Always authoritative.
2. **Global insights** (from cross-repo) -- promoted from local insights after anonymization. Treated as suggestions.
3. **Pattern library** -- curated, community-validated patterns tied to specific technology stacks.

Local always wins. If a global insight contradicts a local insight, the local insight takes precedence without exception.

## When to Use

- When onboarding a new repository into Cortivex and you want to bootstrap with relevant insights from similar projects
- When a local insight has been validated across enough runs (10+) that it likely generalizes to other repos with the same tech stack
- When you want to check whether a known optimization pattern exists for your repo's technology profile before running an expensive pipeline
- When sharing anonymized learnings with other teams or the broader community
- When analyzing a monorepo with multiple sub-projects that share technology stacks

## When NOT to Use

- For insights that are inherently repo-specific (e.g., "file X has unusual import structure"). These should remain local.
- When the insight depends on proprietary code structure, internal APIs, or business logic that does not generalize.
- When the user has not opted in to sharing. Cross-repo sharing is strictly opt-in.
- For repositories with fewer than 5 pipeline runs. There is not enough local signal to promote.
- When privacy controls have not been verified. Never promote an insight before running `privacy_check`.

## How It Works

### Technology Fingerprinting

When a repository is first analyzed, the system generates a technology fingerprint by inspecting:

- **Package manifests**: `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `Gemfile`
- **Framework markers**: directory structures (`src/pages/` for Next.js, `app/controllers/` for Rails), config files (`.eslintrc`, `tsconfig.json`, `django-settings.py`)
- **Build tools**: `webpack.config.js`, `vite.config.ts`, `Makefile`, `Dockerfile`
- **Testing frameworks**: `jest.config.js`, `pytest.ini`, `.mocharc.yml`, `vitest.config.ts`
- **CI/CD**: `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`

The fingerprint is a structured profile, not a hash of file contents. No source code is read or stored -- only the presence and type of configuration files.

```
cortivex_crossrepo({
  action: "fingerprint",
  repo: "/path/to/repo"
})
```

**Response:**

```json
{
  "fingerprint": {
    "id": "fp-8a3b2c",
    "primary_language": "typescript",
    "frameworks": ["express", "react"],
    "build_tools": ["webpack", "babel"],
    "test_frameworks": ["jest"],
    "ci_cd": ["github-actions"],
    "package_manager": "npm",
    "monorepo": false,
    "markers": {
      "has_typescript": true,
      "has_orm": true,
      "orm_type": "prisma",
      "has_docker": true,
      "has_linter": true,
      "linter_type": "eslint"
    },
    "confidence": 0.94
  }
}
```

### Similarity Matching

Given a fingerprint, the system finds repositories in the global registry with similar technology profiles and retrieves their applicable insights:

```
cortivex_crossrepo({
  action: "match",
  fingerprint_id: "fp-8a3b2c",
  min_similarity: 0.70,
  max_results: 10
})
```

**Response:**

```json
{
  "matches": [
    {
      "registry_id": "reg-4d5e6f",
      "similarity": 0.92,
      "shared_traits": ["express", "typescript", "prisma", "jest", "github-actions"],
      "differing_traits": ["react vs vue"],
      "applicable_insights": 7,
      "top_insights": [
        {
          "id": "gi-1a2b",
          "type": "reorder",
          "description": "Express.js repos benefit from running SecurityScanner after CodeReviewer because middleware-chain analysis on reviewed code eliminates 40% of false positives",
          "global_confidence": 0.88,
          "observed_in_repos": 23,
          "tech_scope": ["express", "typescript"]
        },
        {
          "id": "gi-3c4d",
          "type": "adjust_config",
          "description": "Prisma-based repos should set scan_depth to deep for SecurityScanner because ORM-generated queries need schema-aware analysis",
          "global_confidence": 0.82,
          "observed_in_repos": 15,
          "tech_scope": ["prisma"]
        }
      ]
    },
    {
      "registry_id": "reg-7g8h9i",
      "similarity": 0.78,
      "shared_traits": ["express", "typescript", "jest"],
      "differing_traits": ["prisma vs sequelize", "webpack vs vite"],
      "applicable_insights": 4
    }
  ]
}
```

### Insight Promotion

Promoting a local insight to the global registry is an explicit, user-initiated action. The system anonymizes the insight before publishing:

```
cortivex_crossrepo({
  action: "promote",
  insight_id: "ins-7a3b",
  repo: "/path/to/repo"
})
```

The promotion pipeline:

1. **Eligibility check** -- Insight must have confidence >= 0.80 and sample_size >= 10.
2. **Privacy filter** -- Strips file paths, repo names, branch names, author names, code snippets. Retains only structural patterns and technology tags.
3. **Generalization** -- Converts repo-specific language to tech-stack-scoped language. "In repo X, running CodeReviewer before SecurityScanner..." becomes "In Express.js/TypeScript repos, running CodeReviewer before SecurityScanner..."
4. **Deduplication** -- Checks if a semantically equivalent insight already exists in the global registry. If so, increases the existing insight's observation count instead of creating a duplicate.
5. **Publication** -- Adds the anonymized insight to the global registry with the repo's technology fingerprint as scope.

**Response:**

```json
{
  "status": "promoted",
  "global_insight_id": "gi-1a2b",
  "anonymization_report": {
    "fields_stripped": ["repo_path", "branch_name", "file_paths"],
    "fields_generalized": ["description", "scope"],
    "privacy_score": 1.0
  },
  "deduplicated": false,
  "tech_scope": ["express", "typescript"]
}
```

### Importing Global Insights

When starting work on a new or existing repository, import applicable global insights as local suggestions:

```
cortivex_crossrepo({
  action: "import",
  repo: "/path/to/repo",
  fingerprint_id: "fp-8a3b2c",
  min_global_confidence: 0.75,
  max_imports: 20
})
```

**Response:**

```json
{
  "imported": 5,
  "insights": [
    {
      "local_id": "ins-imported-1",
      "global_id": "gi-1a2b",
      "type": "reorder",
      "description": "Express.js repos benefit from running SecurityScanner after CodeReviewer because middleware-chain analysis on reviewed code eliminates 40% of false positives",
      "global_confidence": 0.88,
      "local_confidence": null,
      "status": "suggestion",
      "source": "global_registry",
      "observed_in_repos": 23
    }
  ],
  "skipped": [
    {
      "global_id": "gi-9x0y",
      "reason": "conflicts_with_local",
      "local_insight_id": "ins-4e5f",
      "explanation": "Local insight contradicts this global insight. Local takes precedence."
    }
  ]
}
```

Imported insights start with `local_confidence: null` and `status: "suggestion"`. They are not applied automatically. As the local system observes runs, it updates the local confidence. If the local data confirms the global insight, confidence rises and it becomes eligible for automatic application. If local data contradicts it, the insight is marked as inapplicable for this repo.

### Browsing the Global Registry

```
cortivex_crossrepo({
  action: "registry",
  filter: {
    tech_scope: ["express"],
    min_confidence: 0.80,
    type: "reorder"
  },
  sort_by: "confidence",
  limit: 20
})
```

**Response:**

```json
{
  "total": 34,
  "insights": [
    {
      "id": "gi-1a2b",
      "type": "reorder",
      "description": "Express.js repos benefit from running SecurityScanner after CodeReviewer because middleware-chain analysis on reviewed code eliminates 40% of false positives",
      "global_confidence": 0.88,
      "observed_in_repos": 23,
      "tech_scope": ["express", "typescript"],
      "created_at": "2025-01-02T10:00:00Z",
      "last_confirmed": "2025-01-20T14:30:00Z"
    }
  ]
}
```

### Privacy Verification

Before any promotion, run an explicit privacy check:

```
cortivex_crossrepo({
  action: "privacy_check",
  insight_id: "ins-7a3b",
  repo: "/path/to/repo"
})
```

**Response:**

```json
{
  "safe_to_promote": true,
  "fields_checked": {
    "description": { "contains_paths": false, "contains_names": false, "contains_code": false },
    "evidence": { "contains_paths": false, "contains_names": false, "contains_code": false },
    "recommendation": { "contains_paths": false, "contains_names": false, "contains_code": false }
  },
  "warnings": [],
  "anonymization_preview": {
    "original_description": "Running CodeReviewer before SecurityScanner reduces duration by 22% in this repo",
    "anonymized_description": "In Express.js/TypeScript repos, running CodeReviewer before SecurityScanner reduces duration by approximately 20%"
  }
}
```

If any field contains identifiable information:

```json
{
  "safe_to_promote": false,
  "fields_checked": {
    "description": { "contains_paths": true, "contains_names": false, "contains_code": false }
  },
  "warnings": [
    "Description contains file path 'src/auth/login.ts'. This will be stripped during anonymization but verify the structural pattern is still meaningful without it."
  ]
}
```

## Pipeline Configuration

### Bootstrap Pipeline for New Repositories

```yaml
name: cross-repo-bootstrap
version: "1.0"
description: Fingerprint a new repo and import applicable global insights
nodes:
  - id: fingerprint
    type: CrossRepoAnalyzer
    config:
      action: fingerprint
      scan_manifests: true
      scan_configs: true
      scan_directory_structure: true

  - id: match
    type: CrossRepoAnalyzer
    depends_on: [fingerprint]
    config:
      action: match
      min_similarity: 0.70
      max_results: 10

  - id: import
    type: CrossRepoAnalyzer
    depends_on: [match]
    config:
      action: import
      min_global_confidence: 0.75
      max_imports: 20
      conflict_resolution: local_wins
```

### Post-Run Promotion Pipeline

```yaml
name: cross-repo-promote
version: "1.0"
description: After pipeline runs, promote eligible insights to global registry
nodes:
  - id: find_eligible
    type: CrossRepoAnalyzer
    config:
      action: find_promotable
      min_confidence: 0.80
      min_sample_size: 10

  - id: privacy_check
    type: CrossRepoAnalyzer
    depends_on: [find_eligible]
    config:
      action: privacy_check_batch
      strict_mode: true

  - id: promote
    type: CrossRepoAnalyzer
    depends_on: [privacy_check]
    config:
      action: promote_batch
      require_privacy_pass: true
      deduplicate: true
```

## Node Reference

```yaml
- id: crossrepo
  type: CrossRepoAnalyzer
  config:
    action: fingerprint           # fingerprint | match | import | promote | find_promotable | privacy_check | privacy_check_batch | promote_batch
    scan_manifests: true           # inspect package.json, requirements.txt, etc.
    scan_configs: true             # inspect framework config files
    scan_directory_structure: true  # inspect directory layout for framework markers
    min_similarity: 0.70           # minimum similarity score for match results (0.0-1.0)
    max_results: 10                # maximum number of match results
    min_global_confidence: 0.75    # minimum confidence for importing global insights
    max_imports: 20                # maximum number of insights to import per run
    conflict_resolution: local_wins  # local_wins | ask_user | highest_confidence
    min_confidence: 0.80           # minimum confidence for promotion eligibility
    min_sample_size: 10            # minimum observations for promotion eligibility
    strict_mode: true              # for privacy_check: fail on any identifiable data
    require_privacy_pass: true     # for promote: block promotion if privacy_check fails
    deduplicate: true              # merge with existing global insights if semantically equivalent
```

## Quick Reference

| Operation | MCP Tool | Description |
|-----------|----------|-------------|
| Fingerprint repo | `cortivex_crossrepo({ action: "fingerprint", repo })` | Detect technology stack and generate a structured profile |
| Find similar repos | `cortivex_crossrepo({ action: "match", fingerprint_id, min_similarity })` | Find repos with similar tech profiles in the global registry |
| Promote insight | `cortivex_crossrepo({ action: "promote", insight_id, repo })` | Anonymize and publish a local insight to the global registry |
| Import insights | `cortivex_crossrepo({ action: "import", repo, fingerprint_id })` | Pull applicable global insights into local repo as suggestions |
| Browse registry | `cortivex_crossrepo({ action: "registry", filter, sort_by, limit })` | Search and browse the global insight registry |
| Privacy check | `cortivex_crossrepo({ action: "privacy_check", insight_id, repo })` | Verify an insight is safe to promote (no PII, no code, no paths) |

## Best Practices

1. **Fingerprint every new repo on first run.** The fingerprint is lightweight (reads only manifests and config files, no source code) and enables all downstream cross-repo features. Without a fingerprint, the system cannot match or import.
2. **Import before your first pipeline run.** Global insights give you a head start. A suggestion to reorder nodes or adjust config can save significant cost on the very first run.
3. **Do not promote prematurely.** Wait for confidence >= 0.80 and at least 10 observations. Promoting weak signals pollutes the global registry and misleads other teams.
4. **Always run privacy_check before promote.** Even if you believe the insight is clean, the automated check catches things humans miss -- partial paths in descriptions, team names in evidence fields, branch names that reveal project structure.
5. **Review imported insights before applying.** Imported insights have `status: "suggestion"` for a reason. They are educated guesses based on similar repos, not proven facts about your repo. Let the local learning system validate them over several runs.
6. **Use tech_scope filters when browsing the registry.** The registry may contain thousands of insights. Filtering by your stack (e.g., `["express", "prisma"]`) returns only relevant results.
7. **Prefer narrow tech_scope over broad.** An insight scoped to `["express", "typescript", "prisma"]` is more reliable for your Express/TS/Prisma repo than one scoped to just `["typescript"]`.

## Reasoning Protocol

Before performing any cross-repo operation, reason through these questions:

1. **Is this insight truly generalizable?** A local optimization might work because of a specific file structure, team convention, or dependency version -- not because of the technology stack. Before promoting, ask: "Would this insight help a stranger's Express.js repo, or does it only work because of how this specific repo is structured?"

2. **Has the privacy filter been verified?** Even structural patterns can leak information. A description mentioning "the auth middleware at depth 4 in the chain" is structural, but combined with a technology fingerprint, it could identify a specific open-source project. When in doubt, generalize further.

3. **Am I importing too aggressively?** Importing 50 global insights into a new repo creates noise. Start with the top 5-10 highest-confidence insights that match your exact tech stack. Add more only after the first batch has been validated locally.

4. **Does a local insight already cover this?** Before importing a global insight, check if the local learning system already has an equivalent insight with higher confidence. Local data is always more reliable than global generalizations.

5. **Is the similarity score meaningful?** A 0.72 similarity might mean "same language, same test framework, different everything else." Check the `shared_traits` and `differing_traits` fields. Two repos that share only "typescript" and "jest" may have very different optimization profiles.

6. **Am I respecting the user's sharing preferences?** Promotion is opt-in. Never promote insights automatically, even if they meet the confidence threshold. Always confirm with the user before publishing to the global registry.

## Anti-Patterns

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| Auto-promoting insights without user consent | Violates opt-in sharing contract; erodes trust | Always require explicit user approval before calling `promote` |
| Importing global insights and applying them as if they were local | Untested generalizations may harm pipeline performance | Import as suggestions; let the local learning system validate over multiple runs |
| Promoting insights with fewer than 10 observations | Weak signals pollute the global registry with noise | Enforce `min_sample_size: 10` and `min_confidence: 0.80` as hard gates |
| Skipping privacy_check before promotion | File paths, team names, or code fragments leak into the global registry | Always run `privacy_check` and require a passing result before `promote` |
| Treating similarity score as the sole matching criterion | Two repos with 0.85 similarity may differ in the one trait that matters for an insight | Always inspect `shared_traits` and `differing_traits`; verify the insight's tech_scope is fully covered |
| Using global insights to override local insights | Global generalizations are less reliable than local observations | `conflict_resolution: local_wins` must be the default; global insights never override local ones |
| Promoting insights from repos with unusual configurations | Outlier repos produce insights that do not generalize | Exclude insights tied to non-standard setups (e.g., custom build chains, forked frameworks) |

**WRONG:**
```
# Promote everything above 0.60 confidence without asking
insights = cortivex_insights({ action: "query", repo, min_confidence: 0.60 })
for each insight in insights:
  cortivex_crossrepo({ action: "promote", insight_id: insight.id, repo })
```

This promotes too early (0.60 is below the 0.80 threshold), skips privacy checks, and does not ask the user. The global registry fills with unreliable, potentially identifying data.

**RIGHT:**
```
# Find eligible insights, verify privacy, ask the user, then promote
eligible = cortivex_crossrepo({ action: "find_promotable", min_confidence: 0.80, min_sample_size: 10 })

for each insight in eligible:
  privacy = cortivex_crossrepo({ action: "privacy_check", insight_id: insight.id, repo })
  if privacy.safe_to_promote:
    # Present to user with anonymization preview
    "Insight ins-7a3b is eligible for global sharing:
     Original: 'Running CodeReviewer before SecurityScanner reduces duration by 22% in this repo'
     Anonymized: 'In Express.js/TypeScript repos, running CodeReviewer before SecurityScanner reduces duration by ~20%'
     Share this insight globally? [Y/n]"
    # Only promote after user confirms
    if user_confirms:
      cortivex_crossrepo({ action: "promote", insight_id: insight.id, repo })
```

## Grounding Rules

When you encounter uncertainty in cross-repo operations, follow these rules:

- **Fingerprint detection is ambiguous.** If the system cannot confidently determine the tech stack (e.g., a repo with both `package.json` and `requirements.txt` and no clear primary language), ask the user to confirm the primary stack before matching. Do not guess -- an incorrect fingerprint produces irrelevant matches.

- **Global insight contradicts local data.** Local always wins. Do not attempt to reconcile or average the two. Mark the global insight as `inapplicable` for this repo and continue using local data. The global registry will not be affected -- the insight may still be valid for other repos.

- **No similar repos found in the registry.** This is expected for uncommon tech stacks or when the registry is young. Do not lower `min_similarity` below 0.60 to force matches. Instead, let the local learning system accumulate insights organically. Once this repo has enough validated insights, it can be the first contributor for its tech profile.

- **User wants to share but privacy_check fails.** Show the user exactly which fields contain identifiable data and what the anonymized version would look like. Let them decide whether to manually edit the insight description before re-running the check, or to skip promotion for this insight entirely. Never silently strip data and promote.

- **Imported insight performs poorly after several local runs.** If an imported suggestion is consistently contradicted by local data (local confidence drops below 0.30 after 5+ observations), automatically mark it as `inapplicable` and remove it from the suggestion list. Do not continue suggesting something that demonstrably does not work for this repo.

## Integration with cortivex-learn

Cross-repo extends the learning system from repository-scoped to global. The integration points are:

1. **Insight query** -- When `cortivex_insights({ action: "query" })` runs, it checks both local insights and imported global suggestions. Local insights are returned first; global suggestions are appended with `source: "global_registry"`.

2. **Insight recording** -- After each pipeline run, `cortivex_insights({ action: "record" })` stores data locally as before. If an imported global insight was applied during the run, the recording includes a `global_validation` field that tracks whether the global insight held up locally.

3. **Confidence evolution** -- Imported global insights start with `local_confidence: null`. As runs accumulate, local confidence is calculated independently of global confidence. The two scores are never merged.

4. **Promotion trigger** -- After `cortivex_insights({ action: "record" })` processes a new observation, it checks whether any local insight has crossed the promotion eligibility threshold (confidence >= 0.80, sample_size >= 10). If so, it flags the insight as `promotable` but does not promote automatically.

5. **Retirement sync** -- When a local insight is retired via `cortivex_insights({ action: "retire" })`, and that insight was previously promoted to global, the global registry is notified. If enough source repos retire the same global insight, its global confidence decays.

## Advanced Capabilities

Advanced cross-repo features for deep fingerprinting, propagation governance, dependency tracking, privacy-controlled sharing, and multi-repository analytics.

### Repository Fingerprinting & Classification

Advanced fingerprinting classifies repositories into architectural archetypes with maturity scores, enabling insight matching based on how a repo uses its technologies.

```json
{
  "tool": "cortivex_crossrepo_fingerprint",
  "request": { "action": "deep_fingerprint", "repo": "/path/to/repo", "include_architecture": true, "include_maturity": true }
}
```

```json
{
  "tool": "cortivex_crossrepo_fingerprint",
  "response": {
    "fingerprint_id": "fp-9d4e7f",
    "archetype": "api-service",
    "architecture_style": "layered-mvc",
    "maturity_score": 0.81,
    "classification": { "domain": "backend", "pattern": "rest-api", "complexity": "moderate", "test_coverage_tier": "high" },
    "technology_graph": {
      "runtime": ["node-18"], "frameworks": ["express-4", "react-18"],
      "data_layer": ["prisma-5", "postgresql"], "testing": ["jest-29", "supertest"]
    },
    "confidence": 0.96
  }
}
```

### Insight Propagation Rules
Propagation policies govern how insights flow between repositories, defining eligibility conditions, target constraints, and approval gates.

```yaml
propagation_policy:
  name: enterprise-propagation
  version: "2.0"
  rules:
    - id: high-confidence-auto
      conditions: { min_confidence: 0.92, min_observations: 25, min_source_repos: 5, privacy_check: required }
      target: { archetype_match: exact, min_similarity: 0.85 }
      approval: automatic
    - id: moderate-confidence-review
      conditions: { min_confidence: 0.80, min_observations: 10, privacy_check: required }
      target: { archetype_match: same_domain, min_similarity: 0.70 }
      approval: team_review
      review_timeout_days: 7
    - id: cross-domain-blocked
      conditions: { cross_domain: true }
      approval: admin_only
  decay:
    enabled: true
    half_life_days: 90
    min_reconfirmation_repos: 2
```

### Cross-Repo Dependency Tracking
Dependency tracking maps shared dependencies across repositories, flagging version mismatches that could invalidate transferred insights.

```typescript
interface DependencyGraphRequest {
  action: "build_dependency_graph";
  repos: string[];
  include_transitive: boolean;
  depth: number;
  filter_by?: { category?: "runtime" | "devDependency" | "peer"; min_shared_count?: number };
}
```

```json
{
  "tool": "cortivex_crossrepo_fingerprint",
  "request": { "action": "build_dependency_graph", "repos": ["fp-9d4e7f", "fp-8a3b2c", "fp-2x1y0z"], "depth": 2, "filter_by": { "min_shared_count": 2 } }
}
```

```json
{
  "tool": "cortivex_crossrepo_fingerprint",
  "response": {
    "graph_id": "dg-7k8m9n",
    "shared_dependencies": [
      { "package": "express", "repos_using": ["fp-9d4e7f", "fp-8a3b2c"], "versions": { "fp-9d4e7f": "4.18.2", "fp-8a3b2c": "4.19.0" }, "version_compatible": true },
      { "package": "prisma", "repos_using": ["fp-9d4e7f", "fp-8a3b2c", "fp-2x1y0z"], "versions": { "fp-9d4e7f": "5.4.1", "fp-8a3b2c": "5.4.1", "fp-2x1y0z": "4.16.0" }, "version_compatible": false, "insight_transfer_risk": "high" }
    ],
    "transfer_reliability": { "fp-9d4e7f_to_fp-8a3b2c": 0.91, "fp-9d4e7f_to_fp-2x1y0z": 0.64 }
  }
}
```

### Privacy-Aware Knowledge Sharing

Privacy filters redact, generalize, or block fields based on configurable sensitivity tiers before insights cross repository boundaries. Every share operation produces an audit log entry.

```json
{
  "tool": "cortivex_crossrepo_share",
  "request": {
    "action": "share_with_privacy", "insight_ids": ["ins-7a3b", "ins-9c2d"],
    "repo": "/path/to/repo", "privacy_profile": "strict",
    "filters": { "redact_patterns": ["internal-*", "*.corp.example.com"], "generalize_thresholds": true, "strip_exact_metrics": true, "allow_categories": ["reorder", "adjust_config"], "block_categories": ["custom_script", "file_specific"] }
  }
}
```

```json
{
  "tool": "cortivex_crossrepo_share",
  "response": {
    "shared": 1, "blocked": 1,
    "results": [
      { "insight_id": "ins-7a3b", "status": "shared", "global_id": "gi-5f6g", "transformations_applied": ["redacted 2 internal hostnames", "generalized '22% reduction' to '~20% reduction'"], "privacy_score": 1.0 },
      { "insight_id": "ins-9c2d", "status": "blocked", "reason": "category 'file_specific' is in block list" }
    ],
    "audit_log_entry": "audit-2026-03-23T10:15:00Z-share-7a3b"
  }
}
```

### Multi-Repository Analytics
Aggregate metrics across repositories to surface trends and cross-pollination opportunities. Results use anonymized repository identifiers unless the requester owns all queried repos.

```json
{
  "tool": "cortivex_crossrepo_fingerprint",
  "request": {
    "action": "aggregate_metrics",
    "scope": { "archetype": "api-service", "tech_scope": ["express", "typescript"], "min_repos": 5 },
    "metrics": ["avg_pipeline_duration", "insight_adoption_rate", "false_positive_rate"],
    "group_by": "architecture_style", "time_range": "last_90_days"
  }
}
```

```json
{
  "tool": "cortivex_crossrepo_fingerprint",
  "response": {
    "query_id": "aq-3p4q5r", "repos_analyzed": 42,
    "groups": [
      { "architecture_style": "layered-mvc", "repo_count": 28, "metrics": { "avg_pipeline_duration_seconds": 134.5, "insight_adoption_rate": 0.73, "false_positive_rate": 0.08 } },
      { "architecture_style": "hexagonal", "repo_count": 14, "metrics": { "avg_pipeline_duration_seconds": 98.2, "insight_adoption_rate": 0.81, "false_positive_rate": 0.05 } }
    ],
    "cross_group_insights": ["Hexagonal repos show 27% faster pipelines than layered-mvc with the same tech stack"],
    "anonymized": true
  }
}

## Security Hardening (OWASP AST10 Aligned)

Security controls for cross-repository intelligence aligned with the OWASP Automated Security Testing Top 10 risk framework.

### AST09: Mandatory Privacy Impact Assessment

No insight crosses a repository boundary without a completed Privacy Impact Assessment. This addresses AST09 (Insufficient Security Validation).

```yaml
privacy_impact_assessment:
  # AST09 -- Mandatory PIA before cross-repo sharing
  enforcement: pre_promotion_gate
  required_before: [promote, share_with_privacy, promote_batch]
  assessment_checks:
    - { id: pii_scan, scanner: regex_and_ner, fail_action: block_promotion }
    - { id: repo_identity_leak, scanner: fingerprint_reversibility, fail_action: block_promotion }
    - { id: code_fragment_detection, scanner: ast_pattern_matcher, fail_action: block_promotion }
    - { id: sensitivity_classification, scanner: data_classifier, fail_action: escalate_to_admin, ast_reference: "AST09" }
  on_failure: { action: block_and_notify, notify: [privacy-team, security-ops] }
```

```json
{
  "tool": "cortivex_crossrepo",
  "request": { "action": "promote", "insight_id": "ins-7a3b", "repo": "/path/to/repo" },
  "response": {
    "status": "blocked", "reason": "AST09: Privacy Impact Assessment required before promotion",
    "remediation": "Run cortivex_crossrepo({ action: 'privacy_impact_assessment', insight_id: 'ins-7a3b' }) first"
  }
}
```

### AST09: Fingerprint Anonymization Verification

Fingerprints must satisfy k-anonymity (min k=5) to prevent reverse-engineering of repository identity from technology profiles.

```yaml
fingerprint_anonymization:
  k_anonymity: { min_k: 5, enforcement: pre_match_gate }
  field_generalization:
    exact_version_numbers: generalize_to_major
    directory_structure_depth: max_2_levels
    custom_config_names: strip
    internal_hostnames: strip
  verification_checks:
    - { id: uniqueness_test, action: generalize_and_retry, max_retries: 3, ast_reference: "AST09" }
    - { id: quasi_identifier_scan, action: suppress_fields }
  on_failure: { action: block_fingerprint_sharing, fallback: "Use category tags only" }
```

```typescript
interface FingerprintAnonymizationResult {
  fingerprint_id: string;
  k_anonymity_score: number;
  meets_threshold: boolean;
  quasi_identifiers_found: Array<{ field_combination: string[]; uniqueness_risk: "low" | "medium" | "high" }>;
  generalized_fields: string[];
  ast_reference: "AST09";
}
```

### Propagation Rate Limiting

Rate limits prevent mass insight injection attacks where a compromised repo floods the global registry.

```yaml
propagation_rate_limits:
  per_repository: { max_promotions_per_hour: 5, max_promotions_per_day: 20, max_batch_size: 3 }
  global:
    max_promotions_per_hour: 50
    circuit_breaker: { enabled: true, trip_threshold: 100, trip_window_minutes: 15, reset_after_minutes: 30 }
  anomaly_detection:
    - { pattern: single_repo_burst, action: throttle_and_alert }
    - { pattern: coordinated_promotion, action: quarantine_all_and_alert, ast_reference: "AST09" }
```

```json
{
  "tool": "cortivex_crossrepo",
  "request": { "action": "promote", "insight_id": "ins-flood-12", "repo": "/path/to/repo" },
  "response": {
    "status": "rate_limited",
    "reason": "Propagation rate limit exceeded: 5/5 promotions this hour",
    "retry_after_seconds": 2340, "ast_reference": "AST09"
  }
}
```

### Opt-In Consent Management with Cryptographic Proof

Consent is recorded with Ed25519-signed tokens. Revocation cascades to remove all promoted insights from the global registry.

```yaml
consent_management:
  model: opt_in
  consent_token: { algorithm: Ed25519, signature_verification: required_on_every_promotion }
  consent_scopes:
    - { scope: promote_insights, description: "Allow promoting anonymized insights to global registry" }
    - { scope: receive_insights, description: "Allow importing global insights" }
    - { scope: aggregate_metrics, description: "Allow inclusion in cross-repo analytics" }
  revocation:
    immediate_effect: true
    cascade_actions: [remove_all_promoted_insights, revoke_active_tokens, purge_from_metrics]
    audit_log: required
    ast_reference: "AST09"
```

```json
{
  "title": "ConsentToken", "type": "object",
  "required": ["token_id", "repository_id", "scope", "granted_at", "signature"],
  "properties": {
    "token_id": { "type": "string", "pattern": "^consent-[a-z0-9]+$" },
    "repository_id": { "type": "string" },
    "scope": { "type": "array", "items": { "type": "string", "enum": ["promote_insights", "receive_insights", "aggregate_metrics"] } },
    "granted_at": { "type": "string", "format": "date-time" },
    "signature": { "type": "string" },
    "ast_reference": { "type": "string", "const": "AST09" }
  }
}
```

### Audit Trail for Cross-Repo Data Flows

Every cross-repo operation produces an immutable, tamper-evident audit log entry with SHA-256 hash chaining and configurable retention.

```yaml
audit_trail:
  enabled: true
  storage: { backend: append_only_log, encryption: aes-256-gcm, integrity: sha256_chain, tamper_detection: true }
  captured_events:
    - { event: insight_promoted, fields: [insight_id, source_repo_hash, global_id, pia_id, consent_token_id, timestamp] }
    - { event: insight_imported, fields: [global_id, target_repo_hash, local_id, timestamp] }
    - { event: consent_granted, fields: [repository_id, scope, granted_by, timestamp] }
    - { event: consent_revoked, fields: [repository_id, scope, cascade_actions, timestamp] }
    - { event: rate_limit_triggered, fields: [repository_id, operation, current_usage, timestamp], ast_reference: "AST09" }
  retention: { default_days: 730, consent_events_days: 1825 }
  query_access: { roles: [security-ops, compliance-auditor, privacy-team] }
```

```json
{
  "tool": "cortivex_crossrepo",
  "request": { "action": "audit_query", "repo": "/path/to/repo", "event_types": ["insight_promoted"], "limit": 50 },
  "response": {
    "total_events": 14,
    "events": [{
      "event": "insight_promoted", "timestamp": "2026-02-10T14:22:00Z",
      "insight_id": "ins-7a3b", "global_id": "gi-1a2b",
      "pia_id": "pia-3c4d5e", "consent_token_id": "consent-x7y8z9", "ast_reference": "AST09"
    }]
  }
}
```
