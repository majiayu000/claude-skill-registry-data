---
name: sync-pt-parity
description: Sync files (skills, packages/core/patterns, agents, specs) from EN canonical repo to PT mirror, inserting "Tradução pendente" blockquote after YAML frontmatter, then open PR.
triggers:
  - "sync pt parity"
  - "mirror en to pt"
  - "update pt-br repo"
  - "sync portuguese"
---

# sync-pt-parity

Automate the EN→PT file parity workflow. Given a canonical EN repo and a PT mirror, copy specified files and inject a translation-pending blockquote **after** the YAML frontmatter closing `---` (critical: NOT before).

## When to run

- After shipping new skills, patterns, agents, or specs in the EN canonical repo (`ai-dev-toolkit`).
- When multiple EN files need to be mirrored to the PT repo (`ai-dev-toolkit-pt-br`).
- Before syncing, ensure the EN files have YAML frontmatter with `name:`, `description:`, `triggers:` (if applicable).

## Invocation

Ask: "Sync these files from EN to PT: skills/X.md, packages/core/patterns/Y.md, agents/Z/AGENT.md"

The skill will:

1. Identify each file in the EN canonical repo.
2. Copy to the corresponding path in the PT mirror.
3. **Parse the frontmatter** — extract the closing `---` line number.
4. **Insert after frontmatter**:
   ```markdown
   > **Tradução pendente** — conteúdo em inglês, aguardando tradução para pt-BR. Contribute to [ai-dev-toolkit-pt-br](https://github.com/LucasSantana-Dev/ai-dev-toolkit-pt-br/issues).
   ```
5. Create a feature branch (`feature/skill-sync-pt-parity`) in both EN and PT repos.
6. Commit the changes in both repos.
7. Open PRs on both repos and link them.

## Critical: Blockquote Placement

**ALWAYS** place the "Tradução pendente" blockquote **AFTER** the closing `---` of the YAML frontmatter.

### Why

The kit validator (`packages/core/kit/scripts/validate.sh`) parses frontmatter before rendering markdown. A blockquote **before** the frontmatter breaks the YAML parser and fails validation. The rule:

```
Before frontmatter → INVALID (kit validator fails)
After closing --- → VALID (validator passes, content renders)
```

### What NOT to do

❌ **WRONG** (causes validator failure — see [commit 5c899ef](https://github.com/LucasSantana-Dev/ai-dev-toolkit-pt-br/commit/5c899ef)):

```markdown
> **Tradução pendente** — conteúdo em inglês...

---
name: example
description: ...
---
```

✅ **CORRECT** (validator passes):

```markdown
---
name: example
description: ...
---

> **Tradução pendente** — conteúdo em inglês...
```

## Example Invocation

```
Sync EN → PT for wave 2 patterns:
- packages/core/patterns/cost-aware-routing.md
- packages/core/patterns/local-first-agents.md
- packages/core/patterns/reasoning-model-prompting.md

Source: /Volumes/External\ HD/Desenvolvimento/ai-dev-toolkit
Target: /Volumes/External\ HD/Desenvolvimento/ai-dev-toolkit-pt-br
```

The skill creates:

1. **pt-br repo** — 3 new files with blockquote + frontmatter structure, PR ready.
2. **EN repo** — metadata commit (optional, if file list needs documentation).

## Optional: Helper Script

Use the bundled `sync.sh` script to automate file copy + blockquote insertion:

```bash
bash ~/.claude/skills/sync-pt-parity/sync.sh \
  --source /Volumes/External\ HD/Desenvolvimento/ai-dev-toolkit \
  --target /Volumes/External\ HD/Desenvolvimento/ai-dev-toolkit-pt-br \
  --files "packages/core/patterns/cost-aware-routing.md,packages/core/patterns/local-first-agents.md"
```

The script will:
- Copy each file.
- Find the frontmatter closing `---`.
- Insert blockquote after it.
- Stage for commit.

## References

- Bilingual parity skill: `bilingual-readme-sync`
- PT repo: [ai-dev-toolkit-pt-br](https://github.com/LucasSantana-Dev/ai-dev-toolkit-pt-br)
- Recent syncs: PR #10, #11 on pt-br repo (PRs #69–#70 on EN repo)
