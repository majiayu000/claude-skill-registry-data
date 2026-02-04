---
title: "'Spec-first, Agent Implemented' SDLC Skill for Claude"
date: "2025-12-21"
description: "'Spec-first, Agent Implemented' SDLC Skill for Claude"
tags: ["claude-code", "sdlc", "autonomous-coding", "artificial-intelligence", "ai"]
draft: false
---

Agents like Claude Code and Codex are seeing an increasing adoption in software development lifecycle. Here, I discuss a novel AI agents engagement method that has significantly enhanced my development experience.

AI generated code implementations for complex features may exhibit a wide spectrum of quality based on the AI engagement method. Widely used one shot prompt technique of asking AI agents to implement a feature / function often yields inferior results. More the feature complexity, and dependencies involved, more the divergence of the implementation from the intent.

Part of the reason for this is jumping straight from intent to final code without explicitly considering the high-level design (including primary control-flows, data models involved), preparing ADRs with rationale, and agreeing to an Executable Implementation Spec (with defined API contracts in place).

(Sometimes I really do wonder if the UML guys were right. Seems like they were!)

This skill forces Claude to consider those aspects in details, and even ask open-ended questions from the user before continuing with implementation. This reduces a lot of ambiguity and leverages Claude's thinking capability to the fullest.

> GitHub repo: [https://github.com/esxr/sdlc-skill.git](https://github.com/esxr/sdlc-skill.git)
