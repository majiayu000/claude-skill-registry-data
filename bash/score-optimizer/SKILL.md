---
name: score-optimizer
description: Use when the user wants to iterate on a viral-article scoring system itself, calibrate or improve a scoring prompt against labeled samples, or run batch scoring experiments on a fixed article set. Best for prompt-only scoring research where the evaluator scripts stay fixed and only the scoring rubric/prompt is meant to evolve.
---

# Score Optimizer

这个 skill 只负责一件事：优化文章评分系统本身。

它适合做的是：

- 调整文章爆款评分 Prompt
- 批量给样本文集打分
- 对照标注数据评估评分准确度
- 研究评分维度、权重、few-shot 示例是否更合理

它不负责：

- 直接改文章正文
- 平台改写
- 发布包装

## Working Scope

适用场景：

- 用户说“优化文章评分 prompt”
- 用户说“让这个爆款评分系统更准”
- 用户说“跑一轮样本文集评分实验”
- 用户说“校准 viral score / composite score 的打分规则”

不适用场景：

- 用户说“直接把这篇文章改高分”
- 用户说“按这个评分器去优化文章内容”

后者应改用 `article-optimizer`。

## Required Reads

开始前先读：

1. [references/score_program.md](references/score_program.md)
2. [references/score_prompt.md](references/score_prompt.md)

需要看实现时再读：

- [scripts/run_scoring.py](scripts/run_scoring.py)
- [scripts/evaluate.py](scripts/evaluate.py)
- [assets/articles/labels.example.json](assets/articles/labels.example.json) —— 标注 schema 示例

样本文集位置（**用户自己提供**，本 skill 不带样本）：

- `assets/articles/samples/` —— 把你自己标注过的 .md 文章放进来,然后 `cp labels.example.json labels.json` 填上你的评分。详见 [assets/articles/samples/README.md](assets/articles/samples/README.md)

## Workflow

1. 先确认当前任务是在优化评分器，不是在改文章。
2. 读取 `references/score_program.md`，按它的实验约束执行。
3. 默认只改 `references/score_prompt.md`，不要动评估脚本。
4. 运行批量评分脚本，再运行评估脚本。
5. 比较 `composite_score`、`mae`、`spearman`、`classification`。
6. 记录结果，决定保留还是回滚。

## Commands

在 skill 根目录执行：

```bash
python3 scripts/run_scoring.py > scoring.log 2>&1
python3 scripts/evaluate.py > eval.log 2>&1
grep "^composite_score:\|^mae:\|^spearman:\|^classification:" eval.log
```

如果需要图表：

```bash
python3 scripts/generate_score_chart.py
```

## Guardrails

- 默认不要改 `scripts/evaluate.py`
- 默认不要改 `scripts/run_scoring.py`
- 默认不要安装新依赖
- 如果只是想提高某一篇文章分数，不要用这个 skill
