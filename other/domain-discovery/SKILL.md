---
name: domain-discovery
description: >
  Discover and document a domain following "Domain Modeling Made Functional" methodology.
  Produces a structured domain document from requirements, conversations, or descriptions.
  Use this skill whenever the task involves understanding a new domain, capturing requirements,
  defining bounded contexts, identifying domain events and commands, documenting workflows,
  or creating a domain glossary. Trigger on: "discover domain", "domain discovery", "event storming",
  "bounded context", "context map", "domain events", "ubiquitous language", "document the domain",
  "capture requirements", "model this business process", "what are the workflows", "domain document",
  "domain overview". Also trigger when a user describes a business problem or system they want to
  build and needs the domain decomposed before modeling types or writing code. This skill should
  run BEFORE dmf:domain-modeling - it produces the structured input that modeling consumes.
---

# Domain Discovery (DMF Methodology)

This skill takes raw domain input - descriptions, conversations, requirements, existing docs -
and produces a structured domain document. The output feeds directly into the
`dmf:domain-modeling` skill for type-level modeling.

## Core Philosophy

1. **Events first, not data structures** - Discover what *happens* before what data *exists*.
2. **Listen, don't impose** - No database schemas, no class hierarchies, no technical patterns.
   Capture the domain as the domain expert describes it.
3. **Partition into bounded contexts** - Follow team/department boundaries as strong hints.
4. **Expand to the edges** - Trace events upstream and downstream as far as possible.
5. **Capture the Ubiquitous Language** - Every term must come from the domain, not from tech jargon.
6. **Document unknowns explicitly** - Questions and gaps are first-class outputs, not failures.

## Discovery Process

Follow these steps in order. Each step produces a section of the output document.

### Step 1: Identify Domain Events

Extract every business event mentioned or implied. Events are facts - things that happened.

**Rules for events:**
- Always past tense: "Order placed", "Payment received", "Shipment dispatched"
- Never technical: NOT "Database updated", "Message queued", "API called"
- Include trigger events (what starts a process) AND outcome events (what a process produces)
- Include time-based triggers: "Month-end close", "Daily reconciliation run"
- Include observation-based triggers: "Inventory below threshold"

**Expand to the edges:**
- For every leftmost event, ask: "What caused this? What happened before?"
- For every rightmost event, ask: "What does this trigger? Who needs to know?"
- Keep going until you reach external actors or system boundaries.

### Step 2: Identify Commands

For each event, ask: "What request caused this event?"

**Rules for commands:**
- Always imperative: "Place order", "Ship package", "Send invoice"
- Commands can fail - the event only happens if the command succeeds
- Not all events come from commands - some are time-based or observation-based

**Pattern:**
```
Command: "Place order"
  → triggers workflow: Place Order
  → on success, emits: "Order placed" event
  → on failure, emits: "Order validation failed" event (or goes to error pile)
```

### Step 3: Identify Bounded Contexts

Group related events and commands by the team, department, or area of expertise
that owns them.

**Heuristics for context boundaries:**
- Different vocabulary → different context (even if same word, e.g., "order" means
  different things to shipping vs. billing)
- Different domain experts → different context
- Different team or department → strong hint of separate context
- Ability to operate autonomously → should be its own context
- Different rate of change → separate so they can evolve independently

**Context boundary rules:**
- Each context has a clear, single responsibility
- Contexts communicate via events, never by sharing internal data
- "Good fences make good neighbors" - when in doubt, split

**Classify contexts:**
- **Core domain** - competitive advantage, where the money is made
- **Supportive domain** - necessary but not differentiating
- **Generic domain** - commodity, could be outsourced or use off-the-shelf

### Step 4: Map Context Relationships

For each pair of interacting contexts, determine the relationship:

| Relationship | Who controls the contract? | When to use |
|---|---|---|
| **Shared Kernel** | Both teams jointly | Tightly coupled teams that must agree on shared types |
| **Customer/Supplier** | Downstream (consumer) defines needs | Downstream has specific requirements |
| **Conformist** | Upstream dictates | Using external/legacy system as-is |
| **ACL (Anti-Corruption Layer)** | Neither - translator in between | External system's model doesn't match yours at all |

### Step 5: Document Workflows

For each workflow within the target bounded context, capture:

```
Workflow: "<Name>"
  Triggered by: <event or command>
  Primary input: <data structure, using AND/OR notation>
  Other inputs: <dependencies from other contexts or services>
  Output events: <list of events emitted on success>
  Side effects: <things that happen but aren't events - emails, notifications, etc.>
  Error outputs: <what happens on failure>
```

Then break into substeps:

```
Substep: "<Name>"
  Input: <type from previous step>
  Output: <type for next step> OR <error type>
  Dependencies: <external services or data needed>
  Logic: <pseudocode description of business rules>
```

### Step 6: Document Data Structures

Use AND/OR notation - no technical types, no database schemas.

