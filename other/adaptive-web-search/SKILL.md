---
name: adaptive-web-search
description: 针对不同 Provider 的参数差异进行适配，特别处理 Gemini 和 Grok 不支持 freshness 的限制，并解决 API Key 缺失及抓取时的 Cookie 异常。
version: 1.6
evolved_from: adaptive-web-search
evolution_type: FIX
---

# adaptive-web-search

## 适用场景
1. 当调用 `web_search` 工具，但目标 Provider 对高级过滤参数（`freshness`, `language`）支持不一致时（尤其是 Gemini 和 Grok 不支持 `freshness`）。
2. 当遇到 `missing_brave_api_key` 等配置错误导致搜索不可用时。
3. 当 `web_fetch` 遇到 `Too many redirects` 或 `cookies_not_supported` 等抓取异常时。

## 步骤
1. **Provider 能力预检与参数重构**：
   - **Gemini/Grok 专项处理**：在调用前检查，若 `provider` 为 `gemini` 或 `grok` 且存在 `freshness` 参数：
     - **优先策略**：尝试将 `provider` 切换为 `brave` 或 `perplexity`。
     - **降级策略**：若必须使用当前 Provider，将 `freshness` 映射为自然语言（如 `pw` -> "past week"）并入查询词 `q`，然后**必须移除** `freshness` 参数。
   - **Brave / Perplexity**：保留原生参数。

2. **执行请求与错误捕获**：
   - 调用 `web_search`。
   - **处理 `unsupported_freshness` 错误**：若未预检导致报错（常见于 Grok 返回 `unsupported_freshness`），立即移除 `freshness` 参数，将时间要求写进 `q` 后重试。
   - **处理 API Key 缺失**：若返回 `missing_brave_api_key`：
     - 尝试切换至已配置的 Provider（如 `google`, `bing`）。
     - 若无可用 Provider，提示用户运行 `openclaw configure --section web`。

3. **处理抓取异常**：
   - **Cookie 缺失错误**：若 `web_fetch` 返回 URL 包含 `error=cookies_not_supported`：
     - 说明目标网站（如 Nature, IEEE）有严格的反爬或 Cookie 校验。
     - **对策**：不要重试该 URL，尝试寻找该文章的 DOI 链接或在搜索结果中寻找其他镜像/预印本来源。
   - **重定向过多**：移除 URL 中的 `utm_` 等追踪参数，尝试访问父级路径。

4. **参数映射表**：
   - `pd` (past day) -> "past 24 hours"
   - `pw` (past week) -> "past week"
   - `pm` (past month) -> "past month"
   - `py` (past year) -> "past year"

## 工具和命令
- **配置命令**：`openclaw configure --section web`
- **环境变量**：`BRAVE_API_KEY`, `GOOGLE_SEARCH_API_KEY`, `PERPLEXITY_API_KEY`, `GROK_API_KEY`

## 注意事项
- **强制限制**：向 **Gemini** 或 **Grok** 传递 `freshness` 会直接导致 `400` 错误或 `unsupported_freshness` 异常，必须在调用工具的 JSON 构造阶段拦截。
- **抓取失败降级**：对于 Nature 等学术网站，`web_fetch` 经常因 Cookie 校验失败。此时应优先依赖 `web_search` 返回的 `snippet`（摘要）信息，而非强行抓取全文。
- **语言适配**：若指定 `language="zh"`，建议在 `q` 中加入 "中文" 关键词以增强效果。

## 示例
**场景 1：Grok 搜索适配（预检）**
- **意图**：使用 Grok 搜索过去 24 小时的 AI 融资新闻。
- **动作**：
  ```json
  // 原始意图：web_search(q="AI funding news", freshness="pd", provider="grok")
  // 修正为：
  web_search(q="AI funding news past 24 hours", provider="grok") 
  ```

**场景 2：处理 Grok 返回的 unsupported_freshness 报错**
- **输入**：`web_search` 返回 `{"error": "unsupported_freshness", "message": "freshness filtering is not supported by the grok provider..."}`。
- **动作**：自动重试 `web_search(q="[原关键词] past month", provider="grok")`（移除 freshness 参数，将 pm 映射为自然语言）。

**场景 3：抓取遇到 Cookie 限制**
- **输入**：`web_fetch` 返回 `finalUrl` 包含 `error=cookies_not_supported`。
- **响应**：告知用户：“目标网站 Nature 启用了 Cookie 校验，无法直接抓取。已根据搜索摘要为您总结：[摘要内容]。”