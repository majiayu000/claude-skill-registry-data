---
name: graphql-query-cost-budget
description: "Use when nested GraphQL fields or pagination can cause unbounded resolver work and need a measurable cost limit; not for schema style review."
---

# Graphql Query Cost Budget

## Purpose

Bound GraphQL resource use with a documented model and adversarial tests.

## Required inputs

Schema, resolver costs, pagination limits, request telemetry, complexity rules, and query fixtures.

## Workflow

1. Identify cost drivers such as nested lists, fan-out, remote calls, and pagination; model worst-case growth.
2. Define weights and a maximum budget, accounting for fragments and aliases in the effective operation.
3. Test deep nesting, large pages, repeated aliases, fragments, and requests just below/above the limit.
4. Calibrate estimates against measured latency/resource use and preserve regression fixtures.

## Verification checklist

- [ ] Fragments and aliases cannot bypass effective cost accounting.
- [ ] Nested collections have explicit limits or bounded cost.
- [ ] Over-budget requests fail before expensive work where possible.
- [ ] Weights have evidence from representative workloads.

## Required output

A field-cost map, budget, adversarial results, and calibration notes.

## Boundaries and failure handling

Static complexity scoring is not a complete DoS defense; retain rate limits and execution timeouts.

When evidence, permissions, or environment details are missing, stop at the supported analysis, record the missing prerequisite, and do not report unexecuted validation as passing.

## Trigger examples

- **Positive:** A query can request thousands of nested records via pagination.
- **Negative:** Checking REST response backward compatibility.
