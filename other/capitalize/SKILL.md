---
name: capitalize
description: "Fin de session : analyse git diff, detecte patterns reutilisables, propose TWB blocks ou chainskills workflows a extraire"
model: sonnet
allowed-tools: Bash, Read, Grep, Glob, Edit, Write, Agent, mcp__crag__session_save, mcp__crag__kv_set, mcp__memory__add_observations
---

# /capitalize — Capitalisation de session

Analyse le travail effectue pendant la session et propose des extractions reutilisables.
A lancer en fin de session ou quand un pattern se repete.

## Etape 1 — Collecter les changements

```bash
# Fichiers modifies/crees dans la session
git diff --name-status HEAD~5..HEAD 2>/dev/null || git diff --name-status --cached
git diff --stat HEAD~5..HEAD 2>/dev/null || git diff --stat --cached
git log --oneline -10
```

Lire les fichiers modifies pour comprendre le travail effectue.

## Etape 2 — Detecter les patterns extractibles

Chercher dans les changements :

### A. Nouveau boilerplate repetable
- Nouveau adapter ? → `twb create adapter <name>`
- Nouveau schema Zod ? → `twb create schema <name>`
- Nouvelle config (tsconfig, vitest, docker) ? → `twb create config <name>`
- Nouveau workflow ? → `twb create workflow <name>`
- Nouveau skill Claude Code ? → copier dans chainskills skills
- Nouveau hook ? → `twb create hook <name>`

### B. Script deterministe remplacant du LLM
- Commande repetee 3+ fois ? → script bash dans `.claude/scripts/`
- Validation manuelle repetee ? → hook pre/post commit
- Pattern de recherche recurrent ? → alias ou script

### C. Workflow agentique reutilisable
- Sequence de tool calls qui se repete ? → `.workflow.md`
- Pattern agent specifique ? → agent definition reutilisable
- Pipeline de verifications ? → workflow de validation

## Etape 3 — Proposer les extractions

Pour chaque pattern detecte, presenter :

```markdown
## Propositions de capitalisation

### 1. [type] nom-du-pattern
- **Source** : fichier(s) modifie(s)
- **Commande** : `twb create <type> <name>` ou action manuelle
- **Variables** : parametres a abstraire
- **Economie estimee** : X tokens/session
- **Action** : [creer maintenant] / [noter pour plus tard]
```

Demander validation pour chaque proposition avant de creer.

## Etape 4 — Sauvegarder le resume de session

Utiliser `mcp__crag__session_save` pour persister le resume :

```json
{
  "project": "<projet courant>",
  "summary": "<resume en 2-3 phrases>",
  "files_touched": ["<liste fichiers>"],
  "decisions": ["<decisions prises>"],
  "errors": ["<erreurs rencontrees>"],
  "patterns_used": ["<patterns/blocks utilises>"]
}
```

## Etape 5 — Mettre a jour le graph

Si de nouvelles relations ou observations ont ete decouvertes pendant la session,
les ajouter au graph memory via `mcp__memory__add_observations`.

## Regles

- Ne JAMAIS creer un block TWB sans validation utilisateur
- Privilegier l'extraction de scripts deterministes sur les workflows LLM
- Un pattern doit apparaitre >= 2 fois pour justifier l'extraction
- Toujours verifier `twb search <keyword>` avant de creer un nouveau block
- Sauvegarder le resume de session MEME si aucun pattern n'est extrait
