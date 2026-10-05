---
name: "gsupport-analyze"
argument-hint: "[GSUPPORT-KEY]"
description: "Analyse d'un ticket client GSUPPORT : lit le ticket, tous les commentaires et toutes les pièces jointes, investigue le code, qualifie la nature du problème (bug / config / comportement attendu / évolution) et sauvegarde un rapport <ISSUE_KEY>-analyse.md — sans créer de branche ni de PR"
---

# GSupport Analyze Skill

Skill dédié aux tickets **clients** du projet Jira `GSUPPORT` (Global Customer Support).

Un ticket GSUPPORT n'est **pas** un ticket de développement : c'est une remontée client brute.
L'objectif de ce skill n'est pas de produire un plan d'implémentation, mais de **qualifier** la
demande avant qu'elle ne devienne (ou non) un `ORBISBUG` ou un `HORME`.

> Pour les tickets de développement (`HORME-`, `ORBISBUG-`), utiliser `/task-analyze`.

## Installation

À faire une seule fois sur un nouveau poste.

**1. Variables Jira** dans `~/.bashrc` (chacun génère son propre PAT depuis son profil Jira) :

```bash
export JIRA_DOMAIN="jira.dedalus.com"
export JIRA_API_TOKEN="<PAT Jira Server personnel>"
```

**2. Chemins des repos** — au premier lancement, si les repos ne sont pas trouvés, le skill
**demande où ils se trouvent** et propose d'enregistrer la réponse dans `config.json`. Rien à
préparer donc, mais il reste possible de renseigner `reposDir` à l'avance, ou d'exporter
`REPOS_DIR` qui est prioritaire.

**Aucun repo n'est à cloner à l'avance** : à chaque analyse, le skill affiche l'état des repos
(présent, branche de la version disponible) et indique lesquels sont **requis pour ce ticket
précis**, avec la commande `git clone` correspondante. Un repo absent mais non pertinent n'est pas
signalé comme un problème.

**3. Lier le skill** : `bash skills/setup.sh` depuis la racine de `presc-workflows-tools`.

**Outils requis** : `curl`, `jq`, `python3`, `unzip`, `tar`, `gzip` — tous standards, aucun paquet à
installer. `pdftotext`, `7z` et `unrar` sont optionnels (sans eux, les PDF et les archives `.7z`/`.rar`
joints sont signalés comme non exploitables).

## Configuration requise

- `JIRA_DOMAIN` : domaine Jira (ex. `jira.dedalus.com`)
- `JIRA_API_TOKEN` : Personal Access Token Jira Server

> Les variables sont définies dans `~/.bashrc`. **Toujours lancer `source ~/.bashrc`** avant toute action.

### `config.json` — la connaissance du skill

`config.json`, situé dans ce même dossier, est la **seule** source de vérité. Rien n'est en dur
dans ce fichier-ci : ni un chemin, ni un nom de repo, ni une correspondance version → repo.

| Bloc | Rôle | Utilisé à l'étape |
|---|---|---|
| `reposDir`, `reportDir` | où sont les repos, où écrire le rapport | 3, 8 |
| `agents`, `orchestratorModel` | modèles des sous-agents et modèle attendu pour la qualification | 0, 2, 4 |
| `domains` | routage métier : `aliases` client, `repos`, `paths`, `grepSeeds` | 3.1, 4 |
| `glossary` | jargon client → terme technique | 3.1 |
| `i18nHint` | où se trouvent réellement les libellés affichés | 4.1 |
| `repositories` | rôle de chaque repo, URL de clone, `versionRange` | 3 |
| `excludedRepositories` | repos volontairement hors périmètre, avec le motif | 3 |

Les trois blocs de connaissance — `domains`, `glossary`, `i18nHint` — sont ceux qui font la
différence entre une recherche ciblée et une recherche à l'aveugle. **Ils vieillissent** : les
tenir à jour au fil des tickets fait partie du travail d'analyse, pas d'une maintenance à part.

Chaque entrée de `repositories` porte `name`, `path` (relatif à `reposDir`) et `description`.

Un repo listé dans `excludedRepositories` est **hors périmètre en permanence** : ne jamais lancer
de sous-agent dessus, ne pas le faire apparaître dans le diagnostic de l'étape 3, ne pas proposer
de le cloner. Comme toutes les boucles du skill itèrent sur `.repositories[]`, l'exclusion est
automatique — il suffit de ne pas réintroduire l'entrée. C'est aujourd'hui le cas de
`orme-medication-packaging`, qui ne porte que du packaging et des scripts de livraison, jamais de
logique métier.

```bash
jq -r '.excludedRepositories[] | "\(.name)\t\(.reason)"' "$SKILL_DIR/config.json"
```

Un repo portant `optIn: true` est un cas intermédiaire : il **n'est jamais retenu par le routage
par défaut**, mais reste mobilisable quand son `optInCondition` est remplie — l'analyse désigne
explicitement son périmètre, ou l'utilisateur l'a demandé à l'étape 1b. Deux repos sont dans ce
cas :

- `orme-pgd-config` : il n'a rien d'un repo de prescription, mais reste la seule source de vérité
  quand l'hypothèse retenue est un problème de paramétrage client ;
