---
name: list-volatilities
description: >
  Interactive volatility-based system decomposition following Löwy's Method. Use when the user
  needs to decompose a system into services, identify areas of volatility, build a volatilities
  list, analyze requirements for hidden solutions, or distinguish volatile from variable concerns.
  Trigger on: "decompose", "volatilities", "what could change", "axes of volatility",
  "requirements analysis", "solutions masquerading as requirements", "volatile vs variable",
  or any request to break a system into services. Also trigger when the user presents a set of
  requirements and asks what services to create - this is the entry point for that question.
  WARNING: if the user's proposed decomposition maps services to features or domain entities,
  this skill must flag it as functional/domain decomposition and redirect.
---

# Volatility-Based Decomposition

**Read** `references/decomposition.md` before guiding the user.

You are guiding an interactive decomposition session. The goal is to produce a
**volatilities list** - a structured inventory of what could change in this system -
and then map those volatilities to candidate services.

## Workflow

### Step 1: Gather Context
Ask the user for:
- A one-sentence description of the system
- Available requirements, use cases, or domain knowledge
- Known constraints (tech stack, team size, existing systems)

### Step 2: Identify Core Use Cases
Before decomposing, identify the 2–6 core use cases (see `${CLAUDE_PLUGIN_ROOT}/references/composition.md` §2 if composition reference is needed).
These are the essence of the business, not CRUD operations.

### Step 3: Apply the Axes of Volatility
For each area of the system, ask:
- **Axis 1 (same customer over time):** Will this change for the same customer? What will they want differently next year?
- **Axis 2 (different customers at the same time):** Do different customers need this to work differently right now?

### Step 4: Scrub for Solutions Masquerading as Requirements
For each stated requirement:
1. Ask: "Are there other possible solutions to this need?"
2. If yes → it's a solution, not a requirement
3. Generalize to find the underlying volatility
4. Common signals: "send email" → notification volatility, "store in DB" → storage volatility

### Step 5: Apply the Volatile vs Variable Filter
- **Volatile:** Open-ended variation requiring architectural encapsulation. Changes would ripple across the system.
- **Variable:** Handled with if/else, config, or parameterization. No architectural boundary needed.

### Step 6: Compile the Volatilities List
For each identified volatility, document:

| Volatility | Axis | Evidence | Encapsulation boundary |
|---|---|---|---|
| _name_ | 1, 2, or both | _why it's volatile_ | _candidate service scope_ |

### Step 7: Map to Candidate Services
- Start with obvious 1:1 mappings
- Some volatilities will merge into a single service
- Some will map to operational concepts (queuing, events) rather than services
- Use abstract names: "Storage" not "Database", "Notification" not "EmailService"
- Target order of magnitude ~10 services total

### Step 8: Validate the Mapping
Check the candidate list against these red flags:
- [ ] Any service named after a feature or domain entity? → Functional/domain decomposition
- [ ] Any service that only makes sense in the context of one specific use case? → Functional decomposition
- [ ] Can you describe each service's purpose without referencing a specific requirement? → If not, it's coupled to requirements
- [ ] Does each service encapsulate something that could genuinely change independently?

## Output Format

**Read** `references/output-template.md` and follow the template exactly.

Save the output as **`02-volatilities.md`** in the design directory `cc-docs/design/<topic>/` (see `${CLAUDE_PLUGIN_ROOT}/references/artifact-pipeline.md` for choosing `<topic>`).

**Input file:** `01-domain-discovery.md` (if available - use it for domain context, bounded contexts, and workflow inventory). If not available, gather equivalent context from the user.

**Output file:** `02-volatilities.md` - consumed by Phase 3 (`classify-structure`) and Phase 5 (`validate-use-cases`).

Produce the complete document per the template: core use cases, axes of volatility table, solutions-vs-requirements scrub, candidate services list, decomposition validation checklist, and open questions.

## Key Warnings
- If the user proposes services mapped to features ("BillingService", "ReportingService"), stop and explain why this is functional decomposition. Reference §1 of decomposition.md.
- If the user proposes services mapped to domain entities ("CustomerService", "OrderService"), stop and explain why this is domain decomposition. Reference §2 of decomposition.md.
- Expect organizational resistance. Stakeholders present requirements functionally. The user may need help translating functional language into volatility language.
