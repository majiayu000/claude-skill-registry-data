---
name: ai-crawler-audit
description: 'Audit whether AI crawlers can reach and read one page, then name exactly what blocks them. Use when the user asks why ChatGPT, Claude, Perplexity, Gemini or Doubao never mentions their site, whether GPTBot or ClaudeBot is allowed in, what robots.txt, noindex, JS-only rendering, or a WAF is doing to AI access, or asks for an AI readability checkup of a URL. Scores the URL and returns the blocking reasons with evidence. For whether AI recommends the brand once access works, see ai-visibility. For the files AI reads first, see llms-txt.'
license: MIT
metadata:
  version: "1.8.0"
  homepage: https://github.com/Fangx-AI/geo-doctor
---

# AI 爬虫体检

只回答一个问题：**这个网址，AI 的爬虫能不能取到、能不能读懂正文。** 别的都不在这里做。

用用户的语言交流；本文件是中文的，读懂后用用户的语言转述。

## 什么时候用

- "为什么 ChatGPT / 豆包 / Perplexity 从来不提我的网站？"
- "我的站被 AI 爬虫挡了吗？" / robots.txt、GPTBot、ClaudeBot、PerplexityBot、Google-Extended、noindex、`X-Robots-Tag`、Cloudflare / WAF、JS 渲染的空壳页
- "给这个网址做个 AI 体检" / 想在 CI 里卡住退步

不接的活，交给邻居技能：AI 到底推荐谁 → `ai-visibility`；该写什么内容 → `ai-content-writer`；llms.txt 和事实站 → `llms-txt`。

## 三条必须守住

1. **分数只说明"抓取那一刻能否被机器取到并取出正文"。** 它不是品牌强度、不是搜索排名、不是被 AI 引用的概率。汇报时必须原话带上这一句，徽章上也是这么写的（`Technical audit only, not an AI ranking`）。
2. **每条结论都要有证据**：哪个请求、哪个状态码、哪段 HTML。没实际跑到的一项标"未验证"，不给分，也不许编。
3. **不承诺修完就会被推荐。** 能读到只是入场券。

## 怎么跑

以本 `SKILL.md` 所在目录为技能根，脚本在 `scripts/geo-audit.mjs`，零依赖。

```bash
node scripts/geo-audit.mjs https://example.com/pricing --lang zh --report geo/audit.md
node scripts/geo-audit.mjs https://example.com --phrase "团队版每月 299 元"
node scripts/geo-audit.mjs https://example.com --json --fail-under 80
node scripts/geo-audit.mjs https://example.com --badge geo/badge.svg --card geo/card.png
```

- `--phrase`：检查这句关键正文（价格、型号、核心承诺）是否出现在**原始 HTML** 里。出现不了，靠前端 JS 渲染才显示的内容，多数 AI 爬虫读不到。
- `--no-probe`：跳过"用 AI 爬虫 UA 再抓一次"的防火墙检查。只有明确不能对目标站发额外请求时才用，并在结论里注明这项没测。
- `--badge` 出 SVG 徽章，`--card` 出 1200×630 分享图（`.png` 需要本机有 Chrome 或 Edge，`--badge` 不要）。
- `--fail-under` 给 CI 用：低于分数退出码 1，参数写错退出码 2。

读不了文件、跑不了脚本时：按 `references/crawler-access.md` 做能做完的人工检查（`curl -A` 看 robots、看源码里有没有正文、看 `<meta name="robots">`），其余标"未验证"，**不要估一个分数**。

## 分数是怎么来的

- 每项检查有状态（pass / warn / fail / info）和权重，得分 = 实得权重 ÷ 总权重 × 100，四舍五入。
- **critical 项**（抓取失败、HTTP 非 2xx、robots.txt 读不到或读取异常、robots 明确挡搜索爬虫、以爬虫 UA 重抓被 WAF 拦、`X-Robots-Tag` 或 `<meta name="robots">` 的 noindex、正文为空、JS 空壳页等）**任何一项 fail，总分封顶 60**。
- 所以 60 分有两种含义：真的及格线以下，或者"就卡在一个致命项"。**看到 60 必须先看 critical 列表**，不要按"差一点及格"去解读。

## 读结果与写结论

1. 先按 critical 排，再按权重排；一条 critical fail 抵十条 warn。
2. 每个问题给三件事：**现象**（状态码/HTML 证据）、**原因**、**改法**（谁改、改哪一行）。
3. 区分三种"读不到"：**被规则挡**（robots / noindex，改配置）、**被中间层挡**（WAF、CDN 按 UA 拦，改规则）、**根本不在 HTML 里**（JS 渲染，改渲染或加服务端输出）。三者的改法完全不同，不要混写成"优化抓取"。
4. robots.txt 返回 404/405 不是"链接失效"：没有 robots.txt 按规范等于不限制。同一 URL 对不同 UA 返回不同状态是正常的。
5. 目标用户在海外时，顺带核对 `references/ai-sources-global.md` 里该放行的爬虫；国内用户看 `references/ai-sources-cn.md`。

## 产出

写进用户项目的 `geo/audit.md`：体检时间、URL、总分、critical 清单、逐项证据、按优先级排的修改建议。已有文件时追加新一节并标日期，不覆盖旧结论。

## 结束时

用 3 到 5 行告诉用户：分数、最致命的一两项、改完能解决什么、下一次什么时候复测。不要长篇报告塞进对话。
