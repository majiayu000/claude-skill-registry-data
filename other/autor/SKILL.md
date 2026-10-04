---
name: autor
description: AutoR — human-centered 研究执行框架。8阶段 pipeline，产出可复现 artifact。
trigger: ["autor", "研究执行", "研究 harness", "research run", "论文 pipeline", "可复现研究"]
---

# AutoR

仓库路径: `~/repos/AutoR`

## 定位

AI 负责执行，人类负责方向。不是一键出论文的黑盒，是结构化研究 harness。

## 架构

底层执行器: `claude` / `codex`
8 阶段 pipeline:
01 文献综述 → 02 假设生成 → 03 研究设计 → 04 实现 → 05 实验 → 06 分析 → 07 写作 → 08 发布

产出目录: `runs/<run_id>/` (prompt、日志、代码、数据、图、LaTeX、PDF)

## 常用命令

```bash
# 新 run
cd ~/repos/AutoR && python main.py --goal "研究目标"

# 指定执行器
python main.py --goal "..." --operator claude   # 默认
python main.py --goal "..." --operator codex

# 全自动模式（reviewer agent 代替人工审批）
python main.py --goal "..." --full-auto

# 从已有项目起步
python main.py --goal "..." --project-root /path/to/project

# 从论文语料起步
python main.py --goal "..." --paper-corpus /path/to/papers

# 恢复 run
python main.py --resume-run <run_id>
python main.py --resume-run latest

# 从某 stage 重做
python main.py --resume-run <run_id> --redo-stage 06_analysis

# 回滚 stage（下游全部失效）
python main.py --resume-run <run_id> --rollback-stage 04_implementation

# 指定投稿 venue
python main.py --goal "..." --venue neurips_2025  # 默认
python main.py --goal "..." --venue nature
python main.py --goal "..." --venue jmlr

# 带资源
python main.py --goal "..." --resources paper.pdf data/ code/

# 跳过 intake
python main.py --goal "..." --skip-intake

# 生成方法示意图（需 google-genai + Pillow）
python main.py --goal "..." --research-diagram
```

## 核心原则

1. **Human approval by default** — 每个 stage 结束等你审阅
2. **--full-auto** 可跳过人工，但建议前几个 run 先手动审批
3. **runs/ 目录**是唯一产物 — 所有中间结果都在里面
4. **可恢复** — 随时 resume、redo、rollback

## 适用场景

- 从 arXiv 论文出发，完整复现+扩展
- 从代码仓库出发，补全实验+写论文
- 从研究问题出发，走完 literature → experiment → writing 全流程
- 需要可复现、可审计的研究产物

## 与 Hermes 现有技能的关系

- paper2code: 单篇论文 → 最小代码。AutoR 是更完整的 8 阶段 pipeline
- gap-driven-paper-pipeline: gap → 多篇论文 → 批量代码。AutoR 走更深的实验+写作
- 适用: 需要完整论文产出、需要实验验证、需要投稿格式化时

## 注意

- 不需要 pip install，纯 Python stdlib 运行
- 需要已安装 `claude` 或 `codex`
- Stage 07 写作产出 LaTeX，有 TeX 环境可直接编译 PDF
- 默认 venue: neurips_2025
