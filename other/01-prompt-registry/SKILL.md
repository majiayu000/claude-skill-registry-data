---
name: 01-prompt-registry
description: >
  Use when you need to version, manage, or load prompts for any GenAI agent
  on Databricks. Covers how to register prompts in Unity Catalog, set up
  aliases for safe deployments, link prompts to traces, and load them in
  production apps — even if you just want "register my prompt and give me
  a stable URI." Also use when A/B testing prompt versions or connecting
  prompt changes to evaluation runs. SDLC Step 1.
license: Apache-2.0
compatibility: "Requires Databricks workspace with MLflow 3.10+ and Unity Catalog. Scripts use uv."
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Prompts registered/aliased in the UC Prompt Registry via the MLflow SDK; no bundle resource. Identical on both clients; on Genie Code run any CLI step through runDatabricksCli (pre-authenticated). See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "4.0.0"
  domain: "genai-agents"
  pipeline_position: "S1"
  consumes: "experiment_paths, prompt_templates"
  produces: "registered_prompts, prompt_aliases"
  grounded_in: "https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/prompt-registry/, https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/link-production-traces-to-app-versions, https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/prompt-registry/use-prompts-in-deployed-apps"
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-mlflow-evaluation/SKILL.md"
      relationship: "reference"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
---

# Prompt Registry Patterns (Native MLflow)

Use this skill when you need to **register, version, alias, and load** prompts for GenAI agents on Databricks using **`mlflow.genai`** (Prompt Registry), not legacy Unity Catalog tables plus `mlflow.log_artifact` for prompt bodies.

## Upstream Lineage

This skill references Databricks Agent Skills' `databricks-mlflow-evaluation` skill where prompt versions connect to evaluation runs, GEPA optimization, and production trace lineage. If prompt changes need evaluation-backed promotion guidance, consult the upstream skill first, then apply this skill's Prompt Registry naming and alias contracts.

Typical situations:

- **Agent prompts** — ship judge, benchmark, and instruction templates as first-class registry objects with immutable versions.
- **Prompt versioning** — every change is a new version; use aliases (`production`, `latest`, `staging`) to point workloads at the right snapshot without renaming.
- **A/B testing** — register two versions, bind one alias to champion and another to challenger, then compare metrics in evaluation (see SDLC Step 4).
- **Traceability** — load prompts inside an active MLflow trace for Linked Prompts; in production, tie traces to app/model versions when needed (see References).

---

## CRITICAL: UC Schema Linkage for UI Visibility

Prompts are stored under Unity Catalog, but the **experiment** must advertise which `catalog.schema` backs the Prompt Registry or prompts may not surface correctly in the Experiment UI.

```python
import mlflow

catalog, schema = "main", "my_agent_prompts"
uc_schema = f"{catalog}.{schema}"

mlflow.set_experiment_tags({
    "mlflow.promptRegistryLocation": uc_schema,
})
```

Set this tag **before** registering prompts in that registry location.

> **Load** [references/uc-schema-linkage.md](references/uc-schema-linkage.md) **if** prompts do not appear in the Experiment UI, permissions fail, or you need multi-schema patterns.

---

## Naming Convention (UC-Qualified Names)

Prompt names in UC follow the **three-level** form `catalog.schema.prompt_name`. Build the logical name in application code with normal Python string composition (f-strings or concatenation). **Do not** confuse that with **template variable placeholders inside the prompt body**.

- **Registry object name** (what you pass to `register_prompt(name=...)`): `f"{catalog}.{schema}.{prompt_slug}"` — e.g. `main.my_agent_prompts.judge_syntax`.
- **Template body** (the `template=` string): use MLflow’s native **`{{ variable }}`** syntax for variables the registry and loaders resolve. No custom formatter is required; double braces are MLflow’s template syntax, not Python `str.format()`.

```python
import mlflow.genai

catalog, schema = "main", "my_agent_prompts"
prompt_slug = "judge_syntax"
prompt_name = f"{catalog}.{schema}.{prompt_slug}"

template = """You are a judge. Score the answer for {{ criterion }}.
User question: {{ user_question }}
Answer: {{ answer }}
"""

version = mlflow.genai.register_prompt(
    name=prompt_name,
    template=template,
    commit_message="Initial judge prompt",
    tags={"domain": "my_agent", "type": "judge"},
)
```

> **Load** [references/ownership-conflict-handling.md](references/ownership-conflict-handling.md) **if** `register_prompt` raises ownership or naming conflicts.

For **per-tenant or per-resource** prompts, sanitize the resource id (e.g. `safe_id = re.sub(r"[^a-zA-Z0-9_]+", "_", resource_id).strip("_").lower()`), then `instruction_name = f"{catalog}.{schema}.instructions_{safe_id}"`; use the same alias workflow as shared prompts.

---

## Using Prompts in Deployed Applications

In production Databricks Apps and other deployed workloads, resolve prompts with a **registry URI** so code does not hard-code raw version integers. The documented pattern uses a **`prompts:/`-style** qualified reference (single slash) with an **alias** (for example `@production`).

