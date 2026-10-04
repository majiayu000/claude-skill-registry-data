---
name: agent-foundry-product-evolution
description: Build an AgentFoundry Product Evolution Agent pipeline that analyzes conversation memory, proposes native product/interface improvements, stores product-change proposals for approval, creates Codex-ready implementation tasks, opens PRs after approval, and prepares TestFlight/App Store release candidates. Use when the user wants product evolution from conversations, chat-derived native UI improvements, or a system that turns repeated user needs into reviewed app updates. This is not server-driven UI.
---

# AgentFoundry Product Evolution

## Purpose

Use this skill to build the Product Evolution Agent: a backend-owned product-development loop that turns user conversations into native product improvements.

The core path is:

```text
User chats
→ conversation memory
→ Product Evolution Agent
→ product-change proposal
→ human approval
→ Codex implementation task
→ branch / PR
→ CI / QA
→ TestFlight / App Store release candidate
```

The goal is not runtime-generated UI. The goal is a disciplined product pipeline where chat reveals needs, an agent proposes native app changes, and Codex implements those changes through normal engineering and release review.

## Required References

Load references only when needed:

- Read `references/product-change-proposal.md` before designing proposal schemas, writing proposal examples, or generating Codex-ready implementation tasks.

## Mandatory Design Companion For iOS UI

When this skill proposes, scopes, approves, or generates a Codex task for any AgentFoundry SwiftUI/iOS user-facing interface, read the peer file `../agent-foundry-design/SKILL.md` and require its target baseline, design system, Liquid Glass rules, clickability, keyboard dismissal, shadow/clipping QA, and visual verification gate.

If `agent-foundry-design` cannot be loaded, do not produce a UI implementation task as ready. Mark the task blocked on the missing design companion.

## Product Stance

- Chats are the primary source of intent, confusion, repeated workflows, and missing product surfaces.
- Conversation memory is the durable input layer. Do not insert a separate product-signal layer unless the user explicitly asks for analytics/aggregation.
- Product change proposals are first-class backend objects, not loose chat summaries.
- New interfaces are native product work: SwiftUI/TCA screens, backend schemas, tests, PRs, and release notes.
- When a proposal or Codex task targets an AgentFoundry iOS interface, require `agent-foundry-design` for the target baseline, design system, Liquid Glass rules, clickability checks, and shadow/clipping QA.
- The Product Evolution Agent may propose and prioritize changes, but it must not silently edit production code, open PRs, deploy, or submit releases without explicit human approval.
- Do not implement this as server-driven UI, downloaded executable code, or runtime UI generation that bypasses App Store review.
- Do not create one-off private app binaries per user unless the user explicitly chooses an enterprise/internal distribution path. Default to product improvements that can be reviewed, tested, and released through normal channels.

## Hard Gates

Do not claim the Product Evolution loop is complete unless all are true:

- Conversation data boundaries are explicit: which chats/conversation memories may be analyzed, what is redacted, and what is excluded.
- User-private content is not pasted into GitHub issues, PRs, release notes, logs, or prompts beyond the minimum approved evidence.
- Conversation memory exists or is specified as the durable source of chats/messages.
- A durable product-change proposal store exists or is specified.
- Proposals include evidence, impact, scope, risks, acceptance criteria, and affected native surfaces.
- Human approval is required before creating a Codex implementation branch or PR.
- The generated Codex task is implementable without raw private chat transcripts.
- PR/release output includes tests, QA notes, and rollback considerations.
- App Store/TestFlight release steps are treated as reviewed release workflow, not automatic overnight code execution.

If any gate fails, stop with the smallest next product/engineering action needed to continue.

## Command Ownership

Run every inspection, schema edit, test, and local implementation command yourself when tools allow it.

User-only actions are limited to:

- Approving analysis of specific conversation data.
- Approving product-change proposals.
- Approving use of private evidence in redacted form.
- Approving repository, GitHub, TestFlight, App Store, or deployment actions that require account consent or credentials.
- Merging PRs, submitting App Store releases, or granting the agent permission to do those release actions.

Agent-owned actions include:

- Inspecting the existing app/backend architecture.
- Designing conversation memory access and proposal schemas.
- Implementing backend Product Evolution Agent jobs/endpoints.
- Implementing proposal review UI for operators or users.
- Generating Codex-ready tasks after approval.
- Creating branches/PRs when explicitly approved and tools are available.
- Running tests, build checks, and writing release candidate notes.

## Workflow

### 1. Establish The Evolution Scope

Ask only for facts that change the pipeline:

