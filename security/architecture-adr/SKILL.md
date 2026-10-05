---
name: architecture-adr
description: "Trigger: architecture decision, API contract, ADR, integration boundary. Record reversible and consequential technical choices."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Use for technical decisions with lasting impact.

# Hard Rules
- Record decisions that affect contracts, data model, security, reliability or delivery cost.
- Prefer smallest reversible design compatible with the current MVP.
- Do not use production data through tools.

# Execution Steps
1. State context, constraints and alternatives.
2. Evaluate consequences for React/Vite, NestJS, Prisma, Neon and OpenAI integration.
3. Choose with human TL approval.
4. Save ADR and an Engram observation using a stable topic key.

# Output Contract
Return context, decision, alternatives, consequences and migration/rollback notes.
