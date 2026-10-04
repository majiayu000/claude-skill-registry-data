---
name: mf-envoi-courrier
description: Envoyer un vrai courrier papier — lettre PDF, carte illustrée (carte postale, carte pliée, carte carrée, carte géante), suivi, recommandé avec accusé de réception, recommandé électronique eIDAS — depuis une application, via l'API Merci Facteur. Utiliser dès qu'il s'agit d'envoyer, poster, imprimer ou expédier du courrier physique depuis du code, d'envoyer une carte depuis une application, de brancher un envoi postal sur un événement, un formulaire, un cron ou un webhook, ou de déboguer un appel sendCourrier. Couvre le contrat exact, les pièges de nommage qui font échouer l'appel, l'idempotence et le comportement en cas d'échec.
---

# Envoyer un courrier papier — API Merci Facteur

L'API Merci Facteur imprime et poste un vrai courrier via La Poste depuis une application. Ce document décrit **la capacité d'envoi**, pas l'architecture : formulaire, tâche planifiée, réaction à un événement, webhook — c'est le besoin de l'utilisateur qui décide, pas ce document. N'invente aucun écran, aucun formulaire, aucun déclencheur qui n'a pas été demandé.

Un envoi tient en deux appels : un token (skill `mf-api-authentification`), puis `sendCourrier`. Tout le reste de ce document traite de ce qui fait échouer les intégrations.

Base URL : `https://www.merci-facteur.com/api/1.2/prod/service`

## 1. Avant d'écrire une ligne

**Chaque appel réussi coûte de l'argent et produit un objet physique irrécupérable.** Un courrier posté ne se rappelle pas. Une boucle accidentelle produit de vrais courriers facturés. Cette contrainte gouverne les sections 4 et 5, qui sont la partie que la plupart des intégrations ratent.

**La secret key ne quitte jamais le serveur.** Voir `mf-api-authentification`, section 1. Si l'utilisateur demande un appel depuis du code front, refuse et propose le composant serveur correspondant.

**Ne « corrige » aucun nom de champ.** Plusieurs sont contre-intuitifs et échouent si on les normalise :

| Piège | Règle |
|---|---|
| `adress` | Un seul « d ». Ce n'est pas `address`. |
| `print_sides` | Avec un « s » final, et **dans `content.letter`**, pas à la racine. |
| `adress` et `content` | Des **chaînes JSON**, dans un corps `application/x-www-form-urlencoded`. Pas des objets imbriqués. |
| Tableaux vides | Interdits. Le vide s'écrit `""`. Un `[]` déclenche `LETTER_INVALID_FILES` ou `LETTER_INVALID_BASE64_FILES`. |
| Adresses | Toutes les clés présentes, les inutilisées à `""`. Sinon `INFO_ADDRESS_MISSING`. |
| `dateEnvoi` | Une date complète `AAAA-MM-JJ`, ou le champ totalement absent. Sinon `INVALID_DATE_ENVOI`. |
| PDF | En base64 de préférence, pas en URL. |

**Quand le courrier part réellement.** Validé avant **17 h du lundi au vendredi** → imprimé et posté le jour même. Validé le samedi, le dimanche ou un jour férié → le jour ouvrable suivant. `dateEnvoi` programme un envoi à une date ultérieure précise.

Ça compte pour deux raisons : une application qui promet « votre courrier part aujourd'hui » à 18 h ment, et une fenêtre d'annulation offerte à l'utilisateur ne peut être garantie qu'en retardant l'appel à `sendCourrier` (voir `mf-annuler-envoi`).

## 2. L'appel

**`POST /sendCourrier`**

En-têtes : `ww-access-token`, `ww-service-id`.
Corps : `application/x-www-form-urlencoded`.

