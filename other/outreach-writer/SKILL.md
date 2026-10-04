---
name: outreach-writer
description: "Rédiger messages outreach personnalisés CNIL-compliant depuis profil lead datalake. Email, LinkedIn, WhatsApp."
metadata: { "openclaw": { "emoji": "✉️" } }
user-invocable: true
---

# Skill: outreach-writer

## Quand utiliser cette skill

Invoquer **après** `lead-pipeline` quand un lead a un `hotLeadScore >= 0.6` et qu'un message
sortant doit être rédigé. Ne jamais invoquer sur des données brutes sans enrichissement préalable.

Canaux supportés : **Email**, **LinkedIn InMail**, **WhatsApp** (contact établi uniquement).

## Workflow

```
Input: {siren, nom, département, hotLeadScore, subventions_éligibles, signaux_bodacc, maturite_digitale}
  |
  |-- 1. get_entity_details(siren)         → dénomination exacte, objet social, date création
  |-- 2. get_subvention_data(siren)        → montant max éligible, dispositif, taux couverture
  |-- 3. detect_bodacc_signals(siren)      → signal le plus récent (type + date)
  |-- 4. get_digital_maturity_stats(siren) → score maturité 0-100, lacunes détectées
  |
  +-- 5. Sélectionner template canal → injecter variables → valider règles CNIL → output
```

## Instructions

### Sélection du canal

| Canal     | Condition d'utilisation                              | Longueur max |
|-----------|------------------------------------------------------|-------------|
| Email     | Toujours disponible (source JOAFE = base publique)   | 150 mots    |
| LinkedIn  | Profil LinkedIn identifié dans entity_details        | 300 chars   |
| WhatsApp  | Contact direct préalablement établi **seulement**    | 3 lignes    |

---

### Template Email

```
SUJET : [signal_bodacc OU dispositif_subvention] — [nom_association] × [consultant]

Bonjour [prénom_contact OU "Madame, Monsieur"],

[ACCROCHE — 1 phrase ancrée dans un signal réel]
Exemples :
  - "Votre récente modification statutaire au JOAFE ({{date_signal}}) m'a conduit à regarder
    votre dossier de plus près."
  - "{{nom_association}} figure parmi les bénéficiaires potentiels du dispositif
    {{dispositif_subvention}} — jusqu'à {{montant_max}}€ de financement."

[VALEUR — 2 phrases max]
Avec un reste à charge de 0€, vous pourriez financer {{domaine_lacune}} (score maturité
digitale actuel : {{score_maturite}}/100) via {{dispositif_subvention}}.

[CTA]
Un audit digital gratuit de 30 min vous intéresse ?
Répondez simplement "OUI" et je vous propose 3 créneaux cette semaine.

Cordialement,
[Nom complet du consultant]
[Titre] — [Structure]

---
Source des données : JOAFE / data.gouv.fr (registres publics).
Conformément au RGPD Art. 6(1)(f), vous pouvez vous opposer à tout traitement en répondant
"STOP" ou en écrivant à [email_opt_out]. Aucune donnée sensible n'est utilisée.
```

**Variables à injecter :**
- `{{date_signal}}` — date ISO du signal BODACC/JOAFE
- `{{nom_association}}` — dénomination exacte (get_entity_details)
- `{{dispositif_subvention}}` — libellé dispositif (get_subvention_data)
- `{{montant_max}}` — montant plafond éligible en euros
- `{{domaine_lacune}}` — premier gap détecté (get_digital_maturity_stats)
- `{{score_maturite}}` — score 0-100

---

### Template LinkedIn InMail

```
Bonjour [prénom],

Signal JOAFE {{date_signal}} → {{nom_association}} éligible {{montant_max}}€ ({{dispositif}}).
Votre asso peut financer {{domaine_lacune}} à 0€ reste à charge.
Audit 30 min offert — intéressé(e) ?
```

> 300 caractères max. Supprimer `signal JOAFE {{date_signal}} →` si le signal dépasse
> 30 jours. Ne pas mentionner de données personnelles autres que le prénom.

