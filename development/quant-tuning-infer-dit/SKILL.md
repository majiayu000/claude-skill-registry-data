---
name: quant-tuning-infer-dit
description: 在 W8A8 动态量化后，用 MindIE-SD 冒烟测试 DiT 量化权重是否可加载（可选 skill）。与 `quant-tuning-evaluate`（DiT 扩展节）的区别：本 skill 仅做"能跑通 + 权重可用"的轻量验证（4~16 条 prompt，几分钟出结果），不算分；后者产出视频集交 `quant-tuning-score-dit`（AISBench-VBench 16 维度）评分，是调优回路一环。不引入 vLLM-Ascend、不做精度指标评估（FID/CLIP-score 等）。
license: Apache-2.0
metadata:
  version: 0.1.0
  domain: quantization
  framework: msmodelslim
  protocol: cli
  skill_class: tool
  aliases:
    - dit-infer
    - diffusion-verify
  trigger_intents:
    - 量化后推理验证
    - DiT 推理验证
  keywords:
    - mindie-sd
    - diffusers
    - flux pipeline
    - sd3 pipeline
    - w8a8 inference
---

# Skill: DiT 量化后推理验证（可选）

## 适用与不适用

- **适用**：已经 `quant-tuning-quantize-dit` 产出量化权重，需验证"能跑通 + 权重可用"。
- **不适用**：
  - 精度指标评估（FID/CLIP-score 等；本 skill 不计算）
  - 服务化推理（不引入 vLLM-Ascend / Tritonserver 等后端）
  - LLM/VLM 推理验证（走对应 LLM/VLM 子 skill）

## 协作关系

```
quantization-accuracy-tuning-orchestrator (workflow)
        │  按 model_family 路由到 dit 分支
        ▼ 调用（可选）
quant-tuning-infer-dit (tool)
        │
        ▼ 后端
  MindIE-SD
        │
        ▼ 输出
  {workdir}/infer_outputs/
```

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `quantized_path` | string | ✅ | `quant-tuning-quantize-dit` 产出路径（MindIE-SD 格式；对应其 output 字段 `quantized_path`） |
| `prompt_list` | string[] | ✅ | 文本 prompt 列表；建议 4~16 条 |
| `num_inference_steps` | int | | 字段名 / 默认值按目标 DiT 推理仓差异较大；详见 [`inference_config_field_map.md`](../msmodelslim-model-adapt/references/dit/inference_config_field_map.md) §2 默认值表。 |
| `guidance_scale` | float | | 同上；FLUX 字段同名 `guidance_scale`，HunyuanVideo / Wan 系字段名不同，详见字段表 §1。 |
| `output_dir` | string | ✅ | 推理产物目录；推荐 `{workdir}/infer_outputs/` |
| `inference_repo` | string | ✅ | 推理仓路径（pipeline 所在） |
| `model_family` | string | ✅ | `dit` |

## 推理后端

| 后端 | 说明 |
|------|------|
| **MindIE-SD** | NPU 上跑 MindIE-SD；适用 HunyuanVideo、Wan2.2-T2V/I2V/TI2V、FLUX.1-dev（已迁移）、Wan2.1、Sana、SD3、SD1.5/SDXL 等 |

- **不依赖 vLLM-Ascend**：MindIE-SD 单次调用即可
- **不在本阶段做服务化**：单次调用，不引入额外后端

## 工作流

```
┌───────────────────────────┐
│ 1. 入参校验                │
│ - quantized_path          │
│ - prompt_list 非空         │
└──────────┬────────────────┘
           ▼
┌───────────────────────────┐
│ 2. 加载 MindIE-SD 后端     │
└──────────┬────────────────┘
           ▼
┌───────────────────────────┐
│ 3. 加载量化 DiT pipeline  │
│ - 替换 transformer 为      │
│   量化版本                 │
└──────────┬────────────────┘
           ▼
┌───────────────────────────┐
│ 4. 逐 prompt 生成          │
│ - num_inference_steps     │
│ - guidance_scale          │
└──────────┬────────────────┘
           ▼
┌───────────────────────────┐
│ 5. 保存到 output_dir      │
│ - {idx:04d}.png           │
│ - 记录耗时                 │
└──────────┬────────────────┘
           ▼
┌───────────────────────────┐
│ 6. 汇总                    │
│ status=ok                 │
│ 成功数/总请求数             │
│ 平均推理耗时                │
└───────────────────────────┘
```

## 输出结果

### 成功

```msagent-io v1
{
  "protocol": "msagent.subagent_io",
  "subagent_type": "quant-tuning-infer-dit",
  "status": "ok",
  "output": {
    "status": "ok",
    "backend": "mindie-sd",
    "output_dir": "<workdir>/infer_outputs/",
    "success_count": 8,
    "total_count": 8,
    "avg_inference_sec": 12.3,
    "generated_files": [
      "<workdir>/infer_outputs/0000.png",
      "<workdir>/infer_outputs/0001.png"
    ],
    "commands": [
      {"name": "load_pipeline", "command": "MindIE-SD pipeline 加载"},
      {"name": "inference", "command": "pipeline(prompt=...).images[0]"}
    ]
  }
}
```

### 失败

立即中止，回传：

```msagent-io v1
{
  "protocol": "msagent.subagent_io",
  "subagent_type": "quant-tuning-infer-dit",
  "status": "failed",
  "error": {
    "code": "INFERENCE_ERROR",
    "message": "OOM / NaN / pipeline 加载失败摘要",
    "suggestion": "OOM / NaN → 减小 num_inference_steps 或换设备；pipeline 加载失败 → 检查 quantized_path 是否 MindIE-SD 格式；报 stderr 摘要，等待 orchestrator 决策"
  }
}
```

## 错误处理

| 错误类型 | 处理 |
|----------|------|
| `quantized_path` 不存在 | 立即中止，提示用户先跑 `quant-tuning-quantize-dit` |
| MindIE-SD pipeline 加载失败 | 检查 `quantized_path` 中是否含 MindIE-SD 格式 |
| OOM / NaN | 减小 `num_inference_steps` 或换设备；本 skill 不重试 |
| prompt list 为空 | 立即中止 |

## 约束

- **MindIE-SD only**：禁止引入 vLLM-Ascend / Tritonserver 等后端
- **不做精度指标评估**：本 skill 仅验证"能跑通 + 权重可用"
- **不引入服务化**：单次调用，避免重复拉起服务
- **不修改 LLM/VLM skill 既有行为字段**

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `transformer not found in <quantized_path>` | 量化权重目录结构与 diffusers 不一致 | 检查 `quant-tuning-quantize-dit` save_path |
| `NaN detected in latents` | 量化精度不足 | 回退到 `quant-tuning-quantize-dit` 检查 exclude 列表 |
| `OOM` | 设备内存不足 | 减小 `num_inference_steps` 或换设备 |

## 检查清单

- [ ] `quantized_path` 含 MindIE-SD 格式
- [ ] `prompt_list` 非空
- [ ] 推理参数按目标 DiT 推理仓的 `parse_args` 设置；详见 [`inference_config_field_map.md` §2 默认值](../msmodelslim-model-adapt/references/dit/inference_config_field_map.md)
- [ ] NPU/GPU 设备可用
- [ ] MindIE-SD 已安装

## 参考

- [推理配置 YAML 示例](assets/inference.example.yaml)
- [量化产物路径示例](../quant-tuning-quantize-dit/assets/w8a8_dynamic.example.yaml)