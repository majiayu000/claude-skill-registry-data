---
name: fin-de-tache
description: Ouvre et tient le compte rendu de complétude d'une tâche KLASSCI, pour ne jamais rendre un travail à moitié fait. À utiliser dès qu'une demande comporte plusieurs points, produit du code, des fichiers, des issues ou un livrable. Le hook Stop rappelle une fois les points non cochés avant de rendre la main. Use at the start of any multi-part task, not at the end.
---

# Fin de tâche

## Le défaut que ce skill supprime

Rendre la main sur un travail incomplet, et laisser l'utilisateur relancer — alors que ce qui manquait était **à portée** : une recherche internet, une rule déjà écrite, un agent adverse, une capture d'écran.

Le coût n'est pas le point oublié. C'est que l'utilisateur doit relire, constater le manque, et redemander. Il fait alors le travail de vérification à ma place.

## Quand ouvrir un compte rendu

**Ouvre-le** dès que la demande :

- comporte **plusieurs points distincts** — le cas le plus fréquent, et le plus souvent raté ;
- produit du code, un fichier, une issue, un artéfact, un déploiement ;
- demande une vérification, un audit, une recherche.

**N'en ouvre pas** pour une question, une explication, un échange conversationnel. Le hook ne se déclenche que si le fichier existe : pas de cérémonie sur ce qui n'en demande pas.

## Le geste qui compte : l'ouvrir au DÉBUT

Pas à la fin. Au début.

Le compte rendu sert d'abord à **découper la demande en points distincts avant de commencer**. C'est là que se joue la complétude : une demande longue contient souvent six ou huit demandes, et celle qu'on oublie est presque toujours l'avant-dernière, noyée au milieu d'une phrase.

Relis la demande et compte les verbes. Chaque verbe à l'impératif est un point.

Si la demande est assez large pour des **agents parallèles**, une architecture déjà écrite, ou un risque de couper une vue mobile : charger aussi le skill `orchestrate-until-done` tout de suite après avoir ouvert ce compte rendu. `/orchestrate` fait les deux.

## Le gabarit

Écrire dans `.claude/completude.md` (ignoré par git, donc jamais commité).

```markdown
# Compte rendu — <date> — <titre court>

## Demandé, mot pour mot
> <la demande citée, découpée point par point — ne pas paraphraser,
>  la paraphrase est l'endroit exact où un point disparaît>

## À livrer
- [ ] <un point par ligne, dans l'ordre de la demande>

## Vérifié, et comment
| Ce que j'affirme | Comment je le sais |
|---|---|
| … | lu dans `fichier:ligne` / source liée / exécuté |

## Non fait, et pourquoi
<vide au début ; se remplit seulement quand un point est écarté,
 avec la raison — jamais « pas eu le temps »>

## Moyens employés
- [ ] Recherche internet — ou : sans objet, parce que …
- [ ] Rules `.claude/rules/` et mémoire projet
- [ ] Agent `critique-transversale`
- [ ] `/thermo-review` — ou : exempté, parce que …
- [ ] Preuve d'écran (`/klassci-test-e2e`, capture réelle) — ou : sans objet, parce que …
```

Les quatre cases de « Moyens employés » se cochent **dans les deux cas** : employé, ou écarté avec la raison écrite sur la ligne. Ce qui est interdit, c'est de ne pas y avoir pensé.

## Avant de cocher le dernier point

Trois questions, dans cet ordre :

1. **Chaque point de « Demandé » a-t-il sa ligne dans « À livrer » ?** Relis la demande d'origine, pas ton résumé.
2. **Ce que j'ai livré, l'ai-je vérifié — ou est-ce que je le suppose ?** Un fichier écrit n'est pas un fichier qui marche. Un hook écrit n'est pas un hook testé.
3. **Ce que je m'apprête à déclarer bloqué l'est-il vraiment ?** Une recherche, une rule, un agent adverse répondent à la plupart des « je ne sais pas ».

## Quand un point ne peut pas être fait

Il ne reste pas coché : il **descend dans « Non fait, et pourquoi »**, avec la raison réelle. Le hook débloque, et l'utilisateur lit une décision explicite au lieu de découvrir un trou.

Une raison valable nomme l'obstacle : une décision qui lui appartient, une donnée qui n'existe pas, un outil absent de l'environnement, un risque qu'on refuse de prendre. « Pas eu le temps » n'en est pas une.

## Ce que le hook fait, et ne fait pas

`.claude/hooks/completude-check.sh`, branché sur `Stop` dans `.claude/settings.json`.

**Il interrompt une fois** si `.claude/completude.md` existe et contient une case non cochée, ou le marqueur `À COMPLÉTER`. Une fois, pas indéfiniment : c'est un rappel qui force à regarder la liste, pas un verrou.

**Il compte aussi les preuves.** À partir de trois points cochés, il exige que le
tableau « Vérifié, et comment » porte au moins une ligne pour deux cases. Une case
cochée est une auto-déclaration ; la ligne du tableau dit **par quel moyen on le
sait**, et c'est la seule chose qui la rend vérifiable.

> Pourquoi ce compte existe : le 14 septembre 2026, un dispositif entièrement coché
> citait six méthodes, fichiers et chiffres qui n'existaient pas — une méthode
> `generate()` absente, une rule inexistante, trois tailles de contrôleur recopiées
> d'un `CLAUDE.md` périmé. Toutes les cases étaient cochées. Aucune ne disait
> comment on le savait.

**Il ne peut pas** juger si le travail est bon. Un compte rendu tout coché, preuves
comprises, sur un travail bâclé passe. Le hook empêche l'oubli et l'affirmation sans
source, pas la complaisance — c'est la relecture adverse qui sert à ça.

Il se désactive au second passage (`stop_hook_active`) : une case qu'on n'arrive pas à cocher ne boucle pas indéfiniment. Ce n'est pas une porte de sortie, c'est une sécurité.

## Voir aussi

- `.claude/hooks/completude-check.sh` — le hook
- `.claude/agents/critique-transversale.md` — le second angle
- `/thermo-review` — la revue obligatoire avant commit, fusion et déploiement
- `/klassci-test-e2e` · `/klassci-user-tutorial` — les deux sources de preuve d'écran
- `.claude/rules/pre-merge-checklist.md` · `.claude/rules/feature-delivery-methodology.md`
