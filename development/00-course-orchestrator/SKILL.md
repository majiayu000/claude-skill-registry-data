---
name: 00-course-orchestrator
description: >
  GenAI agent skill navigator for the `genai-agents/` folder. Start here to
  route agent-building, MLflow GenAI, tracing, Databricks Apps Track A, SDLC,
  evaluation, deployment, monitoring, prompt iteration, and vibecoding runtime
  tasks to the correct specialized skill. Uses tiered loading and keyword
  routing so agents read only the skills needed for the current task.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Course navigator/router — selects which genai-agents skills to load; no deployed resource and no deploy verb. Client-agnostic routing. Client-awareness layer present (M06): `client_context` is detected/gated by `skills/vibecoding-state`; `skills/genie-code-environment` referenced by the Runtime Contract and the A7 deploy route. No inline behavior detail."
coverage: full
metadata:
  author: "prashanth-subrahmanyam"
  version: "5.0.0"
  domain: "genai-agents"
  role: "navigator"
  scope: "strictly genai-agents/; alternate tracks only linked as optional accelerator mirrors"
  last_verified: "2026-06-02"
  volatility: low
  upstream_sources: []
  references:
    - "references/canonical-walkthrough-ordering.md"
    - "references/skyloyalty-variants.md"
    - "references/alternate-methods-catalog.md"
    - "../../skills/vibecoding-state/references/state-template.md"
    - "../../skills/vibecoding-state/references/retrospective-template.md"
---

# GenAI Agent Skill Navigator

## Purpose

This skill is the **entry point and router** for all skills under
`genai-agents/`. It chooses the right skill to load for a task, preserves the
canonical course progression, and keeps context small by using progressive
loading.

The navigator does not duplicate implementation instructions. Each worker
skill owns its own commands, validation gates, references, scripts, and notes
to carry forward.

For the full workshop-style walkthrough with per-step Activity / Output / Gate
tables, load [`references/canonical-walkthrough-ordering.md`](references/canonical-walkthrough-ordering.md).

---

## When to Use

| User intent | Route |
|---|---|
| "Start/resume the GenAI agent course", "what skill do I need?", "navigate genai-agents" | This navigator |
| Running a prompt from `Instructions.md` or `example/<use_case>/WALKTHROUGH.md` | `../../skills/vibecoding-state/SKILL.md` first, then the routed skill |
| Creating UC schemas, volumes, MLflow setup, tracing, tools, KA, AI Gateway | Foundation route below |
| Building the canonical Python agent on Databricks Apps | Track A route below |
| Prompt registry, eval datasets, scorers, eval runs, registration, deployment, monitoring, feedback, prompt iteration | SDLC route below |
| Asking about Supervisor API, Model Serving, Node-native variants, or Genie capstone | Optional sidecar catalog: [`references/alternate-methods-catalog.md`](references/alternate-methods-catalog.md) |

---

## Pipeline Progression Overview

The canonical path is Track A: custom Python agent built with OpenAI Agents SDK
and deployed on Databricks Apps.

| Stage | Name | Skill(s) | Key deliverables |
|---|---|---|---|
| 0 | Runtime contract | `../../skills/vibecoding-state/SKILL.md` | State file, applicability gates, retrospective log |
| 1 | Foundation | `../foundation/00-uc-resources-foundation` -> `../foundation/05-knowledge-assistant` | UC schemas/volumes, MLflow, tracing, tools/data, KA |
| 2 | Agent Build | `../tracks/A-custom-agent-apps/01-clone-and-run` -> `../tracks/A-custom-agent-apps/07-deploy-and-query` | Working Track A agent, Databricks Apps deployment, `predict_fn` |
| 3 | SDLC | `../sdlc/01-prompt-registry` -> `../sdlc/07-production-monitoring` + `../sdlc/04c-end-user-feedback` | Versioned prompts, evals, sign-off, registration, deploy, monitor, feedback |
| 4 | Iteration | `../sdlc/08b-prompt-handauthoring` or `../sdlc/08-prompt-optimization` | Improved prompts promoted only after re-eval passes |
| 5 | Debugging | `../tracks/A-custom-agent-apps/08-debugging` | Healthy local/deployed agent when something regresses |

