---
name: firebase-ai-logic-basics
description: Integrate Firebase AI Logic safely across web, Android, Apple, Flutter, or Unity; choose the Firebase-supported Gemini API backend and a verified model.
---

# Firebase AI Logic

Firebase AI Logic is a Firebase-specific integration and therefore uses models and backends supported by Firebase. Be model-version neutral within that product: verify current support and choose from requirements instead of automatically selecting a named model or a `latest` alias.

## Non-Negotiable Safety Rules

- Inspect the platform, existing Firebase app, SDK version, lockfiles, selected project, billing plan, and current backend before changing anything.
- Do not globally install Firebase CLI or run `npx -y ...@latest`. Prefer an existing project-local CLI; otherwise propose a pinned version and obtain authorization for the dependency change.
- Project creation, `firebase use`, API enablement, billing changes, App Check enforcement, Remote Config publishing, and deployment alter external state. Preview the target project and get confirmation unless the user explicitly requested that exact action.
- Never expose service-account credentials or API keys. Do not put a privileged server credential in client code.
- Do not assume a model is available because its name sounds recent. Verify it against the current official Firebase AI Logic model page and the chosen backend.
- Prefer an explicit stable production model. Preview or experimental models require an explicit prototyping reason and retirement plan.

## Decide the Backend

Firebase AI Logic supports a Gemini Developer API backend and a Vertex AI Gemini API backend. Choose using current documentation and project requirements:

| Requirement | Verify |
|---|---|
| Prototype or simple Firebase client | plan, regional availability, quotas, supported models |
| Enterprise IAM, region, or Vertex controls | Blaze requirements, location, quotas, supported models |
| Existing production project | preserve its backend unless migration is requested |

Do not claim one backend is universally the default. Record the selected backend and why.

## Model Policy

At implementation time:

1. open the [official supported models page](https://firebase.google.com/docs/ai-logic/models);
2. filter by the selected backend, platform, capability, region, billing, and release stage;
3. prefer a current explicit stable model for production;
4. verify text, image, audio, video, PDF, tool/function calling, structured output, and streaming support independently;
5. place the model name behind configuration rather than scattering it through code.

For deployed applications, use [Firebase Remote Config](https://firebase.google.com/docs/ai-logic/solutions/remote-config) for the model name and other safe-to-vary generation settings. Give it a known-good client default, validate fetched values against an allowlist, and roll changes out gradually. Remote Config is not a substitute for server-side authorization or secret storage.

Conceptual configuration:

```text
model_name = remote_config("model_name", known_good_stable_default)
assert model_name in approved_model_allowlist
```

Do not copy a model identifier from this skill; use the currently verified value.

## Workflow

### 1. Inspect without mutation

- identify web, Android, Apple, Flutter, or Unity;
- inspect Firebase SDK/BoM and lockfile versions;
- read `.firebaserc` and `firebase.json` without changing the selected project;
- confirm Firebase app initialization order;
- identify current backend, model configuration, App Check, Remote Config, analytics, and consent requirements;
- capture the project's existing test and emulator workflow.

### 2. Plan dependencies

Use the platform's official Firebase SDK package and the existing package manager. Keep versions governed by the project's lockfile or Firebase BoM. Present the exact proposed diff before adding or upgrading dependencies.

Use a local CLI invocation such as the project's package script or pinned `firebase-tools` dev dependency. Never let an unreviewed latest CLI mutate a production project.

### 3. Initialize the service

Follow the current platform-specific [getting started guide](https://firebase.google.com/docs/ai-logic/get-started). Keep Firebase app initialization before AI Logic model creation. Choose the backend explicitly. Use a model name sourced from validated configuration.

### 4. Add the smallest capability

Start with one request and explicit error handling. Then add only the requested features:

- streaming with cancellation and partial-state handling;
- structured output with a schema plus application-side validation;
- multimodal inputs with MIME/type, size, privacy, and storage controls;
- chat with bounded history and a clear reset policy;
- tool/function calling with a server-authorized execution layer;
- image generation only after checking current model and billing support.

Treat all model output and tool arguments as untrusted. The model never grants authorization.

### 5. Production hardening

- Configure App Check in monitor mode before enforcement when appropriate.
- Apply per-user and per-feature quotas and abuse controls.
- Keep sensitive operations on a trusted backend.
- Avoid logging prompts, media, tokens, or personal data by default.
- Define data retention, deletion, consent, and geographic requirements.
- Add Remote Config rollback values and staged rollout.
- Instrument latency, errors, quota exhaustion, safety outcomes, and cost without recording raw sensitive content.

### 6. Verify

Run:

1. platform build/typecheck;
2. initialization-order test;
3. configuration fallback and allowlist tests;
4. structured-output validation tests;
5. tool authorization tests;
6. App Check/emulator checks where supported;
7. one bounded live request only when credentials, billing, and external use are authorized.

Report exact SDK/CLI versions, target Firebase project, backend, model source, test results, and skipped external checks.

## Common Failure Triage

| Symptom | Check first |
|---|---|
| permission denied | target project, service provisioning, backend, App Check, IAM, billing |
| model not found | current Firebase-supported model list, backend, location, retirement status |
| quota or billing error | plan, quotas, selected API backend, request size |
| startup crash | Firebase app configured before model construction |
| schema mismatch | selected model capability and application-side validation |
| released app breaks after retirement | Remote Config fallback, approved model rollout, rollback |

## Completion Gate

- No global or unpinned auto-install command was introduced.
- Target project and external mutations were explicit.
- Model choice was verified from current Firebase documentation.
- Production uses an explicit stable model and a safe remote migration path.
- App Check, authorization, privacy, quotas, and rollback were addressed.
- Platform build and focused tests pass, or skipped checks are clearly stated.
