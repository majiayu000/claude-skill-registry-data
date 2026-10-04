---
name: scan-patterns
description: "Scanne le codebase pour detecter du code duplique extractible en TWB blocks, scripts, ou workflows"
model: sonnet
allowed-tools: Bash, Read, Grep, Glob, Agent
---

# /scan-patterns — Detection de patterns reutilisables

Analyse statique du codebase pour trouver du code a factoriser en assets reutilisables.

## 1. Scanner les duplications de code

```bash
# Fichiers similaires par structure
find ~/projects/ -name "*.ts" -path "*/adapters/*" | head -50
# Schemas Zod repetes
grep -r "z.object" --include="*.ts" -l ~/projects/ | head -30
# Configs dupliquees
diff <(cat projet-a/tsconfig.json) <(cat projet-b/tsconfig.json)
```

## 2. Identifier les candidats

| Type | Signal de detection | Action |
|------|-------------------|--------|
| **Adapter** | Meme structure dans 2+ projets | `twb create adapter` |
| **Schema** | Meme z.object dans 2+ fichiers | `twb create schema` |
| **Config** | tsconfig/vitest/docker identiques | `twb create config` |
| **Workflow** | Meme sequence de commandes | `twb create workflow` |
| **Script** | Meme commande bash repetee | Script dans `.claude/scripts/` |
| **Skill** | Meme prompt/pattern d'agent | Skill Claude Code |

## 3. Cross-reference avec TWB existant

```bash
twb list          # Blocks existants
twb search <mot>  # Chercher si deja couvert
```

Ne proposer QUE les patterns qui n'existent pas encore dans TWB.

## 4. Rapport

```markdown
## Patterns detectes — {date}

### Nouveaux (a extraire)
1. [adapter] nom — present dans {projets} — `twb create adapter nom`
2. [schema] nom — present dans {fichiers} — `twb create schema nom`

### Deja couverts par TWB
- adapter/crawler → twb add adapter crawler
- config/vitest → twb add config vitest

### Statistiques
- Projets scannes : N
- Fichiers analyses : N
- Patterns detectes : N nouveaux, N existants
- Economie estimee : N tokens/session si extraits
```

## Regles

- Scanner TOUS les projets sous ~/projects/
- Ignorer node_modules/, .git/, dist/, build/
- Un pattern doit apparaitre dans >= 2 projets pour etre propose
- Toujours verifier TWB avant de proposer
