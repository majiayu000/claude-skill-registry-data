---
name: generate-readme
description: Generate/update project README by scanning all plugins and tools. Use when user asks to "生成 README", "更新 README", "generate README", "update README".
allowed-tools: Glob, Read, Write
---

# 生成项目 README

自动扫描项目中的所有 plugins 和工具，生成简洁的 README.md。

## 操作流程

1. 读取 `.claude-plugin/marketplace.json` 获取所有 plugins
2. 对每个 plugin，读取其 `plugin.json` 获取名称和描述
3. 扫描 plugin 目录下的内容（skills, subagents, mcp 等）
4. 提取每个工具的名称和描述（读取 SKILL.md 时使用 limit 参数，如 10，只读取 frontmatter）
5. 生成 README.md

## README 格式

```markdown
# my-claude-marketplace

个人 Claude Code 工具集

- **{plugin-name}** - {plugin-description}
  - [Skill] **{skill-name}** - {skill-description}
  - [MCP] **{mcp-name}** - {mcp-description}
  - [Subagent] **{subagent-name}** - {subagent-description}

---

*自动生成*
```

## 注意事项

- 使用树状列表结构，体现 marketplace → plugin → tools 的层级关系
- 工具类型标签：[Skill], [MCP], [Subagent] 等
- 只包含名称和描述，不包含版本、作者等信息
- 描述应该只写核心功能，不列举实现细节（如技术栈、格式、配置等）
- 保持简洁
