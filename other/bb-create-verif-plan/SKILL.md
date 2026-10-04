---
name: bb-create-verif-plan
description: "把 mas/verif_plan_seed.md 扩展为完整验证计划 markdown（功能检查点、覆盖率目标、边界、随机约束、test case 清单）。触发场景：(1) bba-guru-verification 启动时；(2) 显式 /bb-create-verif-plan。"
user-invocable: true

---

# bb-create-verif-plan

## 职责

读 `verif_plan_seed.md` + MAS（接口/FSM/clock_domains），输出 `verification_plan.md`，含 6 个必备 section。

- 调用者：`bba-guru-verification`
- 下游：`bb-generate-tb`
- 禁止使用：Task / Agent / Skill

## Input Args

| arg | type | required | 默认 | 说明 |
|-----|------|----------|------|------|
| verif_plan_seed | path | true | — | `designs/<name>/mas/verif_plan_seed.md` |
| mas_path | path | true | — | `designs/<name>/mas/mas.json` |
| design_name | string | true | — | — |
| stamp | string | false | `<auto>` | — |

## Output Contract

| field | 值 |
|-------|----|
| `artifact_path` | `designs/<name>/verif/verification_plan.md` |
| `script_path` | `designs/<name>/verif/gen_plan_<stamp>.py` |
| `sections` | list[str] |
| `functional_points` | int（FTP 数） |
| `coverage_bins` | int |
| `valid` | bool |
| `error` | string\|null |

## verification_plan.md 必备 sections

1. **Functional Coverage Groups**（FSM 状态 / 操作模式各一） 
2. **Code Coverage Targets**（line / branch / toggle / condition；100%）
3. **Functional Test Points**（编号 `FTP-NNN`，与 PRD FR 对应）
4. **Corner Cases**（边界值 / 溢出 / 复位时序 / CDC crossing）
5. **Random Constraints**（约束随机策略）
6. **Test Case List**（FTP → seq 映射，供 `bb-generate-tb` 用）

## 4-Phase 执行

### Phase 1 — render_plan_py

`scripts/render_plan_py.py`：

```python
import json
mas = json.load(open(mas_path))
seed = open(verif_plan_seed).read()
# 1. 从 mas.fsm 提 FSM 状态 → covergroup
# 2. 从 mas.interfaces 提关键信号 → coverpoint
# 3. 把 seed 中已列条目编号为 FTP-001..
# 4. 渲染 6-section markdown
```

### Phase 2 — run_gen_plan

`timeout 180 uv run python <script_path> > <artifact_path> 2> <log>`

### Phase 3 — parse_plan

`scripts/parse_plan.py`：

- 正则查 6 个必备 `## <Section>` 标题 → `sections`
- 统计 `FTP-\d+` 出现次数 → `functional_points`
- 统计 covergroup `bins` 行 → `coverage_bins`
- `valid = (sections == 6_required)`

### Phase 4 — return

返回 JSON。`bba-guru-verification` 用此初始化 coverage tracker，调 `bb-generate-tb`。

## 收敛 / 失败

| 状态 | 行动 |
|------|------|
| valid=true | 进 `bb-generate-tb` |
| sections 缺失 | 重生成 1 次 |
| 仍失败 | `error="plan sections incomplete"` |

## 资源索引

- `scripts/render_plan_py.py`、`scripts/run_gen_plan.py`、`scripts/parse_plan.py`
- `assets/verif_plan.md.tmpl`
- `references/coverage_naming.md` — covergroup/bin 命名规范
