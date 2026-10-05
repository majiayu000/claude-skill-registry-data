---
name: career-job-hunting
category: career
description: 'Complete job hunting workflow using Hermes Agent — resume setup via visiky-resume-setup, multi-platform job search via mcp-jobs, application tracking in Notion.'
tags:
  - career
  - job-hunting
  - mcp
  - resume
  - internship
trigger: |
  Use this skill when the user wants to:
  - Find job/internship opportunities on Chinese platforms (BOSS直聘, 猎聘, 智联, 51job)
  - Set up or update their online resume
  - Track job applications and interview progress
  - Get recommendations on job hunting tools and workflow
  - Evaluate which tools (mcp-jobs, get_jobs, JobClaw) fit their current stage
---

# Career Job Hunting with Hermes Agent

## Overview

This skill covers the end-to-end workflow for using Hermes Agent to find, track, and apply for jobs/internships — optimized for the Chinese job market (AI/tech roles). The user (冯周杰 / Publieople) is a 大二 AI 专业学生 at 上海中侨职业技术大学, targeting AI toolchain development / Agent application / MLOps roles.

## Components

### 1. Resume Setup (`visiky-resume-setup`)

The user's resume data lives in `publieople/publieople/resume.json` on GitHub. The online editor preview is at `https://visiky.github.io/resume?user=publieople&branch=master`.

See the `visiky-resume-setup` skill for full schema, deployment, and debugging.

Key fields to update (last updated 2026-06-04):
- `profile.positionTitle` — "AI 工具链开发与智能体应用 · 自动化效率工程师"
- `educationList` — 上海中侨职业技术大学, 人工智能（主修：机器学习、深度学习、计算机视觉、自然语言处理、数据结构与算法）, 2024-至今
- `workExpList` — 4 bullet points with quantification (GPU集群管理 + AI服务栈 + 培训 + 知识传承)
- `projectList` — 4 projects (AI Agent生态/产研社/技术博客/AI学习小组)，均补充量化数据
- `awardList` — 4 awards, ordered by actual prestige: 数维杯>中青杯>五一建模>工行杯
- `aboutme` — 精简为3行，无MBTI，突出AI Agent闭环经验

### 2. Job Search (`mcp-jobs` MCP Integration)

**Tool:** `mergedao/mcp-jobs` v1.4.0 — aggregates jobs from 猎聘, BOSS直聘, 智联, 51job via Playwright crawling.

Registration in `~/.hermes/config.yaml`:
```yaml
mcp_servers:
  jobs:
    command: "node"
    args: ["/home/po/.npm-global/lib/node_modules/mcp-jobs/dist/mcp.js"]
```

**Available MCP tools (after Hermes restart):**
- `mcp_jobs_mcp_search_job` — keyword-based job search across platforms
- `mcp_jobs_mcp_job_detail` — fetch details from a specific job URL

**Usage patterns (directly in conversation):**
- "搜上海AI实习岗" → search_job(keyword="AI", city="上海")
- "搜北京Python后端薪资15k以上" → search_job with filters
- "看看这个职位的详情" → job_detail with URL from search results

See `references/mcp-jobs-deployment.md` for install and troubleshooting details.

### 3. Tool Deployment — Detailed Installation & Integration

For each tool's detailed reference see `references/tool-details.md`.

#### 3a. mcp-jobs — Zero-Config Job Aggregator

**Type**: Aggregator (search only) — crawl BOSS, 猎聘, 智联, 51job
**Tech**: Node.js + Playwright + MCP | **Risk**: Low

**Prerequisites**: Node.js v18+, npm, Playwright Chromium (`npx playwright install chromium`)
**Standalone**: `npx -y mcp-jobs`
**Hermes Integration** (see `references/mcp-jobs-deployment.md`):
```yaml
mcp_servers:
  jobs:
    command: "npx"
    args: ["-y", "mcp-jobs"]
    timeout: 180
    connect_timeout: 60
```

