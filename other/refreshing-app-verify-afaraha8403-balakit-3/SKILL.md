---
name: refreshing-app-verify
description: >-
  Keep a generated verification skill and feature map honest: source wave
  per feature, one live pass driving every feature, at most one PR of proven
  corrections. Apply when the user invokes /refreshing-app-verify or
  asks to audit the verify skill. Use generating-app-verify if none
  exists. Never edit product code on this pass.
user-invocable: true
disable-model-invocation: true
version: "1.1.0"
author: "Ali Farahat"
tags: ["verification", "maintenance", "feature-map"]
when_to_use: |
  USE WHEN:
  - The user asks to audit or update an existing verify skill / feature map.
  DO NOT USE WHEN:
  - No verify skill exists (use generating-app-verify).
  - The user wants product-code fixes (report regressions; do not patch the app here).
---

# Refresh an app verify skill

> **Leading words:** source then live, proven corrections, never product code.

Upkeep for a skill from `generating-app-verify`. The unit is the
feature, not every sentence.

Copy these steps into the todo list verbatim. Skip with `skip: <reason>`.

1. Locate `skills/verify-*/` (or the project's verify skill). None → stop and point at generating-app-verify.
2. Index hygiene on the feature-map README.
3. Source wave: one read-only subagent per feature file. Children never drive or edit.
4. Reconcile recipes. Flag user-facing surfaces missing from the map only with a source path.
5. Live pass: exercise every feature at least once. Doctor before first drive and after failed drives. Evidence survives cleanup.
6. Triage: map drift → fix the map. Harness gap → fix harness. App broken → report, do not paper over.
7. Outcome: **clean** (no PR) / **changed** (one PR of proven corrections) / **blocked** (say what blocked).

## Edit scope

Only the verification skill directory. A behavior the map describes that the
app no longer does is doc drift (fix the map) or a product regression (report
it).

## Reply contract

Outcome, features covered, unreachable prerequisites, confirmed drift.