Canonical ordering and time estimates are in
[`references/canonical-walkthrough-ordering.md`](references/canonical-walkthrough-ordering.md).

---

## Runtime Contract

For vibecoding workshops, always load `../../skills/vibecoding-state/SKILL.md` before
acting on a prompt. That sibling skill owns bootstrap, `enter`, `exit`,
applicability checks, state-file updates, and retrospectives. This navigator
only routes to the correct domain skill.

**Client awareness (by reference).** `vibecoding-state` also detects and gates
`client_context`. The course routes the same for every client; only deploy/run
mechanics differ. On the in-workspace agent, load `../../skills/genie-code-environment/SKILL.md`
(pre-auth, serverless, page-context CLI, project-rooted artifacts — skills load from the `.assistant/skills` copy) — local dev servers
and CLI/profile authentication do not apply there (see PRE-REQUISITES §11 for the
IDE/CLI auth path). Routed prompts open with a client-specific RULE_0 preamble;
follow it as written.

**Genie Code first-run.** Clone the whole repo into
`/Users/<your-username>/.assistant/skills/vibe-coding-workshop`, then **start a NEW
Agent-mode chat thread** so the skills load. Full block: [repo-root AGENTS.md](../../AGENTS.md)
("Genie Code" section) / [PRE-REQUISITES.md](../../PRE-REQUISITES.md).

Live state files are gitignored. Templates live in:

| Template | Purpose |
|---|---|
| `../../skills/vibecoding-state/references/state-template.md` | Canonical state-file schema |
| `../../skills/vibecoding-state/references/retrospective-template.md` | Per-prompt and rollup retrospective prompts |

---

## Routing Algorithm

```text
1. Receive the user request.
2. If this is an Instructions.md / WALKTHROUGH.md workshop prompt, load
   ../../skills/vibecoding-state/SKILL.md first.
3. Detect the task family using the tables below.
4. If the task is end-to-end, route to the first skill in that stage and let
   each skill's Next Step / Notes to Carry Forward section advance the flow.
5. If the task is specific, load only that worker skill.
6. Load references/ files only when the selected skill asks for details.
```

---

## Skill Structure And Numbering

| Pattern | Meaning |
|---|---|
| `00-course-orchestrator/` | This navigator; route first, do not implement here |
| `../../skills/vibecoding-state/` | Runtime contract for prompt-driven workshops (repo-root, client-agnostic) |
| `foundation/00-*` | Foundation setup starts here |
| `foundation/01-*`, `02-*`, ... | Ordered foundation worker skills |
| `tracks/A-custom-agent-apps/01-*`, ... | Canonical Track A worker skills |
| `sdlc/01-*`, ... | Ordered MLflow GenAI SDLC worker skills |
| `sdlc/04b-*`, `04c-*`, `08b-*` | Inserted gates/branches around the primary numbered flow |
| `references/` | Sidecar navigator docs loaded on demand |

### How To Navigate A Skill

1. Read the selected `SKILL.md` first.
2. Follow its prerequisites, gates, and validation commands.
3. Load that skill's `references/` files only when needed.
4. Carry forward only the skill's summary outputs before loading the next skill.

---

## Context Budget Management

| Tier | Purpose | Target content |
|---|---|---|
| Tier 1: Navigator | Always loaded | This file only |
| Tier 2: Selected skill | Loaded after routing | One `SKILL.md` for the current task |
| Tier 3: Neighbor skill | Loaded only for direct handoff | Previous/next step summary, not full skill body |
| Tier 4: References | Loaded on demand | Detailed patterns, scripts, templates, external docs |

