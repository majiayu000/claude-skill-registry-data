---
name: lead-pipeline
description: "Workflow datalake → scoring hotLeadScore → profil complet lead associatif. Utiliser quand on demande des prospects, leads, pipeline."
metadata: { "openclaw": { "emoji": "🎯" } }
user-invocable: true
---

# Skill: Lead Pipeline

## Quand utiliser cette skill

Utiliser cette skill dès que l'utilisateur demande :
- Trouver des prospects / leads associations dans un département ou secteur
- Scorer et prioriser des associations cibles pour une prestation numérique
- Générer un profil complet d'une association (maturité digitale, subventions, signaux BODACC)
- Constituer un pipeline commercial associations enrichi et trié par score
- Toute question commençant par "quelles associations", "trouve-moi des leads", "pipeline prospects"

Ne pas utiliser si l'utilisateur demande uniquement des données de subventions sans contexte prospect → utiliser `subvention-scorer` à la place.

---

## Workflow (Pattern Chaining)

```
search_entities → find_all_leads → generate_dossier × N → detect_bodacc_signals × N → scoring consolidé → output structuré
```

### Étape 1 — Recherche entités candidates
```
search_entities(
  query        = <terme métier extrait du message>,
  department   = <code département si mentionné, sinon omis>,
  type         = "association",
  scoring      = true
)
```
- Extraire le `query` depuis l'intention utilisateur (ex: "sport", "culture", "aide alimentaire")
- Toujours passer `department` si un département ou une ville est mentionné dans le message
- Limite : 20 résultats par appel (pagination avec `offset` si l'utilisateur demande "la suite")

### Étape 2 — Filtrage leads qualifiés
```
find_all_leads(
  hotLeadScore_min = 0.5
)
```
- Croiser avec les SIRENs obtenus à l'étape 1
- Conserver uniquement les entités avec `hotLeadScore >= 0.5`
- Trier par `hotLeadScore DESC`

### Étape 3 — Génération dossier complet (par SIREN retenu)
```
generate_dossier(siren = <siren>)
```
- Appeler pour chaque lead retenu (max 10 dossiers par run pour contrôler la latence)
- Extraire : maturité digitale, subventions éligibles, présence web, effectif, budget
- Si `generate_dossier` échoue sur un SIREN → logger le SIREN en erreur et continuer

### Étape 4 — Détection signaux BODACC (par SIRET retenu)
```
detect_bodacc_signals(
  siret        = <siret>,
  event_types  = ["creation", "modification", "cession"]
)
```
- Appeler pour chaque lead dont le dossier a été généré avec succès
- Un signal récent (< 6 mois) est un déclencheur prioritaire → booster le score final
- Ignorer les associations avec un signal "cession" ou "dissolution" → les exclure du pipeline

### Étape 5 — Scoring consolidé

Pour chaque lead, calculer un `score_final` composite :

| Composant              | Poids | Source               |
|------------------------|-------|----------------------|
| hotLeadScore           | 40 %  | find_all_leads       |
| Signal BODACC récent   | 25 %  | detect_bodacc_signals|
| Subventions éligibles  | 20 %  | generate_dossier     |
| Maturité digitale faible (opportunité) | 15 % | generate_dossier |

Formule indicative :
```
score_final = (hotLeadScore × 0.4)
            + (signal_recent ? 0.25 : 0)
            + (nb_subventions_eligibles > 0 ? 0.20 : 0)
            + (maturite_digitale_score < 0.4 ? 0.15 : 0)
```

### Étape 6 — Output structuré

Retourner la liste triée par `score_final DESC` au format :

```json
[
  {
    "siren": "123456789",
    "nom": "Association XYZ",
    "departement": "75",
    "hotLeadScore": 0.82,
    "score_final": 0.91,
    "subventions_eligibles": ["FEDER numérique PME", "AMI Inclusion Numérique"],
    "signaux_bodacc": ["modification_2025-03"],
    "canal_recommande": "email_froid",
    "maturite_digitale": "faible"
  }
]
```

---

## Instructions

### Extraction du contexte
- Détecter automatiquement département (2 chiffres ou nom), secteur activité, taille association
- Si aucun département mentionné → ne pas filtrer géographiquement, lancer national
- Si l'utilisateur mentionne une ville → résoudre en code département avant l'appel

### Gestion des erreurs
- Si `search_entities` renvoie 0 résultats → relancer avec query élargie (retirer qualificatifs)
- Si `generate_dossier` timeout → inclure le lead sans données dossier, annoter "dossier_indisponible"
- Si `detect_bodacc_signals` échoue → inclure le lead sans signaux, annoter "signaux_indisponibles"

### Règles CNIL / confidentialité
- Ne jamais exposer dans l'output : noms de dirigeants, adresses personnelles, données RH nominatives
- Les données retournées concernent uniquement les personnes morales (associations)
- En cas de doute sur une donnée → l'omettre plutôt que l'inclure

### Format de réponse à l'utilisateur
1. Résumé en une phrase : "J'ai trouvé N leads qualifiés en [département/secteur]"
2. Tableau markdown des 5 meilleurs leads (siren, nom, score_final, canal_recommandé)
3. Proposer : "Voulez-vous le dossier complet sur l'un d'eux ?"
4. Ne jamais dépasser 20 leads affichés sans demande explicite de pagination

### Canaux recommandés
- `hotLeadScore >= 0.8` + signal BODACC récent → `appel_direct`
- `hotLeadScore >= 0.6` → `email_froid`
- `hotLeadScore < 0.6` → `nurturing_newsletter`

### Performance
- Paralléliser les appels `generate_dossier` et `detect_bodacc_signals` si le runtime le permet
- Limiter à 10 dossiers générés par run pour maintenir la latence < 30s sur Qwen3.5-9B local
