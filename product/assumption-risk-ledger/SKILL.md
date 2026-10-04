---
name: assumption-risk-ledger
description: "Map product assumptions by risk, confidence, evidence, and next validation step."
---

# Assumption Risk Ledger

Surface and prioritize the untested assumptions embedded in any product plan before development begins.

## Required Inputs

Ask the user for these if not provided:
- **Product brief, PRD, or concept description** (even rough notes work)
- **Stage** (concept / discovery / pre-build / post-launch - affects which assumptions matter most)

## Process
1. Read the provided brief, PRD, or concept description
2. Extract assumptions across four categories:
   - **Desirability** (do users want this?)
   - **Feasibility** (can we build it?)
   - **Viability** (will it sustain the business?)
   - **Usability** (can users actually use it?)
3. Score each assumption:
   - Confidence (1-5): How sure are we this is true?
   - Impact (1-5): How badly does the plan fail if this assumption is wrong?
   - Priority = Impact − Confidence (higher = test first)
4. **Validate completeness** - Ensure at least one assumption per category. If a category is empty, re-read the brief looking specifically for that type.
5. Output a ranked list with recommended validation methods

## Output Structure

### Assumption Map: [Feature/Product Name]

| Assumption | Category | Confidence | Impact | Priority | Validation Method |
|------------|----------|------------|--------|----------|-------------------|
| [assumption] | [type] | [1-5] | [1-5] | [score] | [method] |

#### Critical Assumptions (Impact 4+ and Confidence 2 or below)
[Flagged items with detailed validation recommendations]

#### Top 3 Assumptions to Validate First
[Detailed recommendations including specific research method, estimated effort, and what the result would change]