### Budget Zones

| Zone | Guidance |
|---|---|
| Green, 0-20K tokens | Load this navigator and one or two `SKILL.md` files freely |
| Yellow, 20-50K tokens | Stop browsing broadly; load only task-specific references |
| Red, 50K+ tokens | Summarize phase state, unload previous details, split the task |

---

## Task Detection And Skill Routing

### Bootstrap / Runtime Routes

| Task keywords | Route to | Notes |
|---|---|---|
| "workshop prompt", "Instructions.md", "WALKTHROUGH", "state file", "applicability matrix", "retrospective", "gate" | `../../skills/vibecoding-state/SKILL.md` | Load before the task skill |
| "start from scratch", "new agent course", "bootstrap resources", "UC schemas", "volumes" | `../foundation/00-uc-resources-foundation/SKILL.md` | Canonical first setup step |
| "course order", "canonical walkthrough", "time estimate", "Module 1", "Module 2", "Module 3" | `references/canonical-walkthrough-ordering.md` | Sidecar narrative, not implementation |
| "SkyLoyalty variant", "variant 1", "variant 5", "which walkthrough" | `references/skyloyalty-variants.md` | Variant chooser only |

### Foundation Routes

| Task keywords | Route to | Position |
|---|---|---|
| "UC resources", "Unity Catalog schemas", "managed volumes", "knowledge_sources volume", "signoff volume" | `../foundation/00-uc-resources-foundation/SKILL.md` | F0 |
| "agent spec", "Agent Spec", "tool selection", "agent_tool_selection", "SQL MCP catalog", "SQL MCP schema", "MCP recommendations", "web search MCP" | `../foundation/00b-agent-spec-and-tool-plan/SKILL.md` | F0b |
| "MLflow setup", "GenAI foundation", "autolog", "ResponsesAgent signature", "connection pooling" | `../foundation/01-mlflow-genai-foundation/SKILL.md` | F1 |
| "experiment path", "MLflow tracing", "UC OTEL", "trace storage", "trace_location", "monitoring SQL warehouse" | `../foundation/02-experiment-tracing-and-uc-storage/SKILL.md` | F2 |
| "TypeScript tracing", "Node tracing", "mlflow-tracing npm", "tracedOpenAI" | `../foundation/02b-typescript-tracing/SKILL.md` | F2b |
| "trace user", "trace session", "APP_ENVIRONMENT", "client_request_id", "trace context", "environment metadata" | `../foundation/02c-trace-context-and-environments/SKILL.md` | F2c |
| "MCP", "tools", "Genie tool", "Vector Search MCP", "SQL tool", "UC Functions", "external MCP", "resource grants" | `../foundation/03-tools-and-data-access/SKILL.md` | F3 |
| "AI Gateway", "guardrails", "rate limits", "usage tracking", "inference tables", "LLM endpoint governance" | `../foundation/04-ai-gateway/SKILL.md` | F4, optional hardening after core Track A; only with pre-provisioned Gateway or public admin APIs |
| "Knowledge Assistant", "document Q&A", "KA endpoint", "sync documents", "citations" | `../foundation/05-knowledge-assistant/SKILL.md` | F5 |

### Track A Routes

