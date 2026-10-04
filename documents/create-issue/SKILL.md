---
name: create-issue
description: Create a GitHub issue for KLASSCI with labels, scope, and epic linking. Use when starting new tracked work.
---

# Create Issue — KLASSCI

Create a well-structured GitHub issue for the KLASSCI project.

## Step 1 — Analyze context

```bash
gh issue list --state open --limit 15
gh label list --limit 30
```

Check for:
- Existing epic that this work belongs to (e.g. #158 LMD System)
- Duplicate or similar open issues
- Available labels on the repo

## Step 2 — Decide: new issue or continue existing?

| Situation | Decision | Action |
|-----------|----------|--------|
| New feature, new scope | Create new issue | → Continue to Step 3 |
| Next lot of an epic (#158 LMD, etc.) | Create child issue | → Link with `Parent: #N` |
| Critical bug during feature work | Create new issue NOW | → Label `priority:high` + `bug` |
| Minor bug in same scope | Don't create issue | → Fix in current PR, `Refs #N` in commit |
| Small improvement (< 1 hour) | Don't create issue | → Commit directly with scope |
| Unclear scope, needs discussion | Create issue as research | → Label `question` |

**Inform the user of your decision** — don't ask.

## Step 3 — Determine metadata

**Title format**: `<type>: <description>` (imperative mood)
- Types: `feat`, `fix`, `refactor`, `chore`, `perf`, `docs`

**Labels** (use what exists on the repo):
- Type: `enhancement` (feat), `bug` (fix), or custom `type:*` labels
- Priority: `priority:high`, `priority:medium`, `priority:low` (if they exist)
- Domain: `domain:lmd`, `domain:etudiants`, `domain:finance`, `domain:bulletin` (if they exist)

**Scope** (for KLASSCI context):
- `lmd` — UE, ECUE, parcours, domaines, mentions, bulletin LMD
- `etudiants` — inscriptions, profils, photos, documents
- `finance` — paiements, frais, comptabilité, relances
- `bulletin` — notes, résultats, bulletin BTS/LMD, PDF
- `classes` — classes, planification, emploi du temps
- `chatbot` — assistant IA, tools, streaming
- `sidebar` — navigation, modules, permissions

## Step 4 — Create the issue

```bash
gh issue create \
  --title "<type>: <description>" \
  --label "<label1>,<label2>" \
  --body "$(cat <<'EOF'
## Contexte
[Pourquoi ce travail est nécessaire — 1-2 phrases]

## Périmètre
- [ ] Tâche 1
- [ ] Tâche 2
- [ ] Tâche 3

## Critères d'acceptation
- [ ] [Ce qui définit "terminé"]
- [ ] Testé sur presentation.klassci.com
- [ ] Pas de régression sur esbtp-abidjan

## Liens
- Parent: #N (si epic)
- Related: #M (si lié)

## Impact tenants
- [ ] Zero modification du système BTS existant
- [ ] Compatible multi-tenant (pas de données hardcodées)
EOF
)"
```

## Step 5 — Output

```
Issue #<N> créée: <title>

Prochaines étapes:
  → Travailler dessus: /worktree-start <N>
  → Ou commit direct: Refs #<N> dans les messages de commit
  → Epic parent: #<P> (si applicable)
```

## Rules

- NO INTERACTION: Analyze and create — don't ask the user to fill in details
- TITLE: Imperative mood, French or English matching the conversation language
- LABELS: Only use labels that EXIST on the repo (check Step 1 output)
- EPIC LINKING: Always check open issues for a related parent before creating standalone
- TASK LIST: 2-5 checkboxes in Périmètre to track progress
- TENANT IMPACT: Always include the "Impact tenants" section for KLASSCI

$ARGUMENTS
