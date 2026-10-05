---
name: developing-genkit-python
description: Build and maintain Genkit applications in Python with provider-neutral model configuration, flows, tools, structured output, evaluation, and Dev UI.
---

# Genkit Python

Work from the project's installed Genkit version and chosen provider. Genkit Python is preview software and its API changes quickly, so verify every generated API against the installed package or current official documentation.

## Guardrails

- Inspect `pyproject.toml`, lockfiles, imports, Python version, existing plugins, and environment-variable names before proposing changes.
- Do not install a CLI, package, provider plugin, or model automatically. Dependency changes require the user's request to include them or explicit approval.
- Prefer a project-local environment and locked dependencies. Do not use global `npm install -g`, unpinned `curl | sh`, or system `pip` as an implicit repair.
- Preserve the configured provider. If none exists, present choices based on deployment, privacy, region, capability, latency, and cost; do not pick a vendor by default.
- Never hard-code a "latest" model alias for production. Resolve a model supported by the installed plugin at implementation time and keep the model ID configurable.
- Never print, commit, or place API keys in example commands. Use documented environment variables and `.env` files excluded from version control.

## Source of Truth Order

1. installed package metadata and source in the active environment;
2. project lockfile and existing working code/tests;
3. [current Genkit Python documentation](https://genkit.dev/docs/python/overview/);
4. the selected provider plugin's current documentation.

If these disagree, follow the installed version for an existing project and document any planned upgrade separately.

## Workflow

### 1. Inspect

Record:

- Python and Genkit versions;
- package manager and lockfile;
- registered Genkit plugins;
- configured default model and per-call overrides;
- flows, tools, prompts, evaluators, and deployment entry point;
- current test, typecheck, lint, and Dev UI commands.

The official Python guide currently lists Python 3.10 or later, but an existing project may impose a narrower supported range. Do not rewrite its interpreter constraint without evidence.

### 2. Choose provider and model explicitly

Use the provider already configured by the project. Keep the model behind configuration:

```python
import os

MODEL_ID = os.environ["GENKIT_MODEL_ID"]
```

Register only the plugin required by that ID. A model name is normally namespaced by its plugin, but exact syntax must be verified against the installed version. Validate capabilities such as tools, structured output, images, streaming, embeddings, and safety controls before using them.

For a new project, give a small decision table rather than silently selecting a provider:

| Requirement | Verify before selection |
|---|---|
| Local or private execution | self-hosting support, data path, hardware |
| Managed production | region, retention, IAM, quotas, SLA |
| Tool use or structured output | plugin/model support and schema behavior |
| Multimodal input | supported media types and size limits |
| Cost-sensitive workload | current pricing, rate limits, caching |

### 3. Implement the smallest flow

Follow symbols present in the installed package. A conceptual shape is:

```python
from pydantic import BaseModel

class Request(BaseModel):
    topic: str

class Response(BaseModel):
    summary: str

# Define a flow using the installed Genkit API.
# Pass MODEL_ID or the configured model explicitly.
# Validate input and structured output at the application boundary.
```

Do not invent decorators or copy an example from another SDK language. Confirm whether the installed release expects `ai.run_main`, an application server, or ordinary Python execution.

### 4. Tools and external effects

- Give every tool an object-shaped, validated input schema.
- Keep tool descriptions precise enough for safe selection.
- Separate read-only tools from mutating tools.
- Require confirmation for irreversible, costly, privileged, or external actions.
- Add timeouts, retries with limits, idempotency where needed, and safe error messages.
- Treat model-produced tool arguments as untrusted input.

### 5. Prompts and structured output

- Keep stable instructions separate from user data.
- Delimit untrusted content and state that it is data, not instructions.
- Prefer schema-constrained output when the selected model/plugin supports it.
- Validate output server-side even when the SDK reports structured data.
- Version prompts and preserve evaluation fixtures before changing behavior.

### 6. Verify

Run the narrowest meaningful checks:

1. import/startup test;
2. flow input and output validation;
3. a mocked provider test where possible;
4. one explicit live smoke test only when credentials, network use, and cost are authorized;
5. typecheck, lint, and project tests;
6. Dev UI inspection when it adds diagnostic value.

Record the installed versions, configured provider/model source, commands, and skipped checks.

## Troubleshooting Order

1. capture the exact exception and failing call;
2. verify active interpreter and installed distributions;
3. compare imports and call signatures with installed source;
4. verify plugin registration and namespaced model resolution;
5. check required environment variables without exposing values;
6. isolate network, credential, quota, model-capability, and schema failures;
7. reproduce with the smallest flow;
8. consult current official docs for the installed release line.

Do not solve an API mismatch by upgrading every package. Propose the smallest compatible change and include rollback.

## Completion Gate

- Provider and model were selected from project requirements, not a hard-coded assistant preference.
- Dependency changes were authorized and locked.
- Examples match the installed Genkit Python API.
- Secrets and tool inputs are protected.
- Tests cover validation and external-effect boundaries.
- Preview/upgrade risk and skipped live checks are explicit.
