---
name: web-search-plus-zh
version: 2.9.0
description: 智能自动路由的统一搜索技能。通过多信号分析自动选择 Serper（Google）、Tavily（研究）、Querit（多语言 AI 搜索）、Exa（神经网络）、Perplexity（AI 问答）、You.com（RAG/实时）和 SearXNG（隐私/自托管），并附带置信度评分。
tags: [search, web-search, serper, tavily, querit, exa, perplexity, you, searxng, google, multilingual-search, research, semantic-search, auto-routing, multi-provider, shopping, rag, free-tier, privacy, self-hosted, kilo]
metadata: {"openclaw":{"requires":{"bins":["python3","bash"],"env":{"SERPER_API_KEY":"optional","TAVILY_API_KEY":"optional","QUERIT_API_KEY":"optional","EXA_API_KEY":"optional","YOU_API_KEY":"optional","SEARXNG_INSTANCE_URL":"optional","KILOCODE_API_KEY":"optional — Perplexity 提供商需要（通过 Kilo Gateway）"},"note":"只需配置一个提供商的密钥即可。所有密钥均为可选。"}}}
---

# Web Search Plus

**不用纠结用哪个搜索引擎了，让技能替你选择。**

本技能连接 7 个搜索提供商（Serper、Tavily、Querit、Exa、Perplexity、You.com、SearXNG），并为每次查询自动选择最佳引擎。购物问题？→ Google 结果。研究问题？→ 深度研究引擎。需要直接答案？→ AI 合成并附带引用。重视隐私？→ 自托管方案。

---

## ✨ 有什么不同？

- **直接搜** — 无需思考该用哪个提供商
- **智能路由** — 分析你的查询并自动选择最佳提供商
- **7 个提供商，1 个接口** — Google 结果、研究引擎、神经搜索、AI 问答带引用、RAG 优化和隐私优先，全部整合
- **只需 1 个密钥** — 从任意一个开始，以后再添加更多
- **免费选项** — SearXNG 完全免费（自托管）

---

## 🚀 快速开始

```bash
# 交互式设置（首次使用推荐）
python3 scripts/setup.py

# 或手动：复制配置文件并添加密钥
cp config.example.json config.json
```

向导会逐一介绍每个提供商、收集 API 密钥并配置默认设置。

---

## 🔑 API 密钥

只需 **一个** 密钥即可开始使用。以后可以添加更多提供商以获得更全面的覆盖。

