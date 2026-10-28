---
name: cannbot-skill-reviewer
description: 审查新提交或修改的 CANNBot Skill 是否符合入库质量要求。当用户需要评审 SKILL.md、检查新增 cannbot skill、审查 GitCode PR 中的技能变更、验证测试/开发/NPU/Ascend 相关 skill 是否合格时使用；输出结构门禁、九维评分、阻塞问题和可执行整改建议。
license: CANN-2.0
---

# CANNBot Skill Reviewer

审查新增或修改的 `SKILL.md` 是否可以进入 CANNBot Skills 仓库。审查必须同时覆盖仓库硬性门禁、CANNBot 项目约定、质量评分和安全边界。

## 审查原则

- 先跑自动门禁，再做人工质量判断；自动门禁的 `error` 均为阻塞项。
- 只审查候选 skill 本身及其 `references/`、`scripts/`、`assets/` 等随附资源；不要顺手重构无关 skill。
- 不运行候选 skill 声称的高风险命令，不安装候选依赖，不访问未知外部服务；需要实测时先说明风险和替代方案。
- 评分依据必须能追溯到文件内容、仓库规范或测试输出，不凭印象给分。
- 结论使用 `PASS`、`CONDITIONAL`、`REJECT` 三类，先给结论，再列证据和整改清单。

## 输入识别

支持三类输入：

1. 本地路径：`infra/foo/SKILL.md`、`ops/foo/` 或绝对路径。
2. GitCode PR：先读取 PR diff，只审查新增或修改的 `SKILL.md` 及其随附资源。
3. 粘贴的 `SKILL.md`：保存到临时目录后审查，报告中标记为 `paste` 来源。

若同一次输入包含多个候选 skill，逐个审查并给出汇总表；不要把多个 skill 合并成一个分数。

## 工作流程

### Step 1：定位候选 skill

1. 确认候选 `SKILL.md` 路径。
2. 检查目录名是否与 frontmatter `name` 一致。
3. 记录随附资源：
   - `references/`
   - `scripts/`
   - `assets/`
   - 测试用例或文档入口

### Step 2：运行自动门禁

在 CANNBot Skills 仓库根目录执行：

```bash
python infra/cannbot-skill-reviewer/scripts/review_skill.py <path-to-skill-or-dir>
```

需要给 CI 或工具消费时输出 JSON：

```bash
python infra/cannbot-skill-reviewer/scripts/review_skill.py <path-to-skill-or-dir> --json
```

脚本会复用 `tests/lib/skill_validator.py` 执行成文法门禁，并按 [判例法设计审查](references/case-law-review.md) 生成评分。若脚本不可用，则直接运行：

```bash
python tests/lib/skill_validator.py validate-skill <path-to-SKILL.md>
```

### Step 3：判例法质量复核

按 `references/case-law-review.md` 复核自动评分，重点看：

1. Frontmatter 质量
2. 工作流清晰度
3. 边界条件覆盖
4. 检查点设计
5. 指令具体性
6. 资源整合度
7. CANNBot 架构适配性
8. 领域可信度与安全边界
9. 验证证据

当自动评分与人工阅读明显不一致时，以人工复核为准，并在报告中说明原因。

### Step 4：给出入库结论

判定规则：

| 结论 | 条件 | 处理建议 |
|------|------|----------|
| `PASS` | 无阻塞错误，总分不低于 80，关键维度无明显短板 | 可以进入后续 PR 审查或合入流程 |
| `CONDITIONAL` | 无阻塞错误，但总分 70-79 或存在重要警告 | 修改后复审 |
| `REJECT` | 存在自动门禁 `error`、总分低于 70、或存在安全/可信源硬伤 | 不建议合入，先修阻塞项 |

## 输出格式

```markdown
## Skill Review Report

- Skill: <name>
- Path: <path>
- Verdict: PASS / CONDITIONAL / REJECT
- Score: <score>/100
- Blocking findings: <count>

### Blocking Findings
| Rule | Evidence | Fix |

### Quality Scores
| Dimension | Weight | Score | Reason |

### Required Fixes
1. <必须修复的问题>

### Suggestions
1. <非阻塞优化建议>

### Verification
- Command: `<command>`
- Result: <pass/fail/partial>
```

## 错误处理

- 找不到 `SKILL.md`：要求用户提供准确路径或 PR 链接，不猜测候选文件。
- `PyYAML` 缺失：提示先安装测试依赖，或直接说明无法运行自动门禁，只能做人工审查。
- PR 无法访问：要求用户补充可访问仓库、diff 或本地分支。
- 候选 skill 需要硬件实测但当前无 NPU：标记为 `dry_run`，只给结构和流程结论，不声称实测通过。
- 自动门禁失败：将 `error` 逐条列为阻塞项，先修阻塞项，不用总分抵消硬错误。
- 资源路径缺失：把缺失的 `references/`、`scripts/`、`assets/` 链接列入必须修复项；无法确认时降级为人工复核。
- 外部命令、未知网络或依赖安装有风险：默认不执行，标记为 `blocked`，要求候选 skill 补充可信来源、最小权限和 fallback。
- 审查脚本超时或异常：重试一次；仍失败时保留 stderr/stdout 摘要，报告标记为 `partial`。

## 示例

审查本地新增 skill：

```bash
python infra/cannbot-skill-reviewer/scripts/review_skill.py infra/cannbot-skill-reviewer
```

用户说：

> 帮我审查这个新 skill：`ops/my-new-skill/SKILL.md`，看能不能提 PR。

应输出阻塞问题、九维评分和最小整改清单；若需要修改，应只改候选 skill 相关文件。

## 参考资料

- [成文法门禁规则](references/statutory-rules.md)
- [判例法设计审查](references/case-law-review.md)
- [CANNBot Skills 治理规范](https://gitcode.com/cann/cannbot-skills/blob/master/docs/GOVERNANCE.md)
- [CANNBot Skills 开发规范](../../docs/STANDARDS.md)
- [测试框架说明](../../tests/README.md)
