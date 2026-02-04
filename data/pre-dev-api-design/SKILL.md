---
name: ring:pre-dev-api-design
description: |
  Gate 4: API contracts document - defines component interfaces and data contracts
  before protocol/technology selection. Large Track only.

trigger: |
  - TRD passed Gate 3 validation
  - System has multiple components that need to integrate
  - Building APIs (internal or external)
  - Large Track workflow (2+ day features)

skip_when: |
  - Small Track workflow → skip to Task Breakdown
  - Single component system → skip to Data Model
  - TRD not validated → complete Gate 3 first

sequence:
  after: [ring:pre-dev-trd-creation]
  before: [ring:pre-dev-data-model]
---

# API/Contract Design - Defining Component Interfaces

## Foundational Principle

**Component contracts and interfaces must be defined before technology/protocol selection.**

Jumping to implementation without contract definition creates:
- Integration failures discovered during development
- Inconsistent data structures across components
- Teams blocked waiting for interface clarity
- Rework when assumptions about contracts differ

**The API Design answers**: WHAT data/operations components expose and consume?
**The API Design never answers**: HOW those are implemented (protocols, serialization, specific tech).

## Phase 0: API Standards Discovery (MANDATORY)

**Before defining contracts, check for organizational naming standards.**

See [shared-patterns/standards-discovery.md](../shared-patterns/standards-discovery.md) for complete workflow.

**Context:** API field naming standards
**Output:** `docs/pre-dev/{feature-name}/api-standards-ref.md`

Use AskUserQuestion tool:

**Question:** "Do you have a data dictionary or API field naming standards to reference?"
- Header: "API Standards"
- multiSelect: false
- Options:
  - "No - Use industry best practices" (description: "Generate contracts using standard naming conventions")
  - "Yes - URL to document" (description: "Provide a URL to your data dictionary or standards document")
  - "Yes - File path" (description: "Provide a local file path (.md, .json, .yaml, .csv)")

### If "Yes" Selected:

**1. Load the document:**

| Source Type | Tool | Actions |
|------------|------|---------|
| URL | WebFetch | Fetch document content; parse for field definitions, naming rules, validation patterns |
| File path | Read | Read file content; support .md (Markdown tables), .json (structured), .yaml (structured), .csv (tabular) |

**2. Extract standards:**

MUST extract these elements if present:

| Element | What to Extract | Example |
|---------|----------------|---------|
| **Field naming convention** | camelCase, snake_case, PascalCase | `userId` vs `user_id` |
| **Standard field names** | Common fields used across APIs | `createdAt`, `updatedAt`, `isActive` |
| **Data type formats** | How to represent dates, IDs, amounts | ISO8601, UUID v4, Decimal(10,2) |
| **Validation patterns** | Regex, constraints, rules | Email RFC 5322, phone E.164 |
| **Standard error codes** | Organizational error naming | `EMAIL_ALREADY_EXISTS` vs `DuplicateEmail` |
| **Pagination fields** | Standard query/response pagination | `page`, `pageSize`, `totalCount` |

**3. Save extracted standards:**

Output to: `docs/pre-dev/{feature-name}/api-standards-ref.md`

Format:
```markdown
# API Standards Reference - {Feature Name}

Source: {URL or file path}
Extracted: {timestamp}

## Field Naming Conventions
- IDs: `{pattern}` (example)
- Timestamps: `{pattern}` (example)
- Booleans: `{pattern}` (example)
- Collections: `{pattern}` (example)

## Standard Fields
| Field | Type | Format | Validation | Example |
|-------|------|--------|------------|---------|
| userId | string | UUID v4 | Required, unique | "550e8400-e29b-41d4-a716-446655440000" |
| email | string | RFC 5322 | Required, unique | "user@example.com" |
| createdAt | string | ISO 8601 | Auto-generated | "2026-01-23T10:30:00Z" |

## Standard Error Codes
| Code | Usage | HTTP Equivalent (for reference) |
|------|-------|--------------------------------|
| EMAIL_ALREADY_EXISTS | Duplicate email registration | 409 Conflict |
| INVALID_INPUT | Validation failure | 400 Bad Request |

## Validation Patterns
| Pattern Type | Rule | Example |
|-------------|------|---------|
| Email | RFC 5322, max 254 chars | "user@example.com" |
| Phone | E.164 format | "+5511987654321" |

## Pagination Standards
| Field | Type | Description |
|-------|------|-------------|
| page | integer | 1-indexed page number |
| pageSize | integer | Items per page (max 100) |
| totalCount | integer | Total items across all pages |
```

**4. Apply throughout Gate 4:**

- **Use standard field names** in operation definitions
- **Reference validation patterns** in contract constraints
- **Apply naming conventions** consistently
- **Note any justified deviations** with rationale

### If Dictionary Conflicts with Existing Codebase:

