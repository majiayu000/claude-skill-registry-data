---
name: science-reproducibility
description: Use before reporting any experiment result, when a result cannot be re-run, when writing the methods section, or when preparing a reproducibility package; covers run provenance, environment capture, seed handling, artifact hashing, and the clean-room re-run check.
---

# 可复现性（运行留痕与干净重跑）

## 何时用
- 每次要对外报告一个实验结论之前；
- 方法学部分动笔之前（先把该记的记下来）；
- 有人质疑结果、或自己发现两次运行不一致时。

## 前置检查
1. 项目是否已 `science_project_open`（没有 project_id 的运行记录没有归属）；
2. 实验计划是否已 `science_exp_plan`（预注册式：假设、变量、n、分析计划、风险）；
3. 工作目录是否在 git 仓库内（能拿到 commit 才能谈复现）。

## 步骤
1. **固定环境**：记录解释器版本、关键依赖版本（`pip freeze` / `renv.lock` / `package-lock.json`）并算一个依赖哈希；不要只写"用了 pandas"。
2. **固定随机性**：所有随机源显式 seed（Python `random`、`numpy`、框架各自 seed、DataLoader worker seed）；记录 seed 值。
3. **固定输入**：输入数据算 sha256；外部数据写来源 + 拉取日期 + 许可。
4. **一次运行一条记录**：`science_exp_run` 记 command / cwd / env / seed / commit / 输入输出哈希 / exit_code / 起止时间。日志保留路径，不要只截屏。
5. **产物哈希**：模型文件、图表、结果表都算哈希；同一脚本两次运行哈希不同就要解释（时间戳、浮点非确定性、并发顺序）。
6. **干净重跑**：`science_repro_check` 在空目录里重跑，比对产物哈希与关键指标；不一致就列差异（数值容差、字段缺失、顺序变化）。
7. **写清单**：`science_provenance` 生成 manifest（代码 / 数据 / 环境 / seed / 许可 / 硬件），随稿件一起交付。

## 产出与落库
- `run` 表：command / env_json / seed / commit / dep_hash / inputs_json / outputs_json / exit_code
- `analysis` 表：检验、统计量、效应量、CI、p、校正方法、前提检查
- manifest.json：可复现包清单

## 常见失败与降级
- **拿不到 commit**（不在 git 里）：至少对脚本目录做哈希快照，并在报告里标注"无版本控制"。
- **环境无法重建**（老 CUDA / 私有镜像）：记录到能重建的最小描述 + 已知偏差，明确写"环境不可完全重建"。
- **结果对 seed 敏感**：报告多 seed 的均值与区间，不要只报最好那一次。
- **硬件差异**（GPU 非确定性）：开启确定性模式（如 `torch.use_deterministic_algorithms`）或声明容差。
