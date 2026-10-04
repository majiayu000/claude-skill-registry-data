---
name: mvp-full
description: From idea to working MVP in one workflow
argument-hint: <project-name> [idea text]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: max
---

# MVP — Full Project

Chain: idea-capture → architecture-propose → scaffold → foundation-deps → foundation-config → foundation-testing → foundation-ci → feature-implement (core) → feature-test → pm-assess

## Process

1. Capture the idea: understand what the user wants to build
2. Propose architecture: design the system
3. Get user approval on architecture
4. Scaffold the project: create all boilerplate
5. Install dependencies
6. Set up configuration
7. Set up testing infrastructure
8. Set up CI pipeline
9. Implement the core feature (the one thing that makes this an MVP)
10. Write tests for the core feature
11. Assess: verify everything works, report what's done

## Rules

- Stop and ask the user at key decision points (architecture, core feature definition)
- Every step must leave the project in a working state
- The MVP must actually run and do something useful
- Don't over-build — MVP means minimum viable