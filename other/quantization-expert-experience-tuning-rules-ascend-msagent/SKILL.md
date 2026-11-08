---
name: quantization-expert-experience-tuning-rules
description: |
  量化专家经验调优库：按「L1 通用专家调优意见 → L2 结构化专家调优意见 → L3 模型专属专家调优意见」三级递进，
  输出量化精度调优的完整手段（离群值抑制 / 量化方法·粒度·对称性选型 / 校准集调整 / 敏感层回退 / 模型专属策略），
  每条结论附专家原因分析与专家意见可信度等级。
  本 Skill 是专家经验库，负责说明可选离群值抑制算法并询问用户选择哪些算法，以及回答「怎么调、哪些层需要回退及为什么」；不运行离群值抑制 processor，不修改 YAML、不执行量化、不做 EP 检查 / 服务化 / 任务评测。
license: Apache-2.0
metadata:
  version: 0.2.0
  domain: quantization
  framework: msmodelslim
  protocol: reference
  skill_class: tool
  aliases:
    - quantization-tuning-rules
    - expert-tuning-experience
    - quantization-fallback-rules
    - expert-fallback-experience
  trigger_intents:
    - 量化调优
    - 量化专家经验
    - 敏感层回退
    - 哪些层需要回退
    - 量化精度调优
    - 离群值抑制
  keywords:
    - 专家经验库
    - 量化调优
    - 离群值抑制
    - 量化方法选型
    - 校准集
    - 敏感层回退
    - mlp.down_proj 回退
    - gate/router 排除
    - shared_experts 保持高精度
    - MLA 低秩投影排除
    - fa3_quant
---

# 量化专家经验调优库

## 职责边界

本 Skill 回答「**给定量化目标与模型结构，如何调优量化精度**」，输出基于专家经验分析的调优结论：

- **完整手段链**：离群值抑制算法、量化方法/粒度/对称性选型、校准集调整、敏感层回退、模型专属策略。
- **回退**：排除量化、恢复 BF16/FP16、或把某模块提级到更高精度档位（如 W4A8 中 experts 之外保持 W8A8），只是手段之一，且是**最后手段**。
- **不回退 / 保持量化**：无专家经验支持时保持量化，不等于对所有模型绝对安全。

调优的具体执行（改 YAML、运行离群值抑制 processor、logits 对比、跑
`msmodelslim quant`、EP 检查、服务化、全集/子集测评）由对应执行 Skill 承接，不在本
Skill 范围内。

## 三级知识结构

按「通用 → 模型类 → 专属」递进，**新模型先通读 L1，再按触发信号读 L2 对应小节，最后按 vendor 查 L3 个案**。

| 层级                        | 定位                                                                                                             | 文件                                   | 阅读时机                        |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------------------------- |
| **L1 通用专家调优意见**     | 与具体结构无关的通用专家调优意见                                                                                 | `cross-model-pitfalls.md`              | 任何新模型都先通读              |
| **L2 结构化专家调优意见**   | 仅对某类结构成立（MoE / MLA / 混合 attention / 自定义 modeling / VLM / DiT / DSA-SWA-GatedDeltaNet / Dense FFN） | `structure-family-pitfalls.md`         | 按触发信号判定，可多属，叠加 L1 |
| **L3 模型专属专家调优意见** | 各 `<vendor>/<model>.md` 个案，只放该模型/模型类独有的调优意见                                                   | `models/`（索引见 `models/README.md`） | 命中已收录模型时叠加            |

## 输入

尽量提供：

- 模型结构类型与完整模块名样例（`named_modules`）；
- 量化格式：`w8a8` / `w4a8` / `w4a4`（含 int / mxfp 系）；
- 是否 MoE / EP、routed/shared experts 与 gate/router 命名；
- 当前生效 YAML 的 `include`/`exclude`、回退项与量化配置；
- 浮点基线、量化精度、敏感层分析或异常日志；
- 可引用的既有 Practice YAML 路径。

## 输出

按以下顺序给出调优结论：

1. **场景定位**：结构模型类 + 量化格式，命中 L1/L2/L3 哪几处。
2. **首选调优手段**（非回退）：离群值抑制、量化方法/粒度/对称性、校准集。
3. **优先回退候选**：模块模式、层范围、回退方式与专家原因。
4. **默认保持量化 / 已保持高精度结构**：有明确映射的 BF16 / 排除量化结构。
5. **模型专属策略**：L3 命中项。
6. **建议顺序与风险**、**YAML 变更记录**与专家意见可信度。

进入调优阶段时，先接收调用方基于已安装 Adapter 接口得到的 `supported_algorithms`。
未收到该集合时，先让调用方完成接口预检，再进行算法选择。本 Skill 只从该集合中
向用户介绍离群值抑制候选，说明适用场景和风险，再询问选择；
没有可选算法时不推荐离群值抑制。不得把以下示例中的算法视为当前模型均可选择：

