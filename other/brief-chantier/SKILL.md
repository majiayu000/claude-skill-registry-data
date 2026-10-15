---
name: brief-chantier
description: >-
  Standard for autonomous-execution work plans ("plans de chantier"): AUTHOR a plan, EXECUTE it lot by
  lot, or ORCHESTRATE a batch of chips as parallel worktree chantiers. Use for "plan de chantier",
  "brief-chantier", "exécute le plan", "chantiers parallèles", run autonome/nocturne. Dev plans only.
---

# Brief-chantier — plans d'exécution autonome

Un plan remplace la mémoire de la session qui l'a conçu : un modèle moindre doit pouvoir l'exécuter sans
personne pour répondre. Détermine ton rôle :

- **AUTEUR** : écrire/découper un plan → § Écrire un plan.
- **EXÉCUTANT** : exécuter un plan donné → § Exécuter un plan.
- **ORCHESTRATEUR** : exécuter un LOT de chips « en chantiers » / « en parallèle », ou clôturer un run
  parallèle → § Orchestrer une flotte.

## Règles dures (les trois rôles ; aucun plan ne les assouplit)

- **A1 Budget total.** Par chantier : lignes ajoutées de code + tests + scripts ; suppressions, fichiers
  générés, README et docs ne comptent pas. La cible est proportionnée au chantier, le plafond ≤ 1 000 ; au-delà, découper. Chaque lot estime « ≈ N code +
  M tests », tests au moins égaux au code dans un dépôt doté d'une suite, somme sous le plafond (D3). Ratio tests/code > 2 :
  justifier ; > 4 : découper ou accord humain ; non applicable sous 50 lignes de code.
- **A2 Chips et décisions.** Chaque plan déclare `Chips : autorisés` ou `Chips : interdits`. Une décision par
  remarque (CORRIGER, CHIP si autorisés, NE PAS CORRIGER, INVALIDE) selon la règle 2 de
  `adversarial-pr-review` ; jamais « tout corriger, y compris les mineurs ».