- `orme-common` : à ne fouiller qu'en **second passage**, quand un module fonctionnel n'a pas
  retrouvé le libellé, la clé i18n ou la règle cherchée (voir « Second passage » à l'étape 4).

```bash
jq -r '.repositories[] | select(.optIn == true) | "\(.name)\t\(.optInCondition)"' \
  "$SKILL_DIR/config.json"
```

Le retenir sans que sa condition soit remplie fait perdre un sous-agent sur du code hors sujet ;
l'oublier alors qu'elle l'est fait conclure « bug » sur ce qui n'est qu'une configuration, ou
`Aucun code pertinent identifié.` sur un libellé qui se trouvait simplement ailleurs. Dans les deux
cas, l'indiquer dans le tableau des repos du rapport (`opt-in : retenu / non retenu`).

```bash
SKILL_DIR=$(dirname "$(readlink -f ~/.copilot/skills/gsupport-analyze/SKILL.md)")

# reposDir vient de config.json ; la variable d'environnement REPOS_DIR reste prioritaire.
REPOS_DIR="${REPOS_DIR:-$(jq -r '.reposDir // ""' "$SKILL_DIR/config.json")}"
REPOS_DIR="${REPOS_DIR/#\~/$HOME}"

# Un dossier n'est valide que s'il contient au moins un des repos declares.
is_valid_repos_dir() {
  [ -d "$1" ] || return 1
  jq -r '.repositories[].path' "$SKILL_DIR/config.json" \
    | while read -r p; do [ -d "$1/$p" ] && echo found; done | grep -q found
}

if is_valid_repos_dir "$REPOS_DIR"; then
  echo "reposDir : $REPOS_DIR"
else
  echo "INTROUVABLE : $REPOS_DIR"
  # Pistes a proposer a l'utilisateur.
  for candidate in "$HOME/work" "$HOME/repos" "$HOME/dev" "$HOME/SourceRepo"; do
    is_valid_repos_dir "$candidate" && echo "candidat : $candidate"
  done
fi
```

**Si le dossier est introuvable ou ne contient aucun repo déclaré : demander à l'utilisateur.**
Ne jamais deviner silencieusement, et ne jamais poursuivre l'investigation de code sur un chemin
non confirmé — une recherche dans le vide produirait une conclusion fausse.

1. Poser la question avec l'outil `ask_user`, en proposant les candidats détectés ci-dessus comme
   choix, plus une saisie libre :
   *« Où se trouvent tes repos ORME ? Le chemin configuré `<reposDir>` est introuvable. »*
2. Valider la réponse avec `is_valid_repos_dir`. Si elle ne contient aucun repo déclaré, le dire
   et redemander **une** fois.
3. Une fois le chemin validé, **proposer de l'enregistrer** dans `config.json` pour ne plus avoir
   à le demander (écriture sur un fichier existant → confirmation requise) :

   ```bash
   tmp=$(mktemp)
   jq --arg d "$REPOS_DIR" '.reposDir = $d' "$SKILL_DIR/config.json" > "$tmp" \
     && mv "$tmp" "$SKILL_DIR/config.json"
   ```

4. Si l'utilisateur décline la question ou n'a pas les repos en local : poursuivre l'analyse Jira
   **sans** investigation de code, et l'indiquer clairement dans le rapport
   (`Investigation du code non réalisée : repos non disponibles`) plutôt que de conclure
   `Aucun code pertinent identifié.`, qui serait trompeur.

Lister les repos disponibles une fois `REPOS_DIR` validé :

```bash
jq -r '.repositories[] | "\(.name)\t\(.description)"' "$SKILL_DIR/config.json"
```

Un ticket GSUPPORT ne se limite presque jamais au repo courant : le message d'erreur peut venir
de `orme-prescription-api`, un libellé de `orme-common`, une règle historique de
`orme-medication-legacy`. **Sélectionner les repos à fouiller à l'étape 3**, en confrontant le
symptôme aux `description` de `config.json`. Ignorer un repo absent du disque sans bloquer, et
lister les repos ignorés dans le rapport.

Si `config.json` déclare une entrée pointant vers un fichier de **schéma de base de données**
(markdown), le consulter **uniquement au `grep`** pour retrouver une table ou une colonne — ne
jamais le lire en entier.

## Exécution autonome

| Pré-autorisé — exécuter sans demander | Demande confirmation |
|---|---|
| Appels Jira en lecture (`curl` GET) | Écriture sur un fichier existant |
| Téléchargement des pièces jointes dans `/tmp` | Suppression de fichiers |
| `grep`, `glob`, `view`, lecture de fichiers | Utiliser une branche autre que celle de la version |
| Extraction d'archives dans `/tmp` | Installation de paquets |
| `git grep`, `git show`, `git log`, `git ls-tree`, `git rev-parse` sur `origin/<branche>` | Commit / push |
| `git fetch origin` (met à jour les refs distantes uniquement) | |
| Lancement des sous-agents de collecte (étapes 2 et 4) | |
| Création du dossier de rapport et écriture d'un **nouveau** fichier | |

**Interdit** dans les repos de l'utilisateur, même avec son accord : `git checkout`, `git switch`,
`git stash`, `git worktree`, `git reset`, `git pull`, ou toute commande modifiant la branche
courante, le working tree ou les stashes. Tout est faisable en lecture seule sur `origin/<branche>`.

Ne jamais demander « je continue ? » pour une opération pré-autorisée.

Si `/allow-all` est actif, ce tableau reste la règle de conduite : les opérations de la colonne de
droite continuent d'être annoncées et validées explicitement.

## Architecture d'exécution — orchestrateur et sous-agents

Une analyse GSUPPORT brasse beaucoup de matière brute : un `issue.json` complet, des dizaines de
commentaires, des pièces jointes, puis des recherches de code sur plusieurs repos. Tout garder dans
une seule conversation sature le contexte avant la qualification, qui est justement l'étape qui a
besoin de tout voir.

Le skill est donc découpé : la **collecte** est déléguée à des sous-agents, la **décision** reste
chez l'orchestrateur.

| Bloc | Exécutant | Sortie |
|---|---|---|
| Étapes 0, 1, 1b — résolution et validation de la clé, conseil de permissions, modèle, pré-analyse utilisateur | orchestrateur | — |
| Étape 2 — collecte Jira (ticket, commentaires, pièces jointes, liens) | **1 sous-agent** (modèle rapide) | `compte-rendu-jira.md` |
| Étape 3 — sélection des repos, diagnostic, résolution de branche | orchestrateur | tableau affiché |
| Étape 4 — investigation du code | **1 sous-agent par repo retenu**, en parallèle (modèle fort) | `compte-rendu-code-<repo>.md` |
| Étapes 5 à 9 — qualification, hypothèses, rapport | orchestrateur | `<ISSUE_KEY>-analyse.md` |

### Règle du passage par fichiers

C'est elle qui protège réellement le contexte, plus encore que le découpage lui-même.

Chaque sous-agent **écrit son résultat complet dans un fichier** sous `/tmp/gsupport/<ISSUE_KEY>/`
et ne **renvoie qu'une synthèse courte** (30 lignes maximum) à l'orchestrateur. L'orchestrateur ne
relit ensuite que les sections dont il a besoin, au moment d'écrire le rapport — jamais les
fichiers entiers d'un coup, et jamais le JSON brut.

Un sous-agent qui recopie tout son travail dans sa réponse annule le bénéfice du découpage.

### Ce qui ne se délègue jamais

- Toute question à l'utilisateur (`ask_user`) : pré-analyse (étape 1b), `reposDir`
  introuvable, repo requis manquant, branche approchante à confirmer. Un sous-agent ne peut pas
  dialoguer.
- La **qualification** (étape 5) : elle croise Jira, code et contradictions entre commentaires.
  C'est la raison d'être du skill, elle reste chez l'orchestrateur.
- L'écriture du rapport final.

### Nommage des agents

Plusieurs agents tournent en parallèle : sans nom parlant, l'utilisateur ne sait pas lequel est en
train de travailler ni sur quoi. Renseigner **`name`** et **`description`** à chaque lancement.

| Bloc | `name` | `description` |
|---|---|---|
| Étape 2 | `collecte-ticket-jira-<ISSUE_KEY>` | `Collecte Jira <ISSUE_KEY>` |
| Étape 4 | `investigation-code-<repo>` | `Investigation <repo> sur <branche>` |

Exemples : `collecte-ticket-jira-GSUPPORT-47944`, `investigation-code-orme-prescription` avec la
description `Investigation orme-prescription sur 317XXXX/develop`.

Le nom porte **le repo, pas un numéro** : `investigation-code-1`, `investigation-code-2` ne dit
rien quand trois agents tournent ensemble. Quand un compte rendu sera relu à l'étape 5, c'est par ce nom
qu'on le retrouvera.

### Consignes communes à tous les sous-agents
Les sous-agents sont **sans mémoire** : chaque prompt doit être autoportant. Y inclure
systématiquement :

- la clé du ticket et le chemin `/tmp/gsupport/<ISSUE_KEY>/` où écrire,
- le rappel que `JIRA_DOMAIN` / `JIRA_API_TOKEN` viennent de `source ~/.bashrc`,
- le rappel du masquage des données patient (`Contains PID`),
- la contrainte de sortie : écrire le fichier, ne renvoyer qu'une synthèse ≤ 30 lignes,
- l'interdiction absolue de `git checkout` / `switch` / `stash` / `worktree` / `reset` / `pull`,
- l'interdiction de poser une question : en cas de blocage, l'écrire dans le compte rendu et rendre la
  main.

Si un sous-agent échoue ou rend une sortie vide, **ne pas le relancer une seconde fois** :
exécuter son bloc directement, et le signaler dans le rapport.

### Choix des modèles

Tous les blocs ne demandent pas la même puissance : la collecte Jira est mécanique, l'investigation
de code est du raisonnement. Les modèles sont déclarés dans `config.json` sous `agents`, jamais en
dur ici — les identifiants évoluent et tout le monde n'a pas les mêmes accès.

```bash
jq -r '.agents | to_entries[] | "\(.key)\t\(.value.model // "défaut")\t\(.value.reasoningEffort // "-")"' \
  "$SKILL_DIR/config.json"
```

| Bloc | Clé `config.json` | Intention |
|---|---|---|
| Étape 2 — collecte Jira | `agents.jiraCollect` | modèle rapide : `curl`, `jq`, extraction de documents, gros volume de tokens et peu de raisonnement |
| Étape 4 — investigation code | `agents.codeInvestigate` | modèle fort avec `reasoningEffort` élevé : chaîne message d'erreur → front → REST → condition métier |

Passer ces valeurs aux paramètres `model` et `reasoning_effort` de l'outil `task`. Deux garde-fous :

- Valeur vide → lancer l'agent **sans** forcer de modèle.
- Identifiant refusé (modèle inconnu ou non accessible) → **relancer une fois sans le paramètre
  `model`** plutôt que d'abandonner l'analyse, et le signaler en une ligne. Un `config.json` recopié
  d'un autre poste ne doit jamais bloquer un ticket.

**Le modèle de l'orchestrateur, lui, ne se force pas** : il dépend du `/model` de la session. C'est
pourtant lui qui qualifie (étape 5). D'où la vérification à l'étape 1.

## Commande

### `/gsupport-analyze <ISSUE_KEY>`

`<ISSUE_KEY>` accepte aussi une URL complète (`https://jira.dedalus.com/browse/GSUPPORT-47944`) :
extraire la clé de l'URL le cas échéant.

### Résolution de l'ISSUE_KEY

L'argument tapé après la commande **n'est pas transmis au skill**. Le CLI injecte un message
figé — `The user explicitly invoked the "<nom>" skill. Follow its instructions now.` — qui ne
porte que le nom du skill. Le `argument-hint` du frontmatter n'affiche qu'un repère de saisie
dans l'autocomplétion : il ne transporte pas la valeur non plus. Sans règle explicite, la clé
est donc redemandée alors qu'elle a déjà été fournie. La résoudre est la toute première action,
avant toute question.

Chercher, dans cet ordre, et s'arrêter au premier résultat :

1. un motif `GSUPPORT-\d+` dans le **message qui a déclenché le skill** (présent quand
   l'utilisateur a écrit une phrase libre plutôt qu'une slash-command) ;
2. une URL `https://<domaine>/browse/GSUPPORT-\d+` dans ce même message → en extraire la clé ;
3. **l'historique de saisie du CLI** — c'est lui qui rattrape le cas de la slash-command, car il
   conserve la ligne brute réellement tapée, la plus récente en tête :

   ```bash
   jq -r '.commandHistory[]' ~/.copilot/command-history-state.json 2>/dev/null \
     | grep -m1 -E '^/gsupport-analyze[[:space:]]' \
     | grep -oE 'GSUPPORT-[0-9]+'
   ```

   Si la commande a été lancée sans argument, cette ligne ne renvoie rien : passer au point 4.
   Ne **jamais** élargir le `grep` à tout l'historique, une clé d'un ticket précédent serait
   reprise à tort.
4. un motif `GSUPPORT-\d+` dans les messages récents de la session (ticket en cours de discussion).

Une clé issue du point 3 ou 4 n'a pas été lue directement dans la demande : l'annoncer en une
ligne avant de démarrer — *« Analyse de `GSUPPORT-40380` (clé reprise de ta commande). »* — pour
que l'utilisateur puisse corriger immédiatement.

Une fois résolue, la clé est **figée pour toute l'analyse** : ne plus jamais la redemander, et la
rappeler dans chaque message qui attend une action de l'utilisateur.

---

## Étape 0 — Valider la clé

```
Si aucune clé n'a pu être résolue, ou si ce qui a été fourni n'est pas au format
GSUPPORT-<chiffres> (autre préfixe, numéro manquant, saisie libre) :
  → demander via `ask_user` : « Quel ticket GSUPPORT veux-tu analyser ? (ex. GSUPPORT-47944) »
  → accepter une clé nue ou une URL Jira, puis revalider
  → si la nouvelle saisie est un ticket HORME-/ORBISBUG-, indiquer que ce skill traite
    uniquement les GSUPPORT et rediriger vers /task-analyze, puis arrêter

Sinon : passer directement à l'étape 1.
```

## Étape 1 — Permissions — **ne jamais interrompre l'enchaînement**

L'analyse enchaîne des dizaines d'appels `curl`, `git`, `grep` et d'écritures dans `/tmp`. Valider
chaque demande une par une casse le rythme — mais **poser la question casse davantage** : un skill
ne peut pas exécuter `/allow-all` lui-même, et une fois l'utilisateur invité à le taper, la
conversation s'arrête sans jamais repartir toute seule. Le ticket n'est même pas lu.

**Règle : ne rien demander, ne jamais s'arrêter.** Enchaîner directement sur l'étape 1b puis sur la
collecte Jira, en respectant le tableau « Exécution autonome ».

Se contenter d'un **conseil d'une ligne**, joint au premier message, sans attendre de réponse :

```
Astuce : /allow-all évite d'avoir à confirmer chaque commande de cette analyse.
```

À ne surtout pas faire :

- appeler `ask_user` pour les permissions ;
- écrire « tape `/allow-all`, je reprends ensuite » puis rendre la main — l'analyse meurt là ;
- reposer le sujet plus tard, même si des confirmations s'enchaînent.

> Pour supprimer les confirmations une fois pour toutes, ajouter
> `"defaultPermissionMode": "allow-all"` dans `~/.copilot/settings.json` (fichier **utilisateur**
> uniquement : la clé est ignorée depuis `.github/copilot/settings.json` d'un repo).
> Elle ne s'applique qu'aux nouvelles sessions interactives (pas `--resume`, pas `-p`).

### Vérifier le modèle de la session

La qualification (étape 5) est un exercice de jugement : arbitrer entre « bug » et « comportement
attendu » à partir de commentaires contradictoires et d'une condition métier. Un modèle léger y
conclut mécaniquement.

Comparer le modèle de la session à `orchestratorModel.preferred` de `config.json` :

```bash
jq -r '.orchestratorModel.preferred | join(", ")' "$SKILL_DIR/config.json"
```

S'il n'en fait pas partie, **avertir une fois puis continuer** — ne jamais bloquer l'analyse :

```
Session sur <modèle>. La qualification gagne à tourner sur <liste des modèles préférés>.
Tu peux basculer avec /model puis relancer, ou continuer : l'investigation de code utilisera
de toute façon <agents.codeInvestigate.model>.
```

Ne pas répéter l'avertissement pendant l'analyse, et le reporter en une ligne dans le rapport :
la confiance d'une qualification dépend du modèle qui l'a produite.

## Étape 1b — Pré-analyse de l'utilisateur — **optionnelle**

L'utilisateur a souvent déjà regardé le ticket avant de lancer le skill : il sait que le bug est
purement front Angular, ou qu'il vient du paramétrage. Sans cette information, l'étape 3 route à
l'aveugle et l'étape 4 lance des agents sur des repos hors sujet — du temps et du contexte perdus,
et du bruit dans le rapport.

Poser la question **une seule fois**, via `ask_user`, tous les champs facultatifs. Proposer
explicitement de passer : un utilisateur qui ne sait pas ne doit pas se sentir obligé d'inventer un
périmètre, une mauvaise restriction est pire que pas de restriction du tout.

```
Titre  : As-tu déjà une piste sur ce ticket ?
Texte  : Facultatif. Si tu sais déjà où se situe le problème, l'analyse évite de fouiller des
         repos sans rapport. Laisse vide ou décline si tu préfères que le skill route seul.

Champs :
  - Couche concernée (multi-select, facultatif)
      front Angular | front GWT legacy | back Java | API / REST | configuration PGD |
      référentiel médicament | base de données | je ne sais pas
  - Domaine métier (select, facultatif)      -> alimenté par `domains[].label` de config.json,
                                                plus un choix « laisser le skill router »
  - Repos à exclure (multi-select, facultatif) -> alimenté par `repositories[].name`
  - Piste déjà identifiée (texte libre, facultatif)
      ex. « erreur levée à la validation, seulement pour les lignes si besoin »
```

Alimenter les listes depuis `config.json` — ne rien écrire en dur :

```bash
jq -r '.domains[].label'      "$SKILL_DIR/config.json"
jq -r '.repositories[].name'  "$SKILL_DIR/config.json"
```

Exploitation des réponses :

| Réponse | Effet |
|---|---|
| Couche concernée | restreint les `paths` transmis aux agents (étape 4) et écarte les repos sans rapport : « front Angular » seul → pas d'agent sur `orme-medication-legacy` ni `orme-global-repo` |
| Domaine métier | court-circuite le routage 3.1 : le domaine est retenu d'office, ses `paths`, `i18nBundles` et `grepSeeds` sont utilisés tels quels |
| Repos à exclure | aucun sous-agent n'est lancé sur ces repos |
| Piste déjà identifiée | recopiée telle quelle dans le prompt des agents de l'étape 4 et dans le rapport |

Trois garde-fous, sans lesquels cette étape dégraderait l'analyse au lieu de l'accélérer :

1. **Formulaire décliné, vide ou « je ne sais pas » → comportement inchangé** : routage automatique
   complet, aucun repo écarté. Ne pas insister, ne pas reposer la question.
2. **La restriction est une indication forte, pas un mur.** Un agent qui ne trouve rien dans le
   périmètre imposé le **signale** au lieu de conclure `Aucun code pertinent identifié.` :
   l'orchestrateur peut alors proposer d'élargir. Une hypothèse de l'utilisateur reste une
   hypothèse — le ticket peut la contredire.
3. **La restriction est tracée dans le rapport** (`Périmètre restreint par l'utilisateur`). Une
   conclusion tirée sur un périmètre réduit ne se lit pas comme une conclusion tirée sur l'ensemble.

Si la collecte Jira (étape 2) contredit franchement la pré-analyse — le ticket décrit une erreur
backend alors que l'utilisateur a annoncé « front Angular » —, le dire à l'étape 3 et proposer
d'élargir plutôt que d'appliquer la restriction en silence.

## Étape 2 — Collecte Jira — **déléguée à un sous-agent**

Ce bloc produit le gros du volume brut (JSON complet, commentaires, pièces jointes). Il est confié
à **un seul sous-agent** de type `explore`, nommé `collecte-ticket-jira-<ISSUE_KEY>` et lancé avec le
modèle `agents.jiraCollect` de `config.json`. Il écrit
`/tmp/gsupport/<ISSUE_KEY>/compte-rendu-jira.md` et ne renvoie qu'une synthèse.

> **Pièces jointes et images** — le sous-agent doit pouvoir ouvrir des images avec l'outil `view`.
> S'il n'en est pas capable, il l'écrit dans le compte rendu (`images non exploitées par l'agent`) et
> l'orchestrateur les regarde lui-même après coup, sans relancer tout le bloc.

> **Archives** — toute pièce jointe `.zip`/`.tar.gz`/`.7z`/`.rar` doit être décompressée et son
> contenu lu fichier par fichier (voir 2.3.1). Le compte rendu doit lister les fichiers extraits ; une
> archive restée fermée est un échec de l'étape 2.

### Prompt à fournir au sous-agent

Y reprendre intégralement les sections 2.1 à 2.4 ci-dessous (elles sont le contrat de l'agent),
plus les consignes communes, et exiger cette structure de compte rendu :

```markdown
# Compte rendu Jira — <ISSUE_KEY>
## Champs        <tableau des champs standards et GSUPPORT>
## Symptôme      <description reformatée, scénario, résultat actuel/attendu, message d'erreur exact>
## Commentaires  <synthèse chronologique : auteur, date, apport>
## Pièces jointes <une entrée par PJ : nom, type, ce qu'elle apporte ; "Contenu non exploitable" sinon
 — pour une archive : la liste des fichiers extraits et l'apport de chacun>
## Liens         <tickets liés avec statut + résolution + apport de leur description ; liens externes>
## Pistes de recherche
<les 3 à 8 chaînes de caractères exactes les plus discriminantes pour le `git grep` :
 message d'erreur, libellé d'écran, code d'erreur, nom de bouton, classe apparaissant dans une
 stacktrace. C'est le livrable le plus important pour l'étape 4.>
## Vocabulaire client
<les termes métier employés par le client, traduits via le `glossary` de config.json ;
 signaler tout terme absent du glossaire — il devra y être ajouté>
## Ce qui n'a pas pu être lu
```

La **synthèse renvoyée** (≤ 30 lignes) doit tenir en : version détectée, produit, symptôme en
trois phrases, message d'erreur exact, pistes de recherche, et ce qui n'a pas pu être lu.

### Ce que l'orchestrateur en fait

Lire la synthèse, puis ne relire dans `compte-rendu-jira.md` que les sections nécessaires à l'étape
concernée. Ne jamais charger `issue.json` ni `comments.json` dans le contexte de l'orchestrateur :
ils restent sur disque, à disposition d'un `jq` ciblé si un champ précis manque.

Si `Contains PID = Yes`, vérifier dans la synthèse qu'aucune donnée patient n'a fuité avant de
recopier quoi que ce soit dans le rapport.

---

## 2.1 — Lire le ticket

Récupérer **tous** les champs (les tickets GSUPPORT portent l'essentiel de l'information dans des
custom fields, ne pas filtrer avec `?fields=`) :

```bash
source ~/.bashrc
mkdir -p /tmp/gsupport/<ISSUE_KEY>
curl -s -H "Authorization: Bearer ${JIRA_API_TOKEN}" -H "Accept: application/json" \
  "https://${JIRA_DOMAIN}/rest/api/2/issue/<ISSUE_KEY>" \
  -o /tmp/gsupport/<ISSUE_KEY>/issue.json
```

Si la réponse contient `errorMessages` → afficher `Ticket <ISSUE_KEY> introuvable sur ${JIRA_DOMAIN}` et arrêter.

### Champs standards

| Donnée | Chemin JSON |
|---|---|
| Titre | `fields.summary` |
| Description | `fields.description` (texte wiki Jira Server) |
| Type | `fields.issuetype.name` (ex. `Customer Support Request`) |
| Statut | `fields.status.name` |
| Priorité | `fields.priority.name` |
| Labels | `fields.labels[]` (ex. `AP-HP`, `FR`) |
| Créé / Mis à jour | `fields.created` / `fields.updated` |
| Rapporteur | `fields.reporter.displayName` |
| Liens d'issues | `fields.issuelinks[]` |
| Pièces jointes | `fields.attachment[]` |

### Champs spécifiques GSUPPORT

Ces custom fields sont propres au projet GSUPPORT et portent le contexte client et produit.

| Donnée | Champ | Extraction |
|---|---|---|
| Customer Info | `customfield_32118` | tableau wiki : Customer Ticket ID, Customer ID, Company Name, Contact, Related System |
| Severity | `customfield_11049` | `.value` (ex. `3 - Moderate`) |
| Master Ticket Number | `customfield_20207` | ServiceNow (ex. `MST0126896`) |
| Master Ticket Link | `customfield_20219` | HTML contenant l'URL ServiceNow |
| Customer Tickets | `customfield_20215` | nombre de tickets client rattachés |
| Support Contact | `customfield_20239` | nom du contact support |
| External ID | `customfield_11042` | clé du ticket miroir (ex. `GSUPPORT-48083`) |
| Jira Cloud Key | `customfield_36500` | HTML contenant le lien Jira Cloud |
| [G] Business Unit | `customfield_22703` | `.fields.summary` |
| [G] Product Line | `customfield_22712` | `.fields.summary` (ex. `ORBIS`) |
| [G] Product | `customfield_22709` | `.fields.summary` (ex. `ORBIS Medication`) |
| [G] Detected in Version | `customfield_22705` | `.fields.summary` (ex. `ORBIS Medication 03.17.09.02`) |
| [G] Team | `customfield_22715` | `.fields.summary` |
| [G] PM&E Team | `customfield_30100` | `.fields.summary` |
| Contains PID | `customfield_27001` | `.value` — si `Yes`, données patient présentes |
| ISP Impacted | `customfield_18624` | `.value` |

Commande d'extraction :

```bash
jq -r '
"summary: \(.fields.summary)",
"type: \(.fields.issuetype.name)",
"status: \(.fields.status.name)",
"priority: \(.fields.priority.name)",
"severity: \(.fields.customfield_11049.value // "n/a")",
"labels: \(.fields.labels | join(", "))",
"product: \(.fields.customfield_22709.fields.summary // "n/a")",
"productLine: \(.fields.customfield_22712.fields.summary // "n/a")",
"detectedInVersion: \(.fields.customfield_22705.fields.summary // "n/a")",
"team: \(.fields.customfield_22715.fields.summary // "n/a")",
"businessUnit: \(.fields.customfield_22703.fields.summary // "n/a")",
"masterTicket: \(.fields.customfield_20207 // "n/a")",
"externalId: \(.fields.customfield_11042 // "n/a")",
"containsPid: \(.fields.customfield_27001.value // "n/a")",
"customerInfo:", .fields.customfield_32118,
"description:", .fields.description
' /tmp/gsupport/<ISSUE_KEY>/issue.json
```

> **Attention aux données patient.** Si `Contains PID = Yes`, ou si la description contient un IPP,
> un nom ou une date de naissance : ne jamais recopier ces valeurs dans le fichier généré.
> Les remplacer par `<IPP masqué>`, `<patient masqué>`. Le fichier généré reste dans le repo.

## 2.2 — Lire TOUS les commentaires

Les commentaires portent souvent l'essentiel de l'analyse (échanges support ↔ client ↔ R&D,
compléments de reproduction, contre-exemples). Ils sont **obligatoires**, jamais optionnels.

```bash
curl -s -H "Authorization: Bearer ${JIRA_API_TOKEN}" -H "Accept: application/json" \
  "https://${JIRA_DOMAIN}/rest/api/2/issue/<ISSUE_KEY>/comment?maxResults=1000&orderBy=created" \
  -o /tmp/gsupport/<ISSUE_KEY>/comments.json

jq -r '.comments[] | "--- \(.author.displayName) | \(.created) ---\n\(.body)\n"' \
  /tmp/gsupport/<ISSUE_KEY>/comments.json
```

Vérifier que `.total` est bien couvert par `.comments | length` ; sinon paginer avec `startAt`.

Lire **chaque** commentaire, puis en produire une synthèse chronologique qui retient :
- les compléments de scénario ou de reproduction,
- les demandes d'information restées sans réponse,
- les analyses déjà faites côté support / R&D (et leurs conclusions),
- les contradictions avec la description initiale,
- les décisions déjà prises (ticket rejeté, workaround fourni, escalade…).

## 2.3 — Télécharger et lire TOUTES les pièces jointes

```bash
jq -r '.fields.attachment[] | "\(.id)\t\(.filename)\t\(.mimeType)\t\(.size)\t\(.content)"' \
  /tmp/gsupport/<ISSUE_KEY>/issue.json
```

Télécharger chaque pièce jointe via son champ `.content` (l'URL `/rest/api/2/attachment/content/<id>`
ne fonctionne pas sur cette instance) :

```bash
jq -r '.fields.attachment[] | "\(.content)\t\(.filename)"' /tmp/gsupport/<ISSUE_KEY>/issue.json \
| while IFS=$'\t' read -r url name; do
    curl -sL -H "Authorization: Bearer ${JIRA_API_TOKEN}" "$url" \
      -o "/tmp/gsupport/<ISSUE_KEY>/$name"
  done
```

Puis exploiter selon le type :

- **Images** (`.png`, `.jpg`, `.gif`) → les ouvrir avec l'outil `view` et **décrire ce qu'elles montrent**
  (écran concerné, message d'erreur affiché, état de la prescription, horodatage visible).
- **Word** (`.docx`) → extraire le texte, ces documents contiennent en général le scénario de
  reproduction pas à pas :

  ```bash
  python3 - "/tmp/gsupport/<ISSUE_KEY>/<fichier>.docx" <<'PY'
  import re, sys, zipfile
  z = zipfile.ZipFile(sys.argv[1])
  xml = z.read("word/document.xml").decode("utf8")
  xml = re.sub(r"</w:p>", "\n", xml)
  print(re.sub(r"<[^>]+>", "", xml))
  PY
  ```

  Un `.docx` embarque aussi ses captures d'écran dans `word/media/` — les extraire et les regarder,
  elles portent souvent le message d'erreur exact et les horaires du scénario :

  ```bash
  unzip -o -j "/tmp/gsupport/<ISSUE_KEY>/<fichier>.docx" 'word/media/*' \
    -d "/tmp/gsupport/<ISSUE_KEY>/media"
  ```

- **Excel** (`.xlsx`) → extraire via `python3` (`zipfile` + `xl/sharedStrings.xml`) ou signaler
  `Contenu non exploitable` si l'extraction échoue.
- **PDF** → `pdftotext` s'il est installé, sinon signaler `Contenu non exploitable`.
- **Logs / `.txt` / `.xml` / `.json`** → les lire, chercher les stacktraces et les codes d'erreur.
- **Archives** (`.zip`, `.tar`, `.tar.gz`/`.tgz`, `.gz`, `.7z`, `.rar`) → **obligatoirement les
  décompresser** et traiter chaque fichier extrait comme une pièce jointe à part entière
  (voir 2.3.1). Une archive non ouverte = analyse incomplète.

> Si une pièce jointe ne peut pas être lue, l'indiquer explicitement dans le rapport plutôt que
> de l'ignorer silencieusement — une pièce jointe non lue est une information manquante.

### 2.3.1 — Décompresser les archives (obligatoire)

Les clients joignent très souvent un `.zip` contenant les logs applicatifs, des captures d'écran,
des exports HL7/XML ou un document de reproduction. **Aucune archive ne doit rester fermée.**

Extraire chaque archive dans un sous-dossier portant son nom, puis lister le contenu :

```bash
cd "/tmp/gsupport/<ISSUE_KEY>"
for a in *.zip *.tar *.tar.gz *.tgz *.gz *.7z *.rar; do
  [ -e "$a" ] || continue
  dest="extracted/${a%%.*}"
  mkdir -p "$dest"
  case "$a" in
    *.zip)            unzip -o -q "$a" -d "$dest" ;;
    *.tar)            tar -xf "$a" -C "$dest" ;;
    *.tar.gz|*.tgz)   tar -xzf "$a" -C "$dest" ;;
    *.gz)             gunzip -c "$a" > "$dest/${a%.gz}" ;;
    *.7z)             7z x -y -o"$dest" "$a" >/dev/null 2>&1 || echo "7z indisponible : $a" ;;
    *.rar)            unrar x -o+ "$a" "$dest" >/dev/null 2>&1 || echo "unrar indisponible : $a" ;;
  esac
