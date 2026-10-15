---
name: cobacam-meeting-minutes-creator
description: "Transforme des notes brutes de réunion COBACAM (AGO, AGE, CA, comité) en procès-verbal Word en français canadien, avec règles typographiques québécoises. Utiliser pour \"crée un PV\", \"transforme cette transcription en procès-verbal\", \"corrige la typographie de ce PV\"."
---

# COBACAM Meeting Minutes Creator

Transforme des notes de réunion COBACAM en procès-verbaux Word prêts à signer et archiver, en français canadien.

## Références (lire selon le besoin)

- `references/templates-pv.md`: templates AGO, AGE, CA, comité, exemples commentés. Lire avant de structurer.
- `references/typographie-francais-canadien.md`: majuscules, titres, traits d'union, ponctuation.
- `references/standards-proces-verbaux.md`: mentions obligatoires, valeur juridique, archivage, bonnes pratiques.
- `references/guide-cobacam.md`: terminologie, gouvernance et en-têtes propres à COBACAM.

## Processus

1. **Identifier le type**: AGO, AGE, CA ou comité. Relever date, heure, lieu (physique ou virtuel), présents et absents, ordre du jour, décisions et votes. Si une information manque, la demander avant de continuer.
2. **Structurer** selon le template du type: en-tête (COBACAM, type de document, date, lieu), ouverture (heure, président et secrétaire de séance, quorum), participants, approbation de l'ordre du jour et du PV précédent, points traités, clôture (heure, signatures). Pour chaque point: exposé ou discussion, proposition (proposé par, appuyé par), vote (pour, contre, abstentions, résultat) ou décision.
3. **Appliquer la typographie** (détail dans la référence typographie):
   - Majuscule au premier mot d'un titre et aux noms propres seulement: "Architecture des rôles de sécurité", jamais "Architecture des Rôles de Sécurité".
   - Toujours "procès-verbal" avec trait d'union, pluriel "procès-verbaux".
   - Présent de l'indicatif: "Le président ouvre la séance à 19h00."
   - Accents sur les majuscules.
4. **Rédiger** de façon neutre, factuelle et chronologique, en phrases courtes, sans ambiguïté sur les décisions. Écrire "Le conseil d'administration approuve le budget 2025 à l'unanimité", pas "on a dit oui". Attribuer les propositions: "Mme Marie Dubois propose...". Les discussions houleuses se résument à l'issue ("Après discussion approfondie, le conseil adopte la proposition"), sans détailler les tensions.
5. **Générer le Word**: marges 2,54 cm, Arial ou Calibri 11-12 pt, interligne 1,15 ou 1,5, pagination "Page X de Y", titres en gras, points numérotés, lignes de signature en fin de document, pied de page "Rédigé par: [secrétaire de séance]". Nom de fichier: `PV_COBACAM_[TYPE]_AAAA-MM-JJ.docx`.
6. **Valider avant de présenter**: voir la checklist ci-dessous.

## Cas particuliers

- **Procurations**: noter présents, procurations valides, total des droits de vote et quorum (ex. 15 + 5 = 20, quorum 50 % + 1 = 11).
- **Amendements**: proposition initiale, amendement et son proposeur, vote sur l'amendement, proposition amendée, vote final.
- **Correction d'un PV existant**: analyser le document, corriger majuscules et terminologie, retourner la version corrigée.
- **Archivage électronique**: PDF/A pour la conservation longue durée, métadonnées complètes. **Diffusion**: version allégée possible, décisions officielles toujours conservées.

## Checklist finale

- [ ] En-tête, date, heure, lieu complets
- [ ] Liste exhaustive des participants
- [ ] Tous les points de l'ordre du jour traités
- [ ] Décisions et votes documentés avec résultats
- [ ] Typographie canadienne, trait d'union, présent de l'indicatif, ton neutre
- [ ] Numérotation des pages et espace pour signatures

## Règles non négociables

- Ne jamais inclure d'information sensible sans autorisation. Demander confirmation avant d'inclure un élément délicat.
- Le PV est signé par le président et le secrétaire de séance, puis approuvé à la réunion suivante. Il est archivé de façon permanente (registre physique et copie électronique).
