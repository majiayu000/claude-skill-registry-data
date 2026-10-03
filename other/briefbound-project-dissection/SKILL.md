---
name: briefbound-project-dissection
license: MIT
description: Use when the user wants to understand or learn a repository through source-guided architecture explanation, a representative execution path, design tradeoffs and a reading route; not for risk-first project audits or isolated function questions.
---

# Briefbound 项目拆解教学

把仓库变成能推理、能迁移的理解：从实际数据结构和入口追到业务结果，解释设计选择的代价与失效边界。中文讲解，关键文件、函数与 API 保留原名。

## Briefbound task contract

- Context Boundary: 目标仓库、用途、基准 commit/工作区差异、已读模块、代表链路和未覆盖范围。
- Output Contract: 中文拆解报告、代码证据、阅读路线；完整拆解默认附架构总览和主链路图及独立 HTML/SVG/PNG。
- Allowed Action: 只读目标源码；在任务输出目录生成事实材料、报告与图解。远程源码可克隆到任务临时目录；不安装或运行被调研项目。
- Success Evidence: 解释与代码位置对应，事实与推断分开，主链路可追溯，图解实际导出并通过检查，未覆盖范围如实披露。
- Stop Condition: 缺少决定结论的源码、关键关系无法确认、范围扩大或输出格式无法完成。
- Route Out: 风险审查交 briefbound-project-review；复用选型交 briefbound-feature-reuse-research；图解交 briefbound-diagram-design；验证后的真实残留转 briefbound-development-cleanup；目标分歧交 briefbound-router。

## 统一调用契约

用户可见内容默认中文；Route Out 仅以 Briefbound task contract 为准。末行 `下一步建议: <一个具体动作>`，且限于决策类建议（推荐方向、优先级或需用户拍板的选项，如后续深读方向），不把可自行完成的执行步骤包装成建议交回。继承已确认仓库、用途和深度，不重复询问。普通局部函数解释直接回答，不启动整仓报告。

## 取证与讲解

1. 明确项目解决的问题和最具代表性的场景。先读 README、核心数据结构、入口和测试，再沿该场景追调用、数据转换与输出；不要默认把所有项目套成四层架构。
2. 全仓拆解时读取 [取证与交付](references/dissection-guide.md)，复用 `scripts/scan_repo.py <repo> --out <task-output>/facts` 生成事实材料。已有足够材料或局部问题无需重复全量扫描。扫描输出也是待核对的数据，不是架构结论。
3. 先建立主干再补必要分支；默认追一条代表链路，但不能因固定层数截断关键事务、异步调用或错误传播。
4. 对所选核心模块解释：承担什么职责；本项目约束下有哪些选择及代价；迁移到别处时何时适用、何时失效。不固定句数，不虚构作者否决过某替代方案。
5. 事实绑定文件/符号或命令证据；设计动机无 ADR/提交说明时标“推断”；运行时未执行的行为标“未确认”。目录名、依赖存在或测试文件比例不足以证明架构、实际调用或测试覆盖率。
6. 阅读路线按数据模型、入口、主链路、支撑机制、扩展边界组织，每站给一个能检验理解的问题。列出实际深读与未读模块；没有明确分母时不报覆盖率百分比。

## 默认联动图解

完整拆解自动加载当前可用的 `briefbound-diagram-design`，无需另问是否配图：

- 架构总览：核心模块、职责和有证据的依赖。
- 主链路：真实入口、关键函数、数据流和结果；异步多方交互优先时序图。
- 设计取舍：只有比较确实需要视觉辅助时追加，不凑图数。

拆解技能负责内容与最终报告，图解技能负责布局、生成、几何检查、导出和视觉验收。交接节点/边、证据位置、事实或推断标记、中文说明与原始代码名称；不把未确认关系画成事实。图解必须遵循其 SKILL.md 及相关参考文件，不复制第二套绘图规范。

完整报告默认离线单文件 HTML，使用 [报告骨架](assets/report-template.html)，内嵌已验证 SVG，并交付独立图解 HTML、SVG、PNG。嵌入两张 SVG 时给元素 ID 及其引用分别加前缀，避免 marker 等互相覆盖。用户指定 Markdown 时交付 Markdown 和图片；要求纯文字时跳过配图；简短讲解只在确有帮助时配图。图解能力不可用或导出失败要明确交付缺口，不能把 HTML 链接当 PNG。

交付前检查代码依据、版本与工作区状态、未确认项、未读模块、无模板占位符、离线可读和真实图片。没有证据不编造结论、数字或图。

## 来源

方法、扫描器来自用户提供的本地 WorkBuddy `project-dissection`，按 Briefbound 路由和图解联动重新组织。来源与扫描边界见 [取证与交付](references/dissection-guide.md)。
