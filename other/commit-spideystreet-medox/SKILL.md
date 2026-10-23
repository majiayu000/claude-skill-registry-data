---
name: commit
description: Create a git commit with Medox conventions (co-author, conventional type/scope). Invoke manually with /commit — do NOT trigger automatically.
disable-model-invocation: true
argument-hint: "[type(scope): message hint]"
---

# Skill: Commit

Create a git commit following the conventions defined in `.claude/rules/git.md`.

## Steps

1. `git status` + `git diff --staged` — review what will be committed
2. Stage specific files (avoid `git add .`)
3. Draft message: `<type>(<scope>): <imperative summary>`
4. Commit:
   ```bash
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <summary>

   Co-Authored-By: spidecode-bot <263227865+spicode-bot@users.noreply.github.com>
   EOF
   )"
   ```
5. `git log --oneline -1` — verify
