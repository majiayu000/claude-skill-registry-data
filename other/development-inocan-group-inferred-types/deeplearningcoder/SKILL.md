---
name: DeepLearningCoder
description: Use this skill in the scenario of deep learning project development.
---

# SKILL: 深度学习编程（Deep Learning Coding）

> 目标：把“研究想法/论文方法/训练需求”稳定地落到**可复现、可调试、可扩展**的深度学习代码与实验结果上。

## 1. 适用范围与不适用范围

### ✅ 适用范围

- PyTorch/Lightning/Accelerate/torchrun 分布式训练脚本与模块化工程结构
- 数据管线：dataset/dataloader/augmentation/cache/mmap/webdataset
- 训练与评估：loss/metric/ema/amp/gradient accumulation/checkpoint
- 模型实现：CNN/Transformer/ViT/UNet/DeepLab/SegFormer/自定义模块
- 实验复现：seed、determinism、日志、配置管理、结果表格与可视化
- 性能与稳定性：显存优化、吞吐优化、deadlock/hang、NaN/Inf 排查

### ❌ 不适用范围

- 需要访问私有数据或无法提供的训练环境（只能给出可迁移的实现/调参建议）
- 需要“保证 SOTA”或“保证某个具体 mIoU/Acc”（可以提供合理预期与实验设计）
- 违反实验伦理/数据合规的请求

---

## 2. 交付物（Outputs）

根据需求输出以下一种或多种：

- 代码片段（可直接粘贴到工程）：model/loss/runner/utils
- 训练脚本结构建议（目录树 + 关键文件职责）
- 配置模板（YAML/TOML/argparse/dataclass）
- Debug 清单（按概率排序，含验证手段）
- 实验计划：对照组、超参表、消融表、记录字段

---

## 3. 输入格式（Inputs）

用户提供越多，产出越精确；缺失时应**做合理默认并显式写出假设**。

**最小输入**（Minimum Viable Spec）：

- 任务：分类/检测/分割/生成/自监督
- 数据：数据集名称或数据格式（文件结构、标注格式）
- 目标：指标（mIoU/Acc/F1/PSNR）、约束（显存/速度/复现）

**推荐输入**（Preferred Spec）：

- 代码仓库结构或关键文件片段
- 训练命令、日志片段（loss 曲线/报错/显存占用）
- 模型与 backbone（如 ViT-B/DeiT-S）、输入分辨率、batch size
- 环境：GPU 型号、CUDA/PyTorch 版本、分布式方式

---

## 4. 工作流程（Agent Workflow）

### Step 0：确认问题类型

- 实现类：需要写模块/替换组件/重构
- 复现类：需要对齐 paper setting/metric/seed
- 调参类：需要诊断瓶颈与优先级
- Debug 类：需要最小复现与二分定位

### Step 1：建立可复现最小闭环

- 固定 seed + deterministic（必要时）
- 记录：config、git hash、数据版本、依赖版本
- 跑通：单卡 1 batch forward/backward

### Step 2：拆解到“可测”的子模块

- 数据 → 模型 → loss → 优化器 → 评估
- 每步给出**单元测试**或 sanity check：shape、范围、梯度、耗时

### Step 3：给出实现与验证

- 代码实现（含注释、类型、边界检查）
- 验证手段：对齐输出分布/数值、对比 baseline、可视化

### Step 4：性能与稳定性优化（可选）

- AMP/GradScaler、grad checkpoint、bf16、fused optimizer
- dataloader：num_workers/pin_memory/persistent_workers/prefetch
- DDP：find_unused_parameters、sync_bn、bucket_cap_mb

---

## 5. 代码风格与工程规范

### 5.1 文件/模块建议

- `configs/`：实验配置
- `datasets/`：数据读取与增强
- `models/`：网络结构
- `losses/`：损失函数
- `engine/`：train/eval loop
- `utils/`：logging、distributed、seed、meters、checkpoint
- `scripts/`：启动脚本（torchrun/srun）

### 5.2 约定（强烈推荐）

- 所有张量标注 shape：`(B, C, H, W)` / `(B, N, D)`
- 函数签名清晰：输入 dtype/device、返回值含 key
- 日志统一：每步记录 `lr/loss/grad_norm/mem/time/metric`

---

## 6. 常见模板

### 6.1 Train Loop 骨架（伪代码）

- 关键点：AMP、梯度累计、EMA、DDP 同步、异常捕获

**必备日志字段**：

- `step/epoch`, `loss_total`, `loss_*`, `lr`, `time_data`, `time_iter`, `max_mem`, `metric_*`

### 6.2 Debug NaN/Inf 清单（按优先级）

1. 学习率过大 / warmup 缺失
2. loss 未归一化（像素数/有效 mask）
3. 混合精度溢出（切换 bf16 或缩小 loss scale）
4. 数据异常（空标注/全 ignore/越界值）
5. log/exp/sqrt 等数值域错误

### 6.3 DDP 卡死（Hang）清单

1. dataloader worker 挂起：`num_workers=0` 验证
2. 不同 rank 走了不同分支：条件语句/early return
3. collectives 不匹配：`all_reduce` 次数不同
4. `find_unused_parameters` 配置错误

---

## 7. 反例（Anti-patterns）

- 只给“把这个模型提到 90%+”而不提供任务/数据/指标
- 只贴报错最后一行，不提供 stack trace 与环境版本
- 训练结果不可复现：未记录 config、seed、数据版本
- 过早做复杂优化：在 baseline 跑通前就改 AMP/DDP/加速

---

## 8. 交互方式（How to Ask Me）

你可以用下面任一模板发给我：

### A. 让我写模块

- 任务：语义分割
- 需求：实现一个 region-consensus loss
- 输入/输出：输入 logits `(B,C,H,W)` 与 mask `(B,H,W)`，输出标量 loss
- 约束：支持 AMP；ignore_index=255

### B. 让我排查 bug

- 环境：PyTorch 2.x + CUDA 12.x + torchrun
- 现象：第 1 个 epoch eval 卡死
- 日志：贴出最后 200 行
- 代码：贴出 evaluate() 与 dataloader 构造

---

## 9. 质量标准（Definition of Done）

- ✅ 能跑通（最小闭环 + 单元 sanity check）
- ✅ 可复现（seed + config + 版本信息）
- ✅ 可定位（遇到异常能快速缩小范围）
- ✅ 可扩展（模块化、易替换、日志完整）