**Available tools** (after Hermes restart): `mcp_jobs_mcp_search_job`, `mcp_jobs_mcp_job_detail`

**Known pitfalls**:
- `npx -y mcp-jobs` has no `bin` field — must use the working config above; the `node`/direct `dist/mcp.js` path is a fallback
- v1.4.0 is ~10 months old — platform DOM may have changed
- Proxy: MCP subprocess inherits filtered env from Hermes config, not shell env. If behind `http://127.0.0.1:7890`, add `env:` block to the server config
- First run downloads Playwright browser — may take 30-60s

#### 3b. JobClaw — LLM-Powered Smart Apply

**Type**: Auto-applier (precision, LLM-matched) — BOSS + LinkedIn
**Tech**: Python + Playwright + LLM scoring | **Risk**: Medium

**Prerequisites**: Python 3.11+, Playwright (`playwright install`)
```bash
git clone https://github.com/slothsheepking/jobclaw.git
cd jobclaw
pip install -e .
playwright install
jobclaw login
# Edit profiles/me.yaml with skills, salary, city
jobclaw run
```

**LLM auth** (priority order): Claude OAuth (free) > Anthropic API key > OpenAI API key
**Notification**: Telegram bot / Discord webhook
**Anti-detection**: Randomized apply delays, HR inactivity filter (7d default)
**Proxy**: `HTTP_PROXY` / `HTTPS_PROXY` env vars

**Known pitfalls**:
- Cookie management: cookies in `~/.jobclaw/cookies/` expire; run `jobclaw login --check` to verify
- LinkedIn requires separate cookie login
- LLM auth priority means no API key needed if Claude Code is set up — uses subscription token

#### 3c. get_jobs — Mass Batch Apply

**Type**: Auto-applier (volume) — BOSS (150/day), 猎聘, 前程无忧, 智联
**Tech**: Java + Gradle + ChromeDriver | **Risk**: Medium-High (account restrictions)

**Prerequisites**: JDK 21, Maven/Gradle, ChromeDriver matching Chrome version
```bash
git clone https://github.com/loks666/get_jobs.git
cd get_jobs
./gradlew build
```

**Platform limits**:
- BOSS: 150 hellos/day hard cap; auto-blacklists "not suitable" companies
- 猎聘: unlimited hellos, must bind WeChat
- 前程无忧: degraded, limited applies
- 智联招聘: ~100 applies, broken, not recommended

**Known pitfalls**:
- **Windows-oriented**: hardcoded `chromedriver.exe` paths; ChromeDriver must match Chrome version exactly
- **WSL complication**: Chrome must run headless; ChromeDriver path must be Linux-adjusted
- **Account risk**: BOSS auto-apply patterns can trigger account restrictions — use a secondary account
- **.env config**: Requires API key for LLM greeting generation (`OPENAI_API_KEY` or proxy)
- **Cost**: ~$0.06/day with gpt-5-nano

#### 3d. GeekGeekRun (牛人快跑) — Desktop GUI

**Type**: Auto-applier (desktop UI) — BOSS only
**Tech**: Puppeteer + Electron | **Risk**: Low

**Packages**: Windows (.exe), Linux (.deb), macOS (.dmg)
**Features**: Auto-chat, read-without-reply retry, zombie job cleanup, LLM template editor, config templates
**Repo**: `github.com/geekgeekrun/geekgeekrun` (857 commits, 27 releases)

### 4. Deployment Decision Tree

```
Want to just browse the market?
  └─ mcp-jobs (integrate into Hermes, search by conversation)

Want precision-targeted apply (high match rate)?
  └─ JobClaw (Python, LLM scoring, anti-detection)

Want mass batch apply (volume over precision)?
  └─ get_jobs (Java, multi-platform, cap-aware)

Want a simple GUI without command line?
  └─ GeekGeekRun (Desktop app, BOSS only)
```

### 5. Environment Notes (This User — Verified May 2026)

