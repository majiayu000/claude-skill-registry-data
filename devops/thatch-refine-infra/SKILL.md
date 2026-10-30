---
name: thatch-refine-infra
description: Type-specific requirements for refining a plan that touches infrastructure (CI pipelines, Terraform, Kubernetes manifests, build and deploy configuration). Loaded by thatch-refine after classification; assumes the core loop in thatch-plan-refinement. Use when a wrong premise can break deploys or pipelines for everyone downstream.
---

You are refining a plan for an **infra** change: CI pipelines, Terraform,
Kubernetes manifests, build and deploy configuration. The governing value
is blast radius: a wrong premise here does not break one feature, it
breaks every pipeline, environment, or developer downstream of it, often
silently and often for everyone at once. Load `thatch-plan-refinement`
for the core loop and apply the deltas below; where they disagree, these
win.

## What this type owes

- **Near-absolute pattern-following.** Configuration is the worst place
  for novelty. Copy the established pattern from a sibling pipeline,
  module, or manifest even when a better one exists; propose the better
  one as its own change, after this one lands.
- **Rollback as a first-class deliverable.** Every change names how it
  backs out, concretely (which command, which revert, which state to
  re-apply), not "revert the commit if problems arise."
- **Staged verification.** The plan verifies against a non-production
  target first (staging environment, a canary job, a dry-run or plan
  output) and names what a successful verification looks like before
  production applies it.

## How this changes the loop

- **Deep mode is the default.** Infra changes almost always touch shared
  persistent state that other consumers read, which is the core skill's
  first deep-mode trigger.
- **Premises verify against live state, not memory.** The most dangerous
  infra premise is "the current setup is X" recalled from memory. Check
  the actual manifests, the actual pipeline config, the actual running
  versions, and cite where you checked. Terraform drift and manual
  console changes make memory especially unreliable here.
- **Consensus is unchanged**, but the reviewer prompt should emphasize
  checking the rollback and verification sections explicitly.

## Lens weights

- **Hidden problems (pre-mortem) dominates.** The question is "who reads
  this state that the plan does not know about?" - dependent pipelines,
  environments sharing the module, developers relying on cache behavior,
  jobs relying on timing. Enumerate the dependents by reading what
  actually references the resource, not by recollection.
- **Safe-to-modify is second.** An infra change landing in untested
  configuration without a verification step is a finding.
- **Alternatives and pattern/reuse mostly skip.** The pattern question
  was answered above: follow it.

## Extra plan sections

- **Rollback plan.** Concrete and executable, as above.
- **Verification step.** What runs in staging or dry-run first, and what
  result counts as safe to proceed.
- **Sequencing.** Infra changes often must land in an order (create
  before reference, drain before delete). The plan states the order and
  what breaks if it is violated.

## Docs bar

A one-paragraph change note for the team (what changed, why, how to
roll back) is the deliverable. Config comments explain constraints the
next person must not violate.
