---
name: mf-preuves-courrier
description: Récupérer les preuves d'un courrier envoyé via l'API Merci Facteur avec getProof — preuve de dépôt, avis de réception signé, preuve de téléchargement d'un recommandé électronique. Utiliser quand il s'agit de récupérer, télécharger, archiver ou afficher un AR, une preuve de dépôt ou un justificatif d'envoi, ou de savoir si un recommandé a été distribué.
---

# Preuves et suivi d'un courrier — API Merci Facteur

Un recommandé sans sa preuve ne vaut rien juridiquement. Ce document couvre la récupération des preuves et du suivi. L'envoi est dans `mf-envoi-courrier`, l'authentification dans `mf-api-authentification`.

Base URL : `https://www.merci-facteur.com/api/1.2/prod/service`
En-têtes sur tous les appels : `ww-service-id`, `ww-access-token`.

## 1. Quels envois produisent des preuves

Les preuves n'existent que pour les modes d'envoi qui en génèrent :

| `modeEnvoi` | Preuves récupérables par API |
|---|---|
| `normal` | **aucune** — la lettre verte n'a ni suivi ni preuve |
| `suivi` | preuve de dépôt |
| `lrar` | preuve de dépôt — **l'AR signé revient en papier à l'expéditeur, pas par l'API** |
| `lrare` | preuve de dépôt + AR numérisé, poussé par l'API |
| `ere_otp_mail`, `ere_otp_sms` | preuve de dépôt + preuve de téléchargement |

Si l'utilisateur veut archiver une preuve, ce choix se fait **au moment de l'envoi**, pas après. Un courrier parti en `normal` ne produira jamais de preuve, quelle que soit la suite.

**Le piège, c'est `lrar`.** C'est le recommandé que tout le monde nomme par réflexe, et son avis de réception arrive dans une boîte aux lettres physique. Une application qui doit archiver l'AR ou en déclencher quelque chose a besoin de **`lrare`** : même valeur juridique, AR numérisé et poussé par webhook. Si le code d'envoi utilise `lrar` et que le code de récupération attend un AR numérique, l'intégration ne marchera jamais — et ça se découvre des semaines plus tard.

## 2. Une preuve n'existe pas avant son événement

Une preuve apparaît quand l'événement qu'elle atteste a eu lieu :

- la **preuve de dépôt** après le dépôt effectif chez La Poste, donc au plus tôt le soir de l'impression ;
- l'**avis de réception** quand le destinataire signe, ce qui peut prendre des jours, ou ne jamais arriver ;
- la **preuve de téléchargement** d'un recommandé électronique quand le destinataire s'identifie et ouvre le document, ou jamais s'il ne le fait pas.

Deux conséquences :

**Ne récupère pas une preuve juste après `sendCourrier`.** Elle n'existe pas. Un appel immédiat échoue, et un code qui traite cet échec comme une erreur définitive est faux.

**Ne fais pas de polling.** Merci Facteur pousse chaque étape par webhook, sur l'URL déclarée dans l'onglet « API » de l'interface Merci Facteur Pro — y compris les événements `pdd` et `are` qui signalent qu'une preuve est prête, et la transportent (section 3). Tout se déclenche **en réaction à ces événements**, jamais dans une boucle. Le contrat complet des webhooks est dans `mf-envoi-courrier`, section 6.

## 3. Les preuves arrivent souvent toutes seules

**Avant d'écrire un appel à `getProof`, regarde les webhooks : deux d'entre eux transportent déjà le document.**

| Événement | `statut_courrier` | Champ | Contenu |
|---|---|---|---|
| `pdd` | `scan_pdd` | `detail[].pdd_base64_pdf` | le PDF de la preuve de dépôt, en base64 — courriers suivis et recommandés |
| `are` | `retour_are` | `detail[].are_base64_jpeg` | le JPEG de l'AR signé, en base64 — **`lrare` uniquement** |

Sur ces deux cas, l'intégration correcte est : recevoir le webhook, décoder le base64, stocker le fichier. **Aucun appel API.** Un agent qui écrit un `getProof` pour récupérer une preuve de dépôt réinvente un aller-retour dont il a déjà le résultat dans la requête qu'il vient de recevoir.

`getProof` sert dans trois cas seulement : la preuve de téléchargement d'un recommandé électronique (`document=telechargement`), la récupération d'une preuve perdue parce que le webhook a échoué ou n'était pas encore branché, et un rattrapage historique sur des envois antérieurs.

## 3 bis. Où trouver le numéro de suivi

`sendCourrier` retourne un `envoi_id`. Un envoi peut contenir plusieurs courriers — un par destinataire — et **chaque courrier a son propre numéro de suivi**. C'est ce numéro, pas l'`envoi_id`, que `getProof` attend.

