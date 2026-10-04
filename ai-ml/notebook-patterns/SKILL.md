---
name: notebook-patterns
description: Pedagogical patterns for enriching notebooks (GameTheory model). Use when adding interpretations, structuring notebooks, or creating educational content in Jupyter notebooks.
---

# Notebook Enrichment Patterns

## Standard Header (all notebooks)

```markdown
# Series-N-Title

**Navigation** : [Index](README.md) | [<< Precedent](Series-N-1.ipynb) | [Suivant >>](Series-N+1.ipynb)

## Objectifs d'apprentissage

A la fin de ce notebook, vous saurez :
1. ...
2. ...

### Prerequis
- Python 3.10+ / .NET 9.0
- Cle API configuree (.env)

### Duree estimee : XX minutes
```

## Interpretation Pattern (after significant code output)

```markdown
### Interpretation : [Concept Name]

**Sortie obtenue** : [Brief summary of output]

| Aspect | Valeur | Signification |
|--------|--------|---------------|
| ... | ... | ... |

**Points cles** :
1. ...
2. ...

> **Note technique** : [Detail if relevant]
```

## Positioning Rules (CRITICAL)

- **Introduction cells** go BEFORE the code they introduce (future tense)
- **Interpretation cells** go AFTER the code output they analyze (past tense)
- **Transition cells** go BETWEEN sections
- **Conclusion cells** go at the END of a section or notebook

## Cell Insertion Strategy

1. Work from BOTTOM to TOP to avoid index shifting
2. Use `cell_id` (not index) for NotebookEdit insert reference
3. Verify position immediately after each insertion
4. One cell at a time - never batch inserts

## Domain-Specific Vocabulary

| Domain | Key Terms |
|--------|-----------|
| ML | accuracy, loss, epoch, overfitting, cross-validation |
| Probas/Infer | prior, posterior, distribution, inference, factor graph |
| GameTheory | Nash equilibrium, Shapley value, dominant strategy |
| SymbolicAI | satisfiability, resolution, proof, axiom, theorem |
| GenAI | prompt, tokens, embedding, fine-tuning, hallucination |
| Optimization | fitness, generation, mutation, crossover, convergence |

## Code/Markdown Ratios

| Level | Code | Markdown | Visualizations |
|-------|------|----------|----------------|
| Intro | 35-40% | 55-60% | min 3 |
| Intermediate | 45-50% | 45-50% | min 4 |
| Advanced | 55-60% | 35-40% | min 2 |

## Quality Checklist

- [ ] Navigation header present
- [ ] Learning objectives stated
- [ ] No consecutive code cells without explanation
- [ ] Every significant output has interpretation
- [ ] Summary table at end of each major section
- [ ] Conclusion with takeaways
- [ ] Progressive difficulty (simple to complex)
