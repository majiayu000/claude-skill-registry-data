---
name: model-strategy
version: 2.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-06-13
description: Multi-model orchestration and model-switching strategy. Score-based model selection, cross-agent delegation (Gemini, Codex, Ollama), advisor pairing, escalation triggers, permission matrix, and cost-efficiency optimization.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="model-strategy banner">

> **English** — Official English version of `model-strategy`.


# Model-Switching Strategy (English)

> Multi-model orchestration: score-based model selection, cross-agent delegation, advisor pairing, escalation triggers, and cost-efficiency optimization

---

## 1. Model catalog

### Claude (subagent-capable via the Agent tool)

```
Level 4 (Reviewer):   Opus 4.8  — advisor, math review     [user only: /model, /advisor]
Level 3 (Strategist): Opus 4.6  — architecture, concepts   [subagent: model:"opus"]
Level 3 (Creative):   Fable 5   — creative texts, stories  [subagent: model:"fable"]
Level 2 (Workhorse):  Sonnet 4.6— implementation, debug    [subagent: model:"sonnet"]
Level 1 (Fast):       Haiku 4.5 — boilerplate, formatting  [subagent: model:"haiku"]
```

### External agents (companion scripts / SSH)

```
Level 2-3: Gemini 3.5 pro  — research, scientific databases [agy-companion CLI]
Level 2:   Gemini 3.5 flash— fast research                  [agy-companion CLI]
Level 2-3: Codex 5.5 (GPT) — code review, code generation   [codex-companion CLI]
Level 2:   Codex 4.5 (GPT) — simpler code tasks             [codex-companion CLI]
```

### Local models (token-free, 24/7)

```
Level 1-2: Ollama (Qwen 3.5:35b-a3b) — Haiku-to-Sonnet level [<ollama-host>:11434]
           Invocation: SSH + curl http://<ollama-host>:11434/v1/chat/completions
           Or: delegation via an agent-system control API (if available)
```

### Reachability matrix

| Model | LLM-startable | Invocation path | Constraints |
|-------|---------------|-----------------|-------------|
| Sonnet 4.6 | Yes | `Agent(model:"sonnet")` | — |
| Opus 4.6 | Yes | `Agent(model:"opus")` | — |
| Haiku 4.5 | Yes | `Agent(model:"haiku")` | — |
| Fable 5 | Yes | `Agent(model:"fable")` | — |
| Opus 4.8 | Advisor only | `advisor()` in session | user must set `/advisor` |
| Gemini 3.5 | Yes (Bash) | `companion-for-agy "prompt"` | Windows-only, stdout workaround |
| Codex 5.5/4.5 | Yes (Bash) | `node codex-companion.mjs task "prompt"` | auth required |
| Ollama | Yes (SSH/curl) | SSH + curl to the Ollama host API | VPN/Tailscale must be active |
| Opus 4.8 as main model | No | user: `/model opus 4.8` | user action only |
| Fable 5 as main model | No | user: `/model fable` | user action only |

---

## 2. Score computation

```
Dimensions (0-10):
  CLARITY     : How unambiguous is the task?
  COMPLEXITY  : How many components?
  CREATIVITY  : New solutions needed?
  CONTEXT     : How much prior knowledge?
  CRITICALITY : How important is perfection?

SCORE = (10 - CLARITY) + COMPLEXITY + CREATIVITY + CONTEXT + CRITICALITY
```

### Score thresholds

| Score | Model | Examples |
|-------|-------|----------|
| 0-8 | Ollama (local host) | prompt generation, summaries, simple texts |
| 9-12 | Haiku | `__init__.py`, formatting, boilerplate |
| 13-22 | Sonnet | implementation, bug fixes, standard code |
| 13-22 | Gemini 3.5 | research, literature search, scientific databases |
| 13-22 | Codex 5.5 | code generation (Luau, Node.js), compute scripts |
| 23-28 | Sonnet + advisor review | complex code with quality check |
| 23-35 | Fable 5 | creative texts, marketing, storytelling |
| 29-40 | Opus 4.6 | architecture, strategy, paper writing |
| 35-50 | Opus 4.6 + advisor | proofs, architecture decisions, statistics |
| 40-50 | Opus 4.8 (user recommendation) | mathematical proof work, highest rigor |

---

## 3. Cross-agent delegation

### Which external agent for what?

| Task | Best agent | Reason |
|------|-----------|--------|
| Scientific literature search | Gemini 3.5 pro | native OpenAlex/arXiv/PubMed skills |
| Code review (second opinion) | Codex 5.5 | independent perspective |
| Simple text generation | Ollama (local host) | token-free, 24/7 |
| Creative texts, marketing | Fable 5 | strongest creative output |
| Mathematical proofs | Opus 4.8 (advisor) | highest analytical depth |

### Exclusions (documented weaknesses)

- **Gemini:** NOT for mathematical reviews/proof work (documented direction error in a proof review, 2026-06-07)
- **Codex 4.5:** only when 5.5 is unavailable; otherwise always 5.5

### Invocation paths

