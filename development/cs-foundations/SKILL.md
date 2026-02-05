---
name: cs-foundations
description: Master discrete mathematics, logic, formal proofs, and computational thinking. Build the mathematical foundation for all computer science.
sasmp_version: "1.3.0"
bonded_agent: 01-cs-foundations-expert
bond_type: PRIMARY_BOND
---

# CS Foundations Skill

## Skill Metadata

```yaml
skill_config:
  version: "1.0.0"
  category: theoretical
  prerequisites: []
  estimated_time: "6-8 weeks"
  difficulty: intermediate

  parameter_validation:
    topic:
      type: string
      enum: [logic, proofs, sets, functions, combinatorics, number-theory, graphs]
      required: true
    depth:
      type: string
      enum: [intro, standard, advanced]
      default: standard

  retry_config:
    max_attempts: 3
    backoff_strategy: exponential
    initial_delay_ms: 500

  observability:
    log_level: INFO
    metrics: [topic_usage, proof_verification_rate, exercise_completion]
```

---

## Quick Start

Computer science is built on mathematics. Master these fundamentals:

### Core Topics

**Discrete Mathematics**
- Set theory and operations
- Logic and proof techniques
- Combinatorics and counting
- Number theory basics
- Relations and functions

**Computational Thinking**
- Problem decomposition
- Abstraction and generalization
- Pattern recognition
- Algorithmic thinking

**Formal Logic**
- Propositional logic
- Predicate logic
- Proof by induction
- Truth tables and logical equivalence

---

## Learning Path

**Week 1: Logic Basics**
- Boolean algebra
- Truth tables
- Logical operators
- Inference rules

**Week 2: Proof Techniques**
- Direct proof
- Proof by contradiction
- Mathematical induction
- Strong induction

**Week 3: Set Theory**
- Set operations (∪, ∩, complement)
- Cartesian product
- Relations
- Equivalence relations

**Week 4: Functions**
- Function notation
- Domain, codomain, range
- One-to-one and onto
- Function composition

**Week 5: Combinatorics**
- Counting principles
- Permutations
- Combinations
- Pigeonhole principle

**Week 6: Number Theory**
- Modular arithmetic
- Prime numbers
- GCD and Euclidean algorithm
- Congruence

---

## Practice Problems

1. Prove by induction that 1+2+...+n = n(n+1)/2
2. Prove √2 is irrational
3. Show A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)
4. Count functions from {1,2,3} to {a,b}
5. Solve: x ≡ 5 (mod 12) and x ≡ 3 (mod 8)

---

## Troubleshooting

| Issue | Root Cause | Resolution |
|-------|------------|------------|
| Proof stuck | Missing case or wrong direction | Check base case, verify induction step |
| Set operation confusion | ∪ vs ∩ mix-up | Draw Venn diagram |
| Counting error | Overcounting duplicates | Distinguish P(n,r) vs C(n,r) |
| Modular arithmetic error | Forgot wraparound | Work with remainders explicitly |

---

## Key Concepts

- **Axioms**: Statements we assume true
- **Theorems**: Statements we prove
- **Lemmas**: Helper theorems
- **Corollaries**: Results that follow easily

---

## Why It Matters

These foundations enable:
- Understanding algorithm correctness
- Analyzing computational complexity
- Designing new algorithms
- Proving algorithm properties
- Understanding what's computable

---

## Interview Prep

- Explain mathematical induction
- Prove that a function is injective
- Count permutations with constraints
- Solve modular equations
- Apply pigeonhole principle
