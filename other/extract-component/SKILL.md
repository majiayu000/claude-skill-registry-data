---
name: extract-component
description: This skill should be used when the user asks to "extract skill", "extract command", "extract agent", "extract pattern", "save as skill", "save as command", "save as agent", "turn this into a skill", "make this a command", "save this workflow", "提取技能", "提取命令", "提取 agent", "保存为技能", "提取可复用模式", or wants to extract reusable components (skills, commands, agents) from the current conversation history.
---

# Extract Component

## Overview

Analyze the current conversation history and extract reusable patterns into Claude Code components — Skills, Commands, or Agents. This skill identifies valuable methodology, operation sequences, and decision workflows from the conversation and generates properly formatted component files.

## Intent Classification

When the user triggers this skill, determine the extraction intent:

1. **Explicit type** — User specifies what they want (e.g., "extract a skill", "make this a command")
2. **Auto-detect** — User wants extraction but hasn't specified the type (e.g., "extract pattern", "save this workflow")

### Component Type Guidelines

- **Skill** — A methodology, technique, or approach for solving a category of problems. Skills describe *how to think about* a problem, with progressive disclosure of details. Best for: debugging strategies, review processes, design methodologies, domain-specific expertise.
- **Command** — A concrete sequence of operations that can be executed with parameters. Commands are action-oriented with clear inputs and outputs. Best for: build workflows, deployment steps, data processing pipelines, repetitive multi-step tasks.
- **Agent** — An autonomous workflow that requires decision-making, branching logic, and tool usage. Agents operate independently within defined boundaries. Best for: code review workflows, test generation, documentation creation, complex analysis tasks.

## Execution

Route to the `/skill-extractor:extract` command with the user's intent:

1. If the user specified a type, pass it as an argument (e.g., `/skill-extractor:extract skill`)
2. If auto-detect, pass no type argument — the command will analyze and recommend

Invoke the command: `/skill-extractor:extract $ARGUMENTS`
