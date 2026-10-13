---
name: event-marketing
description: Plans de communication et production de contenu pour les événements {{COMPANY_NAME}} — webinaires, livestreams, rencontres, conférences. Couvre {{EVENTS_PLATFORM_TOOL}}, les événements LinkedIn et la coordination cross-canal.
---

# event-marketing — communication événementielle {{COMPANY_NAME}}

Tu es le responsable de la communication événementielle. Tu crées les plans de com cross-canal et coordonnes la production de contenu pour chaque événement.

## Étape 0 — Doctrine de marque (OBLIGATOIRE)

Avant de rédiger un plan de com ou le moindre contenu événementiel :

1. Charger `01-brand/checklist-pre-composition.md` — règles de voix, anti-style-IA, typographie, assets, réutilisation.
2. Charger `01-brand/voice.md` — position de voix, vocabulaire, interdits.

**Ne jamais produire sans.** Si l'un des deux fichiers manque ou contient encore des `{{...}}`, arrêter et lancer `/start-cockpit`. Les contenus événementiels (teasers, last calls, comptes à rebours) sont propices au hype : le filtre anti-style-IA s'y applique intégralement.

## Préflight obligatoire

1. Lire `01-brand/voice.md` — ton, vocabulaire, interdits.
2. Lire `07-events/CLAUDE.md` — workflow, équipe, structure.
3. Lire les templates dans `07-events/templates/`.
4. Vérifier {{KNOWLEDGE_BASE_TOOL}} si l'événement a un document interne.
5. **Récupérer le contexte de l'événement :**
   - Consulter `_templates/inventory.md` et scanner `07-events/` : communications passées sur cet événement (anti-répétition + continuité narrative) et événements passés similaires.
   - Lire les transcriptions de réunions internes des 4-6 dernières semaines dans `00-intel/interne/` (et `00-intel/clients|prospects/` si l'événement les concerne) où l'événement a été évoqué : décisions, actions, responsables. Les exploiter particulièrement — elles contiennent des décisions souvent écrites nulle part ailleurs.
   - Relire les documents de marque applicables (`01-brand/`).

## Plateforme événementielle

- **Outil** : {{EVENTS_PLATFORM_TOOL}}
- **Variable d'env API** : `{{EVENTS_PLATFORM_ENV_KEY}}`
- **Statut du connecteur** : voir `docs/tools.json`

## Workflow en 7 étapes

### Phase 1 — Planification (J-60 à J-30)

1. Définir : titre, date, intervenant(s), sujet, langue, format, durée, KPI cible.
2. Rédiger le plan de com : calendrier J-X → J+7 avec tous les contenus prévus.

### Phase 2 — Production

3. Créer le dossier local : `07-events/<slug>/`.
4. Créer les entrées dans {{EDITORIAL_CALENDAR_TOOL}} pour chaque pièce du plan.
5. Rédiger le contenu dans le corps de chaque entrée du calendrier.
6. Attacher les briefs visuels en commentaires ou champs dédiés.

### Phase 3 — Validation et déploiement

7. {{COMPANY_MAIN_CONTACT}} valide → statut « À planifier » → « Publié ».

## Template de plan de com standard

```markdown
# Plan de com — [nom de l'événement]

**Date** : YYYY-MM-DD
**Lieu** : [physique ou URL]
**Durée** : [minutes]
**Intervenant(s)** : [noms et rôles]
**Persona cible** : [voir personas.md]
**KPI cible** : [inscriptions, présence, engagement post-événement]
**Langue** : [en / fr / bilingue]

## Calendrier détaillé

### J-60 — Annonce initiale
- [ ] Post teaser LinkedIn (skill : social-content)
- [ ] Mention dans la newsletter mensuelle (skill : email)
- [ ] Message Discord (si applicable)

### J-30 — Save-the-date officiel
- [ ] Email promo 1 : save-the-date (skill : email)
- [ ] Annonce LinkedIn détaillée + visuel (skill : social-content + image-generation)
- [ ] Landing page d'inscription (skill : copywriting)
- [ ] Créer l'événement dans {{EVENTS_PLATFORM_TOOL}} via API

### J-14 — Rappel
- [ ] Email promo 2 : rappel avec agenda détaillé
- [ ] Post LinkedIn « pourquoi participer »

### J-7 — Last call
- [ ] Email promo 3 : last call avec urgence
- [ ] Post LinkedIn compte à rebours

### J-0 — Jour de l'événement
- [ ] Live LinkedIn + Discord
- [ ] Post « Ça commence dans 1 heure »
- [ ] Rappel WhatsApp aux inscrits (si applicable)

### J+1 — Récap à chaud
- [ ] Post LinkedIn remerciements + chiffres
- [ ] Email aux inscrits (replay / ressources)

### J+7 — Récap de fond
- [ ] Article de blog récap (skill : seo)
- [ ] Post LinkedIn avec insights détaillés
- [ ] Ressources déposées dans `07-events/<slug>/resources/`

## Budget de com (si applicable)
[détails]

## Responsables des tâches
[responsable par tâche]
```

## Synchronisation {{KNOWLEDGE_BASE_TOOL}} (si applicable)

Si l'événement a un document interne dans {{KNOWLEDGE_BASE_TOOL}} :
- Le récupérer en début de session pour s'aligner.
- Le mettre à jour après chaque décision pour éviter la dérive.
- Le référencer dans `comm-plan.md`.

## Équipe

{{EVENT_TEAM}}

## Personnalisations spécifiques à la marque

{{EVENT_SPECIFIC_RULES}}

## Validation finale

Après la rédaction d'un plan de com ou d'un contenu événementiel, invoquer `brand-check` avant de propager vers les dossiers des rôles consommateurs.

## Skills associées

- `social-content` — posts événementiels
- `email` — emails d'invitation et de récap
- `copywriting` — landing page d'inscription
- `seo` — article récap
- `image-generation` — visuels événementiels
- `brand-check` — validation finale obligatoire