Ne confonds pas les deux références que porte chaque courrier dans les webhooks :

| Champ | Exemple | Ce que c'est |
|---|---|---|
| `ref_courrier` | `123456-789123456` | la référence interne Merci Facteur du courrier |
| `tracking_number` | `2C123456789` | **le numéro de suivi La Poste — c'est lui que `getProof` attend** |
| `ref_interne` | `client_123` | ta propre référence, celle que tu as passée à l'envoi |

Passer `ref_courrier` à `getProof` échoue. C'est `tracking_number`.

**Le `tracking_number` apparaît à l'événement `printed`**, quand le courrier papier est imprimé. Il n'existe pas avant : l'événement `new` ne le porte pas. Il est également présent sur les événements suivants du cycle de vie (`pdd`, `are`, `delivered`…).

`tracking_number` vaut **`null`** pour un courrier parti en `normal` : la lettre verte n'a pas de suivi, donc pas de numéro, donc pas de preuve. Teste ce `null` avant d'écrire quoi que ce soit en base, plutôt que de découvrir des chaînes `"null"` six mois plus tard.

Stocke `tracking_number` à la réception de `printed`, associé à l'objet métier concerné. Un courrier dont le `tracking_number` n'a pas été conservé est un courrier dont on ne pourra plus récupérer la preuve par API.

> **N'implémente pas de boucle de polling pour découvrir les numéros de suivi.** Les webhooks sont la voie prévue. Si l'application ne peut vraiment pas exposer d'URL — et c'est une contrainte à remettre en cause avant de la contourner — demande au support technique de Merci Facteur plutôt que d'interroger l'API en boucle.

## 4. Récupérer une preuve

**`GET /getProof?trackingNumber=<string>&document=<string>`**

| Paramètre | Emplacement | Requis | Contenu |
|---|---|---|---|
| `ww-service-id` | en-tête | oui | le service ID |
| `ww-access-token` | en-tête | oui | un access token valide |
| `trackingNumber` | query | oui | le `tracking_number` du courrier (section 3 bis) |
| `document` | query | oui | `depot`, `reception` ou `telechargement` |

Les trois valeurs de `document` :

| Valeur | Document obtenu | Disponible pour |
|---|---|---|
| `depot` | preuve de dépôt | `suivi`, `lrar`, `lrare`, `ere_otp_mail`, `ere_otp_sms` |
| `reception` | avis de réception | `lrar`, `lrare` |
| `telechargement` | preuve de téléchargement | `ere_otp_mail`, `ere_otp_sms` |

N'essaie aucun autre libellé : il n'y en a pas trois autres à deviner.

### La réponse est en base64

Le document revient **encodé en base64**, accompagné d'un champ `format_return` qui indique son format réel (PDF ou JPEG). C'est ce `format_return` qui détermine l'en-tête à associer pour écrire le fichier sur disque ou l'afficher — ne présume pas le PDF.

```js
const r = await fetch(
  `https://www.merci-facteur.com/api/1.2/prod/service/getProof` +
    `?trackingNumber=${encodeURIComponent(ref)}&document=reception`,
  { headers: { "ww-service-id": SERVICE_ID, "ww-access-token": token } }
);
const d = await r.json();

const mime = {
  pdf: "application/pdf",
  jpeg: "image/jpeg",
  jpg: "image/jpeg",
}[String(d.format_return).toLowerCase()];

if (!mime) throw new Error("format_return inattendu : " + d.format_return);

// Écriture sur disque
await fs.writeFile(`preuve-${ref}.${d.format_return}`, Buffer.from(d.document, "base64"));

