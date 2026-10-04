---
name: sdd-init
description: Khởi tạo template SDD + ADD, Architecture Profile, governance và cấu trúc dự án
user-invocable: true
---

# SDD Initializer (`/sdd-init`)

Dùng cho greenfield hoặc bootstrap SDD+ADD trong repository chưa có canonical governance. Nếu repository đã có canonical `# Project Ownership` và `# Agent Execution` header trong `.sdd/shared_context.md`, skill này không phải default: giữ nguyên canonical route và dùng `/sdd-adopt` cho repository có sẵn hoặc `/sdd-template-update --check` cho template đã adopt.

## Parameters

- `--project-name=<name>`: Optional.
- `--stack=<tech-stack>`: Optional; only explicit known bindings.
- `--project-ownership=solo|team`: Optional Human governance setting; default `team`.
- `--agent-execution=direct|orchestrated`: Optional execution setting; default `direct`. Use `orchestrated` only when the runtime worker capability is observed.
- `--team-size=solo|team`: Deprecated composite alias for one transition release. `solo` maps to `solo/direct`; `team` maps to `team/orchestrated`. Emit a migration warning.

`solo` means one Human project owner; `team` means multiple Human collaborators. `direct` executes in the current Agent session; `orchestrated` allows `/add-execute` to coordinate one or more workers only after runtime capability is observed. The axes are independent.

Reject `--team-size` when combined with `--project-ownership` or `--agent-execution`. When canonical shared-context headers already exist, reject `--team-size`; the alias is valid only while both headers are absent. A deprecated alias may set only its documented composite pair; a canonical flag selects only its own axis.

## Baseline and Architecture Profile

1. Create `.sdd/architecture-profile.md` as canonical artifact-generation source.
2. Parse `--stack` only into explicit bindings; do not infer framework, ORM, validation or commands.
3. Without `--stack`, seed TypeScript + Node.js + Clean Architecture core-only.
4. Record evidence, unresolved binding and canonical `PENDING HUMAN REVIEW` recommendation in the profile.
5. Context/Spec may be business-neutral; Plan/Tasks/execution block until relevant binding and exact command are approved.
6. Methodology Profile sets depth/risk/review route only; it does not replace the Architecture Profile gate.

## Output

1. Create `.sdd/features/`, `.sdd/reviews/`, `.sdd/rfcs/`, `.claude/skills/`, `docs/`, `scripts/`, `src/{domain,usecase,interface,infra,shared}/` and `tests/` within template scope.
2. Generate `AGENTS.md`, `CLAUDE.md`, `.agentignore` and `.gitignore` from repository/stack evidence; do not copy manifest-specific rules or commands without evidence.
3. Initialize `.sdd/README.md`, Architecture Profile, shared context, MCP policy and constraints. Shared context contains `# Project Ownership: <solo|team>` and `# Agent Execution: <direct|orchestrated>`.
4. Install template-owned documentation and support scripts.
5. Create `.sdd/reviews/init.md` with canonical recommendation; Human reviews bootstrap scope before feature work.

## Governance

- `AGENTS.md` retains its eight canonical sections.
- `CLAUDE.md` mirrors approved architecture and durable project guidance; it does not choose stack.
- `.agentignore` and `.gitignore` use observed patterns and protect secret files.
- `CONSTITUTION.md` Layer 1/2 changes require approved RFC.
- `Project Ownership: solo` allows the sole Human owner to persist Human Final Review; `team` allows an authorized Human collaborator. Agents never self-approve.
- `Agent Execution: direct` retains Intent Packet, Methodology Profile, Feature Lock, Shadow Plan, Action Record, Architecture Profile, material checkpoint and validation. `orchestrated` lets `/add-execute` add bounded worker orchestration after observed runtime capability; it does not reduce or replace the same gates.
- Solo delivery removes PR overhead only. Agent never `git push`; Human handles remote delivery after validation and commit.

## AI Recommendation and Human Final Review

Use `.claude/skills/_shared/ai-review-protocol.md`. Recommendation includes bootstrap scope, profile evidence/unknowns, methodology defaults, selected ownership/execution settings, migration warning if applicable, missing decisions and next command. Human Final Review remains `PENDING` until a human records a durable decision.

## Hướng dẫn sử dụng
- **Khi dùng:** Khởi tạo SDD+ADD cho repository mới hoặc repository chưa có canonical shared-context governance.
- **Không dùng:** Không dùng để reset existing canonical state, overwrite user-owned profile, or infer stack/commands.
- **Input:** Optional project/stack and independent ownership/execution flags; reject conflicting `--team-size` and canonical flags as described above.
- **Điều kiện trước:** Repository target and template scope are writable; if canonical headers already exist, preserve them and route changes through adoption/update.
- **Evidence:** Generated governance/profile, core-only baseline or explicit bindings, `.sdd/reviews/init.md`, and migration warning when legacy input applies.
- **Dừng khi:** Existing canonical route conflicts, missing/conflicting stack evidence, unsafe overwrite, or bootstrap review remains unapproved.
- **Human quyết định:** Human approves bootstrap scope, profile unknowns and ownership/execution settings; Agent does not self-approve or push.
- **Lệnh tiếp theo:** After init review `APPROVED`, `/sdd-context --feature=<feature-slug>`; existing state instead continues via its canonical route.
- **Ví dụ:** `/sdd-init --project-name=orders --project-ownership=solo` only when canonical headers are absent.

## Completion output

Use the [Completion output contract](../_shared/ai-review-protocol.md#completion-output-contract). Summarize generated governance, selected ownership/execution axes and Architecture Profile evidence. Bootstrap review `PENDING` is `Human decision required`; an authorized Human reviewer records the selected non-placeholder decision, reviewer identity and persisted Follow-up with `/sdd-review --target=.sdd/reviews/init.md --status=<APPROVED|REVISE|REJECTED> --decision="<human decision>" --reviewer="<authorized human reviewer>" --follow-up="<exact next command or required action>"`. `continue` only after its persisted `APPROVED`: `/sdd-context --feature=<feature-slug>`. Missing/conflicting stack evidence is `BLOCKED`; request the exact Human binding decision rather than inventing a framework or verification command.
