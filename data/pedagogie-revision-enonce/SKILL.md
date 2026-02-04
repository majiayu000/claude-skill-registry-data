---
name: pedagogie-revision-enonce
description: "Détection et analyse d'ambiguïtés dans les documents pédagogiques (énoncés de TP, consignes, grilles d'évaluation, instructions). Identifie les passages nécessitant clarification et génère un tableau de révision séquentiel. Utiliser quand l'utilisateur demande de réviser, clarifier, améliorer, identifier les ambiguïtés, ou analyser la clarté d'un document pédagogique. Formats supportés - texte, DOCX, PDF, MD, PPTX, images avec texte. Ne PAS utiliser pour révision linguistique OQLF."
---

# Révision pédagogique - Détection d'ambiguïtés

Ce skill détecte et documente les passages ambigus dans les documents pédagogiques destinés aux étudiants.

## Workflow de révision

### Étape 1: Lecture et analyse du document

1. **Identifier le type et format du document**
   - Énoncé de TP, consignes d'évaluation, grille critériée, guide, politique, etc.
   - Format: DOCX, PDF, MD, TXT, PPTX, ou image avec texte

2. **Détecter la discipline pédagogique**
   - Analyser le vocabulaire, les concepts et le contexte
   - Identifier la discipline: Sciences, Sciences humaines, Arts, Santé, Gestion, Techniques, Informatique, ou autre
   - Cette détection permet d'adapter les exemples dans les suggestions de solutions

3. **Extraire le contenu textuel**
   - Documents texte: lire directement
   - DOCX: utiliser python-docx pour extraction
   - PDF: utiliser pdfplumber pour extraction de texte
   - PPTX: extraire texte des diapositives
   - Images: utiliser reconnaissance optique si texte présent

4. **Charger les références nécessaires**
   - Lire `references/ambiguites-pedagogiques.md` pour les 12 types d'ambiguïtés à détecter
   - Lire `references/format-sortie.md` pour le format du tableau de révision
   - Lire `references/adaptation-discipline.md` pour adapter les solutions au contexte disciplinaire

### Étape 2: Détection des ambiguïtés

Parcourir le document de façon séquentielle et identifier les ambiguïtés selon les 12 types:

1. **Références floues** - Pronoms sans antécédent clair
2. **Instructions contradictoires** - Contradictions dans le document
3. **Conditions implicites** - Conditions non spécifiées
4. **Termes non définis** - Jargon sans définition
5. **Dates/délais ambigus** - Indications temporelles imprécises
6. **Quantités floues** - Valeurs numériques vagues
7. **Critères subjectifs** - Évaluation sans indicateurs mesurables
8. **Séquences imprécises** - Étapes sans ordre clair
9. **Portée floue** - Inclus/exclu mal défini
10. **Responsabilités ambiguës** - Qui fait quoi pas clair
11. **Suppositions non vérifiées** - Contexte supposé non partagé
12. **Formats mal spécifiés** - Livrables sans spécifications

Pour chaque ambiguïté détectée:
- Noter la localisation précise (page/section/diapo)
- Extraire l'extrait problématique (contexte suffisant)
- Identifier le type d'ambiguïté
- Formuler la raison du problème
- Proposer une solution concrète

### Étape 3: Génération du tableau de révision

1. **Trier les ambiguïtés par ordre d'apparition** (séquentiel)
   - Par page/section croissante
   - Par ordre dans le texte si même page
   - ❌ Ne PAS grouper par type (cela force des sauts)

2. **Adapter les solutions à la discipline détectée**
   - Utiliser un vocabulaire et des exemples appropriés à la discipline
   - Sciences: protocoles, expériences, données
   - Sciences humaines: analyses, sources, théories
   - Arts: œuvres, démarches, créations
   - Santé: patients, soins, protocoles cliniques
   - Gestion: marchés, stratégies, analyses financières
   - Techniques: procédures, spécifications, normes
   - Informatique: code, architecture, systèmes

3. **Créer le tableau avec les colonnes obligatoires:**
   - N° (séquentiel: 1, 2, 3...)
   - Localisation (Page X, Section Y, Diapo Z)
   - Extrait (citation entre guillemets)
   - Type (utiliser termes standardisés)
   - Raison (1-2 phrases claires)
   - Solution suggérée (action concrète recommandée, adaptée à la discipline)

4. **Ajouter un résumé en haut du document:**
   - **Discipline détectée** (préciser la discipline identifiée)
   - Total d'ambiguïtés détectées
   - Répartition par type
   - Optionnel: niveau de priorité (critique/important/mineur)

