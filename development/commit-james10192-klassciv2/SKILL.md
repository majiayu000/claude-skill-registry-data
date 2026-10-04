---
name: commit
description: Create a conventional commit. Use when the user asks to commit changes.
---

Create a conventional commit following these steps:

0. **Revue `/thermo-review` en sous-agent** — obligatoire avant tout commit qui
   touche du code (rule `pre-merge-checklist.md`, commandement 0). Verdict
   `BLOCK` → on corrige, on ne commite pas. Exemptions : docs seuls, config
   seule, suppressions pures, diff de moins de cinq lignes dans un seul fichier.

1. Run `git status` to see all changed files
2. Run `git diff --staged` and `git diff` to review all changes
3. Run `git log --oneline -5` to understand the project's commit style and scopes in use

4. Analyze the changes and determine:
   - **type**: feat | fix | refactor | test | docs | chore | perf | style | ci
   - **scope**: a short noun describing the area changed (e.g. etudiants, classes, lmd, lmd-ue, lmd-bulletin, lmd-notes, paiements, comptabilite, matieres, liaisons, auth, migrations, sidebar, chatbot)
   - **description**: imperative present tense, ≤ 72 chars (e.g. "add filiere liaison modal")

5. Verify commit author is set correctly in the worktree:
   ```bash
   git config user.name
   git config user.email
   ```
   If not set, configure before committing:
   ```bash
   git config user.name "James10192"
   git config user.email "djedjelipatrick@gmail.com"
   ```

6. Stage only relevant files explicitly (NEVER `git add -A` or `git add .`)
   - Never stage: `.env`, `.env.*`, secrets, build artifacts, OS files (.DS_Store, Thumbs.db)

7. **Detect issue context** (Issue Linking):
   - Check if the user mentioned an issue number in the conversation (e.g. "issue #158", "Refs #42")
   - Check if the branch name contains an issue number (e.g. `feat/158-lmd-system`)
   - Check recent conversation for epic/lot references (e.g. "Lot 3/7", "Part of #158")
   - If issue detected → add `Refs #N` in footer
   - If user says "closes"/"ferme"/"résout" → use `Closes #N`
   - If lot/phase tracking → add `Lot X/Y: description` line before issue ref
   - If no issue context → skip footer entirely (don't guess)

8. Create the commit:
```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

[optional body explaining WHY if not obvious]
[optional: bullet points for 3+ file changes]

[Lot X/Y: description — only if epic/lot context exists]
[Refs #N — only if issue context exists]
EOF
)"
```

## Examples

**Quick commit, no issue:**
```bash
git commit -m "fix(sidebar): hide LMD section when module disabled"
```

**Quick commit with issue:**
```bash
git commit -m "$(cat <<'EOF'
fix(lmd-ue): fix Select2 styling in ECUE modal

Refs #158
EOF
)"
```

**Detailed commit with lot tracking:**
```bash
git commit -m "$(cat <<'EOF'
feat(lmd): add LMDBulletinService with AQ/NAQ/APC validation

- Calculate ECUE averages from weighted evaluations
- Calculate UE averages from weighted ECUEs
- Implement AQ/NAQ/APC validation with compensation
- Add rank calculation and promo stats (min/moy/max)

Lot 3/7: Service de calcul
Refs #158
EOF
)"
```

**Closing commit (last lot of an epic):**
```bash
git commit -m "$(cat <<'EOF'
feat(lmd): add sidebar section and BTS/LMD routing

- Conditional LMD sidebar based on module.lmd.access permission
- BTS/LMD detection on student profile page

Lot 7/7: Sidebar et intégration
Closes #158
EOF
)"
```

## Ce que les hooks n'attrapent pas

`.githooks/commit-msg` et `hygiene-commits.yml` contrôlent la **forme** : signature
d'outil, message non conventionnel, `feat`/`fix` sans entrée au `CHANGELOG`. Ils ne
peuvent rien contre le **fond**. Un bon message porte deux choses — **ce qui change**
et **pourquoi**. Le *quoi* se relit dans le diff ; le *pourquoi* n'est écrit nulle
part ailleurs, et c'est lui qu'on regrette dans six mois.

Quatre défauts à refuser sur son propre message (axe 14 de `/thermo-review`) :

- **Décrire une intention au lieu du changement.** « améliore la gestion des
  paiements » ne dit ni ce qui bouge ni pourquoi.
- **Affirmer ce que le diff ne fait pas.** « corrige X » alors que X reste : c'est
  la forme la plus coûteuse, elle ferme l'enquête future.
- **`[sans-changelog]` par confort.** L'échappatoire vaut pour ce qui n'est
  réellement pas visible par un utilisateur. Sur un `feat`/`fix` qui touche `app/`
  `resources/` `routes/` `database/`, elle demande une raison écrite dans le corps.
- **`--no-verify`.** Pour le **message**, contourner ne fait que déplacer l'échec :
  `hygiene-commits.yml` rejoue les mêmes règles côté serveur. Pour les **pièges
  Blade** de `.githooks/pre-commit`, c'est autre chose — **aucun contrôle serveur ne
  les rejoue**, et `--no-verify` les laisse aller jusqu'en production. Si tu
  l'emploies, dis-le, et dis lequel des deux tu contournes.

Et ce que `git add -A` met dedans n'a pas été relu : résidus d'agent, fichier de
travail, secret. Toujours `git diff --cached` avant de figer.

## Rules

- NO "Generated with Claude Code" or "Co-Authored-By" in commits
- NO WIP commits
- Commit author: `James10192 <djedjelipatrick@gmail.com>`
- If multiple unrelated changes exist, ask the user to split into separate commits
- Always verify `git diff --staged` before committing
- ISSUE LINKING is opt-in: only when issue number is clearly in context
- NEVER fabricate or guess issue numbers

$ARGUMENTS
