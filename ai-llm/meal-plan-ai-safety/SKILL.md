---
name: meal-plan-ai-safety
description: "Trigger: OpenAI meal plan, prompt, structured output, food restrictions, AI evaluation. Build NutrIA AI safely."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Use for meal plan or recipe generation features.

# Hard Rules
- Require explicit preferences, restrictions and objective inputs.
- Enforce a structured response schema and server-side validation.
- Do not make health diagnoses or clinical recommendations.
- Invalid, unsafe or incomplete output fails recoverably; do not invent a substitute.

# Execution Steps
1. Define input/output contract and version prompt/schema.
2. Add deterministic evaluation fixtures for restrictions and malformed outputs.
3. Validate generated output before persistence/display.
4. Attach evaluation evidence to Linear and save durable learnings to Engram.

# Output Contract
Return contracts, safety cases, evaluation result and limitations.
