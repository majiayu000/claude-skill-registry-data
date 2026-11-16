---
name: santifer--career-ops
description: "AI job search system trên Claude Code — A-F scoring 10 dimensions, 15 slash commands, Playwright portal scanning 45+ companies, ATS-optimized PDF resume generation."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Career-Ops: hệ thống tìm việc AI — inverts recruitment dynamics: công ty dùng AI filter ứng viên, ứng viên dùng AI filter công ty.

## Install

```bash
git clone https://github.com/santifer/career-ops
cd career-ops
npm install
playwright install chromium
npm run doctor   # validate prerequisites
```

## Setup

```
1. Tạo cv.md — resume dạng markdown
2. config/profile.yml — career preferences
3. templates/portals.yml — target companies
```

## 15 Slash Commands

```
/career-ops                    — list all commands
/career-ops {paste job URL}    — full auto-pipeline
/career-ops scan               — portal discovery (45+ companies)
/career-ops pdf                — ATS-optimized resume PDF
/career-ops batch              — parallel evaluation
/career-ops tracker            — application status
/career-ops deep               — company research
/career-ops training           — course/cert evaluation
/career-ops contacto           — LinkedIn outreach
```

## Scoring System

```
A-F grade, 10 weighted dimensions:
  - Role match vs CV
  - Compensation research
  - Level strategy
  - Culture fit indicators
  - Growth potential
  ...

< 4.0/5.0 → system strongly recommends NOT applying
```

## Architecture

```
Agent Instructions (AGENTS.md)
    ↓
Mode Selection (modes/*.md)
    ↓
Evaluation Logic (scoring weights)
    ↓
Output: reports, PDFs, TSV pipeline
```

## Stack

- Claude Code (primary) — đọc AGENTS.md + CLAUDE.md
- Node.js + Playwright — portal scanning + PDF gen
- Go + Bubble Tea — TUI dashboard
- Markdown/YAML — config

## Alternative Providers

- Gemini CLI (free tier: 15 req/min, 1M daily tokens)
- OpenCode CLI
- Codex (coming soon)

## Source

https://github.com/santifer/career-ops · MIT · +193⭐ today