| Champ | Contenu |
|---|---|
| `idUser` | entier — l'utilisateur au nom duquel part le courrier |
| `adress` | chaîne JSON : `{"exp":{…},"dest":[{…}]}` |
| `content` | chaîne JSON, voir section 3 |
| `modeEnvoi` | voir le tableau ci-dessous |
| `dateEnvoi` | facultatif, `AAAA-MM-JJ` complet, date non passée |
| `designation` | facultatif, 50 caractères max — voir section 3 bis |
| `antidoublon` | facultatif, 200 caractères max, voir section 4 |
| `gestionNpai`, `anonymize`, `enveloppe` | facultatifs, voir section 3 bis |

**Les modes d'envoi**, et ce qu'ils changent réellement :

| `modeEnvoi` | Ce que c'est | Suivi | Preuves |
|---|---|---|---|
| `normal` | lettre verte | aucun — `tracking_number` reste `null` | aucune |
| `suivi` | suivi simple, date de réception connue, **sans valeur légale** | oui | preuve de dépôt |
| `lrar` | recommandé AR, valeur légale — **l'AR signé revient à l'expéditeur en papier** | oui | preuve de dépôt |
| `lrare` | recommandé AR, valeur légale — **l'AR est numérisé et mis à disposition par l'API** | oui | preuve de dépôt + AR numérisé |
| `ere_otp_mail` | recommandé électronique eIDAS, code de vérification par email | — | preuve de dépôt + preuve de téléchargement |
| `ere_otp_sms` | recommandé électronique eIDAS, code de vérification par SMS | — | preuve de dépôt + preuve de téléchargement |

Deux arbitrages que l'utilisateur doit trancher, pas toi :

- **`lrar` ou `lrare`** — c'est la même valeur juridique. `lrar` renvoie l'AR papier dans une boîte aux lettres ; `lrare` le numérise et le pousse dans l'application. Dès qu'un logiciel doit archiver ou réagir à l'AR, c'est `lrare`. Ne choisis pas `lrar` par défaut « parce que c'est le recommandé classique ».
- **`suivi` n'a pas de valeur légale.** Si l'utilisateur parle de mise en demeure, de résiliation, de préavis ou de délai opposable, `suivi` ne convient pas, quel que soit son coût. Dis-le au lieu de le laisser choisir dans le vide.

Réponse :

```json
{
  "success": true,
  "envoi_id": 123,
  "price": { "total": { "ht": 0, "ttc": 0 } },
  "resume": { "nb_dest": 1, "nb_page": 2 }
}
```

En cas d'échec : `{"success":false,"error":…}`.

**Conserve `envoi_id`.** C'est la seule clé qui permettra ensuite d'annuler l'envoi (`mf-annuler-envoi`) ou d'en récupérer les preuves (`mf-preuves-courrier`). Un envoi dont l'`envoi_id` n'a pas été stocké est un envoi qu'on ne peut plus ni suivre ni annuler.

## 3. Le contenu

```json
{
  "letter": {
    "files": "",
    "base64files": ["<pdf en base64>"],
    "print_sides": "recto",
    "final_filename": "contrat-2026"
  },
  "photo": "",
  "card": ""
}
```

Le vide s'écrit `""` à **tous** les niveaux, jamais `[]` ni `null` :

- pas de photo, pas de carte → `"photo": ""`, `"card": ""` ;
- lettre en base64 → `"files": ""`, `"base64files": ["…"]` ;
- lettre par URL → `"files": ["https://…"]`, `"base64files": ""`.

`print_sides` vaut `recto`, `rectoverso` ou `distinctrectoverso` (recto-verso en insérant une page blanche après les fichiers au nombre de pages impair). `final_filename` est un libellé sans extension, 50 caractères maximum.

Format : PDF uniquement, jusqu'à 10 fichiers par lettre, 50 Mo par fichier.

### Base64 plutôt qu'URL

Les deux modes existent, mais **le base64 est le mode fiable**. Une URL signée de stockage n'est pas toujours téléchargeable par les serveurs de Merci Facteur, et l'échec survient de leur côté, après coup — donc difficile à diagnostiquer depuis l'application.