- **A3 Revue à la clôture seulement, 2 rounds par cycle**, aucune relecture par lot, non contournable par un
  plan. Round 2 = delta. Un 2e cycle seulement après un FAIL, via un chip corrigeant le finding bloquant (règle 1 d'`adversarial-pr-review`).
  Sans convergence : brouillon, défauts listés, sans sentinelle ni ready/non-brouillon.
- **A4 Un comportement se teste une fois**, au niveau le plus proche de l'utilisateur ou du consommateur,
  après exécution réelle de la preuve de la fiche (dry-run, sandbox, app en local). Un socle sans effet
  visible se prouve avec un consommateur jetable, de bout en bout.
- **A5 Disjoncteur.** Un lot au double de son estimation en lignes, ou un chantier au-delà de son plafond :
  arrêt, état propre commité, rapport. La revue n'a lieu que si un lot à effet visible est commité. Un
  dépassement moindre se consigne, le run continue. Revenir sous le plafond = retirer du code AVEC son test.
- **G Fiche d'intention + simplificateur.** Fiche d'1 page, jetable (`assets/fiche-intention.md`, EN :
  `assets/intent-sheet.md`), écrite avec l'humain et validée avant le plan. Le simplificateur
  (`references/simplificateur.md`) passe une fois, avant la PR ; il ne peut que retirer du code et des tests.
- **L Langue.** Plan et fiche dans la langue du projet (FR ou EN) ; le contrat de commit
  `chantier(<slug>): lot N` ne change pas.

## Écrire un plan (rôle AUTEUR)

Exigences : **contexte 100 % autonome** (zéro « cette session », chemins absolus, état du repo décrit,
hypothèses explicites) ; **lots ≤ 2 h**, vérifiables en une passe, repo vert, DONE testable en une phrase ;
**checks par lot** (liste `<ol class="checks">`, voir étape 5) et commandes de fin de run exacts ; **coûts Convex déclarés** ou « aucun ». Texte
figé = renvoi d'une ligne au skill, section sans objet = « aucun ». Détails par étape : `references/auteur-details.md`.

0. **Brain d'abord.** `bun run --cwd ~/Desktop/my-projets/second-brain cli/index.ts search "<sujet + projet>"` ;
   cite les leçons dans « Leçons du brain », ou « aucune leçon applicable ».
1. **Fiche d'intention (G) AVEC l'humain**, sous `.chantier/<slug>/intention.md` (hors `docs/`), validée avant
   le plan. Sans `Validée par : <nom>, <date>`, livre la fiche seule et arrête-toi. Chantier technique :
   « Après » nomme ses consommateurs et ce qu'ils appellent.
2. **Explore le repo sur disque** : chaque fait vérifié et cité par référence, gate d'état en fichiers
   touchés (jamais en SHA), **baseline verte** avant d'écrire, points de contrôle humains en début de run.
3. **Copie `assets/template.html`** vers `<repo>/docs/plans/<AAAA-MM-JJ>-<sujet>.html`, remplis TOUS les
   `{{…}}`, garde le TOC fixe. Lignes de règles lues par le lint (FR ou EN) : `references/auteur-details.md`
   § Étape 3. `s-nice` finit avec ≥ 5 idées adjacentes NON incluses ; un must-have va dans les lots.
4. **Bloc Intention** en 3 à 5 phrases. Chaque garantie du bloc et de la fiche cite la phrase de la demande
   humaine qui l'exige et nomme le test qui échoue si elle casse ; sans citation, nice-to-have. Retirer un
   usage existant (README, CLI) est une décision de l'humain dans la fiche, jamais du tri.
5. **Lots** : le lot 1 livre la tranche verticale minimale que la preuve de la fiche exécute ; chaque lot
   suivant ajoute une garantie en gardant cette preuve verte. Par lot : estimation en heures, fichiers touchés
   (hors liste = arrêt), agent, checks (`<ol class="checks">`, un `<li data-check="id">` par check, UNE commande
   exacte dans `<code>`, exit 0 = succès ; jamais de bloc `<pre class="cmd">` dans un lot), DONE, « Commit du
   lot » `chantier(<slug>): lot N — <titre>`, DERNIER lot de processus compris (lint check 8).
   Le plan déclare ses tranches (`Tranches :` PR, lots, base, empilée ou depuis la branche par défaut) et un
   point de coupe après chaque lot à effet visible (D4) ; design, plan et fiche entrent dans la branche de base
   par une PR de documents avant le run (D7).
6. **Un agent par lot**, jamais `general-purpose` par défaut si le projet a des agents dédiés (`.claude/agents/`) ;
   clôture/PR/merge : « aucun — reste chez l'orchestrateur ».
7. **Galley** : `html_review_register` (chemin absolu), termine par `http://localhost:5179/html-review/<docId>` ;
   jamais le bloc `ws-review-state`.
8. **Approbation** : la fiche signée fait foi ; hub disponible : convo `approval` avec lien Galley
   (`bun run --cwd ~/Desktop/my-projets/workstation convo create <slug-projet> -`).
9. **Relis en candide** ; corrige à la décision, puis propage aux lots.
<!-- runtime-slot:preflight-invoke -->
10. **Préflight obligatoire.** Invoque le skill `brief-preflight` EN PASSANT les arguments
    `<chemin-absolu-du-plan.html> <repo-cible>` (ils déclenchent le lint automatique) : lint déterministe
<!-- /runtime-slot:preflight-invoke -->
    puis revue (rounds comptés en commits ; plafond ≤ 200 : lint seul, ≤ 600 : un round). Plan non préflighté = non livrable.

## Exécuter un plan (rôle EXÉCUTANT)

Chaque étape est un gate.

1. **Lis le plan et sa fiche.** Chemin vide, `undefined` ou inexistant, fiche sans `Validée par : <nom>, <date>`
   (EN : `Approved by: <name>, <date>`), ou convo cité par le plan et refusé : `ABORT` en une ligne. Aucune
   étape aval (revue, simplificateur, vérificateur, clôture) sans commit de lot du chantier.
2. **Restitue l'intention** en 1-2 phrases ; si elle contredit le bloc Intention ou la fiche : STOP, question au hub.
3. **Vérifie l'état du repo** contre « État du repo » ; divergence majeure : arrêt-et-chip. Travaille dans un
   worktree `.worktrees/<slug>` sur une branche créée pour le chantier, jamais dans le checkout principal.
4. **Lot par lot, dans l'ordre.** Dispatche au subagent du champ Agent (jamais `general-purpose` si un agent
   du projet est nommé ; jamais de délégation si « reste chez l'orchestrateur »).
<!-- runtime-slot:wait-subagents -->
   Pour attendre un sous-agent/workflow, préfère le **foreground** (`run_in_background: false`). En
   background : UN wakeup de secours armé (ScheduleWakeup) puis TERMINER LE TOUR ; un second ScheduleWakeup
   ou un `ListAgents` dans le même tour est du polling (le hook `schedule-wakeup-guard` bloque tout
   ré-armement à moins de 30 s). Jamais d'attente nue sans wakeup armé. Ne laisse pas le subagent committer :
<!-- /runtime-slot:wait-subagents -->
   relis son diff et le verdict de la vérification toi-même ; le code réel fait foi sur le plan, consigne
   l'écart. Un lot se ferme quand tous ses checks sortent 0, puis commit `chantier(<slug-du-plan>): lot N —
   <titre>` (jamais de Co-Authored-By). Le git log EST le suivi : ne modifie pas le plan HTML. Fichier hors
   liste, doublures de test, gate humain, run cloud : `references/executant-details.md`. Tiens un journal de
   décisions horodaté, une ligne par écart, découpage ou substitut (C3) ; tu peux couper au point de coupe
   d'une tranche qui déborde, noté au journal.
5. **Clôture (A3, ne bloque jamais)**, dans l'ordre : vérifications globales ; `adversarial-pr-review`
   (Mode A), 2 rounds par cycle, l'autre famille (`cross`) au round 1, vérificateur frais pour
   tout correctif du round 2 ; simplificateur avant la PR ; dernier lot : `git rm` la fiche, commit `chantier(<slug>): lot N — Clôture…` ; push et PR (brouillon sans convergence), aucun merge ;
   hygiène (verrou night-run libéré seulement si ce run l'a pris, serveur dev arrêté). Détail : `references/executant-details.md` § Étape 5.
6. **Rapporte** dans la conversation hub du plan : lots et commits, tests et lignes REMESURÉS à la clôture,
   décisions A2, journal de décisions, chiffres de finalize, lignes retirées par le simplificateur, tout usage existant cassé comme décision humaine. Un test rouge se montre.

## Protocole arrêt-et-chip (sur tout échec)

Un échec de CODE arrête le run. Un échec d'INFRA pré-existant (reproductible sans les modifications du
chantier) ouvre le chip mais laisse finir les vérifications ; dans le doute, c'est du code. Jamais de
contournement improvisé. Arrête-toi au lot en échec : pas de commit du lot raté, diff laissé en l'état.
Ouvre un chip : si `start_session` est disponible, utilise-le (own_initiative) ; sinon `cd ~/Desktop/my-projets/workstation && echo '<JSON>' |
bun run chips add -` avec `{"title","prompt","tldr","cwd"}` (plan, lot, commande, extrait d'erreur de 3-10
lignes, état laissé, reprise). Plan `Chips : interdits` : consigne l'échec dans le rapport. Note l'échec dans
la conversation hub du plan, puis termine (rapport honnête). Tests verts mais fonctionnalité inopérante avec
des données réelles : `references/impossibilite-decouverte.md`.

## Orchestrer une flotte de chantiers (rôle ORCHESTRATEUR)

Phases 1 à 3 (inventaire des chips, briefs, goal prompts) et clôture : `references/orchestration.md`. Lancer un plan à heure fixe (session locale programmée, routine cloud) : `references/nuits-planifiees.md`.

**Phase 3bis — Watchdog (obligatoire).** Le silence ne prouve pas la progression. Disque immobile + agent
absent = mort : relance avec l'état exact vérifié sur disque, jamais « reprends » à vide. Règles et journal :
`references/watchdog.md`.
<!-- runtime-slot:watchdog -->
Tick de 30-45 min, armé tant qu'un chantier n'a pas livré sa PR (ScheduleWakeup ou Monitor), avec la consigne
COMPLÈTE de surveillance dans le `prompt` du ScheduleWakeup (réinjecté à chaque réveil, il survit à la
compaction). Agent vivant : `ListAgents` ; relance : `SendMessage`.
<!-- /runtime-slot:watchdog -->

**Phase 4 — Clôture (nouvelle session, après les PRs).** Baseline verte avant le premier merge ; chaque
intégration passe par une PR (`ship-pr` vers la branche par défaut), jamais par un
merge local poussé sur elle ; gates COMPLETS sur l'intégré AVANT cette PR, redéploiement vérifié ; plans HTML
commités dans `docs/plans/` avant la PR finale ; nettoyage garanti (worktrees, branches locales ET
distantes) ; session review honnête.
