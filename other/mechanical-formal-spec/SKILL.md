---
name: mechanical-formal-spec
description: Compile an English protocol specification into MFS (Mechanism Flow Specification) — a mechanism-level formal language that describes effects, channels, and their composition as a DAG.
---

# Mechanical Formal Spec

Translates English protocol specifications into MFS (Mechanism Flow Specification). MFS sits between English specs and TLA+/Quint: it describes mechanisms, effects, and their composition as a DAG rather than state machines.

## Input

- **spec_path**: Path to an English protocol specification file
- **output_dir** (optional): Directory for output artifacts. Defaults to a directory alongside the input file.

## Output

- `<name>.mfs`: The mechanism-level formal specification
- `language-spec.md`: Reference copy of the MFS language specification (in the skill directory)

## Language Reference

The MFS language specification is at `skills/mechanical-formal-spec/language-spec.md`. Key constructs:

| Construct | Purpose |
|---|---|
| `scope` | Domain over which a mechanism operates (global, per-market, per-partition) |
| `type` / `@opaque type` | Payload type declarations |
| `effect` | Typed observable output with ordering, attestation, scope |
| `channel` | Transport with pattern, fan-out, ordering, reliability, complexity |
| `mechanism` | Trigger + guard + produces/consumes + dissemination rules |
| `flow` | Explicit DAG edge with channel and redundant paths |
| `guarantee` | Property over effects/flows with assumptions and degradation |
| `recovery` | View change strategy (prefix recovery, cursor catchup, snapshot+replay) |
| `gc` | Archiver garbage collection rules |

## Process

### Step 1: Identify Mechanisms

Read the English spec and extract every mechanism:
- What triggers it (external input, upstream effect, condition)
- What effects it produces (typed outputs with sequence/attestation)
- Who receives those effects and over which transport
- What guarantees it provides

### Step 2: Define Scopes and Types

- Identify the scoping hierarchy (global, per-instance, per-partition)
- Declare effect types with payload unions, metadata, ordering constraints
- Declare domain types (structural or `@opaque`)

### Step 3: Define Channels

For every dissemination path:
- Transport type (overlay_pubsub, overlay_directed, request_response, memory)
- Pattern (fire_and_forget, broadcast_then_filter, pull_on_demand)
- Fan-out (1:1, 1:N, N:N)
- Ordering guarantee (fifo_per_source, causal, total, none)
- Reliability (at_most_once, at_least_once, exactly_once)
- Communication complexity class

### Step 4: Define Mechanisms

Write mechanism declarations with:
- Scope reference
- Trigger list
- Optional guard (effect predicate, not internal state)
- Produces/consumes declarations
- Dissemination rules (target + channel + optional filter)

Ensure DAG acyclicity: if two mechanisms exchange effects bidirectionally, split into separate mechanisms with distinct effect types at each stage.

### Step 5: Define Flows (DAG)

Write explicit flow declarations for every dissemination edge. Include:
- Source and target mechanisms
- Effect type carried
- Channel used
- Redundant paths (backup relays, archiver paths)

### Step 6: Define Guarantees

Express properties over effects and flows:
- Sequential consistency per scope
- Data availability (archiver DA)
- Surgical rollback on view change
- Safety properties (no byzantine archiver, phantom leader rejection)
- Commutativity / ordering properties

Include `assumes` for each guarantee and `degradation` for partial failure.

### Step 7: Define Recovery and GC

- Recovery blocks for each service's view change
- Archiver GC rules (backup ack, checkpoint endorsement)

### Step 8: Logic Review

Run `/logic-review` on the output:
1. Review the `.mfs` file against the English spec for completeness
2. Check internal consistency (mechanism declarations vs flow declarations vs guarantees)
3. Fix confirmed issues

### Step 9: Final Consistency Pass

Read the English spec and MFS translation together. Verify:
- Every English spec mechanism has a corresponding MFS mechanism
- Every effect flow is captured in a flow declaration
- Channel annotations are complete
- No concepts were lost in translation

## Example

Input: `english-spec.md` (Unified DA-Ordering Architecture)
Output: `da-ordering.mfs`

See `context/mechanical-formal-spec/da-ordering.mfs` for a complete example translation.

## Conventions

- File extension: `.mfs`
- Identifiers: `snake_case` for values, `PascalCase` for types
- Qualified names: `Service[param].mechanism`
- 2-space indent, no tabs
- Comments: `-- single line` or `{- multi-line -}`
