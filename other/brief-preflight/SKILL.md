---
name: brief-preflight
description: >-
  Pré-analyse d'un plan brief-chantier AVANT exécution : lint déterministe (script auto-exécuté à
  l'invocation) puis au plus 2 rounds de revue adversariale multi-agents, triage must-have /
  nice-to-have. Seulement pour les plans au standard brief-chantier, pas les documents libres.
when_to_use: >-
  Use this skill whenever un brief-chantier vient d'être écrit ou corrigé et
  doit être validé avant de livrer le goal prompt — triggers : « préflight »,
  « pré-analyse du brief », « zones d'ombre », « valide le brief-chantier »,
  « lance l'ultracode sur le plan » — et SYSTÉMATIQUEMENT en fin de rôle
  AUTEUR du skill brief-chantier (qui l'invoque comme étape 10 obligatoire,
  en passant le chemin du plan et le repo cible en arguments).
argument-hint: "<plan.html> <repo-cible> [--legacy]"
arguments: [plan, repo, flags]
allowed-tools:
  - Bash(node ${CLAUDE_SKILL_DIR}/scripts/preflight-lint.mjs *)
  - Bash(node ${CLAUDE_SKILL_DIR}/scripts/preflight-flotte.mjs *)
---

# Brief-preflight — valider un plan avant exécution autonome

Un brief-chantier s'exécute sans personne à qui poser une question : une ambiguïté, un fait faux ou une contradiction arrête le run ou le fait livrer autre chose. Deux couches : le DÉTERMINISTE (un script), puis le JUGEMENT (revue multi-agents). L'invocation de ce skill par brief-chantier ou par l'utilisateur VAUT opt-in ultracode pour les workflows décrits ici.

## Règles dures

