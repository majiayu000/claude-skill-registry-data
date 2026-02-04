---
name: prompt-writer
description: Expert prompt engineering for LLMs and AI agents. Use when users request help writing, reviewing, or improving prompts for chatbots, AI agents, system prompts, instruction sets, or any LLM-based application. Applies research-backed techniques to minimize hallucinations and maximize reliability.
---

# Prompt Writer

## Overview

This skill provides expert guidance for crafting effective prompts for LLMs and AI agents. It applies research-backed techniques from cognitive science, prompt engineering research, and production LLM systems to create prompts that are clear, reliable, and minimize hallucinations.

## When to Use This Skill

Activate this skill when users request:
- "Write a prompt for [agent/chatbot/system]"
- "Help me improve this prompt"
- "Review my prompt for [task]"
- "Create a system prompt for [application]"
- "I need a prompt template for [use case]"
- Any request involving prompt engineering, instruction writing, or LLM configuration

## Workflow

### 1. Load the Prompting Guide

**ALWAYS** start by reading the comprehensive prompting guide:

```bash
Read references/prompting-guide.md
```

This guide contains:
- Mental models for how LLMs process prompts
- Architecture of effective prompts
- Research-backed reasoning techniques (Chain of Thought, Tree of Thoughts, etc.)
- Agent-specific prompting strategies
- Anti-patterns and common mistakes
- Complete examples and templates

### 2. Understand the Use Case

Clarify the prompt's purpose by asking:
- What task should the LLM perform?
- Is this for a chat interface or an AI agent with tools?
- What are the inputs and expected outputs?
- Are there quality/reliability requirements?
- What failure modes should be prevented?

### 3. Apply Prompting Principles

Based on the guide in `references/prompting-guide.md`, apply relevant techniques:

**For All Prompts:**
- Use clear, specific instructions
- Provide concrete examples
- Define the output format explicitly
- Include relevant constraints and guardrails

**For Complex Tasks:**
- Apply Chain of Thought reasoning
- Break down multi-step processes
- Use self-verification steps
- Include error handling instructions

**For AI Agents:**
- Define tool usage patterns clearly
- Specify when to use which tools
- Include decision trees for complex workflows
- Add verification steps before actions

### 4. Structure the Prompt

Follow the architecture from the prompting guide:
1. **Context/Role** - Who is the LLM? What's the scenario?
2. **Task** - What exactly should be done?
3. **Format** - How should the output be structured?
4. **Examples** - Concrete demonstrations (when helpful)
5. **Constraints** - What to avoid, quality requirements
6. **Reasoning Process** - How to think through the task (for complex prompts)

### 5. Review and Iterate

Check the prompt against common failure modes:
- Is it specific enough to prevent hallucinations?
- Does it include examples for clarity?
- Are edge cases handled?
- Is the output format unambiguous?
- Would this work reliably across different inputs?

## Resources

### references/prompting-guide.md

Comprehensive guide covering:
- **Part I:** How LLMs Actually Work
- **Part II:** Architecture of Effective Prompts
- **Part III:** Engineering Reliable Outputs
- **Part IV:** Research-Backed Advanced Reasoning Techniques
- **Part V:** Mastering AI Agent Prompting
- **Part VI:** Advanced Techniques for Complex Tasks
- **Part VII:** Complete Examples and Templates
- **Part VIII:** Anti-Patterns and Common Myths
- **Part IX:** Failure Modes and Recovery
- **Part X:** Advanced Operations
- **Part XI:** Quick Start and Reference

**Usage:** Read this file at the start of every prompt-writing task. Reference specific sections as needed during the writing process.

## Examples

### Example 1: User Request
> "Write me a system prompt for a code review agent"

**Process:**
1. Read `references/prompting-guide.md`
2. Identify this as an AI agent task (Part V)
3. Apply agent-specific patterns
4. Include tool usage instructions
5. Add verification steps

### Example 2: User Request
> "Help me improve this prompt: 'Summarize this document'"

**Process:**
1. Read `references/prompting-guide.md`
2. Identify missing elements (output format, length, focus areas)
3. Apply prompt architecture principles (Part II)
4. Add specificity and examples
5. Define clear success criteria

### Example 3: User Request
> "Create a prompt for extracting structured data from unstructured text"

**Process:**
1. Read `references/prompting-guide.md`
2. Apply Chain of Thought reasoning (Part IV)
3. Define explicit output schema
4. Include examples of input → output
5. Add validation steps to prevent hallucinations
