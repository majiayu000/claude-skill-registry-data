---
name: experiment-analysis
description: >
  Replay-driven post-mortem for finished Orbit Wars experiments. Use for
  /experiment-analysis or requests to analyze or explain replay results,
  compare wins and losses, identify failure turns, summarize inconclusive
  iterations, or update adoption notes in hypotheses.md. Does not train, run
  pipelines, edit code, or decide next-iteration strategy.

---

# Experiment Analysis Skill (Orbit Wars)

Replay-driven post-mortem. Honors the `hypotheses.md` skip list, selects the analysis target by priority, converts replays to Markdown via a Python script, has Codex analyze, summarizes + suggests NEXT ACTION, and finally writes back the **verdict** for the analyzed iter to `hypotheses.md`. Raw replay JSON never enters Codex's context (the script does the Markdown conversion).

**Out of scope**: deciding what the next iteration should be (deepen / broaden / list-consume). That decision lives in `experiment-plan` Step 0.5, which reads this skill's verdict + the recent Iteration log to choose. The NEXT ACTION report from this skill is informational guidance, not a state mutation.

## Skill flow

6 phases. Phase 1.5 (target prioritization) and Phase 4.5 (`hypotheses.md` write-back) are new. A skip-mode bypass for replay analysis is included.

### Phase 1 — Identify the target case and `hypotheses.md`

`a concise user question`, 1 question to confirm the target case (`imitation/case1` / `rulebase/case4` / `Other` free-text). Skip when obvious from recent conversation.

After confirmation:

- Search and read `docs/experiment/<family>/{yyyymmdd}_case{N}_{topic}/hypotheses.md`.
- Cache the skip list / primary metric / Iteration log in memory.
- If `replay 分析を行わない` is in the skip list, run Phase 2 in **skip mode** (no replay-Markdown conversion; analysis uses `iter*_result.md` and training logs only).

If `hypotheses.md` does not exist (legacy directories), fall back to the original mode (no skip-list awareness).

### Phase 1.5 — Prioritize the analysis target (new)

`a concise user question`, 1 question:

| Q | options |
|---|---|
| 分析対象の選び方 | `直前 iter のみ` ⭐推薦 / `直近 3 iter 全部 (横断比較)` / `直近 5 iter 全部` / `採否 inconclusive の iter のみ` / `特定 iter を指定` (Other で iter 番号) / `Other` |

