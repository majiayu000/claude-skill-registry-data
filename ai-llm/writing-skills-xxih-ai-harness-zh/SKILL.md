---
name: writing-skills
description: 当你要创建新 skill、重写已有 skill，或把稳定 workflow 提炼为可复用 skill 时使用。
---

# Writing Skills

这个 skill 解决的不是“写一篇怎么做的说明文”，而是把稳定 workflow 提炼成可发现、可验证、可分发的独立 skill。默认组合三类经验：用 Anthropic 的规范守住 discoverability 与 progressive disclosure，用 Superpowers 的 fail-first 闭环保证 skill 真能改变 agent 行为，用 Codex `skill-creator` 的目录约束保持 skill 包长期可维护。

## 何时使用

- 你准备创建一个新的 skill
- 已有 skill 命中率差、正文过长、边界模糊，准备重写
- 你手头有一段稳定 workflow，准备升级成正式 skill 资产
- 你想验证某个 skill 是否真的改变了 agent 行为，而不是只改了文案

不适用：

- 只是某个项目或团队的私有规则，应该优先写进项目级指令文件或团队文档
- 只是一次性经验，还没形成跨任务复用模式
- 可以靠脚本、lint、schema 或 hook 强制的机械规则
- 只是平台运行时安装、打包、metadata 或导入适配

## 产物

每次使用本 skill，默认产出以下最小集合：

1. 独立 skill 包
   - `<skill-name>/SKILL.md`
   - 只有在需要时再补 `references/`、`scripts/`、`assets/`
2. 验证证据
   - 一份 baseline / rerun 记录，证明这个 skill 修正了什么失败
   - 记录写到当前任务已有的工作面即可，不预设固定仓库目录
3. 分发适配
   - 只有在目标 AI 工具确实需要额外包装时，才补对应适配副本

## 核心原则

### 1. 先判断它是不是一个 skill

先区分这件事应该沉淀到哪里：

- 跨任务、靠判断执行、需要被模型主动发现的稳定能力 -> skill
- 项目或团队的长期私有规则 -> 项目级指令文件或团队文档
- 目录结构说明、人工导览 -> README 或普通文档
- 轻量触发入口、固定命令壳 -> command / prompt template
- 平台运行时 wiring、metadata、hooks、安装流 -> 分发适配层
- 还没稳定的经验候选 -> 临时笔记或研究记录

边界判断和检查清单见 `references/authoring-checklist.md`。

### 2. description 只写触发条件

`description` 的作用是帮助模型判断“现在要不要读这个 skill”，不是偷跑 skill 的 workflow。只写触发条件、症状、上下文，不写步骤数量、子技能链路或执行摘要。

### 3. 先看没有 skill 时会怎么失败

写 skill 前先构造一个 pressure scenario，观察没有 skill 时 agent 会怎么误判、漏步或合理化。没有 baseline，就不知道 skill 到底在修什么。验证循环和模板见 `references/validation-loop.md`。

### 4. 主文档保持短，重资料按需下沉

`SKILL.md` 只保留目标、适用边界、主流程和纪律约束。详细 checklist、模板、长示例放 `references/`；可重复执行的确定性操作放 `scripts/`；最终输出要消费的模板或素材才放 `assets/`。

### 5. 默认保持独立，不绑定当前仓库结构

除非用户明确要求，否则不要把某个仓库里的领域分层、任务容器、记录目录、命令体系或 target 目录写进 skill 正文。skill 默认应该能被单独复制、导入、分发，而不依赖作者当前仓库的内部布局。

### 6. 资产工程化优先于文档堆砌

skill 包只保留完成任务必需的文件。不要为了“看起来完整”额外创建 README、安装指南、变更日志或过程笔记。

## 工作流

1. 定义 skill 候选
   - 明确要教会 agent 的单一能力、适用边界和非目标
   - 先判断它该不该升级为 skill，而不是别的资产类型
2. 先做 fail-first baseline
   - 写一个 pressure scenario，描述不给 skill 时最可能出现的错误
   - 记录基线失败：漏步骤、偷懒捷径、description 误导、结构失控、平台细节污染等
   - 环境支持独立 agent 时，优先用独立 agent 验证；不支持时，也要显式写出 baseline 场景与预期失败
3. 设计 discoverability
   - 先写 `name`
   - 再写 `description`，只描述何时使用，不总结 workflow
   - 用真实会被搜索到的触发词、症状、上下文增强可发现性
4. 设计结构
   - `SKILL.md` 保留核心原则、最小流程和纪律约束
   - 重型参考与模板拆到 `references/`
   - 可执行且重复出现的步骤才放 `scripts/`
   - 只有最终输出需要消费的素材才放 `assets/`
   - 默认以独立 skill 包组织，不预设当前仓库的特定目录层级
5. 写最小 skill
   - 先写成独立 skill 包
   - 只写能修正 baseline 失败的最小正文
   - 若已有相近 skill，优先 `adapt`，不要平行造轮子
6. 验证并补漏洞
   - 用同一 pressure scenario 复跑，确认行为已改变
   - 再补 1 到 2 个近邻场景，检查是否出现新的合理化路径
   - 一旦发现漏洞，补正文或下沉到 `references/`，再复验
7. 收口与同步
   - 只有目标工具需要时，才补分发适配副本
   - 若当前任务有自己的对齐机制，口径变化后先同步工作面，再继续执行
   - 没有 fresh validation evidence，就不要宣称 skill ready

## 纪律约束

- 不要把一次性复盘、任务日志或项目私规包装成通用 skill
- 不要把 workflow 摘要塞进 `description`
- 不要把研究、执行、验证、发布四种职责无限堆进一个 skill
- 不要默认把作者当前仓库的目录结构、记录路径或任务容器写进 skill 正文
- 不要把平台特定术语写进核心资产；只有显式做适配时才下沉到分发层
- 没有 baseline 或 fresh validation evidence，就不要说“这个 skill 已经可用”

## 渐进加载

只在当前意图需要时再读取参考文件：

- 判断该写 skill 还是别的资产：`references/authoring-checklist.md`
- 需要 frontmatter、结构拆分、目录卫生检查：`references/authoring-checklist.md`
- 需要 baseline / green / loophole plugging 模板：`references/validation-loop.md`
