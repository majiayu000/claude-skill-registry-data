---
name: randomization
description: "Implement proper randomization procedures for experiments. Use when: (1) Assigning participants to conditions, (2) Ensuring unbiased allocation, (3) Meeting CONSORT standards, (4) Pre-registration."
allowed-tools: Read, Write, Bash
version: 1.0.0
---

# Randomization Skill

## Purpose
Implement proper random assignment to minimize selection bias.

## Randomization Methods

**1. Simple Randomization**
- Coin flip, random number generator
- Best for large samples (N>200)
- Risk of imbalance in small samples

**2. Block Randomization**
- Ensures equal group sizes
- Blocks of 4, 6, or 8
- Example: AABB, ABAB, BABA, BBAA

**3. Stratified Randomization**
- Balance prognostic factors
- Stratify by sex, age group, severity
- Then randomize within strata

**4. Minimization**
- Dynamic allocation
- Minimizes imbalance across factors
- Used in small trials

## Implementation

**Steps:**
1. Generate random sequence (with seed)
2. Document sequence generation
3. Implement allocation concealment
4. Execute randomization
5. Document actual allocation

**Example (Python):**
```python
import random
random.seed(12345)  # Document seed
sequence = ['A', 'B'] * 50  # 100 participants
random.shuffle(sequence)
```

---
**Version:** 1.0.0