Récupère le PDF depuis ton propre serveur, encode-le, envoie-le dans `base64files`. Le base64 ne contient ni retour à la ligne, ni préfixe `data:application/pdf;base64,`, ni marqueur de fin.

Le base64 gonfle le volume d'environ 33 % et transite dans le corps de la requête : au-delà de quelques mégaoctets, bascule sur `files` avec une URL **publique et non signée**.

Attention à l'encodage lui-même : sur la plupart des runtimes, convertir un tampon d'octets en base64 en une seule passe fait déborder la pile d'appels dès quelques centaines de kilo-octets. Encode par tranches, ou utilise la fonction native du langage qui gère les gros volumes.

### Envoyer une carte illustrée

`content.card` remplace `content.letter` quand le courrier est une carte — papier épais 350 g, de la carte postale à la carte géante A4.

```json
{
  "letter": "",
  "photo": "",
  "card": {
    "format": "postcard",
    "visuel": { "type": "base64", "value": "<jpeg en base64>" },
    "text":   { "type": "base64", "value": "<jpeg en base64>" },
    "coin": "carre",
    "papier": "classic"
  }
}
```

`visuel` est la face illustrée, `text` la face imprimée du message. Les deux sont des **images** : `base64` (fiable) ou `customimg` (URL publique). JPEG uniquement, 4 Mo maximum, jamais de PDF ni de PNG.

**Le dos ne s'envoie pas en HTML.** L'API accepte `text.type: "html"` ; ne l'utilise pas et ne le propose pas. Le rendu échappe à l'application — texte qui déborde, police substituée, césure imprévue — et rien ne le signale : la carte part à l'impression et elle est facturée telle quelle. Compose le dos côté application, rends-le en image, envoie l'image. C'est aussi ce qui permet de montrer à l'utilisateur ce qu'il va poster.

Corollaire : **les classes PHP publiées par Merci Facteur ne conviennent pas pour les cartes**, v1 comme v2 forcent `text.type = 'html'`. Écris l'appel directement.

Trois pièges de nommage qui font échouer l'appel :

| Piège | Règle |
|---|---|
| `visuel` | En français. Ce n'est pas `visual`. `coin` et `papier` aussi, à côté de `format` et `text` en anglais. |
| `format` | `postcard`, `classic`, `folded`, `square`, `large`, `large-a4`. **`square` (carte carrée, 14 × 14 cm) manque à la spec OpenAPI publiée** : l'API l'accepte, mais un client généré depuis la spec le rejette. L'enum contient aussi `naked-postcard` (sans enveloppe) : ne la propose pas, la carte voyage à nu et arrive abîmée. |
| `coin`, `papier` | `carre`/`arrondi`, `classic`/`nacre`/`creation`. Ni traduits, ni inventés — et ils changent le prix, donc ils se demandent à l'utilisateur. |

Dimensions finies, enveloppe par format, contraintes d'image et recadrage : `references/cartes.md`. À lire avant la première série, en particulier pour `square`, dont le ratio 1 contredit la proportion 0,71 exigée des fichiers, et pour les formats pliés, dont la zone utile n'est pas publiée.

### Les adresses

L'expéditeur et chaque destinataire sont écrits **en clair, directement dans l'appel**. Les adresses restent dans la base de l'application appelante ; `sendCourrier` les reçoit à chaque envoi. Rien n'est à créer au préalable côté Merci Facteur.

```json
{
  "exp": {
    "civilite": "Mme",
    "nom": "Dupont",
    "prenom": "Sophie",
    "societe": "Dupont Corp.",
    "adresse1": "9 allée de la Rose",
    "adresse2": "",
    "adresse3": "",
    "cp": "78000",
    "ville": "Versailles",
    "pays": "france",
    "email": ""
  },
  "dest": [
    {
      "civilite": "Monsieur",
      "nom": "Martin",
      "prenom": "Joël",
      "societe": "",
      "adresse1": "33 allée de la Pâquerette",
      "adresse2": "Entrée B",
      "adresse3": "",
      "cp": "75015",
      "ville": "Paris",
      "pays": "france",
      "phone": "",
      "email": "",
      "consent": 0,
      "reference": "ref-client-1"
    }
  ]
}
```

