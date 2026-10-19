---
name: pstack-maintain-verification-skill
description: "Audit a project's verification instructions and feature map against source and live behavior. Use when a verification skill is stale or application flows have changed."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/maintain-verification-skill
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Maintain a verification skill

Keep the verification contract honest. Edit only its owned instructions, feature map, and helpers, unless the user separately authorizes product changes.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Locate and index

Find the named skill and its feature map through known project locations. Resolve ambiguity from context; ask only when the target cannot be established. If none exists, report that prerequisite instead of inventing an audit target.

Compare the index with actual feature files. Identify missing, duplicate, stale, and changed entries without creating a redundant inventory.

## Source pass

Trace every in-scope feature against current entry points, roles, state, persistence, and commands. Source readers may run independently when authorized; only the coordinator drives a shared app instance. Record citations, likely drift, and the smallest live recipe per feature.

## Live pass

Exercise every in-scope feature, including those whose documentation looked correct. Health-check the intended instance before driving it and after surprising failures. Merge overlapping recipes to reuse safe states without losing coverage.

Keep captured evidence through failed attempts and final cleanup. Clean only owned residue. A fresh CLI session and a long-lived UI server have different lifecycle requirements.

A missing role, entitlement, dataset, provider, or OS is a coverage gap with the attempted route and prerequisite. Unreachable is not passed. Repair proven harness drift inside scope and re-drive the affected recipe before accepting it.

## Reconcile and deliver

Classify discrepancies as documentation drift, harness gaps, or product regressions. Fix the first two when authorized; report product regressions separately, preserving the intended contract rather than rewriting it to match a bug.

Report clean, changed, or incomplete with a source/live coverage table. Changed means proven local corrections, not automatic PR creation. No scheduler, issue, PR, or publication is implied by this audit.
