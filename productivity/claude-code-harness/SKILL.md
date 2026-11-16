---
name: claude-code-harness
description: "Use when setting up a structured Plan→Work→Review→Release cycle for autonomous agents, integrating Claude Code with Codex/Cursor/OpenCode, enforcing spec-first development gates, or protecting against agent self-modification. Triggers on: 'claude-code-harness', 'harness cycle', 'agent release cycle', 'spec gate', 'plan work review release', 'harness-plan', 'harness-work', 'harness-review', 'harness-release', 'codex integration', 'cursor integration', 'opencode integration', 'multi-tool agent workflow', 'autonomous agent cycle', 'agent tự động release'."
---

# Claude Code Harness Skill
# Source: chachamaru127/claude-code-harness (MIT) — v4.15.0, 2.6k stars
# Tier: TIER 3 — PRODUCTIVITY

Framework biến agents thành autonomous delivery pipeline.
Plan→Work→Review→Release cycle tự chạy — human chỉ approve spec một lần.

---

## Khi nào dùng

- Muốn agents tự plan + implement + review + release mà không cần trigger từng bước
- Tích hợp nhiều AI tool (Claude Code + Codex + Cursor) trong cùng repo
- Cần verification gate độc lập (agent không tự review code mình viết)
- Bảo vệ harness rules khỏi bị agent tự sửa (v4.15.0 self-modification protection)

---

## 5 Commands cốt lõi

```
/harness-setup    — khởi tạo spec.md + Plans.md, cấu hình tool tier
/harness-plan     — draft spec từ intent → human approve contract
/harness-work     — implement tasks từ approved spec (TDD)
/harness-review   — independent review, không phải agent tự review
/harness-release  — package evidence, prepare deployment
```

**Quan trọng:** `/harness-work` bị block nếu spec.md chưa được approve.
Human chỉ cần approve 1 lần → agents tự chạy phần còn lại.

---

## Tool Capability Matrix

| Capability | Claude Code | Codex CLI | OpenCode | Cursor |
|---|---|---|---|---|
| skill_loading | ✅ Full | ✅ Full | ◐ Partial | ◐ Partial |
| pre_use_guard | ✅ Full | ◐ Partial | ✗ No | ◐ Partial |
| post_use_gate | ✅ Full | ✅ Full | ◐ Partial | ✅ Full |
| memory_bridge | ✅ Full | ◐ Partial | ✗ Future | ✗ Future |
| review_artifact | ✅ Full | ✅ Full | ◐ Partial | ✅ Full |

> "The same capability name ≠ the same enforcement strength" — mỗi tool implement khác nhau.

---

## Cursor Integration (Planning ↔ Implementation)

Cursor làm PM side, Claude Code làm implementation side — cùng repo, không conflict.

```markdown
# Plans.md — shared source of truth
## Task: Add auth middleware
pm:依頼中 / cc:TODO     ← Cursor tạo task
cc:WIP                   ← Claude Code đang làm
cc:完了                  ← Claude Code xong
pm:確認済               ← Cursor approve
```

**Workflow:**
1. Cursor: draft `Plans.md` với acceptance criteria
2. Claude Code: `/harness-work` → implement → update marker `cc:完了`
3. Cursor: review + `/harness-release handoff`

**Rule:** Không để Cursor và Claude Code edit cùng 1 task block cùng lúc.

---

## Codex CLI Integration

```bash
# Codex-specific skills tách riêng khỏi shared skills
skills/          # shared — Claude Code + Codex đều dùng
skills-codex/    # Codex-only — instruction surface khác

# Sync sau khi edit skill
bash scripts/sync-skill-mirrors.sh
```

Codex không có `pre_use_guard` đầy đủ — safety dựa vào Go runtime guardrails thay vì hooks.

---

## OpenCode Integration

OpenCode tier: **internal-compatible** (partial support).

```yaml
# opencode.json config
{
  "harness": {
    "spec_gate": true,
    "pre_use_guard": false,   # OpenCode không support
    "fallback": "go-runtime"  # dùng Go guardrails thay thế
  }
}
```

`memory_bridge` chưa có → facts không persist giữa sessions với OpenCode.

---

## Self-Modification Protection (v4.15.0)

```
Agent KHÔNG được sửa:
  skills/         — skill definitions
  harness-rules/  — gate logic
  Plans.md        — task contracts (chỉ update markers)

Nếu agent cố sửa → Go runtime block + log SELF_MOD_ATTEMPT
```

Tương đương `49-immutable-infrastructure-law.md` của YAMTAM nhưng apply cho harness layer.

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu /harness-work chạy trước khi spec.md được approve
❌ FAIL nếu agent tự review code mình vừa viết (phải dùng /harness-review độc lập)
❌ FAIL nếu Codex/OpenCode dùng feature đánh dấu ✗ trong capability matrix
✅ PASS khi: spec approved → work complete → review pass → release artifact generated
```

## See also
- `executing-plans` — plan execution đơn giản không có release cycle
- `spec-planner` / `spec-executor` — YAMTAM native planning pipeline
- `autonomous-agent-harness` — agent action space design
