---
name: agent-foundry-proof-foundation
description: "Scaffold the reusable production foundation for a new AgentFoundry SwiftUI iOS proof: Tuist plus TCA, Firebase app bootstrap and Anonymous Auth token injection, authenticated durable chat, backend-owned asynchronous OpenAI Agents SDK work, Firestore restore, polling, Markdown rendering, and proof-report structure. Use from agent-foundry-proof after product name, bundle identifier, and Firebase project choice are confirmed."
---

# AgentFoundry Proof Foundation

## Purpose

Create the product-neutral, buildable base of an AgentFoundry proof by rendering bundled assets instead of regenerating boilerplate. Keep product reasoning and product-specific UI outside this skill.

## Required Companion

Read and apply `../agent-foundry-design/SKILL.md` before changing the generated SwiftUI surfaces. The bundled design system is a universal starting point, not permission to skip product-specific design and visual QA.

## Inputs

Require these confirmed values before scaffolding:

- Product display name.
- Swift type/module name.
- Lowercase product slug.
- iOS bundle identifier.
- User-selected Firebase project id or an explicitly approved newly created id.
- Firebase region.

Generate a product-scoped secret resource name by default. Never accept a secret value as a script argument.

## Scaffold

Run the bundled script without reading or rewriting the template assets:

```sh
node <skill-dir>/scripts/scaffold-proof.mjs \
  --output <target-directory> \
  --product-name "<Product Name>" \
  --swift-name <ProductSwiftName> \
  --slug <product-slug> \
  --bundle-id <bundle.identifier> \
  --firebase-project-id <project-id> \
  --region <firebase-region>
```

The script refuses to overwrite a non-empty directory, renders filenames and contents, writes `.agentfoundry-proof.json`, and fails if a placeholder remains.

Read `references/template-contract.md` only when changing template internals, adding a placeholder, or diagnosing scaffold output.

## Product Extension Points

After scaffolding, change only what the product requires:

- Product agent name and instructions in `functions/src/agent.ts`.
- Product palette, ambient fields, symbols, and copy in the DesignSystem module.
- Product-specific empty-state prompts and session naming.
- Domain artifact or durable records through the selected optional capability skill.

Do not regenerate the foundation files from prose. Patch the rendered files when a product-specific difference is necessary.

## Capability Routing

- Use only this skill for chat-first proofs with no durable product object beyond the transcript.
- Also use `agent-foundry-artifact-ui` when the agent produces a plan, comparison, document, dashboard, shortlist, or another typed durable artifact.
- Also use `agent-foundry-proof-domain-tools` when the product reads or mutates bookings, CRM objects, inventory, orders, tasks, work orders, or other operational records.
- Apply both optional skills when the product needs both operational records and a generated artifact surface.
- Keep `agent-foundry-proactive` as a later product-evolution step, not part of the first foundation scaffold.

## Verification

Run:

```sh
node <skill-dir>/scripts/validate-proof.mjs <target-directory>
```

Then install dependencies, generate with Tuist, build the backend and iOS app, and complete the deployment/runtime gates owned by `agent-foundry-proof`. Do not claim a production proof from scaffold validation alone.