**Gate:** URI scheme verified. `mlflow.genai.load_prompt("prompts:/<fqn>@production")` must succeed before any downstream skill references the prompt. The double-slash form (literal `prompts:` followed by `//`) is forbidden.

Canonical prompt FQN (per the canonical_names registry — uses `uc_agent_schema`, not `use_case_slug`):

```text
prompts:/{uc_catalog}.{uc_agent_schema}.system_instructions@production
```

Do not substitute `{use_case_slug}` for the UC schema unless `uc_agent_schema == use_case_slug` has been explicitly captured in state.

Example form (adapt to your catalog, schema, and prompt name):

```text
prompts:/catalog.schema.prompt_name@alias
```

Load in code with the same URI string your runtime expects (per [Use prompts in deployed apps](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/prompt-registry/use-prompts-in-deployed-apps)):

```python
import mlflow.genai

uri = "prompts:/main.my_agent_prompts.judge_syntax@production"
loaded = mlflow.genai.load_prompt(uri)
```

Keep aliases (`production`, `staging`, `latest`) aligned with promotion workflows so deploys only change alias targets, not application code.

---

## Linking Prompts to Production Traces (`MLFLOW_ACTIVE_MODEL_ID`)

Set **`MLFLOW_ACTIVE_MODEL_ID`** in the serving or app environment to the registered model id for the deployment so production traces link to the correct app/model version in MLflow ([Databricks: link production traces](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/link-production-traces-to-app-versions)).

---

## Alias Management

Aliases are mutable pointers to a **specific integer version**. Production traffic should read `@production`; development can use `@latest` or custom aliases.

```python
import mlflow.genai

PRODUCTION_ALIAS = "production"

mlflow.genai.set_prompt_alias(
    name=prompt_name,
    alias=PRODUCTION_ALIAS,
    version=version.version,
)
```

Call `set_prompt_alias` after each successful `register_prompt` for every alias your loaders depend on.

> **Load** [references/ab-testing.md](references/ab-testing.md) **if** you are setting up champion/challenger prompt A/B tests.

---

## Loading and Trace Linking (Evaluation / Notebooks)

Calling `mlflow.genai.load_prompt()` **inside an active trace** associates the prompt with that trace (Linked Prompts in the UI). You can load for side effects only if you only need the association.

```python
import mlflow


def link_prompt_to_trace(prompt_name: str, alias: str = "production") -> None:
    """Load a registered prompt inside the current trace to link it in the UI."""
    if not prompt_name:
        return
    uri = f"prompts:/{prompt_name}@{alias}"
    try:
        mlflow.genai.load_prompt(uri)
    except Exception:
        try:
            mlflow.genai.load_prompt(f"prompts:/{prompt_name}@latest")
        except Exception:
            pass  # optional: log at debug in production scorers
```

If you need the template object, use the return value of `load_prompt()`; trace linking still occurs when a trace is active.

> **Load** [references/loading-patterns.md](references/loading-patterns.md) **if** you need caching strategies, error recovery, or template variable injection patterns.

---

## Fallback Names When UC or Ownership Is Strict

If registration fails due to scope or ownership, try a **small ordered list** of names before giving up: UC-qualified first, then a shorter scoped name if your org allows it.

```python
import re


def prompt_name_candidates(uc_schema: str, domain: str, logical_name: str) -> list[str]:
    """Prefer catalog.schema.name; fall back to a portable slug if needed."""
    safe_domain = re.sub(r"[^a-zA-Z0-9_]+", "_", domain or "default").strip("_").lower() or "default"
    candidates: list[str] = []
    if uc_schema:
        candidates.append(f"{uc_schema}.{logical_name}")
        candidates.append(f"{uc_schema}.{safe_domain}_{logical_name}")
    candidates.append(f"{safe_domain}_{logical_name}")
    return list(dict.fromkeys(candidates))
```

Register in order until `register_prompt` succeeds; document which name won for your environment.

> **Load** [references/ownership-conflict-handling.md](references/ownership-conflict-handling.md) **if** you encounter conflict detection errors or need drop-and-recreate strategies.

---

## A/B Testing with Aliases

| Role | Alias | Typical use |
|------|--------|-------------|
| Champion | `production` | Default scoring and production loads. |
| Challenger | `staging` (or a feature alias) | Experimental template; evaluate side-by-side before promotion. |

Workflow:

1. Register challenger as a **new version** of the same prompt name (or a separate name for isolation).
2. Point `staging` at the challenger version with `set_prompt_alias`.
3. Run evaluation passes that resolve `@staging` vs `@production`.
4. Promote the winner by moving `production` to the winning version.

> **Load** [references/ab-testing.md](references/ab-testing.md) **if** you need a full walkthrough with two versions, evaluation, and promotion.

---

## Do's and Don'ts

