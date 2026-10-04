---
name: plan-and-confirm
description: Explore the codebase, present a clear implementation plan, and wait for explicit user approval before writing any code. Use for any non-trivial change (new feature, bug fix, refactor). Rule #1 — never code without OKAY.
---

# Plan & Confirm

## Phase 1 — Explore (read only, no modifications)

Before writing any plan, explore the relevant files:

1. Read all files directly related to the task
2. Search for usages of affected symbols with `Grep` (function names, class names, component names)
3. Understand the project's patterns and conventions (naming, structure, validation approach)
4. Identify potential side effects: other files that import or depend on what will change

**Rule: zero file modifications in this phase.**

---

## Phase 2 — Present the plan

Structure your response exactly as follows:

### What I understood
- Describe the request with precise file:line references
- Flag any ambiguous or non-obvious points
- List all possible interpretations if more than one exists

### What I will do
- List every file to modify or create, with the reasoning for each change
- State explicitly what will NOT be changed and why
- If the change spans multiple files with ordering constraints, explain the sequence

### Risks & attention points
- Any code that could break elsewhere in the app
- Any assumption made (and why)
- Any breaking API change, DB migration, or env variable addition

---

## Phase 3 — Wait for approval

**STOP. Do not touch any file.**

Output literally:

> Please confirm with **OKAY** if the understanding and plan are correct.
> Otherwise, tell me what is wrong and I will adjust before coding.

**Absolute rule:** If the user does not say OKAY (or equivalent: "yes", "go", "ok", "c'est bon", "lance"), stay in Phase 3. Do not proceed.

---

## Phase 4 — Implement (only after OKAY)

Once OKAY is received:

1. Implement exactly as described in the approved plan — no additions, no improvements beyond scope
2. If something discovered during implementation changes the plan → **stop and re-present** before continuing
3. Summarize changes with file:line references after completion

**Never commit** unless the user explicitly asks.

---

## Phase 5 — Workflow GitHub (après implémentation)

Une fois le code implémenté et validé, suivre ce cycle complet. Chaque étape a un skill dédié :

```
/create-issue → /worktree-start → code → /commit → /create-pr → merge → /worktree-finish
      ↑                                    │                                     │
      └────────────── next issue ──────────┘                                     │
      └────────────── epic still open? ──────────────────────────────────────────┘
```

### Étape 1 — Créer ou identifier l'issue
- Si pas d'issue existante : `/create-issue` (crée avec labels, scope, lien epic)
- Si issue existe déjà : noter le numéro `#N`
- Si c'est un lot d'un epic : lier avec `Parent: #P` dans le body

### Étape 2 — Créer le worktree
- `/worktree-start <N>` → crée `../KLASSCIv2-issue-<N>` basé sur `origin/presentation`
- Si quick fix (< 30 min) : rester sur `presentation`, committer avec `Refs #N`

### Étape 3 — Coder dans le worktree
- Tous les fichiers dans `../KLASSCIv2-issue-<N>/`

### Étape 4 — Committer
- `/commit` → détecte l'issue `#N` automatiquement, ajoute `Refs #N`
- Si lot d'un epic : ajoute `Lot X/Y: description` dans le body
- Si dernier lot : utilise `Closes #N` au lieu de `Refs #N`

### Étape 5 — Créer la PR
- `/create-pr` → base `presentation`, lien issue, tableau epic si applicable
- Tester sur le serveur après deploy si applicable

### Étape 6 — Nettoyer après merge
- `/worktree-finish <N>` → supprime worktree + branches, ferme l'issue
- Vérifie si l'epic parent est encore ouvert → propose la suite

### Decision tree : nouvelle issue ou continuer ?

| Situation | Action |
|-----------|--------|
| Nouvelle feature, nouveau scope | `/create-issue` → `/worktree-start` |
| Prochain lot d'un epic existant | `/create-issue` (avec `Parent: #P`) → `/worktree-start` |
| Bug critique trouvé pendant le dev | `/create-issue` (priority:high) → `/worktree-start` |
| Bug mineur dans le même scope | Fixer dans le PR actuel, `Refs #N` dans le commit |
| Petit fix (< 30 min) | Pas de worktree, committer directement sur `presentation` |

---

## Rules

- **Never code without OKAY** — this is rule #1
- Base all analysis on files actually read — no guessing
- If the plan is rejected, re-explore if needed then present a revised plan
- A "trivial change" (typo, single string edit) does not require this workflow

$ARGUMENTS
