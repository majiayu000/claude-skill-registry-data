---
name: qa-audit
description: QA 审计 — 跑全量文档质量检查,按 P0/P1/P2 严重度分级输出审计报告。设计完成、代码交接前调用本 skill,作为进入实施的最后一道硬门控,确保 P0=0 才放行。
disable-model-invocation: true
version: 4.0.0
requires: [stage-gate, sql-dialect-discipline, doc-numbering]

---

# QA-Audit — 文档质量审计

## Contract

- 输入: 已完成的 01-09 编号文档,项目配置文件,知识库 / 合规 / 技术栈指针
- 输出: `09-QA审计报告.md`
- 门控: `python3 scripts/full-qa-audit.py <project>` 返回 P0=0;整改循环闭环;用户签字
- Required rules: `stage-gate`, `no-field-guessing`, `no-self-invent`, `sql-dialect`, `doc-numbering`, `goal-boundary`
- Required paths: `knowledge-path`, `tech-stack-path`, `compliance-path`, `doc-naming-path`
- 下一步: `/handoff`

## 适用场景

- dev-design 全部产出已签字
- 设计回测已通过
- 进入代码交接前的最后一道闸

## 流程步骤

### 1. 跑全量审计

```bash
python3 <SKILL_ROOT>/analysis-to-delivery/scripts/full-qa-audit.py <项目目录>
```

### 2. 审计维度(6 大类)

| # | 维度 | 工具 |
|---|---|---|
| 1 | 文档格式(frontmatter / H1 / 章节 / 链接 / 占位符) | `doc-validate.py` |
| 2 | 文档编号冲突 | `full-qa-audit.py` |
| 3 | 核心文档完整性(01/05/07 必备) | `full-qa-audit.py` |
| 4 | SQL 方言一致性 | `sql-dialect-check.py` |
| 5 | 字段映射一致性 | `field-alignment-check.py` |
| 6 | 删除/修改的精度 | 人工 + `field-alignment-check.py` |

### 3. 分级处理

| 等级 | 含义 | 处理方式 |
|---|---|---|
| P0 | 致命:导致交接后开发返工 | **必须修复** |
| P1 | 重要:影响开发效率 | 建议修复 |
| P2 | 提示:锦上添花 | 可选 |

### 4. 修复迭代

1. 首次失败 → 读错误输出 → 定位问题文件/行号 → 修复 → 重新跑
2. 二次失败 → 扩大搜索范围,检查关联文件 → 修复 → 重新跑
3. 三次失败 → 停止自动修复,输出完整错误报告,等用户决策

### 5. 写审计报告

输出 `09-QA审计报告.md`:

```markdown
# QA 审计报告:{项目名}

> 审计时间:{日期}
> 审计人:{name}

## 审计概览

- 文档总数:{N}
- P0:{N}  ❌ 必须修复
- P1:{N}  ⚠️ 建议修复
- P2:{N}  💡 可选

## 6 大类审计结果

### 1. 文档格式
✅/⚠️/❌

### 2. 文档编号
✅/⚠️/❌

### 3. 核心文档完整性
✅/⚠️/❌

### 4. SQL 方言
✅/⚠️/❌

### 5. 字段映射
✅/⚠️/❌

### 6. 删除/修改精度
✅/⚠️/❌

## P0 问题清单

| 文件 | 行号 | 问题 | 修复方案 |
|---|---|---|---|
| | | | |

## 修复完成确认

- [ ] P0 全部修复
- [ ] 重新跑审计,P0=0
- [ ] 用户签字进入 `/handoff`
```

## 调用的 rule

- `rules/stage-gate` — 阶段 8 门控
- `rules/sql-dialect` — SQL 方言
- `rules/doc-numbering` — 文档编号

## 结束条件

- [ ] 6 大类审计全部跑过
- [ ] P0=0
- [ ] 审计报告签字(用户 + 接收方)

## 反模式

- ❌ P0 不修复就交付 — P0 必须=0 才能签字进入交接
- ❌ 只查 1 类(只查文档/只查代码) — 必须 6 大类(文档/流程/字段/合规/代码/性能)全跑
- ❌ 审计结果"看起来 OK" — 必须有证据(具体文件 + 行号 + 引用规范)
- ❌ 不分 P0/P1/P2 — 必须按严重程度分级,否则后续修复无法排期
- ❌ 跳过代码 vs 设计对比 — 必须检查"代码实现是否偏离设计"
- ❌ 审计报告无签字栏 — 必须含用户 + 接收方两栏(参考 rules/stage-gate.md 第 8 门)
- [ ] 进入 `/handoff`
