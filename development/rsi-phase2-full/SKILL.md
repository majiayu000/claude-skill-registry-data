---
name: rsi-phase2-full
description: "RSI Phase 2: Full learned proposal integration"
---
# RSI Phase 2: Full Learned Proposal Integration

## Overview
Extend `propose_improvement()` to accept optional `model=` parameter and integrate learned proposals from 2B model with safety-rule validation.

## Architecture

### `propose_improvement(target, content, model=None)`

**ALWAYS** run first: Rule-based proposals (P1-P7 expanded)
- P1: CYCLE_SECONDS timing (>300s → suggest 300)
- P1b: Function-level max_tokens defaults
- P2: max_tokens too small (<100 → suggest 200), both module + function level
- P2b: Duplicate rejection of capacity-fn proposals
- P5: Duplicate module-level import dedup
- P3: Missing error context in except blocks
- P4: Stale comment fixes
- P6: Function signatures without type hints
- P7: **Learned proposals from 2B model** (NEW - only if model provided)

**IF model is provided:**
1. Construct prompt with target file + current content (first 2000 chars)
2. Call model via localhost:8081 with:
   - Model: mini-openamer
   - Temperature: 0.7
   - Max tokens: 300
   - Prompt: "You are OpenAmer improving its own code. Target: {target}. Find ONE improvement: make code better, don't break compilation, don't lose bindings. Return: (kind, old_pattern, new_pattern, reason) OR None"
3. Parse response as 4-tuple: (kind, old, new, reason)
4. Validate:
   a. old pattern exists in content (string `old in content`)
   b. Module bindings preserved (AST compare: lost symbols ≤ 2)
   c. kind in allowed set: {"capacity","timing","capacity-fn","logging","comment-fix","hinting","func-param"}
   d. reason is non-empty string
5. IF ALL validation passes: ADD to proposals list
6. IF ANY validation fails: SKIP (rules still work fine)

**Safety never violated:**
- Never break compilation (sandbox py_compile test always runs in apply_and_test)
- Never lose critical bindings (AST gate, max 2 symbols lost allowed)
- Never accept pattern that doesn't exist in content
- Always have non-empty reason

### `_learned_proposal(target, content, model)` Helper
- Constructs prompt, calls model, parses response, validates, returns tuple or None
- Catches all exceptions soft - never crashes the cron job

### Integration with `improve_once()`
```
proposals = propose_improvement(target, content)  # rules only
# THEN, if model available:
if model is not None:
    learned = _learned_proposal(target, content, model)
    if learned:
        # Validate one more time with apply_and_test gates
        proposals.append(learned)
# Then: sandbox, test, switch, log as before
```

## Proposal Kinds (expanded from Phase 1)
- "capacity": max_tokens increase (module level)
- "timing": CYCLE_SECONDS decrease
- "capacity-fn": function-level max_tokens defaults
- "logging": except block + print error context
- "comment-fix": stale comment corrections
- "hinting": add type hints to function signatures
- "func-param": function parameter pattern optimization
- "learned": **NEW** - model-generated improvements (validated by above gates)

## Success Metrics (Phase 2)
- ≥1 learned proposal accepted per 10 rotation cycles
- 0 compilation failures from learned proposals
- 0 binding-loss incidents from learned proposals (>2 lost symbols = reject)
- Proposal acceptance rate stabilizes at 20-30% (model learns what works)
- Phase 3 transition: ≥5 accepted per 10 cycles → extract templates → build permanent rule library

## Rollback
- Existing git/shutil mechanism covers it
- If learned proposal causes issues: `git checkout -- target_file`
- No special handling needed - existing `apply_and_test()` rollback infrastructure

## Phase 3 Transition (1 Monat)
When learned proposals reach ≥5 accepted per 10 cycles:
1. Extract successful pattern templates from accepted learned proposals
2. Convert successful learned patterns into new permanent rule-based patterns (P8, P9, etc.)
3. Build pattern library from model-learned improvements
4. Some learned patterns become permanent rules, reducing model dependency
5. Phase 3: Cross-Domain Metasketart Extraction (fähigkeitenübergreifendes Extrahieren)

## Risks & Mitigations
| Risk | Mitigation |
|---|---|
| Model generates broken code | Validation gates (compilation test, binding check, pattern existence) |
| Model learns bad patterns | Human review of first 20 accepted proposals; acceptance rate monitoring |
| Performance degradation | Only run learned proposals every N cron cycles (e.g., every 3rd) |
| Model unavailable | Graceful fallback: rules only, log "model_unavailable" in improvements.jsonl |
| Prompt injection in model output | Strict output format validation (4-tuple required, kind in allowed set) |

## File Locations
- **Core**: `~/AppData/Local/openamer-laptop/scripts/training/self_improve.py` (enhanced `propose_improvement()`)
- **Skill**: `~/AppData/Local/openamer-laptop/skills/rsi-phase2-full/SKILL.md` (documentation)
- **World Model**: `~/AppData/Local/openamer-laptop/memory/world_model.jsonl` (phase2 design log entry)
- **Logging**: `~/AppData/Local/openamer-laptop/improvements.jsonl` (all proposal attempts logged)

## Phase 2 Implementation Checklist
- [ ] Enhance `propose_improvement()` to accept optional `model=` parameter
- [ ] Implement `_learned_proposal()` with prompt engineering and model call
- [ ] Add validation gates (pattern exist, bindings ≤2 lost, kind allowed, reason non-empty)
- [ ] Integrate with `improve_once()` - learned proposals run after rules
- [ ] Test with model available (localhost:8081) and not available (graceful fallback)
- [ ] Log all learned proposal attempts to `improvements.jsonl`
- [ ] Track acceptance rate over first 50 rotation cycles
- [ ] Document accepted vs rejected patterns for Phase 3 analysis

## Phase 3 Transition Trigger
Mathematische Bedingung: `accepted_learned / total_learned_attempts >= 0.5` (mindestens 5 von 10 Zyklen akzeptiert)

Bei Trigger:
1. Muster-Extraktion aus akzeptierten learned proposals
2. Neue permanente Regeln P8, P9 etc. generieren
3. Pattern Library aktualisieren
4. Akzeptanzrate monitoring fortsetzen
5. Phase 3: Cross-Domain Metasketart Extraction starten
PYEOF