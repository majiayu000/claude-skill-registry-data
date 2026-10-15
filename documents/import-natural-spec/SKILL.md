---
name: import-natural-spec
description: >
  Import a natural language specification document (Markdown) and interactively convert it
  to a VDM-SL formal specification. Reads the MD file, identifies requirements, flags ambiguities,
  and guides the user through a dialogue to fill gaps — producing a complete .vdmsl file.
  Use this skill whenever the user wants to: convert a requirements document to VDM-SL,
  import a spec from Markdown, formalize a natural language specification, turn a requirements doc
  into a formal spec, or create VDM-SL from an existing document.
  Japanese triggers: 「自然言語仕様をインポートしたい」「要件定義からVDMを作りたい」
  「MDファイルからVDM仕様を生成して」「要件書を形式仕様に変換して」
  「仕様書をVDM-SLにしたい」「ドキュメントからエージェント契約を作りたい」
metadata:
  version: "1.0.0"
---

# Importing Natural Language Specifications into VDM-SL

Read a Markdown requirements document and convert it to a VDM-SL formal specification
through interactive dialogue. The key challenge is that natural language is inherently
ambiguous — this skill systematically identifies and resolves those ambiguities
rather than silently guessing.

MD形式の自然言語仕様をVDM-SL形式仕様に変換する。自然言語の曖昧さを対話的に解消しながら、
漏れのない形式仕様を構築する。

## Why This Skill Exists

The `define-contract` skill builds VDM-SL from scratch through Q&A.
The `extract-spec` skill extracts VDM-SL from existing source code.

This skill fills the gap between them: the user already has a written specification
(requirements document, design doc, API spec, etc.) but it's in natural language,
not code. Rather than starting from zero or from code, we start from the document
and systematically formalize it.

## Dialogue Flow

### Step 1: Read and Parse the Document

Ask the user for the MD file path (or accept it from the conversation context).

Read the file and identify its structure:

- **Headings** → potential module/agent boundaries
- **Bullet lists** → requirements, constraints, rules
- **Numbered lists** → sequential operations, workflows
- **Tables** → data models, field definitions
- **Code blocks** → existing type definitions, API schemas, examples
- **Bold/italic text** → emphasis on important constraints

Produce a structural summary for the user:

```
📄 Document Analysis: requirements.md

Found:
  Sections:        5 (potential modules/agents)
  Requirements:    23 bullet points
  Data models:     2 tables
  Constraints:     7 explicitly stated
  Examples:        3 code blocks

Identified agents/modules:
  1. "User Management" (lines 5-45)
  2. "Order Processing" (lines 47-120)
  3. "Payment Gateway" (lines 122-180)
```

Present this to the user and confirm the scope before proceeding.

### Step 2: Requirement Classification

For each requirement found in the document, classify it:

| Category | VDM-SL Mapping | Example from document |
|----------|---------------|-----------------------|
| Data definition | `types` | "A user has name, email, and role" |
| Constraint | `inv` | "Email must be unique" |
| Operation | `operations` / `functions` | "The system shall allow users to register" |
| Pre-condition | `pre` | "Only active users can place orders" |
| Post-condition | `post` | "After payment, order status becomes confirmed" |
| State | `state` | "The system maintains a list of all orders" |
| Business rule | Combination of `inv` + `pre` + `post` | "Users cannot order more than their credit limit" |

Some requirements will map cleanly. Others won't — and that's where the real value is.

### Step 3: Ambiguity Detection

This is the critical step. Natural language hides ambiguity in many forms.
Scan every requirement for these patterns:

**Vague quantifiers** — "several", "many", "a few", "some"
→ Ask: What's the exact number or range?

**Undefined terms** — Domain-specific words without definition
→ Ask: What exactly does "active user" mean? What states can a user be in?

**Implicit constraints** — Requirements that assume things not stated
→ Ask: "Users can place orders" — can they place orders for other users?
→ Ask: Is there a limit on concurrent orders?

**Missing error cases** — Happy path described but not the sad path
→ Ask: What happens when payment fails? When the item is out of stock?

**Ambiguous relationships** — "associated with", "related to", "linked"
→ Ask: Is this 1:1, 1:N, or N:N? Who owns the relationship?

**Temporal ambiguity** — "before", "after", "during", "when"
→ Ask: Is this a strict ordering? What about concurrent actions?

**Boundary conditions** — "up to", "at least", "maximum"
→ Ask: Is the boundary inclusive or exclusive? What happens at the boundary?

For each ambiguity, create a tagged question:

```
[AMBIGUOUS] Line 34: "Users can have multiple addresses"
  Question: Is there a maximum number of addresses per user?
  Options:
    a) No limit (seq of Address)
    b) Maximum N (seq of Address, inv addrs == len addrs <= N)
    c) At least one required (seq1 of Address)
  Current assumption: No limit (option a)
```

