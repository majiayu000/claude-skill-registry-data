---
name: software-concept-architect-prd-cn
description: Generates PRD files from a confirmed concept model only when the user explicitly invokes $software-concept-architect-prd-cn. / 仅在用户显式调用 $software-concept-architect-prd-cn 时转录概念 PRD。
metadata:
  language: zh-CN
  translation_of: software-concept-architect-prd
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills
---

# 软件概念架构师 · 需求规格

焦点问题：如何把已确认模型持久化，使目的、行为与验收仍可追溯？仅在显式调用 `$software-concept-architect-prd-cn` 时运行。输入模型含 concepts、syncs、依赖、排除与未决；模型缺口回 software-concept-architect-design-cn，代码落地交 software-concept-architect-build-cn。

## 转录原则

确认模型约束目的、行为与取舍；CONCEPT 保存概念契约，SYNCS 保存协调，总体 PRD 索引全局关系。每个模型元素只保留一份权威文件。

保存两层论证及前提：契约 → OP → 概念目的；概念选择/sync → 应用场景 → 应用目的。验收从这些场景或行为契约导出并附来源；文件齐全不能补足模型缺口。

**同步可收窄行为，不可扩展契约**：应用排除与限制归 SYNCS/总体 PRD，保留概念自身允许的行为；模型中的违约协调标为缺口，交回设计修订。

## 转录与核对

1. **核对输入**：读确认模型、需求出处与现有文档；仅核实模块路径及索引所需代码事实。实际代码差异不能未经确认改写模型。
2. **确定落点**：以下为输出路径；模块未就绪时暂存。

   ```text
   docs/prd/README.md        # 总体 PRD
   <模块>/CONCEPT.md          # 或 docs/prd/concepts/<名>.md
   <syncs>/SYNCS.md           # 或 docs/prd/SYNCS.md
   ```

3. **写总体 PRD**：保存应用目的、端到端场景及其概念/sync 依据、Misfits、概念索引（purpose + 链接）、同步图、产品依赖与子集、排除和未决；跨概念前提及论证放这里。
4. **转录规格与验收**：读 [规格契约](references/spec-format.md) 与 [文件编排](references/templates.md)，CONCEPT 保留四节、概念内前提与目的兑现说明；应用背景进 notes。SYNCS 转录 app/include/sync，按入口或规则职责以 `// flow:` 分组，转录期单文件。概念 OP、应用场景和行为契约分别导出验收，均附出处；应用目标缺失时标未决，不从概念目的拼造。
5. **更新核对**：对已有文档做最小编辑，同步索引/派生图，保留人工维护内容；实现期迁移或 sync 拆包由 software-concept-architect-build-cn 承接。

## 完成条件

- 每个模型元素有唯一落点，定义、关系、论证前提、排除与未决无遗漏；未确认信息保持原状态。
- CONCEPT 四节不依赖其他概念定义；同名局部参数合法；无 interactions/dependencies 段，应用实例化归 SYNCS。
- 验收可追溯到概念 OP、应用场景或行为契约；缺口不被占位内容包装成已确认行为。
- sync 参数、绑定与输出对应真实声明，可达失败策略保留，查询空集不变成错误；全局索引链接有效。

首次转录读 [订位例](references/example-reserving.md)；核验规格依据读 [sources.md](references/sources.md)。
