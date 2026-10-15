---
name: galley
description: >-
  POINTEUR vers le skill `workstation` (absorbe Galley). Utilise-le pour toute revue
  d'artefact HTML : « Galley », « revue HTML », « épreuve », .html annoté, outils MCP
  html_review_*, CLI `bun run review`.
---

# Galley — absorbé par le skill unifié `workstation`

Ce skill est un **pointeur** : la doctrine Galley n'est plus maintenue ici.
Elle vit dans le skill unifié `workstation`, versionné dans le repo
workstation et symlinké au scope user des deux runtimes :

- **Source de vérité** : `~/Desktop/my-projets/workstation/.claude/skills/workstation/`.
- **Côté Claude Code** : `~/.claude/skills/workstation/SKILL.md` (symlink).
- **Côté Codex** : `~/.agents/skills/workstation/SKILL.md` (symlink).

## Où lire la doctrine

- Boucle opératoire courte : `workstation/.claude/skills/workstation/references/galley.md`.
- Protocole canonique complet : `~/Desktop/my-projets/workstation/docs/html-review-protocole.md`.
- Conception/invariants : `~/Desktop/my-projets/workstation/docs/html-review.md`.

Rappels non négociables (détaillés dans la source) : ne jamais éditer le bloc
`ws-review-state` à la main ; passer par `html_review_*` (MCP) ou
`bun run review` (CLI, cwd = repo workstation) ; après tout
`html_review_register`, finir par `http://localhost:5179/html-review/<docId>`
(prod = 5179, jamais 5173).
