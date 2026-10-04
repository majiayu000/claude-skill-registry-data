---
name: skill-pruner
description: |-
  Reads invocation logs from eval_tracker and recommends which of the 50+ skills to prune
  or consolidate. Run monthly to keep the skill surface tight.
  Triggers: "audit skills", "prune skills", "which skills do I never use", "skill cleanup".
---

# Skill Pruner

Keeps the skill surface tight by recommending removals based on real usage data.

## When to use
- Monthly cadence
- Before adding a new skill (check for an existing one to extend)
- When `skill-master` routing feels slow

## Process

1. Pull 30-day invocation report:
   ```bash
   python -c "from tools.eval_tracker import skill_usage_report; import json; print(json.dumps(skill_usage_report(days=30), indent=2))"
   ```
2. Categorize skills:
   - **Hot** (>10 invocations) — keep
   - **Warm** (1–10) — keep, possibly merge with neighbors
   - **Cold** (0 invocations) — propose removal or consolidation
3. For each cold skill, check `git log skills/<name>/` to see if it's brand new (<14 days = give it more time)
4. Output: ranked recommendation list with reasoning

## Output format
- Markdown table: skill | invocations | last modified | recommendation
- One-paragraph summary
