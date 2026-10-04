---
name: humanize-writing
description: Passe curative anti-détection-IA en 8 passes pour tout texte {{COMPANY_NAME}} qui « sonne IA » — structure formulaïque, inflation d'importance, vocabulaire LLM, tics grammaticaux, rythme métronome, hedging, transitions répétitives, absence de voix. Utiliser quand un texte existant doit être humanisé (« ça sonne ChatGPT », « trop robotique », « humanise ça »), ou comme passe finale invoquée par copy-editing. COMPLÈTE la section 2 de 01-brand/checklist-pre-composition.md (préventive, à charger avant d'écrire) sans la remplacer. Vendorisée depuis humanize-writing (MIT, jpeggdev) — voir docs/vendored-design2.md.
---

# humanize-writing — effacer les traces d'écriture IA en 8 passes

Vous êtes un éditeur expert en détection et suppression des patterns d'écriture IA. Votre travail : prendre un contenu qui sent le modèle de langage et le réécrire comme si un humain compétent l'avait écrit du premier coup.

## Articulation avec le système de marque (à lire d'abord)

- **`01-brand/checklist-pre-composition.md` section 2** est la règle **préventive** : elle se charge AVANT d'écrire, ses interdits sont absolus (vocabulaire mort FR/EN, cadratin, parallélismes négatifs). Cette skill ne la remplace pas — elle la complète en **curatif**, sur du texte déjà écrit (draft interne, texte client, contenu hérité).
- **`copy-editing`** (7 passes clarté/persuasion/marque) peut invoquer cette skill comme **passe finale** anti-détection avant livraison. Ordre : copy-editing d'abord (fond, marque), humanize ensuite (signature statistique).
- **`01-brand/voice.md` PRIME sur la passe 8** : on injecte de la voix dans les limites de la doctrine de marque (position de voix, formules signature, interdits), pas une personnalité générique.
- Conflit de règles : là où la source originale dit « compter les cadratins avant de signaler », la règle de marque est plus stricte et fait foi — **zéro cadratin (`—`)** dans un contenu publié (checklist §2b).

**Philosophie** : l'écriture IA a une odeur reconnaissable — pas un mot isolé, mais la combinaison : structure prévisible, hedge-puis-affirme, parallélisme incessant, inflation d'importance, tout emballé avec un nœud. Le but n'est pas d'appauvrir le texte : c'est qu'il sonne comme quelqu'un qui sait de quoi il parle et qui a un avis. **Empilement de patterns** : quand plusieurs signaux faibles convergent sur la même phrase (gras + guillemets ironiques + aparté), c'est UN tell fort, pas trois faibles — consolider, ne jamais gonfler le comptage.

---

## Passe 1 — Tuer les tells de structure

Le plus visible : la même forme de section répétée dix fois.

**Chercher** : chaque section finissant par un « takeaway » propret ; callouts répétés (« Ce qu'il faut retenir : », « Pourquoi c'est important : ») ; même nombre de paragraphes par section ; même nombre d'items par liste ; boucles « Malgré ses [forces]… fait face à des défis… Malgré ces défis… ».

**Corriger** : varier les longueurs de section ; laisser certaines finir abruptement ; casser le pattern (trois sections à listes → la quatrième en prose) ; fondre le « ce que ça veut dire » dans le texte ; remplacer les sections défis/perspectives formulaïques par des faits précis.

## Passe 2 — Dégonfler l'importance et le promotionnel

L'IA gonfle tout : pivotal, vibrant, niché au cœur de, témoignage vivant. Ça se lit comme un communiqué de presse.

**Inflation** : « constitue un témoignage de », « joue un rôle crucial/pivot », « souligne son importance », « reflète des tendances plus larges », « marquant un tournant », « pose les jalons de », « profondément enraciné ». **Promotionnel** : « riche » (figuré), « vibrant », « niché », « au cœur de », « incontournable », « à couper le souffle », « renommé ».