> Replace the placeholders `<host>`, `<ollama-host>`, `<tailscale-ip>`, `<user>`, and `~/.ssh/<key>` with your own infrastructure.

**Gemini (via companion-for-agy):**
```
companion-for-agy --researcher --json --timeout 120000 "research prompt"
```

**Codex (via codex-companion):**
```
node "~/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs" task --effort high "code prompt"
```

**Ollama on a remote host (via SSH):**
```
ssh -i ~/.ssh/<key> <user>@<tailscale-ip> "curl -s http://localhost:11434/v1/chat/completions -d '{\"model\":\"qwen3.5:35b-a3b\",\"messages\":[{\"role\":\"user\",\"content\":\"Prompt\"}]}'"
```

**Delegation to an agent system with tools (example):**
```
curl -s -X POST http://<host>:8081/api/chat -H "Content-Type: application/json" -d '{"prompt": "...", "chat_id": "claude-delegate"}'
```

---

## 4. Advisor pairing

### Mechanics

`advisor()` is a **session-level tool** — the advisor model is set by the user via `/advisor`, not programmatically. This yields these pairing patterns:

| Pattern | How it works | When to use |
|---------|--------------|-------------|
| **Session advisor** | user sets `/advisor opus 4.8`, agent calls `advisor()` | standard for proofs/architecture |
| **Orchestrator-as-reviewer** | Opus main model reviews Sonnet subagent output | orchestrator is stronger than the worker |
| **Counter-agent** | agent A works, agent B checks adversarially | independent verification, 2 perspectives |
| **User recommendation** | agent recommends: "do this task with opus 4.8 + advisor" | when the current session is too weak |

### When to recommend an advisor?

- Mathematical proof work (score ≥ 35)
- Architecture decisions with long-term consequences
- Statistical methodology / study design
- Complex bugs after 2+ unsuccessful debug cycles

### When NOT to use an advisor?

- Routine code, content, formatting (score < 23)
- Simple feature implementation
- Well-defined, non-critical tasks

---

## 5. Escalation triggers

### Ollama -> Haiku
- File access required
- Code analysis needed

### Haiku -> Sonnet
- More than 2 files affected
- Decision between alternatives needed
- Unexpected error occurred
- Delete operation requested

### Sonnet -> Opus
- Architecture decision required
- 3+ systems must be integrated
- Requirements contradictory/unclear
- Strategic planning needed

### Sonnet -> Gemini (lateral)
- Scientific research needed
- Bibliography verification

### Sonnet -> Codex (lateral)
- Code review as a second opinion
- Advisor overloaded (fallback reviewer)

### Opus -> Opus + advisor
- Proof review needed
- Critical architecture decision
- Statistical methodology

### De-escalation
- Concept defined -> Sonnet takes over implementation
- Task trivial/repetitive -> Haiku takes over
- Text only, no tool access -> Ollama takes over

---

## 6. Permission matrix

| Operation | Ollama | Haiku | Sonnet | Opus | Gemini | Codex |
|-----------|--------|-------|--------|------|--------|-------|
| Read files | - | Yes | Yes | Yes | Yes* | Yes* |
| Write files | - | Yes | Yes | Yes | Yes* | Yes* |
| Delete files | - | - | Yes** | Yes | - | - |
| System commands | - | - | Yes** | Yes | Yes* | Yes* |
| Architecture decisions | - | - | - | Yes | - | - |
| Web research | - | - | Yes | Yes | Yes | - |
| Call advisor() | - | - | Yes | Yes | - | - |

*via companion script in its own sandbox mode
**with user confirmation

---

## 7. Cost efficiency

### Token savings through routing

| Task type | Without routing | With routing | Savings |
|-----------|-----------------|--------------|---------|
| Trivial | Opus tokens | Ollama (free) | 100% |
| Boilerplate | Opus tokens | Haiku tokens | ~80% |
| Standard code | Opus tokens | Sonnet tokens | ~50% |
| Research | Claude tokens | Gemini tokens | ~70% (different budget) |
| Code review | advisor() tokens | Codex tokens | ~60% (different budget) |

---

## 8. Golden rule

> "Opus thinks, Sonnet builds, Haiku executes, Ollama saves. Gemini researches, Codex reviews, Fable narrates."

---

## Changelog

### 2.0.0 (2026-06-12)
- Cross-agent delegation: Gemini, Codex, Ollama (local host) as routing targets
- Advisor pairing: 4 patterns (session advisor, orchestrator-as-reviewer, counter-agent, user recommendation)
- Reachability matrix: LLM-startable vs. user-only documented
- Ollama (Qwen 3.5:35b-a3b, Haiku-to-Sonnet level) added as level 1-2
- Lateral escalation: Sonnet -> Gemini (research), Sonnet -> Codex (review)
- Exclusions documented (Gemini not for math)
- Score thresholds extended to all models

### 1.0.0 (2026-03-15)
- Ported from BACH v3.8.0 (ing-strategie v2.0.0)

---

*Ported from BACH v3.8.0 | Extended with cross-agent + advisor v2.0.0*
