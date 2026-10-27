---
name: ops-design-paradigms
description: 当需要设计或修订 Broadcast、Reduction、Contraction 等算子范式方案，或查询对应算法、资源规划、语言实现约束和故障经验时使用；提供 Ascend C regbase 与 CANNBotDSL 的设计依据、适用条件和验证要点。
---

# 算子通用设计知识与范式指导

根据算子语义和开发语言提供范式知识，支持方案设计、实现选择与问题定位。内容分为语言中立的算法模型和语言专用的实现约束，按当前问题读取。

## 输入与输出

- 输入：算子规格或等价的数学语义与范式信息、明确的开发语言（`ascendc` 或 `dsl`）、目标平台，以及待解决的设计或实现问题。文件路径由调用方提供。
- 缺少语言或范式信息时，返回具体缺项；确认后再选择专用参考。
- 输出：适用的算法与实现建议、约束及其依据、资源与同步分析、尚待验证的事实。产物格式和保存位置由调用方确定。

## 范式与语言选择

1. 先读取 [知识索引](references/index.md)，按当前问题选择入口。
2. 当 `op.paradigms` 包含 `Contraction`、并且包含`Reduction`、`Broadcast` 其中一个时，先核对实际公式。公式包含注意力分数计算与加权值聚合时，读取 [FA 组合范式](references/paradigms/FA/patterns.md)；其余组合按范式索引逐项读取。标签匹配按集合包含关系判断，顺序及额外标签不影响匹配。
3. 其余情况统一按 [范式索引表](references/paradigms/routes.yaml) 逐项查找。多个范式覆盖不同设计维度，分别按需读取；未注册范式使用已有的对应语言通用方法，缺少对应方法时报告资料缺项。
4. 每个范式的 `patterns.md` 根据调用方提供的语言选择适配层。只读取通用层和对应语言的适配层；其明确引用的配套运行时或同步章节按需读取。缺少适配层时保留通用算法，语言 API 与设备能力依据调用方提供的资料确认，不回退到其他语言的实现。

## 参考选择

| 当前问题 | 入口 |
|---|---|
| Broadcast、Reduction、Contraction 方案与资源规划 | [范式索引表](references/paradigms/routes.yaml) |
| Ascend C regbase 开发方法 | [开发指导](references/knowledge/regbase_development_guide.md) |
| Ascend C API、实现模式、精度风险或开发经验 | [知识分类索引](references/knowledge/index.md) |
| 缺少专用范式或语言适配层 | [Ascend C 通用方法](references/paradigms/general-methodology.md)、[DSL 通用方法](references/paradigms/general-methodology-dsl.md) |
| 选择现有 Ascend C 实现作为参考 | [开源算子表](references/reference-ops/open_source_operator_table.md) |

`knowledge/` 与 `reference-ops/` 是 Ascend C regbase 资料，DSL 问题仅使用相关通用层和 DSL 适配资料。

## 使用约束

- 进入 `api/`、`patterns/`、`pitfalls/` 或 `dev-experience/` 时先读目录索引，按 `purpose`、`read_when`、`keywords` 选取叶子文档。单个子问题最多展开 5 份，仍未解决则拆分问题。
- 能力谓词以对应语言的 `capability-mapping.md` 为依据；标注“待验证”的项须作为假设和验证义务输出。
- 实现参考用于核对 API 与组织方式；名称或类型匹配不能证明可以直接复制或融合，算法与参数需依据当前规格判断。
- 明确资料对应的平台。兼容性经验不能直接作为 `ascend950 / regbase` 的已验证结论。
- 设计输出应能追溯到规格和参考资料；缺少 API、资源或运行证据时报告具体缺口。
