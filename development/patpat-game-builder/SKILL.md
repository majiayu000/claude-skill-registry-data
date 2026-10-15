---
name: patpat-game-builder
description: Build or extend a runnable game or gameplay feature in the user's project. Verify rules and a real playthrough when the target runtime is available. Do not use for game concepts, design documents, repository diagrams, or ordinary applications.
metadata:
  patpat.ontology: '{"schema":"patpat-ontology/v1","mutation_level":"LOCAL_MUTATION","target_entity":"Codebase","requires_state":[],"produces_state":[],"verification_cmd":""}'
---

# Patpat Game Builder

Before following this skill, apply the [skill state and mutation gate](../patpat-loop/references/operating-protocol.md#skill-state-and-mutation-gate).

Work in the user's actual game project and conventions. For a new feature, guide the work from brief to runnable slice; for existing projects, load only the applicable playbooks. Verify requested rules and player-facing behavior on the target runtime when available; name any missing proof. Keep this entry point short: load the primary playbook and only the conditional workflows and matrix rows that apply.

Read [gameplay contract](principles/gameplay-contract.md), [player feedback](principles/player-feedback.md), [smallest safe change](../patpat-loop/principles/smallest-safe-change.md), [preserve safety](../patpat-loop/principles/preserve-safety.md), and [proof over proxy](../patpat-loop/principles/proof-over-proxy.md). For architecture, security, persistence, cross-cutting, or delivery risk, read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full. Do not load the router.

## Choose the workflow

- For a new game or an end-to-end gameplay feature, follow [build a playable slice](playbooks/build-playable-slice.md).
- For a gameplay defect found while building that slice, follow [diagnose gameplay behavior](playbooks/diagnose-gameplay.md). Route an isolated existing defect through [patpat-debug](../patpat-debug/SKILL.md).
- To prove the result on the player's interface, follow [verify a playthrough](playbooks/verify-playthrough.md).
- When the user requests visual direction or polish, also follow [visual iteration](playbooks/visual-iteration.md). A visual pass is not implied by every gameplay request.
- Read the [gameplay validation matrix](references/gameplay-validation-matrix.md) to select relevant checks; skip rows outside the requested scope.

## Keep the work Patpat-native

- Inspect and change the user's target project. Never replace it with a throwaway or canary game to stand in for the requested work.
- Detect and use the project's actual engine, version, launcher, input map, assets, and test conventions. Do not require a particular engine, CLI, MCP, plugin, agent role, or reference-image set.
- Preserve the user's language and design intent. A request inspired by an existing game permits broad mechanic inspiration, not copying its code, identity, art, audio, levels, or presentation.
- Do not use a build, screenshot, or rule test as a substitute for an actual playthrough when player behavior is claimed.
- Keep playable, rule-correct, visual, performance, and release claims separate. Report only the gates the request and evidence cover.
- Do not publish, upload, buy assets, create accounts, or enable online services without explicit authority.

## Proof closure

Define the five-field proof contract before any mutation. Close mutating work with:

- Always: [`patpat-verify`](../patpat-verify/SKILL.md), using authoritative evidence.
- When required: [`patpat-review`](../patpat-review/SKILL.md) for delivery intent, auth/security/billing/secrets, architecture or cross-cutting scope, durable-run LEARN or REPORT, land/merge, or another operating-protocol review gate.

For clear, bounded, reversible local work with none of those review requirements, proceed from verification to REPORT without independent review.
