---
name: maybe-hft
description: Use when hedging EA dengan sistem trailing stop dan pending order otomatis.
  Converted dari MQL5, cross-platform (Windows/Linux/Mac). Compatible dengan mt5linux
  Docker. Use when working with maybe hft.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
- analysis
- docker
- hft
- investigation
- maybe
- research
metadata:
  openclaw:
    emoji: 🛡️
    requires:
      python: true
      pyEnv: trading-venv
  parameters:
    lots:
      type: float
      default: 0.1
      desc: Ukuran lot per transaksi
    stoploss:
      type: int
      default: 1500
      desc: StopLoss dalam point
    trailing:
      type: int
      default: 500
      desc: Jarak trailing dalam point
    trail_start:
      type: int
      default: 1000
      desc: Profit minimal sebelum trailing aktif
    x_distance:
      type: int
      default: 300
      desc: Jarak pending dari SL
    start_direction:
      type: int
      default: 0
      desc: 0=BUY dulu, 1=SELL dulu
      choices:
      - 0
      - 1
    broker:
      type: str
      default: auto
      desc: 'Broker: mt5, simulated, auto'
      choices:
      - mt5
      - simulated
      - auto
    mode:
      type: str
      default: paper
      desc: 'Mode: paper, live'
      choices:
      - paper
      - live
    once:
      type: bool
      default: false
      desc: Jalan sekali aja, tidak loop
version: 1.0.0
category: research
---

# Maybe Hft

## When to Use

**Trigger phrases:**
- "maybe hft"
- "Help me with maybe hft"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


> *"The way to build long-term returns is through preservation of capital and home runs."* — **Paul Tudor Jones**

Expert Advisor cross-platform berbasis Python untuk trading hedging dengan sistem trailing stop dan pending order otomatis.


## When NOT to Use

- When the answer is already known and documented
- For time-sensitive decisions that cannot wait for thorough research
- When the topic is outside your domain of competence


## Overview

Maybe Hft enables thorough investigation with structured methodology.

## Workflow

```python
# Example: Source evaluation
def evaluate_source(url: str) -> dict:
    return {
        "authority": check_domain_authority(url),
        "currency": get_last_updated(url),
        "objectivity": detect_bias(url),
        "accuracy": cross_reference(url),
    }
```

1. **Define question** — Clarify the research objective
2. **Gather sources** — Collect primary and secondary data
3. **Analyze** — Apply analytical frameworks to findings
4. **Synthesize** — Combine insights into actionable conclusions
5. **Present** — Deliver findings in clear, compelling format
6. **Archive** — Store research for future reference

## Source Evaluation

- **Authority** — Is the source credible and expert?
- **Currency** — Is the information recent and relevant?
- **Objectivity** — Is there bias or conflict of interest?
- **Accuracy** — Can claims be verified independently?

## Output Format

- Executive summary (1-2 paragraphs)
- Key findings (bullet points)
- Detailed analysis (sections with evidence)
- Recommendations (actionable next steps)
- Sources and methodology

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "First result is good enough" | Deep research finds better answers. Keep digging. |
| "I do not need to verify sources" | Unverified sources lead to wrong conclusions. Always cross-check. |
| "Research is a one-time thing" | Markets change. Research needs to be continuous, not one-off. |


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run maybe hft workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings