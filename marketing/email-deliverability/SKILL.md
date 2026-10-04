---
name: email-deliverability
description: Base de connaissances email pour {{COMPANY_NAME}} — délivrabilité (SPF/DKIM/DMARC, triage, warm-up), conformité (RGPD, CAN-SPAM, CASL), design d'email dark-mode-safe, benchmarks et playbooks sectoriels. Référence consultative pour la skill email — à charger pour diagnostiquer un problème de délivrabilité, valider une checklist pré-envoi, choisir une plateforme, ou chercher un benchmark. Ne produit pas d'email elle-même.
---

# email-deliverability — référence délivrabilité & conformité email

> Contenu vendorisé et condensé depuis **email-marketing-bible** de CosmoBlk (auteur George Hartley, MIT) — voir `docs/vendored-content.md`. Base construite sur 908 sources et l'exploitation de SmartrMail (~28 000 clients, 6 Mds d'emails). Benchmarks datés mi-2026 : vérifier les chiffres volatils avant de s'y appuyer.

**Rôle : référence consultative.** La production d'emails reste dans la skill `email` (doctrine 01-brand, archives, anti-répétition). Cette skill fournit la couche délivrabilité/conformité/benchmarks que la skill `email` consulte avant validation d'une campagne. Croiser systématiquement avec `docs/etat-de-lart/email.md` (recherche sourcée du template) — les divergences connues sont listées en fin de fichier.

## Garde-fous d'envoi (règles dures, jamais contournées)

- **Jamais d'envoi ni de programmation vers plus d'un destinataire sans validation humaine explicite** dans la conversation. Même un test mono-destinataire se confirme. (Aligné sur la règle du module `04-email/` : dry-run obligatoire.)
- **Toujours présenter le paquet d'approbation avant l'envoi** : taille d'audience, suppressions appliquées, objet, preview text, heure d'envoi, identité expéditeur, désinscription présente (oui/non), risques de conformité.
- **Bloquer l'envoi** si : authentification manquante, désinscription ou adresse postale absente, taux de plainte ≥ 0,1 %, base de consentement floue, audience contenant des supprimés/bounces/plaintes.
- **Jamais sonder un endpoint mutateur inconnu** sur une audience réelle (`/send`, `/dispatch`, `/trigger`, `/fire`, `/publish` peuvent partir immédiatement). Tester sur sandbox ou campagne clonée avec seed list.
- **Séparer les modes** : transactionnel, marketing, lifecycle et cold outbound ont des règles, domaines et bases de consentement différents. Ne jamais mélanger (le cold outbound du template vit dans `12-acquisition/`, jamais sur le domaine principal).
- **Tracer** chaque action autonome (segment modifié, flow édité, campagne créée) pour audit humain.

## Checklist pré-envoi

- [ ] Audience : taille et logique de segment vérifiées contre les comptes réels (les segments générés par IA peuvent être trop larges)
- [ ] Suppressions : désinscrits, bounces, plaintes, cap de fréquence, tickets support en cours
- [ ] Authentification : SPF + DKIM + DMARC alignés (voir triage ci-dessous)
- [ ] Désinscription one-click (RFC 8058) + adresse postale présentes ; honorer sous 48 h
- [ ] Copy : un seul CTA principal, objet court, preview text complémentaire (règles de rédaction détaillées : skill `email` + `docs/etat-de-lart/email.md`)
- [ ] Design : mono-colonne ≤ 600 px, dark-mode-safe, alt text, titre en texte réel (jamais en image)
- [ ] Liens résolus : décoder les URLs trackées pour vérifier la vraie destination des CTA, aucun placeholder
- [ ] Identité expéditeur correcte (from-name + reply-to surveillé)
- [ ] Heure d'envoi et base de consentement valides pour cette audience
- [ ] Test envoyé et relu dans une vraie boîte avec vraies données de fusion
- [ ] Validation humaine capturée

## Délivrabilité — triage

**Authentification (tout est requis)** :
- **SPF** : terminer en `-all`, respecter la limite de 10 lookups DNS
- **DKIM** : clé 2048 bits, rotation annuelle, alignée avec le domaine `From:`
- **DMARC** : progression `p=none` → `quarantine` → `reject`. **Outlook n'accepte plus `p=none` pour ≥ 5 000/jour** (rejet 550 des bulk non conformes) ; Gmail/Yahoo exigent SPF+DKIM+DMARC alignés au même seuil
- BIMI/VMC : levier de confiance Gmail sous-utilisé (pertinent seulement pour expéditeurs matures avec DMARC enforcé + marque déposée)

