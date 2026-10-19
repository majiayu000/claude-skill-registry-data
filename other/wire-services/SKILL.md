---
name: wire-services
description: >
  Decide how services communicate in a Löwy-style layered architecture: direct synchronous calls,
  queued calls, Pub/Sub events, or a full Message Bus. Use when the user needs to choose
  communication patterns between services, implement the "Message Is the Application" pattern,
  design workflow Managers, or decide whether a Message Bus is justified. Trigger on: "message bus",
  "how should services communicate", "pub/sub", "queued calls", "event-driven", "workflow manager",
  "Message Is the Application", "async vs sync", "service wiring", or any question about how
  Clients reach Managers or how Managers coordinate with each other.
---

# Service Wiring & Message Bus Patterns

**Read** `references/message-bus.md` before advising.
If `cc-docs/architecture.md` exists, read it and apply it as described in `${CLAUDE_PLUGIN_ROOT}/references/project-profile.md`.

You are helping the user decide how services in their Löwy-style architecture communicate
and whether a Message Bus is justified.

## Decision Framework

### Level 1: Direct Synchronous Calls (Simplest)
- Client calls Manager directly (request/response)
- Manager calls Engine and ResourceAccess directly
- **Use when:** Simple system, few subsystems, team can't absorb bus complexity

### Level 2: Queued Client-to-Manager Calls
- Client posts to a queue; Manager picks up when ready
- Provides timeline separation and basic throughput
- **Use when:** Need decoupling but not full bus infrastructure

### Level 3: Full Message Bus
- Queued Pub/Sub Utility accessible to all layers (subject to constraints)
- Enables "Message Is the Application" pattern
- **Use when:** High extensibility required, multiple subsystems, long-running workflows, organizational maturity supports it

### Decision Criteria

| Factor | Direct | Queued | Message Bus |
|---|---|---|---|
| System complexity | Low | Medium | High |
| Team maturity | Any | Moderate | High |
| Extensibility need | Low | Medium | High |
| Multi-subsystem | No | Optional | Yes |
| Long-running workflows | No | Limited | Yes |
| Organizational investment | None | Low | Significant |

**Pragmatic rule:** It's easier to morph architecture than to bend the organization.
Start simpler. Upgrade when capabilities mature.

## Architectural Constraints on the Bus

A Message Bus does NOT eliminate closed-architecture rules. The bus is transport, not license.

**Permitted over the bus:**
- Client → Manager (use case initiation)
- Manager → Manager (queued, deferred triggering)
- Manager → Client (event notification)
- Manager publishing events
- Clients and Managers subscribing to events

**Prohibited over the bus (same as without bus):**
- Client ↔ Client
- Engine ↔ Engine
- ResourceAccess ↔ ResourceAccess
- Clients publishing system state events
- Engines publishing or subscribing to events
- ResourceAccess publishing or subscribing to events

## "Message Is the Application" Pattern

When ALL Client-to-Manager communication goes through a Message Bus:

1. **No direct interaction** - use case initiators and executors don't know about each other
2. **Concurrent participation** - multiple Clients can participate in the same use case
3. **Timeline separation** - Client posts and continues; Manager processes when ready
4. **Change response** - change how services respond to messages, not the architecture
5. **Extensibility** - new behavior = new message-processing services, not modifications

## Workflow Managers

When using a Message Bus, all Managers can be implemented as workflow Managers:

1. Receive message from bus
2. Load workflow type + instance from workflow storage
3. Execute next step
4. Persist workflow instance
5. Post result message to bus

**Benefits:** Long-running workflows, multi-session/multi-device support, feature changes = workflow changes.

## Workflow

### Step 1: Assess the System's Communication Needs
- How many subsystems?
- Are there long-running, multi-session workflows?
- How many Client types?
- Does the organization have infrastructure maturity for a bus?

### Step 2: Recommend a Level
Use the decision criteria table. Be honest about organizational readiness.

### Step 3: Define the Wiring
For each use case, specify:
- Which calls are synchronous (→)
- Which are queued/async (⇢)
- Which are event-based (pub/sub)
- Who publishes, who subscribes
- Each message's kind: a **command** (imperative name, exactly one handling Manager, posted by a Client or a Manager) or an **event** (past-tense name, published only by a Manager, any number of subscribers)

### Step 4: Validate Against Constraints
Check every communication path against the permitted/prohibited lists above.

## Output Format

**Read** `references/output-template.md` and follow the template exactly.

Save the output as **`07-service-wiring.md`** in the design directory `cc-docs/design/<topic>/` (see `${CLAUDE_PLUGIN_ROOT}/references/artifact-pipeline.md` for choosing `<topic>`).

**Input files:** `03-layered-architecture.md` (services + layers) + `05-call-chains.md` (validated call patterns) + `04-domain-model.md` (domain types behind each §6 DTO boundary).
If `04-domain-model.md` does not exist, write `TBD (no 04)` in the Domain Type Source column.

**Output file:** `07-service-wiring.md` - consumed by Phase 8 (`dmf:serialization-persistence`).

Produce the complete document per the template: communication level assessment, wiring table with patterns, event catalog, constraint compliance audit, per-use-case wiring flows, DTO boundary list, and open questions.

Flag any violations of the constraint lists.
