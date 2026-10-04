---
name: bb-spec-review
description: "对规格文档（PRD + arch_spec + MAS）做对抗性评审：完整性 / 一致性 / 可实现性 / 验证覆盖。默认 role=ruthless（规格阶段错误成本最高）。在 MAS frozen 前调用。触发场景：(1) bba-architect 写完 MAS；(2) 显式 /bb-spec-review。"
user-invocable: true

---

# bb-spec-review

## 职责

跨文档检查 PRD ↔ arch_spec ↔ MAS 一致性、可实现性、验证覆盖；输出严重程度分级 issues。

- 调用者：`bba-architect`
- 关联：`bb-challenge-code`（通用）
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| prd_path | path | true | — | PRD.md |
| arch_spec_dir | path | true | — | arch_spec 目录 |
| mas_dir | path | true | — | `spec_mas/`（directory containing MAS markdown files） |
| role | enum | false | `ruthless` | `ruthless`\|`linus`\|`balanced` |
| focus | string | false | `feasibility,consistency,coverage` | — |
| design_name | string | true | — | — |
| stamp | string | false | `<auto>` | — |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/spec_review_<stamp>.md` |
| `issues_found` | int |
| `severity_summary` | `{critical,high,medium,low}` |
| `consistency_issues` | list[str] |
| `feasibility_issues` | list[str] |
| `coverage_issues` | list[str] |
| `pass` | bool（critical==0 && high≤2） |
| `valid` | bool |

## 4-Phase 执行

### Phase 1 — build_prompt

```python
prd = open(prd_path).read()
arch = {p.name: p.read_text() for p in Path(arch_spec_dir).glob("*.md")}
mas = {p.name: p.read_text() for p in Path(mas_dir).glob("*.md")}
prompt = render_spec_review_prompt(role, focus, prd, arch, mas)
```

### Phase 2 — run_review

`claude --print "<prompt>" > <artifact_path>` 或 agent 内部生成。15 min timeout（文档可能很长）。

### Phase 3 — parse_spec_review

`scripts/parse_spec_review.py`：

- 提 `## Consistency` / `## Feasibility` / `## Coverage` 段
- 计 severity
- `pass = (critical == 0 && high <= 2)`

### Phase 4 — return

返回 JSON。`pass=false` → bba-architect 修 MAS（≤2 iter），仍失败 → escalate 用户。

## 维度

| 维度 | 检查 |
|------|------|
| consistency | PRD FR ↔ arch module ↔ MAS FSM 三层一致 |
| feasibility | 频率/面积/PDK 能力匹配 |
| coverage | verif_plan_seed 完整、corner 覆盖 |
| ambiguity | 模糊描述、边界缺失 |

## 通过标准

| 级别 | 通过 |
|------|------|
| critical | == 0 |
| high | ≤ 2 |

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| pass=true | frozen MAS + 开 `ready-for-rtl` |
| pass=false & iter<2 | bba-architect 修 MAS 重评 |
| iter≥2 | escalate 用户 |

## 资源索引

- `scripts/build_prompt.py`、`scripts/run_review.py`、`scripts/parse_spec_review.py`
- `references/spec_review_dimensions.md`