```yaml
user_confirmed_anti_outlier_algorithms:
  - { type: quarot, config: {}, source: user_confirmed }
  - { type: flex_smooth_quant, config: {}, source: user_confirmed }
  - { type: flex_awq_ssz, config: {}, source: user_confirmed }
  - { type: iter_smooth, config: {}, source: user_confirmed }
```

示例中的空 `config` 表示用户没有覆盖参数；执行阶段仍须读取 msModelSlim 对应的官方
`*_default` 模板，不能把空对象直接当作 `flex_awq_ssz` 的完整 processor 配置。

该字段只记录用户选择。专家经验不得调用 processor、执行前向或填写 logits PASS/FAIL；
离群值抑制阶段负责算法适配与门禁，调优只信任已安装 Adapter 声明的接口。

不得只根据模块名称直接宣称「回退必然提升精度」，须说明原因（如敏感层、结构重要性、误差传播路径）。

## 最小工作流

1. 通读 L1 `cross-model-pitfalls.md`，确认精度调优递进顺序与手段链。
2. 从真实 `named_modules`/YAML 判断结构模型类，按 L2 触发信号叠加对应小节。
3. 命中有 L3 个案的模型，叠加 `models/<vendor>/<model>.md`。
4. 说明离群值抑制可选项并询问用户选择，记录 `user_confirmed_anti_outlier_algorithms`。
5. 再给出其他非回退手段与敏感层回退候选，每条附专家原因。
6. 结论附专家意见可信度；processor 与 logits 校验由离群值抑制阶段承接。

## 核心规则速查

| 类别                                                          | 默认处理                                                                           | 说明                                                                                           |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| 激活离群值                                                    | 候选包括 Iterative Smooth、Flex Smooth Quant、Flex AWQ SSZ、QuaRot，具体由用户选择 | 各候选在离群值抑制阶段单独执行和校验，不把组合运行结果当作单算法结果                           |
| 权重低比特方法                                                | INT8 用 minmax；INT4 用 ssz，不足再 autoround/gptq                                 | 权重 per_channel + 对称。ssz 在低比特下对分布适应性更好                                        |
| 激活粒度                                                      | 性能 per_tensor；精度 per_token；平衡 pd_mix                                       | 激活通常非对称。per_token 可适应不同 token 的分布差异                                          |
| 校准集                                                        | 10–50 条、场景匹配、删异常、加 badcase                                             | 第 4 步。校准数据不足或分布偏移会导致量化参数估计偏差                                          |
| `mlp.down_proj`                                               | 优先回退候选                                                                       | 该层是 FFN 输出投影，聚合了 up_proj/gate_proj 的激活信号，量化误差易在此累积放大               |
| `o_proj`（self_attn 输出投影）                                | 结构化回退候选                                                                     | `exclude` 增加 `*.o_proj`，单层投影保持浮点。作为 attention 输出聚合层，对整体表征质量影响较大 |
| MoE `gate`/`router`                                           | 排除量化 / 保持高精度                                                              | 路由决策敏感，量化误差可能导致 token 路由到错误 expert，造成推理质量下降                       |
| MoE `experts`                                                 | W4A8/W4A4 下为低比特落点                                                           | 敏感实例才提级回退。experts 数量多、参数量大，是低比特的主要收益来源                           |
| `shared_experts`                                              | 通常保持高精度                                                                     | 每层共享，被所有 routed experts 复用，其误差会被全局放大，故保持高精度                         |
| MLA 低秩投影（`kv_b_proj`/`q_a_proj`/`wk`/`weights_proj` 等） | 条件性排除                                                                         | 该结构承载逐头/低秩信息压缩，量化后误差会沿 attention 路径传播累积                             |
| DSA / SWA / GatedDeltaNet                                     | 保持高精度（bf16）                                                                 | 这些特殊结构在模型中承担交替扫描/线性注意力等特殊功能，分布与标准 attention 差异大             |
| VLM 跨模态融合（`merger`/投影/视觉塔）                        | 初版不量化，常见排除                                                               | 仅量化 LLM 部分。跨模态投影层连接不同模态空间，量化误差可能破坏模态对齐                        |

## 参考资料

- `cross-model-pitfalls.md` — L1 通用专家调优意见（离群值抑制/方法/粒度/校准集/回退）
- `structure-family-pitfalls.md` — L2 结构化专家调优意见（MoE/MLA/混合 attention/VLM/DiT/DSA/自定义 modeling/Dense FFN）
- `models/`（`models/README.md` 为索引）— L3 模型专属专家调优意见（deepseek/glm/minimax）
- 协同执行：`msmodelslim-ep-parallel-adaptation`（EP 适配）；调优主流程由 `quantization-accuracy-tuning-orchestrator` 承接
