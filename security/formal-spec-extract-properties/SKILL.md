---
name: formal-spec-extract-properties
description: Extract properties from a formal spec (TLA+/Lean/ProVerif) into AutoSpec's structured format. Classifies each property with id, statement, essence, and type. Works on formal-spec output or any existing formal spec.
---

# Property Extraction

Takes a formal spec and produces a structured properties file for AutoSpec consumption.

## Input

- Path to a formal spec (TLA+, Lean, or ProVerif)
- Optional: the mapping table from formal-spec (if this follows a formal-spec run)
- Optional: the English spec or code reference that the formal spec was derived from

## Process

### Step 1: Parse properties

Extract all verifiable properties from the spec:

- **TLA+**: everything declared as `INVARIANT`, `PROPERTY`, `THEOREM`, or used in a `SPECIFICATION` block. Also standalone predicates that look like invariants (e.g. `TypeOK`, `Agreement == \A r1, r2 ...`).
- **Lean**: all `theorem` and `lemma` declarations.
- **ProVerif**: all `query` declarations (secrecy, correspondence, reachability).

For each property, extract:
- `id`: assign P1, P2, ... in order of appearance
- `statement`: the formal name (e.g. "Agreement", "TypeOK", "secrecy_key")
- `formal_definition`: the actual formal expression (the TLA+ predicate body, the Lean type, the ProVerif query)

### Step 2: Classify type

For each property, determine its type:

| Type | Criteria |
|---|---|
| safety | "bad thing never happens". invariants, state predicates, \A quantified over states |
| liveness | "good thing eventually happens". temporal operators (eventually, leads-to), fairness |
| security | secrecy, authentication, non-forgery, non-equivocation. ProVerif queries, or TLA+ properties about signatures/keys/attestation |

If ambiguous, default to safety and flag for user review.

### Step 3: Write essence

For each property, write a plain-language `essence`: what the property protects, stated as an intent, not a restatement of the formal definition.

Good essence: "no two replicas ever decide on different values"
Bad essence: "for all r1, r2 in Replicas, decided[r1] != None and decided[r2] != None implies decided[r1] = decided[r2]"

The essence is what must survive even if the formal statement changes during AutoSpec optimization.

If a mapping table is provided (from formal-spec), use the English requirement as the basis for the essence. If an English spec is provided, trace each property back to its English requirement.

If neither is available, derive the essence from the formal definition. Flag these as "essence derived from formal definition, user should verify".

### Step 4: User review

Present the extracted properties to the user in a table:

```
| id | statement | type | essence |
|----|-----------|------|---------|
| P1 | Agreement | safety | no two replicas ever decide on different values |
| P2 | ... | ... | ... |
```

Ask the user:
- Are any essences wrong or incomplete?
- Are any properties missing that should be tracked?
- Are any properties listed that should NOT be preserved (e.g. TypeOK is often just a sanity check, not a meaningful property)?
- Should any properties be merged (e.g. two properties that protect the same underlying guarantee)?

Apply corrections before writing the output.

## Output

Write to `<spec_name>_props.json`:

```json
[
  {
    "id": "P1",
    "statement": "Agreement",
    "essence": "no two replicas ever decide on different values",
    "type": "safety",
    "formal_definition": "\\A r1, r2 \\in Replicas : ...",
    "source": "english_spec | mapping_table | derived",
    "user_verified": true
  }
]
```

Also print the autospec invocation command:

```
autospec <spec_path> --properties <spec_name>_props.json --trust-model <trust_model_path>
```

## Invocation

- `formal-spec-extract-properties <spec_path>`
- `formal-spec-extract-properties <spec_path> --mapping <mapping_table_path>`
- `formal-spec-extract-properties <spec_path> --english <english_spec_path>`
