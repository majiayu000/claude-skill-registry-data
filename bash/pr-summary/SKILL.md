---
name: pr-summary
description: Summarize the current GitHub pull request using live PR context from opt-in !`command` dynamic context placeholders or the fallback collector script.
---

# PR Summary

Use this skill to summarize the current GitHub pull request. Prefer the dynamic context already present in the conversation under `Dynamic context for $pr-summary`.

## Pull Request Context

- PR metadata: !`gh pr view --json number,url,title,state,isDraft,author,baseRefName,headRefName,reviewDecision,mergeable,additions,deletions,changedFiles,statusCheckRollup`
- Changed files: !`gh pr diff --name-only`
- PR comments: !`gh pr view --comments`
- PR diff: !`gh pr diff`

If no dynamic context is present, run:

```bash
python3 <skill-dir>/scripts/collect_pr_context.py --format markdown
```

Resolve `<skill-dir>` to the directory containing this `SKILL.md`.

## Output

Return a concise PR summary with:

- Purpose and user-visible behavior
- Main changed areas
- Review risks or likely regressions
- Test and CI status when available
- Suggested follow-ups only when they are concrete

Do not paste the full diff. Quote only small snippets when needed to explain a risk.