| Task keywords | Route to | Position |
|---|---|---|
| "clone template", "quickstart", "local dev", "agent-openai-agents-sdk", "built-in chat UI" | `../tracks/A-custom-agent-apps/01-clone-and-run/SKILL.md` | A1 |
| "OpenAI Agents SDK", "Agent class", "Runner", "ResponsesAgent", "set_model", "streaming", "ModelConfig" | `../tracks/A-custom-agent-apps/02-agent-framework/SKILL.md` | A2 |
| "function_tool", "wire tools", "DatabricksMCPClient", "MCPServerSse", "agent tools" | `../tracks/A-custom-agent-apps/03-tools-and-mcp/SKILL.md` | A3 |
| "agent auth", "OBO", "service principal", "App Authorization", "User Authorization", "permissions" | `../tracks/A-custom-agent-apps/04-authentication/SKILL.md` | A4 |
| "Lakebase memory", "conversation memory", "AsyncDatabricksSession", "DatabricksStore", "thread_id" | `../tracks/A-custom-agent-apps/05-lakebase-memory/SKILL.md` | A5 |
| "agent-evaluate", "pre-deploy eval", "smoke test", "built-in judges" | `../tracks/A-custom-agent-apps/06-evaluation/SKILL.md` | A6 |
| "deploy to Databricks Apps", "databricks apps deploy", "query deployed app", "OAuth token", "app URL" | `../tracks/A-custom-agent-apps/07-deploy-and-query/SKILL.md` | A7 — deploy verb is client-agnostic; the local dev server / CLI-auth steps are IDE-only (see A7 + `../../skills/genie-code-environment/SKILL.md`) |
| "debug app", "deployment failed", "runtime error", "auth failure", "resource permission", "Lakebase failure" | `../tracks/A-custom-agent-apps/08-debugging/SKILL.md` | A8 |

### SDLC Routes

| Task keywords | Route to | Position |
|---|---|---|
| "prompt registry", "register prompt", "prompt alias", "load_prompt", "A/B test prompt" | `../sdlc/01-prompt-registry/SKILL.md` | S1 |
| "evaluation dataset", "benchmark dataset", "merge_records", "SME labels", "dataset from traces" | `../sdlc/02-evaluation-datasets/SKILL.md` | S2 |
| "scorers", "judges", "Guidelines", "Correctness", "Safety", "thresholds", "custom scorer" | `../sdlc/03-scorers-and-judges/SKILL.md` | S3 |
| "mlflow.genai.evaluate", "evaluation run", "predict_fn", "labeling session", "human labels", "pass/fail gate" | `../sdlc/04-evaluation-runs/SKILL.md` | S4 |
| "stakeholder signoff", "business review", "compliance review", "deployment gate" | `../sdlc/04b-stakeholder-signoff/SKILL.md` | S4b |
| "end-user feedback", "thumbs up", "ratings", "log_feedback", "feedback assessment", "trace_id feedback" | `../sdlc/04c-end-user-feedback/SKILL.md` | S4c |
| "log model", "register model", "Unity Catalog model", "champion alias", "rollback" | `../sdlc/05-logged-model-and-uc-registration/SKILL.md` | S5 |
| "production deploy", "CI/CD", "Asset Bundle", "evaluate then promote", "serving endpoint" | `../sdlc/06-deployment-and-automation/SKILL.md` | S6 |
| "production monitoring", "registered scorers", "sampling", "trace archival", "quality dashboard" | `../sdlc/07-production-monitoring/SKILL.md` | S7 |
| "GEPA", "optimize_prompts", "automated prompt optimization", "prompt quality plateau" | `../sdlc/08-prompt-optimization/SKILL.md` | S8 |
| "hand author prompt", "instruction-shaped failure", "failing scorer rationale", "prompt revision" | `../sdlc/08b-prompt-handauthoring/SKILL.md` | S8b |

---

## Progressive Loading Strategy

### Step 1: Detect

Read this navigator and choose one route from the tables above.

### Step 2: Load The Selected Skill

Load exactly one routed `SKILL.md`. For an end-to-end path, start with the
first skill in the stage, then follow that skill's Next Step.

### Step 3: Execute Or Explain

If implementing, follow the selected skill's commands and gates. If answering a
question, cite only the selected skill and any relevant references.

### Step 4: Carry Forward A Small Summary

At a stage boundary, keep only:

- The live state-file values, if this is a workshop run.
- The selected skill's outputs / Notes to Carry Forward.
- The next skill path.

### Step 5: Load References Only On Demand