---

### Template WhatsApp

```
Bonjour [prénom]
{{nom_association}} est éligible {{montant_max}}€ via {{dispositif}} — reste à charge 0€.
Dispo 30 min cette semaine pour en parler ?
```

> **Jamais en premier contact non sollicité.** Uniquement si échange préalable documenté.
> Ton conversationnel, pas de markdown. Maximum 3 lignes affichées sur mobile.

---

## Règles CNIL obligatoires

1. **Source** : Mentionner explicitement JOAFE ou data.gouv.fr comme origine des données.
2. **Données personnelles** : Utiliser uniquement le prénom + nom de l'association.
   Aucune donnée sensible (santé, appartenance syndicale, etc.) dans le message.
3. **Opt-out** : Chaque email doit contenir une instruction de désinscription claire.
4. **Identité** : Toujours signer avec le nom réel du consultant — jamais un alias.
5. **Base légale** : RGPD Art. 6(1)(f) intérêt légitime, applicable car :
   - Données issues de registres publics (JOAFE, BODACC)
   - Proposition commerciale B2B vers une personne morale
   - Intérêt légitime documenté (financement associatif)
6. **Registre** : Logger chaque envoi dans MEMORY.md `[DATE] outreach → [SIREN] via [canal]`.

## Footer email obligatoire (RGPD — à inclure dans TOUS les emails)

Ajouter systématiquement en fin de message :

---
*Pour ne plus recevoir de messages de notre part, répondez simplement STOP.*  
*[Prénom Nom] — Consultant RGPD & DevSecOps — SIREN [À COMPLÉTER]*  
*Conformément au RGPD (Art. 21) et à l'Art. L34-5 CPCE*

## Validation avant envoi

- [ ] `hotLeadScore >= 0.6` confirmé
- [ ] Signal BODACC ou subvention <= 90 jours (fraîcheur)
- [ ] Opt-out présent (email uniquement)
- [ ] Source JOAFE/data.gouv.fr mentionnée
- [ ] Longueur canal respectée
- [ ] Aucune donnée sensible dans le corps du message

## Boucle Evaluator-Optimizer (qualité)

Après avoir généré un draft de message, appliquer obligatoirement cette boucle avant livraison :

### Critères d'évaluation (score /10)

| Critère | Poids | Description |
|---------|-------|-------------|
| Personnalisation | 30% | Signal BODACC/JOAFE réel et récent ancré dans l'accroche |
| Clarté valeur | 25% | Montant €, dispositif, reste à charge explicitement chiffrés |
| CTA précis | 20% | Un seul CTA clair, action unique demandée |
| Conformité CNIL | 15% | Opt-out présent, source mentionnée, aucune donnée sensible |
| Ton B2B | 10% | Professionnel, direct, pas de sur-promesse |

**Score seuil minimum : 7.5/10** pour livraison.

### Procédure

```
draft = générer_message(template, variables)
iteration = 1

TANT QUE score < 7.5 ET iteration <= 3:
  critique = évaluer(draft, critères)
  corrections = ["améliorer X car Y", ...]
  draft = affiner(draft, corrections)
  score = réévaluer(draft)
  iteration++

SI score < 7.5 après 3 itérations:
  → Signaler à Teddy : "outreach [SIREN] qualité insuffisante (score: X/10)"
  → NE PAS envoyer le message

SINON:
  → Livrer draft + score_final + nb_iterations
```

### Exemples de corrections typiques

- **Personnalisation < 6** : "L'accroche ne mentionne pas de signal réel — chercher événement BODACC/JOAFE des 30 derniers jours"
- **Clarté valeur < 7** : "Le montant max n'est pas chiffré — injecter `{{montant_max}}`€"
- **CTA < 8** : "Deux CTAs détectés — garder uniquement 'audit 30 min gratuit'"
- **CNIL < 9** : "Opt-out absent ou footer incomplet — appliquer template footer obligatoire"