**Les clés ne s'omettent pas.** Renseigne `civilite`, `nom`, `prenom`, `societe`, `adresse1`, `adresse2`, `adresse3`, `cp`, `ville`, `pays`, et mets `""` sur celles qui ne servent pas. Une adresse partielle est rejetée avec `INFO_ADDRESS_MISSING`, même si la clé manquante est facultative sur le papier.

Obligatoires et **non vides** : `nom` **ou** `societe`, `cp`, `ville`, `pays`.

`dest` est toujours un **tableau d'objets**, même pour un seul destinataire.

**Le pays doit avoir une orthographe conforme.** La liste fait autorité côté API et se récupère avec **`GET /getCountry`** — c'est la source à interroger en cas de doute, parce qu'elle ne périme pas. `references/pays.md` en contient une copie, pratique mais figée. N'invente aucun libellé, ne traduis rien.

Limites de caractères : civilité 12, société 90, nom 70, prénom 70, lignes d'adresse 90 chacune, code postal 12, ville 70, pays 70. `reference` : 30 caractères maximum, chiffres, lettres, espaces, `-` et `_` uniquement.

Plusieurs destinataires dans un même `dest` produisent **le même courrier** envoyé à chacun : un envoi, plusieurs courriers, un seul `envoi_id`.

Un recommandé électronique (`ere_otp_mail`, `ere_otp_sms`) exige en plus :

- `email` (canal `ere_otp_mail`) ou `phone` (canal `ere_otp_sms`) **sur l'expéditeur comme sur chaque destinataire** — c'est l'oubli le plus fréquent, parce qu'une adresse d'expéditeur reprise d'un envoi papier n'en contient jamais ;
- `consent: 1` sur chaque destinataire, en entier et non en booléen. Le consentement n'est pas requis pour un destinataire professionnel, mais le champ reste attendu.

**Remplis `reference` sur chaque destinataire.** C'est ta propre référence interne, et elle revient dans tous les webhooks sous le nom `ref_interne`, dans les exports CSV, et sur un recommandé avec AR elle est **imprimée sur l'accusé de réception** retourné.

C'est ce qui rattache un courrier à l'objet métier qui l'a déclenché — une facture, un contrat, un dossier — sans table de correspondance à maintenir. Une intégration qui la laisse vide reçoit des webhooks qu'elle ne sait pas relier à quoi que ce soit. Mets-y l'identifiant que l'application utilise déjà.

## 3 bis. Quatre options facultatives

Elles ne sont pas dans le corps de l'appel par défaut, et elles résolvent chacune un problème que l'utilisateur exprime souvent sans savoir qu'une option existe. Ne les ajoute pas d'office : reconnais le besoin, puis lis `references/options-envoi.md` pour le contrat exact.

