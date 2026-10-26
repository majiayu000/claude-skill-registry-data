---
name: daily-report
description: Write today's daily report in FRENCH, organized by project, under docs/reports/daily/. Use when the user says "daily report", "rapport quotidien", "standup", "what did I do today/yesterday", or wants a log of what changed. Built so nothing gets forgotten.
argument-hint: [optional date YYYY-MM-DD, default today]
allowed-tools: Read, Write, Glob, Grep, Bash(git log*), Bash(git diff*), Bash(git status*), Bash(date*), Bash(find*)
---

## Contexte (collecté avant lecture)

- Aujourd'hui : !`date +%F`
- Commits depuis minuit : !`git log --since=midnight --pretty=format:'%h %s (%an)' 2>/dev/null | head -50`
- Fichiers modifiés aujourd'hui : !`git log --since=midnight --stat --oneline 2>/dev/null | tail -60`
- En cours, non commité : !`git status --short 2>/dev/null | head -40`
- Nom du projet : !`basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"`

## Tâche

Écris `docs/reports/daily/<date>.md` (date = `$ARGUMENTS` ou aujourd'hui) **en français**, en suivant
EXACTEMENT le modèle `docs/templates/daily-report.md`. Le travail est **classé par projet** : un bloc
`### <emoji> <Nom du projet>` par projet sous « ✅ Travail effectué ».

Pour le projet courant, à partir du contexte git ci-dessus (ne jamais inventer d'activité) :

1. **Travail effectué** — les commits (hash + ce qu'ils changent en langage humain, pas le message
   brut), puis les fonctionnalités / améliorations. Mettre en gras les termes qui portent le sens :
   le rapport doit se survoler en dix secondes.
2. **Coordination** — échange client, arbitrage produit, décision de direction. Uniquement si cela a
   réellement eu lieu ; sinon supprimer la section.
3. **En cours** — la tâche en cours actuellement + le blocage éventuel **sur cette tâche précise**.
4. **Blocages** — problème technique, attente client, dépendance externe.
5. **Message pour le client** — un message clair et professionnel **que TU rédiges** au vu du
   rapport, prêt à envoyer (français, ton courtois, sans jargon technique, **sans pourcentages** :
   ce que le client peut voir, et ce dont on a besoin de lui).
6. **Suivi** — le tableau d'indicateurs, une ligne par chantier qui avance séparément (landing,
   front, back, refonte tarifaire…), adaptée au projet.

### La date du rapport = le jour où le travail a eu lieu

Le travail est parfois commité le lendemain. Ne pas se fier aveuglément à `git log` : recouper avec
l'horodatage des fichiers
(`find . -newermt "<date> 00:00" ! -newermt "<date+1> 00:00" -not -path "*/node_modules/*"`).
Si les commits portent une autre date que le travail, **le dire dans le rapport** plutôt que de le
masquer.

### Les chiffres du Suivi : estimer, sourcer, faire corriger

**Renseigne les chiffres** — ne laisse pas les champs vides — mais **jamais au doigt mouillé** :

- **Heures** : dérivées de l'amplitude réelle des horodatages de fichiers (premier → dernier).
- **Pourcentages** (par tranche de 10) : dérivés de ce que le code fait vraiment. Un catalogue écrit
  en dur et zéro appel réseau = back à **0 %**, pas 20 % par politesse. Mesurer l'avancement contre
  le **périmètre du produit visé**, pas contre le périmètre déjà livré.
- **Dire sur quoi repose l'estimation** quand ce n'est pas évident, pour que l'humain puisse corriger
  un chiffre plutôt que discuter avec une valeur nue. C'est lui qui tranche.

Règles :

- **Si le fichier du jour existe déjà**, mets à jour / ajoute uniquement la partie du projet courant
  et conserve les autres parties (projets) intactes.
- Garde-le court et honnête : lisible en moins d'une minute. Liens vers commits/fichiers, pas de diff
  inline. Un blocage pré-existant se signale **comme pré-existant**.
- Écris le fichier, puis **renvoie seulement le chemin du fichier + 3 puces de résumé** (ne recopie
  pas tout le rapport dans le chat).

Astuce : se planifie bien en tâche programmée (« écris mon rapport quotidien chaque soir »).
