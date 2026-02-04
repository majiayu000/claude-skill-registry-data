---
name: design_documents
description: Co-author design docs and propose section-by-section requirement edits
metadata:
  short-description: Design docs plus requirements edits with before/after deltas
---

# SKILL.md

## Overview

Blockprints follows a structured flow from high-level requirements to low-level implementation. This document outlines how agents should contribute to that flow by co-authoring design artifacts alongside human designers.

Agents are expected to:

* Collaborate on design documents.
* Capture irreversible decisions in Architecture Decision Records (ADRs).
* Produce fully self-contained ExecPlans for implementation.
* Propose and apply section-by-section requirement edits when the user asks to edit requirements or PRDs.

## Document Hierarchy

The project maintains the following hierarchy:

### 1. Product Requirements Document (PRD)

* **Location:** `docs/prd.md`
* **Authored by:** Human designers (with agent suggestions permitted)
* **Purpose:** Define what the software must do and why it matters
* **Notes:** Agents may propose PRD edits, but human approval is required

### 2. Design Documents

* **Location:** `docs/design/feature_name.md`
* **Authored by:** Designers and agents
* **Purpose:** Describe how a subsystem or capability will be implemented
* **Properties:**

  * Living documents
  * May include multiple related features
  * Serve as the canonical reference for system behavior and structure

### 3. Architecture Decision Records (ADRs)

* **Location:** `docs/adr/feature_name.md`
* **Authored by:** Agents or designers
* **Purpose:** Record high-impact decisions made during design evolution
* **Properties:**

  * One ADR per significant decision
  * Immutable after acceptance, with status (`Proposed`, `Accepted`, etc.)

### 4. Execution Plans (ExecPlans)

* **Location:** `docs/plans/planNNNN_feature_name.md`
* **Authored by:** Agents (with iterative human review)
* **Purpose:** Provide a complete, self-contained plan for a coding agent to deliver a working feature
* **Formatting and lifecycle:** Governed strictly by `docs/plans.md`

## Agent Responsibilities

* Use the PRD as a source of constraints and goals; do not overwrite without explicit instruction
* Assist in authoring and refining design documents with the goal of creating implementation-ready guidance
* Record important decisions made during design doc creation as ADRs in `docs/adr/`
* Generate executable specifications as ExecPlans in `docs/plans/`, conforming strictly to `plans.md`

## Best Practices for Agents

* Respect the document hierarchy and conventions
* Prefer clarity over cleverness
* Reference design documents when generating code, comments, or ExecPlans
* Treat all authored documents as part of a living design system
* Collaborate closely with the designer; escalate ambiguity through the `Decision Log` section in ExecPlans

## Requirement & PRD Editing Workflow

Use this workflow when the user asks to edit requirements or PRDs with iterative, section-by-section edits.

### Phase 1: Conceptual feedback

1) Review the section and provide numbered, high-level, architectural/conceptual feedback.
2) Iterate with the user until the conceptual feedback is aligned and approved.

### Phase 2: Detailed edits

3) Extract the exact original text to replace.
4) Draft the replacement text based on the approved conceptual direction.
5) Present easy-to-see differences using a numbered before → after list of changes.
6) Wait for user approval.
7) Apply the change after approval.

#### Notes

* Always propose section-by-section.
* Keep diffs minimal and scoped to the user-approved text.
* If the original text does not match, do not replace; ask the user to re-sync or re-copy the section.

## File Naming Summary

* PRD: `docs/prd.md`
* Design Docs: `docs/design/feature_name.md`
* ADRs: `docs/adr/feature_name.md`
* ExecPlans: `docs/plans/planNNNN_feature_name.md` (zero-padded global sequence)

## Last Updated

Jan 2, 2026
