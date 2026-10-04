---
name: perplexitor
description: >-
  Transform vague research requests into optimized Perplexity prompts. 
  Automatically detects search intent (factual, exploratory, comparative, procedural, decisional), 
  selects appropriate mode (🔍 Standard, 🔬 Deep Research, 🎓 Academic), and generates 2-3 
  ranked prompts with different angles. Handles voice-dictated input with cleanup.
  Use when user wants to search, research, find information, compare options, or asks 
  "c'est quoi", "comment", "pourquoi", "meilleur", "vs", "tendances", "actualités".
  Not for tasks Claude can answer directly, code generation, document creation, or brainstorming sessions.
---

# Perplexitor — Générateur de Prompts Perplexity

## Overview

Perplexitor transforme une demande de recherche floue (y compris dictée vocale) en 2-3 prompts Perplexity optimisés et prêts à copier. Le skill détecte automatiquement l'intention, choisit le mode approprié, et propose des angles d'attaque complémentaires.

**Philosophie** : Plus rapide que réfléchir soi-même au prompt. Toujours produire un résultat.

## Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│              Demande de recherche détectée                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Analyse : Nettoyage + Classification + Score Clarté        │
└─────────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
┌──────────────────────┐      ┌──────────────────────┐
│  Clarté ≥ 60         │      │  Clarté < 60         │
│  → MODE EXPRESS      │      │  → MODE GUIDÉ        │
│  Output direct       │      │  P1 + Question       │
└──────────────────────┘      └──────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Output : 2-3 prompts triés par pertinence                  │
│  P1 (Hero) → P2 → P3 (optionnel)                            │
└─────────────────────────────────────────────────────────────┘
```

## Activation

**Détection automatique** sur les patterns suivants :

| Catégorie | Patterns | Confiance |
|-----------|----------|-----------|
| Explicites | "recherche", "cherche", "trouve", "infos sur" | Haute |
| Interrogatifs | "c'est quoi", "comment", "pourquoi", "qui est" | Moyenne |
| Comparatifs | "vs", "différence entre", "comparer", "meilleur" | Haute |
| Exploratoires | "parle-moi de", "état de l'art", "tendances" | Haute |
| Décisionnels | "dois-je", "faut-il", "vaut-il mieux" | Moyenne |

**Non-activation** : Si Claude peut répondre directement sans recherche ET pas de demande explicite.

## Workflow

### Étape 1 : Analyse

1. **Nettoyer** l'input (hésitations, répétitions si dictée)
2. **Classifier** le type de recherche → [taxonomy.md](references/taxonomy.md)
3. **Calculer** le score de clarté (0-100)

### Étape 2 : Mode Express ou Guidé

**Si clarté ≥ 60** → Génération directe

**Si clarté < 60** → Poser 1 question composite + générer P1 best effort

Questions disponibles → [clarification-bank.md](references/clarification-bank.md)

### Étape 3 : Génération

Pour chaque prompt, appliquer les **5 composants Perplexity** :
1. **Instruction** : Verbe d'action clair
2. **Contexte** : Situation/domaine
3. **Input** : Données spécifiques
4. **Mots-clés** : Termes techniques
5. **Format** : Structure attendue

Patterns par type → [prompt-patterns.md](references/prompt-patterns.md)

### Étape 4 : Output

```markdown
## 🔎 Perplexitor

**Demande** : [reformulation nettoyée]
**Type** : [Type détecté]
**Clarté** : [Score]/100

---

### 🎯 P1 — [Angle principal] [🔍|🔬|🎓]

```
[Prompt optimisé - HERO, immédiatement copiable]

Termine ta réponse par une section "📎 Sources NotebookLM" 
listant toutes les URLs sources utilisées, une par ligne, 
sans numérotation ni markdown.
```

⏱️ ~[temps] | 📊 [nb sources]

---

### P2 — [Angle alternatif] [🔍|🔬|🎓]

```
[Prompt optimisé]

Termine ta réponse par une section "📎 Sources NotebookLM" 
listant toutes les URLs sources utilisées, une par ligne, 
sans numérotation ni markdown.
```

