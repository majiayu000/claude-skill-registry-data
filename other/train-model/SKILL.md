---
name: train-model
description: Entrainer le modele ML AML
user-invocable: true
---

Utilise l'agent ml-engineer pour :

1. Telecharger le dataset Elliptic si pas present
2. Preprocessing et feature engineering (5 dimensions)
3. Entrainer XGBoost avec cross-validation 5-fold
4. Evaluer les metriques (precision, recall, F1, AUC-ROC)
5. Exporter le modele en pickle
6. Lancer les tests pytest

$ARGUMENTS
