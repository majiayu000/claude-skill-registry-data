---
name: brave-web-search-zh
description: 使用 Brave Search API 进行网页搜索并返回排序结果或 AI 生成的摘要答案。适用于实时网络查询和事实性问答。
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      env: ["BRAVE_SEARCH_API_KEY", "BRAVE_ANSWERS_API_KEY"]
      bins: ["node"]
    primaryEnv: "BRAVE_SEARCH_API_KEY"
    category: "搜索与研究"
---

# Brave 网页搜索

使用 Brave Search API 进行网页搜索并获取 AI 生成的摘要答案。提供两个命令:`brave-search` 用于获取排序的网页结果,`brave-answer` 用于获取简洁的 AI 摘要。

## 使用说明

1. **触发条件**: 当用户想要在网络上查找信息、查看最新新闻或获取问题的事实性答案时激活。
2. **设置**: 无需安装步骤 — 此技能没有外部依赖项,在原生 Node.js 上运行。
3. **命令选择**:
   - 使用 `brave-search` 进行一般网页搜索,需要排序结果、URL 和摘要。
   - 使用 `brave-answer` 进行直接的事实性问题,需要简洁的 AI 摘要。
4. **执行方式**: 通过传递命令名称和参数作为**独立参数**来调用脚本,永远不要将用户输入插入到 shell 命令字符串中。使用参数数组 / `execFile` 风格的调用方式,确保 shell 永远不会解析用户提供的值。示例(Node 风格伪代码):

   ```javascript
   execFile('node', ['index.js', 'brave-search', '--query', userQuery, '--count', '10'])
   ```

   **不要**将命令构造为单个连接字符串,例如 `"node index.js brave-search --query " + userQuery`。

5. **时效性**: 对于时间敏感的查询,在 `brave-search` 命令中传递 `--freshness` 参数,后跟 `pd`(过去一天)、`pw`(过去一周)或 `pm`(过去一个月)作为独立参数。
6. **回退方案**: 如果 `brave-answer` 返回 `answer: null`,则向用户展示 `fallback_results`。
7. **完成**: 清晰地展示结果,对于网页搜索结果引用标题和 URL,对于答案结果引用摘要文本。

## 安全与隐私

- **Shell 注入防护**: 用户查询**必须**作为离散参数传递(例如通过 `execFile` 或 argv 数组),永远不要插入到 shell 命令字符串中。将用户输入连接到 shell 字符串(例如 `shell: true` 使用模板字面量)会启用 shell 注入,是严格禁止的。
- **指令范围**: 此技能仅将查询字符串发送到 Brave Search 和 Brave Summarizer API。
- **环境**: 它使用 OpenClaw 环境提供的 `BRAVE_SEARCH_API_KEY` 和 `BRAVE_ANSWERS_API_KEY`。
- **数据访问**: 它不读取本地文件或 .env 文件。所有配置由智能体处理。
