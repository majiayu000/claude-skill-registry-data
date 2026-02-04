---
name: Priority Detector
description: Analyse les lifelogs Limitless et extrait engagements, demandes, deadlines pour Christian Boulet
version: 1.0.0
author: Christian Boulet
created: 2024-10-23
---

# Priority Detector Skill

## 🎯 Objectif

Analyser automatiquement les conversations et notes vocales enregistrées dans Limitless pour identifier les priorités d'action de Christian Boulet, fractional CTO chez Boulet Stratégies TI.

## 📋 Fonctionnalités

Le skill détecte trois types de priorités :

### 1. ✅ Engagements pris
- Actions que Christian a promis de réaliser
- Phrases clés : "je vais...", "je te reviens avec...", "je m'engage à..."
- Promesses faites à des clients/prospects
- Livrables mentionnés

**Exemple :**
> "Je vais te préparer une proposition pour le rôle de Fractional CTO d'ici vendredi."

### 2. 📥 Demandes reçues
- Requêtes nécessitant une action de Christian
- Questions directes : "Peux-tu...", "J'aurais besoin de...", "Pourrais-tu..."
- Informations demandées par des clients
- Documents à fournir

**Exemple :**
> "Est-ce que tu peux m'envoyer ton CV et quelques case studies ?"

### 3. ⏰ Deadlines
- Échéances temporelles explicites
- "Avant [date]", "Pour [jour]", "D'ici [deadline]"
- Dates de livraison mentionnées
- Urgences

**Exemple :**
> "Il me faudrait la documentation avant le 25 octobre."

## 🔄 Workflow

```
1. Fetch Lifelogs
   └─ Récupérer conversations depuis Limitless API
   └─ Période : aujourd'hui ou dernière semaine

2. Analyze with Claude
   └─ Envoyer transcripts à Claude Sonnet 4.5
   └─ Appliquer prompts de détection
   └─ Extraire priorités structurées

3. Create TODOs
   └─ Créer pages Notion pour chaque priorité
   └─ Inclure type, description, source, confidence

4. Format Output
   └─ Générer markdown lisible
   └─ Afficher résumé avec lien Notion
```

## 📊 Output Format

Le skill génère un rapport markdown structuré :

```markdown
## 🎯 Priorités du jour - 23 octobre 2024

### Engagements pris
- [ ] Préparer proposition Fractional CTO pour Marc Veilleux (ESI)
- [ ] Envoyer calendrier disponibilités à JF Poulin

### Demandes reçues
- [ ] FLB : documenter architecture actuelle avant départ
- [ ] Guy Tremblay : partager case studies transformation IA

### Deadlines
- [ ] Finaliser REQ Boulet Stratégies TI (deadline: 25 oct)

---
✅ 5 TODOs créés dans Notion : https://notion.so/...
```

## ⚙️ Configuration

Le skill utilise la configuration du fichier `config/config.yaml` :

```yaml
priority_detector:
  confidence_threshold: 0.8  # Seuil de confiance minimum
  max_priorities_per_day: 10 # Limite de priorités par jour
```

## 🧪 Tests de Validation

### Critères de succès MVP :
- ✅ Temps d'exécution < 30 secondes
- ✅ Précision > 90% (pas de faux positifs critiques)
- ✅ 100% des priorités détectées créées dans Notion

### Cas de test :
1. **Engagement clair** : "je vais te revenir avec ça demain"
2. **Demande implicite** : "ça serait génial si tu pouvais..."
3. **Deadline floue** : "le plus tôt possible"
4. **Conversation sans priorité** : discussion générale

## 📚 Ressources

- **Prompts** : `resources/prompt_templates.json`
- **Scripts** : `scripts/analyze.py`, `scripts/format_output.py`
- **Docs** : Blueprint.md (Section 4 - Workflow MVP)

## 🚀 Usage

Via CLI :
```bash
# Priorités du jour
nexus priorities today

# Priorités de la semaine
nexus priorities week

# Mode dry-run (test sans créer dans Notion)
nexus priorities today --dry-run
```

## 🔍 Debugging

Logs détaillés disponibles dans `nexus.log` :
- Nombre de lifelogs récupérés
- Temps d'analyse Claude
- Priorités extraites avec confidence scores
- Succès/échecs de création Notion

## 📈 Métriques

Le skill track :
- Nombre de lifelogs analysés
- Priorités par type (engagements/demandes/deadlines)
- Confidence scores moyens
- Temps d'exécution
- Taux de succès Notion

---

**Version :** 1.0.0
**Dernière mise à jour :** 23 octobre 2024
