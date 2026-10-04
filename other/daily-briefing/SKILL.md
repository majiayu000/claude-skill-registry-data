---
name: daily-briefing
description: "Briefing matinal : hotLeads du jour, signaux BODACC/JOAFE, KPIs pipeline, 3 priorités. Cron 7h ou manuel."
metadata: { "openclaw": { "emoji": "🌅" } }
user-invocable: true
---

# Skill: daily-briefing

## Quand utiliser cette skill

Déclenchement **automatique à 7h00** via cron OpenClaw (`@daily-briefing`).
Peut aussi être invoqué manuellement : `"Albert, donne-moi mon briefing"`.

Destinataire unique : fondateur solo. Canal de sortie : **Telegram** (markdown sobre, émojis).

## Workflow

```
STEP 1 — Leads chauds
  find_all_leads(hotLeadScore_min=0.7, limit=20)
  → Trier par (hotLeadScore × fraîcheur_signal) DESC
  → Conserver top 3 pour affichage

STEP 2 — Signaux nuit
  detect_bodacc_signals(event_types=["creation","modification"], days_back=1)
  → Compter créations / modifications
  → Identifier signal le plus saillant (type + nom entité)

STEP 3 — Santé infra
  get_workers_status()
  → Parser statut de chaque crawler
  → Si status == "error" sur >=1 worker → flag ALERTE_INFRA = true

STEP 4 — Lire pipeline (MEMORY.md)
  Extraire : leads contactés, RDV planifiés, signatures en attente

STEP 5 — Générer priorités
  Règle P1 : si ALERTE_INFRA → "Résoudre incident crawler [nom]"
  Règle P2 : lead score le plus élevé avec signal < 24h → "Contacter [NOM]"
  Règle P3 : RDV le plus proche dans pipeline → "Préparer RDV [NOM] à [HEURE]"
  Fallback P3 : "Prospecter lot [département] leads score 0.6-0.7"

STEP 6 — Formatter output Telegram → envoyer
```

## Instructions

### Calcul du score de fraîcheur

```
score_tri = hotLeadScore × fraîcheur
fraîcheur = 1.0  si signal_date == aujourd'hui
           0.7  si signal_date == hier
           0.4  si signal_date <= 7 jours
           0.1  si pas de signal récent
```

Trier `top_leads` par `score_tri` DESC avant d'afficher les 3 premiers.

### Règles de génération des priorités

| Condition                                      | Priorité générée                                  |
|------------------------------------------------|---------------------------------------------------|
| `get_workers_status` retourne `error`          | **P1 bloquant** : résoudre incident crawler       |
| Lead avec `score_tri >= 0.85` ET signal < 24h  | Contacter immédiatement (email ou LinkedIn)       |
| RDV confirmé dans MEMORY.md dans les 48h      | Préparer brief association avant le RDV           |
| Aucun lead chaud ET aucun signal BODACC        | Lancer prospection batch sur département prioritaire |

### Format output Telegram

```
*Briefing Albert — [DATE JJ/MM/AAAA] — [HH:MM]*

*Pipeline*
• Leads chauds (>0.7) : [N]
• Signaux BODACC nuit : [N] créations / [N] modif
• RDV en attente : [N]
• Dernier crawl JOAFE : [DATETIME]

*Top 3 Leads du jour*
1\. [NOM\_ASSOCIATION] ([dept]) — score [X.XX] — [signal\_court]
2\. [NOM\_ASSOCIATION] ([dept]) — score [X.XX] — [signal\_court]
3\. [NOM\_ASSOCIATION] ([dept]) — score [X.XX] — [signal\_court]

*Alertes infra* : [OK / ERREUR crawler\_name]

*3 priorités*
1\. [priorité P1]
2\. [priorité P2]
3\. [priorité P3]
```

> **Règles de formatage Telegram :**
> - Markdown mode `MarkdownV2` : échapper `.` `(` `)` `-` avec `\`
> - Jamais de blocs de code ou tableaux (illisibles sur mobile)
> - `[signal_court]` = 3 mots max ex. "création BODACC", "modif statuts", "subv éligible"
> - `[NOM_ASSOCIATION]` tronqué à 30 chars si nécessaire + `…`

### Gestion des cas limites

| Cas                                    | Comportement                                                  |
|----------------------------------------|---------------------------------------------------------------|
| `find_all_leads` retourne 0 résultats  | Afficher "Aucun lead chaud aujourd'hui" + P1 = prospection    |
| `detect_bodacc_signals` timeout        | Afficher "Signaux BODACC indisponibles" + continuer           |
| `get_workers_status` retourne error    | P1 = incident, bloquer outreach jusqu'à résolution            |
| MEMORY.md absent ou vide              | Afficher "Pipeline vide — initialiser MEMORY.md"             |

## Mise à jour MEMORY.md post-briefing

Après génération, ajouter en tête de MEMORY.md :

```
## Briefing [DATE]
- Leads chauds : [N] | Signaux nuit : [N] | Crawl JOAFE : [DATETIME]
- Priorités : [P1 résumé] / [P2 résumé] / [P3 résumé]
```
