---
name: agent-foundry-artifact-ui
description: "Add a typed durable agent-produced artifact, inline native SwiftUI card, and restorable detail surface to an AgentFoundry iOS proof. Use when the useful result is a plan, comparison, shortlist, dashboard, document, case packet, cart, tracker, or other product object rather than only assistant Markdown. Requires agent-foundry-design."
---

# AgentFoundry Artifact UI

## Outcome

Extend the proof lifecycle to:

```text
user message
-> durable assistant Markdown
-> validated/versioned artifact
-> inline native card
-> typed route
-> restorable product detail surface
```

This is fixed-registry native UI, not arbitrary server-driven UI. The backend may choose typed data and safe actions; iOS renders only reviewed SwiftUI artifact types.

## Required Companions And References

Read and apply `../agent-foundry-design/SKILL.md`. Stop before UI work if it is unavailable.

Load:

- `references/agent-surface-contract.md` before schema, persistence, or DTO work.
- `references/qchat-agent-ui-pattern.md` for inline card rendering, actions, and routing.
- `references/travel-planner-pattern.md` for session-level plans, dashboards, or full product workspaces.

The product's explicit schema is authoritative; the references provide safety and lifecycle guardrails.

## First Slice

Choose one artifact type, one version, one inline card, one detail surface, and one safe `open_detail` action. Define:

- product-object source of truth;
- readiness states: `generating`, `needs_input`, `partial`, `ready`, `stale`, `failed` as applicable;
- real data/enrichment requirements;
- message pointer versus session-scoped artifact path;
- version/unknown-type fallback;
- restoration and navigation behavior.

Design around the artifact, not the transcript. The detail screen must be useful without rereading chat.

## Bundled Overlay For New Proofs

When `.agentfoundry-proof.json` exists, apply the bundled extension surface:

```sh
node <skill-dir>/scripts/apply-artifact-overlay.mjs \
  --project <proof-directory> \
  --artifact-type <lower_snake_case_type> \
  --artifact-swift <UpperCamelCaseName>
```

Do not read or regenerate the assets unless diagnosing them. The overlay supplies a versioned envelope, Zod parser, known-type inline card, unsupported fallback, and detail shell. It refuses overwrites and records the capability in the proof manifest.

Immediately replace generic `title`, `summary`, and `highlights` with the smallest real product schema. The uncustomized overlay is not a finished artifact.

## Backend Contract

- Generate the artifact server-side and parse it with Zod before persistence.
- Normalize/enrich real data before it reaches iOS; do not present guessed or placeholder data as ready.
- Persist assistant Markdown and artifact/pointer atomically when practical.
- Use a stable artifact id, type, version, readiness, updated timestamp, and typed payload.
- Store full session-level artifacts under an owner-scoped path; message cards point to that identity.
- Keep submission idempotent by message/request key.
- Unknown or invalid output becomes a typed incomplete/failed state, never raw model JSON.
- Artifact actions cannot bypass domain authorization, confirmation, transactions, or external-action safety.

Markdown explains the result briefly. The artifact is the source of truth for the product surface.

## iOS Contract

Keep transport DTOs, domain models, feature state, and views separate. Add:

- explicit decoder for the known type/version;
- safe unknown-type/version card;
- TCA state for artifact store and presented route;
- typed card-tap action such as `.artifactTapped(id:)`;
- loading, generating, partial/stale, missing, failed, and restored detail states;
- native domain components under the TravelPlanner2-derived product-workspace language.

Inline cards are compact pointers: identity, readiness, two or three useful facts, and one clear action. Do not duplicate the detail view. Background refresh must not navigate automatically or change selection unexpectedly.

## Hard Gates

Do not call the contour complete unless:

- provider credentials remain backend-only;
- user message is persisted before model work;
- assistant Markdown and every UI payload are typed, validated, versioned, and durable;
- important artifact state survives relaunch and session switching;
- unknown versions render safely rather than as JSON;
- the same artifact identity drives inline and detail surfaces;
- taps route through typed state;
- fake/low-confidence data is absent or explicitly incomplete;
- external/destructive actions are allowlisted or confirmed;
- design, clickability, shadow/clipping, and state QA pass.

## Verification

Run backend tests for parse failure, persistence, and idempotency; iOS tests for known/unknown decoding and card routing; reducer tests for send → generating → text+artifact → open; close/reopen restoration; command-line backend and iOS builds; and visual QA for all readiness states.

Report the artifact name/version, source-of-truth path, DTO/storage contract, route, design concept, verified states, and remaining blockers.