Prefer task-specific `references/` files over broad reading. Treat scripts as
black-box utilities unless debugging them.

---

## Complete Skill Directory Map

```text
genai-agents/
├── 00-course-orchestrator/SKILL.md                      # Navigator: routes all genai-agents tasks
│   └── references/
│       ├── canonical-walkthrough-ordering.md             # Canonical course narrative and timing
│       ├── skyloyalty-variants.md                        # SkyLoyalty V1-V5 chooser
│       └── alternate-methods-catalog.md                  # Optional non-canonical paths, outside main scope
│   (vibecoding-state relocated to repo-root skills/vibecoding-state/  # Runtime contract: state, gates, retrospectives)
├── foundation/
│   ├── 00-uc-resources-foundation/SKILL.md               # F0: UC schemas and managed volumes
│   ├── 00b-agent-spec-and-tool-plan/SKILL.md            # F0b: PRD -> Agent Spec -> Tool Plan
│   ├── 01-mlflow-genai-foundation/SKILL.md               # F1: MLflow GenAI setup and autolog
│   ├── 02-experiment-tracing-and-uc-storage/SKILL.md     # F2: experiments, tracing, UC OTEL storage
│   ├── 02b-typescript-tracing/SKILL.md                   # F2b: Node/TypeScript MLflow tracing
│   ├── 02c-trace-context-and-environments/SKILL.md       # F2c: users, sessions, env/version metadata
│   ├── 03-tools-and-data-access/SKILL.md                 # F3: MCP, tools, resource grants
│   ├── 04-ai-gateway/SKILL.md                            # F4: AI Gateway, guardrails, usage tracking
│   └── 05-knowledge-assistant/SKILL.md                   # F5: Knowledge Assistant lifecycle
├── tracks/
│   └── A-custom-agent-apps/
│       ├── 01-clone-and-run/SKILL.md                     # A1: clone template and run locally
│       ├── 02-agent-framework/SKILL.md                   # A2: OpenAI Agents SDK + ResponsesAgent
│       ├── 03-tools-and-mcp/SKILL.md                     # A3: function tools and MCP tools
│       ├── 04-authentication/SKILL.md                    # A4: SP, OBO, resource permissions
│       ├── 05-lakebase-memory/SKILL.md                   # A5: conversation memory and thread IDs
│       ├── 06-evaluation/SKILL.md                        # A6: pre-deploy agent evaluation
│       ├── 07-deploy-and-query/SKILL.md                  # A7: Databricks Apps deploy and query
│       └── 08-debugging/SKILL.md                         # A8: local/deployed agent debugging
└── sdlc/
    ├── 01-prompt-registry/SKILL.md                       # S1: UC prompt registry and aliases
    ├── 02-evaluation-datasets/SKILL.md                   # S2: eval datasets and trace/label import
    ├── 03-scorers-and-judges/SKILL.md                    # S3: scorers, judges, thresholds
    ├── 04-evaluation-runs/SKILL.md                       # S4: mlflow.genai.evaluate and labels
    ├── 04b-stakeholder-signoff/SKILL.md                  # S4b: business/compliance sign-off gate
    ├── 04c-end-user-feedback/SKILL.md                    # S4c: production feedback assessments
    ├── 05-logged-model-and-uc-registration/SKILL.md      # S5: log/register/promote agent model
    ├── 06-deployment-and-automation/SKILL.md             # S6: deploy, CI/CD, AI Gateway handoff
    ├── 07-production-monitoring/SKILL.md                 # S7: registered scorers and dashboards
    ├── 08-prompt-optimization/SKILL.md                   # S8: GEPA / optimize_prompts
    └── 08b-prompt-handauthoring/SKILL.md                 # S8b: manual prompt iteration
```

---

## Post-Completion: Skill Usage Summary

After a routing or orchestration session, output a concise Skill Usage Summary
reflecting what was actually loaded.

