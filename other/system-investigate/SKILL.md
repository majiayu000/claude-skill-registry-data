---
name: system-investigate
description: Investigate an underdefined product, codebase, architecture, integration, or operational question through read-only repository tracing, bounded runtime evidence, and current public research. Use when the user wants to validate suspected behavior, explain why it occurs, compare plausible designs for existing behavior, or recommend the smallest safe change before planning or implementation; not for designing a new system or feature, which belongs to system-design.
---

# System Investigation

Own one investigation from the user's question to an evidence-backed verdict and practical next step. Treat the prompt as a hypothesis, repository and runtime evidence as authority, and implementation as out of scope.

## Establish the investigation

1. Extract the question, suspected behavior, affected system, decision it informs, and requested terminal result.
2. Stop and route to `system-design` when the question asks how to build behavior that does not exist yet, such as a greenfield system or a new capability. Investigate only behavior the repository, runtime, or public sources can show.
3. Write one explicit investigation goal and stopping condition. Use a persisted goal when the host supports it; mark it complete only after the evidence answers the question or proves a precise blocker.
4. State the working hypothesis without treating it as fact. Record plausible alternatives that would materially change the conclusion.
5. Keep the investigation read-only: do not edit code or durable configuration, commit, push, open or modify pull requests, install dependencies, or mutate live systems. Route a later request to act on the recommendation through the applicable planning or implementation workflow.
6. Read all applicable repository instructions before repository-specific work.

## Maintain autonomous progress

1. Continue without routine confirmation. Resolve discoverable facts before asking the user.
2. Check safe sources in this order as applicable:
   - repository instructions, source, tests, documentation, configuration, and relevant history;
   - installed command help, local versions, APIs, connectors, and authorized browser sessions;
   - exact or bounded runtime and remote state;
   - official documentation, specifications, upstream source, and release notes for current public facts.
3. Never send private issue, repository, runtime, or customer data to public search. Search only the public technical terms needed to answer the question.
4. Choose the smallest reversible recommendation when several approaches satisfy the evidence. Record assumptions and proceed.
5. Ask one concise question only when the unresolved answer changes required behavior or scope, authoritative sources conflict, necessary access is unavailable, or every safe path requires a high-risk or irreversible action.
6. Keep the decision to ask with the owning agent. A subagent may report missing evidence but must not interrupt the user.
7. Report inconclusive evidence as inconclusive. Silence and missing tooling are not proof.

## Coordinate independent investigation

1. Use one agent by default. Add a subagent only when its evidence track is independent and parallel work materially improves time or context isolation.
2. Give each subagent one dedicated investigation goal, the minimum raw context it needs, explicit read-only scope, stopping condition, and expected evidence. Use a lower-cost host-supported model and low or moderate effort for bounded retrieval, scanning, and summarization. Keep ambiguous reasoning, source conflicts, and final synthesis with the owning agent. Have each subagent create a persisted goal when the host supports one. Use the `yarstack:reviewer` agent for investigation and research subagents when the host provides it. Delegation does not expand user authority.
3. When current public context could materially change the conclusion, assign a separate research agent only when the research is necessary and independent; otherwise keep it with the owning agent. Have a research agent add, remove, and refine search terms as it learns and cover only the technology, library, tool, protocol, or platform facts that the question depends on. Unless the question is about them, do not research analogous products, competitors, or general best practices; they import requirements the user did not state. Prefer primary and official sources.
4. Keep the owning agent responsible for the hypothesis, scope, user questions, source conflicts, and final synthesis.
5. Verify subagent claims against cited repository, runtime, or public evidence. Agent agreement is not proof.
6. Integrate all required results and stop subagent work before finalizing.

## Trace the current system

1. Find the owning module and closest existing behavior before surveying adjacent code.
2. Trace the complete affected path from its user, API, event, command, or scheduler entry point through validation, domain decisions, persistence, external calls, and observable outcome.
3. Identify the source of truth, invariants, state transitions, retries, cancellation, cleanup, ordering, concurrency, compatibility boundaries, and failure reporting that can affect the question.
4. Read the focused tests, configuration, documentation, and history that define or contradict the current contract.
5. Use exact refs, identifiers, and server-side filters for remote evidence. Never answer by scanning an unbounded history or collection.
6. Separate observed implementation, documented intent, live behavior, historical rationale, and inference.
7. Stop discovery when the current behavior, relevant constraints, verification surface, and remaining unknowns are clear. Do not inventory unrelated modules, generated output, dependencies, or build artifacts.

## Test the hypothesis

1. State what evidence would confirm, refute, or leave the hypothesis unresolved.
2. Challenge the leading explanation with the strongest plausible alternative.
3. Run focused repository-native, read-only checks or tests when they can distinguish the alternatives. Do not execute untrusted code or mutate production state.
4. Use `technical-spike` when one external or version-specific fact requires deeper bounded research. Use `architecture-refine` only when a user decision, rather than discoverable evidence, must define the desired architecture.
5. Treat tests of current behavior as baseline evidence, not proof that a proposed behavior is correct. Require a behavioral test or realistic evaluation for the proposed contract.
6. Record source limitations, stale evidence, and facts that could change with versions or deployment state.

## Recommend the smallest safe next step

1. Give a direct verdict: confirmed, refuted, partially supported, or inconclusive.
2. Explain why the current behavior does or does not satisfy the intended contract.
3. Choose the smallest reversible design supported by the evidence. Define:
   - the exact behavior to change;
   - the minimal owning files or units;
   - the data and control flow, including errors and cleanup;
   - the tests and runtime evidence needed;
   - the behavior that must remain unchanged.
4. Identify contract migration, mixed-version behavior, rollout, rollback, security, resource, and operational requirements only when they materially apply.
5. Separate prerequisite work, intentional deferrals, and unrelated cleanup from the recommendation.
6. Do not implement the recommendation, expand it into a system or feature design, or turn it into a full implementation plan. Use `system-design` for a new design and `plan-create` when the user separately requests an implementation-ready plan.

## Report the result

Lead with the verdict and affected system. Then report the current behavior, decisive evidence, recommended behavior, smallest safe change surface, quality and operational risks, checks performed, intentionally deferred cleanup, remaining uncertainty, and next workflow if needed. Link local files at useful lines and cite public sources near the claims they support.

Finish when the investigation goal has a supported answer and practical next step, or when further progress requires new authority or unavailable evidence. Do not claim completion while required evidence tracks or subagents remain unfinished.
