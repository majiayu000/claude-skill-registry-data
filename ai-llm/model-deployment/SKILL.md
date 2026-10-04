---
name: model-deployment
description: Deploy a new LLM model via LiteLLM (GitOps) and/or Azure (Terraform + node backend), add it to the ai toolkit, create the required pull requests, and verify end-to-end. Use when rolling out a model to any environment, adding a model to the toolkit, troubleshooting "model not available" errors, or finding pricing/token limits/model ids for any provider.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "3.1.0"
  languages: all
  audience: developers operators
  workflow: operations
  since: "2026-04-15"
---

# Model deployment (LLM — any provider)

This skill guides the full lifecycle of deploying a new LLM model across the Unique platform:

- **monorepo** — LiteLLM proxy config (GitOps), node-chat backend (Azure track), Terraform
- **ai repo** — toolkit language model registry (`LanguageModelInfo`)

**Cardinal rule:** never guess token limits, capabilities, pricing, or provider strings. Always cite the source (model card URL, LiteLLM registry, Jira ticket, or PR). If no authoritative source exists, ask the user.

## When to use this skill

- Deploying a new model to Dev, QA, UAT, or Prod (any provider).
- Adding a model to the LiteLLM proxy and/or Azure OpenAI.
- Adding a model to the ai toolkit language model registry.
- Troubleshooting "model not available on cluster" or config-sync issues.
- Finding pricing, token window sizes, or model identifiers for any provider.

---

## Step 0 — Gather information before touching any file

| Question | Why |
|----------|-----|
| **Track:** `azure`, `litellm`, or `both` | Determines which repos/files to touch |
| **Environments** and **rollout order** (e.g. qa → uat01 → prod) | Controls which overlay files are edited and in what sequence |
| **Model identifiers** — For LiteLLM: user-facing `model_name` + provider model string. For Azure: model name, version, deployment names, API version, capacity | Required for config entries |
| **Token limits / capabilities** — with a cited source | Required for toolkit `LanguageModelInfo` |
| **Toolkit:** already merged / has open PR / needs to be done now? | Avoids duplicate work |
| **Allowlist / exposure constraints** | Determines selectability — see [MODEL-SELECTABILITY.md](references/MODEL-SELECTABILITY.md) |

### Where to find model facts