**Réputation** : le domaine pèse plus que l'IP pour Gmail (mémoire ~120 jours). IP dédiée seulement à partir de ~1 M/mois. Sous-domaines marketing et transactionnel séparés dès ~40 K/mois.

**Chemin de diagnostic quand le placement chute** : symptôme → authentification → blocklists → réputation → logs de bounce → patterns d'envoi → contenu → test/validation → corriger la cause racine → surveiller la récupération (2-4 semaines, jusqu'à 120 jours chez Gmail).

**Seuils et actions** :
- Plainte ≥ 0,1 % : suspendre les envois larges, restreindre aux cliqueurs 30 j, inspecter la source d'acquisition, vérifier la visibilité de la désinscription
- L'engagement est un signal primaire : une grande liste désengagée perd contre une petite liste engagée — sunset automatique du poids mort
- « Bounce bas » ≠ « sûr » : consentement et engagement peuvent suspendre un compte même à 0,1 % de bounce

**Envoi par tiers d'engagement (levier n° 1)** : cliqué 30 j → tous les envois ; 60 j → 75 % ; 90 j → les meilleurs seulement ; 90-180 j → flow de réengagement uniquement ; 180 j+ → sunset. Gain typique : +15-30 % d'ouvertures, −20-40 % de plaintes.

**Warm-up** : montée progressive engagés-d'abord (ex. domaine 300 → 500 → … → 10 K/jour sur ~14 jours ; nouvelle identité 20 → 80/jour sur 2 semaines). Changement d'ESP : vérifier la liste, envoyer aux plus engagés d'abord par tranches, ré-opt-in des dormants 6 mois+.

**Ère IA** : Gmail Gemini et Apple Intelligence résument l'email depuis les **~150-200 premiers caractères de texte réel** (ils priment sur le preheader) → charger l'offre en tête, en vrai texte, jamais image-only. Le texte IA brut non personnalisé est filtré plus durement (filtre gen-AI de Google) : les tokens de personnalisation sont devenus une exigence de délivrabilité.