If Phase 0 from Gate 0 (Research) found existing patterns that conflict with the dictionary:

**STOP and use AskUserQuestion:**

**Question:** "Dictionary says `{dictionary_pattern}`, but codebase uses `{codebase_pattern}`. Which should we follow?"
- Header: "Standards Conflict"
- multiSelect: false
- Options:
  - "Follow dictionary" (description: "Use organizational standards, refactor existing code later")
  - "Follow codebase" (description: "Maintain consistency with existing implementation")
  - "Hybrid approach" (description: "Let me decide per-field")

### If "No" Selected (Industry Best Practices):

Proceed with standard naming conventions:
- camelCase for field names (JavaScript/TypeScript)
- snake_case for field names (Python/Ruby/SQL)
- ISO 8601 for timestamps
- UUID v4 for identifiers
- RFC 5322 for emails

**Document the choice** in `api-standards-ref.md` with rationale.

## Mandatory Workflow

| Phase | Activities |
|-------|------------|
| **0. API Standards Discovery** | Check for organizational field naming standards (data dictionary); load from URL or file if provided; extract field conventions, types, validation patterns; save to `api-standards-ref.md` for reference throughout gate |
| **1. Contract Analysis** | Load approved TRD (Gate 3), Feature Map (Gate 2), PRD (Gate 1); identify integration points from TRD component diagram; extract data flows |
| **2. Contract Definition** | Per interface: define operations, specify inputs/outputs, define errors, document events, set constraints (validation, rate limits), version contracts; **apply standards from Phase 0 if available** |
| **3. Gate 4 Validation** | Verify all checkboxes in validation checklist before proceeding to Data Modeling |

## Explicit Rules

### ✅ DO Include
Operation names/descriptions, input parameters (name, type, required/optional, constraints), output structure (fields, types, nullable), error codes/descriptions, event types/payloads, validation rules, rate limits/quotas, idempotency requirements, auth/authz needs (abstract), versioning strategy

### ❌ NEVER Include
HTTP verbs (GET/POST/PUT), gRPC/GraphQL/WebSocket details, URL paths/routes, serialization formats (JSON/Protobuf), framework code, database queries, infrastructure, specific auth libraries

### Abstraction Rules

| Element | Abstract (✅) | Protocol-Specific (❌) |
|---------|--------------|----------------------|
| Operation | "CreateUser" | "POST /api/v1/users" |
| Data Type | "EmailAddress (validated)" | "string with regex" |
| Error | "UserAlreadyExists" | "HTTP 409 Conflict" |
| Auth | "Requires authenticated user" | "JWT Bearer token" |
| Format | "ISO8601 timestamp" | "time.RFC3339" |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "No need to ask about data dictionary" | Organizations have standards. Check first, don't assume. Phase 0 is MANDATORY. |
| "I'll just use common sense for field names" | "Common sense" varies. Ask for standards, or explicitly choose best practices. |
| "Skip Phase 0, user will mention standards if important" | User doesn't know when to mention it. YOU must ask proactively. |
| "REST is obvious, just document endpoints" | Protocol choice goes in Dependency Map. Define contracts abstractly. |
| "We need HTTP codes for errors" | Error semantics matter; HTTP codes are protocol. Abstract the errors. |
| "Teams need to see JSON examples" | JSON is serialization. Define structure; format comes later. |
| "The contract IS the OpenAPI spec" | OpenAPI is protocol-specific. Design contracts first, generate specs later. |
| "gRPC/GraphQL affects the contract" | Protocols deliver contracts. Design protocol-agnostic contracts first. |
| "We already know it's REST" | Knowing doesn't mean documenting prematurely. Stay abstract. |
| "Framework validates inputs" | Validation logic is universal. Document rules; implementation comes later. |
| "This feels redundant with TRD" | TRD = components exist. API = how they talk. Different concerns. |
| "URL structure matters for APIs" | URLs are HTTP-specific. Focus on operations and data. |
| "But API Design means REST API" | API = interface. Could be REST, gRPC, events, or in-process. Stay abstract. |

## Red Flags - STOP

If you catch yourself writing any of these in API Design, **STOP**:

- HTTP methods (GET, POST, PUT, DELETE, PATCH)
- URL paths (/api/v1/users, /users/{id})
- Protocol names (REST, GraphQL, gRPC, WebSocket)
- Status codes (200, 404, 500)
- Serialization formats (JSON, XML, Protobuf)
- Authentication tokens (JWT, OAuth2 tokens, API keys)
- Framework code (Express routes, gRPC service definitions)
- Transport mechanisms (HTTP/2, TCP, UDP)

**When you catch yourself**: Replace protocol detail with abstract contract. "POST /users" → "CreateUser operation"

## Gate 4 Validation Checklist