done
find extracted -type f -printf '%s\t%p\n' | sort -rn
```

Règles :

- **Récursivité** : si l'extraction produit elle-même une archive, la décompresser aussi
  (relancer la boucle jusqu'à ce qu'il n'en reste plus). Limiter à 3 niveaux d'imbrication.
- **Traiter chaque fichier extrait** selon son type avec les règles ci-dessus : images ouvertes
  avec `view`, `.docx`/`.xlsx` extraits, logs lus.
- **Gros fichiers de logs** : ne pas les lire intégralement. Chercher d'abord les occurrences
  utiles autour de l'horodatage et des identifiants du ticket :

  ```bash
  grep -rniE "ERROR|SEVERE|Exception|Caused by|<CODE_ERREUR>|<ID_PATIENT>" \
    /tmp/gsupport/<ISSUE_KEY>/extracted | head -100
  ```

  puis lire les blocs de contexte autour des hits pertinents (`grep -n -A 30`).
- **Archive protégée par mot de passe ou outil manquant** (`7z`, `unrar`) : le signaler
  explicitement dans le compte rendu et dans le rapport (`Archive non décompressée : <nom> — <raison>`),
  ne jamais l'ignorer silencieusement.
- Dans le rapport, chaque archive donne une entrée listant **les fichiers qu'elle contenait** et
  ce que chacun apporte.

## 2.4 — Liens distants et issues liées

```bash
curl -s -H "Authorization: Bearer ${JIRA_API_TOKEN}" -H "Accept: application/json" \
  "https://${JIRA_DOMAIN}/rest/api/2/issue/<ISSUE_KEY>/remotelink"
