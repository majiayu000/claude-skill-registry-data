---
name: data-classification-prompt-standard
description: Use when writing, reviewing, or optimizing batch data classification prompts. Enforces the strict structural anatomy, taxonomy rules, input/output formats, and few-shot requirements necessary for high-accuracy data classification at scale.
---

# Data Classification Prompt Standard

This skill defines the **structural standard** for writing batch classification prompts. Any agent or user building a data classification prompt must adhere to this standard. It acts as the "constitution" for classification workflows.

## 1. Prompt Anatomy

Every classification prompt MUST include the following sections, ordered exactly as shown:

1. **SYSTEM CONTEXT & PERSONA** (Top): Define the AI's role, persona, and domain expertise. This establishes the context before providing any tasks.
2. **OBJECTIVE** (Near top): A clear, concise statement of the specific classification task and a high-level overview of the expected output format.
3. **TAXONOMY / CATEGORIES** (Middle-top): The complete list of target categories (labels) the model is allowed to output, along with their precise definitions. See Taxonomy Enforcement Rules below.
4. **EXCLUSIONS & BOUNDARIES** (Middle): Explicit instructions on what to ignore, edge cases that do not qualify, and boundaries for classification.
5. **INSTRUCTIONS & REASONING** (Middle): Numbered, hard rules the model MUST follow. Explain the step-by-step reasoning or thought process (Chain of Thought) the model should execute before arriving at an answer.
6. **FEW-SHOT EXAMPLES** (Lower-middle): Minimum 3 complete input-to-output examples. This grounds the instructions in reality.
7. **OUTPUT FORMAT** (Near end): The strict JSON schema definition and output formatting constraints. Placed near the end to leverage recency bias.
8. **INPUT DATA** (Very end): The actual data to classify, using `{placeholders}` for dynamic replacement.

## 2. Taxonomy Enforcement Rules

Taxonomies dictate the boundaries of the classification. You must enforce these four rules during taxonomy creation:

### Rule 1: Atomic Taxonomy Names
- Every taxonomy label MUST be atomic and singular in concept.
- **FORBIDDEN**: The use of `/`, `&`, or `\` to combine distinct concepts (e.g., "IT Support & Server Maintenance", "Hardware/Software").
- If a proposed label contains these characters, you must challenge the user: *"Should this be split into two separate taxonomies? If they represent different concepts, they MUST be split. Only keep them combined if they are the exact same concept known by different names."*

### Rule 2: Hierarchical Definition Format
Every taxonomy item must follow this precise format, containing a definition and examples:

```markdown
**Level 1: [Category Name]**
Definition: [Scope boundaries — explicitly state when to use this category]
Positive Example: [1 real-data example that perfectly matches this category]

  **Level 2: [Subcategory Name]** (If applicable)
  Definition: [Precise scope + explicit exclusion boundary]
  Positive Example: [Real data that SHOULD match]
  Negative Examples: [1-3 edge cases that SHOULD NOT match, explaining why they belong elsewhere]
```

### Rule 3: Mutual Exclusivity Validation
- Check all taxonomy pairs for potential overlap or ambiguity.
- If two categories could potentially apply to the same input, you MUST force the user to define a disambiguation rule to ensure mutual exclusivity.

### Rule 4: Dual Fallback Categories
Every classification taxonomy MUST include two mandatory fallback categories:
1. **Unmapped Context**: Use when the row is a valid target for the classification objective, but none of the defined taxonomy categories fit.
2. **False Positive**: Use when the row itself is irrelevant and does not fit the classification objective or scope at all.

## 3. Input/Output Standard

- **Input Placeholders**: Use curly braces for dynamic variables at the end of the prompt (e.g., `Text: {Text}`, `Row Data: {Row_Data}`).
- **Output Structure**: The final output MUST be a **single flat JSON object**. No arrays of objects unless absolutely unavoidable.
- **Multi-value Fields**: If a field can have multiple values, use a pipe `|` delimiter within a single string (e.g., `"tags": "tag1 | tag2"`), NOT JSON arrays.
- **No Markdown Wrapping**: Output ONLY raw JSON. Do not wrap the JSON in ```json blocks.
- **Reasoning Key**: Ensure there is a `"reasoning"` key that captures the Chain of Thought as a single continuous string. DO NOT use arrays for reasoning steps.
- **Confidence Key**: Include a `"confidence"` key containing either `"high"`, `"medium"`, or `"low"`. This serves as a secondary signal for human-in-the-loop review.

## 4. Few-Shot Example Standard

- **Minimum Requirement**: Include at least 3 complete examples. 4 to 5 is recommended.
- **Coverage**: The examples must cover:
  1. A typical, straightforward case (True Positive).
  2. A tricky edge case.
  3. A fallback / false-positive case.
- **Completeness**: Each example must include the simulated Input, the simulated Chain of Thought/Reasoning, and the final Output JSON.
- **Realism**: Use real or highly realistic data. Do not use synthetic "lorem ipsum" placeholders.

## 5. Context Engineering Integration

- **Lost-in-the-Middle Mitigation**: Place critical, "do-not-break" constraints at the very START and very END of the prompt.
- **Propagation Rules**: If there are rules about how a fallback category impacts other fields (e.g., "If Category is False Positive, then Impact must also be False Positive"), place these near the TOP of the Instructions.
- **Stable Placement**: The Taxonomy definitions should remain in the middle, as they are large blocks of stable context that require lower attention pressure.
