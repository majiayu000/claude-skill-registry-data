---
name: job-application
description: Analyse d'offres d'emploi, adéquation profil-poste, et génération de CV/lettre adaptés. Activer ce skill quand l'utilisateur parle de candidature, offre d'emploi, lettre de motivation, ou CV adapté.
version: 1.1.0
commands:
  - job-analyze
  - job-fit
  - job-cv
  - job-letter
---

# Job Application Skill

Système d'assistance au processus de candidature : analyse d'offres, évaluation de l'adéquation, génération de CV et lettres adaptés.

## Available Commands

### job-analyze

Analyse une offre d'emploi et extrait les informations structurées.

```bash
job-analyze [URL ou texte de l'offre]
```

**Fonctionnalités:**

- Parse l'offre depuis URL (LinkedIn, WTTJ, Indeed) ou texte
- Extrait exigences obligatoires vs souhaitées
- Identifie les mots-clés ATS
- Recherche des informations entreprise (optionnel)
- Génère un rapport d'analyse structuré

Voir [workflows/job-analyze.md](workflows/job-analyze.md) pour les détails.

### job-fit

Analyse l'adéquation entre le profil et le poste avec validation interactive.

```bash
job-fit [--application=ID]
```

**Fonctionnalités:**

- Compare le CV aux exigences de l'offre
- Calcule un score d'adéquation global (0-100)
- Identifie forces et lacunes
- Génère des talking points pour l'entretien
- **Questionnaire de validation** (AskUserQuestion ou fallback textuel)
- **Confirmation avant génération CV** (arrêt possible si fit insuffisant)
- Fournit une recommandation go/no-go

Voir [workflows/job-fit.md](workflows/job-fit.md) pour les détails.

### job-cv

Génère une version du CV adaptée à l'offre avec questionnaire interactif.

```bash
job-cv [--format=short|long] [--dry-run]
```

**Fonctionnalités:**

- **Choix format en miroir de l'annonce** (courte → court, longue → long)
- **Questionnaire de personnalisation** (titre, ordre, expériences, mots-clés, sidebar)
- Réorganise les expériences par pertinence
- Intègre les mots-clés ATS de l'offre
- Ajuste les compétences de la sidebar
- Génère le fichier Typst adapté avec **métadonnées document**
- Compile le PDF automatiquement
- **Vérification visuelle** post-compilation (pages, zones blanches, débordements)
- Produit un rapport des modifications

Voir [workflows/job-cv.md](workflows/job-cv.md) pour les détails.

### job-letter (Planned - INF-011)

Génère une lettre de motivation personnalisée.

```bash
job-letter [--style=formal|modern]
```

## Architecture

```text
.claude/skills/job-application/
├── SKILL.md                    # Ce fichier (Level 1)
├── workflows/                  # Instructions détaillées (Level 2)
│   ├── job-analyze.md
│   ├── job-fit.md
│   ├── job-cv.md
│   └── job-letter.md
└── templates/                  # Templates de sortie
    └── cv-adapted-template.typ

data/applications/              # Données par candidature
└── {app_id}/                   # Format: {company-slug}-{YYYY-MM-DD}
    ├── {app_id}-job-posting.md     # Offre originale
    ├── {app_id}-analysis.md        # Résultat job-analyze
    ├── {app_id}-fit-report.md      # Résultat job-fit (validé)
    ├── {app_id}-modifications.md   # Choix utilisateur job-cv
    ├── {app_id}-cv-adapted.typ     # CV adapté (source Typst)
    └── {app_id}-cv-adapted.pdf     # PDF compilé
```

## Workflow typique

```text
     [Offre d'emploi]
            |
            v
    +---------------+
    | job-analyze   |  --> {app_id}-analysis.md
    +---------------+
            |
            v
    +---------------+
    | job-fit       |  --> {app_id}-fit-report.md
    +---------------+        |
            |                v
            |         [Questionnaire validation]
            |                |
            |          +-----+-----+
            |          |           |
            |     [Continuer]  [Arrêter]
            |          |           |
            |          v           v
            |    +----------+   [FIN]
            |    | job-cv   |
            |    +----------+
            |          |
            |          v
            |    [Questionnaire personnalisation]
            |          |
            |          v
            |    [Génération + Compilation]
            |          |
            |          v
            |    [Vérification visuelle]
            |          |
            v          v
+-----------+    [CV adapté]
| job-letter|
+-----------+
      |
      v
  [Lettre]
```

## Modèle de données

```yaml
application:
  id: "{company-slug}-{date}"      # ex: wavestone-2025-11-30
  job:
    title: string
    company: string
    location: string
    type: string                   # CDI, CDD, freelance
    url: string
    word_count: number             # Pour déterminer format CV
    company_type: string           # startup, grand_groupe, cabinet
    requirements:
      must_have: []
      nice_to_have: []
    responsibilities: []
    keywords: []                   # ATS keywords
  fit_analysis:
    score: number                  # 0-100
    strengths: []
    gaps: []
    talking_points: []
    recommendation: string         # go/consider/no-go
    validated: boolean             # Validation utilisateur
  cv_customization:
    format: string                 # short/long
    title: string                  # Titre adapté
    experiences_order: []          # Ordre personnalisé
    experiences_omit: []           # Expériences omises
    keywords_priority: string      # all/selection
    sidebar_order: string          # auto/manual
  outputs:
    cv_adapted: path
    cover_letter: path
```

## Nommage des fichiers

Tous les fichiers utilisent le préfixe `{app_id}` (slug de candidature):

| Fichier | Description |
|---------|-------------|
| `{app_id}-job-posting.md` | Offre originale sauvegardée |
| `{app_id}-analysis.md` | Analyse structurée de l'offre |
| `{app_id}-fit-report.md` | Rapport d'adéquation validé |
| `{app_id}-modifications.md` | Choix utilisateur pour le CV |
| `{app_id}-cv-adapted.typ` | Source Typst du CV adapté |
| `{app_id}-cv-adapted.pdf` | PDF compilé |

## Compilation

```bash
# Compiler un CV adapté
just build-adapted {app_id}

# Exemple
just build-adapted wavestone-2025-11-30
```

## Links

- **CV Source:** [src/cv.typ](../../../src/cv.typ)
- **CV Short:** [src/cv-short.typ](../../../src/cv-short.typ)
- **CV Modules:** [src/shared/](../../../src/shared/)
- **Applications Data:** [data/applications/](../../../data/applications/)

---

**Version:** 1.1.0
**Last Updated:** 2025-11-30