// Ou affichage / téléchargement côté client
// `data:${mime};base64,${d.document}`
```

Trois erreurs à éviter :

- **Coder en dur `application/pdf`.** Un avis de réception numérisé peut revenir en JPEG. Lis `format_return`.
- **Réencoder le base64.** Le champ est déjà encodé : il se décode, il ne se traite pas comme du texte.
- **Servir la preuve au navigateur en la re-téléchargeant à chaque affichage.** Décode une fois, stocke le fichier (section 5), sers-le depuis ton stockage.

## 5. Archiver, pas seulement afficher

Une preuve a une valeur juridique : elle sert à démontrer, plus tard et devant un tiers, qu'un courrier a été déposé ou reçu. Deux règles pratiques :

**Stocke le fichier, pas un lien.** Une URL de preuve peut expirer ou changer. L'intégration qui a besoin de la preuve dans deux ans doit détenir le fichier, dans son propre stockage, associé à l'objet métier concerné (contrat, litige, résiliation, relance).

**Enregistre la date de récupération et le numéro de suivi à côté du fichier.** Un PDF de preuve isolé, sans le contexte de l'envoi auquel il se rattache, n'est pas exploitable.

## 5 bis. Lire un statut

Chaque entrée de webhook porte `statut_courrier` (le code) et `statut_description` (le texte lisible). Les codes qui décident d'une bifurcation métier :

**Courriers papier**

| Code | Événement | Ce que ça veut dire |
|---|---|---|
| `wait` | `new` | en attente d'impression — annulation encore possible |
| `imprime` | `printed` | imprimé, posté sous peu — **porte le `tracking_number`** |
| `pris_en_charge` | `new-state` | pris en charge par La Poste |
| `attente_presentation` | `new-state` | en attente de distribution |
| `distribution_en_cours` | `new-state` | en cours de distribution |
| `attente_au_guichet` | `new-state` | avis de passage déposé, à retirer au bureau de poste |
| `probleme_en_cours` | `error` | La Poste rencontre un problème |
| `non_distribuable` | `error` | courrier non distribuable |
| `retour_expediteur` | `error` | retourné à l'expéditeur |
| `distribue` | `delivered` | **distribué au destinataire — fin d'acheminement** |
| `distribue_expediteur` | `pnd` | **revenu à l'expéditeur — fin d'acheminement, c'est le NPAI** |
| `archivage_pnd` | `pnd` | NPAI d'un `lrare` archivé chez Merci Facteur pour 3 ans |
| `retour_are` | `are` | AR numérisé disponible |
| `scan_pdd` | `pdd` | preuve de dépôt disponible |

Les envois internationaux ajoutent des statuts de transit et de douane (`entree_douane`, `sortie_douane`, `retenu_douane`, `transit_pays_intermediaire`, `traitement_pays_destination`, `prix_en_charge_pays_destinataire`). Ils sont informatifs : ne construis pas de logique métier dessus.

**Courriers électroniques**

| Code | Événement | Ce que ça veut dire |
|---|---|---|
| `wait` | `new` | en attente d'envoi |
| `envoye` | `sended` | envoyé au destinataire |
| `accept_wait` | `new-state` | en attente d'acceptation |
| `accept_lock` | `error` | bloqué 3 h après 6 échecs d'identification OTP |
| `accept_notification_error` | `error` | email erroné ou boîte pleine — **fin d'acheminement** |
| `accepted` | `delivered` | accepté et AR signé |
| `accepted_downloaded` | `delivered` | accepté, AR signé, et document téléchargé |
| `expired` | `pnd` | non accepté dans le délai imparti |
| `refused` | `pnd` | refusé par le destinataire |

**Trois règles pour coder contre ces statuts :**

- **Teste le code, pas la description.** `statut_description` est du texte lisible avec une date dedans, il change ; `statut_courrier` est stable.
- **Identifie les fins d'acheminement.** `distribue`, `distribue_expediteur`, `accept_notification_error`, `expired`, `refused` : au-delà, plus rien n'arrivera. C'est là qu'un processus en attente doit être débloqué, pas laissé en suspens indéfiniment.
- **Un `error` n'est pas toujours final.** `probleme_en_cours` peut être suivi de `probleme_resolu` et la distribution reprendre. Ne clôture pas un dossier sur le premier `error`.

## 6. Le cas NPAI

Un courrier peut revenir non distribué — NPAI, « n'habite pas à l'adresse indiquée ». C'est un événement poussé par webhook, et c'est le seul moyen de l'apprendre : aucune preuve ne sera produite, et l'absence de preuve n'est pas en soi un signal exploitable.

Une intégration qui envoie du recommandé sans écouter les webhooks ne saura jamais qu'un pli est revenu. Si l'utilisateur construit un flux de relance ou de mise en demeure, le traitement du NPAI n'est pas optionnel : c'est précisément le cas où le processus métier doit bifurquer.

## 7. Diagnostic

| Symptôme | Cause à vérifier |
|---|---|
| Aucune preuve disponible, envoi pourtant réussi | `modeEnvoi` à `normal` — voir section 1 |
| Preuve introuvable juste après l'envoi | l'événement n'a pas encore eu lieu — voir section 2 |
| `trackingNumber` refusé | `envoi_id` ou `ref_courrier` passé à la place de `tracking_number` — voir section 3 bis |
| `tracking_number` vide en base | courrier parti en `normal`, ou webhook `printed` non écouté |
| Appel `getProof` pour une preuve de dépôt | inutile : le webhook `pdd` la contient déjà — voir section 3 |
| `document=reception` refusé | l'envoi n'est pas un `lrar`/`lrare` — voir le tableau de la section 4 |
| Fichier écrit illisible | `format_return` ignoré, ou base64 réencodé au lieu d'être décodé |
| AR jamais disponible | le destinataire n'a pas signé, ou le pli est revenu en NPAI — voir section 6 |
| `401` | token expiré, ou `ww-service-id` absent à côté de `ww-access-token` |