Read the `iterN_result.md` (or `result.md`) of the selected iter group. They serve as **input to replay selection** (which iter's matches we pick).

When multiple iters are involved, do not run Phases 2–3 once per iter. Instead, pick two representative replays (e.g. one win + one loss from the most recent inconclusive iter) and do a single Markdown conversion. Markdown conversion is the dominant context cost, so **never exceed n = 2**.

### Phase 2 — Pick two replays (skippable)

If `replay 分析を行わない` is set, **skip Phase 2** and go to Phase 3 (analyze `iter*_result.md` / training logs only).

Otherwise:

`a concise user question`, 1 question (population = the iter group from Phase 1.5):

| Q | options |
|---|---|
| 選定戦略 | `長戦 (拮抗・終局直前) + 最速敗北 (構造的弱点) (推薦・両極から学べる)` / `win 1 + loss 1` / `loss × 2` / `win × 2` / `seed 直接指定` / `Other` |

Why "long match + fastest loss" is the default:
- **Long match** = `total_turns` ≥ p75 of the population. Useful for studying mid-game tactics and end-game closure.
- **Fastest loss** = `total_turns` ≤ p25 of the population AND self_reward = -1. Reveals structural early-game weaknesses (failed initial neutral capture, early home loss, opening ship-spread mistakes).
- Picking two extreme turn-lengths often gives a stronger diagnostic signal than `win + loss`.

Selection implementation:
- Read `data/lake/selfplay/matches/index.parquet` with polars; filter by winner / agents / total_turns.
- "Long" = latest match where `total_turns >= quantile(0.75)`.
- "Fastest loss" = latest match where `total_turns <= quantile(0.25) AND self_reward == -1`.
- If `index.parquet` is missing or has no `total_turns` column, run `pick_match_pair.py` (see scripts section) to compute it from raw replays.
- Worktree `data/` is a symlink; the actual replays live under `/Users/user/project/orbit-wars/data/...`. **Pass absolute paths to the script.**

### Phase 3 — Markdown conversion via Python script

Run `replay_to_markdown.py` against the two selected replays to produce `result_1.md` / `result_2.md`. stdout is exactly two lines (`wrote ... (N lines)`). **Do not paste raw JSON or per-turn tables into Codex's chat.**

Output directory:

```
data/output/experiment/{family}/case{N}/replay_analysis/{yyyymmdd_HHMM}/result_{1,2}.md
```

(Under `data/output/`, not `docs/experiment/`. Reference paths from `hypotheses.md` / `iterN_analysis.md`.)

### Phase 4 — Read the Markdown and analyze

Codex `Read`s `result_1.md` / `result_2.md` (in skip mode, only `iter*_result.md`) and must cover three views:

1. **why_lost** — pinpoint decisive turns / events from Turning points / Key events of the loss match. Up to 3 candidate hypotheses, each backed by supporting/refuting turn-level facts.
2. **what_worked** — behaviors that functioned in the win match (or in the early phase of the loss match). Patterns worth reproducing.
3. **where_to_focus_next** — turn ranges and metrics to drill into next. e.g. "turn 50–80 around the comet appearance" or "turn 150 in-flight ratio during the all-out battle".

n = 2 is for hypothesis generation, not conclusion. If `n<300 で結論を出さない` is in the skip list, always frame findings as "what would it take to confirm this in N more matches?" rather than declarative claims.

### Phase 4.5 — Adoption write-back to `hypotheses.md`

Run only when `hypotheses.md` exists. Read → edit → write back. **Only the verdict for the analyzed iter is written.** The next-iteration decision (deepen / broaden / list-consume) is made by `experiment-plan` Step 0.5 when it reads this file later — do not touch `状態:` or append new hypothesis rows here.

**What to write back**:

1. **Hypothesis checkbox update** — change the `- [ ]` of the hypothesis tied to the analyzed iter (e.g. H3) to `- [x]` and append an adoption note inline:
   ```markdown
   - [x] (P1) H3: focal α 0.25→0.75 — adopted (iter9: 5/100 vs baseline_v5, inconclusive @300)
   ```
2. **Update / replace the iter's row in the Iteration log table** — iter / start time / hypothesis# / plan path / run_id / primary metric / verdict / result path / analysis path. (`experiment-execution` Phase 8 already added a provisional row marked `(analysis 未実施)`; replace that row with the final verdict + analysis path.)
3. Update **last-updated date** (`最終更新`) to session `currentDate`.

**Out of scope for this skill** (handled by `experiment-plan` Step 0.5 instead):

- ❌ Do **not** rewrite `状態:` (no auto `paused` here).
- ❌ Do **not** append `- [ ] (auto, deep) ...` follow-up hypotheses.
- ❌ Do **not** count consecutive rejections to trigger broaden.

The replay-derived `where_to_focus_next` and follow-up-suggestion content goes into the `iter*_analysis.md` write-up and Phase 6's NEXT ACTION report — `experiment-plan` reads those when deciding the next iter's mode.

When `hypotheses.md` does not exist, skip Phase 4.5 entirely.

### Phase 5 — Summary report

Structured Japanese report to the user (always include the paths to `result_1.md` / `result_2.md`):

- **2-match headline comparison** (omit in skip mode): planets / ships / production / total_turns delta table
- **why_lost**: decisive turn + 3–5 key events + up to 3 candidate hypotheses with supporting/refuting evidence
- **what_worked**: 2–3 behaviors that worked, with turn numbers
- **where_to_focus_next**: turn ranges + metrics to watch
- **`hypotheses.md` updates**: verdict written for the analyzed iter (checkbox + Iteration log row), in 1 line. Next-iter decision is left to `experiment-plan`.

### Phase 6 — NEXT ACTION suggestions

Suggest 2–3 concrete follow-ups, e.g.:

- "seed×10 で同一傾向か再評価" (increase n or re-run the same case)
- "turn N–M の action 分布を抽出して passive gating 検証"
- "次 iter で <仮説に基づく修正> を実装" (→ `/experiment-plan` will pick the mode and may auto-append a deepen hypothesis)
- "replay-viewer で seed=X を目視確認" (→ `/replay-viewer`)
- "ジャンル全体の筋を見直したい" (→ `/experiment-plan` will detect broaden and recommend `/experiment-hypothesize`)

Do not auto-spawn other skills. Suggest by name only.

## Python scripts: usage and spec

### Layout

- `.agents/skills/experiment-analysis/scripts/replay_to_markdown.py` — converts two replays to Markdown (Phase 3)
- `.agents/skills/experiment-analysis/scripts/pick_match_pair.py` — auto-picks "long match + fastest loss" from the population (default Phase 2 strategy)

### Phase 2 helper: `pick_match_pair.py`

```bash
python3 .agents/skills/experiment-analysis/scripts/pick_match_pair.py \
  --replays-dir /Users/user/project/orbit-wars/data/lake/selfplay/matches/replays \
  --self-player-id 1 \
  --limit 200
```

stdout is exactly two lines (`long\t<abs_path>` / `fastest_loss\t<abs_path>`). Codex parses these and feeds them into `replay_to_markdown.py`.

| arg | default | description |
|---|---|---|
| `--replays-dir` | (required) | directory containing `*.json.gz`; symlinks OK |
| `--self-player-id` | `1` | own player ID |
| `--limit` | `200` | scan only the latest N files |
| `--long-quantile` | `0.75` | upper quartile threshold for `total_turns` |
| `--fast-quantile` | `0.25` | lower quartile threshold for `total_turns` |

### Phase 3 main: `replay_to_markdown.py`

```bash
python3 .agents/skills/experiment-analysis/scripts/replay_to_markdown.py \
  --replay <ABS_PATH_A.json.gz> --replay <ABS_PATH_B.json.gz> \
  --label win --label loss \
  --out-dir data/output/experiment/{family}/case{N}/replay_analysis/<id>/
```

No `uv` needed (stdlib only). Always pass **absolute paths** when running from a worktree.

| arg | required | default | description |
|---|---|---|---|
| `--replay PATH` | yes (×2) | — | absolute path to `.json.gz` |
| `--label LABEL` | yes (×2) | — | `win` / `loss` / `seed42` etc. |
| `--out-dir DIR` | yes | — | output directory |
| `--player-id INT` | no | inferred from label | viewpoint player ID |
| `--ship-loss-abs INT` | no | `20` | absolute threshold for ship-loss-burst detection |
| `--ship-loss-rel FLOAT` | no | `0.30` | relative threshold for ship-loss-burst detection |
| `--full-stats` | no | OFF | include full per-turn stats table |

Output Markdown layout:

```markdown
# Replay seed={N} — {label}

## Meta
- file / viewpoint / winner / rewards / statuses / total_turns

## Headline stats (final)
| metric | self | opponent |

## Turning points (top 5 by ship-margin delta)
| turn | delta | side | note |

## Key events
| turn | side | type | detail |

<details><summary>Full per-turn stats</summary>  ※ --full-stats 指定時のみ
| turn | mp | op | ms | os | mpr | opr | mif | oif |
</details>
```

Size guard: ~600 lines / ~40KB asserted in the script. On overflow, trim events to 30 turns and force `--full-stats` OFF. 1v1 is the primary support; FFA is allowed with a WARN.

## Risk gates this skill enforces

- **Honor the `hypotheses.md` skip list.** When `replay 分析を行わない` is set, Phase 2 is skipped.
- **Adoption write-back only.** Update the hypothesis-row checkbox + Iteration log row + `最終更新`. Do **not** touch `状態:`, do **not** append new hypothesis rows. State transitions belong to `experiment-plan` Step 0.5.
- **Don't conclude from n = 2.** Only generate hypotheses. When `n<300 で結論を出さない` is set, always include a confirmation plan.
- **Never paste raw replay JSON / per-turn tables into Codex's chat.** Always go via the script.
- **No code edits / commits / RunPod / Kaggle submission.** Read-only on code; only the limited `hypotheses.md` write-back is permitted.
- **Never use Kaggle publicScore in the verdict** (project rule).
- **NEXT ACTION suggestions are advisory only.** Never auto-spawn other skills.

## Common shapes

| User says… | Skill behavior |
|---|---|
| `/experiment-analysis` | Phase 1 confirms the case → Phase 1.5 picks "直前 iter のみ" ⭐ → Phases 2–6. |
| "勝った試合と負けた試合を比較して" | Phase 1.5 = "直前 iter"; Phase 2 picks `win + loss`. |
| "case2 の敗因を replay から深掘り" | Phase 2 picks `loss × 2`; weight Phase 4 toward why_lost. |
| "iter9 で何が機能してた?" | Phase 1.5 = iter9; Phase 2 picks `win × 2`. |
| "直近 inconclusive iter まとめて" | Phase 1.5 = "inconclusive のみ"; pick a representative pair. |
| "seed=42 と seed=99 比較して" | Phase 2 = "seed 直接指定"; feed the two files directly to the script. |
| "replay は要らない、result.md だけで分析して" | hypotheses.md skip list contains `replay 分析を行わない` (or session-level flag) → skip mode (Phase 4 only). |

## Things to avoid

- Pasting raw replay JSON into Codex's chat. Use the script.
- Forgetting Phase 4.5 when `hypotheses.md` exists.
- Touching `状態:` or appending new hypothesis rows. Those are `experiment-plan` Step 0.5's domain.
- Treating n = 2 as conclusive. Stay at hypothesis generation.
- Citing Kaggle publicScore as evidence.
- Auto-spawning `/experiment-hypothesize` or `/experiment-plan`.
- Putting machine-generated artifacts (JSON / tables) under `docs/experiment/`. They go under `data/output/experiment/`.

## Language

- Internal reasoning and thinking should be in English
- **All user-facing output, a concise user question labels/descriptions, and the analysis summary must be in Japanese** (per `.codex/AGENTS.md`)
