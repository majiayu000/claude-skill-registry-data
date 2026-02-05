---
name: llm-call
description: External LLM invocation. Triggered ONLY by @council,@probe,@crossref,@gpt,@gemini,@grok,@qwen.
---

# LLM Call

External LLM access. **Only activates on explicit triggers.**

## Triggers

| Trigger | Action |
|---------|--------|
| `@council` | Query all 4 models in parallel |
| `@gpt` | GPT-5.1 only |
| `@gemini` | Gemini 3 Pro only |
| `@grok` | Grok 4.1 Fast only |
| `@qwen` | Qwen3 Max only |
| `@probe` | Follow-up question with auto-context from session history |
| `@crossref` | Models comment on each other's previous responses |

No trigger → Claude handles alone.

**Auto-save:** All requests automatically save to session with step-based folders for history tracking.

## Why This Pattern Exists

**The value is independent perspective, not review.**

If Claude shows its draft to external models, they anchor on it. Instead:
1. Claude forms complete answer first
2. External models answer the same question independently (they never see Claude's draft)
3. Claude compares all answers afterward

**External models cannot:** search web, use tools, see files, or access conversation history. Claude must include all relevant context in the query.

## Workflow - Follow STRICTLY

**Input:** `===QUERY===` (required), `===DRAFT===` (optional), `===PROBE===` (probe only)

**Draft:** If Claude has answered the question, Claude SHOULD NOT include this section in `council` phase to save context window. Claude can pass the draft if the user invoked `@crossref` afterall.

### Single Model (`@gpt`, `@gemini`, `@grok`, `@qwen`)

```bash
cli.py -m single -M gpt << 'EOF'
===QUERY===
Question + context
===DRAFT===  
Claude's answer
EOF
```

### Council (`@council`)

```bash
cli.py -m council << 'EOF'
===QUERY===
Question + context
===DRAFT===
Claude's answer
EOF
```

Add `-c` for confidence ratings.

### Probe (`@probe`)

Follow-up with auto-context from ALL previous steps.

```bash
cli.py -m probe << 'EOF'
===QUERY===
Explain more about [point]
===PROBE===
@gpt
EOF
```

Auto-gathers history → sends to model → saves to new step.

### Crossref (`@crossref`)

**Purpose:** Each model sees what ALL others said and comments on their responses.

Crossref requires Claude's draft. Two ways to provide it:

1. If you already included ===DRAFT=== in the council step:
```bash
   cli.py -m crossref
```

2. If you only sent the query in council (no draft):
```bash
   cli.py -m crossref << 'EOF'
   ===DRAFT===
   Claude's answer here
   EOF
```

**What each model receives:**
- Original question
- Their own previous answer (if they had one)
- Claude's draft (if available)
- All OTHER models' responses

ALL 4 models are always invoked, even if one failed in the council step. A model that failed earlier can still comment on others' responses.

**Session:** Auto-saves to `/tmp/sessions/s_TIMESTAMP/1/`, `/2/`, etc. Each step folder contains `.md` files (query, draft, gpt, gemini, grok).

## Script Reference

| Mode | Usage |
|------|-------|
| `council` | All 4 models (auto-save) |
| `single -M <model>` | One model (auto-save) |
| `probe` | Follow-up with auto-context |
| `crossref` | Models critique each other |
| `status` | Show session |
| `clear` | Delete session |

**Flags:**
- `-M` model (gpt/gemini/grok/qwen)
- `-c` confidence mode
- `-S` session ID or `new` (optional)

## The `-c` Flag (Confidence)

**What it does:** Asks each model to rate its confidence and explain what would change its answer.

**When to use it:**
- Factual/analytical questions where certainty matters
- To surface what evidence each model is relying on

## The `-S` Flag (Session)

**Options:**
- `-S new` — Force create a new session (useful when starting a new topic)
- `-S <session_id>` — Use a specific session (e.g., `-S s_20250101_120000_1234`)
- *(omit)* — Auto-use current session, or create if none exists

**When to use `-S new`:**
- Starting a completely new topic/question
- Want to keep previous session separate