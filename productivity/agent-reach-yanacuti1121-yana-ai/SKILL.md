---
name: agent-reach
description: "Use when an agent needs to read the internet without paid API keys — Twitter/X, Reddit, YouTube, Bilibili, GitHub, TikTok, Xiaohongshu, RSS, web pages. Triggers on: 'agent-reach', 'agent đọc internet', 'đọc Twitter không API', 'đọc Reddit không API', 'agent xem YouTube', 'agent đọc Bilibili', 'agent đọc B站', 'agent đọc XHS', 'agent đọc Xiaohongshu', 'read social media free', 'agent internet eyes', 'no API key scraping', 'unified social reader'."
---

# Agent Reach Skill
# Source: Panniantong/Agent-Reach (MIT) — pluggable channel design, no paid APIs
# Tier: TIER 3 — PRODUCTIVITY

Cho agent đọc 14+ nền tảng internet mà không cần API key trả phí.
Mỗi channel dùng một open-source CLI backend riêng.

**Do NOT use for:** bypass auth, collect private data, spam, DDOS.

---

## Khi nào dùng

- Agent cần đọc Twitter/Reddit/YouTube/Bilibili mà không có API key
- Cần tổng hợp thông tin từ nhiều nền tảng trong 1 workflow
- Muốn agent đọc nội dung tiếng Trung (B站, XHS, V2EX, Weibo)
- Research task cần nguồn thực tế, không qua wrapper trả phí

**Do NOT use for:** `exa-search` (đã có, cover search API), `browser-use` (full browser automation).

---

## Cài đặt

```bash
# Nói với agent: cài Agent Reach
pip install agent-reach

# Hoặc để agent tự cài qua script
curl -fsSL https://raw.githubusercontent.com/Panniantong/Agent-Reach/main/install.sh -o /tmp/agent-reach-install.sh
# Inspect first: head -40 /tmp/agent-reach-install.sh — then run if safe:
bash /tmp/agent-reach-install.sh
```

Sau khi cài, agent đọc docs được register tự động.

---

## Platform Patterns

### Web pages (không cần cài thêm)

```bash
# Jina Reader — render JS page thành markdown
curl https://r.jina.ai/https://example.com

# Với header để bypass một số block
curl -H "X-Return-Format: markdown" https://r.jina.ai/https://example.com
```

### Twitter / X

```bash
# Tìm kiếm tweet
twitter search "AI agent 2025" --limit 20

# Timeline user
twitter user @username --limit 30

# Không cần API key — dùng twitter-cli backend
```

### Reddit

```bash
# Đọc subreddit
rdt-cli r/MachineLearning --limit 10

# Tìm kiếm
rdt-cli search "LLM agent" --subreddit r/LocalLLaMA
```

### YouTube / Bilibili

```bash
# Lấy transcript YouTube
yt-dlp --write-auto-sub --skip-download --sub-format vtt "https://youtube.com/watch?v=ID"

# Metadata + description
yt-dlp --dump-json "https://youtube.com/watch?v=ID" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d['title'], d['description'][:500])
"

# Bilibili — cùng cú pháp
yt-dlp --dump-json "https://bilibili.com/video/BVXXXX"
```

### Xiaohongshu (XHS / 小红书)

```bash
# Đọc post
xhs-cli post POST_ID

# Search
xhs-cli search "关键词" --limit 10
# Cần login lần đầu: xhs-cli login
```

### V2EX / Weibo / Xueqiu

```bash
# V2EX — qua RSS (không cần login)
python3 -c "import feedparser; f=feedparser.parse('https://www.v2ex.com/index.xml'); [print(e.title, e.link) for e in f.entries[:5]]"

# Weibo trending (via weibo-cli nếu cài)
weibo-cli trending --limit 10

# Xueqiu (stock discussion) — qua RSS public
python3 -c "import feedparser; f=feedparser.parse('https://xueqiu.com/hq/rss'); [print(e.title) for e in f.entries[:5]]"
```

### RSS / Podcast

```python
import feedparser
feed = feedparser.parse("https://example.com/feed.xml")
for entry in feed.entries[:5]:
    print(entry.title, entry.link)
```

### Exa AI — semantic search (free MCP tier)

```bash
# Cài Exa MCP (free, không cần API key với public tier)
npx @modelcontextprotocol/inspector exa-mcp

# Dùng trong workflow — semantic search thay vì keyword
# Exa MCP trả về: title, URL, highlight, published date
# Tốt hơn Google search cho research use cases
```

**Lưu ý:** `exa-search` skill dùng paid Exa API. Exa MCP free tier ≠ paid tier.
Dùng Exa MCP khi cần semantic search; dùng platform CLIs ở trên khi cần nội dung cụ thể.

### GitHub (via gh CLI)

```bash
# Trending repos
gh api "search/repositories?q=stars:>1000+created:>2025-01-01&sort=stars" \
  --jq '.items[:5] | .[] | "\(.stargazers_count) \(.full_name) — \(.description)"'

# README của repo
gh api "repos/owner/repo/readme" --jq '.content' | base64 -d
```

---

## Multi-platform workflow

```python
# Tổng hợp từ nhiều nguồn cho 1 topic
import subprocess, json

topic = "AI agent 2025"

# Twitter
tw = subprocess.run(["twitter", "search", topic, "--limit", "5"],
                    capture_output=True, text=True)

# Reddit
rd = subprocess.run(["rdt-cli", "search", topic, "--limit", "5"],
                    capture_output=True, text=True)

# Web
import urllib.request
web = urllib.request.urlopen(f"https://r.jina.ai/https://news.ycombinator.com/").read()

print("=== Twitter ===\n", tw.stdout[:500])
print("=== Reddit ===\n", rd.stdout[:500])
print("=== Web ===\n", web[:500].decode())
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu dùng OpenAI browsing (trả phí) khi agent-reach đủ
❌ FAIL nếu nhầm Exa MCP free tier với paid Exa API — đây là 2 thứ khác nhau
❌ FAIL nếu không cài backend CLI trước khi gọi (twitter-cli, rdt-cli, yt-dlp)
❌ FAIL nếu dùng để collect private/protected content
✅ PASS khi: CLI backend trả về data, không có rate-limit error, không cần API key
```

## See also
- `exa-search` — search API có trả phí, kết quả structured hơn
- `browser-use` — full browser automation khi cần JS render
- `terminal--reddit-insights` — Reddit analytics chuyên sâu
- `terminal--youtube-transcription` — transcript pipeline đầy đủ
