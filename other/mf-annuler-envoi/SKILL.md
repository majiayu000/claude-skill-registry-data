---
name: mf-annuler-envoi
description: Annuler un envoi de courrier papier déjà validé via l'API Merci Facteur (deleteEnvoi). Utiliser quand il s'agit d'annuler, supprimer, stopper, rappeler ou rembourser un courrier envoyé par erreur, d'implémenter une fenêtre d'annulation dans une application, ou de comprendre pourquoi une annulation n'a été que partielle. Couvre le contrat deleteEnvoi, l'irréversibilité de l'opération et les quatre issues possibles.
---

# Annuler un envoi — API Merci Facteur

`deleteEnvoi` annule un envoi et les courriers qu'il contient. **L'opération est irrémédiable** : un envoi annulé ne se restaure pas, et l'issue dépend de l'avancement du courrier dans la chaîne d'impression et de dépôt.

Base URL : `https://www.merci-facteur.com/api/1.2/prod/service`
Authentification : voir `mf-api-authentification`.

## 1. L'appel

**`DELETE /deleteEnvoi?idEnvoi=<entier>`**

| Paramètre | Emplacement | Type | Requis | Contenu |
|---|---|---|---|---|
| `ww-service-id` | en-tête | string | oui | le service ID |
| `ww-access-token` | en-tête | string | oui | un access token valide |
| `idEnvoi` | query | integer | oui | l'`envoi_id` retourné par `sendCourrier` |

Réponse en succès : `{"success": true}`
Réponse en échec (400 / 401) : `{"success": false, "error": {"code": "...", "text": "..."}}`

```js
const r = await fetch(
  `https://www.merci-facteur.com/api/1.2/prod/service/deleteEnvoi?idEnvoi=${idEnvoi}`,
  {
    method: "DELETE",
    headers: {
      "ww-service-id": SERVICE_ID,
      "ww-access-token": token,
    },
  }
);
const d = await r.json();
```

`idEnvoi` est l'`envoi_id` rendu par `sendCourrier`. Une intégration qui ne l'a pas stocké ne peut rien annuler : c'est la raison pratique de le persister systématiquement.

## 2. Les quatre issues

Un envoi n'est pas un objet figé : il est composé, imprimé, mis sous pli, puis déposé. `deleteEnvoi` intervient quelque part dans cette chaîne, et son effet réel dépend de l'endroit :

| Issue | Ce qui se passe |
|---|---|
| **Rejet immédiat** | L'envoi est trop avancé, rien n'est annulé. |
| **Rejet différé** | L'annulation est enregistrée mais ne prend pas effet tout de suite. |
| **Annulation partielle** | Une partie seulement des courriers est annulée ; la facturation est **partiellement** remboursée. |
| **Acceptation intégrale** | L'envoi entier est annulé. |

Trois conséquences pour l'intégration :

**Ne considère jamais `success: true` comme « le courrier ne partira pas ».** Un succès peut recouvrir une annulation partielle. Sur un envoi multi-destinataires en particulier, une partie des plis peut déjà être partie.

**N'affiche pas de montant remboursé calculé côté application.** Le remboursement est décidé par Merci Facteur selon l'avancement réel. Toute somme affichée à l'utilisateur avant confirmation est une promesse que l'API n'a pas faite.

**Vérifie l'état après coup plutôt que de le déduire.** Les webhooks et le suivi (`mf-preuves-courrier`) disent ce qui est réellement arrivé à chaque courrier. L'appel `deleteEnvoi` dit seulement que la demande a été prise en compte.

## 3. Le délai réel

Les courriers validés avant **17 h, du lundi au vendredi**, sont imprimés et postés le jour même. Une annulation demandée après ce point de bascule a peu de chances d'aboutir intégralement.

Si l'application doit offrir une fenêtre d'annulation à ses utilisateurs, la façon fiable de la garantir n'est pas `deleteEnvoi` : c'est de **retarder l'appel à `sendCourrier`**. Mets l'envoi en file d'attente côté application, laisse la fenêtre d'annulation s'écouler, puis appelle `sendCourrier`. Tant que l'appel n'a pas eu lieu, l'annulation est certaine, gratuite et instantanée.

`deleteEnvoi` est un filet de sécurité pour l'erreur constatée après coup, pas un mécanisme d'annulation garanti.

## 4. Ce qu'il faut demander avant d'appeler

`deleteEnvoi` détruit sans retour. Dans un agent, un script ou une automatisation, l'appel ne se déclenche jamais implicitement :

- **Confirme l'`idEnvoi` avec l'utilisateur** avant d'appeler, en rappelant ce que contient cet envoi (destinataires, nombre de courriers) si l'information est disponible.
- **N'annule jamais en boucle** sur une liste d'envois sans validation explicite de chaque élément, ou du lot en toute connaissance de cause.
- **N'appelle pas `deleteEnvoi` en réaction à un timeout** de `sendCourrier`. Un timeout laisse l'issue indéterminée : annuler un envoi dont on ignore s'il existe produit soit un échec, soit l'annulation d'un envoi qu'on voulait garder. Le traitement correct du timeout est dans `mf-envoi-courrier`, section 5.

## 5. Diagnostic

| Symptôme | Cause à vérifier |
|---|---|
| `401` | token expiré, ou `ww-service-id` absent à côté de `ww-access-token` |
| `400` | `idEnvoi` absent, non entier, ou n'appartenant pas à ce compte |
| `success: true` mais le courrier arrive quand même | annulation partielle, ou rejet différé — voir section 2 |
| Annulation systématiquement refusée | demande postérieure au dépôt La Poste — voir section 3 |
