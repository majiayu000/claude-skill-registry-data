---
name: ai-ml-engineering
description: AI/机器学习工程全流程技能。覆盖GPU加速（RAPIDS/CuPy/Numba/CUDA kernel调优）、scikit-learn经典ML、SHAP模型解释、特征工程与数据泄漏防护、时序验证、PyTorch Lightning分布式训练、强化学习（Stable-Baselines3）、TimesFM零样本预测、EDA数据体检、pymoo多目标优化。触发词：机器学习、深度学习、GPU加速、CUDA、kernel调优、模型训练、特征工程、数据泄漏、模型解释、SHAP、sklearn、交叉验证、分布式训练、强化学习、时序预测、机器学习工程, machine learning, GPU acceleration, CUDA kernel, feature engineering, data leakage, SHAP, scikit-learn, cross validation, distributed training, PyTorch Lightning, reinforcement learning, time series forecasting, TimesFM, EDA, optimization。用于：加速数据管线、训练/调参/解释模型、检测特征泄漏、配置分布式训练、编写CUDA kernel等场景。
metadata:
  agent_created: true
---

# AI/ML Engineering（机器学习工程）

从数据体检到 GPU 调优的 ML 全流程。核心立场：**先 profile 再优化、先防泄漏再谈指标**；结论按证据分级（已确认 / 工程推论 / 估算 / 待验证 / 数据不足）。

## 症状 → 加载哪个 reference

| 症状 / 任务 | 加载 |
|---|---|
| NumPy/pandas/sklearn 太慢；要写/调 CUDA kernel；GPU 相关报错 | `references/gpu-acceleration.md` |
| 训练分类/回归模型；调参；解释预测（SHAP） | `references/classical-ml.md` |
| 做时序/金融特征；指标好得离谱（>70% 准确率）；怀疑泄漏 | `references/timeseries-leakage.md` |
| 分布式训练；RL 智能体；TimesFM 预测；训练报错 | `references/deep-learning.md` |
| 拿到新数据集不知从何下手；数据脏/缺失/分布可疑 | `references/eda-data-quality.md` |

## 工作流（默认顺序）

1. **EDA 体检**：缺失、分布、泄漏红旗，输出数据质量报告（不动原始数据）。
2. **基线**：最简单能跑通的 Pipeline 先跑通，任何复杂度提升都要跟它比。
3. **特征/模型**：预处理放 Pipeline 内逐折拟合；时序数据按时间切分 + embargo。
4. **验证**：嵌套 CV；指标与基线和"随机猜测"双对照。
5. **解释**：SHAP 做 additivity 校验后再出图。
6. **优化**：需要速度时先测 GPU 适用性（≥10K 元素、高并行、显存放得下）。

## 铁律

**MUST**
- 先 profile 再优化（`ncu --set full` / `cupyx.profiler.benchmark()`），禁止凭猜测优化。
- sklearn 预处理放进 Pipeline、每折内重拟合；分类切分必加 `stratify=y`。
- SHAP 解释前做 additivity 校验（`base_values + values.sum(axis=1)` 对比模型输出）。
- TimesFM：先跑 `check_system.py`，先 `compile()` 再 `forecast()`；SB3：训练前必跑 `check_env()`。
- Lightning 多卡指标日志加 `sync_dist=True`，`training_step` 必须返回 loss。
- GPU 浮点结果用容差比较，不做逐位比较。

**NOT**
- 禁止对时序数据做随机 CV 或全样本统计（lookahead）。
- 禁止在 GPU 上用 float64（消费卡吞吐仅 float32 的 1/32），累加器保持 FP32。
- 每个 CUDA kernel 无 `if i < size` 越界守卫不得提交。
- 禁止加载不可信的 pickle/joblib 模型文件（反序列化即代码执行）。
- 禁止在 EDA 阶段自动删除离群值/插补/改写原始数据；缺失 ≠ 0，ND ≠ LOQ。
- 禁止对已归档/停止维护的库用于新项目（cuSpatial、cuxfilter）。

## 参考索引

每个 reference 按"第一步→判据→如何证明根因"组织。GPU 库映射表与零改码加速入口在 `gpu-acceleration.md` 开头。

