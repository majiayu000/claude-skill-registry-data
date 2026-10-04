---
name: cm-idea
description: 用户说“我有个点子”“帮我梳理产品”或需要先聊清目标时使用。通过逐题访谈整理为可交给 cm-prd 的 PRD；已有明确需求文档时改用 cm-prd，不写代码、不拆开发任务。
---

# cm-idea — 点子 → PRD（流程上游入口，非 N1–N8 步骤）

先读取 `../../runtime/project-context.md`。Codex 入口为 `$cm-idea`；Claude Code 跨平台入口为 `/cm-idea`，macOS/Linux 另有历史别名 `/cm:idea`。

用户明确要求外部专家，或为本次访谈开启 AUTO 时，先读取
`../../runtime/external-expert.md` 并执行 `../external-expert/SKILL.md` 的任务路由。
AUTO 只在复杂方案/材料综合时 CONSULT，需要权威事实时 VERIFY，其余 LOCAL。外部
结果只作为访谈输入，不能替用户确认产品方向；没有明确请求，也没有本次 AUTO 授权
时，保持原来的纯对话、不联网流程。

**用法**：`$cm-idea 一句话点子`（如 `$cm-idea 我想做个帮宝妈记录辅食的小程序`）

## JS 只读准入

在加载访谈引用、联网或探测保存目录之前，先执行：

```bash
node "{CM_WORKFLOW_ROOT}/scripts/cm-idea-entry.mjs" \
  --skill-dir "{CM_WORKFLOW_ROOT}/skills/cm-idea"
```

只有 `ready / interview` 才继续加载下方引用。该结果不读取或回显点子内容，不调用外部专家，
也不授权保存文件；保存前仍必须按访谈引用取得用户对完整路径的确认。JS宿主管理轮次和保存，
`references/idea-to-prd.md` 继续是访谈规则唯一事实源。

把模糊想法聊成成熟 PRD 的产品访谈搭档。**本命令只做一件事**：加载 `references/idea-to-prd.md` 并严格按其规则执行——本文件不复制不改写访谈规则，该引用文件是唯一事实源。

## 执行

1. 读取 `references/idea-to-prd.md`，缺失则提示重装最新包后中止
2. 按 [当前会话接线](references/js-host.md) 启动JS宿主，把用户实际输入送入访谈；判定类型、一次一题、L1骨架和按需加深仍遵循原引用，交易/Web3先读领域包
3. 全程遵守技能自身纪律（一次一题、防诱导选项、狠收敛、纯对话不联网）

## 与 cm 流程的衔接（只提示，不自动执行）

只有JS返回 saved 且文件已回读，才追加下面的“已保存”提示；未保存则如实报告草稿状态，不伪造路径或自动代跑后续命令：

```text
📄 PRD 已保存: {路径}(成熟度 {L1/L2/L3},「待明确的问题」剩 {N} 条(口径:只数 PRD 第 7 节的条目,正文散落的待补标记不计;路径用绝对路径)——带着未决问题交棒,prd 的产品角色会重新追问;想少被问就先在这里加深)
下一步(需要你手动执行,本命令不代跑):
  1. 建 specs 文件夹,把这份 PRD 放进 docs/
  2. $cm-prd {specs路径}   ← 拆成规格三件套
  3. 人审摘要卡后 $cm-ai 开始开发
```

## 边界

cm-idea 位于 specs 上游，按设计不读写规格审批位 `.cm-specs-status`；这是职责边界，不是遗漏。

- 不写代码、不拆任务、不调 $cm-prd——想法阶段结束就交棒
- 已有现成需求文档的项目不需要本命令，直接 `$cm-prd`
- 触发词自然唤起（"我有个点子…"）与本命令等效，习惯哪个用哪个
