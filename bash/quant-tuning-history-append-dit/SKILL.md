---
name: quant-tuning-history-append-dit
description: Append a DiT-tuning round to history.yaml. DiT-side counterpart of the LLM-path accuracy_append.py; records practice.md5, inference_outputs, fp_baseline_outputs, and the scoring fields (scores / overall_score / loss_vs_baseline / is_satisfied) populated by quant-tuning-score-dit. Idempotent on practice_id.
license: Apache-2.0
metadata:
  version: 0.1.0
  domain: quantization
  framework: msmodelslim
  protocol: script
  skill_class: tool
  gating:
    model_family: dit
  aliases:
    - dit-history-append
  keywords:
    - history.yaml
    - inference_outputs
    - practice_id
---

# Skill: DiT 调优历史追加

## 1. 概述

每轮 DiT 调优结束后，orchestrator 调用本 Skill 把本轮记录追加到 `{workdir}/history/history.yaml`。

## 2. 适用与不适用

- **适用**：`model_family=dit` 调优回路；每轮 inference 跑完即追加
- **不适用**：
  - LLM/VLM 路径（用既有 `accuracy_append.py`）
  - 评分字段本身由 `quant-tuning-score-dit` 填充；本 skill 仅负责把这些字段透传到 `history.yaml`（若 `quant-tuning-score-dit` 未触发则保持 `null`）

## 3. 协作关系

```
quant-tuning-evaluate DiT 扩展节 (产出 infer_outputs/round_N/...)
   │
   ▼
quant-tuning-history-append-dit (本 skill)
   │  scripts/append.py
   ▼
{workdir}/history/history.yaml  ←  dit_records 段
```

## 4. 输入参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `history_path` | str | ✅ | `{workdir}/history/history.yaml` |
| `practice_id` | str | ✅ | 唯一 ID（如 `dit-round-2`） |
| `practice_path` | str | ✅ | `{workdir}/round_{N}/practice.yaml`（自动算 md5） |
| `inference_outputs` | list | ✅ | 本轮推理产物路径列表 |
| `fp_baseline_outputs` | list | ⛏️ | FP baseline 产物路径（`quant-tuning-evaluate` DiT 扩展节跑 FP baseline 模式时填） |
| `scores` | object | ⛏️ | 每维度 score dict；来自 `quant-tuning-score-dit` 的 `scores` 字段 |
| `overall_score` | float | ⛏️ | 加权总分；来自 `quant-tuning-score-dit` 的 `overall_score` 字段 |
| `loss_vs_baseline` | float | ⛏️ | 量化 vs FP 的 overall 差；启用 `--baseline-outputs` 时存在 |
| `is_satisfied` | bool | ⛏️ | `loss_vs_baseline >= -tolerance`；orchestrator 据此决定是否退出回路 |
| `append_as` | str | | YAML 段名，默认 `dit_records` |

## 5. 工作流

```
┌──────────────────────────────────────┐
│ 1. 入参校验                            │
│ - history_path / practice_path 存在   │
│ - inference_outputs 非空             │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────�
│ 2. 计算 practice.yaml md5            │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│ 3. 读现有 history.yaml（若有）         │
│ - 找 dit_records 段                   │
│ - 按 practice_id upsert（替换/追加）  │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│ 4. 写回 history.yaml（保留 LLM 记录） │
└──────────────────────────────────────┘
```

## 6. CLI 调用

```bash
python msagent/skills/quantizer/quant-tuning-history-append-dit/scripts/append.py \
    --history-path output/wan22-t2v-a14b-w8a8/history/history.yaml \
    --practice-id dit-round-2 \
    --practice-path output/wan22-t2v-a14b-w8a8/round_2/practice.yaml \
    --inference-outputs \
        "output/wan22-t2v-a14b-w8a8/infer_outputs/round_2/overall_consistency/0000.mp4,output/wan22-t2v-a14b-w8a8/infer_outputs/round_2/subject_consistency/0001.mp4"
```

## 7. 输出结果

```msagent-io v1
{
  "protocol": "msagent.subagent_io",
  "subagent_type": "quant-tuning-history-append-dit",
  "status": "ok",
  "output": {
    "ok": true,
    "record": {
      "practice_id": "dit-round-2",
      "quant_config_md5": "44c42e68...",
      "time": "2026-08-08 12:34:56",
      "practice_path": "/abs/path/to/round_2/practice.yaml",
      "inference_outputs": [
        "/abs/path/to/infer_outputs/round_2/overall_consistency/0000.mp4",
        "/abs/path/to/infer_outputs/round_2/subject_consistency/0001.mp4"
      ],
      "fp_baseline_outputs": null,
      "scores": null,
      "overall_score": null,
      "loss_vs_baseline": null,
      "is_satisfied": null
    }
  }
}
```

## 8. 错误处理

| 错误 | 处理 |
|---|---|
| `history_path parent not writable` | 立即中止 |
| `practice_path not found` | 立即中止 |
| `inference_outputs 为空` | 立即中止（防止无效 history 记录） |
| YAML 解析失败 | 报 stderr 摘要，立即中止 |

## 9. 约束

- **幂等**：同一 `practice_id` 重复调用覆盖旧记录而非重复追加
- **不破坏 LLM 记录**：仅在 `dit_records` 段追加，与 LLM `records` 段平行
- **不修改既有字段名**：`practice_id` / `quant_config_md5` / `time` 与既有 LLM schema 对齐
- **错误即停**

## 10. 参考

- 输出规范：[output_format.md §3](../../quantization-accuracy-tuning-orchestrator/references/output_format.md)
- 既有 LLM：[quantization-accuracy-tuning-orchestrator/scripts/accuracy_append.py](../../quantization-accuracy-tuning-orchestrator/scripts/accuracy_append.py)
- YAML 工具：[quantization-expert-experience-tuning-rules/scripts/yaml_utils.py](../../quantization-expert-experience-tuning-rules/scripts/yaml_utils.py)
