---
name: pattern-extraction
description: Three-tier system for documenting code patterns to optimize token usage
---

# Pattern Extraction Workflow

## Purpose

Optimize token usage and ensure consistency by documenting code patterns once instead of repeatedly exploring codebases.

## Problem

When implementing features in existing codebases, agents typically:
1. Explore the codebase to understand patterns
2. Find example files demonstrating patterns
3. Extract imports, structure, and style
4. Adapt patterns for new features

**Inefficiency**: Repeating exploration wastes tokens and risks inconsistency.

**Solution**: Extract patterns once using a three-tier documentation system, then reference docs instead of re-exploring.

---

## Three-Tier Documentation System

### Tier 1: Architecture Patterns (Conceptual)

**File**: `systems/{system}/architecture-patterns.md`

**Purpose**: Explain **WHY** patterns exist and **WHAT** the rules are.

**Contents**:
- Non-negotiable patterns and mandatory rules
- Architectural reasoning and trade-offs
- When each pattern applies
- Quick reference table of canonical files
- Common import paths

**Example**: VioletDashboard's API Proxy Pattern explains why all backend calls must go through Next.js API routes.

---

### Tier 2: Reference Implementations (Concrete)

**File**: `systems/{system}/reference-implementations.md`

**Purpose**: Point to specific **EXAMPLES** in the actual codebase.

**Contents**:
- File paths with line numbers
- Detailed code excerpts from actual files
- What each reference file demonstrates
- When to use each as a template

**Example**: Points to `pages/api/merchants/[merchantId]/index.ts:16-36` as the canonical PUT handler example.

---

### Tier 3: Code Snippets (Boilerplate)

**File**: `systems/{system}/code-snippets.md`

**Purpose**: Provide **COPY-PASTABLE** starting points.

**Contents**:
- Template code for common patterns
- Boilerplate with placeholders
- Common imports and setup
- Usage examples

**Example**: Full template for a Redux thunk ready to adapt for any CRUD operation.

---

## Implementation Workflow

### When Implementing Features

1. **Read Tier 1 (Architecture Patterns)** first
   - Understand mandatory patterns
   - Identify which pattern applies to your task
   - Review architectural reasoning

2. **Look up Tier 2 (Reference Implementation)**
   - Find the canonical example file path
   - Switch to that repo and read the actual file
   - Observe exact style, imports, error handling

3. **Copy Tier 3 (Code Snippet)**
   - Start with boilerplate template
   - Replace placeholder names/types
   - Adapt logic for your specific use case

4. **Implement**
   - Follow pattern exactly
   - Match import paths, naming conventions, structure
   - Run type checks early

### When to Update Patterns

If documented patterns are outdated or incomplete:

1. **Explore the codebase** to understand current implementation
2. **Update all three tiers**:
   - Update conceptual explanation in Tier 1
   - Update file paths and examples in Tier 2
   - Update boilerplate in Tier 3
3. **Update `last_verified` metadata** in all docs
4. **Document what changed** in commit message

---

## Benefits

| Benefit | Description |
|---------|-------------|
| **Token Efficiency** | Read small pattern docs (~2k tokens) instead of large code files (10k+ tokens) |
| **Consistency** | All implementations follow the same patterns |
| **Onboarding** | New developers/agents learn patterns quickly |
| **Maintainability** | Update patterns in one place |
| **Speed** | No repeated exploration for common tasks |

---

## Applying to New Systems

To document a new system (e.g., VioletConnect, MerchantService):

### Step 1: Create Tier 1 (Architecture Patterns)

```bash
# Create file
touch systems/{system}/architecture-patterns.md
```

Document:
- Mandatory patterns with NON-NEGOTIABLE labels
- Why each pattern exists
- When patterns apply
- Quick reference table

**Template**:
```markdown
---
last_verified: YYYY-MM-DD
verified_against: {System} @ {branch} ({commit})
maintainer: architect
---

# {System} Architecture Patterns

## Pattern 1: {Pattern Name}

### Rule
**{Mandatory requirement}**

### Why
- {Reason 1}
- {Reason 2}

### Implementation
```code example```

## Reference Implementations

| Pattern | Reference File | What It Demonstrates |
|---------|---------------|---------------------|
| ... | ... | ... |
```

### Step 2: Create Tier 2 (Reference Implementations)

```bash
touch systems/{system}/reference-implementations.md
```

Document:
- 5-10 canonical example files
- File paths with key line numbers
- What each file demonstrates
- When to use as template

### Step 3: Create Tier 3 (Code Snippets)

```bash
touch systems/{system}/code-snippets.md
```

Document:
- Copy-pastable templates
- Common imports
- Boilerplate for each pattern
- Usage examples

### Step 4: Link from Brain Repo

In `CLAUDE.md` or system-specific section:
```markdown
### Reference Documentation

- [Architecture Patterns](systems/{system}/architecture-patterns.md)
- [Reference Implementations](systems/{system}/reference-implementations.md)
- [Code Snippets](systems/{system}/code-snippets.md)
```

---

## Example: VioletDashboard

VioletDashboard has all three tiers in `prism-brain`:

**Tier 1**: `systems/violet-dashboard/architecture-patterns.md`
- API Proxy Pattern (mandatory)
- Redux state management (no React Query)
- Form handling (React Hook Form + Yup)
- Feature flags (env vars, build-time)

**Tier 2**: `systems/violet-dashboard/reference-implementations.md`
- `pages/api/merchants/[merchantId]/index.ts` - CRUD API routes
- `redux/thunks/merchant.ts` - Async Redux operations
- `components/Form/MainAppSettings/index.tsx` - Form patterns

**Tier 3**: `systems/violet-dashboard/code-snippets.md`
- API route template (GET/POST/PUT/DELETE)
- Redux thunk template
- Form component template

**Result**: Implementing new features requires ~2k tokens (reading docs) vs 10k+ tokens (exploring code).

---

## When NOT to Use

- **First time with system**: Exploration necessary to create patterns
- **Patterns don't exist**: Create them first
- **Unique one-off code**: Not worth documenting
- **Rapidly changing code**: Wait for stabilization

---

## Metadata Standards

All three tier files should include:

```yaml
---
last_verified: YYYY-MM-DD
verified_against: {System} @ {branch} ({commit or "extracted from live code"})
related_specs:
  - product/specs/{feature}/
maintainer: {role}
---
```

This enables staleness detection and trust signals.

---

## Related Skills

- **v-architect**: Use when designing system architecture
- **v-tech-lead**: Use when reviewing code patterns
- **v-frontend** / **v-backend**: Use when implementing features

---

## Invocation

This skill is informational - read it to understand the three-tier system. Then create/update the three files in your brain repo's `systems/{system}/` directory.
