---
name: conversation-json-to-md-cn
description: 当用户需要将聊天导出 JSON 拆分为按会话保存的 Markdown，并保留用户与助手问答结构时使用。
---

# Conversation JSON 转 Markdown（中文）

## Overview

将用户提供的聊天导出 JSON 转换为多个结构清晰的 Markdown 文件，并统一为问答结构。流程会按会话拆分文件，只保留用户与助手问答，保留回答中的 Markdown，并在导出后做一次命名和标题结构的二次整理。

## 何时使用

当用户有以下需求时使用本技能：
- 把一个对话导出 JSON 拆成多个 `.md`
- 一个会话对应一个 Markdown 文件
- 只保留用户与助手问答内容
- 问题作为标题，回答统一为 `回答`
- 导出后再做一次命名和标题二次格式化

## 不要使用

以下场景不应使用本技能：
- 与 JSON 对话导出无关的普通文本改写
- 非会话数据结构处理任务
- 用户要的是语义总结而非结构化导出

## 使用说明

1. 必须读取用户明确提供的输入文件路径，不假设默认文件名。
2. 自动识别 JSON 结构并提取会话。
3. 每个会话导出为一个 Markdown 文件。
4. 仅保留用户/助手问答内容。
5. 问答格式固定为：
   - `## <问题文本>`
   - `### 回答`
6. 保留回答正文的 Markdown，并将回答内部标题整体降级 1 级。
7. 导出完成后执行一轮独立二次格式化检查与修正。

## 支持的输入结构

脚本可识别以下常见格式：
- DeepSeek/ChatGPT 类 `mapping/root/children/fragments`
- Qwen 类 `data[].chat.messages[]` + `content_list`（优先 `phase=answer`）
- Claude 网页导出 `list[{ name, chat_messages: [...] }]`
- 通用消息数组 `messages/history/conversations/dialog/turns`
- 成对问答字段 `question-answer`、`prompt-response`、`input-output`

如果结构无法识别，停止并让用户提供样例片段，再扩展解析规则。

## 运行脚本

```bash
python3 scripts/convert_conversations.py \
  --input /path/to/<用户提供>.json \
  --output-dir /path/to/conversations_md \
  --clean
```

## 输出格式（固定）

```md
# <会话标题>

## <用户问题1>
### 回答
<助手回答 Markdown>

## <用户问题2>
### 回答
<助手回答 Markdown>
```

## 二次格式化流程（独立步骤）

导出后，对输出目录执行二次格式化：

1. 文件名规范化：
- 保持“仅会话标题”命名
- 清理非法字符
- 重名补齐 ` (2)`、` (3)` 序号

2. 标题结构规范化：
- 一级标题仅保留会话标题：`# <会话标题>`
- 每个问题必须是二级标题
- 每个回答必须是 `### 回答`

3. 回答正文规范化：
- 保留 Markdown
- 内部标题降级 1 级，避免与外层结构冲突

4. 结果复检：
- 发现不符合规则的文件时逐个修正后再交付

## 验证清单

- 导出文件数与识别到的会话数一致
- 文件名无随机后缀
- 文件中不出现 `## REQUEST` / `## RESPONSE`
- 回答块统一为 `### 回答`
- Markdown 预览渲染正常
