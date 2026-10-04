---
name: opencli
description: Use OpenCLI to gather information from websites without login. Trigger when the user wants to fetch data from websites (news, finance, research papers, tech trends, Stack Overflow, Wikipedia, etc.) via CLI, needs structured web data in JSON/CSV/Markdown, mentions opencli, or wants to discover public APIs on any website. Also use when the user asks to scrape, monitor, or pull live data from public web sources without authentication.
license: Apache-2.0
---

# OpenCLI: Gather Web Information Without Login

OpenCLI turns websites into CLI commands. Many adapters work against **public APIs** — no browser, no login, no credentials needed. This skill covers the no-login subset: 25+ built-in public adapters plus AI-powered discovery for any website.

> **Verified against `opencli list`** — only adapters tagged `[public]` are listed below. Adapters tagged `[cookie]`, `[intercept]`, or `[ui]` require browser login and are excluded.

## Before You Start

Check that opencli is installed:

```bash
opencli --version
```

If not installed:

```bash
npm install -g @jackwener/opencli
```

Requires **Node.js 20+**. No Chrome or browser extension needed for public commands.

## Quick Reference: Public Adapters

These adapters work immediately — no login, no browser. Verified via `opencli list` output:

| Adapter | Best Commands | Use Case |
|---------|--------------|----------|
| `hackernews` | `top`, `new`, `best`, `search`, `ask`, `show`, `jobs`, `user` | Tech news & discussions |
| `stackoverflow` | `hot`, `search`, `bounties`, `unanswered` | Programming Q&A |
| `arxiv` | `search`, `paper` | Academic papers (note: API can rate-limit, see Known Issues) |
| `wikipedia` | `search`, `summary`, `random`, `trending` | General knowledge |
| `devto` | `top`, `tag`, `user` | Developer blog posts |
| `bbc` | `news` | World news headlines (RSS) |
| `lobsters` | `hot`, `newest`, `active`, `tag` | Tech link aggregator |
| `dictionary` | `search`, `synonyms`, `examples` | Word definitions |
| `steam` | `top-sellers` | Top selling games |
| `huggingface` | `top` | Trending AI papers |
| `apple-podcasts` | `search`, `episodes`, `top` | Podcast discovery |
| `xiaoyuzhou` | `podcast`, `podcast-episodes`, `episode` | Chinese podcasts |
| `paperreview` | `submit`, `review`, `feedback` | Paper peer review |
| `bluesky` | `trending`, `user`, `search`, `thread`, `profile`, `followers`, `following` | Bluesky social |
| `google` | `news`, `search`, `suggest`, `trends` | Google search & trends |
| `imdb` | `search`, `title`, `top`, `trending`, `person`, `reviews` | Movies & TV |
| `sina-finance` | `news`, `stock` | Chinese finance news & stock quotes |
| `product-hunt` | `posts`, `today` | Product launches |
| `v2ex` | `hot`, `latest`, `node`, `topic`, `member`, `replies`, `user` | Chinese tech forum |
| `weread` | `ranking`, `search` | Book rankings (WeRead) |
| `substack` | `search` | Newsletter search |
| `tieba` | `hot` | Baidu Tieba hot topics |
| `ctrip` | `search` | Travel destination search |

**Bloomberg** (all public via RSS):
`main`, `markets`, `economics`, `tech`, `politics`, `opinions`, `industries`, `businessweek`, `feeds`

> **NOT public (require browser login):** `barchart` (all `[cookie]`), `bilibili`, `douban`, `zhihu`, `weibo`, `xiaohongshu`, `twitter/x`. There is NO `yahoo-finance` adapter — use `sina-finance stock` for stock quotes instead.

For the full adapter reference with all flags and examples, read `references/public-adapters.md`.

## Output Formats

Always pick the right format for the context:

```bash
opencli hackernews top --limit 5 -f json    # Structured data for processing
opencli hackernews top --limit 5 -f md      # Readable markdown
opencli hackernews top --limit 5 -f csv     # Spreadsheet-friendly
opencli hackernews top --limit 5 -f yaml    # Human-readable structured
opencli hackernews top --limit 5            # Default: rich terminal table
```

**When gathering data for further analysis or piping**, always use `-f json`. It produces clean, parseable output that you can work with programmatically.

Add `-v` for verbose pipeline debugging if a command behaves unexpectedly.

## Common Patterns