⏱️ ~[temps] | 📊 [nb sources]

---

### P3 — [Angle complémentaire] [🔍|🔬|🎓] *(si pertinent)*

```
[Prompt optimisé]

Termine ta réponse par une section "📎 Sources NotebookLM" 
listant toutes les URLs sources utilisées, une par ligne, 
sans numérotation ni markdown.
```

⏱️ ~[temps] | 📊 [nb sources]

---

**💡 Pourquoi ces choix ?**
- P1 : [justification]
- P2 : [justification]
- P3 : [justification]

**🔄 Pour aller plus loin**
- "[suggestion 1]"
- "[suggestion 2]"
- "[suggestion 3]"
```

## Modes Perplexity

| Mode | Icône | Temps | Sources | Quand l'utiliser |
|------|-------|-------|---------|------------------|
| Standard | 🔍 | 30-60s | 5-10 | Question factuelle, procédurale |
| Deep Research | 🔬 | 3-5min | 20-30 | Exploratoire, comparative, décisionnelle |
| Academic | 🎓 | 2-4min | 10-20 | Sources peer-reviewed requises |

## Critical Rules

1. **Toujours générer P1** même en mode Guidé (best effort)
2. **Maximum 1 question** de clarification, jamais d'interrogatoire
3. **P1 = Hero** : Le plus visible, immédiatement copiable
4. **5 composants systématiques** sur chaque prompt
5. **Enrichir automatiquement** : temporalité, critères, format
6. **Neutre** : Pas d'enrichissement basé sur le profil utilisateur
7. **Prompts en français** : Toujours générer les prompts Perplexity en français
8. **Instruction NotebookLM** : Chaque prompt doit se terminer par l'instruction de lister toutes les URLs sources

## Examples

### Exemple Express (Clarté 78/100)

**Input** : "Compare React et Vue pour un gros projet e-commerce"

**Output** : Voir [prompt-patterns.md](references/prompt-patterns.md#exemple-comparative)

### Exemple Guidé (Clarté 35/100)

**Input** : "cherche moi des trucs sur les tests"

**Output** :
```markdown
## 🔎 Perplexitor

**Demande** : Recherche sur les tests (domaine non précisé)
**Type** : Exploratoire (incertain)
**Clarté** : 35/100

---

### 🎯 P1 — Best effort (tests logiciels) 🔬 Deep Research

```
État de l'art des pratiques de tests logiciels en 2025.
Types de tests (unitaires, intégration, E2E, performance), 
outils populaires, tendances (tests assistés par IA, shift-left).
Focus : développement web et applications.
Sources récentes (2024-2025) en français et anglais.

Termine ta réponse par une section "📎 Sources NotebookLM" 
listant toutes les URLs sources utilisées, une par ligne, 
sans numérotation ni markdown.
```

⏱️ ~3-5 min | 📊 20-30 sources

---

**❓ Pour affiner** :

Tu parles de quel type de tests ?
- **Tests logiciels** → le P1 ci-dessus est adapté
- **Tests médicaux** → je reformule
- **Tests A/B / UX** → je reformule

Tape `go` pour continuer avec mon interprétation.
```

## Knowledge Base

- [Taxonomy](references/taxonomy.md) — 8 types de recherche avec indicateurs
- [Prompt Patterns](references/prompt-patterns.md) — Patterns de génération par type
- [Clarification Bank](references/clarification-bank.md) — Questions contextuelles

## Limitations

Ce skill ne fait PAS :
- Répondre directement aux questions (il génère des prompts)
- Exécuter les recherches Perplexity
- Enrichir avec le contexte utilisateur
- Gérer les sessions de brainstorming (→ utiliser brainstormer)
- Fonctionner avec des commandes (100% dialogue naturel)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2025-02-05 | Added NotebookLM sources instruction to all generated prompts |
| 1.0.0 | 2025-01-23 | Initial release |

## Current: v1.1.0

## Owner

- **Author**: Édouard
- **Contact**: Via Claude.ai
