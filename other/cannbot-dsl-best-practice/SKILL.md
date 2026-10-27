---
name: cannbot-dsl-best-practice
description: "为 CANNBotDSL 算子提供整体实现、局部写法和生产代码最佳实践。当需要职责划分、Host 约束校验、Channel/同步/布局、注册与适配、编译启动、AICPU 负载均衡 metadata、VF 向量计算或命名建议时使用。"
metadata:
  category: implementation
---

# CANNBotDSL 实现最佳实践

针对当前实现问题提供可应用的写法、选择依据和正反例。参考内容按主题组织，示例使用通用对象名，不要求某种算法、工程目录或特定实现存在。

## 输入

- 算子规格与设计资料：由调用方提供文件或目录，确定数学语义、执行路径和目标设备约束。
- 当前实现代码与需要解决的组织或微模块问题。
- 按需提供当前 Unit、测试用例和 Golden，用于说明本次能力边界与验证方法。

## 输出

针对当前问题给出代码组织或微模块写法建议，写明设计依据、适用前提、需核实的 API/设备事实，以及应执行的相关测试。调用方决定建议的记录位置和是否用于修改代码。

## 参考选择

| 问题或关键词 | 参考 | 解决的问题 |
|---|---|---|
| 整体结构、入口、Host、Kernel、@export、Native 导出、生命周期 | [整体实现](references/overall-implementation.md) | 公共骨架、导出与程序管理 |
| 命名、常量、重复、注释、docstring、可读性 | [生产代码](references/production-code.md) | 清楚表达数据、单位与计算意图 |
| Host 校验、非法输入、约束拦截、dtype、shape、参数组合 | [Host 约束校验](references/patterns/host-validation.md) | 在分配、编译和启动前拒绝非法元数据 |
| Channel、Buffer、双缓冲、深度、slot | [Channel 与 Buffer](references/patterns/channel-buffer.md) | 存储选择、生命周期和复用 |
| CrossCore、同步、事件、屏障、流水线交接 | [同步](references/patterns/synchronization.md) | 写入、可见、读取、复用顺序 |
| VF、寄存器向量、mask、向量归约、cast、pack/unpack | [VF 向量计算](references/patterns/vf.md) | 向量操作链、尾部掩码、类型转换与累计状态 |
| layout、stride、ND/NZ、视图、尾块、有效行 | [布局与尾块](references/patterns/layout-tail.md) | 物理跨度、格式转换与有效范围 |
| workspace、临时存储、资源容量、别名、跨阶段复用 | [Workspace](references/patterns/workspace.md) | 分配、所有权、容量与生命周期 |
| AICPU、负载均衡、metadata、调度协议、记录消费、任务成本、分核、分轮 | [AICPU 负载均衡 Metadata](references/patterns/aicpu-load-balance-metadata.md) | 设备侧调度、成本划分、记录生成与消费 |
| Torch 注册、schema、Meta/Fake、dispatch、torch.ops | [Torch 注册](references/patterns/torch-registration.md) | 注册契约与真实计算一致 |
| aclnn、参数映射、接口兼容、运行时适配 | [aclnn 适配](references/patterns/aclnn-adaptation.md) | 语义转换与接入职责 |
| 编译、程序复用、特化、TensorSpec、launch | [编译与启动](references/patterns/compilation-launch.md) | 编译结果复用与本次输入绑定 |

生成完整算子或设计其公共结构时，必须读取 [整体实现](references/overall-implementation.md)，落实其中的公共骨架与必备 `@export` 入口；生成或修改算子源码时读取 [生产代码](references/production-code.md)，应用代码规范与轻量检查规则。

按问题含义选择内容；多个主题直接相关时组合读取。仅有命名问题时不需要读取全部计算参考，缓冲覆盖问题则同时涉及 Channel 与同步。

## 应用原则

1. 先确认当前问题和公开契约，再读取直接相关的参考。建议应指向具体代码位置，说明为什么适合这里。
2. 示例只展示一个核心决策。将其中的维度、类型、资源上限换成当前契约；不要把示例选择推广成硬件默认值。
3. `text` 代码块是结构伪码，其中的操作名不是 DSL API。落地前从当前源码、安装包或官方资料核实签名、同步语义和设备限制；不能把伪码当成已通过编译的代码。
4. 每条建议附带能够暴露该问题的检查，例如跨步输入、尾块或缓冲复用。诊断信息和反例放在对应主题内，不要求独立探针或额外执行流程。
5. 设计规定的设备计算和搬运由 DSL 完成；Host 处理元数据、分配、已确认的零拷贝视图和启动，可使用不下发额外设备算子的 torch。禁止正式路径用 torch 设备小算子补算、初始化或转换；按实际调用效果和 msprof 证据验收，不限制设计所需的自定义 DSL Kernel 数量。独立 Golden 与测试代码不承担公开结果的补算。

6. 区分设计强制承诺、允许选项与待定候选；在选项内调整实现，保留已交付行为并回归受影响能力。关键补证失败或改变强制执行域、通路、同步、复杂度等承诺时，向调用方记录失败证据与影响，不以数学等价替代设计完成，不自行修改冻结设计或调度回滚。