- Which product/repo/app should evolve.
- Which chat sources may be analyzed.
- Whether the first loop is personal-single-user, internal operator-reviewed, or multi-user aggregate.
- Where proposals should be reviewed: in-app admin screen, GitHub issue, Linear, Notion, or a local report.
- Whether Codex should create PRs automatically after approval or only produce implementation tasks.

Default to a safe first slice:

- Single product.
- Owner-approved analysis.
- Redacted evidence.
- Proposal review in a backend/admin surface or markdown report.
- Codex task generation after approval.
- No automatic merge or App Store submit.

### 2. Use Conversation Memory

Use the app's existing durable chat/message storage as Product Evolution input. If it does not exist, create or specify a conversation memory layer.

Recommended shape:

```text
users/{uid}/chats/{chatId}
  title
  purpose
  createdAt
  updatedAt

users/{uid}/chats/{chatId}/messages/{messageId}
  role
  messageMarkdown
  createdAt

users/{uid}/conversationMemory/{memoryId}
  chatId
  messageIds
  summary
  durableFacts[]
  openQuestions[]
  userGoals[]
  possibleInterfaceNeeds[]
  createdAt
```

The Product Evolution Agent can read selected chats directly, or read conversation memory summaries when raw chat access is not approved.

Examples of interface needs the agent may infer:

- Case/status tracker.
- Program comparison workspace.
- Product pitch workspace.
- Document checklist.
- Deadline tracker.
- Research collection.
- Native workflow for a repeated task.

Raw chats may stay in conversation memory. Proposals, Codex tasks, GitHub issues, PR descriptions, and release notes should use summaries/redacted evidence unless the user explicitly approves sharing specific excerpts.

### 3. Build The Product Evolution Agent

The Product Evolution Agent should run on the backend as a scheduled job, operator-triggered job, or explicit analysis endpoint.

Inputs:

- Selected recent chats and/or conversation memory summaries.
- Existing product surfaces and routes.
- Existing backend schemas and feature flags.
- Prior proposals and release history.
- Release constraints and App Store/TestFlight status when available.

Outputs:

- New or updated product-change proposals.
- Rationale for rejecting weak/noisy product-change ideas.

The agent should prefer repeated high-friction patterns over one-off requests. It should distinguish:

- A missing answer the chat agent should handle.
- A missing artifact/state model.
- A missing native interface.
- A missing backend capability.
- A release/process problem.

### 4. Create Product-Change Proposals

Use `references/product-change-proposal.md` for the concrete proposal shape.

At minimum, every proposal must include:

- Title.
- Problem.
- Evidence, redacted by default.
- Proposed native surfaces.
- Backend/domain changes.
- User value.
- Scope.
- Non-goals.
- Risks.
- Privacy review.
- Acceptance criteria.
- Test plan.
- Rollout/release notes.
- Codex implementation task draft.

Do not let a proposal skip approval just because confidence is high.

### 5. Approval And Codex Task Generation

After approval, generate a Codex-ready task that can be implemented without raw private transcripts.

The task should state:

- Repo/app/module targets.
- Native screens/components to add, including the `agent-foundry-design` target and visual QA requirements when the task touches AgentFoundry SwiftUI UI.
- Backend schemas/endpoints/jobs to add.
- Migration/backfill needs.
- Tests and smoke checks.
- Release note draft.
- Explicit files or areas to avoid touching.

If the user approves implementation in the current repo, create the branch/changes yourself when possible. If GitHub tooling is available and the user asked for a PR, open the PR after tests pass.

### 6. Release Path

Treat release as a normal reviewed product release:

- PR with implementation and tests.
- CI/build verification.
- QA notes and screenshots when relevant.
- TestFlight release candidate when available.
- App Store submission only when explicitly requested/approved.

Never describe overnight delivery as automatic App Store mutation. Say it as a release pipeline: approved changes can be built, reviewed, and shipped so the user later receives a native update.

## First MVP

For an AgentFoundry iOS/Firebase/OpenAI app, the smallest useful Product Evolution slice is:

- Firestore conversation memory source or adapter over existing chats.
- Firestore product-change proposal model.
- Backend Product Evolution Agent function that analyzes selected chats/conversation memory into proposals.
- Proposal approval status: `draft | proposed | approved | rejected | implemented | released`.
- A local/admin proposal report or native operator view.
- Codex task generation from approved proposals.

Do not start by building many native feature types. First prove the loop with one proposal, one approval, and one Codex-ready task.

## Stop Rules

Stop instead of improvising when:

- Conversation analysis scope is not approved.
- Raw private chats would need to be copied into public or third-party surfaces.
- The user asks for runtime-generated native code or App Store bypass.
- No approval gate exists before code generation/PR creation.
- The proposed product change cannot be implemented as a reviewable native app/backend update.
- The implementation would require rewriting unrelated product architecture.
