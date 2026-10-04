---
name: scbe-world-anvil-lore-rag-7th-tongue
description: Build and operate a lore-focused RAG system using World Anvil exports and SCBE docs, with deterministic Claude/Codex cross-talk packets for handoff. Use when users ask to structure lore canon retrieval, sync worldbuilding data, enforce citation-grounded generation, or coordinate a 7th Tongue overseer lane across multiple AI agents.
---

# SCBE World Anvil Lore RAG (7th Tongue)

Use this skill to turn World Anvil structure into a local, queryable lore index and keep Codex/Claude synchronized through packetized handoffs.

## Quick Start

1. Build index from exports + docs:

```bash
python C:/Users/issda/.codex/skills/scbe-world-anvil-lore-rag-7th-tongue/scripts/build_lore_index.py \
  --repo-root C:/Users/issda/SCBE-AETHERMOORE \
  --inputs exports/world_anvil docs content/articles/story_series notes \
  --db artifacts/lore_rag/world_anvil_lore.sqlite
```

2. Query lore:

```bash
python C:/Users/issda/.codex/skills/scbe-world-anvil-lore-rag-7th-tongue/scripts/query_lore_index.py \
  --repo-root C:/Users/issda/SCBE-AETHERMOORE \
  --db artifacts/lore_rag/world_anvil_lore.sqlite \
  --query "Kael OR future OR \"seventh tongue\"" \
  --top-k 10
```

SQLite FTS uses query operators; use `OR` for broad recall and quotes for phrase matches.

3. Emit cross-talk handoff packet:

```bash
python C:/Users/issda/.codex/skills/scbe-world-anvil-lore-rag-7th-tongue/scripts/emit_crosstalk_packet.py \
  --repo-root C:/Users/issda/SCBE-AETHERMOORE \
  --sender agent.codex \
  --recipient agent.claude \
  --summary "7th Tongue lore index refreshed; citations ready for generation lane." \
  --next-action "Claude generate lore answer using only top cited chunks."
```

4. Live sync from World Anvil API (then index):

```bash
python C:/Users/issda/.codex/skills/scbe-world-anvil-lore-rag-7th-tongue/scripts/sync_world_anvil_live.py \
  --repo-root C:/Users/issda/SCBE-AETHERMOORE \
  --self-test

python C:/Users/issda/.codex/skills/scbe-world-anvil-lore-rag-7th-tongue/scripts/sync_world_anvil_live.py \
  --repo-root C:/Users/issda/SCBE-AETHERMOORE \
  --endpoints articles,categories,timelines,maps,manuscripts,chronicles,secrets
```

If env vars are not set, the sync script can read from DPAPI mirror services (`world_anvil_app_key`, `world_anvil_user_token`) automatically.

Store keys into DPAPI mirror (one-time):

```bash
python C:/Users/issda/.codex/skills/scbe-api-key-local-mirror/scripts/key_mirror.py store --service world_anvil_app_key --env WORLD_ANVIL_APP_KEY
python C:/Users/issda/.codex/skills/scbe-api-key-local-mirror/scripts/key_mirror.py store --service world_anvil_user_token --env WORLD_ANVIL_USER_TOKEN
```

No-live-account test mode:

```bash
python C:/Users/issda/.codex/skills/scbe-world-anvil-lore-rag-7th-tongue/scripts/sync_world_anvil_live.py \
  --repo-root C:/Users/issda/SCBE-AETHERMOORE \
  --output-dir exports/world_anvil/mock_sync_test \
  --mock
```

## Codex + Claude Structure

1. `KO/Lead (Codex)`:
- Build/refresh index.
- Run primary retrieval queries.
- Emit packet with retrieval proof.

2. `RU/Canon Guard (Claude)`:
- Consume packet.
- Generate lore output strictly from citations.
- Flag canon conflicts as `needs-reconcile`.

3. `EL/7th Tongue Overseer`:
- Resolve conflicts between outputs.
- Enforce final canon decision with packetized audit.

## Output Contract

- Local index DB: `artifacts/lore_rag/world_anvil_lore.sqlite`
- Query results: JSON output from `query_lore_index.py`
- Packet artifacts:
- `artifacts/agent_comm/YYYYMMDD/*.json`
- `artifacts/agent_comm/github_lanes/cross_talk.jsonl`
- `notes/_inbox.md`

## Invariants

- Keep source-grounded answers with explicit chunk citations.
- Prefer World Anvil export records when available; use repo docs as fallback context.
- Keep all handoffs deterministic and packetized.
- Never include raw secrets in packets.

## Resource Guide

- `scripts/build_lore_index.py`: Parse exports/docs and build SQLite FTS index.
- `scripts/query_lore_index.py`: Retrieve top lore chunks with citation metadata.
- `scripts/emit_crosstalk_packet.py`: Append Claude/Codex handoff packet.
- `scripts/sync_world_anvil_live.py`: Pull live World Anvil API data to local exports.
- `references/world_anvil_field_mapping.md`: Field normalization and expected export shapes.
