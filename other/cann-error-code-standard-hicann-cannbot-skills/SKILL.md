---
name: cann-error-code-standard
description: CANN算子错误码的基准知识源，提供官方文档错误码清单、来源与版本治理、选码和上报规范、机器可读契约。触发：新算子错误码设计、源码静态检查、问题定位或整改Skill需要统一错误码基准时；不直接修改算子源码或执行构建测试。
---

# CANN错误码基准

本Skill是算子错误码知识的唯一上游真源。下游开发、整改、问题定位和静态检查Skill应引用这里的清单与规范，不复制后形成独立版本。

## 使用路由

- 需要选择或评审错误码：读取[开发使用规范](references/development-standard.md)，再在[文档错误码清单](references/documented-error-code-catalog.md)中检索候选。
- 文档清单没有合适语义：按归属组件读取[组件错误码源码索引](references/component-error-code-source-index.md)，继续核对目标版本注册项；不得凭索引跨模块直接借码。
- 需要静态检查或自动化消费：读取[来源与维护规则](references/source-and-maintenance.md)中的数据契约，使用[机器可读码表](references/documented-error-codes.json)。
- 需要判断资料是否收录：使用码表的`codes[].code`与对应`url`；不要把“资料收录”解释为“目标版本已注册并可调用”。
- 需要更新基准：只依据[来源与维护规则](references/source-and-maintenance.md)允许的公开可信源，同时更新Markdown与JSON并完成一致性检查。

## 证据层级

1. 官方公开错误码资料证明“资料收录、公开语义和用户指引”。
2. 目标版本开源注册表和头文件证明“编号、Arglist、宏及模块入口存在”。
3. 目标构建的CMake/include链证明“调用点实际使用哪个实现”。
4. 目标安装包和负向运行日志证明“交付版本实际行为”。

这四层不能互相替代。结论必须注明核对到了哪一层；缺少目标版本注册或运行证据时，不得声称错误码可直接使用或已经生效。

## 标准输出契约

下游Skill引用本基准后，每个选码或校验结论至少给出：

- 根因类别与首报责任层；
- 候选正式码、文档URL和目标版本注册证据；
- 实际调用宏/入口及Arglist；
- 必须输出的`opName/parameter/actual/expected/reason/rc`字段；
- 外层是正式首报还是仅日志透传；
- 公开返回值是否保持兼容；
- 仍缺少的编译、负向测试或运行证据。

本Skill只给出基准结论，不修改源码、不解析项目include链，也不执行编译和测试；这些动作由下游执行类Skill完成。
