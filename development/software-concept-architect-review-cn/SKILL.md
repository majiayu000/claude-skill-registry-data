---
name: software-concept-architect-review-cn
description: Audits software-concept-architect-design-cn arguments and optional code conformance only when the user explicitly invokes $software-concept-architect-review-cn. / 仅在用户显式调用 $software-concept-architect-review-cn 时审查概念设计及实现符合性。
metadata:
  language: zh-CN
  translation_of: software-concept-architect-review
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills
---

# 软件概念架构师 · 审查

焦点问题：概念及应用设计能否兑现各自目的，已有实现是否符合设计？仅在显式调用 `$software-concept-architect-review-cn` 时运行，全程只读。无代码可审设计；无规格只能审可验证的代码性质；缺失材料对应的结论标未核实。

## 审查原则

分别审查契约 → OP → 概念目的、概念选择/sync → 应用场景 → 应用目的及其前提。实现符合规格、OP 测试通过或局部目的成立，均不证明应用适合实际需要。

按五维核对：

- **适切性**：声明前提下的行为满足实际需要；用事实与反例检验。
- **独立性**：概念定义不依赖其他概念；本仓还要求概念模块互不引用。
- **组合**：**同步可收窄行为，不可扩展契约**；行为减少本身不是违约，剩余场景仍须满足需要。
- **漂移**：实现与确认契约的差异；区分遗漏与明确矛盾。
- **子集**：保留目的、入口、同步与资源，另查实现支持。

证据来自已读需求、模型、实现或测试；推断另标，材料缺失只支持未核实结论。

## 执行

1. **界定范围**：读 [规格契约](references/spec-format.md) 区分格式兼容与语义缺陷，再读取需求、CONCEPT/SYNCS、总体 PRD 及暂存链接；有实现时沿入口读调用、状态/schema/迁移和测试。记录版本、关键术语、事实/推断、覆盖与缺口。
2. **审设计论证**：明确概念与应用目的；逐概念审契约/OP 论证，应用论证随组合一起审。按单一目的、完整行为、独立性、熟悉性查 conflation/fragmentation；新颖或基础设施身份本身不是缺陷，先确认使用者（含 API 程序员）与价值。
3. **查漂移与独立性**：有代码时读 [drift-checklist.md](references/drift-checklist.md)，对账签名、输出、不变量、状态及真实依赖，含公开 API 互调、共享可变状态、私有访问及 DTO/协议类型侵入概念契约；同名局部类型参数不算语义依赖。
4. **查组合**：读 [composition-checklist.md](references/composition-checklist.md)，从应用目的推演端到端场景，核对每段动作/sync 的作用及欠/过同步；逐概念核对组合行为序列，再查完成事件、绑定、隔离、失败、重放与循环。设计材料支持静态推演，运行时符合性另需实现证据。
5. **查依赖与子集**：分别核验 PRD 产品依赖及代码限制；具体子集须保留目的、入口、sync 与资源，有实现时再查构建支持。产品图与代码图无需同构。
6. **聚合**：交叉核对 include、动作/query、参数、输出与图；合并根因并列受影响位置，按适切性/独立性/组合/漂移/子集五维报告，未执行项不能算通过。

## 报告与完成条件

```markdown
# 审计报告 <日期>
范围：<需求/规格/代码版本；已核实、未核实及原因>
Summary：<覆盖、发现数、严重度>

| 命题/发现 | 场景与证据位置 | 失败关系或未决前提 | 影响/严重度 | 修复路由 |
| --- | --- | --- | --- | --- |

覆盖：<五维、每个概念及入口/规则组的结论>
修复顺序：<合并根因、受影响位置、当前修复步骤及后续依赖>
```

严重度按漂移参考校准；Medium 以上需当前规格/代码证据，纯设计可作规格推演。OP 无测试与目的落空分开归因；无实现不报实现违约。欠/过同步附场景，完整核验后才断言不存在。

模型问题 → software-concept-architect-design-cn；转录/索引错误 → software-concept-architect-prd-cn；代码违约 → software-concept-architect-build-cn。一个发现先给当前修复目标，连续阶段另列依赖；无需求依据时不能默认规格追随代码。

核验 Jackson 与判据出处读 [sources.md](references/sources.md)。安装包独立可读；审计不写规格、代码或历史。
