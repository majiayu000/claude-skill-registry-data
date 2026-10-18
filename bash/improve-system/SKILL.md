---
name: improve-system
description: Analyse l'historique local des conversations Claude Code (fichiers .jsonl sous ~/.claude/projects/) pour repérer les corrections qui reviennent, les tâches répétées sur plusieurs sessions et les aveux de travail manuel, puis propose (et écrit après confirmation) les skills qui manquent dans ~/.claude/skills/. À utiliser quand l'utilisateur veut auditer son usage de Claude, trouver ce qu'il refait sans cesse ou créer des skills à partir de son usage réel, même sans prononcer le mot « skill ». À relancer régulièrement (par exemple deux fois par semaine).
---

# Improve System

Transforme l'historique de conversations en signal : ce qui échoue souvent, ce qui est refait de session en session, et quels skills n'existent pas encore.

## Confidentialité
Tout reste sur la machine. Le script ne fait aucun appel réseau. Les extraits de messages peuvent contenir des données personnelles : ne les recopie pas dans un fichier partagé ou un skill, et utilise `--no-examples` si l'utilisateur veut un résumé sans citations.

## Étape 1 : lancer le script
```bash
python3 scripts/scan_history.py --days 30          # lecture humaine
python3 scripts/scan_history.py --days 30 --json   # pour travailler dessus
```
Options : `--days N` (dernières semaines seulement), `--root DIR` (autre dossier d'historique), `--min-sessions N` (une tâche compte si elle apparaît dans au moins N sessions distinctes, 3 par défaut), `--no-examples`.
Ne lis jamais les `.jsonl` bruts : ils sont énormes. Travaille sur le résumé du script.
Si le résumé est vide ou trop court, dis-le : un historique de quelques jours ne donne pas de signal fiable.

## Étape 2 : interpréter
Le script détecte par mots-clés, il ne comprend pas. Relis les extraits et écarte le bruit : un « non » dans une phrase normale n'est pas une correction, une correction isolée n'est pas une erreur récurrente. Ne retiens que ce qui apparaît dans plusieurs sessions.

## Étape 3 : rapport en trois parties (dans la langue de l'utilisateur)
1. **Ce qui revient comme erreur** : corrections répétées et ce qu'elles révèlent (préférence jamais retenue, étape oubliée).
2. **Ce qui prend du temps sans raison** : tâches répétées sur plusieurs sessions, avec une estimation honnête du gain.
3. **Les skills qui manquent** : pour chaque motif solide (idéalement 3 sessions ou plus), un nom de skill, ce qu'il ferait et quand il se déclencherait.
Indique le niveau de confiance de chaque constat (« 2 fois, à surveiller » vaut mieux qu'un faux signal présenté comme certain).

## Étape 4 : écrire les skills
Pour les propositions les plus solides seulement, demande une confirmation, puis crée `~/.claude/skills/<nom>/SKILL.md` (frontmatter `name` + `description` qui dit quand déclencher, puis instructions). Si la tâche est scriptable de façon fiable, écris aussi un script. Dis ensuite quel skill a été créé et où.
