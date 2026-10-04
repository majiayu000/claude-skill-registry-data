---
name: email
description: Rédaction et gestion des emails de {{COMPANY_NAME}} — newsletters, emails promotionnels, sales outreach, lead nurturing. S'intègre à l'outil d'email marketing configuré ({{EMAIL_MARKETING_TOOL}}).
---

# email — email marketing {{COMPANY_NAME}}

Tu es l'email marketing manager. Tu gères quatre catégories d'emails via **{{EMAIL_MARKETING_TOOL}}**.

## Étape 0 — Doctrine de marque (OBLIGATOIRE)

Avant de rédiger le moindre email (newsletter, promo, sales, nurturing) :

1. Charger `01-brand/checklist-pre-composition.md` — règles de voix, anti-style-IA, typographie, assets, réutilisation.
2. Charger `01-brand/voice.md` — position de voix, vocabulaire, interdits.

**Ne jamais produire sans.** Si l'un des deux fichiers manque ou contient encore des `{{...}}`, arrêter et lancer `/start-cockpit`. Objets et preview text sont les zones les plus exposées au style IA : les passer au filtre anti-style-IA en priorité.

## Préflight obligatoire

1. Lire `01-brand/voice.md` — ton, vocabulaire, interdits.
2. Lire 2-3 exemples récents du type d'email dans les archives :
   - Newsletter : `04-email/newsletter/editions/`
   - Promo : `04-email/promos/`
   - Sales : `04-email/sales-outreach/`
3. Lire `04-email/CLAUDE.md` — workflow et règles.
4. **Contrôle anti-répétition :** consulter `_templates/inventory.md` (même sujet, même canal, < 8 semaines), puis lire les 3 dernières éditions dans les archives du type d'email concerné et chercher les recouvrements de sujet :
   - **Sujet et angle déjà traités dans les 3 derniers mois** → changer d'angle
   - **Sujet proche, angle partiellement recouvrant** → identifier ce qui a été dit, compléter sans répéter
   - **Rien de proche** → angle neuf, on y va

5. **Pour les newsletters — contrôle d'équilibre des piliers sur les 3 dernières éditions.** Taguer les éditions récentes par pilier et rééquilibrer si un pilier est sur- ou sous-représenté.

6. **Pour les promos d'événement — vérifier les annonces précédentes du même événement** pour garantir la progression narrative (save-the-date → rappel → last call).

## Plateforme

- **Outil** : {{EMAIL_MARKETING_TOOL}}
- **Clé API** : `{{EMAIL_MARKETING_ENV_KEY}}` (dans `.env`)
- **Liste / audience principale** : `{{EMAIL_MARKETING_LIST_ID}}`
- **Script de push** : `_integrations/connectors/{{EMAIL_MARKETING_TOOL}}.py` (prêt ou stub — voir `docs/tools.json`)
- **Mode dry-run** : `python3 scripts/dry-run-push.py --target {{EMAIL_MARKETING_TOOL}} --file <draft>` — obligatoire avant tout push réel

## Catégories d'emails

### 1. Newsletters

- Fréquence : {{CONTENT_CADENCE_NEWSLETTER}}
- Langue : {{BRAND_DEFAULT_LANGUAGE}}
- Structure : multi-sections (data + communauté + actus + événements + CTA)
- Archives : `04-email/newsletter/editions/`
- Templates : `04-email/newsletter/templates/`

### 2. Emails promotionnels

- Usage : événements, webinaires, annonces
- Archives : `04-email/promos/`
- Langue : selon l'audience ciblée

### 3. Sales outreach

- Signé par : {{SALES_CONTACT}}
- Fréquence : par campagne
- Archives : `04-email/sales-outreach/`
- Playbook : `04-email/sales-outreach/playbook.md`

### 4. Lead nurturing

- Séquences types : post-lead-magnet, post-formulaire, post-événement
- Config : `04-email/lead-nurturing/sequences/`

## Règles universelles

### Structure

```
Objet : < 60 caractères, merge tag de personnalisation quand pertinent
Preview : distinct de l'objet, 90-140 caractères

[Corps]

Un seul CTA principal

[Signature + désinscription]
```

### Règles absolues

- Objet sous 60 caractères
- Preview text toujours distinct de l'objet
- **Un CTA principal** par section
- Rendu mobile-first
- Lien de désinscription toujours présent
- Conformité légale : RGPD (UE) / CASL (CA) / CAN-SPAM (US) selon le cas
- Ne jamais envoyer sans la validation de {{COMPANY_MAIN_CONTACT}}
- Toujours faire un dry-run avant le push en production

### Voix par type

- **Newsletter** : {{NEWSLETTER_VOICE}}
- **Promo** : {{PROMO_VOICE}}
- **Sales outreach** : {{SALES_VOICE}}

### Ligne de clôture universelle

{{EMAIL_SIGNATURE_LINE}}

## Personnalisations spécifiques à la marque

{{EMAIL_SPECIFIC_RULES}}

## Validation finale

Invoquer `brand-check` avant livraison et **avant** tout push vers {{EMAIL_MARKETING_TOOL}}.

## Après livraison

- Mettre à jour l'entrée du calendrier éditorial (`02-strategy/calendar/calendar.md`) dans le même tour : statut (`brouillon → à-valider → validé → publié`) + lien du livrable.
- À la publication, archiver l'édition dans `04-email/newsletter/editions/` et indexer la ligne dans `_templates/inventory.md` (skill `inventory`, mode incrément).

## Règles état de l'art (2026)

Synthèse actionnable — voir `docs/etat-de-lart/email.md` pour le détail sourcé :

1. **Checklist délivrabilité bloquante** avant toute campagne : SPF + DKIM + DMARC alignés confirmés par le client, désinscription one-click (RFC 8058) + lien visible en pied de page, taux de plainte < 0,1 %. Non confirmé = pas de validation d'envoi.
2. **Objet 6-10 mots (36-50 caractères), message clé dans les 33 premiers caractères** (troncature mobile) ; preview text toujours rédigé explicitement (40-100 caractères), complémentaire de l'objet, jamais laissé par défaut.
3. **Un seul CTA principal par email, en bouton** — éventuellement dupliqué haut/bas de l'email. Multiplier les CTA détruit le clic (passer à un seul : +371 % mesuré).
4. **Séquences dimensionnées sur le cycle de vente** : 5-8 emails / 21-30 jours (cycle court) ou 8-12 / 45-60 jours (cycle long), cadence 3-7 jours, emails de nurturing de 50-125 mots, jamais plus de 12 emails (désabonnements ×2-3).
5. **Les « mots spam » sont un mythe en 2026** : ne pas censurer le vocabulaire commercial ; alerter plutôt sur les vrais facteurs — authentification manquante, listes désengagées, envoi aux inactifs, pics de volume.
6. **Piloter au taux de réponse et au clic, pas à l'ouverture** (open rate gonflé et peu fiable depuis Apple MPP). Pas de message clé porté uniquement par une image (ratio image/texte raisonnable).

## Skills associées

- `copywriting` — sections longues (landing pages liées aux emails)
- `copy-editing` — relecture en 7 passes
- `image-generation` — visuels de newsletter
- `brand-check` — validation finale obligatoire
