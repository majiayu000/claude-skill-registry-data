---
name: dev-prompt-engineering
description: "Expert guide for crafting high-performance Claude prompts, based on Anthropic's interactive tutorial."
---

# Prompt Engineering (Dev Prompt Engineering)

## Core Principles (Anthropic Best Practices)

### 1. The "Context-First" Rule
- **Context**: Always provide relevant context *before* the instruction.
- **Role**: Assign a persona (e.g., "You are an expert Python architect").
- **XML Tags**: Use XML tags (e.g., `<documents>`, `<instruction>`) to structure input. Claude loves XML.

### 2. The Power of Examples (Few-Shot)
- **Show, Don't Just Tell**.
- Provide 3+ examples of "Input -> Ideal Output" to guide style and format.
- **Anti-Hallucination**: Include examples of how to say "I don't know" or handle edge cases.

### 3. Precognition (Chain of Thought)
- **Let Claude Think**: For complex tasks, ask Claude to "Think step-by-step" before answering.
- **Thinking Tags**: Use `<thinking>` blocks to verify logic before generating the final `<answer>`.

### 4. Language Strategy (Performance vs Usability)
- **Prompt Language**: **English**. (LLMs reason better in English). All instructions, constraints, and system prompts must be in English.
- **Output Language**: **Korean**. The final response meant for the user must be in Korean.
- **Rule**: "Think in English, Speak in Korean."

## 🏗️ Structure of a Great Prompt

1.  **Role & Goal**: Who is Claude? What is the objective?
2.  **Context/Data**: Reference materials wrapped in XML.
3.  **Rules & Constraints**: Dos and Don'ts.
4.  **Examples (Few-Shot)**: Golden samples.
5.  **Instruction**: The immediate task.
6.  **Pre-computation**: "Take a deep breath and think step by step..."

## ✅ Quality Standards
- **Clarity**: Unambiguous instructions.
- **Separation**: Data and instructions are visually distinct (XML).
- **Iterative**: Every prompt should be tested and refined.

## Checklist
- [ ] **Persona**: Is a specific role assigned?
- [ ] **XML Structuring**: Are data parts wrapped in tags?
- [ ] **Examples**: Are there at least 2-3 examples?
- [ ] **CoT**: Is identifying the reasoning process (Thinking) required?
