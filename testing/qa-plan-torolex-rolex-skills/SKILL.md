---
name: qa-plan
description: 根据最近一批 commit 生成 step-by-step QA 测试计划，并保存为 GitHub issue。用户通过 /qa-plan 调用。
disable-model-invocation: true
---

# QA Plan

审查最近 N 个 commit，生成一份可照做的 QA 测试计划，保存为 GitHub issue（`qa-plan` 标签）。

## 参数

- 用户传入数字时，按该数字取最近 N 个 commit；否则默认取**上一个 tag 以来的改动**。

## 流程

### 1. 收集变更

默认取上一个 tag 以来的范围：

```bash
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -n "$LATEST_TAG" ]; then
  git log --oneline "$LATEST_TAG"..HEAD
  git diff "$LATEST_TAG"..HEAD
else
  echo "未找到 tag，回退到最近 10 个 commit"
  git log --oneline -10
  git diff HEAD~10..HEAD
fi
```

用户传入 N 时（例如 `/qa-plan 5`）：

```bash
N=5  # 用户指定的数字
git log --oneline -"$N"
git diff HEAD~"$N"..HEAD
```

完成标准：已拿到 commit 列表和完整 diff。

### 2. 理解变更

阅读 diff，必要时查看相关源文件。按**用户可感知的功能/场景**分组，不按 commit 顺序排列。

完成标准：能列出每个变更能力及其代码路径，且每个变更能力至少对应一个测试步骤。

### 3. 起草 QA 计划

使用 Markdown checklist，每个步骤包含：

| 字段 | 说明 |
|------|------|
| 测试什么 | 要验证的功能或行为 |
| 如何测试 | 测试者执行的具体操作 |
| 预期结果 | 正确行为是什么 |
| 优先级 | P0（核心）/ P1（重要边界）/ P2（锦上添花） |

完整示例见 [EXAMPLES.md](EXAMPLES.md)。

完成标准：每个变更能力至少有一个步骤；每个步骤的四项字段都已填满。

### 4. 发布 GitHub issue

先检查 `gh` 登录状态：

```bash
gh auth status
```

未登录则停止，请用户运行 `gh auth login`。

将 QA 计划写入临时文件，然后创建 issue：

```bash
gh label create qa-plan --description "QA test plans" --color 0366D6 2>/dev/null || true
gh issue create \
  --title "QA Plan: $(date +%Y-%m-%d) — 变更简述" \
  --label qa-plan \
  --body-file /tmp/qa-plan-body.md
```

完成标准：成功返回 issue URL。

### 5. 汇报

向用户输出：

- GitHub issue 链接
- 步骤统计（P0 X 项 / P1 Y 项 / P2 Z 项）
- 建议重点关注的变更或高风险区域