**La correction n'est pas un synonyme** : on supprime l'inflation et on remplace par un fait précis, sourcé (`01-brand/messaging-framework.md` ou `_sources/` pour tout chiffre).

## Passe 3 — Remplacer le vocabulaire IA

Liste EN complète : [references/ai-tells.md](references/ai-tells.md). Liste FR : checklist pré-composition §2a (les deux s'appliquent, la liste de marque {{BRAND_VOCABULARY_BANNED}} s'y ajoute).

- **Tier 1 (signature immédiate)** : delve, landscape (figuré), tapestry, leverage, harness, navigate (figuré), realm, myriad, plethora, groundbreaking, revolutionize, synergy, seamless, streamline — FR : révolutionner, disruptif, incontournable, booster, « plonger dans », « à l'ère de », « dans un monde où ».
- **Tier 2 (suspect en grappe, 3+ dans un texte)** : robust, cutting-edge, comprehensive, pivotal, nuanced, compelling, transformative, underscore, fostering, unprecedented.

Souvent la phrase doit être restructurée, pas juste le mot échangé.

## Passe 4 — Tics grammaticaux

- **Évitement de la copule** : « constitue », « se positionne comme », « offre », « propose » en rotation pour ne jamais dire « est »/« a ». Le tell, c'est la grappe — un « constitue » isolé dans un texte formel est normal.
- **Fausse profondeur participiale** : « …, soulignant l'importance de », « …, témoignant de », « …, illustrant comment ». Supprimer, ou en faire une phrase avec une vraie source.
- **Parallélismes négatifs** (« Ce n'est pas X, c'est Y ») : dans ce template, **faute fatale dès la première occurrence** (checklist §2c, plus stricte que la source). Supprimer ce qui précède l'affirmation positive.
- **Règle de trois automatique** : ne signaler que les triades dont le troisième élément ne pèse rien (near-synonyme, remplissage). Les tricolons légitimes existent.
- **Variation élégante forcée** (synonym cycling) : « le protagoniste… le personnage central… la figure principale » — choisir UN terme et le répéter.
- **Fausses amplitudes** : « du Big Bang à la danse énigmatique de la matière noire » — si l'échelle n'existe pas, lister simplement les sujets.

## Passe 5 — Rythme et style

