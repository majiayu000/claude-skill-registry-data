---
name: x-format-advisor
description: Use when a user needs to choose between an X/Twitter long Post, Article or Thread for a topic or draft, or compare the practical and algorithmic implications of those formats.
---

# Choose an X format

For a new natural-language request, use `x-assistant` first when installed. If this workflow was explicitly selected, delegated with `routed_by: x-assistant`, or installed alone, execute directly; do not route back.

Use [the evidence guide](references/knowledge-guide.md), especially topic 03 and related retrieval, indexing, cold-start and unknown entries. Answer in the user's language; operate independently of the other skills.

1. Identify the content, intended reader, publishing goal, available media and confirmed format access. Use the supplied draft and context; ask only for a missing fact that would change the decision. Respect a format the user has already chosen and optimize within it.
2. Read the full format comparison and its source conditions. Use the original report's six comparison layers: **object/content identity; V8.2 representation; V5 representation; behavior/event records; examined candidate and scoring paths; visibility**. Keep V5 and V8.2 separate. Then check relevant retrieval/indexing, cold-start/age, product access and measurement conditions as additional evidence. Distinguish the code's path from the user's actual reader experience.
3. Compare a long Post, Article and Thread for this material. Explain what each can preserve, how readers encounter the key finding, how evidence/media fit, and where a reader must navigate. Separate an Article's title/body/carrier and a Thread's root/parts.
4. Give one recommendation with concrete packaging: opening or carrier introduction, where the evidence goes, first-image role, and any Thread part boundaries. State the condition that would change your recommendation. Include the strongest alternative only when useful.
5. Do not select a winner from unmatched lifetime view counts. If comparing performance, propose comparable topics, observation windows, audience/promotion context and metric scopes. Record assumptions rather than claim Article superiority or a format-specific bonus.

Measure actual complete text with `python3 scripts/inspect_draft.py --text draft.txt` when Python is available; otherwise use the measurement fallback in the evidence guide. Treat 4000/200-character code paths according to their exact scope, not as universal publishing limits. A navigation/reading benefit is an editorial reason, not evidence of an algorithm bonus.

For claims about the present algorithm, first read the dated-update procedure in [the knowledge guide](references/knowledge-guide.md). Apply relevant current updates alongside historical claims, and state the reviewed revision when it matters.
