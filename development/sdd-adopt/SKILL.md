---
name: sdd-adopt
description: Khảo sát repository có sẵn, tạo Architecture Profile và tích hợp SDD + ADD không làm thay đổi source hiện có
user-invocable: true
---

# SDD Brownfield Adoption (`/sdd-adopt`)

Dùng để adopt SDD+ADD vào repository có source hoặc tạo Reverse Spec cho module legacy. Đây là default khi repository đã có source hoặc đã có canonical shared-context governance. Trên repository đã adopt template, `/sdd-template-update` là canonical route cho template drift; `/sdd-adopt` không reset canonical header hay approved profile đã tồn tại.

## Parameters

- `--stack=<tech-stack>`: Optional explicit stack.
- `--reverse-feature=<feature-slug>`: Optional.
- `--path=<module-path>`: Optional; used with `--reverse-feature`.
- `--project-ownership=solo|team`: Optional Human governance setting; default `team`.
- `--agent-execution=direct|orchestrated`: Optional execution setting; default `direct`. Use `orchestrated` only when the runtime worker capability is observed.
- `--team-size=solo|team`: Deprecated composite alias for one transition release: `solo` maps to `solo/direct`; `team` maps to `team/orchestrated`. Emit a migration warning.

`solo` is one Human project owner and may use orchestrated workers. `team` is multiple Human collaborators and may use direct execution. Do not infer either from the other. Reject `--team-size` when combined with `--project-ownership` or `--agent-execution`; when canonical shared-context headers already exist, reject `--team-size` because the alias is valid only while both headers are absent. Canonical flags select only their own axis.

## Adoption workflow

1. Survey root, manifest, lockfile, runtime/bootstrap, database/migration, CI, test configuration, source layout and docs.
2. Create/update Architecture Profile with evidence, confidence and conflicts for runtime, framework, DB, ORM/query, validation and test/build/lint commands.
3. Resolve approved profile → clear repository evidence → explicit `--stack` → core-only baseline.
4. Keep conflicts `PENDING HUMAN REVIEW`; do not self-resolve.
5. Context/Spec may be business-neutral; Plan/Tasks/execution need selected/evidenced binding and exact command.
6. Generate/reconcile governance from actual repository; never overwrite approved Constitution rules.
7. Install template-owned docs and support scripts under their staged/NEVER safety rules.

## Governance generation

Generate `AGENTS.md`, `CLAUDE.md`, `.agentignore` and `.gitignore` from observed convention, paths, commands and secret boundaries. Persist `Project Ownership` and `Agent Execution` independently in shared context. If a legacy collaboration header is found and new headers are absent, create a durable `PENDING HUMAN REVIEW` migration recommendation; never rewrite it silently.

`/add-execute` maps persisted orchestrated execution to Claude Code `Agent` only with observed host evidence; unavailable runtime is `BLOCKED`, not direct fallback. Adoption does not copy assumed settings, identity provider or permission configuration. A solo Human owner may persist review; a team review must be persisted by an authorized Human collaborator. Agents never self-approve or push.

## Reverse Spec

With `--reverse-feature` and `--path`:

1. Observe source and tests; produce Context, Spec, Plan and Tasks as evidence of current behavior.
2. Keep Spec `DRAFT`; existing code is not approved business intent.
3. Include Intent Packet, Methodology Profile, Feature Lock/deferred-work decision, state-change classification and trace/sync implications.
4. Add `@ears` or change source only after explicit scope approval and relevant profile gate.

## Shared contract and execution

Only the named contract owner changes frozen shared contracts. Direct execution retains the same ownership/checkpoint constraints. Orchestrated execution requires task ID, frozen version, ownership boundary, selected binding/evidence, exact commands, checkpoint and audit reference in every worker packet.

## AI Recommendation and Human Final Review

Create `.sdd/reviews/adopt-<slug>.md` with canonical protocol block. Include discovered evidence, unresolved/conflicting binding, governance impact, selected ownership/execution settings, migration impact, recommendation and required Human decision. Agent does not self-approve or treat reverse-engineered behavior as approved business intent.

## Hướng dẫn sử dụng
- **Khi dùng:** Bootstrap governance in an existing repository or reverse-spec a named legacy module without treating behavior as approved intent.
- **Không dùng:** Không dùng để overwrite approved Constitution, silently rewrite existing canonical governance, or execute feature code.
- **Input:** Optional explicit `--stack`, `--reverse-feature` with `--path`, and canonical ownership/execution flags; reject `--team-size` when canonical headers exist or with canonical flags.
- **Điều kiện trước:** Repository root and evidence are readable; existing canonical shared-context headers take precedence and are preserved.
- **Evidence:** Adoption survey, Architecture Profile conflicts, generated/reconciled governance, reverse Spec `DRAFT`, and `.sdd/reviews/adopt-<slug>.md`.
- **Dừng khi:** Evidence conflicts, missing binding for planning, unsafe overwrite boundary, or reverse path/feature is invalid.
- **Human quyết định:** Human approves adoption scope, migration, bindings and reverse-spec intent; Agent never self-approves or pushes.
- **Lệnh tiếp theo:** After persisted adoption review, use its exact Follow-up; normally `/sdd-context --feature=<feature-slug>` for new feature work.
- **Ví dụ:** `/sdd-adopt --reverse-feature=legacy-orders --path=src/orders` records current behavior as `DRAFT` only.

## Completion output

Use the [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Summarize observed repository evidence, generated/reconciled governance, profile conflicts and reverse-spec state when applicable. Adoption review is `Human decision required`; an authorized Human reviewer records the selected non-placeholder decision, reviewer identity and persisted Follow-up with `/sdd-review --target=.sdd/reviews/adopt-<slug>.md --status=<APPROVED|REVISE|REJECTED> --decision="<human decision>" --reviewer="<authorized human reviewer>" --follow-up="<exact next command or required action>"`. Only the persisted Follow-up can select a next feature command. Conflicting/missing binding evidence is `BLOCKED`; do not infer a stack or treat reverse-engineered behavior as approved intent.