5. **Format de sortie:**
   - Document court (< 5 pages): tableau Markdown simple
   - Document moyen (5-15 pages): résumé + tableau
   - Document long (> 15 pages): résumé exécutif + top problèmes + tableau complet

### Étape 4: Livraison du résultat

1. **Créer le fichier Markdown** dans `/mnt/user-data/outputs/`
   - Nom: `revision_[nom-document]_[date].md`
   
2. **Présenter au format lisible** avec:
   - Titre clair
   - Résumé des statistiques
   - Tableau complet séquentiel
   - Légende des types d'ambiguïtés

3. **Offrir export optionnel** en XLSX si l'utilisateur le demande explicitement

## Principes de détection

### Contexte pédagogique

Toujours considérer le public cible (étudiants) et se demander:
- Un étudiant qui lit ceci pour la première fois comprendrait-il clairement?
- Y a-t-il plusieurs interprétations possibles?
- Quelles questions l'étudiant pourrait-il se poser?
- Les attentes sont-elles explicites et mesurables?

### Sensibilité à l'ambiguïté

Être plus strict pour:
- Critères d'évaluation (impact direct sur la note)
- Dates limites (risque de malentendu sur remise)
- Instructions de remise (format, procédure)
- Conditions d'application (pénalités, bonus)

Être moins strict pour:
- Texte narratif ou explicatif
- Exemples illustratifs
- Contexte général du cours

### Faux positifs à éviter

Ne PAS signaler comme ambiguïté:
- Pronoms avec antécédent clair dans la phrase précédente
- Termes définis plus tôt dans le document
- Références à des ressources externes clairement identifiées
- Variations stylistiques acceptables (synonymes, paraphrases)

## Cas particuliers

### Documents multilingues
- Analyser uniquement la langue principale
- Signaler si instructions critiques seulement dans une langue

### Documents avec annexes
- Traiter les annexes comme sections séparées
- Vérifier que les références aux annexes sont claires

### Documents avec tableaux/diagrammes
- Vérifier que les éléments visuels sont référencés clairement dans le texte
- Signaler si tableaux complexes sans légende explicative

### Versions multiples d'un document
- Si plusieurs versions analysées, identifier les changements qui créent ambiguïtés
- Signaler les incohérences entre versions

## Exemple de sortie

```markdown
# Révision pédagogique - Laboratoire d'analyse chimique

## Résumé
- **Discipline détectée:** Sciences naturelles (Chimie)
- **Total d'ambiguïtés détectées:** 8
- **Distribution:**
  - Référence floue: 3
  - Date/délai ambigu: 2
  - Condition implicite: 2
  - Format mal spécifié: 1

## Tableau de révision séquentiel

| N° | Localisation | Extrait | Type | Raison | Solution suggérée |
|----|--------------|---------|------|--------|-------------------|
| 1 | Page 1 | "Vous devez le remettre avant..." | Référence floue | Le pronom "le" pourrait référer au rapport, aux calculs ou aux observations. | Remplacer par: "Vous devez remettre **le rapport de laboratoire complet** avant..." |
| 2 | Page 1 | "Deadline: vendredi prochain à minuit" | Date/délai ambigu | "Vendredi prochain" est relatif. "Minuit" peut signifier début ou fin de journée. | Spécifier: "Date limite: vendredi 15 novembre 2025 à 23h59" |
| 3 | Page 2 | "L'équipe doit produire un rapport" | Responsabilité ambiguë | Pas de précision sur la contribution individuelle ou l'évaluation. | Ajouter: "Chaque membre sera évalué selon sa contribution documentée dans le cahier de laboratoire et le rapport d'analyse." |
```

## Notes importantes

- **Ce skill ne fait PAS de révision linguistique OQLF** - il se concentre uniquement sur les ambiguïtés pédagogiques
- Le tableau est **toujours séquentiel** pour faciliter la révision sans sauts dans le document
- Les solutions suggérées sont des **pistes**, pas des corrections imposées
- L'analyse considère le **contexte pédagogique** et la perspective de l'étudiant

## Références

- `references/ambiguites-pedagogiques.md` - Guide complet des 12 types d'ambiguïtés avec exemples
- `references/format-sortie.md` - Spécifications détaillées du format de tableau de révision
- `references/adaptation-discipline.md` - Guide d'adaptation du vocabulaire et des solutions selon la discipline détectée