```

Recenser : liens Confluence, liens ServiceNow (Master Ticket), tickets Jira liés
(`fields.issuelinks[]`), ticket miroir (`External ID`), et tout `ORBISBUG`/`HORME` déjà créé.

Pour **chaque** ticket lié, suivre le lien sur **un niveau** et récupérer aussi sa **description** —
pas seulement son titre : un ticket lié contient fréquemment l'analyse déjà menée, le motif de
rejet ou le correctif appliqué.

```bash
curl -s -H "Authorization: Bearer ${JIRA_API_TOKEN}" -H "Accept: application/json" \
  "https://${JIRA_DOMAIN}/rest/api/2/issue/<LINKED_KEY>?fields=summary,status,resolution,description,components,labels,fixVersions"
```

Conclure explicitement : le sujet a-t-il **déjà** été traité, rejeté, ou corrigé dans une version ?

## Étape 3 — Sélection des repos et diagnostic — **orchestrateur**

Cette étape reste chez l'orchestrateur : elle est peu volumineuse, et elle peut avoir à
**questionner l'utilisateur** (repo requis manquant, branche approchante à confirmer), ce qu'un
sous-agent ne sait pas faire. Elle produit le contexte exact que recevront les agents de l'étape 4 :
**repo + branche résolue**.

### 3.1 — Choisir les repos

**Partir de la pré-analyse (étape 1b) si elle a été renseignée** : un domaine imposé remplace le
routage ci-dessous, une couche annoncée et des repos exclus retirent d'office des candidats. Ne
réexécuter le routage complet que sur ce qui reste ouvert.

#### Router par domaine métier

`config.json` porte une table `domains` : chaque domaine décrit un périmètre fonctionnel avec ses
`aliases` (le vocabulaire du **client**, en français, anglais et allemand), les `repos` concernés,
des `paths`, des `i18nBundles` et des `grepSeeds`.

Confronter le symptôme et le message d'erreur aux `aliases`, puis retenir le ou les domaines qui
correspondent :

```bash
jq -r '.domains[] | "\(.name)\t\(.label)\t\(.aliases | join(" | "))"' "$SKILL_DIR/config.json"
```

Les tickets GSUPPORT arrivent dans la langue du client : c'est **son** vocabulaire qu'il faut
reconnaître, pas le nom technique du module. « Absetzen », « discontinue » et « stopper la ligne »
désignent le même domaine.

Le domaine retenu donne les repos, et surtout les `paths` / `grepSeeds` transmis aux agents de
l'étape 4 — c'est ce qui les empêche de partir en recherche large.

> **Ce sont des indications, jamais un filtre.** Si aucun domaine ne correspond, ou si un agent ne
> trouve rien dans les `paths` annoncés, il doit chercher au-delà. Un périmètre figé produirait des
> `Aucun code pertinent identifié.` faussement rassurants — le pire résultat possible pour ce skill.
>
> Quand une analyse révèle qu'un domaine a mal routé (alias manquant, chemin obsolète, `grepSeed`
> qui ne renvoie plus rien), **corriger `config.json` dans la foulée** et le mentionner à
> l'utilisateur. Sans entretien, cette table sera fausse en quelques mois.

#### Traduire le vocabulaire du client

Un ticket client parle en jargon de service, pas en noms de classes. `config.json` porte un
`glossary` qui fait le pont : chaque entrée donne les `terms` employés par le client, leur
`meaning`, le `technical` correspondant et, quand elle existe, le `domain` visé.

```bash
jq -r '.glossary[] | "\(.terms | join(" / "))\t→ \(.technical)\t[\(.domain // "-")]"' \
  "$SKILL_DIR/config.json"