### Step 4: Interactive Resolution

Present the ambiguities to the user in priority order:

1. **Blocking** — Cannot generate any VDM-SL without this answer
   (e.g., what are the states in a state machine?)
2. **Important** — Affects pre/post-conditions or invariants
   (e.g., is this constraint inclusive or exclusive?)
3. **Clarifying** — Would make the spec more precise
   (e.g., is there an upper limit on this list?)

Use AskUserQuestion for efficient resolution. Group related questions when possible
to reduce dialogue rounds. Present options where you can infer them, but always
include a "something else" option.

After each batch of answers, summarize what was decided:

```
✅ Decisions recorded:
  - Address limit: No maximum, but at least one required (seq1 of Address)
  - User states: <ACTIVE> | <SUSPENDED> | <DELETED>
  - Order cancellation: Only allowed in <PENDING> state
```

It's fine to cycle through multiple rounds. Complex documents may need 3-5 rounds
of clarification before the VDM-SL is complete.

### Step 5: VDM-SL Generation

Generate the VDM-SL specification from the resolved requirements.
Follow the same type mapping rules as `define-contract` (Step 2 of that skill).

**Structure the output clearly:**

```vdmsl
module AgentName
-- Generated from: requirements.md
-- Source sections: "User Management" (lines 5-45)
-- Resolved ambiguities: 4 (see generation log)

definitions

types
  -- [REQ-001] "A user has name, email, and role"
  User :: name   : seq1 of char
          email  : Email
          role   : Role
  inv u == len u.name <= 100;

  -- [REQ-002] "Users can be active, suspended, or deleted"
  Role = <ADMIN> | <USER> | <VIEWER>

state UserSystem of
  users : map UserId to User
  -- [REQ-003] "Email must be unique across all users"
  inv mk_UserSystem(users) ==
    forall u1, u2 in set rng users &
      u1 <> u2 => u1.email <> u2.email
end

operations
  -- [REQ-004] "The system shall allow users to register"
  RegisterUser(name: seq1 of char, email: Email, role: Role) res: UserId
    pre email not in set {u.email | u in set rng users}
    post res in set dom users~ and users(res).email = email;
```

Each VDM-SL element should trace back to its source requirement with a `[REQ-nnn]` tag
and the original natural language text as a comment. This traceability is essential —
it lets the user verify that nothing was lost or invented in the translation.

### Step 6: Gap Analysis

After generating the initial VDM-SL, perform a gap analysis:

**Forward check** — Does every requirement in the MD have a corresponding VDM-SL element?
List any requirements that couldn't be formalized (e.g., UI requirements, performance NFRs).

**Backward check** — Does the VDM-SL contain anything not traceable to a requirement?
If so, it was inferred — flag it for user confirmation.

**Completeness check** — Are there operations without pre-conditions?
Types without invariants? State without initialization?

Present the gap analysis to the user:

```
📊 Gap Analysis:

Requirements covered:     19/23 (82.6%)
Requirements not covered:  4
  - REQ-010: "The UI should be responsive" (non-functional, cannot formalize)
  - REQ-015: "Performance should be acceptable" (vague, needs quantification)
  - REQ-018: "Integration with external payment API" (external dependency)
  - REQ-022: "Logging and monitoring" (infrastructure concern)

Inferred elements:         2
  - inv on OrderState: assumed orders cannot return to PENDING once CONFIRMED
  - pre on CancelOrder: assumed only order owner can cancel

Missing elements:          1
  - No initialization operation defined for UserSystem state
```

### Step 7: Finalize and Connect

Save the generated VDM-SL file and inform the user about next steps:

1. **Verify** — Use `verify-spec` to run syntax/type checks and generate proof obligations
2. **Refine** — Use `refine-spec` if further dialogue is needed on specific parts
3. **Generate** — Use `generate-code` to produce TypeScript/Python implementation
4. **Full pipeline** — Use `integrated-workflow` to run verify → prove → generate → test

Also generate a brief **traceability matrix** (as a comment block or separate MD file)
mapping each requirement ID to its VDM-SL element.

## Important Notes

- Never silently resolve ambiguity. Every interpretation choice must be presented to the user.
  The whole point of formalization is making the implicit explicit.
- Preserve the user's domain terminology. If the document says "patron" instead of "user",
  use Patron in the VDM-SL type names. The spec should feel familiar to domain experts.
- Non-functional requirements (performance, scalability, UI) cannot be formalized in VDM-SL.
  Acknowledge them, list them as out-of-scope, and move on — don't try to force them into types.
- Large documents (50+ requirements) benefit from incremental generation:
  produce one module at a time, confirm with the user, then proceed to the next.
- If the document contains contradictory requirements, flag them immediately.
  Contradictions in natural language specs are common and valuable to catch early.
- For VDM-SL syntax guidance, refer to the `formal-methods-guide` skill.