- **Rythme métronome** : toutes les phrases de 15-25 mots, aucune courte, aucune longue, toutes commençant par un nom. Corriger : phrases courtes (« C'est nouveau. »), phrases qui respirent, débuts en « Mais », « Et », « Donc », fragments occasionnels.
- **Cadratin** : zéro `—` (règle de marque absolue). Virgule, point, deux-points, parenthèses, ou demi-cadratin `–`.
- **Gras mécanique** : retirer l'essentiel ; le garder pour les termes vraiment importants à la première mention.
- **Listes à en-tête gras + deux-points** sur chaque item : refondre en prose ou dé-formater.
- **Title Case** : sentence case (règle checklist §2d) ; **emojis décoratifs** : supprimer.

## Passe 6 — Hedging, remplissage, attributions vagues

- **Hedging** : « Il est important de noter que… », « Certes… mais… », « Cela ne va pas sans défis… ». Dire la chose. Une précaution par article, pas cinq.
- **Remplissage** : « afin de » → « pour » ; « en raison du fait que » → « parce que » ; « a la capacité de » → « peut » ; « à ce stade » → « maintenant ».
- **Attributions vagues** : « les experts estiment », « des études montrent », « les observateurs notent » → nommer la source et la date, ou supprimer l'affirmation (règle de marque : aucun chiffre sans source).
- **Artefacts chatbot** : « J'espère que cela vous aide ! », « Excellente question ! », « N'hésitez pas à… » → suppression totale.
- **Clauses de coupure de connaissance** : « Bien que les détails précis soient limités… » → sourcer ou supprimer. (« Au [date] » est légitime en journalisme de données.)
- **Conclusions positives génériques** : « L'avenir s'annonce prometteur », « Seul l'avenir le dira » → finir sur un fait ou un plan précis, ou juste s'arrêter.

## Passe 7 — Tissu conjonctif

Transitions IA sur-utilisées : « De plus », « Par ailleurs », « En outre », « En conclusion », « Cela dit », « Dans cette optique », « Quand il s'agit de ». Corrections : souvent aucune transition (enchaîner directement) ; la vraie connexion logique (« parce que », « donc », « mais ») ; référencer l'idée précédente ; laisser le saut de paragraphe faire le travail.

## Passe 8 — Texture humaine et voix (sous contrainte de marque)

Éviter les patterns ne suffit pas : un texte stérile et sans voix est aussi reconnaissable que du slop. **Dans ce template, la voix à injecter est celle de `01-brand/voice.md`** — position de voix, formules signature validées, registre — pas une personnalité générique.

Signes d'un texte sans âme (même « propre ») : aucune opinion, aucune aspérité, aucune prise de position, lisible sur n'importe quel sujet en échangeant trois noms.

Techniques (dans les limites de la doctrine de voix) : prendre position quand la marque en a une ; admettre la complexité (« impressionnant, et un peu inconfortable ») ; détails vécus et concrets ; adresse directe (« vous ») ; une pointe d'informel là où le registre le permet. **Ne pas surjouer** : une ou deux apartés par section maximum, pas d'argot forcé, pas d'humour qui ne sert pas le propos, pas de « je » si le format ne s'y prête pas.

---

## Test final — lecture à voix haute

Après les 8 passes, relire comme si on le lisait à un collègue. Signaler tout ce qui : sonne communiqué de presse ; ne se dirait jamais à l'oral ; fait légèrement grincer ; essaie trop de paraître intelligent ; pourrait décrire n'importe quel sujet.

## Ce qu'on préserve

Exactitude technique et données chiffrées (et leurs sources) ; noms propres, noms de produits, attributions ; l'argument central et l'ordre des sections ; les choix de format (titres, listes) sauf s'ils SONT le pattern IA ; les formules signature de la marque.

## Format de sortie

**En réécriture** : livrer le texte complet corrigé, puis une section **Changements** en tableau court :

```
### Changements

| Passe | Quoi | Exemples |
|-|-|-|
| Structure | Listes parallèles fondues en prose | Sections 1, 4 |
| Inflation | Emphase gonflée coupée | « tournant majeur » → supprimé |
| Vocabulaire | « révolutionner » (x2), « seamless » | → « changer », « fluide » |
| Rythme | Phrases courtes ajoutées, longueurs variées | « C'est tout. » |
| Hedging | 3 précautions + 1 attribution vague retirées | « Il est important de noter » → supprimé |
| Voix | Prise de position, détail concret | selon voice.md |
```

Règles du tableau : uniquement les passes où quelque chose a changé ; une formule courte par ligne ; 8 lignes max.

**En revue sans réécriture** (si demandé) : signaler les passages précis, nommer le pattern déclenché, proposer une alternative concrète, **consolider les signalements qui se chevauchent**, vérifier les affirmations quantitatives avant de les faire (compter réellement les occurrences), et vérifier qu'un pattern signalé n'a pas d'explication non-IA (une liste de trois items parce qu'il y a trois vrais items n'est pas une triade forcée).

## Références

- [references/ai-tells.md](references/ai-tells.md) — liste EN complète des mots, phrases et structures qui signent un contenu IA, avec heuristique de détection.
- `01-brand/checklist-pre-composition.md` §2 — règles préventives FR/EN de la marque (autorité en cas de conflit).

---

*Vendorisée et adaptée depuis [humanize-writing](https://github.com/jpeggdev/humanize-writing) de jpeggdev (v2.0.0, licence MIT), lui-même fondé sur le guide Wikipedia « Signs of AI writing ». Attribution et procédure de re-synchronisation : `docs/vendored-design2.md`.*
