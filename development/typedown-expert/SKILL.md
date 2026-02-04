---
name: typedown-expert
description: Expert guidance on writing correct Typedown code, focusing on syntax, best practices, and common pitfalls.
---

# Typedown Expert

This skill provides expert knowledge for writing **Typedown** files (`.td`). Typedown is a Consensus Modeling Language that embeds Pydantic models and Pytest logic into Markdown.

## Core Syntax Rules

1. **File Structure**:

   - Typedown files are valid Markdown files.
   - They consist of natural language text interleaved with special Code Blocks.
   - **Crucial**: Every `.td` file MUST start with a Level 1 Heading (`# Title`) and a brief textual description. Never start with a code block.

2. **Model Blocks (`model:<Name>`)**:

   - Used to define Pydantic models.
   - **One Model Per Block**: Do NOT define multiple classes in a single block. Each class gets its own `model:ClassName` block.
   - **No Imports in Block**: Do NOT import `typing` or `pydantic` inside the block unless it's a specific, non-standard import. The environment pre-loads standard types.
   - **Class Name Match**: The class defined MUST match the block argument (e.g., `class User` inside ` ```model:User `).

3. **Config Blocks (`config`)**:

   - Used for global configuration and exports.
   - **Location**: Strictly restricted to `config.td` files only. Do NOT use `config` blocks in regular `.td` files.
   - **Exposure**: All symbols defined in `config` are automatically exposed to the directory scope and inherited by subdirectories.

4. **Entity Blocks & Identifiers**:

- Every Entity MUST have a unique identity.
- **Syntax**: `entity <Type>: <Identifier>`
- **The Identifier**:
  - The string after the colon is the **System ID (L1)**.
  - **Styles**: Can be a simple name (`alice`), a slug (`user-alice-v1`) or a UUID (`550e84...`).
- **Content**: Valid YAML matching the Pydantic model.
  - **Reference Rule**: When referencing other entities within an entity block, you **MUST** use the `[[Identifier]]` (Wiki Link) syntax.

5. **References (`[[...]]`)**:

- Typedown resolves references using a **Three-Layer String Matching** strategy (L0 → L2).
- **Matching Priority**:
  1. **L0 (Cryptographic Truth)**: `[[sha256:...]]`
     - Matches content hash exactly. Immutable and absolute.
  2. **L1 (Exact System ID)**: `[[<ID>]]`
     - Matches the defined System ID exactly (e.g., `[[user-alice-v1]]` or `[[alice]]`).
     - **Recommendation**: Always use **Slug Style** for stable, long-term L1 references.
  3. **L2 (Contextual Handle)**: `[[<Handle>]]`
     - Matches the System ID via **Fuzzy Lookup** in the current scope.
     - Example: `[[alice]]` might resolve to `user-alice-v1` if configured in `config.td`.

6. **Evolution Semantics (`former`)**:

When tracking object changes over time:

- **Syntax**: `former: [[<Identifier>]]`
- **Rule**: You **MUST** use the reference syntax `[[]]` for the `former` field.
- **Rule**: Prefer using **Global Identifiers (L1)** or **Hashes (L0)** for `former` pointers to ensure historical stability. Do NOT use fleeting Local Handles (L2) for history.

7. **Spec Blocks (`spec`)**:

- Used for validation logic.
- Contains Python functions decorating with `@target`.

## The Typedown Mindset: Consensus Modeling

Typedown is not just a syntax; it is a rigorous method for converting loose natural language into strict systemic consensus. When using Typedown, follow this 5-step cognitive process:

### 1. Entity Discovery (Identification)

Scan the unstructured text or requirement to identify Key Entities. Immediately instantiate them using `entity` blocks to fix their existence.

- **Action**: Create `entity:<Type>` blocks with YAML content.
- **Goal**: Turn "User Alice" into data.

### 2. Schema Abstraction (Structure)

Analyze the `entity` blocks you just created. Abstract their common structure into Pydantic models (`model`).

- **Action**: Define `model:<Type>` blocks.
- **Context**: Place shared models in a parent `config.td` or `common.td` and `export` them if they are used across multiple files.

### 3. Constraint Engineering (Logic)

Analyze the business rules governing these entities. Enforce them using three layers of defense:

- **Layer 1 (Field Types)**: Use strict types (e.g., `EmailStr`, `PositiveInt`).
- **Layer 2 (Validators)**: Use Pydantic `@field_validator` or `@model_validator` for self-contained consistency.
- **Layer 3 (Specs)**: Use `spec` blocks with `@target` tags for cross-entity or graph-level validation (e.g., "A specific user must exist in the admin group").

### 4. Reference & Learning (Research)

If you are unsure about advanced syntax (e.g., how to use `former` for versioning or `tags` for filtering):

- **Action**: Create a `_reference` directory (it is git-ignored).
- **Action**: Clone the official repo: `git clone https://github.com/IndenScale/typedown.git _reference/typedown`.
- **Action**: Read `docs/` or `examples/` in the reference to ground your knowledge.

### 5. Verification (Feedback)

Never assume your code is correct. Always verify with the compiler.

- **Action**: Run `uvx typedown check <path>` immediately after editing.
- **Action**: Treat warnings as errors.

## Example: The Modeling Loop

- Step 1: Raw Draft
  "We need a server 'Alpha' compliant with ISO-27001."

- Step 2: Typedown Modeling

```model:ComplianceStandard
class ComplianceStandard(str, Enum):
    ISO_27001 = "ISO-27001"
    SOC2 = "SOC2"
```

```model:Server
class Server(BaseModel):
    hostname: str
    compliance: List[ComplianceStandard]

    @model_validator(mode='after')
    def check_security(self):
        if ComplianceStandard.ISO_27001 in self.compliance:
            # Enforce some logic...
            pass
        return self
```

```entity Server: alpha-01
hostname: "alpha-01"
compliance:
  - "ISO-27001"
```
