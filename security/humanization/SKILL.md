---
name: humanization
description: Humanize local-file prose and UI text across six locales. Use automatically only when a task will create or update a local file containing prose or audience-facing copy; exclude chat-only output. Explicit invocation remains available.
---

# Humanization 4.0.0 (MAGA adaptation)

## MAGA 默认出口

当前任务将在本地文件中写入或修改面向人阅读的自然语言时，自动执行一次本 Skill。
唯一的自动判据是：本次工作是否会产生本地文件变更？没有本地文件变更就不自动触发。
文章、故事和报告使用 `prose`；Markdown 文档、保存为文件的邮件或消息、产品或营销
内容使用 `copy`；网页或应用源码、资源文件中附着在控件、状态和用户流程上的文字
使用 `ui-microcopy`；写给设计、开发或交接人员的界面行为说明使用 `ui-description`。

用户明确指定语言时使用该 locale；否则在会话语言清楚时将它记录为显式 locale。
静默推断 format 和 surface，不因 Humanization 的触发、locale、format 或 surface 向
用户提问，也不声明、引用或解释本 Skill 已运行。无法安全判断且选择会改变事实、承诺、
隐私或 CTA 时，保留原内容或返回 `no_change`。代码、命令、路径、URL、标识符、
placeholder、变量、ICU、markup、数据、机器协议和逐字引用不进入语言改写；
只处理文件中真正面向人阅读的自然语言。仅在聊天中返回的普通问答、解释、文章、邮件
草稿、诊断汇报、状态总结、建议、下一步、确认、工具结果和 Git 状态一律不自动触发，
即使它们很长、使用 Markdown 排版、可直接复制或以后可能被分享。用户仍可显式调用
本 Skill。短而准确的文件内容可以保持短，`no_change` 是有效结果。

先用通用契约判断候选信息是否属于当前表面，再读取一个语言档案和一个格式模块完成写作或改稿。不要自动猜测混合文本的 locale，也不要把某种语言的禁令提升为全局规则。

## 按需执行

先读取 [编辑与校验](references/routed-editing.md)，按输入选择一个 locale 和
一个 format，保留事实与技术结构。`author_sample` 只用于用户明确指定的本次
表达校准，不为本 Skill 单独追问。普通改稿只处理实际变更的文字，并采用一次
直接相关的验证；交付作品本身。

只有用户明确要求完整审计、逐项盘点或覆盖回执时，才读取
[完整审计](references/full-audit.md)。旧的 `web-microcopy` 与
`check_prose.py` 入口继续兼容。
