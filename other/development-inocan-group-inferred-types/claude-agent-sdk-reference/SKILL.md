---
name: Claude Agent SDK Reference
description: Document for build custom AI agents with the Claude Agent SDK, include full SDK Reference and Example Codes.
---

# Claude Agent SDK Reference

## Instructions
Follow this document to develop any custom AI Agent based on Claude Agent SDK, with system prompts, context management, MCP/Tools/Subagents/Slash Commands/Skills Support.

For any detailed information, read the reference document.

## Agent SDK overview → See [reference/Agent SDK overview.md](reference/Agent SDK overview.md)
Why use the Claude Agent SDK?
What can you build with the SDK?

## Agent SDK reference - TypeScript → See [reference/Agent SDK reference - TypeScript.md](reference/Agent SDK reference - TypeScript.md)
Complete API reference for the TypeScript Agent SDK, including all functions, types, and interfaces.

## Agent SDK reference - Python → See [reference/Agent SDK reference - Python.md](reference/Agent SDK reference - Python.md)
Complete API reference for the Python Agent SDK, including all functions, types, and classes.

## Guides - Streaming Input → See [reference/Streaming Input.md](reference/Streaming Input.md)
Understanding the two input modes for Claude Agent SDK and when to use each.
The Claude Agent SDK supports two distinct input modes for interacting with agents:
    - Streaming Input Mode (Default & Recommended) - A persistent, interactive session
    - Single Message Input - One-shot queries that use session state and resuming
This guide explains the differences, benefits, and use cases for each mode to help you choose the right approach for your application.

## Guides - Handling Permissions → See [reference/Handling Permissions.md](reference/Handling Permissions.md)
Control tool usage and permissions in the Claude Agent SDK.
The Claude Agent SDK provides powerful permission controls that allow you to manage how Claude uses tools in your application.
This guide covers how to implement permission systems using the canUseTool callback, hooks, and settings.json permission rules.

## Guides - Session Management → See [reference/Session Management.md](reference/Session Management.md)
Understanding how the Claude Agent SDK handles sessions and session resumption.
The Claude Agent SDK provides session management capabilities for handling conversation state and resumption. Sessions allow you to continue conversations across multiple interactions while maintaining full context.

## Guides - Hosting the Agent SDK → See [reference/Hosting the Agent SDK.md](reference/Hosting the Agent SDK.md)
Deploy and host Claude Agent SDK in production environments.
The Claude Agent SDK differs from traditional stateless LLM APIs in that it maintains conversational state and executes commands in a persistent environment. This guide covers the architecture, hosting considerations, and best practices for deploying SDK-based agents in production.

## Guides - Modifying system prompts → See [reference/Modifying system prompts.md](reference/Modifying system prompts.md)
Learn how to customize Claude’s behavior by modifying system prompts using three approaches - output styles, systemPrompt with append, and custom system prompts.
System prompts define Claude’s behavior, capabilities, and response style. The Claude Agent SDK provides three ways to customize system prompts: using output styles (persistent, file-based configurations), appending to Claude Code’s prompt, or using a fully custom prompt.

## Guides - MCP in the SDK → See [reference/MCP in the SDK.md](reference/MCP in the SDK.md)
Extend Claude Code with custom tools using Model Context Protocol servers.
Model Context Protocol (MCP) servers extend Claude Code with custom tools and capabilities. MCPs can run as external processes, connect via HTTP/SSE, or execute directly within your SDK application.

## Guides - Custom Tools → See [reference/HCustom Tools.md](reference/Custom Tools.md)
Build and integrate custom tools to extend Claude Agent SDK functionality.
Custom tools allow you to extend Claude Code’s capabilities with your own functionality through in-process MCP servers, enabling Claude to interact with external services, APIs, or perform specialized operations.

## Guides - Subagents in the SDK → See [reference/Subagents in the SDK.md](reference/Subagents in the SDK.md)
Working with subagents in the Claude Agent SDK.
Subagents in the Claude Agent SDK are specialized AIs that are orchestrated by the main agent. Use subagents for context management and parallelization.
This guide explains how to define and use subagents in the SDK using the `agents` parameter.

## Guides - Slash Commands in the SDK → See [reference/Slash Commands in the SDK.md](reference/Slash Commands in the SDK.md)
Learn how to use slash commands to control Claude Code sessions through the SDK.
Slash commands provide a way to control Claude Code sessions with special commands that start with /. These commands can be sent through the SDK to perform actions like clearing conversation history, compacting messages, or getting help.

## Guides - Agent Skills in the SDK → See [reference/Agent Skills in the SDK.md](reference/Agent Skills in the SDK.md)
Extend Claude with specialized capabilities using Agent Skills in the Claude Agent SDK.
Agent Skills extend Claude with specialized capabilities that Claude autonomously invokes when relevant. Skills are packaged as SKILL.md files containing instructions, descriptions, and optional supporting resources.

## Guides - Tracking Costs and Usage → See [reference/Tracking Costs and Usage.md](reference/Tracking Costs and Usage.md)
Understand and track token usage for billing in the Claude Agent SDK.
The Claude Agent SDK provides detailed token usage information for each interaction with Claude. This guide explains how to properly track costs and understand usage reporting, especially when dealing with parallel tool uses and multi-step conversations.

## Guides - Todo Lists → See [reference/Todo Lists.md](reference/Todo Lists.md)
Track and display todos using the Claude Agent SDK for organized task management.
Todo tracking provides a structured way to manage tasks and display progress to users. The Claude Agent SDK includes built-in todo functionality that helps organize complex workflows and keep users informed about task progression.
​
## Guides - Plugins in the SDK → See [reference/Plugins in the SDK.md](reference/Plugins in the SDK.md)
Load custom plugins to extend Claude Code with commands, agents, skills, and hooks through the Agent SDK.
Plugins allow you to extend Claude Code with custom functionality that can be shared across projects. Through the Agent SDK, you can programmatically load plugins from local directories to add custom slash commands, agents, skills, hooks, and MCP servers to your agent sessions.