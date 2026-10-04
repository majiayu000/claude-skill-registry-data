---
name: caveman-auto
description: Automatically activate token-saving caveman/cavecrew/caveman-compress patterns for any software engineering task. Use by default when the user asks to implement, fix, refactor, review, or investigate code, unless they explicitly request verbose output.
---

# Caveman Auto — Réduction automatique des tokens

## Quand s'activer

S'active automatiquement sur les tâches d'ingénierie :

- Implémenter / fixer / refactorer du code.
- Faire une review.
- Investiguer un bug.
- Toute tâche où la verbosité n'est pas le but.

Ne pas s'activer si l'utilisateur demande explicitement une explication détaillée, pédagogique, ou une documentation narrative.

## Activation automatique de caveman

Active le mode `caveman` (niveau `full` par défaut) quand l'utilisateur envoie un des signaux suivants :

- "caveman", "mode caveman", "parle comme un caverne"
- "be brief", "sois bref", "less tokens", "moins de tokens"
- "résumé", "concis", "terse", "compressed"

## Délégation cavecrew automatique

Quand une sous-tâche mécanique est déléguée, utiliser les presets cavecrew pour réduire le contexte retourné :

| Tâche | Subagent |
|-------|----------|
| Localiser du code / lister des usages | `cavecrew-investigator` |
| Edit chirurgical ≤ 2 fichiers | `cavecrew-builder` |
| Review de diff | `cavecrew-reviewer` |

N'utiliser les subagents verbeux que si l'utilisateur demande des explications longues.

## Compression mémoire

Si des fichiers mémoire (`CLAUDE.md`, `AGENTS.md`, `worklog.md`) sont détectés comme verbeux (> 500 lignes), proposer `/caveman:compress FILEPATH` avec confirmation.

## Exceptions

Désactiver caveman automatiquement pour :

- Warnings de sécurité.
- Confirmations d'actions destructrices.
- Explications pédagogiques demandées.
- Messages où l'ambiguïté créée par la compression serait dangereuse.
