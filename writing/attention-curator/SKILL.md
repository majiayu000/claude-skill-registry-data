---
name: attention-curator
description: Distill a large, fast-moving research information stream into source-backed recommendations with separate impact, buzz, utility, and attention-budget judgments. Use for PaperTrace radar, daily digests, social trend reviews, or deciding what researchers should read now.
---

# Attention Curator

Turn “everything that happened” into a small set of defensible next reads. Optimize for the reader's limited attention, not content volume.

## Required output

For every selected item, provide:

- the original source and publication date;
- one sentence on what changed;
- `why_now`: why this deserves attention now rather than eventually;
- three independent 0–100 scores: `impact`, `buzz`, and `utility`;
- `attention_budget`: `skim` (3–5 min), `read` (10–25 min), or `deep_dive` (45+ min);
- one concrete next action such as read a section, run a demo, migrate a model, reproduce a result, or join a discussion;
- confidence and any missing evidence.

## Selection rules

1. Start from primary sources: paper, official model/lab announcement, repository, documentation, dataset, or benchmark.
2. Treat X, Xiaohongshu, newsletters, blogs, and public accounts as discovery and discussion signals. Link the underlying primary source whenever one exists.
3. Do not convert likes or reposts into scientific impact. Keep the three scores separate:
   - `impact`: evidence quality, technical consequence, downstream adoption, or field significance;
   - `buzz`: recent, verifiable discussion velocity across public channels;
   - `utility`: runnable code/data/demo, setup cost, and relevance to real research tasks.
4. Never invent engagement counts. If a platform metric cannot be checked, label buzz as qualitative and lower confidence.
5. Reward cross-field transfer when the connection is concrete; do not force every item into AI.
6. Prefer five strong items with distinct reasons over twenty near-duplicates.

## Attention budget

- `skim`: the headline changes awareness but does not change current work.
- `read`: the method, release, or tool may affect a current decision.
- `deep_dive`: the item changes a research workflow, enables a new capability, or needs careful evidence review.

Always state what the reader should learn by the end of the allocated time.

## Publishing

Use concise bilingual copy when writing for PaperTrace. Preserve technical names, version identifiers, dates, and benchmark numbers exactly. Mark vendor claims as reported claims until independently reproduced.
