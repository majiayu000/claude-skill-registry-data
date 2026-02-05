---
name: Formal Specification Driven Development
description: Use this skill when the user wants to implement code with formal verification. This workflow discusses requirements, creates Idris2 specifications, reviews them, compiles for verification, then implements in the target language (Python, Rust, or TypeScript). Trigger when user mentions "formal spec", "idris2", or requests rigorous code implementation.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
---

# Formal Specification Driven Development

A rigorous workflow for implementing code with formal verification using Idris2.

## Workflow Steps

### Phase 1: Requirements Discussion
1. Engage with the user to understand the problem thoroughly
2. Ask clarifying questions about:
   - Input/output types and constraints
   - Edge cases and error conditions
   - Performance requirements
   - Invariants that must hold
3. Summarize the requirements for user confirmation

### Phase 2: Idris2 Specification
1. Create an Idris2 specification that captures:
   - Type definitions with dependent types where appropriate
   - Function signatures with precise types (with explicit multiplicities if needed)
   - Proofs of key properties (totality, correctness conditions)
   - Example usage and test cases
2. Place specification in `.specs/` directory (create if needed)
3. Use clear naming: `<feature-name>.idr`

### Phase 3: Initial Compilation & Verification
1. **Immediately compile** the Idris2 specification: `idris2 --check <file>.idr`
2. Fix any type errors or proof obligations
3. Ensure the specification is total and type-checks
4. **Iterate automatically until compilation succeeds** (no user involvement needed)
5. If fundamental design issues arise, discuss with user

### Phase 4: Specification Review
1. Present the **compiled and verified** Idris2 specification to the user
2. Explain key design decisions:
   - Why certain types were chosen
   - What properties are being enforced
   - What the proofs guarantee
3. Ask for feedback and iterate if needed (recompile after changes)
4. Use AskUserQuestion for critical design choices
5. Get user approval before proceeding to implementation

### Phase 5: Target Language Implementation
1. Ask user which target language to use (if not specified):
   - Python
   - Rust
   - TypeScript
2. Implement the specification in the target language:
   - Preserve type information using language features (type hints, generics, etc.)
   - Add runtime validation where compile-time guarantees aren't available
   - Include comments referencing the Idris2 spec
   - Maintain the same logical structure
3. Add comprehensive tests based on Idris2 examples
4. Document any gaps between formal spec and implementation

### Phase 6: Final Review
1. Show both the Idris2 spec and implementation side-by-side
2. Highlight how the implementation preserves formal properties
3. Discuss any limitations or assumptions
4. Get user approval before integrating into project

## Best Practices

### For Idris2 Specifications
- Start with simple types, add dependent types only when needed
- Write proofs for critical properties
- Include concrete examples as test cases
- Use `%default total` to ensure all functions terminate
- Document assumptions clearly
- Be explicit with multiplicity annotations when using linear types
- Import necessary modules from `base` (Prelude is minimal in Idris2)
- Use qualified names when disambiguation is needed

### For Target Language Implementation
- **Python**: Use type hints, runtime validation with `assert`, dataclasses
- **Rust**: Leverage type system, use `Result`/`Option`, implement traits
- **TypeScript**: Use strict mode, generics, branded types for validation

### Communication
- Always explain trade-offs clearly
- Don't proceed to next phase without user approval
- If Idris2 compilation fails, discuss the issue before fixing
- Make the formal specification human-readable, not just machine-checkable

## Example Interaction

```
User: "I need a function to merge sorted lists"

Assistant Phase 1: Let me understand the requirements:
- Should this preserve duplicates?
- What should happen with empty lists?
- Do we need to prove the result is sorted?
[... discussion ...]

Assistant Phase 2: I'll create an Idris2 specification.
[Creates .specs/merge-sorted.idr with dependent types]

Assistant Phase 3: Compiling and verifying the specification...
[Runs idris2 --check, fixes errors, ensures totality]
[Iterates until successful compilation]

Assistant Phase 4: Here's the verified specification. Notice how the type
guarantees the output is sorted. Do you approve?
[... review ...]

Assistant Phase 5: Which language should I implement this in?
[User chooses Rust]
[Implements with proper types and tests]

Assistant Phase 6: Here's the final implementation. The Rust version
uses the type system to maintain similar guarantees...
```

## Directory Structure

This skill expects/creates:
```
project-root/
├── .specs/              # Idris2 specifications
│   └── feature.idr
├── src/                 # Target language implementations
│   └── feature.{py,rs,ts}
└── tests/               # Tests derived from specs
    └── test_feature.*
```

## Idris2-Specific Guidelines

### Key Differences from Idris 1

**Quantitative Type Theory (QTT):**
- Variables have multiplicities: `0` (erased), `1` (linear), or unrestricted
- Implicit arguments may be erased at runtime (use `0` prefix)
- Linear resources require explicit `1` multiplicity annotation

**Smaller Prelude:**
- Always import needed modules explicitly: `Data.List`, `Data.Nat`, `Data.Vect`, etc.
- Functions previously auto-available now require imports

**Syntax Changes:**
- Use `%default total` instead of individual `total` keywords
- `let` bindings are now lambda-equivalent (use local functions for recursive definitions)
- Named application syntax: `f {arg = value}`
- New dot notation for record access: `record.field`

**Type System:**
- Less aggressive disambiguation - use qualified names more often
- Missing interface implementations now cause compile errors
- Pattern matching on erased variables (`0` multiplicity) is restricted

**Common Patterns:**
```idris
-- Explicit imports (required in Idris2)
import Data.Vect
import Data.Fin

-- Default totality (recommended)
%default total

-- Linear resource (1 multiplicity)
useOnce : (1 x : Resource) -> IO ()

-- Erased proof (0 multiplicity)
compute : (0 prf : IsValid x) -> (x : Nat) -> Nat
```

## Notes

- Idris2 must be installed and available in PATH
- The `.specs/` directory serves as formal documentation
- Link implementation files to their specs in comments
- Use git to track both specs and implementations together
- This workflow is most valuable for critical algorithms and data structures
- When migrating Idris 1 code, watch for implicit erasure and import requirements