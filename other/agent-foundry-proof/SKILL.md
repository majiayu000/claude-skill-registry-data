---
name: agent-foundry-proof
description: "Orchestrate the first production proof of an AgentFoundry AI-native iOS product with one upfront setup authorization and autonomous continuation. Use for a new product idea that needs a real SwiftUI/TCA iPhone app, a generated and verified production App Icon, Firebase-authenticated durable chat, backend OpenAI Agents SDK work, and optionally typed artifact UI or safe operational domain tools. This skill selects and applies reusable proof contours instead of regenerating boilerplate."
---

# AgentFoundry Proof

## Outcome

Turn a product idea into the smallest real AgentFoundry iPhone proof:

- native SwiftUI/TCA app targeting iOS 26.1;
- Firebase Anonymous Auth with backend token verification;
- server-owned OpenAI Agents SDK runtime and secret;
- durable sessions/messages with asynchronous agent work and restore;
- product-specific design derived from the TravelPlanner2 golden reference;
- generated product-specific App Icon, compiled into the app and verified at runtime;
- optional native durable artifact and/or operational records;
- build, deployment, runtime evidence, and a completed proof report.

Do not generate this architecture from scratch. Compose the bundled capability skills and customize only product-specific behavior.

## Required Companions And References

Always read and apply:

1. `references/product-proof-contract.md` for completion and stop gates.
2. `references/upfront-authorization.md` for the single permission request and authorization ledger.
3. `../agent-foundry-design/SKILL.md`, including its routed design references.
4. `../agent-foundry-proof-foundation/SKILL.md` for every new proof.
5. `../agent-foundry-app-icon/SKILL.md` after the product design concept is defined.

Load only when needed:

- `references/backend-architecture.md` before Firebase project mutation, secret setup, deploy, or IAM repair.
- `references/ios-architecture.md` when modifying generated module boundaries or adapting an existing iOS app.
- `../agent-foundry-artifact-ui/SKILL.md` for a generated plan, shortlist, comparison, dashboard, document, case packet, or other durable product artifact.
- `../agent-foundry-proof-domain-tools/SKILL.md` for bookings, CRM records, orders, inventory, tasks, approvals, work orders, or other mutable operational records.
- `references/proof-report.md` when completing the report and final verification.

The older prose templates in `references/agent-foundry-modern-ios-base.md`, `references/tca-feature-template.md`, and `references/domain-data-and-agent-tools.md` are compatibility guidance for existing projects. For new projects use the executable foundation and overlay assets.

## Capability Selection

Choose before implementation and record the choice in the proof report.

| Product need | Foundation | Artifact UI | Domain tools |
|---|---:|---:|---:|
| Conversation/assistant only | required | no | no |
| Agent creates a durable result the user views or edits | required | required | optional |
| Agent reads or mutates operational records | required | optional | required |
| Agent manages records and produces a plan/dashboard/document | required | required | required |

Do not add domain tools merely because the backend uses Firestore for chat. Do not omit artifact UI when the useful output is a durable product object and text alone would leave the app as a chat wrapper. Keep `agent-foundry-proactive` outside the first proof unless the user explicitly asks for proactive behavior.

## Read-Only Preflight And Single Authorization

Discover without mutating or exposing credentials:

- product display name, Swift name, slug, and bundle identifier;
- one-sentence first agent workflow and durable core object;
- existing target directory versus a new project;
- Firebase project and billing state/options;
- Firebase region;
- selected capability contours;
- reusable existing OpenAI credential presence versus a new product-scoped key;
- preferred real iPhone when connected, otherwise Simulator;
- one proposed App Icon metaphor direction, product-aligned palette, generation output paths, and Image API use covered by the upfront ledger.

Lists of local Firebase/GCP/OpenAI/Apple resources are discovery only. Never select or mutate them merely because a matching resource exists.

Before scaffold or any persistent mutation, follow `references/upfront-authorization.md`: present one complete manifest covering product/scaffold values, Firebase project and immutable region, billing/Blaze, Anonymous Auth, Firestore, all required service APIs, app registration, secret and deploy, OpenAI key reuse/creation plus exact ignored staging path, narrow conditional IAM, and Apple signing when applicable. Ask for one confirmation only.

After confirmation, record an authorization ledger and continue autonomously. Do not ask separately before scaffold, Firebase project creation, billing linkage, API enablement, Anonymous Auth, Firestore creation, OpenAI key creation/destination, secret upload, deploy, or ledger-covered narrow IAM. Do not ask the user to reply `готово`; verify state directly and resume.

Use `openai-platform-api-key` for secure key reuse/creation. Treat the single upfront manifest as that skill's required credential-decision message: it must be the next substantive message after safe credential inspection, resolve reuse versus creation, and confirm the exact ignored local staging destination. Do not send a standalone credential question or invoke a second destination-confirmation form when the ledger contains the exact path. A hosted picker may still require the user to select an OpenAI organization/project, but its follow-up is not a new permission question. Continue automatically, transfer the key with `scripts/promote-openai-key.mjs`, verify secret metadata, and delete only the dedicated staging file. Never request or print a plaintext key, pass it to a scaffold command, or use a generic cross-project secret by default.

## Execution

### 1. Scaffold Or Adapt

For a new project, run the foundation scaffold exactly as its skill specifies. Do not read or retype its assets. It creates the Tuist/TCA graph, Firebase-only app composition boundary, authenticated backend client, durable chat lifecycle, block-aware Markdown renderer, asynchronous Functions worker, deny-by-default rules, and proof report.

