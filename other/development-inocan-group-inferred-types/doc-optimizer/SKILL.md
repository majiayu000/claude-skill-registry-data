---
name: doc-optimizer
description:
  Optimize documentation for conciseness and clarity by strengthening vague instructions and removing redundancy.
  Use when asked to optimize, condense, or clarify documentation files, Claude Skill, Claude Command, etc.
---

# Documentation Optimizer Skill

Optimize documentation by eliminating vagueness and redundancy while preserving clarity and meaning.

## Quick Start

When optimizing a document:

1. **Evaluate each instruction**: Is it clear without examples?
2. **Strengthen vague instructions**: Add explicit criteria and measurable steps
3. **Remove redundant content**: Eliminate unnecessary examples and explanations
4. **Preserve execution-critical content**: Keep commands, formats, success criteria

## Core Optimization Goals (Priority Order)

1. **Eliminate vagueness** - Strengthen instructions with explicit criteria and measurable steps
2. **Increase conciseness** - Remove redundancy while preserving necessary information
3. **Preserve clarity AND meaning** - Never sacrifice understanding for brevity

**Critical Constraint**: Only update instructions if the new version retains BOTH the same meaning AND clarity. If optimization reduces clarity or changes meaning, reject the change.

## The Execution Test (Primary Decision Framework)

Before removing ANY content, ask these questions in order:

1. **Can Claude execute the instruction CORRECTLY without this content?**
   - If NO → KEEP (execution-critical)
   - If YES → Proceed to question 2

2. **Does this content explain WHY (rationale/educational)?**
   - If YES → REMOVE (not needed for execution)
   - If NO → KEEP (operational detail)

3. **Does this content show WHAT "correct" looks like (success criteria)?**
   - If YES → KEEP (execution-critical)
   - If NO → Proceed to question 4

4. **Does this content extract a general decision rule from a specific example?**
   - If YES → KEEP (pattern extraction for future cases)
   - If NO → May remove if redundant

See [execution-test.md](references/execution-test.md) for detailed decision framework and examples.

## Evaluation Methodology

### Step 1: Evaluate for Vagueness

Cover examples and read only the instruction. Ask:

- Can it be executed correctly without looking at examples?
- Does it contain subjective terms like "clearly", "properly", "immediately" without definition?
- Are there measurable criteria or explicit steps?

**If VAGUE** → Proceed to Step 3 (Strengthen First)
**If CLEAR** → Proceed to Step 2 (Evaluate Examples)

### Step 2: If Clear (Examples Not Needed for Understanding)

Determine if examples serve operational purpose:

- ✅ Defines what "correct" looks like → **KEEP**
- ✅ Shows exact commands with success criteria → **KEEP**
- ✅ Sequential workflows where order matters → **KEEP**
- ✅ Resolves ambiguity in instruction wording → **KEEP**
- ✅ Data structures (JSON formats) → **KEEP**
- ❌ Explains WHY (educational/rationale) → **REMOVE**
- ❌ Only restates already-clear instruction → **REMOVE**

### Step 3: If Vague (Examples Needed for Understanding)

**DO NOT REMOVE EXAMPLES YET - Strengthen instruction first.**

1. Identify source of vagueness (subjective terms, missing criteria, unclear boundaries)
2. Strengthen the instruction with explicit criteria and measurable steps
3. **KEEP all examples** - They're needed until instruction is strengthened
4. Mark for next pass - Examples can be re-evaluated after strengthening

## Content to ALWAYS Keep

Even with clear instructions, preserve:

1. **Executable Commands** - Bash scripts, jq commands, git workflows
2. **Data Structures** - JSON formats, configuration schemas, API contracts
3. **Boundary Demonstrations** - Prohibited vs permitted patterns, edge cases
4. **Concept Illustrations** - Examples showing what vague terms mean
5. **Templates** - Reusable formats for structured responses
6. **Prevention Examples** - Wrong vs right patterns for frequently violated rules
7. **Pattern Extraction Rules** - Annotations that generalize examples into reusable principles

See [anti-patterns.md](references/anti-patterns.md) for common mistakes to avoid.

## Conciseness Strategies

Apply these techniques while preserving clarity:

1. **Eliminate Redundancy**
   - Remove repeated information across sections
   - Consolidate overlapping instructions
   - Replace verbose phrases with precise terms

2. **Tighten Language**
   - Replace "you MUST execute" with "execute"
   - Replace "in order to" with "to"
   - Remove filler words ("clearly", "obviously", "simply")

3. **Use Structure Over Prose**
   - Convert narrative paragraphs to bulleted lists
   - Use numbered steps for sequential processes
   - Use tables for multi-dimensional information

**Warning**: Do NOT sacrifice these for conciseness:

- Scannability (vertical lists > comma-separated concatenations)
- Pattern recognition (checkmarks/bullets > prose)
- Explicit criteria ("ALL", "at least ONE", "NEVER")
- Measurable thresholds (counts, file paths, exact strings)

## Reference-Based Consolidation Rules

### ❌ NEVER Replace with References

1. **Content within sequential workflows** (Steps 1→2→3) - Breaks execution flow
2. **Quick-reference lists in methodology sections** - Serve different purpose than detailed explanations
3. **Success criteria at decision points** - Must be inline at moment of decision

### ✅ OK to Replace with References

1. **Explanatory content appearing in multiple places** - Rationale, background, historical context
2. **Content at document boundaries** (intro/conclusion) - User not mid-execution
3. **Cross-referencing related but distinct concepts** - "See also" style references

See [execution-test.md](references/execution-test.md) for semantic equivalence tests.

## Execution Flow

1. **Read** the target document
2. **Analyze** each section using the evaluation methodology
3. **Optimize** directly:
   - Strengthen vague instructions with explicit criteria
   - Remove redundant content while preserving clarity
   - Apply conciseness strategies where beneficial
4. **Report** changes made to the user
5. **Commit** the optimized document

## Quality Standards

Every change must satisfy ALL criteria:

- ✅ Meaning preserved - Instructions mean exactly the same thing
- ✅ Executability preserved - Claude can execute correctly without removed content
- ✅ Success criteria intact - What "correct" looks like is still clear
- ✅ Ambiguity resolved - Any ambiguous terms still have defining examples
- ✅ Conciseness increased - Redundancy eliminated or prose tightened

## Idempotent Design

This optimization can be run multiple times:

- **First pass**: Strengthens vague instructions, removes obvious redundancy
- **Second pass**: Further conciseness improvements if instructions are now self-sufficient
- **Subsequent passes**: No changes if already optimized

## Reference Documentation

- [execution-test.md](references/execution-test.md) - Detailed decision framework with examples
- [anti-patterns.md](references/anti-patterns.md) - Common optimization mistakes to avoid
- [examples.md](references/examples.md) - Before/after optimization examples
