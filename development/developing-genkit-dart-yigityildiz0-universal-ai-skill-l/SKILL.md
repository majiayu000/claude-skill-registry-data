---
name: developing-genkit-dart
description: Build and troubleshoot Genkit applications in Dart with installed-version-first APIs, provider-neutral model configuration, flows, tools, schemas.
license: MIT
---

# Genkit Dart

Inspect `pubspec.yaml`, lockfile, Dart/Genkit/plugin versions, imports, configured provider/model, flows, tools, deployment, and tests. Dart support may evolve quickly; verify symbols and compatibility against installed packages and current official Genkit/provider documentation.

## Guardrails

- Do not run global installs, broad upgrades, `latest`, or network setup scripts implicitly.
- Preserve the project's provider. If none exists, present choices by deployment, privacy, region, capability, latency, cost, and support maturity.
- Keep the exact model ID in validated configuration and verify current plugin support at implementation time.
- Never expose keys in mobile/web clients, source, logs, or prompts. Put privileged provider calls behind an appropriate trusted boundary.

## Implementation

1. Register only needed plugins using APIs present in the installed version.
2. Define typed/validated input and output schemas plus application invariants.
3. Separate stable instructions from untrusted user/retrieved content.
4. Give tools strict schemas, least privilege, authorization, timeouts, idempotency, and confirmation for destructive/costly/external effects.
5. Bound tool rounds, retries, concurrency, tokens, time, and spend.
6. Keep provider/model configuration outside reusable flow code where the installed API allows it.
7. Add observability without logging secrets or sensitive payloads.

Conceptual configuration:

```dart
final modelId = Platform.environment['GENKIT_MODEL_ID'];
if (modelId == null || modelId.isEmpty) {
  throw StateError('GENKIT_MODEL_ID is required');
}
// Pass modelId through the API supported by the installed provider plugin.
```

## Verify

Run analyzer/format/tests/build, schema tests, mocked provider/tool tests, timeout/cancellation/retry/authorization cases, and a bounded live smoke test only when credentials/network/cost are authorized. Report installed versions, configuration source, commands, deployment/data boundary, and skipped checks.
