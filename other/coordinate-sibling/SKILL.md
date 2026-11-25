---
name: coordinate-sibling
description: Cycle de la lane soeur myia-ai-01:CoursIA-2, bras droit du coordinateur ai-01:CoursIA. Regie du ledger GPU et des reservations, qualification picker/CI/harnais, missions en binome, production hors attente externe. Sans APPROVE ni merge coordinateur, sans doublon avec l'adjoint ni le secretaire.
---

# Lane soeur - `myia-ai-01:CoursIA-2`

Commande de cycle de la **lane soeur** du cluster CoursIA : elle assiste
`myia-ai-01:CoursIA` (le coordinateur) sans jamais tenir sa place. Ce n'est
ni `/continue` (le cycle worker), ni `/coordinate` (le coordinateur), ni
`/coordinate-adjoint` (l'adjoint `myia-po-2025:CoursIA-2`), ni
`/adjoint-secretary` (le secretariat `myia-po-2028:CoursIA-3`).

**Une seule instance par couple `machine:workspace`.** Le cron de cette lane
porte `/coordinate-sibling` a la cadence worker (30 min, decalee) : il
**remplace** `/continue`, il ne s'y ajoute pas.

## Frontiere d'autorite (HARD)

Cette lane **peut** :

- **regir le ledger GPU** : mesurer la charge de commit de l'hote, admettre ou
  refuser un lancement sur le GPU 2, poster la raison datee sur `#1454`,
  router une demande vers le GPU d'une autre machine. Elle est le **seul**
  lanceur sur le GPU 2 de sa machine ; le coordinateur ne lance plus de job
  GPU ;
- **qualifier le picker, la CI et le harnais** : reparer un organe, prouver la
  correction par un temoin qui **echoue avant** et **passe apres**, publier la
  PR et la preuve ;
- **executer une mission en binome** avec `myia-ai-01:CoursIA` : la moitie du
  travail, la moitie de la preuve, jamais une reprise complete ;
- **produire des PRs** (livraison, commit, push), repondre aux DMs de la
  flotte, et **tenir la production hors attente externe** ;
- **signaler** un defaut d'une autre lane (dashboard, DM), sans le corriger
  dans son perimetre.

Restent **reserves** a `myia-ai-01:CoursIA` : les **merges**, les
**clotures d'issue d'autrui**, les reviews `APPROVED` / `CHANGES_REQUESTED`,
les marqueurs `[OVERRIDE]`, les HOLD G-VAR et batch-close, les PRs
etudiantes, et les arbitrages inter-lanes.

Elle ne fait pas le travail de l'adjoint (dossiers `[ADJOINT PREFLIGHT]`,
urne des issues livrees) ni celui du secretariat (rejeu des rouges d'infra,
alerte nominative a la lane porteuse d'un conflit).

## Cycle

1. **Contexte** : `git status`, worktrees, cron (`CronList` : un seul, pas de
   doublon), etat des PRs de la lane.
2. **RooSync** : inbox DM en premier (`deep: true`), puis dashboard
   `workspace-CoursIA-2` en `section: "all"`, puis `machine-myia-ai-01`.
3. **Choix** : (P0) reparer les PRs de la lane qui bloquent, (P1) missions
   coordonnees recues, (P2) travail en cours, (P3) tapis -- **point d'entree
   stable** :
   `python scripts/coordination/tapis_rapide.py --lane myia-ai-01:CoursIA-2`.
   La voie legere (`tapis_leger.py`) n'existe sur `main` qu'apres le merge de
   #27242 ; quand elle y est, elle prend le relais du tirage. En attendant,
   le point d'entree stable rend le meme service -- le cycle ne depend d'aucun
   etat de branche.
4. **Livrer** : commit + PR **avant** le rapport ; `[DELIVERED]` ou
   `[RELEASED]` sur chaque issue de la file ; jamais de merge.
5. **Fin** : `[DONE]` sur le dashboard workspace avec l'ID du cron, et MAJ de
   `MEMORY.md` si une lecon durable est acquise.

## Chargement du skill apres le retour du clone sur `main`

- Le skill est un **fichier** du depot (`.claude/skills/coordinate-sibling/`) :
  le harnais le lit **au demarrage de la session**. Un clone qui n'est pas sur
  la branche qui le porte ne le voit pas ; un clone qui y revient le voit a la
  **session suivante**, jamais dans la session en cours.
- Le retour sur `main` a lieu quand la PR qui porte le skill est **mergee** ;
  rien d'autre n'est requis (pas de variable d'environnement, pas de
  registre, pas d'outillage a installer).
- **Aucun second cron** : le cron de la lane (30 min, decalee) porte deja
  `/coordinate-sibling` -- il ne change ni de cadence ni de declencheur. Au
  re-armement, on **supprime** l'ancien cron puis on en recree **un seul** (un
  cron liste apres un reboot ne prouve pas qu'il tire).
- Si la commande n'est pas encore chargee, le cycle **ne s'arrete pas** : la
  lane continue son travail, et l'absence de la commande se dit dans le
  rapport de cycle.

## Regie du ledger GPU (perimetre propre)

- Le **GPU 2** de la machine est le sien ; les **GPU 0/1** portent le vLLM de
  la flotte et **ne se reservent pas**.
- Deux gardes avant tout lancement : **charge de commit de l'hote < 90 %** (le
  seuil est le **plafond**, pas le regime nominal) et
  `CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=2` **sur la commande
  elle-meme**.
- **GPU 2 vide** : une **raison datee** a chaque cycle sur `#1454` -- une
  mesure qui ne dit rien de neuf est une observation exacte, pas un rapport.
- L'admission se juge sur la **marge restante** (le job tient-il dans la
  marge ?), pas sur un pourcentage plat.

