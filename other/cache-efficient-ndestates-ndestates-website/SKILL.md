---
name: cache-efficient
description: >
  ndestates-io cache-first session with minimal tokens: load INDEX + targeted cache/memories
  only, respond in short bullets. Use at every session start, when cost matters, or
  .github/skills/cache-efficient/SKILL.md. Default tone for this repo unless user asks for depth.
user-invocable: true
disable-model-invocation: false
---

# Cache-Efficient Mode

**Non-negotiable for this repo**: maximize cached knowledge; minimize tokens.

## Load (do not skip)

Read manifest `token_policy` first. **Spine** (free): README index, `.codebase-scan.txt`, latest TODO, `INDEX.md`.

**Capped loads** (`max_cache_files_default`, default **2**):
1. ≤2 files from `docs/codebase/*` — **grep headings first**, then section `Read` only.
2. ≤1 INDEX-selected memory (counts toward cap if 2 codebase docs already loaded).

Optional: `IMPLEMENTATION_SUMMARY.md` / `BRANCH_ANALYSIS.md` — **one section** only if task requires; prefer grep.

**Hard rules**:
- **Grep before Read** on registry, skills, or any file >80 lines.
- **No application source** until user confirms direction (`no_source_until_confirmed`) or names one exact path.
- At **≥100k** session context (`session_refresh_context_tokens`), recommend `.github/skills/chain/SKILL.md session-start` in a fresh thread.

## Respond

- Default cap: **≤120 words** unless user asks for detail, code, or a plan.
- Format: bullets; one line per finding; cite `path` or `path:line` — **no** large code fences.
- Reference cache by name (“per CONCERNS §…”, “per ndestates-io-cache”) — do not quote paragraphs.
- End with **Next** (1–3 numbered actions) when helpful.
- Orchestrator JSON / handoff schemas: still valid when that skill requires them — keep JSON compact.

## After load, confirm in one line

Example: `Cache: INDEX + codebase-cache + esign memory + CONCERNS(§signing). Fresh. Ready.`

## Token meter (always-on)

When `token_policy.report_tokens_estimate: true` (manifest default), end **every substantive response** with the one-line footer from `/token-usage-meter`:

1. Run `python3 .github/skills/token-usage-meter/scripts/token_monitor.py --sync --project .` once per turn.
2. Append the printed line: `Token meter: ctx … · +… this turn · … turns · STATUS`.
3. Surface any WARNINGS above the footer.

Skip only for trivial acks or when user opts out (`no token meter`).

## Chaining

- **Auto-compose:** `.github/skills/chain/SKILL.md <intent>` — discovers skills from `chains/registry.yaml`, one shared cache load, minimal handoffs (see `CHAIN.md`).
- Standup: `.github/skills/chain/SKILL.md session-start` or `.github/prompts/daily-standup-with-cache.prompt.md` then stay in cache-efficient tone.
- Deep work: user says “go deep” or `.github/skills/chain/SKILL.md complex-task` / ``.github/prompts/orchestrator-v2.prompt.md`` — expand stepwise, still cache-first per step.
- For full .github/prompts/read-codebase.prompt.md or major changes: start with cache-efficient load, then expand only as needed.