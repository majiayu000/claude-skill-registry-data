---
name: laohan-sousuo
version: 1.0
description: 老韩联网搜索查证——开发中不确定的技术问题先查再判断，三路检索（官方文档/GitHub issue/社区心得）+ 来源标注输出。优先级高于其他搜索类 skill。Use when 用户说"上网搜""上网搜索""搜索""搜索教程""查心得""搜一下""查一下""帮我查""查证""先查再说""别凭记忆""别人怎么解决""踩坑""最佳实践"，或开发/写代码/技术判断前对 API 用法、库版本行为、配置项语义、报错归因、兼容性不确定时。与 laohan-jiaocheng 等搜索类 skill 冲突时本 skill 优先（Jeffrey 2026-10-02 拍板）。
argument-hint: [搜索问题，如 "Tauri 怎么拿 HttpOnly cookie" / "为什么报 XXX 错"]
---

# 老韩搜索（laohan-sousuo）

联网查证引擎：不确定的技术问题先查再判断，结论必须带来源标注。

## 为什么存在

Jeffrey 观察（2026-10-02 钉死）：开发中经常不主动查教程、凭记忆做判断，经常出错，过去靠人工提醒"上网查下教程"。本 skill 把"先查再说"固化为默认行为。配套条款在 `~/.claude/rules/workflow.md`「技术断言前置查证」——rules 管"必须查"（每次会话无条件加载），本 skill 管"怎么查"。

## 优先级与让位

普通搜索类意图优先命中本 skill，由本 skill 内部路由工具：

| 意图 | 归属 |
|------|------|
| 上网搜 / 搜索 / 搜教程 / 查心得 / 查证 / 查一下怎么用 | **本 skill**（其他搜索 skill 让位） |
| 装软件 / 配置工具（claude-mem、ECC 等 5 个本地教程） | laohan-jiaocheng |
| AI 资讯 / 日报 / 热点 | aihot |
| 平台内容下载、评论、博主数据 | laohan-xiazai |
| 视频号下载、JS 渲染/反爬抓取降级 | 见 `~/.claude/rules/cli-tools.md` 总路由 |

## 三路检索（按问题类型选路线）

| 问题类型 | 路线 | 动作 |
|---------|------|------|
| API 用法 / 配置语义 / 参数含义 | 官方文档 | anysearch search（`--content_types doc`）→ 命中官方 URL → anysearch extract 读原文 |
| 报错归因 / 版本兼容 / "为什么不行" | GitHub issue | `gh search issues "关键词" --repo owner/repo`、`gh api repos/:owner/:repo/releases`；issue 比搜索引擎准（2026-09-30 实证：WebSearch 自我怀疑误判，gh 逐一核验 9 个 issue 全真实） |
| "别人怎么解决" / 踩坑心得 / 最佳实践 | 社区心得 | anysearch（含 reddit/blog 结果）→ agent-reach（平台）→ WebFetch 读原文 |

问题跨类时（如"这个 API 为什么报错"）issue + 官方文档并查，交叉印证。

## 工具链与降级

1. **anysearch**（默认引擎）：

   ```bash
   python3 ~/.claude/skills/anysearch/scripts/anysearch_cli.py search "query" --max_results 5
   # 批量：batch_search --queries '[{"query":"q1"},{"query":"q2"}]'
   # 读正文：extract "URL"
   ```

   端点无关（本地 CLI 调 api.anysearch.com），不占智谱搜索额度；huo 端点 WebSearch 403 时唯一可用通用搜索（2026-10-02 实测）。已加载 anysearch skill 时优先用其 runtime.conf 配置的命令。
2. **WebSearch 原生**：anysearch 失败/限额时降级。注意：cc 端点=智谱 web_search_prime 后端（占智谱额度，常 429 code 1310）；huo 端点 403 不可用。2026-10-03 起 `pre:websearch-to-anysearch` hook（10 目录）拦截 WebSearch 并在 deny reason 里注入 anysearch 命令——被拦即按 reason 里的命令跑 anysearch，不要重试 WebSearch（见 `~/.claude/rules/custom-hooks.md`）。
3. **gh**：GitHub 相关问题直接用，不经过搜索引擎。
4. **WebFetch / anysearch extract**：已知 URL 读正文。

## 输出合同（强制）

每次查证输出必须含：

1. **结论**：直接回答问题
2. **来源标注**：`(verified: URL)`（沿用 anti-patterns #18 格式）；无标注 = 违规
3. **版本/日期**：来源的版本号或发布日期——API 随版本变，旧教程会骗人
4. **记忆冲突**：查证结果与旧记忆冲突时明说"记忆是错的，实际是 X"
5. **查不到**：如实说"未查到可靠来源，以下是推断"，禁止推断冒充查证

## 安全边界

- 敏感信息（密钥、内部数据、未公开业务）不进搜索词——anysearch/WebSearch 都把查询发给第三方
- 查询词最小化：只放技术关键词，不带业务上下文

## 安装与验证

真身：`~/Documents/laohan-skills/laohan-sousuo/`（git 仓库）。

```bash
# symlink（已建则跳过）
ln -s ~/Documents/laohan-skills/laohan-sousuo ~/.agents/skills/laohan-sousuo
ln -s ../../.agents/skills/laohan-sousuo ~/.claude/skills/laohan-sousuo

# 验证
readlink ~/.claude/skills/laohan-sousuo   # 应输出 ../../.agents/skills/laohan-sousuo
python3 ~/.claude/skills/anysearch/scripts/anysearch_cli.py search "test" --max_results 1  # CLI 通
```
