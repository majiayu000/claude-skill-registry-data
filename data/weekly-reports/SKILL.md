---
name: weekly-reports
description: Génération et mise à jour de rapports hebdomadaires avec CFD (Cumulative Flow Diagram). Activer ce skill quand l'utilisateur parle de récapitulatif, bilan hebdomadaire, rapport de la semaine, ou CFD.
version: 1.0.0
commands:
  - report-create
  - report-update
---

# Weekly Reports Skill

Système de génération de rapports hebdomadaires pour le suivi des tâches du projet CV.

## Available Commands

### report-create

Crée un nouveau rapport hebdomadaire complet avec CFD.

```bash
report-create [--week YYYY-WNN]
```

**Fonctionnalités:**

- Collecte automatique des tâches terminées/créées de la semaine
- Génération du CFD (Cumulative Flow Diagram)
- Création du rapport markdown
- Statistiques par catégorie

Voir [workflows/report-create.md](workflows/report-create.md) pour les détails.

### report-update

Met à jour un rapport existant (données, CFD, notes).

```bash
report-update [--week YYYY-WNN]
```

**Fonctionnalités:**

- Mise à jour des données JSON
- Régénération du CFD
- Ajout de notes et observations

Voir [workflows/report-update.md](workflows/report-update.md) pour les détails.

## Architecture

```text
.claude/skills/weekly-reports/
├── SKILL.md                    # Ce fichier (Level 1)
└── workflows/                  # Instructions détaillées (Level 2)
    ├── report-create.md
    └── report-update.md

scripts/reports/                # Module Python (Level 3)
├── __init__.py
├── cfd.py                      # Génération CFD
├── weekly_report.py            # Génération rapport markdown
├── generate_cfd.py             # CLI
└── tests/                      # 34 tests

.tasks/reports/                 # Rapports générés
├── YYYY-WNN-recap.md           # Rapport markdown
├── YYYY-WNN-cfd.png            # Image CFD
└── YYYY-WNN-data.json          # Données brutes
```

## Métriques du CFD

Le Cumulative Flow Diagram permet de visualiser:

| Métrique | Lecture | Signification |
|----------|---------|---------------|
| **Throughput** | Pente de la zone verte | Vitesse de livraison (tâches/jour) |
| **WIP** | Épaisseur de la zone orange | Travail en cours |
| **Lead Time** | Distance horizontale | Temps moyen de traitement |
| **Backlog** | Hauteur de la zone bleue | Tâches restantes |

## Commandes CLI

```bash
# Générer un CFD depuis données JSON
uv run --with matplotlib --with numpy scripts/reports/generate_cfd.py \
  --data .tasks/reports/2025-W48-data.json \
  --output .tasks/reports/

# Afficher les métriques
uv run --with matplotlib --with numpy scripts/reports/generate_cfd.py \
  --data .tasks/reports/2025-W48-data.json \
  --metrics

# Mode interactif (afficher le graphique)
uv run --with matplotlib --with numpy scripts/reports/generate_cfd.py \
  --data .tasks/reports/2025-W48-data.json \
  --show
```

## Format des données JSON

```json
{
  "week": "2025-W48",
  "title": "Cumulative Flow Diagram - Semaine 48",
  "data": [
    {"date": "2025-11-24", "backlog": 29, "in_progress": 0, "done": 12, "comment": "État initial"},
    {"date": "2025-11-25", "backlog": 22, "in_progress": 0, "done": 32, "comment": "20 terminées"}
  ],
  "summary": {
    "tasks_completed": 28,
    "tasks_created": 19,
    "avg_wip": 0.5
  }
}
```

## Links

- **Reports Directory:** [.tasks/reports/](../../../.tasks/reports/)
- **Python Module:** [scripts/reports/](../../../scripts/reports/)
- **Tests:** [scripts/reports/tests/](../../../scripts/reports/tests/)

---

**Version:** 1.0.0
**Last Updated:** 2025-11-27
