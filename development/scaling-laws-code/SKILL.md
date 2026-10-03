---
name: scaling-laws-code
title: "Scaling Laws for Code: Every Programming Language Matters"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.13472
keywords: [scaling-laws, multilingual-code, pre-training, allocation-strategy]
description: "Establish language-specific scaling laws for multilingual code pre-training across 7 programming languages (0.2B-14B models, 1T tokens). Show interpreted languages scale better than compiled, synergy gains depend on syntax similarity, and parallel pairing improves translation—enabling proportion-dependent token allocation outperforming uniform distribution."
---

## Overview

This research establishes the first comprehensive scaling law framework for multilingual code pre-training. Unlike language-agnostic approaches, the work reveals that programming languages have fundamentally different scaling characteristics and transfer behaviors. These insights enable principled token allocation strategies.

## Core Technique

The key insight is that different programming languages exhibit distinct scaling relationships and transfer properties.

**Language-Specific Scaling Laws:**
Each language exhibits power-law relationships with distinct exponents.

```python
# Scaling law analysis per programming language
import numpy as np

class LanguageScalingLaws:
    def __init__(self):
        self.languages = ['python', 'java', 'javascript', 'c', 'c++', 'rust', 'go']
        self.scaling_laws = {}

    def fit_scaling_law(self, language, model_sizes, perplexities):
        """
        Fit power law: L = a * (N + D)^(-b)
        where N = model size, D = data size, L = loss
        """
        # Log-linear regression
        log_sizes = np.log(model_sizes)
        log_losses = np.log(perplexities)

        coefficients = np.polyfit(log_sizes, log_losses, deg=1)
        # coefficients: [exponent_b, intercept_a]

        self.scaling_laws[language] = {
            'exponent': abs(coefficients[0]),  # b term
            'category': self.categorize_language(language)
        }

        return self.scaling_laws[language]

    def categorize_language(self, language):
        """
        Interpreted vs compiled affects scaling behavior.
        """
        if language in ['python', 'javascript']:
            return 'interpreted'
        else:
            return 'compiled'

    def analyze_scaling_differences(self):
        """
        Interpreted languages scale better with model/data increase
        than compiled languages.
        """
        interpreted = [
            law for lang, law in self.scaling_laws.items()
            if law['category'] == 'interpreted'
        ]
        compiled = [
            law for lang, law in self.scaling_laws.items()
            if law['category'] == 'compiled'
        ]

        print(f"Interpreted avg exponent: {np.mean([l['exponent'] for l in interpreted]):.3f}")
        print(f"Compiled avg exponent: {np.mean([l['exponent'] for l in compiled]):.3f}")
        # Typical result: Interpreted benefit more from scale
```

**Synergy Gain Matrix:**
Cross-lingual transfer depends on language similarity.

```python
def compute_synergy_gains(language_pairs, training_results):
    """
    Measure cross-lingual transfer effects.
    Syntactically similar languages show positive transfer.
    """
    synergy_matrix = {}

    for lang1, lang2 in language_pairs:
        # Joint training performance
        joint_performance = training_results[(lang1, lang2)]

        # Individual training performance
        individual_performance = (
            training_results[lang1] + training_results[lang2]
        ) / 2

        # Synergy = improvement from joint training
        synergy = joint_performance - individual_performance

        # Syntactic similarity metric
        similarity = compute_syntactic_similarity(lang1, lang2)

        synergy_matrix[(lang1, lang2)] = {
            'synergy_gain': synergy,
            'syntax_similarity': similarity
        }

    return synergy_matrix

def analyze_transfer_patterns(synergy_matrix):
    """
    Similar languages (Java-C#) show positive transfer.
    Dissimilar languages show minimal or negative transfer.
    """
    positive_synergies = [
        (pair, data['synergy_gain']) for pair, data in synergy_matrix.items()
        if data['synergy_gain'] > 0
    ]
    print("Positive transfer pairs (high syntax similarity):")
    for pair, gain in positive_synergies:
        print(f"  {pair}: +{gain:.3f}")
```

**Parallel Pairing Strategy:**
Concatenating code with translations improves multilingual translation.

```python
def parallel_pairing_training(code_datasets):
    """
    For each code snippet, include translation to related language.
    Improves multilingual translation with favorable scaling.
    """
    paired_data = []

    for code_sample in code_datasets['python']:
        # Original code
        original = code_sample

        # Translation to Java (similar-enough for transfer)
        translated = translate_code(code_sample, 'python', 'java')

        # Pair them in training data
        paired_data.append({
            'source': original,
            'translation': translated,
            'source_lang': 'python',
            'target_lang': 'java'
        })

    return paired_data
```

**Proportion-Dependent Allocation Strategy:**
Optimal token allocation balances utility and saturation properties.

```python
def optimal_token_allocation(languages, total_tokens, scaling_laws):
    """
    Allocate tokens based on:
    1. Scaling utility (languages benefiting more get more)
    2. Saturation rate (fast-saturating languages get less)
    3. Cross-lingual synergies
    """
    allocations = {}

    # Compute utility weight per language
    utility_weights = {}
    for lang in languages:
        law = scaling_laws[lang]

        # High exponent = benefits more from scale
        scaling_benefit = law['exponent']

        # Saturation rate (compiled langs saturate faster)
        if law['category'] == 'compiled':
            saturation_penalty = 0.7  # Reduce allocation
        else:
            saturation_penalty = 1.0  # Full allocation

        utility_weights[lang] = scaling_benefit * saturation_penalty

    # Normalize weights to sum to total_tokens
    total_weight = sum(utility_weights.values())
    for lang in languages:
        allocations[lang] = int(
            (utility_weights[lang] / total_weight) * total_tokens
        )

    return allocations
```

## When to Use This Technique

Use these scaling laws when:
- Pre-training on multilingual codebases
- Deciding language-specific model sizes
- Allocating computational budget across languages
- Predicting multilingual code model performance

## When NOT to Use This Technique

Avoid this approach if:
- Single-language code models (simpler approach)
- Scaling laws unavailable for your languages
- Transfer between your specific languages unpredictable
- Computational budget not constraining

## Implementation Notes

The framework requires:
- 1000+ experiments across language-size combinations
- Scaling law fitting infrastructure
- Cross-lingual transfer measurement
- Parallel pairing data generation
- Token allocation optimization

## Key Performance

- Language-specific exponents range 0.07-0.15
- Positive transfer for syntactically similar languages
- Parallel pairing improves translation with favorable scaling
- Optimized allocation outperforms uniform distribution

## References

- Language-specific power-law scaling relationships
- Interpreted vs compiled language scaling differences
- Synergy gain matrix from cross-lingual training
- Parallel pairing for translation improvement
- Proportion-dependent token allocation strategy
