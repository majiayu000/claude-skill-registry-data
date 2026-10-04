---
name: patpat-automation
description: Design or scaffold a safe external automation for a concrete provider, trigger, and verification surface. Use when an integration is named and write authority, idempotency, compensation, secrets, and kill-switch behavior must be settled.
---

# Patpat Automation

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) and [execution graph](../patpat-loop/references/execution-graph.md) in full. Do not load the router.

Read [boundary discipline](../patpat-loop/principles/boundary-discipline.md), [idempotent effects](../patpat-loop/principles/idempotent-effects.md), and [preserve safety](../patpat-loop/principles/preserve-safety.md). Apply the [automation design playbook](../patpat-loop/playbooks/automation-design.md). For a named issue-source triage and reproduce loop, also apply the [issue loop playbook](../patpat-loop/playbooks/issue-loop.md). Do not copy a host automation pack or enable a scheduler.

Require a concrete provider, immutable trigger identity, trusted coordinator, exact allowed writes, secret source outside the repository, idempotency key, dedupe behavior, immediate preflight, bounded retries and cost, safe test surface, verifier, and kill switch. Require compensation when reversal is possible; otherwise name the irreversible boundary and fail before it when state or authority is uncertain. Fail closed when any write-critical field is missing: return a configuration checklist and do not produce runnable or enabled automation.

Keep external writes under one coordinator. Give workers no credentials, write tools, or posting instructions. Default generated automation to disabled and test it against a sandbox or dry-run surface.

Enabling, scheduling, posting, filing, publishing, or deployment requires explicit authority immediately before the action. A provider-triggered issue loop may open only a draft pull request by default. Ready-PR delivery requires separate fresh interactive delivery intent (not activation alone).

## Proof closure

Close repository mutations through:

- [`patpat-verify`](../patpat-verify/SKILL.md)
- [`patpat-review`](../patpat-review/SKILL.md)
