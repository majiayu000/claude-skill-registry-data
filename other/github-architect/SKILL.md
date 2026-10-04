---
name: github-architect
description: Arquitecto estratégico de presencia en GitHub v2.1. Inventaría repositorios mediante GraphQL de ultra-alto rendimiento (1 punto de cuota), audita la salud determinista (score 0-100 con nota A-F), recomienda acciones de remediación (CI, metadatos, licencias), genera plantillas CI (.github/workflows/ci.yml) y ejecuta planes con aprobación Human-in-the-Loop.
---

# GitHub Architect v2.1 — Strategic Repository Presence & Health Lifecycle

**Role**: Strategic architect for GitHub presence. Evaluates account repositories using optimized GraphQL queries, scores health deterministically, classifies by taxonomy, generates impact/effort action plans, scaffolds CI pipelines, and executes approved changes safely via GitHub API / MCP tools.

## Trigger Phrase Examples
- `"audita mi github"`
- `"qué repos archivar"`
- `"itera /github-architect"`
- `"generar ci workflow"`
- `"github architect"`

---

## 🔁 7-Step Operational Lifecycle (v2.1 GraphQL Optimized)

1. **Identify Account**: Detect target user account or organization context (e.g., `@borjamoskv`).
2. **Ultra-Optimized Inventorying**: Execute `python3 scripts/fetch_repos_graphql.py <username>` to fetch up to 100 repositories, licenses, topics, and `.github/workflows` presence in **1 single GraphQL query** (1 API credit point, zero rate limit risk).
3. **Deterministic Health Scoring & Recommendations**: Pipe inventory JSON into `python3 scripts/repo_health.py` to generate 0–100 scores, A–F letter grades, and actionable recommendations.
4. **Taxonomic Classification**: Classify repositories into dispositions using [references/rubric.md](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/references/rubric.md) (*Flagship*, *Maintain*, *Incubate*, *Archive*, *Delete*, *Fork hygiene*).
5. **Emit Architecture Report**: Output a structured markdown report featuring quick wins, strategic investments, recommended archivals, and auto-remediation scaffolds.
6. **Human-In-The-Loop Execution**: Execute ONLY user-approved mutations (archiving, tagging, doc updates, CI workflow deployment) using GitHub MCP tools or explicit API calls.

---

## 🛡️ Safety Guardrails

- **Zero Unsanctioned Deletions**: Never delete a repository or close issues/PRs without explicit, imperative user authorization.
- **Archive by Default**: For abandoned or inactive repositories (> 1 year without commits), archiving (read-only mode) is always the primary recommended action over deletion.
- **Transparent Heuristics**: Health scores are deterministic calculations based on `scripts/repo_health.py`, not opaque black-box estimates.
- **Resilient CLI Auth**: Always execute `env -u GITHUB_TOKEN gh` to prioritize user keyring credentials over environment token overrides.
- **Public vs. Private Taxonomy**: Enforce C5-REAL separation (Standards/Theory/Tools -> Public; Arbitrage/System Mutators/Alphas -> Private).
- **Zero-Debt Kebab-Case Normalization**: Rename repos to clean kebab-case leveraging GitHub's native URL & Git remote redirect guarantee.
- **Agent Commit Hygiene**: Audit and polish public commit messages to eliminate raw agent placeholder text.

---

## 🛠️ Included Tools & Resources

- [scripts/fetch_repos_graphql.py](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/scripts/fetch_repos_graphql.py): Ultra-fast GraphQL fetcher integrating `github-api-rate-limit-optimization`.
- [scripts/repo_health.py](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/scripts/repo_health.py): Deterministic health scoring script v2.0 (supports ISO datetime parsing, recommendation engine, and `--scaffold-ci [python|node|generic]` workflow generator).
- [references/rubric.md](file:///Users/borjafernandezangulo/.gemini/config/skills/github-architect/references/rubric.md): Taxonomy definitions, Impact vs. Effort matrix, profile narrative checks, and report skeleton.
