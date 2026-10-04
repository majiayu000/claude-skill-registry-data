---
name: auto-skill-creator
description: |-
  Automatically creates new skills from complex problem-solving sessions. Triggers at the end of 
  multi-step tasks that required novel approaches, debugging sessions, or workflow creation.
  Use when: a task took 3+ tool calls, involved a non-obvious solution, or established a pattern 
  likely to recur. Also triggers on: "create a skill from this", "save this as a skill", 
  "this should be a skill".
---

# Auto Skill Creator

Turns complex problem-solving into reusable skills — automatically.

## When to Trigger

After completing a multi-step task, evaluate:

1. **Complexity** — Did it take 3+ tool calls or require debugging?
2. **Novelty** — Was the solution non-obvious or undocumented?
3. **Recurrence** — Will this pattern likely happen again?

If 2 of 3 are true → create a skill.

## Process

### 1. Extract the Pattern

From the completed task, identify:
- **Problem class** — what category of problem was this? (e.g., "proxy crash recovery", "WhatsApp reconnect")
- **Key steps** — the minimal sequence that solves it
- **Gotchas** — what didn't work or was misleading
- **Prerequisites** — what tools/access/knowledge is needed

### 2. Check for Duplicates

Before creating:
```bash
grep -rl "<problem-class-keywords>" skills/*/SKILL.md
```
If a similar skill exists, update it instead of creating a new one.

### 3. Create the Skill

Structure:
```
skills/<skill-name>/
├── SKILL.md          # Frontmatter + instructions
├── scripts/          # Only if deterministic code was part of the solution
└── references/       # Only if reference material is needed
```

Rules:
- `name`: lowercase, hyphenated, verb-led (e.g., `debug-litellm-proxy`, `recover-whatsapp-gateway`)
- `description`: max 1024 chars, includes what + when to use
- Body: <500 lines, imperative form, concrete steps
- Include the gotchas — what looked right but wasn't
- No README.md, no CHANGELOG.md, no auxiliary files

### 4. Register in Manifest

After creating the skill directory:
```bash
cd /path/to/workspace/skills
python3 -c "
import json, os, glob
manifest = []
for skill_dir in sorted(glob.glob('*/SKILL.md')):
    name = os.path.dirname(skill_dir)
    with open(skill_dir) as f:
        content = f.read()
    # Extract description from frontmatter
    if '---' in content:
        fm = content.split('---')[1]
        for line in fm.split('\n'):
            if line.strip().startswith('description:'):
                desc = line.split(':', 1)[1].strip().strip('\"').strip(\"'\")
                manifest.append({'name': name, 'description': desc[:200]})
                break
with open('_manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2)
"
```

### 5. Git Commit

```bash
git add skills/<skill-name>/ skills/_manifest.json
git commit -m "auto-skill: <skill-name> — <one-line description>"
git push
```

### 6. Log It

```bash
python3 tools/eval_tracker.py log proactive_action "auto-created skill: <skill-name>" 2
```

And add to daily notes:
```
[HH:MM IL] Auto-created skill <skill-name> from <task description>.
```

## Quality Gate

Before committing, verify:
- [ ] Frontmatter has `name` and `description`
- [ ] Description explains both WHAT and WHEN
- [ ] Body is <500 lines
- [ ] Steps are concrete (not "be careful" or "check things")
- [ ] Gotchas section exists if there were false leads
- [ ] No duplicate of existing skill

## Anti-Patterns

- Don't create skills for one-off tasks that won't recur
- Don't create skills that are just "read this doc"  
- Don't create skills for things the model already knows (basic git, basic Python, etc.)
- Don't create skills during time-sensitive tasks — queue it and create after

## Integration with proactive-pa

The proactive-pa skill's "Next step without asking" pattern should evaluate:
> "Did I just solve something hard? Should this be a skill?"

If yes, trigger auto-skill-creator before closing the task.