| Fact | Where to look |
|------|---------------|
| **Azure model deployments** | [Azure AI Foundry](https://ai.azure.com/) — Deployments page (single source of truth for Azure) |
| **Token window** | Vendor model card: [OpenAI](https://platform.openai.com/docs/models), [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models), [Google](https://deepmind.google/models/), [LiteLLM registry](https://models.litellm.ai/) |
| **Pricing** | [Azure AI Foundry](https://ai.azure.com/) Quota page, [OpenAI](https://openai.com/api/pricing/), [Anthropic](https://www.anthropic.com/pricing), [Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/pricing) |
| **Model identifiers / provider prefix** | [LiteLLM model registry](https://models.litellm.ai/) |
| **API version (Azure)** | [Azure AI Foundry](https://ai.azure.com/) Deployments page or Azure REST API changelog |
| **Capabilities** | Vendor model cards, release blog posts, changelogs |

---

## Repo and file map

| Repo | What you touch |
|------|----------------|
| **monorepo** | LiteLLM overlay: `gitops-resources/argocd/clusters/<cluster>/<env>/value-overlays/litellm.yaml`. Node-chat: language-model enum + Azure factory config. Terraform: `azurerm_cognitive_deployment`, Key Vault secret. |
| **ai repo** | Toolkit: `LanguageModelName` enum + `LanguageModelInfo.from_name()` case + tests in `unique_toolkit/unique_toolkit/language_model/infos.py`. |

```
gitops-resources/argocd/clusters/
├── unique/          # multi-tenant: qa/, uat01/, prod/, us01/
├── <single-tenant>/ # e.g. tree, burger, cat, ...
```

---

## Track A — LiteLLM (GitOps)

### A1) Validate model id and provider prefix

1. Search [LiteLLM model registry](https://models.litellm.ai/) for the model.
2. Document the two strings: **user-facing key** (`model_name`, no prefix, hyphens) and **provider model** (`litellm_params.model`, with prefix).

See [LITELLM-CONFIG.md](references/LITELLM-CONFIG.md) for config examples and provider prefix conventions.

### A2) Update ArgoCD overlay(s)

Edit `monorepo/gitops-resources/argocd/clusters/<cluster>/<env>/value-overlays/litellm.yaml`. Add a new entry under `proxy_config.model_list`, following the existing alphabetical grouping style.

### A3) Monorepo PR

- **Branch:** `feat/litellm-<model-name>`
- **Commit:** `feat(litellm): add <model_name> model to <envs>`
- Commit, push, and create the PR after validation. Include the env overlays changed, model names, source links, and verification steps in the PR body.

### A4) After merge — sync + restart

1. In ArgoCD, sync the LiteLLM application for the target environment.
2. **Roll the LiteLLM Deployment** (not HPA — restarting HPA does not reload pods).

### A5) Verify

1. Confirm model appears in LiteLLM dashboard.
2. Smoke test with the exact model id users will request (e.g. `litellm:<model_name>`).

---

## Track B — Azure (Terraform + node backend)

### B1) Gather Azure deployment details

Check [Azure AI Foundry](https://ai.azure.com/) first — the Deployments page lists all active model deployments with name, version, capacity, rate limits, and retirement dates.

Confirm: Azure OpenAI account, model name + version, deployment names, capacity, API version.

### B2) Terraform changes

Add `azurerm_cognitive_deployment` resource(s) in the **infrastructure** repo. See [AZURE-NODE-CHAT.md](references/AZURE-NODE-CHAT.md) for Terraform patterns.

### B3) Node backend registration

Three files in `next/services/node-chat/src/openai/`: `language-model.enum.ts`, `azure-sdk-openai.service.factory.ts`, `azure-sdk-openai.service.ts`. See [AZURE-NODE-CHAT.md](references/AZURE-NODE-CHAT.md) for code examples.

### B4) PR + apply workflow

1. Create PR; link to Jira ticket and source docs.
2. Review Terraform plan — stop if unexpected drift appears.
3. Apply via Atlantis, one workspace at a time.

### B5) Verify

1. Confirm deployments exist in [Azure AI Foundry](https://ai.azure.com/).
2. **Roll the node-chat Deployment** (not HPA).
3. Smoke test **both** plain chat (node-chat) **and** agentic assistant space (assistants-core) — bugs can hide in one path. See [LESSONS-LEARNED.md](references/LESSONS-LEARNED.md) for why.

---

## Model selectability

Two layers control whether a model is available and user-selectable. See [MODEL-SELECTABILITY.md](references/MODEL-SELECTABILITY.md) for full details.

Quick decision matrix:

| Want the model to... | `UNIQUEAI_SUPPORTED_MODELS` | `UNIQUEAI_ALLOWED_MODELS` |
|---|---|---|
| Be available and selectable by users | Add | Add |
| Be available but only for internal use | Add | Do **not** add |
| Not be available at all | Do **not** add | N/A |

---

## Track C — AI toolkit

### C1) Check existing state

Check whether the model already exists in `unique_toolkit/unique_toolkit/language_model/infos.py` (merged, open PR, or needs to be added).

### C2) Add model to toolkit

Add `LanguageModelName` enum entry and `LanguageModelInfo.from_name()` case. See [TOOLKIT-REGISTRY.md](references/TOOLKIT-REGISTRY.md) for code examples and field reference.

**Critical:** for `default_options`, use the string `"none"` — never Python `None`. See [LESSONS-LEARNED.md](references/LESSONS-LEARNED.md).

### C3) PR + release

- **Branch:** `feat/toolkit-<model-slug>`
- **Commit:** `feat(toolkit): add <model_name> model info`
- Commit, push, and create the PR after validation. Include the exact model identifier, cited model specifications, and tests run in the PR body.
- Merge with a conventional commit (`feat(toolkit): add <model_name> model info`). release-please updates `unique_toolkit` version and `CHANGELOG.md` on the standing Release PR — do not edit those files in the feature PR.

For early exposure before the toolkit release, use the `LANGUAGE_MODEL_INFOS` env override — see [TOOLKIT-REGISTRY.md](references/TOOLKIT-REGISTRY.md).

---

## Multi-cluster rollouts

1. **One monorepo PR** touching multiple cluster overlays.
2. After merge, rollout **per cluster**: ArgoCD sync → roll Deployment → verify + smoke test.
3. Repeat in the agreed rollout order.

---

## Pull request completion

When implementing a model deployment, finish each repository's code changes by:

1. Running the relevant formatter, linter, and targeted tests.
2. Committing with the track's conventional commit message.
3. Pushing the branch and creating a non-draft PR.
4. Linking the Jira ticket and authoritative model sources in the PR body.
5. Returning every created PR URL to the user.

Create separate PRs for separate repositories. A direct request to run this skill and implement the deployment authorizes creating the required PRs; stop before PR creation only when the user asks for local changes, a draft, or a plan.

---

## Final checklist (every track)

- [ ] Required PRs created and URLs returned
- [ ] Correct environment(s) targeted and rollout order followed (qa → uat → prod)
- [ ] Config synced in ArgoCD where applicable
- [ ] Correct **Deployment** rolled (not HPA)
- [ ] Smoke test succeeded using the exact model id users will request
- [ ] Sources cited for token limits, capabilities, and model identifiers
- [ ] **Model selectability decided:** added to `UNIQUEAI_SUPPORTED_MODELS` (cluster-available) and, if user-facing, to `UNIQUEAI_ALLOWED_MODELS` env var
- [ ] Rollout notes captured (Jira comment + links + timestamps)

---

## Rollback and safety

- **Explicit approvals required** before editing committed code, suggesting Atlantis apply, or anything affecting production.
- If Terraform drift or "model not discoverable" looks wrong: **stop**, explain what you see, propose the smallest safe next action.
- For incident patterns and past mistakes, see [LESSONS-LEARNED.md](references/LESSONS-LEARNED.md).
