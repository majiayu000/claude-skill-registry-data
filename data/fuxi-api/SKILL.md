---
name: fuxi-api
description: 使用 Vanna AI SQL 问答接口（伏羲环境）帮用户用自然语言查询伏羲数据库，例如“查询伏羲上的张博文准驾等级”等驾驶相关业务数据。
metadata:
  {
    "openclaw":
      {
        "emoji": "🧮",
        "requires": { "bins": ["node"] }
      },
  }
---

# Vanna Fuxi SQL（伏羲数据问答）

基于已部署的 Vanna AI SQL 问答服务（伏羲环境）接口：

- `POST https://vanna-ai-sql-api-ontest.inner.chj.cloud/ask`

当用户询问“伏羲上的数据”时（例如“我想查伏羲上的张博文准驾等级”“帮我查伏羲里某人的驾驶证信息”），使用本 skill 调用该接口并整理结果后回复用户。

## 触发场景（给模型看的）

当满足以下任意条件时，优先考虑使用本 skill：

- 用户明确提到“伏羲”“伏羲上的数据”“伏羲系统”“Vanna SQL 问答”等。
- 用户用自然语言问与驾驶/准驾等级/人员车辆信息等相关的问题，并你知道这些数据在伏羲库里。

示例触发语句：

- “我想查伏羲上的张博文准驾等级”
- “帮我看看伏羲里某个驾驶人的违规记录”
- “用 Vanna 那套 SQL 问答帮我看下这个人近期的驾驶情况”

## 调用方式

使用 `exec` 工具调用 Node.js 脚本：

```bash
node {baseDir}/scripts/ask.js "<自然语言问题>"
```

其中：

- `<自然语言问题>` 直接使用用户的问题文本，例如：  
  `我想查伏羲上的张博文准驾等级`

脚本会：

1. 向 `https://vanna-ai-sql-api-ontest.inner.chj.cloud/ask` 发送 `POST` 请求。
2. 请求体 JSON 结构遵循后端 `QuestionRequest` 模型：

   ```json
   {
     "question": "我想查伏羲上的张博文准驾等级",
     "visualize": false,
     "allow_llm_to_see_data": true,
     "model": null
   }
   ```

3. 得到形如 `QuestionResponse` 的 JSON：

   - `success`: 是否成功
   - `question`: 实际问句
   - `sql`: 生成并执行的 SQL
   - `data`: 查询结果（列表，元素为对象）
   - `explanation`: 对 SQL / 结果的解释（如果有）
   - 其他辅助字段（`visualization`, `data_markdown`, `error`, `execution_time` 等）

4. 将完整 JSON 输出到标准输出。

## 对话流程建议

1. 检查用户问题是否属于伏羲数据范围：  
   - 如果只是一般业务咨询，不需要查库，则按普通对话处理。  
   - 如果需要真实数据（例如“准驾等级”“近半年违章次数”等），用本 skill。

2. 调用脚本：

   ```bash
   node {baseDir}/scripts/ask.js "<用户原始问题>"
   ```

3. 读取脚本输出的 JSON，按以下规则总结回答给用户（用中文）：

   - 如果 `success == false` 或有 `error` 字段：
     - 告知用户“伏羲查询失败”，简要给出错误信息（避免泄露敏感内部栈信息）。
   - 如果 `success == true` 且 `data` 有内容：
     - 简要说明：你已经调用伏羲 SQL 问答接口并成功返回结果。
     - **若有 `sql` 字段且非空，请把生成的 SQL 展示给用户**（可用代码块包裹）。
     - 结合 `data` 和 `sql`/`explanation`，提炼用户最关心的信息：
       - 对于“准驾等级”类问题，只强调相关字段（例如某人的准驾等级、证件状态等）。
       - 如有多行数据，说明筛选条件（例如按最新记录、或者全部罗列）。
   - 尽量用自然语言解释，必要时可附上一小段表格或项目符号列表。

4. 如有歧义（例如伏羲数据里有多个同名“张博文”）：
   - 向用户说明存在同名记录。
   - 给出区分字段（如身份证号尾号、所属部门等），请用户补充信息后再调用一次接口。

## 注意事项

- 本 skill 假定远端接口已经在伏羲环境正确配置并可访问。  
- 如遇网络故障 / 5xx 等错误，先向用户说明是“后端服务不可用或网络异常”，再视情况建议稍后重试。
- 不要在对话中泄露完整内部 URL 日志，只说明是调用了“伏羲 SQL 问答接口”。

