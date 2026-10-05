---
name: agent-reach
description: Give your AI agent eyes to see entire internet - Read & search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu - one CLI, zero API fees - Use when user says 全网调研, 帮我调研, research whole internet, search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, read webpage, RSS, etc.
---

# Agent Reach - Internet Eyes - Free Capability Layer

> Inspired by https://github.com/Panniantong/agent-reach - Give your AI agent eyes to see entire internet - Read & search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu — one CLI, zero API fees

## What is Agent Reach?

Agent Reach is a capability layer, not another tool. It does selection, installation, health check, routing - not underlying reading itself. Reading by Agent directly calling upstream tools, no wrapper.

Original pain points it solves (same as Hermus Free):
- YouTube tutorial what does it say -> Can't get subtitles
- Search Twitter about product -> Twitter API paid
- Reddit bug -> 403 blocked, server IP banned
- XiaoHongShu -> Must login
- Bilibili tech video summary -> Generic download blocked
- Web search -> Paid or low quality
- Web page -> HTML tags not readable
- GitHub repo what does it do? -> Auth config troublesome
- RSS -> Need to code

## Supported Platforms (Free, Zero API Fees)

| Platform | Zero Config (No Auth) | Config Unlocks | How Config (Free) |
|----------|----------------------|----------------|-------------------|
| 🌐 Web | Read any webpage | — | No config - Jina Reader free |
| 📺 YouTube | Subtitle extraction + video search | — | No config - yt-dlp free |
| 📡 RSS | Read any RSS/Atom | — | No config - feedparser free |
| 🔍 Full web search | — | Full semantic search | Auto config MCP free no key - DuckDuckGo free |
| 📦 GitHub | Read public repo + search | Private repo, Issue/PR, Fork | Tell Agent "help me login GitHub" - gh CLI |
| 🐦 Twitter/X | Read single tweet | Search tweets, timeline, long article | Tell Agent "help me config Twitter" - Cookie-Editor manual export free local |
| 📺 Bilibili | Search + video details (bili-cli, no login) | Subtitle (OpenCLI) | Tell Agent "help me config Bilibili" |
| 📖 Reddit | — (no zero-config: anonymous blocked) | Search + read posts/comments | Desktop OpenCLI browser login or rdt-cli + Cookie free |
| 📘 Facebook | — | Search, homepage, Feed, group list | Desktop OpenCLI Chrome session free |
| 📷 Instagram | — | User search, Profile, recent posts, Explore | Desktop OpenCLI Chrome session free |
| 📕 XiaoHongShu | — | Search, reading, comments | OpenCLI Chrome session free; MCP/Cookie-Editor |
| 💼 LinkedIn | Jina Reader public page | Profile details, company, job search | Tell Agent "help me config LinkedIn" |
| 💻 V2EX | Hot posts, node posts, post details+replies, user info | — | No config |
| 📈 Xueqiu | Stock行情, search stock, hot posts, hot stock ranking | — | Tell Agent "help me config Xueqiu" |
| 🎙️ Xiaoyuzhou podcast | — | Podcast audio to text Whisper free Key | Tell Agent "help me config Xiaoyuzhou podcast" |

> Don't know how to config? Directly tell Agent "help me config XXX", it knows what needed, guides step by step.

Cookie only locally, not uploaded, code open source reviewable. Local computer no proxy needed. Proxy only for server ~$1/month.

## Tools - Zero API Fees, Free

**Core:**
- `web_read(url)` - Any webpage via Jina AI Reader https://r.jina.ai/http:// free
- `rss_read(rss_url)` - RSS via feedparser free
- `youtube_transcript(video_url)` - YouTube subtitle via yt-dlp free no config
- `youtube_search(query)` - YouTube search via ytsearch or DuckDuckGo fallback free
- `github_read(repo, path)` - GitHub public repo via gh CLI or API free no key
- `github_search(query)` - GitHub search API free
- `v2ex_hot()` - V2EX hot posts free no config

**Need config (free if you have Chrome session):**
- `twitter_read(tweet_url)` - Single tweet via Jina free no config, search/timeline needs Cookie-Editor free local
- `bilibili_search(query)` - Bilibili search via bili-cli free no login
- `reddit_read(subreddit, post_id)` - Reddit via old.reddit.com .json + Jina fallback free, search needs OpenCLI Chrome session free
- `facebook_search(query)` - Facebook via OpenCLI Chrome session free
- `instagram_user_search(username)` - Instagram via OpenCLI free
- `xiaohongshu_search(query)` - XiaoHongShu via OpenCLI only uses existing Chrome session, cookie only locally
- `linkedin_read(url)` - LinkedIn Jina public page free, details needs OpenCLI
- `xiaoyuzhou_transcribe(podcast_url)` - Podcast Whisper with Groq->OpenAI fallback free

**Doctor:**
- `doctor_check_all()` - Doctor check all channels with real probing, ordered backend candidates, tells apart missing/broken/timeout - like agent-reach doctor --json
- `doctor_text_report()` - Human readable report

All free, zero API fees, privacy: Cookie only locally not uploaded.

## Design Philosophy

Agent Reach is capability layer, not another tool - does selection/install/health-check/routing, not underlying reading. Reading by Agent directly calling upstream tools, no wrapper.

When you give new Agent environment, you spend time finding tools, installing deps, config - Twitter what to read? Reddit how to login? XiaoHongShu CLI stopped what's replacement? Each time re-step. Agent Reach does: current most stable access method, we choose, install, health-check for you - access method will iterate, you don't worry.

Hermus Free already has this philosophy: free stack, no paywall, SQLite FTS5, auto skills. Now with Agent Reach tools, Agent can see entire internet free.

## Quick Start - No Config Needed

Tell Agent:

- "Help me read this webpage https://example.com" → `web_read` via Jina free
- "This GitHub repo what does it do Panniantong/agent-reach" → `github_read` via gh CLI free
- "This YouTube video what does it say" → `youtube_transcript` via yt-dlp free
- "Bilibili search AI tutorial" → `bilibili_search` via bili-cli free no login
- "Full web search LLM framework comparison" → `web_search` DuckDuckGo free + Exa free MCP no key

No need to remember commands - Agent reads this SKILL.md and knows which tool to call.

Need login platforms (XiaoHongShu, Twitter, Reddit, Facebook, Instagram)? Tell Agent "help me config XXX" and it guides step by step free local only.

## Standing Rules (for Agent)

- Probe `doctor --json` active_backend before acting on multi-backend platforms
- Announce which skill/backend is in use
- Follow documented retry chains
- Compose multi-platform research
- For login-backed platforms, check if OpenCLI Chrome session available via `doctor_check_all`
- If platform requires config, tell user how to config via Cookie-Editor manual export free local, not via API fees

## Quick Commands

- `bili search <query>` - Bilibili search (bili-cli, no login)
- `doctor --json` - Check all channels status, backend candidates, active backend
- `doctor` - Human readable report

## Compatible

Compatible with all Agents: Claude Code, OpenClaw, Cursor, Windsurf... any can run shell commands.

## Install (One Sentence - Original Agent Reach)

Original: `Help me install Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md`

Free clone already included - no extra install needed for core, optional:

```bash
pip install feedparser yt-dlp  # for RSS and YouTube full
pip install bili-cli  # for Bilibili no login
```

All zero API fees, fully open source.
