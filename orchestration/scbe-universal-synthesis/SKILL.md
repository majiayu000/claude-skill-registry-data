---
name: scbe-universal-synthesis
description: Orchestrate all installed Codex skills through an auto-updating synthesis matrix with Sacred Tongues routing, emotion/intent metadata, and decodable lexicon packets tied to established SCBE characters. Use when the user asks for cross-skill coordination, auto skill updates, multi-skill routing, or Sacred Tongues intent mapping.
---

# SCBE Universal Synthesis

Use this skill when work spans many installed skills and needs one consistent routing layer.

## Goals

1. Keep a current inventory of installed skills.
2. Route tasks to recommended Sacred Tongues and character lanes.
3. Maintain a decodable lexicon (`prefix:stem`) with emotion + intent.
4. Auto-refresh references so coordination does not drift.

## Core Workflow

1. Refresh synthesis references:
```powershell
python C:/Users/issda/SCBE-AETHERMOORE/scripts/system/refresh_universal_skill_synthesis.py
```

2. Read generated references:
- `references/skill_inventory.json`
- `references/synthesis_matrix.json`
- `references/sacred_lexicon.json`
- `references/summary.md`

3. Select skills by intent:
- Match user request to `categories` and `recommended_tongues` in `synthesis_matrix.json`.
- Pull only the minimal set of skills required for execution.

4. Emit decodable tongue packets:
- Use lexicon tokens like `ko:anchor`, `av:forge`, `ru:verify`, `ca:pulse`, `um:guard`, `dr:release`.
- Decode rule: prefix maps to tongue metadata; stem maps to action semantic.

5. Execute + cross-talk:
- Run selected skills in sequence.
- Mirror updates into terminal lane and Obsidian lane when multi-agent handoff is required.

## Tongue/Character Guidance

Use canonical mappings from generated `sacred_lexicon.json`:
- KO: architect lane (clarity, system design)
- AV: coder lane (creative flow, implementation)
- RU: reviewer lane (discernment, quality review)
- CA: tester lane (assurance, validation)
- UM: security lane (vigilance, protection)
- DR: deployer lane (resolve, release execution)

Prefer established characters from the lexicon payload (`agentic_character`, `runtime_character`) for narrative continuity.

## Safety Rules

1. Never hardcode API keys or secrets in skill files or references.
2. Keep generated references append-safe and reproducible.
3. If a skill has invalid frontmatter, report it and continue with valid skills.
4. Keep orchestration deterministic for governance and audit paths.
