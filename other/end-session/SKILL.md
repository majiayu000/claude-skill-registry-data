---
name: end-session
description: "Cloture propre de session : resume, capitalisation, sauvegarde CRAG + graph memory"
allowed-tools: Bash, Read, Grep, Glob, mcp__crag__session_save, mcp__crag__kv_set, mcp__memory__add_observations
---

# /end-session — Cloture de session

Resume rapide + sauvegarde automatique. Plus leger que /capitalize (pas d'extraction).

## 1. Collecter le contexte

```bash
git diff --stat HEAD~5..HEAD 2>/dev/null || echo "pas de commits recents"
git log --oneline -5 2>/dev/null
```

## 2. Generer le resume

Format court :
- **Projet** : nom du projet
- **Travail effectue** : 2-3 bullets
- **Decisions prises** : choix architecturaux, techniques
- **Erreurs rencontrees** : bugs, blocages, solutions
- **Patterns utilises** : TWB blocks, skills, workflows

## 3. Sauvegarder dans CRAG

```
mcp__crag__session_save({
  project: "...",
  summary: "...",
  files_touched: [...],
  decisions: [...],
  errors: [...],
  patterns_used: [...]
})
```

## 4. Mettre a jour le graph memory

Si nouvelles observations sur un projet/convention/outil :
```
mcp__memory__add_observations([...])
```

## 5. Collecter les metriques de session

```bash
bash ~/.claude/scripts/post-session.sh
```

Stocker le resume dans KV :
```
mcp__crag__kv_set({ key: "metrics:last-session", value: "<output du script>" })
```

## 6. Proposer /capitalize si pertinent

Si le travail a genere du boilerplate repetable, suggerer de lancer `/capitalize`
pour extraire des blocks TWB.
