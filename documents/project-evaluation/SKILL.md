---
name: project-evaluation
description: Discover, clone, build/test, and evaluate candidate open-source projects
user-invocable: true
disable-model-invocation: false
---

# Project Evaluation

When user asks "find something like X / evaluate Y / compare candidates":

1. **Search** — `web_search` for "open source alternative to X" + GitHub topic search via `web_search`/`browser`. Collect 5–8 candidates.
2. **Inspect** — `web_fetch` repo README, `browser` for stars/issues/last commit, note license, stack, architecture.
3. **Rank** — Score by activity, docs, tests, maintenance, fit. Pick 2–3 promising to clone.
4. **Clone & Build** — `exec` inside sandbox: `git clone` → `/data/projects/<slug>/source`, `npm/pip/cargo install`, `build`, `test`. Use controlled `network: bridge` for installs (see `docs/sandbox.md`).
5. **Verify** — Run app/tests, check `build result`, `test result`, `runtime result`, `resource usage`. Distinguish **README claims vs verified by running**.
6. **Report** — Markdown table + per-project section:
   - Project / Repository / License / Last meaningful activity / Tech stack / Architecture
   - Installation difficulty / Build result / Test result / Runtime result / Resource usage
   - Strengths / Weaknesses / Best use case / Recommendation
7. **Artifacts** — Keep `source` + `metadata` (eval json/md) under `/data/projects/<slug>/`. Persist evaluation md to `/data/documents/research/YYYY-MM-DD-<query>-evaluation.md` and deliver via `message`.
8. **Compare** — Ranked summary with clear recommendation.
