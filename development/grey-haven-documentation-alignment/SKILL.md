---
name: grey-haven-documentation-alignment
description: "6-phase verification system ensuring code matches documentation with automated alignment scoring (signature, type, behavior, error, example checks). Reduces onboarding friction 40%. Use when verifying code-docs alignment, onboarding developers, after code changes, pre-release documentation checks, or when user mentions 'docs out of sync', 'documentation verification', 'code-docs alignment', 'docs accuracy', 'documentation drift', or 'verify documentation'."
# v2.0.43: Skills to auto-load for docs verification
skills:
  - grey-haven-code-style
# v2.0.74: Tools for documentation alignment verification
allowed-tools:
  - Read
  - Grep
  - Glob
  - TodoWrite
---

# Documentation Alignment Skill

6-phase verification ensuring code implementations match their documentation with automated alignment scoring.

## Description

Systematic verification of code-documentation alignment through discovery, extraction, analysis, classification, fix generation, and validation.

## What's Included

- **Examples**: Function signature mismatches, parameter changes, type updates
- **Reference**: 6-phase process, alignment scoring formula
- **Templates**: Alignment report structures
- **Checklists**: 101-point verification checklist

## Alignment Scoring

Score = (Signature×30% + Type×25% + Behavior×20% + Error×15% + Example×10%)
- 95-100: Perfect
- 80-94: Good
- 60-79: Poor
- 0-59: Failing

## Use When

- Onboarding new developers (reduces friction 40%)
- After code changes
- Pre-release documentation verification

## Related Agents

- `documentation-alignment-verifier`

**Skill Version**: 1.0
