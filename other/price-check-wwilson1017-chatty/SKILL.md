---
name: price-check
description: Verify and refresh AI model pricing in Chatty's pricing.py from official provider pricing pages, and regenerate PRICING.md. Run during any PR that touches providers or usage. Skips re-fetching if pricing was already verified earlier in the current chat. Only operates inside the Chatty repo.
---

# price-check

Keeps `backend/core/providers/pricing.py` (`MODEL_PRICING` + `PRICING_SOURCES`) current with published per-token rates and regenerates the reviewable report `backend/core/providers/PRICING.md`. No provider's models API exposes price, so this skill is the maintenance mechanism that keeps the usage/cost dashboard accurate as new models are added dynamically.

## When to run
- During any PR that adds/changes models or touches `core/providers/` or `core/agents/usage/` (required by the project `CLAUDE.md` → Model Pricing).
- On request: "check prices", "refresh model pricing", "is pricing current?".

## Guard 1 — ship only in the Chatty repo
Before writing or committing anything, confirm this is the Chatty repo:
- `git remote -v` contains `wwilson1017/chatty`, **OR**
- `CLAUDE.md` starts with `# Chatty` **AND** `backend/core/providers/pricing.py` exists.

If neither holds, STOP: report that price-check only runs in the Chatty repo, and make no changes.

## Guard 2 — skip if already verified this chat
If model pricing was already fetched/verified earlier in THIS conversation, or `backend/core/providers/PRICING.md` already shows `Last verified: <today>` with no pending diff, do NOT re-fetch. Reuse the in-session results and report "already current". Re-fetching wastes calls and risks rate limits.

## Procedure
1. **Model set.** Union of the keys in `MODEL_PRICING` and each provider's current model list — the fallback `*_MODELS` constants, plus (if credentials are configured) what `GET /api/providers/{provider}/models` returns. This prices newly-surfaced dynamic models, not just legacy ones.
2. **Fetch** current STANDARD-tier rates (USD per 1M input / output tokens) via WebFetch from the official pages:
   - Anthropic — `https://platform.claude.com/docs/en/about-claude/models/overview`
   - OpenAI — `https://developers.openai.com/api/docs/pricing`
   - Google — `https://ai.google.dev/gemini-api/docs/pricing`
   - Together — `https://www.together.ai/pricing`
   Record tier caveats (e.g. Gemini 2.5 Pro is the ≤200K-prompt tier) in a code comment.
3. **Diff** against the current `MODEL_PRICING`; classify each model: added / changed / unchanged / unverifiable.
4. **Never fabricate.** If a model's rate isn't on the official page, leave it OUT of `MODEL_PRICING` and report it as "unknown" — the usage dashboard already flags unpriced paid models (`is_priced` / per-agent `has_unknown_pricing`). Do NOT guess from memory or community posts.
5. **Write** `backend/core/providers/pricing.py`:
   - `MODEL_PRICING[model] = (input, output)`
   - `PRICING_SOURCES[model] = (source_url, "<YYYY-MM-DD>")` — use the current session date.
   Keep proven legacy entries (the dashboard prices historical rows by model id via longest-prefix match).
6. **Regenerate** `backend/core/providers/PRICING.md` from the updated `pricing.py` (do not hand-author divergent numbers): a header line `Last verified: <YYYY-MM-DD> (price-check)` followed by a per-provider table `model | input $/M | output $/M | source | verified`.
7. **Report** a concise diff table to the user. When run during a PR, also place the diff in the PR description.

## Commit
- Commit `pricing.py` and `PRICING.md` together, e.g. `Refresh model pricing (price-check <YYYY-MM-DD>)`.
- No `Co-Authored-By` or "Generated with Claude Code" footers (repo policy).
- Never commit secrets; never run `gcloud secrets`/`--set-secrets` commands.

## Notes
- The session date is authoritative for the `verified` date — read it from the environment context, don't compute it in code.
- This skill is committed into the Chatty repo so it travels with the project; it is the canonical place to evolve the pricing-refresh workflow.
