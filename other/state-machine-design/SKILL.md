---
name: state-machine-design
description: Use when designing or reviewing run, task, or step states and allowed transitions in PonyBunny.
---

# State Machine Design

## Use this skill when
- defining statuses
- changing lifecycle logic
- adding retries or resume
- fixing invalid transitions
- reviewing execution safety

## Goals
- make states explicit
- prevent illegal transitions
- improve recoverability
- support clear debugging

## Process
1. Define the entity.
2. List valid states.
3. Define allowed transitions.
4. Define transition triggers.
5. Define terminal states.
6. Define retry and resume behaviour.
7. Define forbidden transitions and invariants.

## Output contract
Return:
- state list
- allowed transitions
- transition triggers
- terminal states
- retry/resume notes
- invariants
- forbidden transitions
