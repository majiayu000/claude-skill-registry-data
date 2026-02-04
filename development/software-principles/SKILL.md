---
name: software-principles
description: Core software engineering principles including DRY, SOLID, KISS, and YAGNI for writing maintainable and scalable code
---

# Software Principles

This skill provides guidance on fundamental software engineering principles that help you write clean, maintainable, and scalable code.

## When to Use This Skill

Use this skill when:
- Designing new features or systems
- Refactoring existing code
- Reviewing code for quality and maintainability
- Making architectural decisions
- Identifying code smells or technical debt
- Teaching or learning software engineering best practices

## Core Principles

This skill covers four fundamental principles:

1. **DRY (Don't Repeat Yourself)** - Eliminate code duplication
2. **SOLID** - Five principles for object-oriented design
3. **KISS (Keep It Simple, Stupid)** - Favor simplicity over complexity
4. **YAGNI (You Aren't Gonna Need It)** - Don't add functionality until it's needed

## How to Apply These Principles

### During Design Phase
- Start with YAGNI: only design what's needed now
- Apply KISS: choose the simplest solution that works
- Consider SOLID: design for extensibility where it makes sense
- Plan to avoid duplication with DRY

### During Implementation
- Apply DRY: extract common code into reusable functions/modules
- Follow SOLID: especially Single Responsibility and Open/Closed principles
- Maintain KISS: resist the urge to over-engineer
- Remember YAGNI: don't add "nice to have" features

### During Code Review
- Check for DRY violations: repeated logic or patterns
- Validate SOLID adherence: proper separation of concerns
- Evaluate complexity: ensure KISS is followed
- Question features: verify YAGNI isn't being violated

### During Refactoring
- Identify duplication and apply DRY
- Improve design with SOLID principles
- Simplify complex code using KISS
- Remove unused features (YAGNI violations)

## Principle Documentation

Detailed documentation for each principle:

- [DRY - Don't Repeat Yourself](./principles/DRY.md)
- [SOLID - Object-Oriented Design Principles](./principles/SOLID.md)
- [KISS - Keep It Simple, Stupid](./principles/KISS.md)
- [YAGNI - You Aren't Gonna Need It](./principles/YAGNI.md)

## Balancing Principles

These principles sometimes create tension:
- DRY vs YAGNI: Don't create abstractions until duplication is clear
- KISS vs SOLID: Don't add complexity for theoretical extensibility
- All principles vs pragmatism: Follow principles but deliver working software

## Key Takeaway

These principles are guidelines, not laws. Apply them with judgment based on context, team size, project complexity, and business needs. The goal is better software, not perfect adherence to principles.
