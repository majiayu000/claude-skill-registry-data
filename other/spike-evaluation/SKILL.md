---
name: spike-evaluation
description: Run bounded spike work to test feasibility before committing to a normal implementation path. Use when Spec wants Builder to try an idea, library, integration, or technical approach and report back against explicit success and failure criteria.
---

# Spike evaluation

## Purpose
Use spikes to answer viability questions, not to smuggle in normal delivery work.

## Ownership
- Spec creates the spike issue
- Spec defines the question being tested
- Spec defines explicit success and failure criteria
- Builder performs the bounded experiment and reports results
- Orchestrator decides next-step routing after the spike outcome is visible

## Branch model
- use a spike branch, not a normal feature branch
- keep the branch clearly tied to the spike issue
- do not treat spike output as merge-ready implementation by default

## Output expectations
A spike should report:
- what was attempted
- what succeeded
- what failed
- constraints discovered
- recommendation for next step
- whether a normal implementation issue should now be created

## Guardrails
- keep scope narrow and time-boxed
- do not quietly convert a spike into a production feature
- if spike code should survive, create a follow-on normal issue and PR path intentionally