| 提供商 | 免费额度 | 擅长 | 注册 |
|----------|-----------|----------|---------|
| **Serper** | 2,500 次/月 | 购物、价格、本地、新闻 | [serper.dev](https://serper.dev) |
| **Tavily** | 1,000 次/月 | 研究、解释、学术 | [tavily.com](https://tavily.com) |
| **Querit** | 联系销售/免费额度不同 | 多语言 AI 搜索、国际资讯 | [querit.ai](https://querit.ai) |
| **Exa** | 1,000 次/月 | "类似 X"、创业公司、论文 | [exa.ai](https://exa.ai) |
| **Perplexity** | 通过 Kilo | 带引用的直接回答 | [kilo.ai](https://kilo.ai) |
| **You.com** | 有限额度 | 实时资讯、AI/RAG 上下文 | [api.you.com](https://api.you.com) |
| **SearXNG** | **免费** ✅ | 隐私、多源、$0 费用 | 自托管 |

**设置密钥：**

```bash
# 方式 A：.env 文件（推荐）
export SERPER_API_KEY="你的密钥"
export TAVILY_API_KEY="你的密钥"
export QUERIT_API_KEY="你的密钥"

# 方式 B：config.json
{ "serper": { "api_key": "你的密钥" } }
```

---

## 🎯 什么时候用哪个提供商

| 我想... | 提供商 | 示例查询 |
|--------------|----------|---------------|
| 查产品价格 | **Serper** | "iPhone 16 Pro Max 价格" |
| 查附近的餐厅/商店 | **Serper** | "我附近最好的披萨" |
| 了解某事的原理 | **Tavily** | "HTTPS 加密是怎么工作的" |
| 做深度研究 | **Tavily** | "2024 年气候变化研究" |
| 跨语言搜索/国际资讯 | **Querit** | "德国最新 AI 政策动态" |
| 查找类似 X 的公司 | **Exa** | "类似 Notion 的创业公司" |
| 查找研究论文 | **Exa** | "transformer 架构论文" |
| 获取带来源的直接答案 | **Perplexity** | "柏林这周末有什么活动" |
| 了解某事的最新状态 | **Perplexity** | "以太坊升级进展如何" |
| 获取实时信息 | **You.com** | "最新 AI 监管新闻" |
| 不被追踪地搜索 | **SearXNG** | 任何内容，私密搜索 |

**专业提示：** 正常搜索就好！自动路由能正确处理大多数查询。需要时用 `-p provider` 手动覆盖。

---

## 🧠 自动路由的工作原理

技能会分析你的查询并选择最佳提供商：

```bash
"iPhone 16 价格"              → Serper（购物关键词）
"量子计算是怎么工作的"        → Tavily（研究问题）
"德国最新 AI 政策动态"        → Querit（多语言 + 时效性）
"类似 stripe.com 的公司"      → Exa（检测到 URL，相似性搜索）
"格拉茨这周末的活动"          → Perplexity（本地 + 直接回答）
"最新 AI 新闻"                → You.com（实时意图）
"私密搜索"                    → SearXNG（隐私关键词）
```

**选错了怎么办？** 手动覆盖：`python3 scripts/search.py -p tavily -q "你的查询"`

**调试路由：** `python3 scripts/search.py --explain-routing -q "你的查询"`

---

## 📖 使用示例

### 让自动路由选择（推荐）

```bash
python3 scripts/search.py -q "特斯拉 Model 3 价格"
python3 scripts/search.py -q "解释机器学习"
python3 scripts/search.py -q "德国最新 AI 政策动态"
python3 scripts/search.py -q "类似 Figma 的创业公司"
```

### 指定提供商

```bash
python3 scripts/search.py -p serper -q "柏林天气"
python3 scripts/search.py -p tavily -q "量子计算" --depth advanced
python3 scripts/search.py -p querit -q "德国最新 AI 政策动态"
python3 scripts/search.py -p exa --similar-url "https://stripe.com" --category company
python3 scripts/search.py -p you -q "突发科技新闻" --include-news
python3 scripts/search.py -p searxng -q "linux 发行版" --engines "google,bing"
```

---

## ⚙ 配置

```json
{
  "auto_routing": {
    "enabled": true,
    "fallback_provider": "serper",
    "confidence_threshold": 0.3,
    "disabled_providers": []
  },
  "serper": {"country": "us", "language": "en"},
  "tavily": {"depth": "advanced"},
  "exa": {"type": "neural"},
  "you": {"country": "US", "include_news": true},
  "searxng": {"instance_url": "https://your-instance.example.com"}
}
```

---

## 📊 提供商对比

| 特性 | Serper | Tavily | Exa | Perplexity | You.com | SearXNG |
|---------|:------:|:------:|:---:|:----------:|:-------:|:-------:|
| 速度 | ⚡⚡⚡ | ⚡⚡ | ⚡⚡ | ⚡⚡ | ⚡⚡⚡ | ⚡⚡ |
| 直接回答 | ✗ | ✗ | ✗ | ✓✓ | ✗ | ✗ |
| 引用来源 | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| 事实准确性 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 语义理解 | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| 完整页面内容 | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ |
| 购物/本地 | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ |
| 查找相似页面 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| RAG 优化 | ✗ | ✓ | ✗ | ✗ | ✓✓ | ✗ |
| 隐私优先 | ✗ | ✗ | ✗ | ✗ | ✗ | ✓✓ |
| API 费用 | $$ | $$ | $$ | 通过 Kilo | $ | **免费** |

---

## ❓ 常见问题

### 我需要为所有提供商都配 API 密钥吗？
**不需要。** 只需为你想用的提供商配置密钥。先从一个开始（推荐 Serper），以后再添加。

### 我应该从哪个提供商开始？
**Serper** — 最快、最便宜、最大免费额度（每月 2,500 次查询），且能很好地处理大部分查询。

### 免费额度用完了怎么办？
技能会自动回退到你配置的其他提供商。或者切换到 SearXNG（无限制、自托管）。

### 费用大概多少？
- **免费额度：** 2,500（Serper）+ 1,000（Tavily）+ 1,000（Exa）= 每月 4,500+ 次免费搜索
- **SearXNG：** 完全免费（自托管在 VPS 上约 $5/月）
- **付费套餐：** 根据提供商不同，约 $10-50/月起

### SearXNG 真的隐私吗？
**自托管的话，是的。** 你控制服务器，无追踪、无画像。公共实例取决于运营方的政策。

### 怎么搭建 SearXNG？
```bash
# Docker（5 分钟）
docker run -d -p 8080:8080 searxng/searxng
```
然后在 `settings.yml` 中启用 JSON API。参见 [docs.searxng.org](https://docs.searxng.org/admin/installation.html)。

### 为什么我的查询被路由到了"错误"的提供商？
有些查询存在歧义。用 `--explain-routing` 查看原因，需要时用 `-p provider` 手动覆盖。

---

## 🔄 自动回退

如果某个提供商失败（达到频率限制、超时、错误），技能会自动尝试下一个提供商。发生回退时，你会在响应中看到 `routing.fallback_used: true`。

---

## 📤 输出格式

```json
{
  "provider": "serper",
  "query": "iPhone 16 价格",
  "results": [{"title": "...", "url": "...", "snippet": "...", "score": 0.95}],
  "routing": {
    "auto_routed": true,
    "provider": "serper",
    "confidence": 0.78,
    "confidence_level": "high"
  }
}
```

---

## ⚠ 重要提示

**Tavily、Serper 和 Exa 不是 OpenClaw 核心提供商。**

❌ 不要修改 `~/.openclaw/openclaw.json` 来配置这些  
✅ 使用本技能的脚本 — 密钥会从 `.env` 自动加载

---

## 🔒 安全

**SearXNG SSRF 防护：** SearXNG 实例 URL 经过纵深防御验证：
- 仅允许 `http`/`https` 协议
- 阻止云元数据端点（169.254.169.254、metadata.google.internal）
- 解析主机名并阻止私有/内部 IP（环回、RFC1918、链路本地、保留地址）
- 有意在内网自托管的运营方可以设置 `SEARXNG_ALLOW_PRIVATE=1`

## 📚 更多文档

- **[FAQ.md](FAQ.md)** — 更多问题的详细解答
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — 常见错误修复
- **[README.md](README.md)** — 完整技术参考

---

## 🔗 快速链接

- [Serper](https://serper.dev) — Google 搜索 API
- [Tavily](https://tavily.com) — AI 研究搜索
- [Exa](https://exa.ai) — 神经网络搜索
- [Perplexity](https://www.perplexity.ai) — AI 合成回答（通过 [Kilo Gateway](https://kilo.ai)）
- [You.com](https://api.you.com) — RAG/实时搜索
- [SearXNG](https://docs.searxng.org) — 隐私优先元搜索
