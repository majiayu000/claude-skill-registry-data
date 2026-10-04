---
name: nowcoder-public-intel
description: Collect, normalize, and synthesize public Nowcoder / 牛客 search, discuss, interview-experience, job, and offer-signal posts for career, recruiting, salary, JD, and interview research. Use when Codex needs low-volume public Nowcoder evidence for AI/LLM/PhD job-family mapping, offer-signal scouting, interview posts, company discussions, or community career intelligence without cookies, login scraping, private comments, or personal-profile harvesting.
---

# Nowcoder Public Intel

Use this skill for low-volume public 牛客 / Nowcoder intelligence. Treat outputs as community signals, not authoritative facts.

## Safety Defaults

- Use only public pages or unauthenticated public endpoints.
- Do not request, read, store, or paste cookies, tokens, headers, local browser profiles, usernames, contact data, private screenshots, or private comments.
- Do not bypass login, CAPTCHA, paywalls, anti-bot controls, hidden-content permissions, or rate limits.
- Keep results small. Prefer `--max-pages 1` or `2`; avoid broad historical crawling.
- Save only normalized metadata, links, short snippets, and your own synthesis.
- Mark offer/salary claims as low confidence unless cross-validated by official JD, multiple samples, or another channel.

## Quick Commands

From a repo that has the skill installed globally:

```powershell
$skill = "C:\Users\Administrator\.codex\skills\nowcoder-public-intel"
python "$skill\scripts\nowcoder_public_intel.py" schema
```

Search public Nowcoder:

```powershell
$skill = "C:\Users\Administrator\.codex\skills\nowcoder-public-intel"
python "$skill\scripts\nowcoder_public_intel.py" search `
  --query "腾讯 大模型 博士 offer 深圳" `
  --tag 面经 `
  --order create `
  --max-pages 1 `
  --max-results 10 `
  --output nowcoder-results.jsonl
```

Batch search:

```powershell
$skill = "C:\Users\Administrator\.codex\skills\nowcoder-public-intel"
python "$skill\scripts\nowcoder_public_intel.py" batch-search `
  --query "华为 大模型 博士 offer" `
  --query "腾讯 青云 博士 offer" `
  --query "大模型 算法 博士 深圳" `
  --max-pages 1 `
  --max-results 10 `
  --output nowcoder-batch.jsonl
```

When network fetches fail or access is blocked, use planning mode:

```powershell
python "$skill\scripts\nowcoder_public_intel.py" plan `
  --query "字节 大模型 博士 offer" `
  --tag 面经
```

## Workflow

1. Scope the question.
   - Identify companies, cities, job families, degree level, and timeframe.
   - Prefer concrete query bundles such as `腾讯 大模型 博士 offer 深圳`, `华为 OD 博士 offer`, `大模型 推理 infra 面经`.
2. Run a small public search.
- Use `search` for one query or `batch-search` for a bounded set.
- Use tags only when helpful: `面经`, `求职进度`, `内推`, `公司评价`.
- Use `--order create` for recency-sensitive scans.
- Use `--max-results` to cap per-query output before writing project artifacts.
3. Normalize evidence.
   - Keep `url`, `title`, `snippet`, `created_at`, counts, platform, query, tag, confidence, and matched signal keywords.
   - Do not copy full post bodies unless the user explicitly asks for a short, compliant excerpt from public content.
4. Synthesize conservatively.
   - Separate JD/interview signals from salary/offer signals.
   - Label rumors, single posts, and ambiguous degree/level data as low confidence.
   - Cross-check with official career pages, company programs, or other independent samples before using in a career-value conclusion.
5. Record source ledgers.
   - For project work, save JSONL/CSV/Markdown in the relevant project folder.
   - Include access date and uncertainty notes.

## Script Behavior

The bundled script first tries Nowcoder's public search endpoint. If that fails, it emits structured fallback URLs for manual/browser or AnySearch follow-up rather than switching to private/authenticated routes.

Read `references/source-routing.md` when choosing between public endpoint, page search, RSSHub-style routes, AnySearch fallback, and manual review.

Read `references/output-schema.md` before integrating results into a career-value matrix or source ledger.

## Non-Goals

- No 脉脉, Offershow, BOSS, Liepin, Xiaohongshu, or Zhihu crawling.
- No login-required comments, private feeds, user-profile harvesting, contact extraction, automated messaging, or resume/job-application automation.
- No claims that Nowcoder posts prove salary levels by themselves.
