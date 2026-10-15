---
name: bdd-tdd-expert
description: Expert in Behavior-Driven Development (BDD), the Red/Green/Refactor (TDD) cycle, and Gherkin language. Use when creating or modifying features using behavior-driven or test-driven development workflows.
---

# BDD and TDD Expert

This skill provides expert guidance for Behavior-Driven Development (BDD) and the Red/Green/Refactor (TDD) cycle. It focuses on creating robust, maintainable, and well-tested code through collaborative behavior definitions and iterative development.

## Core Workflows

### 1. Behavior-Driven Development (BDD)
BDD bridges the gap between stakeholders and developers.
- **Discovery**: Work with the user to define clear, concrete examples of feature behavior.
- **Formulation**: Document behaviors as Gherkin specifications (`.feature` files).
- **Automation**: Use the specifications to guide test implementation.
- **Guidance**: See [bdd-gherkin.md](references/bdd-gherkin.md) for principles and Gherkin syntax.

### 2. Red / Green / Refactor (TDD)
The core loop for reliable software implementation.
- **Red**: Write a failing test first to define the goal.
- **Green**: Implement just enough code to pass the test.
- **Refactor**: Improve the code while keeping it green.
- **Guidance**: See [red-green-refactor.md](references/red-green-refactor.md) for phase details and best practices.

## Agent Instructions for Gherkin and Coding

When acting on a development task:
1. **Identify the Feature**: Start by defining the high-level goal in a `.feature` file using Gherkin.
2. **Draft Scenarios**: Create scenarios that cover happy paths, edge cases, and error states.
3. **Execute Red/Green/Refactor**:
   - Create tests corresponding to the Gherkin scenarios (e.g., unit tests or integration tests).
   - Ensure they fail.
   - Implement the minimal logic to make them pass.
   - Refactor for quality and performance.
4. **Validation**: Confirm the implementation matches the Gherkin behavior by running the automated tests.

## External Resources
- [Codecademy: TDD Red/Green/Refactor](https://www.codecademy.com/article/tdd-red-green-refactor)
- [Cucumber: Behavior-Driven Development](https://cucumber.io/docs/bdd/)
