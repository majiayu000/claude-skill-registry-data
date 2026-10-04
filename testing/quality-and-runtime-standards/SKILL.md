---
name: quality-and-runtime-standards
description: Enforce high test coverage, high code quality, portable test harnesses, CI workflows, and containerized backend execution. Use when defining quality gates, QA expectations, README/run documentation, test harness requirements, GitHub Actions workflows, or Docker-based execution standards for project repos.
---

# Quality and runtime standards

## Documentation baseline
The project root `README.md` should always let a new contributor quickly:
- set up the project
- run the project
- run tests
- understand core developer workflows

## Quality baseline
- unit test coverage should be high
- code quality should be high using standard tooling for the stack
- integration tests should be part of the quality model
- bugs, edge cases, and race cases found in delivery should gain regression automation in a portable test harness where practical

## Ownership
- QA and Spec define and enforce quality expectations
- Builder implements within those expectations and reports any gaps
- Orchestrator resolves quality-threshold disputes when agents disagree

## CI and environment standards
- build GitHub Actions workflows that run the sensible test harnesses at the right lifecycle points
- run backend build/test flows in appropriate Docker containers so local and CI environments stay aligned where practical