| | Do | Don't |
|---|---|---|
| **Tags** | Set `mlflow.promptRegistryLocation` on the experiment to your prompts’ `catalog.schema`. | Omit the tag and expect prompts to always appear in the Experiment UI. |
| **Aliases** | Call `set_prompt_alias` after every successful `register_prompt` for each alias loaders use. | Force callers to hard-code raw version integers. |
| **Templates** | Use `{{ variable }}` in the **template body** for MLflow variables. | Run Python `str.format()` on the template string expecting `{{` to interpolate. |
| **Deploys** | Resolve prompts via `prompts:/...` URIs (single slash) with aliases in deployed apps. | Bake immutable version numbers into app config — or use the forbidden double-slash form. |

---

## Common Mistakes

| Mistake | Why it hurts | What to do instead |
|--------|----------------|-------------------|
| Skipping `mlflow.promptRegistryLocation` | Prompts may not show as expected in Experiment UI | Set tag to `catalog.schema` for the registry you use |
| Non–UC-qualified names when UC is required | Registration or resolution fails or lands in wrong scope | Use `catalog.schema.prompt_name` for `name=` |
| Using `str.format()` on MLflow template bodies | `{{ name }}` is MLflow syntax, not Python formatting | Pass variables at load/inference time per MLflow prompt APIs |
| Only one hard-coded name | Ownership or collision errors block registration | Try `prompt_name_candidates()` order until one succeeds |
| Expecting `log_artifact` for registry visibility | Artifacts are not Prompt Registry versions | Use `mlflow.genai.register_prompt` + aliases |
| Forgetting `set_prompt_alias` after register | Callers cannot rely on stable pointers | Set `production` / `latest` / `staging` explicitly |

---

## Validation Checklist

- [ ] Experiment tag `mlflow.promptRegistryLocation` matches the UC `catalog.schema` used for prompts.
- [ ] Every `register_prompt` name uses three-level UC qualification when your workspace requires it.
- [ ] Template bodies use `{{ variable }}` syntax for MLflow prompt variables.
- [ ] After each successful registration, aliases used by loaders (`production`, `latest`, etc.) are updated.
- [ ] Trace-linked paths call `load_prompt` while a trace is active where Linked Prompts matter.
- [ ] Registration tries fallback names from `prompt_name_candidates()` when the first name fails.
- [ ] Deployed apps use documented `prompts:/...@{alias}` URIs (single slash, not the forbidden double-slash form).
- [ ] When linking traces to deployed revisions, `MLFLOW_ACTIVE_MODEL_ID` is set in the app/serving environment.

---

## Example Script (Reference Implementation)

**Example script** (copy or adapt): [`scripts/register_prompts.py`](scripts/register_prompts.py) — experiment tag → register → alias → verify; supports `--template-text` / `--template-file`, `--alias`, `--dry-run`, `--tags`. Run `python scripts/register_prompts.py --help` for flags.

---

## References

### Official documentation (Databricks)

- [Prompt Registry](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/prompt-registry/)
- [Link production traces to app versions](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/link-production-traces-to-app-versions)
- [Use prompts in deployed apps](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/prompt-registry/use-prompts-in-deployed-apps)

### MLflow docs (cross-check)

[Prompt Registry](https://mlflow.org/docs/latest/genai/prompt-version-mgmt/prompt-registry/) · [Create/edit prompts](https://mlflow.org/docs/latest/genai/prompt-version-mgmt/prompt-registry/create-and-edit-prompts) · [Databricks reference](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/prompt-registry/reference) · [Use prompts in apps](https://mlflow.org/docs/latest/genai/prompt-registry/use-prompts-in-apps/)

### Local deep-dives

| File | Topic |
|------|-------|
| [references/uc-schema-linkage.md](references/uc-schema-linkage.md) | Experiment tag, permissions, multi-schema patterns |
| [references/ab-testing.md](references/ab-testing.md) | Champion/challenger aliases, evaluation, promotion & rollback |
| [references/loading-patterns.md](references/loading-patterns.md) | `load_prompt()`, caching, trace linking, variable injection |
| [references/ownership-conflict-handling.md](references/ownership-conflict-handling.md) | Ownership conflicts, fallback names, error classification |

### Related skills

[04-evaluation-runs](../04-evaluation-runs/SKILL.md) · optional multi-agent / Genie orchestration via upstream [`databricks-agent-bricks`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-agent-bricks) + [`databricks-genie`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-genie)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2026-04-10 | De-coupled from repo-specific imports. Grounded in official Databricks Prompt Registry docs. Added deployed application prompt patterns and production trace linking. |
| 3.1.0 | 2026-03-27 | Added 4 reference deep-dives, `register_prompts.py` script, Do's/Don'ts table, version history, reference pointers after code blocks. |
| 3.0.0 | 2026-03-26 | Rewritten for native `mlflow.genai` Prompt Registry. Dropped legacy UC-table patterns. Added fallback naming, instruction versioning, validation checklist. |
| 2.0.0 | 2026-03-20 | Added alias management, trace linking, A/B testing section. |
| 1.0.0 | 2026-03-15 | Initial skill: basic registration and UC-qualified naming. |
