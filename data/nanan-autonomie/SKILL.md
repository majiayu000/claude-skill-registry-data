---
name: nanan-autonomie
description: Apprend à Nanan, l'assistante KLASSCI, une opération qu'on vient de faire à la main pour une école (CLI, SQL, tinker, écran détourné), pour qu'elle la refasse seule la fois suivante. À utiliser dès qu'une demande d'école se règle par une manipulation manuelle, avant de rendre la main, et avant tout déploiement qui touche la CLI ou routes/. Couvre l'outil de lecture, l'action « proposer puis Valider », les droits, le prompt, la séance d'entraînement, le registre de couverture, les tests et le déploiement.
---

# Nanan autonome

## Le défaut que ce skill supprime

Une école écrit « ajoute une classe de 60 places partout », « délie cette UE de LPA », « elle n'est pas dans les arriérés, enlève sa dette ». On le fait à la main, en CLI ou en SQL, et c'est fini pour aujourd'hui. Le mois suivant, la même demande revient, et quelqu'un la refait à la main. L'école reste dépendante de nous.

**Une opération faite à la main pour une école n'est terminée que lorsque Nanan sait la refaire.**

## Quand l'appliquer

- Une opération d'écriture faite pour une école par la CLI (`klassci …`, `/api/cli/*`), en SQL, en tinker, ou en contournant un écran.
- Une nouvelle route d'écriture sous `/api/cli` : `bin/verifier-couverture-nanan.php` la refusera tant qu'elle n'est pas déclarée.
- Avant de rendre la main sur une demande d'école : relire ce qu'on a fait de la journée, opération par opération.

Ne s'applique PAS à l'exploitation (déploiement, migrations, cache), aux données de démonstration, ni aux comptes et droits. On les déclare `hors_nanan` avec la raison, on ne les apprend pas.

## Le parcours, dans l'ordre

### 1. Décrire l'opération comme une école la demanderait

Une phrase, avec les mots de l'école : « Passe les classes de 1re année à 60 places. » Noter ce qu'il faut savoir avant d'agir (quelle classe, combien de places), ce qui peut mal tourner (moins de places que d'inscrits), et ce qui reste une décision humaine (le motif d'une exonération).

### 2. Un outil de LECTURE, s'il manque

Nanan doit pouvoir constater avant d'agir : `search_classes`, `diagnostiquer_reinscription`, `chercher_dans_piece`. Un outil de lecture hérite de `App\Services\Chatbot\Tools\ChatbotTool`. Il rend `results` (ce que voit l'écran) et `diagnostic` (ce que lit le raisonnement : identifiants, cause, verdicts). Le `diagnostic` passe par `ResumeOutil`, plafonné à 6 000 octets : **les verdicts passent d'abord, en entier**. Un résumé coupé ne doit jamais se lire comme une absence.

### 3. Une ACTION « proposer, puis Valider »

`App\Domain\Assistant\Actions\ActionAgent`, dans `app/Domain/Assistant/Actions/<Domaine>/`. Modèles : `AjouterClasses`, `ModifierClasses`, `LierUeAuxParcours`, `AjusterMontantSouscription`.

- `preparer()` n'écrit RIEN. Elle rend une `Proposition` : un tableau avant/après, des `manques` (ce qu'il faut demander, jamais deviné), des `avertissements`, des `donnees` (ce qui sera écrit) et un `etat` (l'instantané qui rend la proposition périmée s'il bouge).
- `executer()` reverrouille, compare l'`etat`, lève `PropositionPerimee` si quelque chose a changé, puis écrit **par le même chemin que l'écran ou la CLI** : un service partagé, jamais une seconde implémentation.
- Les mêmes gardes que l'écran : permissions, plafonds, audit, motif. Une règle qui n'existe que dans l'action est une règle que l'écran n'applique pas.

### 4. Brancher

- `config/assistant.php` → `actions.classes` : la classe de l'action.
- `config/chatbot.php` → `tools` : `proposer_<cle>` avec ses permissions, **les mêmes que la route de l'écran**, plus un `libelle` et une `suggestion`.
- `ConstructeurDePrompt` : une ligne de mode opératoire (quand l'utiliser, ce qu'il faut demander, ce qu'il ne faut jamais supposer).
- `resources/data/nanan-couverture.php` : la route CLI correspondante passe de `a_apprendre` à `nanan`.

### 5. La séance d'entraînement

Un test qui prouve le parcours de bout en bout, sur le modèle de `tests/Feature/Assistant/ActionsDuJourTest.php` :

- `executeAuthorized()` puis `valider()` : rien n'est écrit avant « Valider », tout l'est après ;
- chaque `manque` et chaque refus : sans le nombre de places, Nanan le demande ; sous les inscrits, il refuse ;
- la vraie boucle (`BoucleAgent`), le vrai catalogue et le vrai prompt, avec un modèle scripté (`FauxFournisseur`) qui suit le mode opératoire.

Puis **retirer le correctif et relancer** : un test qui reste vert sans le correctif ne prouve rien.

### 6. Contrôles avant de pousser

```bash
php bin/verifier-couverture-nanan.php      # chaque route d'écriture déclarée
php artisan test --filter='ActionsDuJourTest|<ta classe>'
sh .githooks/pre-commit --arbre            # pièges Blade
```

Le hook `pre-push` relance la couverture dès qu'un push touche `routes/`, la CLI, `config/chatbot.php` ou le registre. La CI la rejoue (étape « Couverture Nanan »).

### 7. Revue, puis déploiement

- Revue thermo-nucléaire en sous-agent (commandement 0 de `pre-merge-checklist.md`). `BLOCK` : on corrige avant de fusionner.
- Entrée au `CHANGELOG.md` : ce que Nanan sait faire de plus, du point de vue de l'école.
- Fusion par PR, déploiement sur presentation (`/api/cli/pull`, puis `cache/clear`, puis `permissions/sync`), capture réelle du chat, puis propagation aux écoles.

## Faire le point d'une journée

Avant de rendre la main, lister les opérations d'écriture faites à la main dans la session, et pour chacune répondre :

| opération | outil de lecture | action | test d'entraînement | registre |
|---|---|---|---|---|

Une case vide est du travail restant, pas une remarque. `php bin/verifier-couverture-nanan.php --a-apprendre` donne le reste à apprendre côté CLI.

## Anti-patterns

1. ❌ Clore une demande d'école réglée en CLI ou en SQL sans rien apprendre à Nanan.
2. ❌ Une action qui écrit dans `preparer()`, ou qui écrit sans comparer l'`etat`.
3. ❌ Une action qui réimplémente l'écriture de l'écran au lieu d'appeler le même service.
4. ❌ Des permissions d'outil différentes de celles de la route de l'écran.
5. ❌ Supposer une valeur que la personne doit donner (places, montant, motif) au lieu de la mettre en `manques`.
6. ❌ Déclarer `hors_nanan` une opération d'école pour faire passer le contrôle : c'est `a_apprendre`.
7. ❌ Un résumé d'outil qui peut couper un verdict.
8. ❌ Annoncer « Nanan sait le faire » sans séance d'entraînement qui passe, et qui échoue sans le correctif.