### Pattern 1: Quick Data Fetch

When the user wants specific data from a known source:

```bash
# Tech news
opencli hackernews top --limit 10 -f json

# Stock quote (Chinese & US markets via Sina Finance)
opencli sina-finance stock AAPL -f json

# Research papers
opencli arxiv search "transformer architecture" --limit 5 -f json

# Programming questions
opencli stackoverflow search "rust async" --limit 5 -f json

# Word lookup
opencli dictionary search "ephemeral" -f json

# Bluesky trending
opencli bluesky trending -f json

# Product launches
opencli product-hunt today -f json
```

### Pattern 2: Multi-Source Research

When the user needs a broad picture, combine multiple adapters:

```bash
# Gather from multiple sources, then synthesize
opencli hackernews search "AI safety" --limit 5 -f json
opencli arxiv search "AI safety" --limit 5 -f json
opencli devto tag "ai" --limit 5 -f json
opencli stackoverflow search "AI safety" --limit 5 -f json
```

Run these commands, collect the JSON outputs, and synthesize a summary for the user.

### Pattern 3: Discover Public APIs on Unknown Sites

When the user wants data from a site that doesn't have a built-in adapter, use the AI discovery workflow. Read `references/ai-discovery.md` for the full guide. Quick version:

```bash
# One-shot: explore and generate adapter in one step
opencli generate https://example.com --goal "trending posts"

# Or step by step for more control:
opencli explore https://example.com --site mysite    # Discover APIs
opencli synthesize mysite                             # Generate adapter
opencli mysite <command> --limit 5 -f json           # Use it
```

The `cascade` command auto-probes authentication tiers (PUBLIC first):

```bash
opencli cascade https://api.example.com/data
```

### Pattern 4: Install Community Plugins

If someone has already built an adapter for a site:

```bash
opencli plugin install github:<user>/<repo>
opencli plugin list
```

### Pattern 5: Create a Custom YAML Adapter

For sites with simple public JSON APIs, you can create a YAML adapter with zero code. Read `references/custom-yaml-adapter.md` for the full guide. Basic structure:

```yaml
site: mysite
name: trending
description: Get trending items
domain: api.example.com
strategy: public
browser: false
args:
  - name: limit
    type: int
    default: 10
    help: Number of results
pipeline:
  - fetch:
      url: https://api.example.com/trending?limit=${{ args.limit }}
  - map:
      title: ${{ item.title }}
      url: ${{ item.url }}
      score: ${{ item.score }}
columns: [title, url, score]
```

Save as `~/.opencli/plugins/mysite/trending.yaml` and it's immediately available.

## Known Issues

- **arXiv API rate limiting:** The `arxiv search` command can return HTTP 429 if called too frequently. If this happens, wait a few seconds and retry, or fall back to WebFetch on `https://arxiv.org/search/` as a workaround.
- **No Yahoo Finance adapter:** Despite references in OpenCLI's website docs, there is no `yahoo-finance` adapter. Use `sina-finance stock <TICKER>` for stock quotes instead.
- **`barchart` requires login:** All barchart commands are `[cookie]` strategy — they need Browser Bridge. Do not use for login-free gathering.
- **Region-restricted adapters:** Some Chinese platform adapters (Bilibili, Zhihu, Douban, Xiaohongshu) may not work outside China even with login.

## Troubleshooting

- **"command not found"** — Run `npm install -g @jackwener/opencli`
- **Exit code 69 / "Browser Bridge not connected"** — You're using a `[cookie]` adapter that needs browser login. Check with `opencli list` — only `[public]` adapters work without browser.
- **HTTP 429** — API rate limit. Wait and retry, or use a different adapter/source.
- **Empty results** — Some adapters are region-restricted. Stick to global public adapters.
- **Unexpected errors** — Run `opencli doctor` for diagnostics
- **Node errors** — Ensure Node.js 20+: `node --version`
- **Check adapter strategy** — Run `opencli list` to see `[public]`, `[cookie]`, `[intercept]`, or `[ui]` tags for each command

## Decision Tree

```
User wants web data
├── Known site with public adapter? → Use the adapter directly
├── Known site without adapter?
│   ├── Has community plugin? → opencli plugin install
│   ├── Site has public JSON API? → Create YAML adapter
│   └── Unknown API structure? → opencli generate/explore
└── Multiple sources needed? → Run multiple adapters, synthesize results
```
