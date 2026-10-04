---
name: infra-kit.workflow.verify
description: Standardize post-change verification and “definition of done” evidence for infra work (IaC/Helm/GitHub/Kubernetes).
---

# Verification (Definition Of Done)

Use this skill after implementing changes (or before marking a ticket “done”) to produce a clear, repeatable verification record.

This skill is cross-cutting: it applies regardless of whether the change was Terraform/Terragrunt, Helm, GitHub Actions, or a Kubernetes rollout.

## Outcomes

- Prevent false “fixed” claims by requiring explicit, recorded evidence
- Make rollback readiness explicit
- Produce a skimmable verification section suitable for PR description and ticket updates

## Where This Fits In The Flow

- Use after implementation work and before `infra-kit.workflow.audit` (or as part of the final readiness gate).
- Use to fill `implementation-notes.md` and to complete `plan.md` `Verification` with real outputs.

## Output Rules

- Always write verification evidence to the repo (not only chat output).
- Prefer writing into the active work item:
  - `docs/infras-kit/work-items/<id>-<slug>/implementation-notes.md`
  - and/or add a short `verification.md` in the same folder when the evidence is large.
- List only commands that were actually run, and capture the observed outputs (or summaries with links/files).

## Workflow

1. Confirm the “definition of done” inputs:
   - acceptance criteria from `ticket.md`
   - verification intent from `plan.md`
2. Build a verification matrix (AC -> check -> expected -> observed).
3. Run the strongest deterministic checks available for the change surface:
   - IaC: `terraform fmt/validate/plan` or `terragrunt validate/plan`
   - Helm: `helm lint`, `helm template`, schema validation (`kubeconform`), dry-run apply when safe
   - GitHub Actions: `actionlint` when available; confirm permissions and triggers by inspection
   - Kubernetes runtime: `kubectl get/describe/logs` evidence (read-only first)
4. Capture evidence:
   - commands run
   - key outputs (or file paths to captured outputs)
   - what was not run and why (missing creds, missing tools, no cluster access)
5. Rollout and rollback readiness:
   - what was rolled out (or not)
   - rollback trigger and exact rollback steps
6. Close with remaining risks and follow-ups.

## Verification Record Template

Write the following (at minimum) into `implementation-notes.md` or `verification.md`:

- Scope verified:
- Acceptance criteria verification matrix:
- Commands run:
- Observed evidence:
- Skipped checks (and why):
- Rollback readiness:
- Residual risks:

## Guardrails

- Do not claim “verified” unless you can point to a command output, log excerpt, or explicit inspected file.
- If verification requires prod access, ask for approval and limit blast radius (read-only first).
