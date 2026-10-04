---
name: task-manager
description: "Gérer la file de tâches autonomes d'Albert. Ajouter, lister, prioriser, planifier des tâches. Exécution autonome via heartbeat."
metadata: { "openclaw": { "emoji": "📋" } }
user-invocable: true
---

# Skill: Task Manager

## Quand utiliser cette skill

Invoquer quand l'utilisateur :
- Demande d'ajouter une tâche ("ajoute une tâche", "fais ça plus tard", "rappelle-moi de")
- Demande de lister les tâches ("liste les tâches", "qu'est-ce qui est en cours", "mes tâches")
- Demande de modifier une tâche ("priorise", "change la date", "supprime la tâche")
- Demande de planifier une action récurrente ("tous les jours à 7h", "chaque lundi", "chaque mois")
- Demande le statut d'une tâche ("où en est la tâche X")

## Fichier de référence

Toutes les tâches sont dans `TASKS.md` dans le workspace courant.

## Commandes

### Ajouter une tâche
1. Générer un ID unique (T + numéro séquentiel, ex: T001)
2. Extraire la description de la demande utilisateur
3. Déterminer la priorité (high/medium/low) — défaut: medium
4. Extraire la date due si mentionnée — sinon: pas de due
5. Extraire les tags pertinents (growth, data, product, dev, reporting, legal, intel)
6. Ajouter la ligne dans la section "Pending" de TASKS.md

Format ligne: `| T001 | medium | Description de la tâche | 2026-03-21 14:00 | growth |`

### Lister les tâches
Lire TASKS.md et formatter:
- Pending: triées par priorité (high → medium → low) puis par due date
- In Progress: avec durée depuis le début
- Recurring: avec next_run
- Completed: 7 derniers jours uniquement

### Modifier une tâche
- Changer priorité: mettre à jour la colonne Priority
- Changer due: mettre à jour la colonne Due
- Supprimer: retirer la ligne de TASKS.md
- Marquer terminée: déplacer vers "Completed" avec date + résultat

### Planifier une tâche récurrente
1. Générer un ID récurrent (R + numéro séquentiel, ex: R08)
2. Déterminer le schedule:
   - "tous les jours à Xh" → `daily HH:MM`
   - "chaque lundi" → `weekly lun HH:MM`
   - "chaque mois le X" → `monthly Xème HH:MM`
   - "en semaine à Xh" → `weekdays HH:MM`
3. Calculer le prochain next_run
4. Ajouter dans la section "Recurring"

### Exécuter une tâche (appelé par heartbeat)
1. Analyser la description de la tâche
2. Identifier les skills nécessaires (lead-pipeline, outreach-writer, etc.)
3. Exécuter la tâche en utilisant les skills appropriées
4. Si la tâche prend > 5 min → sessions_spawn
5. Mettre à jour TASKS.md avec le résultat
6. Si tâche récurrente → calculer next_run et mettre à jour

## Règles
- Ne JAMAIS exécuter de tâche qui envoie des messages/emails sans confirmation
- Ne JAMAIS supprimer de tâche sans confirmation explicite
- Toujours confirmer l'ajout d'une tâche en résumant ce qui a été ajouté
- Les tâches "high" priority qui échouent → alerte immédiate sur Telegram