**L'échec silencieux est le vrai risque** : un flow qui cesse d'envoyer sans bruit se détecte des jours plus tard. Prévoir une revue programmée (quels flows n'ont pas tiré, lesquels sont en erreur, quelles métriques ont chuté) — à intégrer au rituel `11-reporting/`.

## Conformité

Porte de décision avant tout envoi : (1) type d'email ? (2) région du destinataire ? (3) base de consentement ? (4) désinscription + adresse postale présentes ? (5) suppressions appliquées ? (6) contenu matériellement exact ? Si un point est flou : refuser ou demander.

| Régulation | Consentement préalable | Règles clés | Sanction |
|---|---|---|---|
| RGPD (UE) | Oui | effacement sous 30 j, preuve de consentement | jusqu'à 4 % du CA / 20 M€ |
| CAN-SPAM (US) | Non (opt-out) | en-têtes exacts, adresse postale, opt-out ≤ 10 j | ~51 744 $/email (2026) |
| CASL (Canada) | Oui | consentement implicite 2 ans post-achat | jusqu'à 10 M$ CAD |
| Spam Act (AU) | Oui | consentement + identité + désinscription ≤ 5 j ouvrés | jusqu'à 2,22 M$ AUD/jour |

- One-click unsubscribe (RFC 8058) requis dès 5 000/jour vers Gmail/Yahoo/Microsoft ; honorer sous 48 h.
- **L'IA ne transfère pas la responsabilité** : vous répondez des envois de l'agent ; ne jamais lui faire confiance pour préserver la désinscription/le footer quand il édite un template — vérifier à chaque édition.
- Prospection B2B : cadre France/UE dans `12-acquisition/conformite-rgpd.md` (fait autorité pour ce template) ; le cold email reste séparé de l'infrastructure marketing (domaines dédiés, warm-up 2-4 semaines, 10-30/boîte/jour).

## Design d'email (dark-mode et anti-slop)

- **Contraintes par défaut dans tout brief** : mono-colonne ≤ 600 px, cibles tactiles 44 px, tables `role="presentation"`, couleurs dark-mode-safe (**jamais de fond #000 pur ni de logo #fff** — base ~#121212), alt text sur chaque image.
- **Titres en texte réel, jamais en image** : triple gain accessibilité + dark mode + résumé IA.
- Générer dans un substrat sûr (MJML, React Email, Maizzle) qui compile en HTML compatible boîtes de réception (Outlook inclus) — jamais du HTML brut prompté.
- Anti-slop : posséder une couleur (30-60 % de la surface), soustraire plutôt que décorer, vraie photo plutôt qu'image IA visible (baisse la confiance), un message unique. Pour ce template : les tokens de `01-brand/style-guide.md` font autorité.
- QA avant staging : rendu mobile, dark mode, poids images (< 200 Ko chacune, < 800 Ko total), préview cross-clients.
- Archétypes de design selon la situation (produit ennuyeux → voix audacieuse ; premium → minimal et jamais discount-led ; welcome/win-back → founder-letter plain-text qui appelle une réponse ; transactionnel → l'email le plus ouvert, le designer, pas le templater).

## Flows (rappel de priorité) et benchmarks

**Les flows rapportent ~30× plus par destinataire que les campagnes.** Ordre de construction : welcome → panier abandonné → browse abandonment → post-achat → win-back → cross-sell → VIP → sunset. (Détail des séquences : skill `email-sequence` du plugin marketing ou skill `email`.)

**Métriques (l'open rate est du bruit post-MPP** — juger sur clics, réponses, conversions, revenu/destinataire — cohérent avec R16 de l'état de l'art) :

| Métrique | Bon | Fort | Alerte |
|---|---|---|---|
| CTR | 2-3 % | 4 %+ | < 1 % |
| CTOR | 10-15 % | 20 %+ | < 5 % |
| Désinscription | < 0,2 % | < 0,1 % | > 0,5 % |
| Bounce | < 2 % | < 1 % | > 3 % |
| Plainte spam | < 0,1 % | < 0,05 % | > 0,3 % |
| Placement inbox | 85-94 % | 94 %+ | < 70 % |

Par type (ouverture/CTR, directionnel) : welcome 50-60 % / 5-8 % · panier 40-50 % / 5-10 % · transactionnel 60-80 % / 5-15 % · promo 15-20 % / 2-3 % · newsletter 20-30 % / 3-5 %.

**Playbooks sectoriels (essentiel)** : e-commerce DTC → l'email pèse 25-40 % du CA, le profit est dans les flows automatiques ; SaaS B2B → onboarding comportemental, un CTA par email ; newsletter/créateur → la voix anti-slop est le différenciateur, inflexion ~10 K abonnés ; nonprofit → ratio 3:1 valeur/sollicitation. Fréquences : e-commerce 2-4/sem. engagés · SaaS 1-2/mois · newsletter 1-3/sem.

## Divergences avec `docs/etat-de-lart/email.md` (arbitrages)

1. **Longueur d'objet** — EMB : « ≤ 45 caractères, < 25 ouvre le mieux » ; état de l'art (R7) : « 6-10 mots / 36-50 caractères, message clé dans les 33 premiers ». Les études sous-jacentes diffèrent. **Arbitrage template : suivre R7 (36-50 car.) en plaçant le message clé dans les 33 premiers caractères** — ce qui satisfait aussi la contrainte mobile d'EMB.
2. **Chiffres CTA** — EMB : bouton +27 %, CTA unique +42 % ; état de l'art (R10-R11) : bouton +45 %, CTA unique +371 %. Même direction, ampleurs très différentes selon les études. **Traiter comme ordres de grandeur ; la règle opérationnelle (un seul CTA principal, en bouton, dupliqué haut/bas) est identique des deux côtés.**
3. **DMARC** — état de l'art (R1) : `p=none` accepté comme point de départ (exigence Gmail/Yahoo) ; EMB : Outlook exige `p=quarantine` ou plus pour ≥ 5 000/jour. Pas une contradiction mais un durcissement : **retenir la règle la plus stricte (viser `p=quarantine` minimum) dès que l'audience contient du Outlook/Microsoft en volume.**
4. **Pas de contradiction** sur : plainte < 0,1 % cible / 0,3 % enforcement, one-click RFC 8058 sous 48 h/2 j, mythe des « mots spam », open rate non fiable, welcome email le plus ouvert, cold email 50-125 mots. Les deux sources se renforcent.
5. **Conflit d'intérêt signalé** : la table de plateformes d'EMB recommande nitrosend, qui partage un fondateur avec le guide (divulgué dans la source). Pour ce template, le choix d'outil reste `{{EMAIL_MARKETING_TOOL}}` configuré via `/tools-setup` — ne pas relayer cette recommandation sans ce contexte.