- **Shell**: Arch Linux via WSL2
- **Node.js**: v26.1.0 ✅ | **npm**: 11.14.1 ✅
- **Playwright**: 1.59.0 (chromium-1217, chromium_headless_shell-1217) ✅
- **Python**: 3.11.14 ✅
- **Java**: NOT installed ❌ (needed for get_jobs)
- **Proxy**: `http://127.0.0.1:7890` (for HTTP/HTTPS traffic)
- **HF Mirror**: `HF_ENDPOINT=https://hf-mirror.com`
- **Resume repo**: `publieople/publieople` with `resume.json` (visiky/resume format)

### 6. Application Tracking (Notion)

Set up a Notion database with columns:
- Company, Position, Platform, URL
- Status (已投递 / 已读 / 约面 / 一面 / 二面 / Offer / 感谢信)
- Date applied, Last follow-up, Notes
- Resume version used

Use Hermes' `notion` skill to interact with this database.

## Quick Start for New Sessions

1. **Resume**: Ensure `publieople/publieople/resume.json` is up to date → push to GitHub
2. **Search**: Use mcp-jobs tools (requires Hermes restart after config change) — "帮我搜上海AI实习岗"
3. **Track**: Log interesting matches in Notion
4. **Apply**: For high-match roles, draft custom greeting and submit manually or via JobClaw

## Job Hunting Timeline (2026)

| Period | Focus | Tool |
|--------|-------|------|
| **大二暑假 (now, 2026.06-08)** | Resume polish, portfolio building, market research. Target 上海日常实习 for 大三上 (Sep start). | web_search (实习僧/Boss直聘/官网) |
| **大三上 (2026.09-12)** | Start regular internship in Shanghai (3-4 days/week, 3-6 months preferred). Daily internships hire year-round, less competition than summer. | mcp-jobs + manual apply |
| **大三寒假** | Continue or upgrade internship | — |
| **大三暑假** | Summer internship push for return offer / full-time pipeline | get_jobs for volume |

Key strategy: **福州暑假无大厂AI机会 → 7-8月打磨简历 + 线上调研 → 9月上海日常实习入职。** 日常实习全年可投、竞争小于暑期实习、可拉长3-6个月含金量更高。

## Pitfalls

- **mcp-jobs may return empty**: v1.4.0 is ~10 months old and platform DOM changes can break it. **Fallback: use `web_search` with site-specific queries** (`site:shixiseng.com`, `site:zhipin.com`, 搜索 "上海 AI Agent 实习 2026"). web_search returns richer, more current results than mcp-jobs in many cases.
- **mcp-jobs has no `bin` field**: `npx -y mcp-jobs` fails. Must install globally and use `node` with direct `dist/mcp.js` path. See `references/mcp-jobs-deployment.md`.
- **Proxy**: Behind `http://127.0.0.1:7890`, Node.js MCP subprocess inherits filtered env from Hermes. If mcp-jobs can't reach target sites, try passing proxy env explicitly:
  ```yaml
  env:
    http_proxy: "http://127.0.0.1:7890"
    https_proxy: "http://127.0.0.1:7890"
  ```
- **Playwright browsers**: mcp-jobs requires Chromium. Install with `npx playwright install chromium` if not present.
- **get_jobs is Windows-oriented**: uses chromedriver.exe and IntelliJ IDEA. Hard to run in WSL without modifications. Requires JDK 21 which is NOT installed.
- **BOSS account risk**: Auto-apply patterns (get_jobs, JobClaw) can trigger account restrictions. Use a secondary account for volume apply.
- **JobClaw cookie management**: Cookies in `~/.jobclaw/cookies/` expire; run `jobclaw login --check` to verify before batch runs.
- **Session recall tool is unreliable**: do not use session_search to find past internship discussions. Memory and skills carry the durable state.

## Phase 0: Reconcile User Intent (Before Any Planning)