| Le besoin exprimé | L'option |
|---|---|
| « je veux savoir quand un courrier revient », adresse fausse, relance à suspendre | `gestionNpai` — le pli non distribué revient chez Merci Facteur, est numérisé, et remonte par webhook (modes `normal` et `suivi` ; pour un recommandé c'est le mode `lrare`) |
| RGPD, rétention, données sensibles, DPO | `anonymize` — supprime contenu et/ou adresses des serveurs, 1 à 40 jours après impression |
| logo de l'expéditeur, enveloppe à l'image de l'entreprise, charte, branding | `enveloppe` — enveloppe personnalisée créée dans « Votre branding », désignée par son ID. **C'est la voie du logo expéditeur** |
| « je dois retrouver ce courrier dans l'interface » | `designation` — 50 caractères, libellé de recherche ; **visible par le destinataire** sur un envoi ERE |

## 4. `antidoublon` — la décision structurante

`antidoublon` accepte une référence unique de ton choix, 200 caractères maximum. Si un second `sendCourrier` arrive avec la **même** valeur dans les 30 jours glissants, l'API retourne une erreur au lieu de produire un second courrier.

Le champ est facultatif, mais il détermine la stratégie de reprise de toute l'intégration :

- **sans** : aucune reprise automatique sûre n'est possible ;
- **avec** : un envoi dont l'issue est inconnue peut être rejoué à l'identique sans risque.

La valeur doit identifier **le courrier**, pas la tentative : elle reste identique d'un essai à l'autre. Un numéro de facture plus un numéro de relance, un identifiant de contrat, l'identifiant d'une ligne en file d'attente conviennent. **Un UUID régénéré à chaque tentative ou un horodatage ne protègent de rien** — c'est l'erreur classique.

Si aucune référence stable n'existe côté métier, omets le champ. N'en fabrique pas une.

## 5. Que faire quand ça échoue

Chaque appel réussi imprime et poste un courrier facturé. Un second appel identique produit un second courrier. Trois situations, trois traitements :

| Ce qui s'est passé | Le courrier est-il parti ? | Que faire |
|---|---|---|
| L'API répond `success: false` | Non, avec certitude | Corriger et réessayer sans risque |
| Échec **avant** `sendCourrier` (validation locale, token en échec) | Non, avec certitude | Réessayer sans risque |
| Timeout, coupure réseau, réponse illisible **pendant** `sendCourrier` | **Indéterminé** | Dépend d'`antidoublon` |

La troisième ligne est la seule qui compte. Un timeout ne signifie pas que l'envoi a échoué : la requête a pu aboutir côté Merci Facteur et la réponse se perdre au retour.

- **Avec `antidoublon`** : rejoue à l'identique, même valeur. Le second appel est refusé si le premier était passé. Trois tentatives espacées suffisent.
- **Sans `antidoublon`** : ne réessaie jamais automatiquement. Marque l'envoi « à vérifier », sors-le de la file, laisse un humain trancher depuis l'interface Merci Facteur Pro.

Codes d'erreur les plus fréquents et leur cause réelle :

| Code | Cause |
|---|---|
| `LETTER_INVALID_FILES`, `LETTER_INVALID_BASE64_FILES` | un `[]` là où il fallait `""` |
| `INFO_ADDRESS_MISSING` | une clé d'adresse absente, même facultative |
| `INVALID_DATE_ENVOI` | `dateEnvoi` vide ou tronquée |

## 6. Contraintes à respecter, quel que soit le déclencheur

**Le déclencheur n'appartient pas à l'appel.** Écris l'envoi comme une fonction ou un point d'entrée unique, sans hypothèse sur son appelant. C'est ce qui permet de brancher ensuite ce que l'utilisateur veut sans retoucher la partie API.

**Un envoi ne se rejoue pas librement.** Il n'existe aucun moyen de vérifier après coup si un envoi donné est passé. Toute forme de déclenchement répétable — retry, cron qui repasse, événement rejoué, double clic — doit soit porter un `antidoublon` stable, soit être empêchée en amont.

**Un envoi déclenché sans témoin doit laisser une trace.** Un envoi lancé par un système n'a personne pour constater son échec. Conserve au minimum l'`envoi_id` retourné, ou l'erreur, associés à ce qui a déclenché l'envoi.

**Le volume se plafonne.** Prévois une limite par période et un refus au-delà.

**Le temps d'exécution compte.** Encoder un PDF en base64 puis le transmettre prend du temps. Sur une plateforme à timeout court, traite un envoi par invocation plutôt qu'un lot.

### Recevoir l'état des courriers : les webhooks

`sendCourrier` ne dit rien de ce qui arrive ensuite au courrier. **Les webhooks sont la seule voie de retour.** Une intégration qui envoie sans les écouter ne saura jamais qu'un pli est revenu en NPAI, qu'un recommandé a été signé, ni qu'une preuve est disponible.

L'URL de notification se déclare dans l'onglet « API » de l'interface Merci Facteur Pro. La même page permet de déclencher chaque événement en test et de consulter l'historique des webhooks envoyés.

**Les événements :**

| Événement | Signifie |
|---|---|
| `new` | courrier(s) créé(s) |
| `printed` | courrier(s) papier imprimé(s) — **porte le `tracking_number`** |
| `sended` | courrier(s) électronique(s) envoyé(s) |
| `new-state` | nouveau statut |
| `delivered` | arrivé chez le destinataire |
| `error` | erreur de distribution |
| `pnd` | pli non distribuable (NPAI) |
| `are` | avis de réception électronique disponible — **contient l'AR en base64** |
| `pdd` | preuve de dépôt disponible — **contient la preuve en base64** |

**La charge utile** arrive en POST avec deux objets : `event` (`name_event`, `id_user`, `date_event`) et `detail`, un tableau des courriers concernés. Un webhook ne porte qu'un seul type d'événement, mais peut concerner plusieurs courriers.

Chaque entrée de `detail` contient l'adresse du destinataire, `mode_envoi`, `id_envoi`, `statut_courrier`, `statut_description`, et **trois références à ne pas confondre** :

- `ref_courrier` — la référence interne Merci Facteur (`123456-789123456`) ;
- `tracking_number` — le numéro de suivi La Poste (`2C123456789`), **`null` en mode `normal`** ;
- `ref_interne` — la référence que tu as toi-même passée à l'envoi.

`tracking_number` est celui qu'attend `getProof` (skill `mf-preuves-courrier`). C'est la raison pratique d'écouter `printed` même quand on ne suit rien d'autre.

**Vérifier l'origine.** Les webhooks partent de plusieurs IP : le filtrage par IP ne fonctionne pas. Merci Facteur envoie une clé dans l'en-tête **`X-Mf-Webhook-Secret-Key`**, à récupérer dans l'onglet « API » du compte. Compare-la en temps constant, et rejette la requête si elle ne correspond pas. N'applique pas l'authentification applicative à cet endpoint : il n'est pas appelé par un utilisateur connecté.

**Répondre 200.** L'endpoint doit retourner un statut 200 avec un corps de moins de 500 caractères. En cas d'échec, Merci Facteur réessaie **deux fois** : 60 minutes après la première tentative, puis 24 h après la seconde. Au-delà, l'événement est perdu.

Deux conséquences sur la conception de l'endpoint :

- **Réponds vite, traite après.** Enregistre la charge utile et réponds 200 ; fais le travail lourd (décodage base64, écriture en stockage, notification) en arrière-plan. Un traitement long dans la requête provoque un timeout, donc une relance, donc un doublon.
- **Rends le traitement idempotent.** Trois tentatives sur le même événement doivent produire un seul effet. Déduplique sur le couple (`name_event`, `ref_courrier`).

## 7. Fichiers de référence

- `references/implementations.md` — implémentations complètes et testables en JavaScript/TypeScript, PHP, Python, et les notes pour les outils no-code (n8n, Make, Zapier).
- `references/cartes.md` — le contrat exact de `content.card` : les formats et leurs dimensions, papiers, coins, contraintes d'image et recadrage.
- `references/options-envoi.md` — le contrat exact de `gestionNpai`, `anonymize`, `enveloppe` et `designation`.
- `references/pays.md` — copie de la liste des valeurs acceptées par `pays`. En cas de doute, `GET /getCountry` fait autorité et ne périme pas.

Charge-les seulement quand tu en as besoin : le contrat des sections 2 et 3 suffit pour écrire l'appel.
