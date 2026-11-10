---
name: x-explain
description: Use when a user asks a factual or practical question about X/Twitter posting, recommendations, ranking weights, reach, reading, media, links, labels, frequency or Articles, without requesting a draft review or account inspection.
---

# Explain X

For a new natural-language request, use `x-assistant` first when installed. If this workflow was explicitly selected, delegated with `routed_by: x-assistant`, or installed alone, execute directly; do not route back.

Answer the question in the user's language. Use [the evidence guide](references/knowledge-guide.md) to retrieve all relevant English entries, their conditions, original sources and unresolved questions. This specialist works independently; the router is optional.

For claims about the present algorithm, first read the dated-update procedure in [the knowledge guide](references/knowledge-guide.md). Apply relevant current updates alongside historical claims, and state the reviewed revision when it matters.

## Procedure

1. Identify the actual decision or mechanism. Reuse context. A general question needs no draft, account URL or analytics export.
2. Read the relevant topic catalogs and full claims. For cross-topic questions combine their evidence; search rank does not determine truth or completeness.
3. Give the direct answer first, followed by what the user should do and why. Keep known facts, observations and recommendations distinguishable. Cite the original supporting URLs beside claims.
4. Preserve numerical conditions and the processing stage. For questions such as daily frequency, explain what the code does count and offer a feasible publishing or observation approach without inventing a daily optimum.
5. For unresolved claims explain the known portion, missing evidence, implications and practical next step. If the question is about current deployment or beyond the corpus, consult current primary sources when available and label new research.

## Response example

For “Should I use an Article or a long Post?”, explain the supported differences and relevant limits. If the user wants a decision for their actual draft, apply the format-selection workflow when available; otherwise perform that comparison from topic 03 without requiring another installation.

## Check before answering

The answer addresses the user's decision, provides a usable action and real source links, identifies snapshot versus current evidence, and does not substitute a generic disclaimer for an explanation. Do not publish, modify the corpus automatically, or silently start an account audit.