```

Faire cette traduction **avant** de router et avant tout `git grep` : chercher « plan de soins »
dans le code ne donnera jamais rien, `DirectAdministration` si. Une entrée du glossaire peut
désigner directement un domaine, ce qui règle le routage.

Comme pour les domaines, entretenir : un terme client mal compris pendant une analyse doit être
ajouté ici dans la foulée.

#### Compléter par les descriptions de repos

Un ticket peut ne relever d'aucun domaine, ou déborder du sien. Confronter alors le symptôme aux
`description` des repos, et retenir les repos pertinents. Annoncer la sélection et la justifier en
une ligne par repo. Commencer par le plus probable.

**Écarter d'emblée les repos `optIn: true`** de cette confrontation : leur `description` est
attirante — celle de `orme-pgd-config` parle de configuration, ce que fait la moitié des tickets
GSUPPORT — alors que leur `optInCondition` est bien plus étroite. Ne les rappeler qu'après coup, si
la condition est explicitement remplie.

#### Repos soumis à une version

Un repo peut n'être valable que pour certaines versions : il porte alors un champ `versionRange`
dans `config.json` (`>=3.22`, `<3.22`, `>=3.17 <3.22`…). **La règle est dans le fichier, pas ici** :
ne jamais réénoncer une correspondance version → repo en dur, elle divergerait du config.

La version de référence est **`[G] Detected in Version`** (`customfield_22705`, ex.
`ORBIS Medication 03.17.09.02` → `3.17`) — en extraire les deux premiers segments :

```bash
VERSION=$(jq -r '.fields.customfield_22705.fields.summary // ""' \
  /tmp/gsupport/<ISSUE_KEY>/issue.json \
  | grep -oE '[0-9]+\.[0-9]+' | head -1 | sed 's/^0*//;s/\.0*/./')
```

Filtrer ensuite les repos applicables. Un repo sans `versionRange` vaut pour toutes les versions :

```bash
jq -r --arg v "$VERSION" '
  def num: split(".") | (.[0]|tonumber) * 1000 + (.[1]|tonumber);
  def sat($r): $r
    | split(" ") | map(select(length > 0))
    | all(
        capture("^(?<op>>=|<=|>|<|=)(?<ver>[0-9]+\\.[0-9]+)$") as $c
        | ($v|num) as $a | ($c.ver|num) as $b
        | if   $c.op == ">=" then $a >= $b
          elif $c.op == "<=" then $a <= $b
          elif $c.op == ">"  then $a >  $b
          elif $c.op == "<"  then $a <  $b
          else $a == $b end
      );
  .repositories[]
  | select((has("versionRange") | not) or sat(.versionRange))
  | "\(.name)\t\(.description)"
