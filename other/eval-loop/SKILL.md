---
name: eval-loop
description: Use this after a task fails or produces wrong output. Documents the failure in growth-os/eval/corrections.md so future agents don't repeat it. Three-part format—what went wrong, root cause, fix. Terse bullet points, not essays.
---

# Eval Loop

When a task fails, document it in `growth-os/eval/corrections.md` so the next agent doesn't repeat the mistake.

## When to use

- Outreach message bounced or got negative reply
- Copy failed commodity-gate after multiple rewrites
- Agent hallucinated customer data
- Wrong pricing, wrong brand voice, wrong exclude list
- Any task that failed and might be repeated

## Format for corrections.md

Three-part terse bullet format:

```markdown
## [Date] [Task description]

**What went wrong**: [one sentence, specific outcome]

**Root cause**: [why it failed—missing context, wrong assumption, unclear instruction]

**Fix**: [what to do differently—new check, new source, new gate]
```

## Example

```markdown
## 2026-09-02 Brighton cafe cold email bounced

**What went wrong**: Email to James Groom at JustAir sent as a cold pitch

**Root cause**: Agent didn't check growth-os brands/chrisschouk/excludes.md which lists James as existing contact

**Fix**: Before any chrisscho.uk outreach, read brands/chrisschouk/excludes.md and brands/chrisschouk/contacts.md
```

## Writing style

- Terse bullet points
- Specific outcome, not generic description
- Root cause must be actionable (not "AI made a mistake")
- Fix must be a concrete step (not "be more careful")
- UK spelling
- No AI fluff

## Where corrections.md lives

`growth-os/eval/corrections.md` in the private growth-os repo.

If growth-os isn't cloned, note the correction and tell Chris to add it manually.

## Related

- growth-os-read: how to read marketing memory
- commodity-gate: quality gate before publishing
