---
name: dbt-cloud
description: "dbt Cloud skill for managed data transformation platform. Deep expertise in Cloud IDE (Studio), dbt Canvas, dbt Copilot, Fusion engine, job scheduling, CI/CD workflows, Semantic Layer APIs, dbt Explorer, dbt Mesh, environment management, and enterprise governance. WHEN: \"dbt Cloud\", \"dbt Cloud CLI\", \"dbt Cloud IDE\", \"Studio IDE\", \"dbt Canvas\", \"dbt Copilot\", \"dbt Explorer\", \"dbt Fusion\", \"dbt Mesh\", \"dbt Semantic Layer\", \"dbt Cloud CI\", \"Advanced CI\", \"dbt compare\", \"dbt Cloud job\", \"dbt Cloud scheduling\", \"dbt Cloud environment\", \"state-aware orchestration\", \"dbt Discovery API\", \"dbt Admin API\", \"dbt webhook\", \"dbt Cloud pricing\", \"dbt Cloud Enterprise\", \"dbt Canvas drag-and-drop\", \"dbt RBAC\", \"dbt SSO\". Do NOT use for open-source dbt Core mechanics (Jinja, materializations, incremental strategies, macros, `ref()`/`source()`, local project structure) -- use the `dbt-core` skill."
license: MIT
---

# dbt Cloud

This skill covers dbt Cloud, the managed SaaS platform built on dbt Core that provides web-based development, job orchestration, the Semantic Layer, dbt Explorer, dbt Mesh, and enterprise governance. It provides deep knowledge of the Cloud IDE (Studio), Canvas visual editor, Copilot AI, Fusion engine, CI/CD workflows, environment management, APIs, and enterprise features (RBAC, SSO, audit logging). For dbt Core-specific questions (Jinja, materializations, incremental strategies, macros, testing), see the `dbt-core` skill.

## When to Use This Skill

**Use this skill for:**
- "Set up a CI job in dbt Cloud"
- "dbt Cloud IDE vs VS Code extension"
- "Configure dbt Mesh cross-project references in Cloud"
- "dbt Cloud Semantic Layer API integration with Tableau"
- "dbt Explorer column-level lineage"
- "dbt Canvas for analysts"
- "Advanced CI compare changes"
- "State-aware orchestration to reduce costs"
- "dbt Cloud Enterprise RBAC setup"
- "dbt Cloud job failed -- how to debug"
- "dbt Cloud vs dbt Core -- which to choose"
- "dbt Fusion engine performance"
- "Webhook integration for external orchestration"

**See a different skill for:**
- Jinja macros, materializations, incremental strategies, ref/source, testing --> `dbt-core` skill
- Spark DataFrame transformations --> `spark` skill
- Comparing dbt vs Spark vs DuckDB --> `transformation` skill
- Warehouse-specific tuning (Snowflake, BigQuery) --> the database plugin's `{platform}` skill
- ETL architecture, tool selection --> `overview` skill

## How to Approach Tasks

1. **Classify** the request:
   - **Platform features/setup** -- Load `references/architecture.md` for IDE, environments, jobs, APIs, Mesh, Semantic Layer
   - **CI/CD and workflows** -- Load `references/best-practices.md` for CI jobs, environment strategy, cost optimization
   - **Debugging/failures** -- Load `references/diagnostics.md` for job failures, Git issues, IDE problems, API errors
   - **dbt Core fundamentals** -- See the `dbt-core` skill

2. **Determine context** -- Ask if unclear: licensing tier (Developer/Starter/Enterprise), warehouse platform, team size, Git provider, whether this is setup vs troubleshooting.

3. **Analyze** -- Apply dbt Cloud-specific reasoning: environment isolation, job orchestration, Slim CI with deferral, Semantic Layer architecture, Mesh governance.

4. **Recommend** -- Provide actionable guidance with specific UI paths, API calls, YAML configs, and CLI commands. Explain tier requirements.

5. **Verify** -- Suggest validation: check job run logs, use `dbt debug` in IDE, inspect compiled SQL, check status.getdbt.com for platform issues.

## Platform Overview

dbt Cloud is a managed platform that runs dbt Core under the hood but adds infrastructure, governance, and developer experience layers. It provides multiple development surfaces, built-in scheduling, CI/CD automation, hosted documentation, a Semantic Layer with API access, and enterprise security features.

### What dbt Cloud Adds Over Core

