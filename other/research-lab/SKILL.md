---
name: research-lab
description: |
  使用独立 Research Core 把模型比较、软件评估或其他可证伪问题转化为可恢复、可复现、证据可追溯的研究。
  仅用于需要真实执行对照实验的场景：模型/方案/系统的实证对比、基线比较、模型替代评估、消融、盲评、可复现实验。
  不用于简单事实查询、只读审计/盘点/调查（即使涉及"证据"）、无需实验的低风险判断，或用户只要求普通文案/解释的场景。
---

# Research Lab

## 目标

Research Skill 是独立 Research Runtime 的使用协议，不是研究系统本体。它负责识别研究任务、约束研究设计、调用稳定 `research_` 前缀工具，并依据 Evidence 返回结论；实验、统计、Workspace、同步和恢复由 Research Core 负责。

## 触发门禁

满足任一条件时使用：

- 用户要求比较模型、方案或系统，且需要质量、成本或延迟证据。
- 用户提出“能否替代”“是否显著更好”“哪个更可靠”等可证伪问题。
- 结论依赖数据集、Baseline、重复运行、盲评、消融或环境记录。
- 用户要求恢复、复现、审计或跨设备继续既有 Research。

不要用于简单事实查询、单一确定答案、无需实证的文案建议或低成本可逆选择。

## 硬规则

1. 不得从用户问题直接跳到结论；先建立或验证 ResearchSpec。
2. Spec 至少明确 question、hypotheses、单个 `baseline`、`candidates`、dataset/cases、metrics、decision rules 和 adapters；执行字段以当前 `research validate` 为准。
3. 不具备所需模型、数据或执行能力时返回 `UNSUPPORTED`，不得模拟实验结果。
4. Spec 或执行过程无效时返回 `INVALID`；有效实验但证据不足时返回 `INCONCLUSIVE`。
5. 结论必须引用 Evidence、Run 和 Artifact digest；不能只复述模型输出。
6. 不把 API key、token、私钥、绝对用户路径或 credential value 放入 Spec、Workspace、CAS 或工具参数；只使用设备本地配置或 credential reference。
7. 多设备 revision 冲突必须显式呈现，禁止静默选择最后写入版本。

## 标准流程

1. **识别任务**：把问题改写成可证伪 question；明确候选方案与 Baseline。
2. **建立 Spec**：若用户已有 Spec，调用 `research_validate`；否则生成便携 JSON 文件后调用 `research_create`。
3. **执行前检查**：用 `research_inspect` 检查 revision、数据集、Adapter 和决策阈值。缺关键条件时停止执行并返回结构化缺口。
4. **执行或恢复**：调用 `research_execute`。已有 run 时传入 run id；中断后调用 `research_continue`，不要创建重复研究冒充恢复。
5. **检查状态**：用 `research_status` 查看已完成/失败/待执行项，不进行热轮询；等待真实执行反馈。
6. **比较与证据**：调用 `research_compare`，再用 `research_evidence` 获取支撑与限制。
7. **返回结论**：只使用 Runtime 的 Decision 枚举：`SUPPORTED`、`REJECTED`、`INCONCLUSIVE`、`UNSUPPORTED`、`INVALID`。

## LLM 对比最小 Spec

```json
{
  "protocolVersion": "1.0",
  "researchId": "model-replacement-evaluation",
  "question": "Candidate 是否可替代 Baseline 完成指定任务？",
  "taskType": "llm-comparison",
  "hypotheses": [{"id": "h1", "statement": "candidate 质量不低于 baseline 且成本更低"}],
  "baseline": {"id": "baseline", "adapter": "command"},
  "candidates": [{"id": "candidate", "adapter": "command"}],
  "dataset": {
    "cases": [{"id": "case-1", "input": "...", "expected": "..."}]
  },
  "metrics": ["exact_match", "latency_ms", "cost"],
  "decisionRules": {
    "minDelta": 0.0,
    "preferred": "candidate"
  },
  "adapters": {
    "command": {
      "type": "command",
      "command": ["python", "path/to/adapter.py"]
    }
  }
}
```

字段以安装版本的 `research validate` 为准；不要凭 Skill 正文猜测 Core 已新增的字段。

## 输出契约

最终报告包含：

```text
Research ID / revision
Question 与 Hypothesis
Baseline、Candidate、数据集与指标
Run 状态和环境/Adapter 版本
Decision
关键 Evidence（含 artifact digest）
限制、冲突与尚缺证据
复现或继续命令
```

不得把 `ok: true`、工具成功或单次模型输出当作研究结论。相关示例见 `examples/llm-replacement.md`。
