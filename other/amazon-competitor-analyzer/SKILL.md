---
name: amazon-competitor-analyzer
description: 基于输入的亚马逊 ASIN，通过项目内置 BrowserWorker 插件浏览器采集公开商品页数据，执行竞品分析。对比规格、价格、评论质量与视觉策略，识别竞争对手的护城河与薄弱点，辅助市场决策。
title: 亚马逊竞品分析
example: 对比分析亚马逊竞品 B09G9GB4MG、B07ABC11111 和 B08N5WRWNW，找出它们在评分和买家痛点上的差异。
version: 1.0.0
---
# Amazon Competitor Analyzer

This skill collects Amazon product data from user-provided ASINs through the project-local BrowserWorker plugin browser and performs deep competitive analysis.

## When to Use This Skill

- Competitive research: Input multiple ASINs to understand market landscape
- Pricing strategy analysis: Compare price bands across similar products
- Specification benchmarking: Deep dive into technical specs and feature differences
- Review insights: Analyze review quality, quantity, and sentiment patterns
- Market opportunity discovery: Identify gaps and potential threats

## What This Skill Does

1. **ASIN Data Collection**: Extract product title, price, rating, review count, images
2. **Specification Extraction**: Deep extraction of technical specs, features, and materials
3. **Review Quality Analysis**: Analyze review patterns, keywords, and sentiment
4. **Multi-Dimensional Comparison**: Side-by-side comparison of key metrics
5. **Moat Identification**: Identify core competitive advantages and barriers
6. **Vulnerability Discovery**: Find competitor weaknesses and market opportunities

## Features

1. **Stable browser extraction**: Use BrowserWorker `page_semantics` / `semantic_key` first, then snapshot/evaluate loops to verify and read the rendered Amazon page.
2. **No external browser service**: Do not require BrowserAct, Playwright, Selenium, ChromeDriver, or a site-specific remote browser API.
3. **Cross-platform install behavior**: Browser control goes through the bundled daemon and Chrome extension transport on macOS and Windows.
4. **Bounded execution**: Keep ASIN count and detail visits limited; stop on login, captcha, region prompts, or blocks.
5. **Cost efficient**: Reduces manual research time without adding paid automation-service credentials.

## Prerequisites

### BrowserWorker Runtime

- ManAI 主程序或项目内 `BrowserWorker` daemon 可用。
- 端口发现顺序：`BrowserWorker_PORT` -> `BrowserWorker_LOCK_FILE` -> `MANAI_WORKSPACE_ROOT` / `MANAI_HOME` 下的 `storage/browser_daemon.lock` -> 默认 `12321`。
- 不要求用户注册 BrowserAct、配置 `BROWSERACT_API_KEY`，也不要求用户安装 Python 第三方包。
- 浏览器交互必须先读取 `page_semantics` 并按 `semantic_key` 或结构化 target 理解关键区域；缺少语义记录时再用 `snapshot` / `detect_page_state` 验证当前页面，随后通过 `browser.evaluate(...)` 从真实渲染 DOM 中提取标题、价格、评分、评论数、图片、规格和 bullet points。不要在可复用脚本中保存 snapshot `ref` / `handle`。
- 遇到 Amazon 登录、验证码、地区确认、风控或空白页时，必须调用 `browser.request_help(...)` 或停止，严禁绕过验证或高频重试。

## Usage

### Basic Analysis

```bash
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG
```

### Multiple Products

```bash
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG B07ABC11111 B08N5WRWNW
```

### With Output Directory

```bash
python amazon-competitor-analyzer/amazon_competitor_analyzer.py B09G9GB4MG --max-detail-visits 1
```

### Output Formats

- **Markdown**: Comprehensive report
- **JSON**: Raw data with analysis

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| asins | string | - | One or more Amazon ASINs to analyze |
| --amazon-url | string | https://www.amazon.com/ | Amazon marketplace base URL |
| --max-detail-visits | integer | 10 | Maximum product detail pages to open in one run |
| --wait-ms | integer | 2200 | Base wait after page navigation |

## Dependencies

Browser automation must use the bundled BrowserWorker daemon and Python standard library HTTP client. Do not add `requests`, `python-dotenv`, BrowserAct SDKs, Playwright, Selenium, ChromeDriver, pandas, or BeautifulSoup as runtime requirements for this skill.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| BrowserWorker_PORT | No | Optional BrowserWorker daemon HTTP port override |
| BrowserWorker_LOCK_FILE | No | Optional BrowserWorker lock file path |

## Error Handling

- **BrowserWorker down**: Resolve port from lock file; if daemon is not responding, start the project-local BrowserWorker daemon.
- **Login/Captcha/Region Prompt**: Request user help in the plugin browser and continue only after page state is valid.
- **Network Error**: Verify internet connection and retry with a smaller ASIN set.
- **Rate Limit/Block**: Stop the run, reduce scope, and avoid repeated navigation.
- **Invalid ASIN**: Verify ASIN format (10 alphanumeric characters)

---

**Version**: 1.0.0  
**Updated**: 2026-02-09  
**Template ID**: `77814333389670716`
