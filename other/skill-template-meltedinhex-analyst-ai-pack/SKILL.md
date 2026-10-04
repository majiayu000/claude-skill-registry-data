---
name: skill-template
description: 'One to three sentences describing what this skill does and the conditions
  under which an agent should activate it. Start with a verb, name the tools and artifacts
  involved, and end with the trigger phrasing (e.g. "Activates for requests involving ...").'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - tag-one
  - tag-two
  - tag-three
  - tag-four
  - tag-five
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T0000
d3fend:
  - D3-XXX
car:
  - CAR-0000-00-000
references:
  - 'Source title — https://example.com/primary-source'
---

# Skill Title

> Replace every bracketed placeholder. Delete this quote block and the `Safety & Handling`
> section if the skill does not touch live malware samples. Keep section order.

## When to Use

- [Concrete trigger: a situation where this skill is the right tool]
- [Another trigger]
- [Another trigger]

**Do not use** for [explicit out-of-scope cases]; instead reach for [the correct skill].

## Prerequisites

- [Tool + minimum version, with install/download pointer]
- [Lab/environment requirement]
- [Prior knowledge or input artifact required]

## Safety & Handling

*(Sample-handling skills only — delete otherwise.)*

- Work only inside an isolated analysis VM with no path to production or the internet
  unless deliberately routed through a controlled gateway.
- Store samples encrypted or in password-protected archives (password `infected`); never
  leave live samples loose on disk.
- Defang indicators (`hxxp://`, `1.2.3[.]4`) in any output that leaves the lab.
- Never execute a sample on the host or detonate outside the sandbox.

## Workflow

### Step 1: [Action]

[What to do and why.]

```bash
# Real, runnable command — not pseudocode
tool --do-the-thing sample.bin
```

### Step 2: [Action]

[Explanation.]

```python
# Original example code
```

### Step 3: [Action]

[Explanation.]

## Validation

- [How to confirm the analysis/hunt produced a correct, trustworthy result]
- [A cross-check or second method to corroborate findings]

## Pitfalls

- [Common mistake and how to avoid it]
- [Evasion trick or false-positive trap to watch for]

## References

- See [`references/api-reference.md`](references/api-reference.md) for tooling details and
  the full list of sources this skill was synthesized from.
- [Key external source — title and URL]
