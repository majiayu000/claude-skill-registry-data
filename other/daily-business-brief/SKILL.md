---
name: daily-business-brief
description: Create a daily business brief from local docs, memory, tasks, and safe web context.
risk: medium
required_tools:
  - file.list
  - file.read
  - memory.search
  - web.search
suggested_subagent: business-operator
business_domain: operations
cadence: daily
approval_required_for:
  - memory.propose
  - file.write_safe
---

# Daily Business Brief

Use this skill when the user wants a daily operating summary.

Rules:
- Summarize priorities, risks, customer signals, marketing ideas, and decisions needed.
- Keep assumptions separate from observed facts.
- Do not write durable business rules without approval.
