---
name: tdd
description: Test-driven development — crear tests antes del código de producción
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

## What I do
- Guía para implementar Test-Driven Development (TDD)
- Ciclo Red-Green-Refactor
- Crear tests antes del código de producción
- Asegurar que el código pase todos los tests

## When to use me
Use this when:
- Building new features test-first
- User mentions "red-green-refactor"
- Wanting integration tests
- Fixing bugs with test coverage
- Improving existing test suites

## TDD Cycle
1. **Red**: Escribir un test que falle
2. **Green**: Escribir el código mínimo para que pase
3. **Refactor**: Limpiar el código manteniendo los tests verdes

## Project Context
- Framework: Vitest
- E2E: Playwright
- Run tests: `pnpm test:unit`
- Coverage: Aim for meaningful coverage, not 100%
