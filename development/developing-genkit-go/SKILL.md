---
name: developing-genkit-go
description: Build and maintain Genkit applications in Go with provider-neutral model configuration, flows, tools, structured output, streaming, middleware, and Dev UI.
---

# Genkit Go

Use the project's installed Genkit module and configured provider as the source of truth. Verify fast-changing APIs against `go.mod`, installed module source, tests, and current official Genkit Go documentation.

## Guardrails

- Inspect `go.mod`, `go.sum`, imports, existing plugins, environment variables, and entry points first.
- Do not run `go get ...@latest`, `go mod tidy`, an install script, or a global CLI install unless dependency changes are already authorized.
- Preserve the configured provider. If none exists, compare available plugins against deployment, privacy, region, capabilities, latency, and cost; do not choose one automatically.
- Never embed a named newest model in a reusable example. Resolve a model supported by the configured plugin at implementation time and source the ID from project configuration.
- Keep secrets out of source, logs, command history, and examples.
- Treat model-produced tool inputs as untrusted and bound every external side effect.

## Source of Truth Order

1. the project's `go.mod`, `go.sum`, tests, and working code;
2. the exact Genkit module source in the module cache;
3. [current Genkit Go documentation](https://genkit.dev/docs/go/);
4. current documentation for the selected provider plugin.

For an existing project, follow its installed release even when a newer guide differs. Propose upgrades separately with compatibility tests and rollback.

## Workflow

### 1. Inspect

Record:

- Go and Genkit module versions;
- registered plugins and configured model source;
- flows, prompts, tools, middleware, and HTTP handlers;
- deployment target and data boundary;
- existing build, test, lint, and Dev UI commands.

### 2. Configure provider and model

Use the provider already present in the project. Keep the model name in validated configuration rather than a hard-coded sample:

```go
modelID := os.Getenv("GENKIT_MODEL_ID")
if modelID == "" {
    return errors.New("GENKIT_MODEL_ID is required")
}
```

Pass that verified value through the API supported by the installed Genkit version. Namespacing and model-reference constructors differ by plugin/release; inspect the installed package before writing the call.

For new work, verify these capabilities independently: structured output, streaming, tool calling, multimodal inputs, embeddings, safety controls, region, quota, and production support.

### 3. Initialize narrowly

Register only required plugins. Pass the Genkit instance explicitly when that matches the installed API; avoid hidden mutable globals. Build the smallest flow first, then add middleware and tools after the basic request is covered by tests.

Conceptual structure, not copy-paste API:

```go
func main() {
    ctx := context.Background()
    modelID := mustConfiguredModelID()
    g := initializeGenkitWithSelectedPlugin(ctx)
    _ = defineValidatedFlow(g, modelID)
}
```

Confirm actual symbol names and signatures from the module source.

### 4. Flows and structured output

- Define typed input and output contracts.
- Add useful schema descriptions without leaking secrets.
- Validate lengths, ranges, formats, and cross-field invariants after generation.
- Propagate context cancellation and deadlines.
- Keep HTTP authentication/authorization outside the model.
- Return safe errors; do not expose prompts, credentials, or provider payloads.

### 5. Tools

- Use object-shaped, strict schemas and clear descriptions.
- Split read-only and mutating operations.
- Enforce authorization in Go code, never in prompt text alone.
- Require approval for destructive, costly, privileged, or externally visible actions.
- Bound tool rounds, concurrency, retries, response sizes, and timeouts.
- Make retried mutations idempotent where possible.

### 6. Middleware and fallback

Use middleware only for cross-cutting behavior that the installed release supports. Be explicit about order. Retry only transient failures with limits and jitter. A fallback model must satisfy the same capabilities, privacy/region constraints, output contract, and authorization requirements; do not silently route data to another provider.

### 7. Dependencies and CLI

Prefer the existing project toolchain. If the CLI is absent, provide the current official installation options and exact proposed version/change; do not execute a network installer implicitly. Keep module changes reviewable, then run `go mod tidy` only as part of an authorized dependency update.

### 8. Verify

Run the smallest relevant checks:

1. `go test` for the affected packages;
2. build and static analysis used by the project;
3. flow input/output and schema tests;
4. mocked provider and tool tests where possible;
5. cancellation, timeout, retry, and authorization tests;
6. one bounded live smoke test only when credentials, network use, and cost are authorized;
7. Dev UI inspection when it adds diagnostic value.

Record exact module versions, provider/model configuration source, commands, and skipped checks.

## Troubleshooting

1. capture the exact error and failing call;
2. verify the active module versions and imported package paths;
3. inspect the installed symbol/signature instead of guessing from memory;
4. confirm plugin registration and model namespace;
5. check credential presence without printing values;
6. separate schema, capability, quota, network, and authorization failures;
7. reproduce with the smallest flow;
8. avoid broad upgrades until the incompatibility is proven.

## Completion Gate

- Provider/model selection came from project requirements and current plugin support.
- No `@latest`, fixed model alias, global install, or implicit network installer was introduced.
- Dependency mutations were authorized and locked.
- Tool and HTTP authorization is enforced in code.
- Tests cover typed output and external-effect boundaries.
- Upgrade, preview, and skipped-live-test risks are explicit.
