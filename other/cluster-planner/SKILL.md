---
name: cluster-planner
description: Layer 6 of the keyword research pipeline. Organizes the vetted keyword queue into money clusters (from clusters.md), picks each cluster's keystone vs supporting articles, tracks coverage, and PROPOSES new clusters from high-business-value topics or live products not yet covered — so the blog strategy expands as the company grows. Emits cluster-tagged queue + cluster-map.md + cluster-proposals.md.
allowed-tools: Read, Write, Edit, Bash
---

# Cluster Planner Skill

Turn the flat, ranked keyword queue into a **strategy**: a few **money clusters**, each a business-value parent topic tied to a live product, with a keystone article + a supporting ring. This is the layer that makes us publish *on a plan* instead of one-off keywords. See `STRATEGY.md` §1.

**It is also the engine's anti-"stuck" mechanism:** every run it proposes NEW clusters when it finds high-business-value demand, or a live product, that no cluster covers yet. The cluster list is a *living* config, never a fixed list.

## Input
`/cluster-planner` (no args). Reads:
- `content-pipeline/0-keywords/clusters.md` — the cluster config (the control surface; `status: active`/`planned`/`archived`).
- `content-pipeline/0-keywords/keyword-queue.csv` — the vetted, ranked, winnability-scored queue from `/keyword-prioritization`.
- `brand-config.md` → **Products / Features** — the live product set (to detect products with no cluster).

## Process

1. **Read the active clusters** from `clusters.md` (skip `archived`; treat `planned` as not-yet-coverable but track them).

2. **Assign each queued keyword to a cluster.** Match on relevance to the cluster's `parent_topic` + `seeds` (token/topic overlap; a keyword may only belong to ONE cluster — its best match). A keyword that matches no active cluster → `cluster = unclustered`.

3. **Per cluster, pick the keystone + supporting ring.** The keystone is the deep, definitive hub the cluster's internal links point to — and it MUST be winnable (never a hub we can't rank). Pick in this order:
   - The cluster's **`parent_topic`** term is the *strategic* keystone target. If a member matching the parent_topic is **winnable** (`winnability ≥ 5`), it's the active **`keystone`**.
   - If the parent_topic term is **above-ceiling** (`winnability ≤ 3` — too hard for our DR right now), tag it `role = planned_keystone` (the head term we build *toward* as DR rises — `STRATEGY.md` §2) and **promote the best WINNABLE member as the active `keystone`**. Among winnable candidates, prefer the **highest `traffic_potential`** (the broadest hub), not the narrowest long-tail — the keystone should be a broad term others link up to.
   - If **no member of the cluster is winnable**, set `coverage = keystone_deferred` and leave no active keystone — build the supporting ring first; the keystone unlocks when DR rises.
   - **Supporting** = every other member (sub-topics, long-tail, intent variants) — each its own article, internally linked up to the keystone.
   - Tag every row: `cluster` (id) + `role` (`keystone`|`planned_keystone`|`supporting`).
   - **Winnable-first ordering:** within a cluster, order by `winnability` then `priority_score`, so we build the rankable members before the reach ones (`STRATEGY.md` §2 — ambition expands as DR grows).

4. **Coverage check.** For each active cluster flag: `no_keystone` (zero members in the pool → a seeding gap to fill via Layer 1b), `keystone_deferred` (members exist but none winnable yet — supporting-only until DR rises), `thin` (< 3 supporting members), or `healthy`. A cluster whose parent_topic is above-ceiling but has a winnable active keystone is still `healthy` (the head term sits as `planned_keystone`).

5. **Cluster discovery — propose new clusters (the self-extension).** Two sources:
   - **Uncovered demand:** cluster the `unclustered` rows by theme; if a theme has ≥ 3 members that are **winnable** (winnability ≥ 5) AND **business-value ≥ 2**, propose it as a new cluster candidate (suggested `id`, `name`, `parent_topic` = highest-`traffic_potential` member, `seeds` = the theme's terms).
   - **Uncovered products:** compare each live product/feature in `brand-config.md` against the `product` column of active clusters. Any **live** product with no cluster → propose a cluster for it (so a newly-shipped product gets a blog beachhead even if `clusters.md` lags). Ignore `coming-soon`/`roadmap` products (don't propose clusters for things we can't demo yet).
   - Never auto-edit `clusters.md` — write proposals for human/EO review (adding a cluster is a deliberate strategy call).

6. **Write outputs:**
   - **Cluster-tag the queue (ATOMIC — PLE-3063 item 4):** read the *entire* `keyword-queue.csv`, add/update the `cluster` + `role` values for every row **in memory**, then `Write` the whole file back in one shot. **Never use `Edit` to patch individual cells / the role column in place** — a linter/format hook can race a partial `Edit` and corrupt or half-tag the queue (that's the "mutated queue role column" bug). One read → mutate the full table → one `Write`. Preserve column order and every other column untouched; no row duplication.
   - **`content-pipeline/0-keywords/cluster-map.md`** — per active cluster: keystone (keyword + slug + priority + winnability), supporting count, coverage status. The at-a-glance strategy board.
   - **`content-pipeline/0-keywords/cluster-proposals.md`** — the new-cluster candidates from step 5, each with why (members, traffic, BV) and a ready-to-paste `clusters.md` row. Empty file with "no new clusters proposed" if none.

7. **Tell the user / log:** one line per active cluster (`<name>: keystone "<kw>" (winnability X, priority Y), N supporting, <coverage>`), then `N new cluster(s) proposed` (or none).

## Output
- `keyword-queue.csv` gains `cluster` + `role` columns (every queued row tagged).
- `cluster-map.md` — the live cluster board (keystone + ring + coverage per cluster).
- `cluster-proposals.md` — new-cluster candidates (the growth feed).

## Autonomous behavior (Layer 6 of /keyword-research-pipeline)
- Run AFTER `/keyword-prioritization` (it needs `priority_score` + `winnability`).
- Only cluster rows that reached the queue (BID-PASS, not tool-led, not gap=strong).
- In autonomous mode, skip the user-facing suggestion; emit the one-line-per-cluster summary + the proposal count, and ensure `cluster-map.md` + `cluster-proposals.md` are written for the publish loop + the operator to read.

## Quality checklist
- [ ] Every queued keyword has a `cluster` (or `unclustered`) + `role`.
- [ ] Every active cluster with ≥1 winnable member has exactly one active `keystone`, and that keystone is **winnable** (`winnability ≥ 5`) — an above-ceiling keystone is a bug; it should be `planned_keystone` with a winnable member promoted.
- [ ] `cluster-proposals.md` actually fires when the queue contains a winnable, high-BV theme outside the current clusters (the anti-stuck check — if it never proposes anything across many runs while unclustered winnable rows exist, the discovery step is broken).
- [ ] No cluster maps to a `coming-soon`/`roadmap` product (we can't demo it → not a money cluster yet).

## Discipline
- A cluster must be **product-led** (BV ≥ 2). Don't invent clusters for high-traffic, no-product-fit themes (the GIF trap — `STRATEGY.md` anti-pattern #8); route those to `unclustered` and leave them.
- The keystone is chosen on **winnable** traffic potential, not raw volume — a parent topic we can't rank for yet stays a *planned* keystone until DR supports it (`STRATEGY.md` §2).
