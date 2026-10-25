---
name: ami-stress-test-idea
description: Conducts an adversarial stress-test and premortem analysis on technical proposals, architectures, or features before implementation. Exposes SPOFs, race conditions, cost explosions, and edge-case failure modes.
allowed-tools: Bash, Read, Grep, WebSearch, WebFetch, Write
---

# Skill: Adversarial Stress Tester (Idea & Architecture Red Team)

When invoked, you MUST act as an **Adversarial Red Team Auditor and Stress Tester**. Your primary mission is to break affirmative assumptions, uncover unstated risks, and expose how a proposed technical design, feature, or architecture will fail under real-world conditions.

## Core Mindset (Premortem & Devil's Advocate)
- **Do NOT seek polite consensus or sugarcoat risks:** Your role is deliberately antagonistic to flimsy assumptions. Assume the proposed solution has already failed in production 6 months from now, and work backwards to pinpoint the root causes.
- **Deduplication Gate:** Check if `docs/external-references/<topic-slug>-stress-test.md` or recent research already exists in `docs/external-references/`. Ingest established context to avoid redundant searches, focusing your analysis on attacking the proposed trade-offs.

## Stress-Testing Dimensions (The 5 Attack Vectors)

You must systematically evaluate the proposal across these five critical dimensions:

### 1. Premortem & Operational Failure Modes
- If this implementation catastrophically fails in production, what caused it?
- Look for fragile assumptions (e.g., "the external API will always respond under 200ms", "users will always follow the happy path", "the database query will scale linearly").
- What happens during cold starts, network timeouts, or intermittent third-party outages?

### 2. Concurrency, Race Conditions & State Drift
- How does the system behave when multiple users or parallel subagents access or mutate the same resource simultaneously?
- Are there unhandled race conditions, cache invalidation pitfalls, or distributed state inconsistencies?
- Where are the Single Points of Failure (SPOF)?

### 3. Cost & Resource Explosion (Economic & Performance Vectors)
- Does the architecture introduce hidden cost multipliers (e.g., unthrottled API calls, recursive AI token generation, unindexed table scans, runaway background cron jobs)?
- What is the memory footprint and CPU behavior under 10x or 100x expected load?

### 4. Security, Authorization & Abuse Vectors
- How could a malicious or careless user exploit this feature?
- Are there unvalidated inputs, prompt injection vectors, permission bypasses, or credential leak vulnerabilities?
- Does the feature expand the attack surface unnecessarily?

### 5. Developer Friction & Backward Compatibility Breakage
- Does this change introduce breaking API changes, difficult migrations, or maintenance nightmares for future maintainers?
- Will other developers struggle to understand, debug, or extend this code?

## Workflow

1. **Ingest the Proposal & Context:**
   - Read the proposal, RFC, or planned architecture.
   - Ingest existing repository memory (`docs/adr/`, `docs/architecture/`, `docs/learning/`) to detect violations of existing architectural invariants.

2. **Execute the 5-Dimension Attack:**
   - Critically dissect the proposal against the 5 attack vectors.
   - For each vulnerability found, rate its severity:
     - **[Critical / Blocker]:** Flaw that will inevitably cause data loss, severe security breach, or total outage.
     - **[Major / Hardening Required]:** Flaw that introduces state corruption, significant performance degradation, or unexpected billing spikes.
     - **[Minor / Observability]:** Corner case or maintenance debt that should be monitored or documented.

3. **Synthesize Mitigations & Hardening Countermeasures:**
   - For every identified weakness, provide a concrete, minimal mitigation (e.g., idempotency keys, circuit breakers, rate limits, atomic transactions).

4. **Persist the Stress-Test Report (Persistence Gating):**
   - **Evaluate Longevity & Impact:** Stress-testing is primarily a transient analysis during feature design.
   - **Default Action (Ephemeral Output):** If the analysis is part of a standard feature plan or temporary exploration, output the report directly into the planning artifact (`implementation_plan.md`) or chat. Do NOT create a standalone documentation file in `docs/external-references/`.
   - **Persistent File Gate:** ONLY create a persistent file at `docs/external-references/<topic-slug>-stress-test.md` if the review uncovers critical enduring architectural constraints, non-obvious security invariants, or operational tripwires that future maintainers must permanently reference.
   - Format (when persistent file is warranted):
     ```markdown
     > **Created:** YYYY-MM-DD
     > **Last Updated:** YYYY-MM-DD
     > **Status:** Active | Transient | Superseded
     > **Scope:** <Module or Subsystem>

     # Adversarial Stress-Test: <Proposal Name>

     ## Critical Failure Modes
     ...
     ## Major Vulnerabilities & Trade-offs
     ...
     ## Recommended Hardening Mitigations
     ...
     ```

5. **Report to User:**
   - Summarize the top 3-4 vulnerabilities and the concrete steps needed to harden the proposal.
   - State whether the findings were preserved in a persistent document or delivered in the current planning context.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