| Capability | dbt Core | dbt Cloud |
|---|---|---|
| SQL/Jinja transformations | Yes | Yes |
| Web-based IDE | No | Studio IDE, Canvas |
| Job scheduling | No (external tools) | Built-in scheduler |
| CI/CD automation | Manual (GitHub Actions) | Native CI jobs on PR |
| Documentation hosting | Self-hosted static site | Auto-hosted, auto-updated |
| Semantic Layer | MetricFlow CLI only | Full hosted API service |
| Multi-project Mesh | Limited | Native cross-project refs |
| RBAC / SSO / Audit | No | Enterprise tier |
| AI assistance | No | dbt Copilot |
| Visual editor | No | Canvas (Enterprise) |
| State-aware orchestration | No | Yes |

## Development Surfaces

### Studio IDE (Cloud IDE)

Browser-based development environment. No local setup required.

- Syntax highlighting, autocomplete, real-time DAG visualization
- File editor with Git integration (commit, branch, PR)
- Preview/compile SQL inline before running
- SQLFluff linting and formatting built in
- Best for: quick edits, onboarding new team members, environments without local dev setup

### dbt Canvas (Visual Editor)

Drag-and-drop interface for building models without writing SQL. Enterprise tier.

- Discover sources and models visually
- Apply transformations (joins, filters, aggregations) via UI
- Preview outputs step by step with always-on data profiling
- Compiles to SQL automatically, integrates with Git (commit, open PRs)
- Includes dbt Copilot AI assistance
- Best for: analysts who prefer visual interfaces over SQL

### dbt Cloud CLI

Local command-line interface connected to dbt Cloud:

- Local development with cloud features (deferral, cross-project refs, credential management)
- Authenticates against dbt Cloud for artifacts and environment resolution
- Best for: power users who prefer local editors with cloud benefits

### VS Code Extension

Official dbt Labs extension with Fusion engine integration:

- Language server (LSP) for fast parsing and validation
- Compile cache for faster developer feedback
- OAuth authentication for platform connectivity
- Best for: power users wanting IDE integration with cloud features

## Environments

### Environment Types

| Environment | Purpose | Credentials |
|---|---|---|
| **Development** | Per-developer workspace | Individual developer credentials |
| **Staging** (optional) | Release branch testing | Limited production-like access |
| **Production** | Scheduled and deploy jobs | Production service account |

### Deferral

Enable deferral in development environments to resolve `{{ ref() }}` against production artifacts without building upstream models:

- Developers only build/test edited models
- Saves significant compute and storage costs
- Configure in Environment Settings > Deferral

### Environment Configuration

- Each environment can run a different dbt version (Fusion Latest is default for new projects)
- Use separate warehouse credentials per environment with least-privilege access
- Restrict production credentials to production jobs only
- Store secrets as environment variables in dbt Cloud (never in Git)

## Job Types and Scheduling

### Scheduled Jobs

Cron-based scheduling for regular dbt runs:

- Configurable frequency, model selection, and commands
- Email and Slack notifications for job status
- Logging and alerting built in

### CI Jobs (On Pull Request)

Triggered automatically when a PR is opened or commits are pushed:

- **Slim CI**: Uses `state:modified+` to build only changed models and children
- **Advanced CI** (Enterprise): Compare changes shows data-level diffs between PR and production
- SQLFluff linting as a pre-build step
- Defers to production environment for artifact comparison

### Deploy/Merge Jobs

Triggered on merge to main branch. Runs full or selective builds in production.

### API-Triggered Jobs

Triggered via the Administrative API for external orchestration integration (Airflow, Prefect, Dagster).

### State-Aware Orchestration

Skips models that already satisfy freshness requirements. dbt Labs reported 64% compute cost reduction internally using Fusion + state-aware orchestration.

## Semantic Layer

### Architecture

MetricFlow (open-source engine) powers the Semantic Layer. Define metrics, dimensions, entities in YAML. MetricFlow generates optimized SQL and pushes computation to the warehouse.

### API Access

| API | Protocol | Use Case |
|---|---|---|
| **GraphQL** | HTTP | Strongly-typed metric queries; `queryRecords` endpoint |
| **JDBC** | Arrow Flight SQL | BI tool integrations (Tableau, Power BI) |
| **ADBC** | Arrow Database Connectivity | Alternative connectivity |
| **Python SDK** | Python | Programmatic access |

### Native BI Integrations

Tableau, Power BI, Hex, Mode, Excel, DataGrip/DBeaver. Any tool supporting JDBC, ADBC, GraphQL, or Python SDK can connect.

### When to Define Metrics

- Key business KPIs needing a single source of truth (revenue, churn, DAU)
- Same metric consumed by multiple BI tools or teams
- Start with critical metrics suffering from inconsistent definitions
- Add incrementally; avoid defining everything at once