```
data Order =
    CustomerInfo
    AND ShippingAddress
    AND BillingAddress
    AND list of OrderLine
    AND AmountToBill

data OrderLine =
    ProductCode
    AND Quantity
    AND Price

data ProductCode = WidgetCode OR GizmoCode
data WidgetCode = string starting with "W" then 4 digits
data GizmoCode = string starting with "G" then 3 digits
```

**Lifecycle stages:** If an entity goes through distinct stages (as most do), define
separate types per stage. This is critical and almost always applies.

```
data UnvalidatedOrder =
    UnvalidatedCustomerInfo
    AND UnvalidatedShippingAddress
    AND list of UnvalidatedOrderLine

data ValidatedOrder =
    ValidatedCustomerInfo
    AND ValidatedShippingAddress
    AND list of ValidatedOrderLine

data PricedOrder =
    ValidatedCustomerInfo
    AND ValidatedShippingAddress
    AND list of PricedOrderLine
    AND AmountToBill        // new at this stage
```

**Rules:**
- Capture constraints: "integer between 1 and 1000", "string max 50 chars"
- Mark unknowns explicitly: `data BillingAddress = ??? // details TBD`
- Use domain expert terminology for every name
- If the domain expert wouldn't recognize a name, it's wrong

### Step 7: Build the Ubiquitous Language Glossary

Every distinct term used in the domain document gets an entry:

```
| Term | Meaning | Context |
|------|---------|---------|
| Order | A confirmed request to purchase and ship products | Order-Taking |
| Quote | A request for pricing only, no shipment | Order-Taking |
| Order | Items to be picked, packed, and dispatched | Shipping |
| Placed Order | An order that has been validated and priced | Order-Taking |
```

Note: the same word CAN appear multiple times with different meanings in different contexts.
This is expected and important to document - it's why bounded contexts exist.

### Step 8: Capture Non-Functional Requirements

For each workflow, document:
- **Scale**: How many per day/hour? Seasonal spikes?
- **Latency**: How fast must it respond?
- **User expertise**: Beginners or power users?
- **Reliability**: What's the cost of failure?
- **Audit**: Does every action need a trail?

### Step 9: Capture Open Questions

Every uncertainty, disagreement, or unknown gets documented as a question.
Questions are valuable output - they prevent premature implementation.

```
## Open Questions
- [ ] What are the upper bounds for KilogramQuantity? (Ask Ollie)
- [ ] Does the billing context need the full line items or just the total?
- [ ] How should the system handle duplicate order submissions?
- [ ] Is "Express Delivery" a separate workflow or a flag on the order?
```

## Output Document Template

The skill produces a single markdown document with this structure.
Read `references/output-template.md` for the full template.

Save the output as **`01-domain-discovery.md`** in the design directory `cc-docs/design/<topic>/` (see `${CLAUDE_PLUGIN_ROOT}/references/design-directory.md` for choosing `<topic>`).

**Input:** Raw requirements, interviews, business descriptions.

**Output file:** `01-domain-discovery.md` - consumed by Phase 4 (`dmf:domain-modeling`), Phase 6 (`dmf:workflow-implementation`) and Phase 8 (`dmf:serialization-persistence`); with the `lowy` plugin, also Phases 2, 3 and 5 (`lowy:list-volatilities`, `lowy:classify-structure`, `lowy:validate-use-cases`).

## Anti-Patterns to Avoid

**Database-driven thinking:**
- WRONG: "We need an Order table with a foreign key to Customer"
- RIGHT: "An Order contains CustomerInfo AND ShippingAddress AND ..."

**Class-driven thinking:**
- WRONG: "We need an OrderBase class with Order and Quote subclasses"
- RIGHT: "An incoming form is an Order OR a Quote"

**Technical leakage:**
- WRONG: "The OrderPlaced event is published to a Kafka topic"
- RIGHT: "The OrderPlaced event is sent to the shipping and billing contexts"

**Premature implementation:**
- WRONG: "The validation step calls the REST API at /api/address/validate"
- RIGHT: "The validation step uses an address checking service (external dependency)"

**Ignoring lifecycle stages:**
- WRONG: One "Order" type with nullable Price and IsValidated flags
- RIGHT: UnvalidatedOrder → ValidatedOrder → PricedOrder (distinct types per stage)

## When to Stop Discovery

Discovery is done when:
- [ ] All bounded contexts are identified and classified (core/supportive/generic)
- [ ] Context relationships are mapped
- [ ] Every workflow in the target context has inputs, outputs, substeps, and dependencies
- [ ] Data structures use AND/OR notation with constraints
- [ ] Lifecycle stages of key entities are captured as separate types
- [ ] Ubiquitous Language glossary exists
- [ ] Open questions are documented (not resolved - just documented)
- [ ] Non-functional requirements are captured

The output document is now ready to be consumed by `dmf:domain-modeling` for
type-level modeling.
