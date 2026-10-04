---
name: reddit-creator-deploy
description: Turn a KOL roster + subreddit brand-fit analysis into a deployable creator network. Splits creators into KOL (authority) and KOC (grassroots) layers, matches each to a main + secondary subreddits by real gear/shooting-type ∩ community fit, and emits an account×subreddit deployment_matrix (with a ≤3-per-sub ceiling + no-cross-interaction rule) plus per-creator persona_cards. Route A disclosed-compliance baked into every card (FTC disclosure required on any material connection). Consumes reddit-kol-finder's kol_roster.json natively. READ-ONLY, deterministic, no LLM key needed.
---

# reddit-creator-deploy

## 用途 / Purpose
The packaging step between "who could post" (reddit-kol-finder) and "who posts what, where" (reddit-content-brief). Takes real creators + real subreddit brand-fit and produces the **deployment plan**: KOL/KOC two-layer split, an account×subreddit matrix, and per-creator persona cards — all under Route A disclosed-creator compliance (no sockpuppets, disclosure mandatory, ≤3 of our creators per sub, no cross-creator interaction). Generalised from the AcmeGear campaign (`创作者花名册` + `部署矩阵`).

## 输入 / Inputs
| arg | required? | type | where it comes from | error if missing |
|---|---|---|---|---|
| `--roster` | yes | file | `kol_roster.json` from reddit-kol-finder (uses `reddit_native[]`), or a plain `[{handle,subreddits,tier,gear,shooting_types,geo,profession}]` list | `ERROR: --roster file not found` (exit 2); 0 creators → exit 3 |
| `--subs` | yes | file | subreddit brand-fit map `{"<sub>":{"fit_score":N,"tolerance":".."}}` or sweep jsonl (`{"sub":..,"verdict":{"fit_score":..}}`) | `ERROR: --subs file not found` (exit 2) |
| `--brand` | yes | string | brand name (used in disclosure lines) | `ERROR: the following arguments are required: --brand` |
| `--products` | no | comma list | product lines (for context) | — |
| `--out-dir` | no | dir | output dir (default `out`) | — |

## 输出 / Outputs
- **`deployment_matrix.json`** — `{brand, n_creators, n_kol, n_koc, max_per_sub, saturated_subs, rows[]}`; each row `{handle, layer(KOL/KOC), geo, main_sub, secondary_subs[], cadence, disclosure}`.
- **`deployment_matrix.md`** — the human table + 合规底线 block; flags any subreddit over the ≤3-creator ceiling.
- **`persona_cards.md`** — one card per creator (真实身份 / 主副场 / 社区匹配逻辑 / 披露式品牌关系 / 节奏), labelled 招募画像 (real people fill in later).

## 逻辑 / How it decides
- **Layer**: roster `tier` A → KOL; B/C → KOC; else infer from `signals.upvotes_total` (≥200 → KOL).
- **Main/secondary subs**: rank the creator's own subreddits by real `fit_score` from `--subs`; top = main, next 1-2 = secondary. A creator only ever lands in communities they actually belong to.
- **Cadence**: KOL = 1 post/2-3wk + weekly comments; KOC = comment-led + 1 post/3wk.
- **Compliance (baked, not optional)**: every card carries the FTC disclosure requirement; matrix enforces ≤3 of our creators per sub (flags saturation), no cross-creator interaction, no same-content multi-sub. Route A only — no fabricated personas.

## Usage
```
$ python3 scripts/generate.py --roster kol_roster.json --subs subs_fit.json \
    --brand "AcmeGear" --products "兔笼,快装板,监视器支架" --out-dir out
{"n_creators": 5, "n_kol": 2, "n_koc": 3, "saturated_subs": {}, "out_dir": "out"}
```
Test: `python3 scripts/test.py` (real fixture in `fixtures/`, asserts layer split + fit-ranked mains + disclosure on every row).

## Pipeline position
Runs after `reddit-kol-finder` (consumes its `kol_roster.json`) and before `reddit-content-brief` (which writes what each deployed creator posts). Front-end recon comes from `subreddit-deep-research` (community universe + high-upvote logic + rules) → its `--subs` fit output feeds this skill.
