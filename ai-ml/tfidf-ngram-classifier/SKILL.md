---
name: nlp-tfidf-ngram-classifier
description: >
  High n-gram TF-IDF (3-5 grams) with sublinear TF feeding into a weighted soft-voting ensemble of traditional ML classifiers.
---
# TF-IDF N-gram Classifier

## Overview

For text classification where transformer fine-tuning is too slow or data is limited, use high-order n-gram TF-IDF (3-5 grams) with sublinear term frequency. Feed into a weighted soft-voting ensemble of MultinomialNB + SGDClassifier + LightGBM/CatBoost. This approach is fast, interpretable, and surprisingly competitive — it reached 0.96+ AUC on AI text detection.

## Quick Start

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import VotingClassifier

# Vectorize with high n-grams
vectorizer = TfidfVectorizer(
    ngram_range=(3, 5),
    sublinear_tf=True,
    strip_accents='unicode',
    lowercase=False,
    analyzer='word',
)
X_train = vectorizer.fit_transform(train_texts)
X_test = vectorizer.transform(test_texts)

# Ensemble of diverse classifiers
nb = MultinomialNB(alpha=0.02)
sgd = SGDClassifier(max_iter=8000, tol=1e-4, loss='modified_huber')

ensemble = VotingClassifier(
    estimators=[('nb', nb), ('sgd', sgd)],
    weights=[0.3, 0.7],
    voting='soft',
    n_jobs=-1,
)
ensemble.fit(X_train, y_train)
preds = ensemble.predict_proba(X_test)[:, 1]
```

## Workflow

1. Tokenize text (custom BPE or whitespace)
2. Vectorize with TF-IDF using 3-5 n-grams and sublinear TF
3. Train diverse classifiers: NB (fast, generative), SGD (discriminative), GBDT (nonlinear)
4. Combine via soft voting with tuned weights
5. Output calibrated probabilities

## Key Decisions

- **N-gram range**: (3,5) captures phrases; (1,3) for shorter texts
- **sublinear_tf=True**: log(1+tf) dampens high-frequency terms — almost always helps
- **SGD loss='modified_huber'**: Outputs proper probabilities unlike 'hinge'
- **NB alpha**: Low alpha (0.02) works better with high-dimensional sparse features

## References

- LLM - Detect AI Generated Text (Kaggle)
- Source: [0-960-phrases-are-keys](https://www.kaggle.com/code/hubert101/0-960-phrases-are-keys)
