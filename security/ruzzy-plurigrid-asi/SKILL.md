---
name: ruzzy
description: Rust fuzzing with Ruzzy for automated vulnerability discovery.
category: testing-handbook-skills
author: Trail of Bits
source: trailofbits/skills
license: AGPL-3.0
trit: -1
trit_label: MINUS
verified: true
featured: false
---

# Ruzzy Skill

**Trit**: -1 (MINUS)
**Category**: testing-handbook-skills
**Author**: Trail of Bits
**Source**: trailofbits/skills
**License**: AGPL-3.0

## Description

Rust fuzzing with Ruzzy for automated vulnerability discovery.

## When to Use

This is a Trail of Bits security skill. Refer to the original repository for detailed usage guidelines and examples.

See: https://github.com/trailofbits/skills

## Related Skills

- audit-context-building
- codeql
- semgrep
- variant-analysis


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 8. Degeneracy

**Concepts**: redundancy, fallback, multiple strategies, robustness

### GF(3) Balanced Triad

```
ruzzy (+) + SDF.Ch8 (−) + [balancer] (○) = 0
```

**Skill Trit**: 1 (PLUS - generation)


### Connection Pattern

Degeneracy provides fallbacks. This skill offers redundant strategies.