**Always do this before writing a plan, picking companies, or editing the resume.** A user saying "let's discuss my internship plan" is NOT permission to start drafting — it's permission to *discover what the plan should be*.

Pull signals from every available source and check them against each other:

| Source | What to extract | How |
|---|---|---|
| `publieople/publieople/resume.json` | Stated `positionTitle`, project list, skill tags | `gh api` or `curl raw.githubusercontent.com` |
| GitHub repos + stars | Actual shipped projects, language depth, what they spend time on | `gh api /users/{name}/repos` |
| Blog (`blog.for-people.cn`) | Topics they actually write about vs what they claim to be good at | `curl /feed` (NotionNext ships /feed) |
| **Notion `求职意向` data_source** | The single highest-signal artifact — user's *actual* ranked company list with reasons | `/data_sources/{id}/query` |
| Notion `大学`, `阅历`, `编程`, `AI`, `大二上 课程` | Course context, hobby/identity tags | search → list data_sources |
| mem0_search + session_search | Past stated preferences and decisions | before drafting anything |

**Notion API 2025-09 pitfalls when doing this:**
- `POST /v1/search` `filter.value` MUST be `"data_source"`, not `"database"` (returns 400 otherwise — older tutorials are wrong)
- Sort + no query = 400. Omit sort if you have no query.
- 404 on `/data_sources/{id}/query` does NOT mean "doesn't exist" — it means "integration not shared with this database". Try a different data_source.

**Then surface the contradictions directly.** In this user's case, the Notion 求职意向 table contained 28 WLB-first foreign-tech companies (VMware/AWS/NVIDIA/Microsoft/Apple/...) while resume.json said "AI 工具链开发与智能体应用 · 自动化效率工程师". Both are real, but they don't match — and HR will read whichever is on the resume. Don't paper over this with a "best of both worlds" recommendation; ask the user to pick.

Use the **Reconnaissance Report** format when reporting back (see `references/reconnaissance-report-template.md`):
1. **已确认画像** (identity, skills, projects, honors) — concrete facts only
2. **求职意向表的真正信号** — what the company list + reasons reveal
3. **4 个尖锐问题** — explicit mismatches between stated position and inferred direction
4. **5 个事实问题 (A-E)** — what the user must answer before planning resumes

Only after the user answers the A-E questions does planning begin. Never write a resume, company list, or timeline until intent is aligned.

## Resume Optimization Rules (from 2026-06-04 session)

When helping the user optimize their resume:

1. **Never guess competition prestige** — verify via web_search before ranking. 校级 awards go last.
2. **Don't add projects the user hasn't vouched for** — ask first. The user knows which projects are solid vs. "不能细看".
3. **University courses may not matter** — the user considers self-taught skills more important than formal coursework. Ask before adding.
4. **Quantify everything possible** — 子弹点 = 动词 + 事项 + 数据. "100+ Skills模块" beats "沉淀百余个".
5. **Personal evaluation stays short** — 3 lines max, no MBTI, no filler.
6. **Section title "更多信息" should be renamed** to something concrete like "竞赛获奖" if that's what it contains.

## Related Skills

- `visiky-resume-setup` — online resume JSON schema, deployment, and debugging
- `native-mcp` — general MCP server configuration for Hermes (includes the no-bin-field fix for mcp-jobs)
- `notion` — application tracking database management

## References

- `references/mcp-jobs-deployment.md` — mcp-jobs install, troubleshooting, and MCP integration details
- `references/tool-details.md` — detailed tool comparisons: mcp-jobs v1.4.0 deps, get_jobs platform limits, JobClaw LLM auth, GeekGeekRun features, environment verification
- `references/job-tools-landscape.md` — broader auto-apply tool landscape (NEAR agent market, OpenOutreach, MoneyPrinterTurbo, etc.)
- `references/reconnaissance-report-template.md` — Phase 0 user-intent alignment: 4-source cross-check, 4-section report format, A-E gate questions
