---
name: concept-analyzer
description: "Analyze Claude Code features and capabilities to uncover advanced usage patterns, best practices, and real-world application scenarios. Use this skill whenever the user mentions a Claude Code feature (like Streaming Tool Execution, Hooks, MCP, Skills, Subagents, Context Management, Permission Modes, etc.) and wants to know how to leverage it effectively — including advanced tips, workflow optimizations, creative use cases, and pitfalls to avoid. Also trigger when the user pastes a feature description or asks 'how to use X better in Claude Code', even without explicitly saying 'analyze'."
---

# Claude Code Feature Analyzer

Analyze Claude Code features and capabilities in depth, producing actionable guidance on advanced usage, best practices, and real-world application scenarios.

## When This Skill Activates

The user provides a Claude Code feature or capability — it could be a feature name like "Streaming Tool Execution", a mechanism like "Hooks", a short question like "MCP 有什么进阶用法？", or a file containing a feature description — and wants to understand how to leverage it effectively in their Claude Code workflow.

## How to Work

### Step 1: Identify the Feature

Read the user's input carefully. It might be:
- A feature name (e.g., "Hooks", "Streaming Tool Execution", "Subagents")
- A question about a capability (e.g., "Skills 有什么进阶用法和最佳实践？")
- A file path containing a feature description — if so, read the file first

If the feature is ambiguous, briefly clarify with the user. Otherwise, proceed directly.

### Step 2: Research the Feature

This step is critical — the analysis must be grounded in how the feature actually works, not generic speculation.

1. **Search the Claude Code source code** in the current workspace to understand the feature's implementation, configuration options, and internal behavior. Look for relevant source files, types, schemas, and test cases.
2. **Search the web** for the latest Claude Code documentation, blog posts, and community discussions about this feature. Claude Code evolves rapidly, so up-to-date information matters.
3. **Cross-reference** what you find in the source code with the documentation to build a complete picture.

Spend real effort here. The quality of the analysis depends entirely on how well you understand the feature's actual capabilities and constraints.

### Step 3: Produce the Analysis Report

Generate a structured markdown report. The depth should match the feature's complexity — a simple configuration option gets a focused analysis, while a major capability like Hooks or MCP deserves a thorough deep dive.

## Report Template

ALWAYS follow this structure:

```
# [Feature Name] — Claude Code 进阶指南

## 功能概述
What this feature is and what problem it solves in the Claude Code workflow.
One paragraph, concise and clear.

## 工作原理
How the feature works under the hood. Include:
- The execution flow (what happens when this feature is triggered)
- Key configuration options and their effects
- How it interacts with other Claude Code components

Use diagrams (text-based) or step-by-step flows when the mechanism
involves multiple phases or components.

## 进阶用法
This is the core section. For each advanced usage pattern:
- **Pattern name**: A descriptive title
- **Scenario**: When you'd want to use this pattern
- **How to set it up**: Concrete configuration or commands
- **Example**: A realistic, copy-pasteable example
- **Why it works**: The reasoning behind this approach

Organize from most practical to most creative. Include at least 3-5 patterns.

## 最佳实践
Actionable recommendations for using this feature effectively.
Each practice should explain the reasoning — not just "do X"
but "do X because Y, which prevents Z".

Focus on:
- Configuration best practices
- Performance and efficiency tips
- Security considerations
- Common mistakes and how to avoid them

## 应用场景
Concrete real-world scenarios where this feature shines:
- **Solo development**: How an individual developer benefits
- **Team workflows**: How teams can leverage this feature
- **CI/CD integration**: How to use this in automated pipelines
- **Domain-specific**: Specialized use cases (data science, DevOps, etc.)

For each scenario, describe the problem, the solution using this feature,
and the outcome.

## 注意事项与陷阱
Honest assessment of limitations and gotchas:
- Known limitations or edge cases
- Performance implications
- Compatibility considerations
- Things that look like they should work but don't

## 与其他功能的组合
How this feature combines with other Claude Code capabilities
to create powerful workflows. For example:
- Hooks + Skills for automated workflows
- MCP + Subagents for parallel research
- Context Management + Hooks for session optimization

## 延伸阅读
Pointers to official documentation, relevant source code files,
community resources, and related features to explore next.
```

### Guidelines

- **Language**: Default to Chinese with English technical terms preserved (e.g., "Hooks", "MCP", "Streaming"). If the user writes in English, respond in English.
- **Be concrete**: Every recommendation should include a realistic example — a config snippet, a command, or a workflow description. Avoid vague advice like "use it wisely".
- **Source-grounded**: Reference specific source code files, configuration schemas, or documentation URLs when making claims about how a feature works. This builds trust and lets the user verify.
- **Practical over theoretical**: Prioritize "here's how to do it" over "here's how it works internally". The user wants to level up their Claude Code usage, not read an architecture doc.

### Output

Save the analysis report as `<feature-name>-claude-code-guide.md` in the current working directory, and display the key highlights in the conversation. If the user specified an output path, use that instead.