| Category | Requirements |
|----------|--------------|
| **Contract Completeness** | All component-to-component interactions have contracts; all external integrations covered; all event/message contracts defined; client-facing APIs specified |
| **Operation Clarity** | Each operation has clear purpose/description; consistent naming convention; idempotency documented; batch operations identified |
| **Data Specification** | All inputs typed and documented; required vs optional explicit; outputs complete; null/empty cases handled |
| **Error Handling** | All scenarios identified; error codes/types defined; actionable messages; retry/recovery documented |
| **Event Contracts** | All events named/described; payloads specified; ordering/delivery semantics documented; versioning defined |
| **Constraints & Policies** | Validation rules explicit; rate limits defined; timeouts specified; backward compatibility exists |
| **Technology Agnostic** | No protocol specifics; no serialization formats; no framework names; implementable in any protocol |

**Gate Result:** ✅ PASS (all checked) → Data Modeling | ⚠️ CONDITIONAL (remove protocol details) | ❌ FAIL (incomplete)

## Contract Template Structure

Output to `docs/pre-dev/{feature-name}/api-design.md` with these sections:

| Section | Content |
|---------|---------|
| **Overview** | TRD/Feature Map/PRD references, status, last updated |
| **Versioning Strategy** | Approach (semantic/date-based), backward compatibility policy, deprecation process |
| **Component Contracts** | Per component: purpose, integration points (inbound/outbound), operations |

### Per-Operation Structure

| Field | Content |
|-------|---------|
| **Purpose** | What the operation does |
| **Inputs** | Table: Parameter, Type, Required, Constraints, Description |
| **Validation Rules** | Format patterns, business rules |
| **Outputs (Success)** | Table: Field, Type, Nullable, Description + abstract structure |
| **Errors** | Table: Error Code, Condition, Description, Retry? |
| **Idempotency** | Behavior on duplicate calls |
| **Authorization** | Required permissions (abstract) |
| **Related Operations** | Events triggered, downstream calls |

### Event Contract Structure

| Field | Content |
|-------|---------|
| **Purpose/When Emitted** | Trigger conditions |
| **Payload** | Table: Field, Type, Nullable, Description |
| **Consumers** | Services that consume this event |
| **Delivery Semantics** | At-least-once, at-most-once, exactly-once |
| **Ordering/Retention** | Ordering guarantees, retention period |

### Additional Sections

| Section | Content |
|---------|---------|
| **Cross-Component Integration** | Per integration: purpose, operations used, data flow diagram (abstract), error handling |
| **External System Contracts** | Operations exposed to us, operations we expose, per-operation details |
| **Custom Type Definitions** | Per type: base type, format, constraints, example |
| **Naming Conventions** | Operations (verb+noun), parameters (camelCase), events (past tense), errors (noun+condition) |
| **Rate Limiting & Quotas** | Per-operation limits table, quota policies, exceeded limit behavior |
| **Backward Compatibility** | Breaking vs non-breaking changes, deprecation timeline |
| **Testing Contracts** | Contract testing strategy, example test scenarios |
| **Gate 4 Validation** | Date, validator, checklist, approval status |

## Common Violations

| Violation | Wrong | Correct |
|-----------|-------|---------|
| **Protocol Details** | "Endpoint: POST /api/v1/users, Status: 201 Created, 409 Conflict" | "Operation: CreateUser, Errors: EmailAlreadyExists, InvalidInput" |
| **Implementation Code** | JavaScript regex validation code | "email must match RFC 5322 format, max 254 chars" |
| **Technology Types** | JSON example with "uuid", "Date", "Map<String,Any>" | Table with abstract types: Identifier (UUID format), Timestamp (ISO8601), ProfileObject |

## Confidence Scoring

| Factor | Points | Criteria |
|--------|--------|----------|
| Contract Completeness | 0-30 | All ops: 30, Most: 20, Gaps: 10 |
| Interface Clarity | 0-25 | Clear/unambiguous: 25, Some interpretation: 15, Vague: 5 |
| Integration Complexity | 0-25 | Simple point-to-point: 25, Moderate deps: 15, Complex orchestration: 5 |
| Error Handling | 0-20 | All scenarios: 20, Common cases: 12, Minimal: 5 |

**Action:** 80+ autonomous generation | 50-79 present options | <50 ask clarifying questions

## After Approval

1. ✅ Lock contracts - interfaces are now implementation reference
2. 🎯 Use contracts as input for Data Modeling (`ring:pre-dev-data-model`)
3. 🚫 Never add protocol specifics retroactively
4. 📋 Keep technology-agnostic until Dependency Map

## The Bottom Line

**If you wrote API contracts with HTTP endpoints or gRPC services, remove them.**

Contracts are protocol-agnostic. Period. No REST. No GraphQL. No HTTP codes.

Protocol choices go in Dependency Map. That's a later phase. Wait for it.

**Define the contract. Stay abstract. Choose protocol later.**