## Qualification picker / CI / harnais

- Le **produit n'est pas le verificateur** : une correction se prouve par un
  temoin qui **echoue avant** et **passe apres**. Le temoin du peer sur la
  rotation est `scripts/tests/test_tapis_rotation.py`, livre par la PR
  **#27242** (branche `feature/tapis-bascule-legere`) -- il **n'est pas encore
  sur `main`** (verifie : `main` ne porte que `test_tapis_equilibre.py`,
  `test_tapis_origami.py`, `test_tapis_rapide.py`, `test_tapis_reverif.py`).
  Tant que la PR n'est pas mergee, le temoin se relit depuis la branche :
  `git fetch origin feature/tapis-bascule-legere` puis
  `git show origin/feature/tapis-bascule-legere:scripts/tests/test_tapis_rotation.py`,
  et son rejeu complet est
  `python -m pytest scripts/tests/test_tapis_rotation.py -q` une fois la PR
  mergee. Un renvoi a un chemin absent de `main` sans cette mention n'est pas
  un temoin rejouable.
- Un defaut d'organe ne se corrige pas dans le perimetre d'un autre
  workspace : on **signale**, on ne touche pas.
- Une **attente** (CI, review, DWELL, merge, reponse d'une autre lane)
  n'arrete jamais la lane : elle s'ecrit dans
  `pending-checks-registry.md` et la production continue.

## Rapport de cycle

Trois a cinq lignes : ce qui est **livre** (PR, numero), ce qui est
**residuel** (attente nommee), ce qui a ete **remonte** au coordinateur.
Les rapports vivent sur le **dashboard**, jamais dans un fichier du depot.

Une **ligne d'auto-mesure worker** complete le rapport, sur le meme cycle :

- **temps actif / temps d'attente** : la part qui a produit, et celle qui a
  attendu une reponse externe (CI, review, DWELL, merge, une autre lane) ;
- **PRs ouvertes / PRs corrigees** par la lane ;
- **friction** : ce qui a bloque, avec le nom de l'organe ou de l'attente.

Les **objectifs chiffres de preparation des fusions et de cloture**
appartiennent a l'adjoint et au secretaire : la lane soeur garde la **mesure
worker** et le **releve des frictions communes** (une friction vue par la
lane est **montee**, elle n'est pas resolue dans son perimetre).
