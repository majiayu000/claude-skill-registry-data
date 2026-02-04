---
name: deep-research-synthesizer
description: Given outputs from 5 research sub-agents (time-sliced or partitioned), validate and synthesize them into a coherent, citation-backed Markdown deep research report with deduplication, contradiction handling, and explicit debug visibility when inputs are missing or malformed.
license: MIT
compatibility: Framework-agnostic; assumes you can run 5 sub-agents and collect their text outputs (Markdown with a JSON packet header recommended).
metadata:
  author: github.com/anthony-maio
  version: "1.0"
---

# Deep Research Synthesizer

Use this skill when you have **five sub-agent research results** and need to produce a **single high-quality Markdown report** that:
- answers the user’s question directly
- preserves evidence + citations
- removes duplication
- flags contradictions and gaps
- never “silently fails” when one agent output is missing or malformed

This skill is designed to fix a common anti-pattern: *a coordinator prompts 5 agents, then tries to “just synthesize” without a contract, validation, or observability*.

---

## Inputs expected (minimum)

1) `user_question` — the user’s original question (verbatim)

2) `agent_outputs[5]` — one output per agent.  
Each output MUST follow the **Research Packet Contract** (see `references/AGENT_PACKET_CONTRACT.md`).

If you cannot guarantee the contract, run `scripts/validate_packets.py` and repair nonconforming outputs before synthesis.

---

## The 5-agent pattern that works

### Step 1 — Partition the work (pick ONE strategy)

**Strategy A: Time slicing (good for “what happened” / “how it evolved”)**
- Agent 1: earliest timeframe
- Agent 2: next window
- …
- Agent 5: most recent window + “what changed recently”

**Strategy B: Source slicing (good for broad topics)**
- Agent 1: primary sources / official docs
- Agent 2: academic papers / standards
- Agent 3: practitioner writeups
- Agent 4: competing viewpoints / critiques
- Agent 5: synthesis + “what you should do” recommendations

**Strategy C: Sub-question slicing**
- Agent 1: definitions / scope
- Agent 2: current state
- Agent 3: failure modes / risks
- Agent 4: options + tradeoffs
- Agent 5: recommendations + decision framework

### Step 2 — Enforce the Research Packet Contract
Every agent must output:
- a machine-parseable JSON “packet header”
- a short narrative
- a “Run Log” with searches + errors

Contract details: `references/AGENT_PACKET_CONTRACT.md`.

### Step 3 — Validate before you synthesize
Run:

```bash
python scripts/validate_packets.py --in packets/
```

Fix failures immediately:
- missing sources
- missing claims/evidence mapping
- missing run logs
- malformed JSON

### Step 4 — Normalize + deduplicate
Use:
```bash
python scripts/merge_packets.py --in packets/ --out merged.json
```

Then synthesize using the report template:
- `references/REPORT_TEMPLATE.md`
- include contradictions + gaps explicitly

### Step 5 — Synthesize the final report (Markdown)
Write the report in this order:

1. **Executive Summary** (5–10 bullets)
2. **Direct Answer** (2–6 paragraphs)
3. **Key Findings** (grouped, deduped)
4. **Evidence & Citations** (trace claims → sources)
5. **Contradictions / Uncertainties** (what doesn’t match)
6. **Recommendations** (actionable, prioritized)
7. **Appendix**
   - per-agent “Run Log”
   - per-agent “Raw Findings” (optional)

### Step 6 — QA checklist (do not skip)
Use `references/QA_CHECKLIST.md`.

If you can’t pass the checklist due to missing info, output a partial report and explicitly list:
- which agents failed
- what is missing
- what follow-up tasks would resolve it

---

## Failure-handling requirements (what stops “constant failures”)

### 1) Never hide missing agent outputs
If any agent output is missing/empty:
- produce the report anyway
- mark the missing agent as “NO DATA”
- do not invent what it “would have found”

### 2) Surface tool errors verbatim
If an agent hit a tool error (HTTP, MCP, API):
- carry the raw error into the appendix
- summarize the impact in “Limitations”

### 3) Preserve traceability
Every major claim must have:
- source id(s)
- agent id
- confidence

This avoids “big report looks plausible but can’t be debugged.”

---

## Files in this skill

### References
- `references/AGENT_PACKET_CONTRACT.md` — required output format for sub-agents
- `references/REPORT_TEMPLATE.md` — Markdown structure + guidance
- `references/QA_CHECKLIST.md` — deterministic quality gates
- `references/FAILURE_MODES.md` — common causes of synthesis failure + mitigations

### Scripts
- `scripts/validate_packets.py` — validates packet conformance and prints actionable errors
- `scripts/merge_packets.py` — merges packets into a single normalized JSON file
- `scripts/render_report_skeleton.py` — generates a Markdown skeleton from merged JSON