For an existing project, inspect current architecture first. Reuse compatible files and patch deliberately; never apply an overlay that would overwrite user code. Use the foundation template only as a comparison source when needed.

### 2. Apply Product Design

Use TravelPlanner2 as the golden reference through `agent-foundry-design/references/product-workspace-language.md`:

- define navigation/continuity, durable workspace, and agent presence;
- replace the neutral palette with a product-specific atmospheric color story;
- keep soft coherent geometry and selective Liquid Glass;
- make the durable product object visually primary when one exists;
- preserve context between artifact/domain surfaces and chat;
- design empty, loading, generating, partial/stale, failed, and restored states.

Do not ship the neutral template palette/copy as final design and do not copy travel-specific metaphors into unrelated products.

### 3. Apply Optional Contours

If artifact UI is selected, run its bundled overlay once for the first artifact type, replace the generic payload with the real schema, persist it as the product source of truth, and wire its inline card to a typed TCA detail route.

If domain tools are selected, run its bundled overlay once for the first operational model, replace generic fields and tool names with workflow language, derive owner/org scope from verified auth context, and wire validated endpoints plus agent tools. Use transactions, expected versions, idempotency, audit fields, and confirmation gates.

Both contours may be used together. The artifact may summarize or organize domain records, but it must not bypass domain authorization or mutation invariants.

### 4. Customize The Agent

Change the generated server agent name/instructions for the one-sentence product workflow. Add only tools required for the first slice. The backend remains the sole owner of model calls and provider credentials.

The message lifecycle remains:

```text
iOS creates stable session/message ids
-> authenticated sendMessage validates and commits the user message/job
-> response returns accepted/latest durable snapshot
-> backend worker runs the agent
-> assistant Markdown and optional artifact/domain changes are validated and persisted
-> iOS polling/foreground refresh restores latest state without changing selection unexpectedly
```

Repeated submission of the same message id must not duplicate messages or jobs.

### 5. Configure Firebase And Credentials

After the single setup authorization:

- create or select the exact authorized Firebase project and link the authorized billing account when applicable;
- register the exact iOS bundle id and install `GoogleService-Info.plist` without committing secrets;
- enable/verify Anonymous Auth;
- enable/verify Firestore, Secret Manager, Functions, Cloud Build, Artifact Registry, Cloud Run, Eventarc, Pub/Sub, Cloud Storage, Firebase, Identity Toolkit, and Secure Token APIs in one batch where possible;
- create/verify the default Firestore database in the authorized immutable region;
- create or securely reuse the authorized OpenAI API key through `openai-platform-api-key`, promote it into the generated product-specific secret by metadata-only verification, and remove a dedicated temporary staging file;
- install/build backend dependencies;
- deploy rules/indexes/functions to the user-selected project;
- apply only authorization-ledger-covered, error-proven, narrow IAM repair as described in `references/backend-architecture.md`.

Drive available browser/tool flows for billing and credentials, poll metadata after platform gates, and continue without asking for a status reply. Login, OAuth/2FA, payment method, hosted OpenAI picker, OS permission, Apple account/team, and physical device trust may still require direct user interaction because the platform owns those gates. If one blocks deployment, finish independent work and surface only that exact platform action. Never replace the real agent with a mock to claim completion.

### 6. Generate And Ship The App Icon

Run `agent-foundry-app-icon` after the visual concept/color story exist and the authorized product-scoped credential is usable. Derive one simple product-specific metaphor, write the detailed English prompt, generate an opaque full-bleed 1024x1024 master, inspect it at full size and 40x40, and make only targeted iterations.

Persist the master in `output/imagegen`, wire it into `AppIcon.appiconset`, regenerate the source project graph when required, and verify `actool`, built bundle icon files/`Assets.car`, primary-icon metadata, install, and launch. Do not claim completion from an image file or successful build alone.

Image generation, authorized key use, project asset mutation, signing, install, and launch must be covered by the single upfront ledger. Reuse the already authorized product-scoped credential path without printing or persisting plaintext and without starting a second key-creation flow.

### 7. Verify

Run the foundation validator, backend build/tests, Tuist generation, iOS tests/build, and real runtime smoke test. Prefer a connected usable iPhone; otherwise use Simulator.

Evidence must prove:

- launch and anonymous authentication;
- authenticated message acceptance;
- real backend Agents SDK response, not hardcoded text;
- user message persisted before model work;
- generating state followed by durable assistant Markdown;
- close/relaunch restores sessions and selected context safely;
- retrying a message id is idempotent;
- selected artifact/domain contour restores and enforces its contract;
- the final App Icon is opaque 1024x1024, remains legible at 40x40, is compiled by `actool`, appears in primary-icon bundle metadata, and the build containing it installs/launches on the selected target;
- no provider secret or Firebase import exists in feature modules;
- main design states pass clickability, shadow/clipping, light/dark, and Dynamic Type QA.

Scaffold validation alone is not production-proof evidence.

## Completion

Complete `AGENTFOUNDRY_PROOF_REPORT.md` using `references/proof-report.md`. Include capability selection, architecture, Firebase project/region, secret resource name only, approved persistent changes, build/deploy commands and outcomes, runtime evidence, design concept, App Icon metaphor/prompt/master/asset/build evidence, verified states, and remaining blockers.

Claim the proof complete only when `references/product-proof-contract.md` passes. Otherwise state the exact smallest blocker and do not describe planned or mocked behavior as verified.
