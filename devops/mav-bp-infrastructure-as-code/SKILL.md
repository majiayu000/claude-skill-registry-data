---
name: mav-bp-infrastructure-as-code
description: Infrastructure as Code conventions for all deployed projects. Covers IaC principles, environment parity, secrets management in IaC, version control, and runbook fallback for unsupported platforms. Applied when reviewing or configuring infrastructure.
user-invocable: false
disable-model-invocation: true
---

# Infrastructure as Code Standards

All infrastructure must be defined, versioned, and reproducible from code; manual provisioning is a last resort and must be documented in a runbook.

## Maverick's Rules

- **Never auto-apply destructive changes** — resource deletion or replacement requires human review before apply. CI follows validate → plan → review → apply; post the plan output to the pull request.
- **One provisioning tool per resource layer** — do not mix (e.g.) Terraform and CloudFormation for the same resources.
- **Secrets never in IaC files** — no credentials in definitions or variable files (including `.tfvars`); reference a secret manager with dynamic injection at deploy time, and mark secret outputs as sensitive.
- **State handling** — remote backend with locking, state isolated per environment, never committed to the repository, never hand-edited (use the tool's state commands). Treat state files as sensitive.
- **Environment parity** — one set of templates parameterised per environment; no separate per-env template copies. Promote dev → staging → prod; run regular plan/diff for drift detection.
- **Traceability** — tag every resource (service, environment, owner, commit SHA); the CI apply identity has limited, audited permissions.
- **Runbook fallback** — any unavoidable manual step gets a runbook stored alongside IaC (e.g., `docs/runbooks/`), including prerequisites, verifiable numbered steps, verification, rollback, owner, and whether it is temporary or should be migrated to IaC. Review runbooks like code.
- **IaC is versioned with application code** and follows the same review/merge process. Container orchestration definitions (Helm, Kustomize, manifests) are IaC too.

## Project Implementation Lookup

Check for `docs/maverick/skills/infrastructure-as-code/SKILL.md`. If present, read it and follow it — it wins on specifics (library, config, conventions). If missing, proceed with these standards and note the gap in your summary.

## Detecting IaC Issues in Code Review

| Pattern                                        | Issue                          | Fix                                                  |
| ---------------------------------------------- | ------------------------------ | ---------------------------------------------------- |
| Hard-coded secret in IaC file                  | Secret exposure                | Move to secret manager, reference dynamically        |
| Copy-pasted templates per environment          | Environment drift risk         | Parameterise a single template                       |
| State file committed to repository             | State corruption risk          | Move to remote backend with locking                  |
| No plan step in CI pipeline                    | Blind apply                    | Add plan stage, require review before apply          |
| Manual infrastructure change with no runbook   | Undocumented, unreproducible   | Write a runbook or convert to IaC                    |
| Resources with no tags or labels               | Untrackable resources          | Add standard tags (service, environment, owner, SHA) |
| Destructive changes auto-applied               | Accidental data loss           | Require human approval for destroy/replace actions   |
| Mixed IaC tools for the same resource layer    | Conflicting state management   | Standardise on one tool per layer                    |

<!-- maverick-plugin-version: 4.0.2-dev -->