## dbt Explorer (Catalog)

- Interactive DAG lineage visualization
- Column-level lineage across sources and models
- Multi-project lineage for Mesh architectures
- Global search across all project resources
- Performance insights with historical execution data
- Project optimization recommendations
- Documentation auto-updated after each production run

## dbt Mesh (Multi-Project)

### Core Concepts

- Multiple dbt projects aligned to business domains
- Federated ownership with cross-project dependencies
- Cross-project refs: `{{ ref('upstream_project', 'shared_model') }}`
- Upstream models must have `access: public`
- Full lineage rendered in dbt Explorer

### Governance Features

- **Access modifiers**: `private`, `protected`, `public`
- **Model contracts**: Column names, types, constraints enforced at build time
- **Model versions**: API-style versioning with deprecation dates
- **Cross-platform Mesh**: Apache Iceberg catalog integration (Snowflake + BigQuery)

## APIs

### Administrative API (v3 recommended)

Manage accounts, projects, environments, jobs, runs, users programmatically. Enabled by default for Starter+.

### Discovery API (GraphQL)

Query DAG metadata: models, sources, tests, exposures, metrics. Supports lineage exploration, automated reporting, data monitoring.

### Webhooks

Event-driven notifications for job status changes. `job.run.completed` event with status filtering. 10-second timeout, 5 retry attempts, 30-day log retention.

## Licensing Tiers

| Tier | Price | Seats | Models/Month | Key Features |
|---|---|---|---|---|
| **Developer** | Free | 1 | 3,000 | IDE, scheduling, basic features |
| **Starter** | $100/user/mo | Up to 5 | 15,000 | Semantic Layer, Copilot, APIs |
| **Enterprise** | Custom | Custom | 100,000 | SSO, RBAC, Mesh, Canvas, Advanced CI |
| **Enterprise+** | Custom | Custom | Unlimited | PrivateLink, IP restrictions |

## Anti-Patterns

1. **Using dbt Cloud as "just a scheduler"** -- dbt Cloud's value comes from IDE, Explorer, Semantic Layer, and CI/CD integration. If you only need scheduling, use Airflow + dbt Core.

2. **Skipping deferral in development** -- Without deferral, developers must build the entire upstream DAG in their dev environment. Enable deferral to reference production tables for unmodified models.

3. **Full builds in CI** -- Use Slim CI (`state:modified+`) to test only changed models and their children. Full builds in CI waste compute and slow feedback.

4. **Not setting up CI jobs** -- Every PR should trigger automated validation. CI is a near-zero-effort quality gate that prevents production failures.

5. **Hardcoding credentials** -- Never commit database passwords or API keys to Git. Use dbt Cloud's environment variable management.

6. **One environment for everything** -- Separate development, staging (optional), and production environments. Each should have isolated credentials and schemas.

7. **Ignoring Explorer insights** -- dbt Explorer provides performance recommendations and cost insights. Review them regularly to identify optimization opportunities.

8. **Premature Mesh adoption** -- Don't split into multiple projects until the single project causes team or performance pain. Governance overhead increases with each project.

## Cross-Domain References

| Technology | Reference | When |
|---|---|---|
| dbt Core | `dbt-core` skill | Jinja, materializations, incrementals, macros, testing fundamentals |
| Spark | `spark` skill | When transformations exceed SQL capability |
| Transformation | `transformation` skill | Comparing dbt vs Spark vs DuckDB |
| ETL Domain | `overview` skill | Cross-platform ETL architecture |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- Platform architecture (development surfaces, Fusion engine, environments, job types, scheduler), APIs (Admin, Discovery, Semantic Layer, webhooks), dbt Explorer, dbt Mesh (access modifiers, contracts, versioning, cross-platform), Semantic Layer (MetricFlow, APIs, BI integrations), Git provider integration, warehouse connections
- `references/best-practices.md` -- Environment strategy (layout, deferral, configuration), CI/CD workflows (Slim CI, Advanced CI, deploy jobs), Semantic Layer best practices (when/how to define metrics, governance, performance), Mesh best practices (when to split, contracts, versioning, cross-project refs), collaboration (PR reviews, documentation, IDE workflows), cost optimization (platform, compute, state-aware orchestration)
- `references/diagnostics.md` -- Job failure categories (SQL, dependency, schema, resource, compilation), debugging workflow, environment configuration issues, Git sync problems (GitHub, GitLab, Azure DevOps), performance issues (slow jobs, scheduler, warehouse), IDE troubleshooting (Studio, VS Code, CLI), API and webhook errors, platform status monitoring
