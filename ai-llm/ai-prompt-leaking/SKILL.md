---
name: ai-prompt-leaking
description: >
  Systematically extract hidden system prompts, core directives, and invisible context intentionally 
  concealed within Large Language Model (LLM) applications. This skill utilizes targeted linguistic 
  engineering and boundary manipulation to bypass prompt opacity.
domain: cybersecurity
subdomain: ai-red-teaming
category: Prompt Engineering
difficulty: beginner
estimated_time: "1 hour"
mitre_atlas:
  tactics: [AML.TA0001]
  techniques: [AML.T0043, AML.T0051]
mitre_attack:
  tactics: [TA0009]
  techniques: [T1592]
platforms: [ai, web]
tags: [ai, prompt-leaking, gen-ai, intelligence-gathering, prompt-engineering]
tools: [chat-interfaces, intercepting-proxy]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# AI Prompt Leaking

## When to Use
- When analyzing an AI-powered system (customer support bot, coding assistant, data analyst) to uncover its proprietary internal instructions, hidden API keys, or pre-configured biases.
- To demonstrate how seemingly secure conversational agents can be tricked into revealing their foundational programming.


## Prerequisites
- Access to target AI/ML system or local model deployment for testing
- Python 3.9+ with relevant ML libraries (transformers, torch, openai)
- Understanding of LLM architecture and prompt processing pipelines
- Authorized scope and rules of engagement for AI red team testing

## Workflow

### Phase 1: Context Boundary Testing

```text
# Concept: The LLM ```

### Phase 2: Targeted Extraction Prompts

```text
# ```

### Phase 3: Translation and Obfuscation Exploitation

```text
# ```

### Phase 4: Summarization Attacks

```text
# ```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Formulate Prompt ] --> B{Prompt Leaked ]}
    B -->|Yes| C[Document System ]
    B -->|No| D[Refine ]
    C --> E[Exploit Further ]
```

## 🔵 Blue Team Detection & Defense
- **Strict Delimiters**: **Heuristic Output Filtering**: Key Concepts
| Concept | Description |
|---------|-------------|
## Output Format
```
Ai Prompt Leaking — Assessment Report
============================================================
Target: [Target identifier]
Assessor: [Operator name]
Date: [Assessment date]
Scope: [Authorized scope]
MITRE ATT&CK: [Relevant technique IDs]

Findings Summary:
  [Finding 1]: [Severity] — [Brief description]
  [Finding 2]: [Severity] — [Brief description]

Detailed Results:
  Phase 1: [Phase name]
    - Result: [Outcome]
    - Evidence: [Screenshot/log reference]
    - Impact: [Business impact assessment]

  Phase 2: [Phase name]
    - Result: [Outcome]
    - Evidence: [Screenshot/log reference]
    - Impact: [Business impact assessment]

Risk Rating: [Critical/High/Medium/Low/Informational]
Recommendations:
  1. [Immediate remediation step]
  2. [Long-term hardening measure]
  3. [Monitoring/detection improvement]
```


## 📚 Shared Resources
> For cross-cutting methodology applicable to all vulnerability classes, see:
> - [`_shared/references/elite-chaining-strategy.md`](../_shared/references/elite-chaining-strategy.md) — Exploit chaining methodology and high-payout chain patterns
> - [`_shared/references/elite-report-writing.md`](../_shared/references/elite-report-writing.md) — HackerOne-optimized report writing, CWE quick reference
> - [`_shared/references/real-world-bounties.md`](../_shared/references/real-world-bounties.md) — Verified disclosed bounties by vulnerability class

## References
- Learn Prompting: [Prompt Leaking](https://learnprompting.org/docs/prompt_hacking/leaking)