' "$SKILL_DIR/config.json"
```

Deux repos aux `versionRange` complémentaires couvrent le même périmètre à des époques
différentes : **n'en fouiller qu'un**, celui que le filtre retient. C'est aujourd'hui le cas de
`orme-medication-legacy` et `orme-global-repo`. Indiquer dans le rapport la version retenue et le
repo correspondant.

Si la version détectée est absente ou illisible, ne pas filtrer : retenir le repo dont le
`versionRange` couvre les versions les plus récentes, et **le signaler explicitement comme une
hypothèse** dans le rapport.

### 3.2 — Se placer sur la branche de la version, sans rien casser

**Ne jamais chercher dans les fichiers du disque.** Les repos locaux sont sur des branches
quelconques (ticket en cours, migration, version différente de celle du client) et peuvent porter
du travail non commité. Chercher dedans produirait une analyse du mauvais code, donc une
qualification fausse.

**Ne jamais faire de `git checkout`, `git switch`, `git stash` ni `git worktree`** dans les repos
de l'utilisateur. La recherche se fait **directement sur les références distantes**, en lecture
seule : branche courante, `HEAD`, stashes et fichiers modifiés restent intacts.

```bash
git -C "$REPO" grep -n "<motif>" "origin/<branche>" -- '<filtre>'   # rechercher
git -C "$REPO" show "origin/<branche>:<chemin>"                     # lire un fichier
git -C "$REPO" ls-tree -r --name-only "origin/<branche>"            # lister les fichiers
git -C "$REPO" log -S "<motif>" "origin/<branche>" -- '<chemin>'    # tracer une regression
```

**Pourquoi en local et pas via l'API GitHub** — la recherche de code GitHub n'indexe que la
**branche par défaut** du dépôt (`main/develop`) et n'accepte aucun filtre de branche : elle
renverrait le code le plus récent au lieu de celui de la version du client, ce que toute cette
section vise justement à éviter. S'ajoutent un quota de 10 recherches/minute contre ~0,15 s par
`git grep` local. **Ne pas remplacer ces commandes par une recherche GitHub.**

#### Résoudre la branche depuis la version

Les branches de version suivent le motif `<clé>/develop`, où la clé encode la version sur 7
chiffres (`major` 1 + `minor` 2 + `patch` 2 + `build` 2), `X` servant de joker :
`03.17.09.02` → `3170902` → `317XXXX/develop`.

Retenir la branche **la plus spécifique** qui correspond (une clé exacte prime sur un joker) :

```bash
pick_branch() {
  local repo="$1" version="$2" key best="" pat re xs bxs
  key=$(echo "$version" \
        | grep -oE '[0-9]{2}\.[0-9]{2}\.[0-9]{2}\.[0-9]{2}|[0-9]+\.[0-9]+' \
        | head -1 | tr -d '.' | sed 's/^0//')
  while read -r b; do
    pat="${b%%/develop}"; pat="${pat#origin/}"
    case "$pat" in (*[!0-9X]*|"") continue;; esac
    re="^${pat//X/[0-9]}$"
    if [[ "$key" =~ $re ]]; then
      xs=${pat//[!X]/}; bxs=${best//[!X]/}
      { [ -z "$best" ] || [ ${#xs} -lt ${#bxs} ]; } && best="$pat"
    fi
  done < <(git -C "$repo" branch -r | grep -E '/develop$' | tr -d ' ')
  echo "$best"
}
```

Correspondances validées : `03.17.09.02` → `317XXXX`, `03.21.02.05` → `32102XX`,
`03.21.00.01` → `3210001` (exacte, préférée à `32100XX`).

#### Rafraîchir les références

Avant tout diagnostic et toute recherche, mettre à jour les refs distantes de **chaque repo
présent**. `fetch` ne touche ni la branche courante, ni le working tree, ni les stashes :

```bash
git -C "$REPO" fetch --quiet origin
```

#### Diagnostic des repos — à afficher avant toute recherche

Après le `fetch` (sinon une branche récente paraîtra absente à tort), dresser l'état des repos et
**l'afficher à l'utilisateur** : il doit savoir sur quoi l'analyse s'appuie, et ce qui lui manque.

```bash
printf '%-28s %-9s %-16s %s\n' REPO PRESENT BRANCHE STATUT
jq -r '.repositories[] | "\(.name)\t\(.path)\t\(.url // "")"' "$SKILL_DIR/config.json" |
while IFS=$'\t' read -r name path url; do
  dir="$REPOS_DIR/$path"
  if [ ! -d "$dir/.git" ]; then
    printf '%-28s %-9s %-16s %s\n' "$name" "non" "-" "MANQUANT : git clone $url"
  else
    b=$(pick_branch "$dir" "$VERSION")
    if [ -n "$b" ]; then
      printf '%-28s %-9s %-16s %s\n' "$name" "oui" "$b/develop" "OK"
    else
      printf '%-28s %-9s %-16s %s\n' "$name" "oui" "-" "pas de branche pour cette version"
    fi
  fi
done
```

Interpréter chaque cas :

| Cas | Signification | Conduite à tenir |
|---|---|---|
| `OK` | repo cloné et branche de la version disponible | analyser |
| `pas de branche pour cette version` | repo cloné mais la version n'y existe pas | souvent normal (repo plus récent que la version, ou repo exclu par son `versionRange`) — proposer la branche la plus proche et demander confirmation |
| `MANQUANT` | repo absent du poste | donner la commande `git clone` exacte |

**Distinguer le nécessaire du superflu.** Croiser ce diagnostic avec les repos retenus à
l'étape 3.1 : un repo manquant mais non pertinent pour ce ticket ne doit pas inquiéter
l'utilisateur. Formuler par exemple :

- *« `orme-global-repo` est requis pour ce ticket (version 3.17) et il est absent :
  `git clone git@github.com:dedalus-cis4u/orme-global-repo.git` dans `<reposDir>`. »*
- *« `orme-pgd-config` est absent mais n'est pas nécessaire ici. »*

Si un repo **requis** manque, proposer à l'utilisateur de le cloner (commande fournie), puis
attendre sa réponse. S'il refuse ou ne peut pas, poursuivre en excluant ce repo, et écrire dans le
rapport ce qui n'a pas pu être vérifié à cause de cette absence — une conclusion tirée sans un repo
requis doit voir sa confiance abaissée.

#### Branche absente

Vérifier l'existence avant toute recherche :

```bash
git -C "$REPO" rev-parse --verify -q "origin/<branche>" >/dev/null || echo "ABSENTE"
```

Si la branche de la version n'existe pas dans un repo, c'est souvent **normal** : un repo dont le
`versionRange` exclut la version du client n'a par construction aucune branche pour elle. Dans ce
cas :

1. Ne pas se rabattre silencieusement sur `main/develop` — le code y est plus récent que celui du
   client et mènerait à une conclusion erronée.
2. Le signaler, proposer la branche existante la plus proche, et **demander confirmation** avant
   de l'utiliser.
3. Si l'utilisateur refuse, exclure ce repo et l'indiquer dans le rapport.

#### Tracer

Le rapport doit indiquer, **pour chaque repo fouillé, la branche réellement analysée**, ainsi que
la version dont elle découle. Sans cette information, une conclusion n'est pas vérifiable.

## Étape 4 — Investigation du code — **déléguée, un sous-agent par repo**

Une fois les repos retenus et leur branche résolue (étape 3), lancer **un sous-agent `explore` par
repo**, tous **en parallèle** : les repos sont indépendants, rien ne justifie de les enchaîner.
Chacun porte le nom `code-<repo>`, avec la branche analysée dans sa `description`.

Chaque agent est lancé avec le modèle et le `reasoningEffort` de `agents.codeInvestigate` : c'est
le bloc qui demande le plus de raisonnement, et le seul où un modèle fort change réellement la
qualité de la conclusion.

Chaque agent écrit `/tmp/gsupport/<ISSUE_KEY>/compte-rendu-code-<repo>.md` et ne renvoie qu'une synthèse
de 30 lignes maximum.

### Prompt à fournir à chaque agent

L'agent est sans mémoire : sans ces éléments, il partira en recherche large, exactement ce que
cette étape interdit. Le prompt doit contenir :

| Élément | Pourquoi |
|---|---|
| Chemin absolu du repo et **branche résolue** (`origin/<branche>`) | il ne doit ni redeviner la branche ni toucher au working tree |
| Version détectée du client | pour l'analyse de régression |
| Symptôme en trois phrases + **message d'erreur exact** | son point d'entrée |
| Les « Pistes de recherche » du `compte-rendu-jira.md` | les motifs `git grep` à essayer en premier |
| Les `grepSeeds`, `paths` et `i18nBundles` du domaine retenu | ses points de départ vérifiés dans ce repo |
| Le champ `i18nHint` de `config.json` | où chercher un libellé client (étape 4.1) |
| Scénario de reproduction résumé | pour confronter la règle trouvée au cas client |
| La chaîne de recherche 4.1 → 4.6 et les consignes de recherche ci-dessous | sa méthode |
| Le rôle du repo (`description` de `config.json`) | pour cadrer son périmètre |
| La **pré-analyse de l'utilisateur** (étape 1b), si renseignée : couche, piste | l'oriente d'emblée ; préciser que c'est une hypothèse à confirmer, pas une consigne, et qu'il doit **signaler** s'il ne trouve rien dans ce périmètre plutôt que de conclure à l'absence de code pertinent |

Récupérer les éléments du domaine pour un repo donné :

```bash
jq -r --arg d "<domaine>" --arg r "<repo>" '
  .domains[] | select(.name == $d)
  | "paths:\n  " + ((.paths // []) | join("\n  "))
  + "\ni18nBundles:\n  " + ((.i18nBundles // []) | join("\n  "))
  + "\ngrepSeeds:\n  " + ((.grepSeeds // []) | join("\n  "))
' "$SKILL_DIR/config.json"
```

Les `paths` d'un domaine couvrent l'ensemble de ses repos : **un chemin inexistant dans le repo
confié à l'agent est simplement ignoré**, ce n'est pas une anomalie. Le préciser dans le prompt,
sinon l'agent perdra du temps à s'en inquiéter.

Rappeler enfin que ces éléments sont des **amorces, pas des limites** : si les `grepSeeds` ne
donnent rien, l'agent doit élargir et consigner les motifs essayés dans ses
`## Pistes non concluantes`.

Y ajouter les consignes communes, et en particulier l'interdiction stricte de toute commande
modifiant le repo (`checkout`, `switch`, `stash`, `worktree`, `reset`, `pull`) : ces repos sont
ceux de l'utilisateur, avec du travail en cours dessus.

### Structure du compte rendu attendu

```markdown
# Compte rendu code — <repo> @ origin/<branche>
## Chaîne de raisonnement   <message d'erreur → front → REST → métier → données>
## Fichiers retenus         <une section par fichier : chemin:lignes, rôle, extrait 10–30 lignes>
## Condition exacte qui produit le symptôme
## Version et régression    <la règle existe-t-elle déjà sur cette branche ? git log -S / diff>
## Verdict du repo          <ce que ce repo établit, et ce qu'il ne permet pas de conclure>
## Pistes non concluantes   <motifs cherchés sans résultat — évite qu'on les recherche deux fois>
```

Si l'agent ne trouve rien, il écrit `Aucun code pertinent identifié.` **et** la liste des motifs
essayés : une recherche infructueuse documentée vaut mieux qu'un silence.

### Ce que l'orchestrateur en fait

Il collecte les synthèses, puis **relit les comptes rendus fichier par fichier au moment de rédiger
l'étape 9**. Un verdict de repo qui contredit un autre est un signal fort : le dire dans la
qualification plutôt que de trancher en silence.

### Second passage — les repos `optIn`

Les repos `optIn` ne sont pas lancés avec la première vague. C'est l'issue de cette vague qui
décide de les réveiller, avant de passer à la qualification :

| Constat dans les comptes rendus de la première vague | Second passage |
|---|---|
| Le libellé client, la clé i18n ou la règle n'a pas été retrouvé dans le module fonctionnel | agent sur `orme-common` (bundles partagés `backend/legacy/shared`, briques transverses) |
| La chaîne de raisonnement aboutit à un paramètre client, un droit ou un profil | agent sur `orme-pgd-config` |

Ce second passage suit exactement les mêmes règles que le premier : même nommage
(`investigation-code-<repo>`), même modèle `agents.codeInvestigate`, même compte rendu
`compte-rendu-code-<repo>.md`. Lui transmettre en plus les **`## Pistes non concluantes`** des
agents de la première vague : c'est précisément ce qu'il ne faut pas rechercher une seconde fois.

Ne pas déclencher de second passage quand la première vague a déjà établi une chaîne complète —
il n'apporterait rien et retarderait la qualification. À l'inverse, conclure
`Aucun code pertinent identifié.` sans avoir tenté `orme-common` alors que le libellé restait
introuvable est une erreur d'analyse : le rapport doit alors le dire explicitement.

### Chaîne de recherche

Suivre cet ordre : chaque étape fournit le point d'entrée de la suivante. Ne pas sauter d'étape,
ne pas partir en recherche large.

**4.1 — Message d'erreur et libellés**
Point d'entrée le plus efficace : le **texte exact** remonté par le client (description,
commentaire, ou capture d'écran). Le chercher dans les bundles i18n pour retrouver sa **clé**, puis
chercher cette clé dans le code.

Où chercher exactement dépend du produit : suivre le champ `i18nHint` de `config.json` et les
`i18nBundles` du domaine plutôt que de supposer un emplacement. Sur ORME aujourd'hui, les libellés
affichés par le front Angular viennent des `.properties` du **backend** — chercher un `fr.json`
Angular ne donnerait rien.

Un libellé introuvable dans le repo confié à l'agent n'est **pas** une impasse : il vit peut-être
dans les bundles partagés de `orme-common`. L'agent l'écrit noir sur blanc dans son
`## Verdict du repo` (`libellé "<texte>" absent de ce repo`) et rend la main — c'est ce constat qui
déclenche le second passage côté orchestrateur.

**4.2 — Écran / composant front**
Si un écran est identifié : localiser le composant Angular (ou GWT) qui l'affiche, son template
et son service.

**4.3 — Point d'entrée REST**
Depuis le service front : retrouver l'endpoint appelé côté back (`@Path`, `@GET`, `@POST`, DTO
correspondant).

**4.4 — Logique métier**
Depuis le contrôleur : remonter aux services et **à la condition exacte qui lève l'erreur**.
Confronter cette règle au scénario décrit par le client.

**4.5 — Données / persistance**
Si le problème est lié aux données : entités JPA, requêtes, migrations, contraintes. Utiliser le
schéma DB au `grep` si `config.json` en déclare un.

**4.6 — Configuration et tests**
Fichiers de configuration, feature flags, paramétrage client. Puis les tests existants qui
couvrent (ou devraient couvrir) le comportement : un test qui affirme le comportement dénoncé
oriente fortement vers « comportement attendu ».

### Consignes de recherche

- Toutes les recherches passent par `git grep` / `git show` sur `origin/<branche>` — **jamais** par
  une lecture directe des fichiers du disque, qui reflètent une autre branche.
- Motifs ciblés, jamais de recherche large ; limiter les résultats (`head_limit`).
- `git ls-tree -r --name-only origin/<branche>` pour trouver les fichiers par nom, puis
  `git show origin/<branche>:<chemin>` pour lire la zone utile.
- Java : `.java` (classes, méthodes, annotations) · Angular : `.ts`, `.html` · SQL : `.sql` ·
  config : `.properties`, `.yml`, `.json` — via le filtre `-- '<motif>'` de `git grep`.

### Version et régression

Vérifier la **version détectée** (`[G] Detected in Version`) : la règle en cause existe-t-elle déjà
sur la branche de cette version, ou a-t-elle été introduite / corrigée depuis ? Le client parle
souvent de « régression » — le confirmer ou l'infirmer en comparant la branche de sa version à une
branche plus ancienne :

```bash
git -C "$REPO" log -S "<motif>" --oneline "origin/<branche>" -- '<chemin>'
git -C "$REPO" diff "origin/<branche ancienne>" "origin/<branche client>" -- '<chemin>'
```

### Restitution

Pour chaque fichier retenu : repo, chemin, plage de lignes, extrait (10–30 lignes max) et
explication de son rôle dans le symptôme. Restituer le résultat comme une **chaîne de raisonnement
traçable** (message d'erreur → front → REST → service → données), pas comme une liste de fichiers.

Cette restitution va dans le **compte rendu du repo**, pas dans la réponse de l'agent.

Si rien n'est trouvé : écrire `Aucun code pertinent identifié.` et préciser les repos fouillés.

## Étape 5 — Qualification — **orchestrateur, jamais déléguée**

C'est la section centrale du skill et sa raison d'être : décider **ce qu'est** la demande avant
de décider quoi en faire.

Elle s'appuie sur les comptes rendus produits aux étapes 2 et 4. Avant de trancher, relire les sections
utiles : `## Symptôme` et `## Commentaires` du `compte-rendu-jira.md`, et `## Verdict du repo` de chaque
`compte-rendu-code-<repo>.md`.

Deux réflexes propres au mode délégué :

- **Un compte rendu muet n'est pas une preuve d'absence.** Si un agent a rendu `Aucun code pertinent
  identifié.`, regarder ses `## Pistes non concluantes` : cherchait-il les bons motifs ? Si le
  message d'erreur exact n'y figure pas, la recherche était mal amorcée — le refaire soi-même sur
  ce motif avant de conclure.
- **Deux verdicts de repos qui se contredisent** sont une information, pas un bruit à arbitrer en
  silence : le mentionner dans « Éléments contradictoires ou incertains » et baisser la confiance.

Abaisser également la confiance si un repo requis était absent, ou si une pièce jointe n'a pas pu
être lue.

Choisir **une** catégorie principale, avec un niveau de confiance (Élevée / Moyenne / Faible) et
les éléments concrets qui la justifient (extrait de code, commentaire, capture, scénario) :

| Catégorie | Signification | Suite à donner |
|---|---|---|
| Bug dans notre code | Le comportement contredit la règle métier attendue | Créer un `ORBISBUG` |
| Configuration / données | Paramétrage, droits, données client ou environnement en cause | Retour au support / à l'équipe déploiement |
| Comportement attendu | Le produit fonctionne comme spécifié, le client attendait autre chose | Réponse fonctionnelle argumentée au client |
| Évolution / changement de comportement | La demande sort du comportement spécifié | Créer un `HORME` (à arbitrer produit) |
| Informations insuffisantes | Scénario non reproductible en l'état | Questions précises à poser au client |

Toujours indiquer :
- ce qui **soutient** la catégorie retenue,
- ce qui **la contredit** ou reste incertain,
- les catégories écartées et pourquoi.

Ne jamais conclure « bug » par défaut faute d'information : c'est le cas
`Informations insuffisantes`.

## Étape 6 — Hypothèses techniques

Uniquement si la catégorie est `Bug dans notre code` ou `Évolution`.
Lister 2 à 4 hypothèses classées de la plus à la moins probable :

- **Probabilité** : Élevée / Moyenne / Faible
- **Mécanisme** : ce qui se passe réellement
- **Localisation** : fichier + méthode (+ ligne si connue)
- **Correction envisagée** : changement concret
- **Impact / risque** : effets de bord, périmètre de régression

## Étape 7 — Informations manquantes et prochaines actions

### Informations manquantes

Pour **chaque** information qui manque à la conclusion, préciser trois choses :

| Information | Pourquoi elle est nécessaire | Qui peut la fournir |
|---|---|---|

Sans cette table, une catégorie `Informations insuffisantes` n'est pas exploitable.

### Prochaines actions

- Questions précises à poser au client (numérotées, chacune rattachée à une ligne du tableau ci-dessus).
- Vérifications à faire en interne (base, logs, environnement, version livrée).
- Brouillon de réponse support (ton factuel, sans jargon interne, en anglais si le ticket est en anglais).
- Si un `ORBISBUG` ou un `HORME` est à créer : titre proposé et résumé prêt à copier.

## Étape 8 — Sauvegarder le rapport

Un rapport existant n'est **jamais** écrasé : il constitue l'historique de l'analyse.

Le dossier de sortie vient de `reportDir` dans `config.json` (relatif à la racine du dépôt courant) :

```bash
SKILL_DIR=$(dirname "$(readlink -f ~/.copilot/skills/gsupport-analyze/SKILL.md)")
REPO_ROOT=$(git rev-parse --show-toplevel)
REPORT_DIR="${REPO_ROOT}/$(jq -r '.reportDir // ".copilot/analyses"' "$SKILL_DIR/config.json")"
mkdir -p "$REPORT_DIR"

REPORT="${REPORT_DIR}/<ISSUE_KEY>-analyse.md"
n=2
while [ -e "$REPORT" ]; do
  REPORT="${REPORT_DIR}/<ISSUE_KEY>-analyse-${n}.md"
  n=$((n + 1))
done
echo "$REPORT"
```

Écrire le contenu de l'étape 9 dans `$REPORT`, puis afficher :

```
Rapport sauvegardé : <chemin>
```

Si un rapport précédent existe, le signaler et indiquer **ce qui a changé** depuis.

En cas d'échec d'écriture : afficher `Impossible de sauvegarder le rapport : <erreur>` et continuer.

## Étape 9 — Structure du rapport

Même contenu dans le fichier et dans le chat.

```markdown
# <ISSUE_KEY> — <SUMMARY>

| | |
|---|---|
| Type | <ISSUE_TYPE> |
| Statut | <STATUS> |
| Priorité | <PRIORITY> |
| Sévérité | <SEVERITY> |
| Créé le | <CREATED> |
| Mis à jour le | <UPDATED> |
| Jira | https://<JIRA_DOMAIN>/browse/<ISSUE_KEY> |

## Contexte client

| | |
|---|---|
| Client | <CUSTOMER_COMPANY_NAME> |
| Ticket client | <CUSTOMER_TICKET_ID> |
| Contact | <CONTACT_PERSON> |
| Contact support | <SUPPORT_CONTACT> |
| Master ticket | <MASTER_TICKET_NUMBER> — <MASTER_TICKET_LINK> |
| Labels | <LABELS> |
| Données patient | <CONTAINS_PID> |

## Contexte produit

| | |
|---|---|
| Business Unit | <BUSINESS_UNIT> |
| Product Line | <PRODUCT_LINE> |
| Produit | <PRODUCT> |
| Version détectée | <DETECTED_IN_VERSION> |
| Équipe | <TEAM> |

## Symptôme

### Description client
<description reformatée en markdown, données patient masquées>

### Scénario de reproduction
<étapes numérotées, consolidées depuis la description, les commentaires et les documents joints>

### Résultat actuel
<...>

### Résultat attendu
<...>

### Message d'erreur
```
<message d'erreur exact, tel que remonté>
```

## Commentaires
<synthèse chronologique — auteur, date, apport du commentaire>
<ou "Aucun commentaire.">

## Pièces jointes
<pour chaque pièce jointe : nom, type, auteur, date, et ce qu'elle apporte>
<pour les images : description de ce qui est visible>
<pour les documents : extrait utile>
<pour les archives : liste des fichiers extraits et apport de chacun>
<ou "Aucune pièce jointe.">

## Liens
### Tickets liés
<clé — titre — statut, et relation>
### Documentation / liens externes
<titre → URL>
<ou "Aucun.">

## Investigation du code

**Version de référence** : <[G] Detected in Version> → clé `<clé>`
**Domaine métier retenu** : <domaine(s) de `config.json`, ou "aucun — routage par description de repo">

| Repo | Requis | Branche analysée | Remarque |
|---|---|---|---|
| <repo> | oui / non | `origin/<branche>` | <exacte / plus proche confirmée / absent du poste / exclu / opt-in non retenu> |

**Repos requis manquants** : <liste + commande `git clone`, ou "aucun">
**Non vérifié faute de repo** : <ce qui n'a pas pu être confirmé, ou "rien">
**Périmètre restreint par l'utilisateur** : <couche / domaine / repos exclus / piste fournie à
l'étape 1b, ou "non — routage automatique complet">

### Chaîne de raisonnement
1. Point de départ : <message d'erreur / écran / libellé>
2. Front : <composant>
3. REST : <endpoint>
4. Métier : <service + condition qui lève l'erreur>
5. Données / configuration : <...>

### <repo> `origin/<branche>` — <chemin/du/fichier>:<lignes>
Rôle : <...>

```<langage>
<extrait>
```

### Version et régression
<la règle existe-t-elle sur la branche de la version détectée ? comparaison avec une branche
antérieure, confirmation ou infirmation de la régression>

<ou "Aucun code pertinent identifié." + repos et branches fouillés>
<ou "Investigation du code non réalisée : repos non disponibles">

## Qualification

**Catégorie retenue** : <catégorie>
**Confiance** : Élevée | Moyenne | Faible

**Justification**
<éléments concrets qui soutiennent la catégorie>

**Éléments contradictoires ou incertains**
<...>

**Catégories écartées**
- <catégorie> : <raison>

**Suite à donner** : <ORBISBUG | HORME | retour support | réponse client | demande d'information>

## Hypothèses techniques
<uniquement si bug ou évolution>

### Hypothèse 1 — <titre court>
- **Probabilité** : <...>
- **Mécanisme** : <...>
- **Localisation** : <repo / fichier / méthode>
- **Correction envisagée** : <...>
- **Impact / risque** : <...>

## Informations manquantes

| Information | Pourquoi elle est nécessaire | Qui peut la fournir |
|---|---|---|
| <...> | <...> | <...> |

<ou "Aucune — l'analyse est concluante en l'état.">

## Prochaines actions

### Questions au client
1. <...>

### Vérifications internes
- <...>

### Brouillon de réponse support
<texte prêt à envoyer>

### Ticket à créer
- **Type** : <ORBISBUG | HORME | aucun>
- **Titre** : <...>
- **Résumé** : <...>

## Traçabilité
Modèles : orchestrateur `<modèle de session>` · collecte `<agents.jiraCollect.model>` ·
code `<agents.codeInvestigate.model>`
<mention si un modèle configuré n'était pas disponible et a été remplacé par le modèle par défaut>

Digests de collecte (non versionnés, effacés au redémarrage) :
- `/tmp/gsupport/<ISSUE_KEY>/compte-rendu-jira.md`
- `/tmp/gsupport/<ISSUE_KEY>/compte-rendu-code-<repo>.md`
```

---

## Gestion des erreurs

| Situation | Message |
|---|---|
| Préfixe différent de `GSUPPORT-` | `Préfixe inattendu. Utiliser /task-analyze pour HORME-/ORBISBUG-.` |
| Ticket introuvable | `Ticket <KEY> introuvable sur ${JIRA_DOMAIN}` |
| Token absent | `Configurer JIRA_API_TOKEN dans ~/.bashrc` |
| Pièce jointe illisible | `Contenu non exploitable` (et le signaler dans le rapport) |
| Archive non décompressable (mot de passe, `7z`/`unrar` absent) | `Archive non décompressée : <nom> — <raison>` (et le signaler dans le rapport) |
| Aucun commentaire | `Aucun commentaire.` |
| Aucune piste dans le code | `Aucun code pertinent identifié.` |
| Écriture du rapport impossible | `Impossible de sauvegarder le rapport : <erreur>` |
| Sous-agent en échec ou sortie vide | Exécuter le bloc soi-même, sans relancer l'agent, et l'indiquer dans le rapport |

---

## Maintenir la documentation d'architecture

`ARCHITECTURE.md` est la vue d'ensemble du skill : c'est par lui que l'équipe comprend le
découpage orchestrateur / sous-agents. Une doc qui diverge du skill est pire que pas de doc —
elle fait raisonner sur un fonctionnement qui n'existe plus.

**Règle : toute modification de `SKILL.md` ou de la structure de `config.json` doit être
accompagnée de la mise à jour de `ARCHITECTURE.md` dans le même commit.**

Cela vaut aussi bien pour une modification humaine que pour une modification faite par un agent :
si l'agent édite le skill, il met à jour `ARCHITECTURE.md` avant de rendre la main, sans attendre
qu'on le lui demande.

### Quel changement impacte quel schéma

| Changement dans le skill | À répercuter dans `ARCHITECTURE.md` |
|---|---|
| Ajout, suppression ou renumérotation d'une étape | § 2 flowchart global, § 3 tableau « qui fait quoi » |
| Un bloc passe de l'orchestrateur à un sous-agent (ou l'inverse) | § 2, § 3, et la liste « ne se délègue jamais » |
| Nouveau fichier écrit dans `/tmp/gsupport/<KEY>/` | § 4 passage par fichiers |
| Nouveau type de pièce jointe ou nouvelle règle d'extraction | § 5 aiguillage des pièces jointes |
| Changement dans le routage (domaines, glossaire, `versionRange`, branche) | § 6 (texte et exemples de vocabulaire, pas un schéma) |
| Nouvelle catégorie de qualification ou nouveau garde-fou | § 7 |
| Nouveau cas d'erreur ou de reprise | § 8 tableau de reprise sur incident |
| Nouvelle clé structurante dans `config.json` | § 9 « ce qu'il faut entretenir », et § 2 si elle alimente une étape |

Ajouter une simple précision de rédaction dans une étape existante ne demande pas de toucher aux
schémas. Le déclencheur, c'est le **flux** : qui exécute quoi, dans quel ordre, avec quelles
entrées et quelles sorties.

### Vérifier les diagrammes avant de committer

Un diagramme Mermaid invalide ne s'affiche pas sur GitHub, il ne casse rien d'autre — donc
personne ne le remarque. Les valider explicitement :

```bash
cd skills/gsupport-analyze
rm -rf /tmp/mmd && mkdir -p /tmp/mmd

python3 - <<'PY'
import re, pathlib
src = pathlib.Path("ARCHITECTURE.md").read_text()
for i, block in enumerate(re.findall(r"```mermaid\n(.*?)```", src, re.S)):
    pathlib.Path(f"/tmp/mmd/d{i}.mmd").write_text(block)
PY

for f in /tmp/mmd/*.mmd; do
  npx -y @mermaid-js/mermaid-cli@11 -i "$f" -o "${f%.mmd}.svg" >/dev/null 2>&1 \
    || echo "Diagramme invalide : $f"
done
rm -rf /tmp/mmd
```

Enfin, si le changement modifie ce que le skill fait **pour l'utilisateur** (et pas seulement
comment il le fait), mettre aussi à jour la ligne du skill dans `skills/README.md`.
