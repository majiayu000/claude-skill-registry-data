---
name: codeburn
description: Use when you want to see token consumption by task type, model, one-shot rate, or USD cost — observability dashboard for Claude Code sessions
user-invocable: true
disable-model-invocation: true
---

# Codeburn — Token Cost Observability

Reads directly from `~/.claude/projects/` (no API keys, no wrappers) and renders a TUI dashboard showing where tokens go.

**Complementary to rtk:** rtk reduces tokens spent (efficiency); codeburn shows which tasks need optimization most (observability). Together they close the feedback loop.

## Key Commands

```bash
codeburn                          # Interactive TUI dashboard (keyboard navigation)
codeburn today                    # Today's sessions only
codeburn report -p 30days         # 30-day rolling window
codeburn report --project <name>  # Filter by project
codeburn export --format csv      # Export for further analysis
codeburn export --format json     # JSON output
```

## What It Measures

| Metric                              | Why it matters                                                |
| ----------------------------------- | ------------------------------------------------------------- |
| Tokens by task type (13 categories) | Find which work type is most expensive                        |
| One-shot rate per task type         | % tasks done in 1 API call vs retry loop                      |
| Per-model breakdown                 | Cost difference between Opus and Sonnet for your actual tasks |
| USD cost estimate                   | Real spend per session / project                              |
| Input vs output token split         | Output tokens cost 3-5× more than input                       |

## The 13 Task Categories

`refactor` · `bug-fix` · `feature` · `test` · `docs` · `review` · `debug` · `config` · `migration` · `research` · `security` · `cleanup` · `other`

## Optimization Feedback Loop

```
codeburn report → find low one-shot rate task type
  → add context/rules for that category in CLAUDE.md or claude/*.md
  → rtk reduces token output on those commands
  → re-run codeburn to verify improvement
```

**Signal:** If one-shot rate < 50% for a task type, it needs more upfront context or better rules.

## Install

```bash
npm install -g codeburn      # Global install
npx codeburn                 # One-shot without global install
```

Requires Node.js 18+.
