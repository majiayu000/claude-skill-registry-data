---
name: post-compact-context-reload
description: Full context reload. Use after /clear, after compaction, or at session start. Loads conversation history, indexes docs, maps code, scans configs, checks git. Gets you immediately helpful.
allowed-tools: Bash, Read, Grep, Glob
---

# Context Reload

**The master command for getting up to speed.**

Use after:
- `/clear` command
- Context compaction
- Session start
- Anytime context feels thin

## The Reload Sequence

Execute in order. Each builds on the previous.

---

### 1. CONVERSATION HISTORY (Who was I? What was I doing?)

```bash
cd ~/.claude/services
python3 conversation-search.py --list-sessions | head -5
```

Then search for the current project:

```bash
python3 conversation-search.py "PROJECT_NAME" --max 3 --full
```

**Capture:** Last task, pending items, user preferences.

---

### 2. DOCUMENTATION INDEX (What should I know?)

```bash
find . -name "*.md" -type f -not -path "*/.git/*" -not -path "*/node_modules/*" | xargs grep -n "^# " 2>/dev/null | head -30
```

**Capture:** Doc structure, key files, where to dig deeper.

---

### 3. CODEBASE INDEX (How does it work?)

```bash
# Entry points
rg "if __name__|^func main" --type py --type go -l 2>/dev/null | head -10

# Classes
rg "^class " --type py -c 2>/dev/null | head -15

# API routes (if applicable)
rg "@(app|router)\.(get|post|put|delete)" --type py -c 2>/dev/null | head -10
```

**Capture:** Entry points, core abstractions, API surface.

---

### 4. CONFIG SCAN (How is it configured?)

```bash
ls pyproject.toml package.json app.yaml cloudbuild.yaml .env* 2>/dev/null
ls .github/workflows/*.y*ml 2>/dev/null | head -5
```

**Capture:** Build system, cloud config, CI/CD, environment.

---

### 5. GIT STATE (What's in flight?)

```bash
git status --short | head -15
git branch -v | grep "^\*"
git log --oneline -5
```

**Capture:** Current branch, uncommitted work, recent direction.

---

### 6. PROJECT RULES (How should I behave?)

```bash
cat CLAUDE.md 2>/dev/null | head -50
```

**Capture:** Project-specific instructions, patterns, constraints.

---

## One-Shot Reload (Copy-Paste)

```bash
echo "=== SESSIONS ===" && cd ~/.claude/services && python3 conversation-search.py --list-sessions | head -3 && cd - > /dev/null
echo "=== DOCS ===" && find . -name "*.md" -not -path "*/.git/*" | xargs grep -n "^# " 2>/dev/null | head -15
echo "=== CODE ===" && rg "if __name__|^func main" --type py --type go -l 2>/dev/null | head -5
echo "=== CONFIGS ===" && ls pyproject.toml package.json app.yaml .env* 2>/dev/null
echo "=== GIT ===" && git status --short | head -10 && git branch -v | grep "^\*"
```

---

## After Reload

You now have:

| Know | Source |
|------|--------|
| What I was working on | Conversation history |
| How the project is organized | Doc index |
| How the code is structured | Codebase index |
| How it's configured | Config scan |
| What's in flight | Git status |
| Project-specific rules | CLAUDE.md |

**Next:** Continue previous task OR ask user what's next.

---

## License Corp Context

### Repo: lc (licensecorporation/lc)
- Entity structure: 1-LC, 2-LA, 3-LR, 4-The-Plan, Z-Orchestration
- Products in x.1, Analytics in x.2
- FedRAMP High for LR (us-east5 only)

### Repo: la (licensecorporation/la)
- B2B compliance platform
- Standard GCP regions

### Repo: lr (licensecorporation/lr)
- Government regulatory platform
- FedRAMP High - us-east5 only

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| repo-map | Complete pattern reference |
| index-docs | Doc structure (headings, mermaid, tables) |
| codebase-index | Code architecture |
| read-configs | Config discovery |
| search-history | Conversation search |