1. **2 rounds au plus par plan**, comptés dans les commits du plan (message contenant « preflight round N »), non contournable. Un appelant qui en trouve 2 ne relance que le lint.
2. **Une décision par finding** : CORRIGER (bloquant ou majeur qui sert l'intention), NICE-TO-HAVE, NE PAS CORRIGER (une ligne de raison), INVALIDE. Un mineur n'est JAMAIS CORRIGER.
3. **Le plan respecte A1-A5 et G.** Le lint impose la forme, la lentille « Règles & process » le fond.
4. **Déterminisme d'abord** : aucun round sur ce qu'un script attrape.
5. **Plafond ≤ 200 lignes : lint seul ; ≤ 600 : un seul round.**

## Étape 0 — Lint déterministe (auto-exécuté à l'invocation)

<!-- runtime-slot:etape0-run -->
Le verdict ci-dessous est la sortie réelle du script sur le plan passé en argument, produite par préprocessing AVANT que tu lises ces lignes :

!`node "${CLAUDE_SKILL_DIR}/scripts/preflight-lint.mjs" $plan $repo $flags 2>&1 || true`

Si ce bloc montre une erreur d'arguments, relance à la main :

```bash
node ${CLAUDE_SKILL_DIR}/scripts/preflight-lint.mjs <chemin-absolu-du-plan.html> <repo-cible> [--legacy]
```
<!-- /runtime-slot:etape0-run -->

Le lint (plans FR et EN) vérifie sans jugement : placeholders, phrases interdites, chemins, scripts et ancres existants, structure et TOC, section flotte, règles dures (revue sans fin interdite, `Budget total : <cible> / <plafond>` avec cible ≤ plafond ≤ 1000, `Chips`, `Tranches`, `Fiche d'intention` validée, `Doublures de test`, « ≈ N code + M tests » par lot et leur somme sous le plafond).

**Checks de lot.** Chaque lot liste ses checks en `<ol class="checks">` : un `<li data-check="id">` par check (id unique dans le plan), UNE commande exacte dans `<code>`, exit 0 = succès. Refusés : commande vague (consigne, phrase, placeholder, `|| true`), fichier ou script npm absent du repo cible, sauf fichier listé dans les « Fichiers touchés » du lot ou d'un lot précédent, ou check marqué `(nouveau)`.

`--legacy` rétrograde en avertissement les conventions récentes (jamais les clauses sans fin ni la flotte). VERDICT FAIL = corrige TOUTES les erreurs avant tout round, puis relance le lint.

## Étape 0bis — Lint de VAGUE (chantiers parallèles uniquement)

Le lint mono-plan ne voit pas deux plans qui se chevauchent. Ce script prend N ≥ 2 plans ENSEMBLE ; l'ORCHESTRATEUR le lance en fin de Phase 2, **avant de dispatcher la flotte** :

```bash
node ${CLAUDE_SKILL_DIR}/scripts/preflight-flotte.mjs <plan1.html> <plan2.html> …
node ${CLAUDE_SKILL_DIR}/scripts/preflight-flotte.mjs <répertoire-de-plans> [--depuis <N>]
```

Erreurs : plan sans section flotte ; plage absente, illisible, en collision ou sous `--depuis` ; noms de vague divergents ; **même fichier dans les « Fichiers touchés » de deux plans**, sauf si l'un déclare `Dépend de` l'autre. Avertissements : frères incomplets, trous entre plages, `Dépend de` orphelin.

<!-- runtime-slot:flotte-proof -->
Un run PASS enregistre sa preuve (contenu-adressée) dans `~/.claude/.flotte-lint-runs.json`, et le Stop hook global `~/.claude/hooks/flotte-plage-gate.mjs` empêche toute session ayant écrit ≥ 2 plans d'une même vague de s'arrêter tant que cette preuve manque ou ne correspond plus au contenu actuel des plans.
<!-- /runtime-slot:flotte-proof -->

## Étape 1 — Revue de jugement (round 1)

<!-- runtime-slot:models -->
- **Les lentilles** tournent TOUJOURS en agents `model: 'sonnet'`, `effort: 'medium'`, épinglés dans les opts du Workflow. L'alias `sonnet` suit le dernier Sonnet publié : jamais d'id daté.
- **Le triage** (étape 2) reste au modèle de la SESSION : le jugement et la correction du plan reviennent au modèle fort de l'authoring. Ne pas ajouter de `model:` au frontmatter de ce skill.
<!-- /runtime-slot:models -->

<!-- runtime-slot:etape1-intro -->
Un Workflow lance EN PARALLÈLE un agent par lentille (findings structurés : titre, sévérité bloquant/majeur/mineur, zone du plan, détail, fix proposé). Chaque agent lit le plan EN ENTIER + le repo cible : vérifier dans le code avant d'affirmer, rendre une liste VIDE plutôt que des findings cosmétiques, ignorer ce qui est hors périmètre. Le script du Workflow DOIT `throw` si le chemin du plan ou le repo cible est `undefined`/vide.
<!-- /runtime-slot:etape1-intro -->

Quatre lentilles :

1. **Candide** : exécuter le plan ce soir sans personne. Chaque commande lançable telle quelle, chaque DONE testable, chaque preuve en direct nomme la donnée qui existe aujourd'hui (C2) ? Où faudrait-il deviner ? Deux sections se contredisent-elles ?
2. **Fact-check** : chaque affirmation technique (fichier:ligne, noms d'état, scripts, clés, valeurs recopiées) confrontée au code réel.
3. **Mécanique du domaine** : le design tient-il ? Ne juge que les comportements que la fiche demande : chaque garantie cite la demande de l'humain, sinon NICE-TO-HAVE. Tout artefact NEUF hérite des invariants de l'existant.
4. **Règles & process** : A1-A5 et G. Budget : ton estimation l'emporte sur celle de l'auteur ; au-dessus du plafond, CORRIGER = découper, jamais NE PAS CORRIGER (D3). Chips cohérents, fiche d'intention PERTINENTE (le plan sert son « pourquoi » et reste hors de son « ce que ce n'est pas »), preuve réelle avant tout test simulé. Puis cohérence avec CLAUDE.md : lots ≤ 2 h à état vert, gates complets.

Sur demande seulement, pour alimenter le nice-to-have : **Personas** (rôles, langues, thème sombre, mobile, accessibilité, états vides) et **Futur** (volume, deuxième consommateur, migration).

## Étape 2 — Triage et correction (par l'auteur, modèle de la session)

- **CORRIGER** (bloquant ou majeur, ancré `fichier:ligne` ou comportement démontrable) : corrige d'abord la DÉCISION (architecture), puis propage aux lots, jamais un patch local dans un seul lot.
- **NICE-TO-HAVE** : ne gonfle PAS les lots ; ajoute l'item à « Nice-to-have » (≥ 5), l'utilisateur arbitre.
- **NE PAS CORRIGER** (style, hors périmètre, hors fiche) : une ligne de raison dans ta sortie, pas dans le plan. **INVALIDE** (faux) : rejette.

Après les correctifs : relecture CANDIDE du plan entier, puis relance du lint.

## Étape 3 — Round 2 (delta seulement), arrêt, sortie

Plafond > 600, round 1 corrigé : UN round 2 : les lentilles concernées relisent les passages modifiés et ce qui en dépend. Même triage, relance du lint, puis **STOP**. Un bloquant restant se signale à l'utilisateur, jamais par un round 3.

Rends compte : rounds, findings par décision, bloquants tués ou ouverts, verdict du lint, et « le plan est prêt pour exécution » ou ce qui l'en empêche.
