---
name: validate-use-cases
description: >
  Validate a layered architecture against core use cases by producing call chains.
  Use when the user has a proposed architecture (services assigned to layers) and needs to
  prove it supports the required behavior. Trigger on: "validate architecture", "call chain",
  "does this design support", "core use cases", "use case validation", "composable design",
  "prove the architecture", "test the design", or any request to verify that a set of services
  can satisfy a set of use cases. Also trigger when the user asks how a specific use case
  flows through the architecture - that is a call chain request.
---

# Architecture Validation via Call Chains

**Read** `${CLAUDE_PLUGIN_ROOT}/references/composition.md` before validating.
If `cc-docs/architecture.md` exists, read it and apply it as described in `${CLAUDE_PLUGIN_ROOT}/references/project-profile.md`.

You are helping the user prove that their architecture supports every core use case.
Validation is done by producing **call chains** - the sequence of service interactions
that implement each use case.

## Workflow

### Step 1: Identify Core Use Cases
If the user hasn't already identified them:
- A system typically has **2–6** core use cases
- They represent what the system fundamentally *is*, not what it currently *does*
- They are rarely stated explicitly in requirements - they are abstractions
- Ask: "What makes this system different from a spreadsheet?" The answer points to the core use case
- A single-page marketing brochure for the system typically has ≤3 bullet points - those are roughly the core use cases

### Step 2: Produce Call Chains for Each Core Use Case
For each core use case:
1. Identify which services participate
2. Trace the flow: Client → Manager → Engine/ResourceAccess → Resource (with Utilities as needed)
3. Verify at each step:
   - Every call respects closed-architecture rules (down only, permitted relaxations only)
   - The Manager is orchestrating, not the Client
   - Only Managers publish events (Design Don'ts #6-#9). A Client may post a request for one Manager to start a use case (a queued call, not an event). Events that stay inside one Client (UI wiring) are not architectural events.
   - No Design Don't violations

### Step 3: Check for Symmetry
Call chains across different use cases should look structurally similar:
- Same layers involved in similar order
- Similar depth of call nesting
- Asymmetry signals uneven decomposition or missed volatility

### Step 4: Validate Non-Core Use Cases
Once core use cases validate, check the remaining use cases:
- They should be satisfiable with the **same** set of services
- Different use cases = different Manager workflow code, not different services
- If a regular use case cannot be satisfied → a volatility was missed → go back to decomposition

### Step 5: Verify "There Is No Feature"
For each service in the architecture:
- Can you describe it WITHOUT naming a feature? If not → functional decomposition
- Does any single service "own" a feature? If yes → the feature should emerge from integration

### Step 6: Assess Change Containment
For each core use case, simulate a requirement change:
- "What if the customer wants to change X about this use case?"
- The change should be containable within a Manager's workflow
- Engines, ResourceAccess, Resources, Utilities, Clients should NOT need to change
- If the change propagates beyond the Manager → decomposition problem

## Output Format

**Read** `references/output-template.md` and follow the template exactly.

Save the output as **`05-call-chains.md`** in the design directory `cc-docs/design/<topic>/` (see `${CLAUDE_PLUGIN_ROOT}/references/artifact-pipeline.md` for choosing `<topic>`).

**Input files:** `03-layered-architecture.md` (classified services) + `02-volatilities.md` §2 (core use cases) + `01-domain-discovery.md` §6 (workflows, for the §7 workflow-to-service mapping).
If `01-domain-discovery.md` does not exist, map the use cases to services in §7 instead and say so.

**Output file:** `05-call-chains.md` - consumed by Phase 6 (`dmf:workflow-implementation`) and Phase 7 (`wire-services`).

Produce the complete document per the template: call chains per use case with layer compliance tables, symmetry analysis, non-core validation, "There Is No Feature" check, verdict with severity, workflow-to-service mapping, and open questions.

Then a summary verdict:
- ✅ Architecture validates - all core use cases supported
- ⚠️ Partial - use cases X, Y need investigation
- ❌ Invalid - use case X cannot be satisfied, missing volatility: _description_

## Key Principle

> **Never design against the requirements. Design against the core use cases.**
>
> Requirements change. Core use cases almost never do. If your architecture
> supports the core use cases via composable services, requirement changes
> manifest as different Manager workflow code - not architectural change.