| # | Step / Phase | Skill / Reference Read | Type | Used For |
|---|---|---|---|---|
| 1 | Routing | `genai-agents/00-course-orchestrator/SKILL.md` | Navigator | Chose the route |

End with:

- **Totals:** X navigator/runtime skills, Y foundation skills, Z Track A skills, W SDLC skills, R reference files.
- **Routing path:** The skill sequence actually used.
- **Skipped:** Skills considered but not needed, with reason.
- **Unplanned:** Skills read outside the normal route, with reason.

---

## Maintenance

When adding or moving a `genai-agents/` skill:

1. Keep the skill's `SKILL.md` focused; move detailed patterns to `references/`.
2. Add or update frontmatter fields: `name`, `description`, `metadata.domain`, `metadata.pipeline_position` or `metadata.role`.
3. Add a routing row in the correct Task Detection table above.
4. Add one line in the Complete Skill Directory Map.
5. If the skill changes canonical order or timing, update `references/canonical-walkthrough-ordering.md`.
6. If the skill affects workshop state/gates, update `../../skills/vibecoding-state/SKILL.md` or its references.
7. Verify every linked `SKILL.md` exists.

---

## References

### Local references

- [`references/canonical-walkthrough-ordering.md`](references/canonical-walkthrough-ordering.md)
- [`references/skyloyalty-variants.md`](references/skyloyalty-variants.md)
- [`references/alternate-methods-catalog.md`](references/alternate-methods-catalog.md)
- [`../../skills/vibecoding-state/SKILL.md`](../../skills/vibecoding-state/SKILL.md)
- [`../../skills/vibecoding-state/references/state-template.md`](../../skills/vibecoding-state/references/state-template.md)
- [`../../skills/vibecoding-state/references/retrospective-template.md`](../../skills/vibecoding-state/references/retrospective-template.md)

### Official documentation

- [Author an AI agent and deploy it on Databricks Apps](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent)
- [Authentication for AI agents](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-authentication)
- [Debug AI agents](https://docs.databricks.com/aws/en/generative-ai/agent-framework/debug-agent)
- [Agents development workflow](https://docs.databricks.com/aws/en/generative-ai/guide/agents-dev-workflow)
- [Store MLflow traces in Unity Catalog](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/trace-unity-catalog)
- [Collect end-user feedback](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/collect-user-feedback/)
- [Automatically optimize prompts](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/prompt-registry/automatically-optimize-prompts)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 5.0.0 | 2026-04-27 | Recast as a generalized, context-efficient navigator for skills strictly under `genai-agents/`. Moved workshop narrative, SkyLoyalty variants, and alternate-method catalog to sidecar references. Added routing algorithm, keyword tables, progressive loading, directory map, usage summary, and maintenance checklist inspired by `data_product_accelerator/skills/skill-navigator/SKILL.md`. |
| 4.0.0 | 2026-04-26 | Resynced to current `genai-agents/` tree: Track A is the sole canonical path; new SDLC and Foundation skills surfaced; Track A debugging added; alternate tracks and capstone routed through references; SDLC ordering aligned to `example/skyloyalty/WALKTHROUGH.md`; F4 AI Gateway moved into S6 deployment. |
| 3.3.0 | 2026-04-21 | Added SkyLoyalty Variant Selector linking the five concrete walkthroughs. |
| 3.2.0 | 2026-04-19 | Moved generalized state + retrospective templates from `example/` into a skill-owned references area. |
| 3.1.0 | 2026-04-19 | Added optional Track B Step 0 (Knowledge Assistant Lifecycle) ahead of B1. |
| 3.0.0 | 2026-04-10 | Three-module architecture: Foundation, Agent Tracks, SDLC Pipeline. |
| 2.0.0 | 2026-04-10 | Single unified track. Prescribed OpenAI Agents SDK. |
| 1.0.0 | 2026-04-10 | Initial two-track architecture. |
