---
name: slipstream-aliases
description: Suggested shell aliases based on usage patterns
---

## Detected Patterns
- (Repeated command sequences will be noted here)

## Suggested Aliases
- (Alias suggestions will be added as patterns emerge)

## Example
When a pattern like `git add -A && git commit -m "..." && git push` is detected,
the learner will suggest:
```zsh
alias gcp='git add -A && git commit -m "$1" && git push'
```
