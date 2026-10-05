---
name: article-optimizer
description: Use when the user wants to improve a specific article under a fixed viral-scoring rubric, iterate on one article to raise its score, or run single-article scoring plus rewrite loops. Best for content optimization experiments where the scoring prompt stays fixed and the article text is the thing being changed.
---

# Article Optimizer

这个 skill 只负责一件事：在固定评分器下优化一篇具体文章。

它适合做的是：

- 给单篇文章打分
- 根据评分返回的改进建议改稿
- 做多轮版本迭代
- 对比不同版本的 viral score

它不负责：

- 调整评分器本身
- 校准整套评分系统
- 批量样本评估

如果目标是改评分 Prompt，而不是改文章，应该改用 `score-optimizer`。

## Working Scope

适用场景：

- 用户说“把这篇文章优化到更高分”
- 用户说“按固定评分规则改稿”
- 用户说“给单篇文章打分并根据建议改写”
- 用户说“跑 single article optimization loop”

不适用场景：

- 用户说“让这套评分系统更准”
- 用户说“批量评估一组样本文章”

## Required Reads

开始前先读：

1. [references/optimize_program.md](references/optimize_program.md)
2. [references/score_prompt.md](references/score_prompt.md)

需要看实现时再读：

- [scripts/run_single_score.py](scripts/run_single_score.py)
- [scripts/generate_optimize_chart.py](scripts/generate_optimize_chart.py)

## Workflow

1. 先确认当前任务是在改文章，不是在改评分器。
2. 读取 `references/optimize_program.md`，确认实验约束。
3. 确认目标文章路径。
4. 用单篇打分脚本跑出基线分数和改进建议。
5. 每轮只改文章，不动评分规则。
6. 保存迭代版本，再重新打分比较。

## Commands

在 skill 根目录执行：

```bash
python3 scripts/run_single_score.py <article_path>
```

如果需要图表：

```bash
python3 scripts/generate_optimize_chart.py
```

## Guardrails

- 默认不要改 `references/score_prompt.md`
- 默认不要改 `scripts/run_single_score.py`
- 每轮优先只改文章内容
- 如果用户要的是“训练裁判”，不要用这个 skill
