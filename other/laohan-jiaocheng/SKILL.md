---
name: laohan-jiaocheng
version: 1.0
description: 教程路由器，输入关键词加载对应配置教程并按步骤引导安装。覆盖 claude-mem、CLAUDE.md、Chrome Gemini 侧边栏、Claude Code + 智谱 GLM、ECC 插件安装维护。Use when 用户说"教程""怎么配置""安装教程""怎么装"或提到"claude-mem""ecc""glm""gemini侧边栏""CLAUDE.md"等具体工具名+配置需求。本 skill 只管上述 5 项本地工具的配置教程；联网搜教程/搜心得/查最佳实践让位 laohan-sousuo（Jeffrey 2026-10-02 拍板，冲突时 sousuo 优先）。
argument-hint: [教程关键词，如 claude-mem / ecc / glm / gemini / claude-md]
---

# 老韩教程路由

根据关键词加载对应教程，按步骤引导用户完成配置，关键步骤验证结果。

## 核心理念

教程类 skill 的核心不是"讲知识"而是"帮用户跑通"。每个教程都必须验证结果——服务启动了吗、命令能用了吗。跑通比理解重要。

## 不适用场景

- 问"XX工具怎么用"（使用教程）→ 按 SKILL.md 内容直接回答，不走分步引导
- 问"帮我配置 XX"但路由表中没有对应教程 → 告诉用户目前只有 5 个教程，列出可选范围
- 问"写一个教程"（创建教程）→ 用 laohan-skillcreator 的流程

## 路由表

| 关键词匹配 | 教程文件 | 一句话说明 |
|-----------|---------|-----------|
| "claude-mem"/"litellm"/"记忆"/"健忘" | `references/claude-mem-litellm.md` | claude-mem + LiteLLM 让 Claude Code 用国产模型实现跨会话记忆 |
| "CLAUDE.md"/"claude-md"/"配置指南"/"四个原则" | `references/claude-md-guide.md` | CLAUDE.md 四个核心原则（想清楚再动手/能50行别200行/只改该改的/目标驱动执行） |
| "gemini"/"侧边栏"/"chrome gemini" | `references/gemini-sidebar-fix.md` | Chrome Gemini 侧边栏国内修复（Mac + Windows 双平台） |
| "glm"/"智谱"/"claude-code-glm"/"国产模型" | `references/claude-code-glm.md` | Claude Code 接入智谱 GLM 作为后端 |
| "ecc"/"插件"/"everything-claude-code" | `references/ecc-plugin-guide.md` | ECC 插件安装、rules 分发、hooks 加载机制 |

## 执行逻辑

1. **匹配教程**：从用户输入提取关键词，按路由表确定目标教程
   - **如果关键词匹配不到任何教程 → 列出 5 个可选教程，让用户选择**
2. **加载教程**：读取 `references/<对应文件>.md` 全文
   - **完成条件：** 文件存在且非空
3. **分步引导**：将教程内容按步骤呈现，每步完成后用户确认再进入下一步
4. **验证**：关键步骤执行后验证结果（服务启动、配置生效、命令可用）
   - **完成条件：** 验证命令返回成功（如 `curl /health` 返回 200、命令 `--version` 输出版本号）
5. **完成**：输出配置总结 + 下一步建议

## 教程源与同步

教程源文件在 `~/Documents/laohan-skills/docs/` 维护。本 skill 的 `references/` 是同步副本。

**更新流程**：
1. 修改 `docs/*.md`（源文件）
2. `cp docs/*.md laohan-jiaocheng/references/`（同步）
3. 如有新教程，同步后更新本路由表
4. `git add && git commit && git push`

**同步检查**（每次使用时执行）：
- 验证 `references/` 下 5 个文件均存在
- 如文件缺失，提示先同步：`cd ~/Documents/laohan-skills && cp docs/*.md laohan-jiaocheng/references/`
