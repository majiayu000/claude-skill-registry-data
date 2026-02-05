---
name: Design System Français (DSFR)
description: Documentation et accessibilité concernant le Design System Français (DSFR), un ensemble de composants et de bonnes pratiques pour créer des interfaces utilisateur conformes aux standards du gouvernement français. Use when user wants to implement DSFR components, needs DSFR documentation, asks about French government design system, requires RGAA accessibility guidelines, works with French government websites, or needs HTML/CSS examples for accessible components.
version: 1.0
author: skelz0r
tags: [design system, DSFR, accessibilité, documentation, interface utilisateur, gouvernement français]
---

# Design System Français (DSFR)

Le Design System Français (DSFR) est le système de conception de référence de l'État français. Il fournit des composants réutilisables et des règles pour créer des interfaces utilisateur cohérentes, accessibles et conformes aux standards du gouvernement français.

## À propos de ce skill

Ce skill contient la documentation complète de 23 composants essentiels du DSFR. Chaque composant est documenté avec :
- Une présentation générale et des règles d'usage
- Des spécifications d'accessibilité conformes au RGAA 4.1
- Une documentation technique complète (HTML, CSS, JavaScript)
- Des spécifications design détaillées
- Des exemples de code HTML complets et fonctionnels

## Comment utiliser cette documentation

### Structure des fichiers

**IMPORTANT :** Chaque composant dispose **systématiquement** de ces 5 fichiers :

1. **index.md** - Vue d'ensemble du composant
   - Présentation et cas d'usage
   - Quand utiliser / ne pas utiliser ce composant
   - Règles éditoriales et bonnes pratiques
   - Exemples visuels (do/don't)

2. **accessibilite.md** - Conformité RGAA
   - Interactions clavier requises
   - Attributs ARIA nécessaires
   - Critères RGAA applicables
   - Tests avec lecteurs d'écran
   - Compatibilité navigateurs/technologies d'assistance

3. **code.md** - Documentation technique
   - Structure HTML complète et détaillée
   - Classes CSS obligatoires et optionnelles
   - Dépendances JavaScript
   - API JavaScript (window.dsfr)
   - Événements personnalisés disponibles
   - Exemples d'implémentation

4. **design.md** - Spécifications design
   - Anatomie du composant (éléments constitutifs)
   - Variantes disponibles (tailles, couleurs, états)
   - États visuels (défaut, hover, focus, disabled, error, success)
   - Personnalisation possible
   - Guidelines design et espacement

5. **examples/** - Exemples HTML complets
   - Fichiers HTML autonomes et fonctionnels
   - Imports DSFR CSS et JS depuis CDN
   - Code prêt à copier-coller
   - Démonstration de différentes variantes

**Ces fichiers existent toujours.** Dans la liste des composants ci-dessous, seul le chemin vers `index.md` est indiqué. Les 4 autres fichiers sont toujours présents dans le même dossier.

### Répondre aux demandes utilisateur

**Pour une question générale sur un composant :**
→ Consulter d'abord `index.md` pour la présentation et les cas d'usage

**Pour une question d'accessibilité :**
→ Consulter `accessibilite.md` pour les spécifications RGAA, ARIA et interactions clavier

**Pour une question d'implémentation :**
→ Consulter `code.md` pour la structure HTML, classes CSS et API JavaScript
→ Consulter `examples/` pour des exemples complets

**Pour une question de design ou d'apparence :**
→ Consulter `design.md` pour les variantes, états et spécifications visuelles

**Pour créer un exemple de code :**
→ Toujours inclure les imports DSFR CSS et JS
→ S'inspirer des exemples dans `examples/`
→ Respecter la structure HTML de `code.md`
→ Mentionner les contraintes d'accessibilité importantes

## Standards et conformité

### RGAA 4.1
Tous les composants sont conçus pour respecter le Référentiel Général d'Amélioration de l'Accessibilité version 4.1. Les critères RGAA applicables sont détaillés dans les fichiers `accessibilite.md`.

### ARIA
Les attributs ARIA nécessaires sont documentés pour chaque composant. Ils sont essentiels pour l'accessibilité et doivent être implémentés correctement.

### Compatibilité navigateurs
Les composants sont testés et compatibles avec :
- Chrome/Edge (versions récentes)
- Firefox (versions récentes)
- Safari (versions récentes)
- Internet Explorer 11 (support limité)

### Technologies d'assistance
Les composants sont testés avec :
- NVDA (Windows)
- JAWS (Windows)
- VoiceOver (macOS/iOS)
- TalkBack (Android)

## Architecture technique du DSFR

### Imports requis

Pour utiliser les composants DSFR, il faut toujours inclure :

```html
<!-- CSS du DSFR -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr/dist/dsfr.min.css">

<!-- JavaScript du DSFR (si le composant a des interactions) -->
<script type="module" src="https://cdn.jsdelivr.net/npm/@gouvfr/dsfr/dist/dsfr.module.min.js"></script>
```

### Classes CSS

Les classes suivent une convention de nommage stricte :
- Préfixe `fr-` pour tous les composants
- Pattern : `fr-{composant}`, `fr-{composant}__{élément}`, `fr-{composant}--{variante}`
- Exemples : `fr-btn`, `fr-btn--secondary`, `fr-accordion__title`

### JavaScript

Les composants interactifs utilisent l'API JavaScript du DSFR :
- Initialisation automatique au chargement de la page
- API globale accessible via `window.dsfr`
- Événements personnalisés pour les interactions
- Pas de dépendance externe (pas de jQuery requis)

## Liste des composants disponibles

**23 composants disponibles**


### Accordéon (`accordion`)
Masquer ou révéler du contenu textuel

**Documentation** : [`composants/accordion/index.md`](composants/accordion/index.md)


### Alerte (`alert`)
Relayer une information importante

**Documentation** : [`composants/alert/index.md`](composants/alert/index.md)


### Badge (`badge`)
Affichage d’un statut informatif

**Documentation** : [`composants/badge/index.md`](composants/badge/index.md)


### Fil d'Ariane (`breadcrumb`)
Se repérer dans l’arborescence avec le fil d’Ariane.

**Documentation** : [`composants/breadcrumb/index.md`](composants/breadcrumb/index.md)


### Bouton (`button`)
Déclenchement d’une action dans l’interface

**Documentation** : [`composants/button/index.md`](composants/button/index.md)


### Carte (`card`)
Carte cliquable redirigeant vers une page éditoriale avec aperçu.

**Documentation** : [`composants/card/index.md`](composants/card/index.md)


### Case à cocher (`checkbox`)
Sélection multiple dans une liste

**Documentation** : [`composants/checkbox/index.md`](composants/checkbox/index.md)


### Pied de page (`footer`)
Informations complémentaires en bas de page

**Documentation** : [`composants/footer/index.md`](composants/footer/index.md)


### En-tête (`header`)
Identification du site et accès rapides

**Documentation** : [`composants/header/index.md`](composants/header/index.md)


### Champ de saisie (`input`)
Saisie de données dans une interface.

**Documentation** : [`composants/input/index.md`](composants/input/index.md)


### Lien (`link`)
Navigation secondaire vers d’autres contenus

**Documentation** : [`composants/link/index.md`](composants/link/index.md)


### Modale (`modal`)
Affichage focalisé d’un contenu secondaire

**Documentation** : [`composants/modal/index.md`](composants/modal/index.md)


### Navigation principale (`navigation`)
Orienter l’usager dans les sections du site.

**Documentation** : [`composants/navigation/index.md`](composants/navigation/index.md)


### Bandeau d'information importante (`notice`)
Afficher une alerte temporaire prioritaire.

**Documentation** : [`composants/notice/index.md`](composants/notice/index.md)


### Pagination (`pagination`)
Navigation entre plusieurs pages d’une liste

**Documentation** : [`composants/pagination/index.md`](composants/pagination/index.md)


### Bouton radio (`radio`)
Sélection d’une option unique

**Documentation** : [`composants/radio/index.md`](composants/radio/index.md)


### Barre de recherche (`search`)
Accès rapide à un contenu par mot clé

**Documentation** : [`composants/search/index.md`](composants/search/index.md)


### Liste déroulante (`select`)
Sélectionner une option dans une liste.

**Documentation** : [`composants/select/index.md`](composants/select/index.md)


### Onglet (`tab`)
Structuration de contenu avec des onglets

**Documentation** : [`composants/tab/index.md`](composants/tab/index.md)


### Tableau (`table`)
Présentation du composant Tableau pour organiser et comparer des données.

**Documentation** : [`composants/table/index.md`](composants/table/index.md)


### Tag (`tag`)
Le tag sert à classer ou filtrer les contenus.

**Documentation** : [`composants/tag/index.md`](composants/tag/index.md)


### Tuile (`tile`)
Rediriger l’usager vers du contenu via des tuiles.

**Documentation** : [`composants/tile/index.md`](composants/tile/index.md)


### Interrupteur (`toggle`)
Basculer entre deux états opposés

**Documentation** : [`composants/toggle/index.md`](composants/toggle/index.md)


## Comment répondre aux questions utilisateur

### Exemples de questions et approches recommandées

**"Comment créer un bouton ?"**
1. Consulter `composants/button/code.md` pour la structure HTML du composant Bouton (`button`)
2. Montrer un exemple simple avec les imports DSFR
3. Mentionner les variantes disponibles (primaire, secondaire, tertiaire)

**"Mon bouton n'est pas accessible, comment le corriger ?"**
1. Consulter `composants/button/accessibilite.md` du composant Bouton (`button`)
2. Vérifier les attributs ARIA requis
3. Vérifier les interactions clavier
4. Proposer les corrections nécessaires

**"Quelle est la différence entre un bouton primaire et secondaire ?"**
1. Consulter `composants/button/index.md` du composant Bouton (`button`) pour la hiérarchie d'usage
2. Consulter `composants/button/design.md` pour les différences visuelles
3. Expliquer les cas d'usage de chaque variante

**"Donne-moi un exemple complet d'accordéon"**
1. Lire un fichier dans `composants/accordion/examples/` du composant Accordéon (`accordion`)
2. Présenter le code complet
3. Expliquer les éléments clés (structure, classes, attributs)

**"Comment personnaliser la couleur d'un badge ?"**
1. Consulter `composants/badge/design.md` du composant Badge (`badge`) pour les variantes de couleur disponibles
2. Montrer les classes CSS correspondantes depuis `code.md`
3. Avertir si une personnalisation n'est pas recommandée par le DSFR

### Principes à respecter

**Toujours privilégier l'accessibilité :**
- Mentionner les contraintes ARIA et RGAA importantes
- Rappeler les interactions clavier nécessaires
- Inclure les attributs d'accessibilité dans les exemples de code

**Fournir du code complet et fonctionnel :**
- Inclure les imports CSS et JS du DSFR
- Respecter la structure HTML documentée
- Utiliser les classes CSS exactes du DSFR
- Ne pas inventer de classes ou attributs non documentés

**Être précis sur les variantes :**
- Utiliser les noms exacts des variantes (ex: `fr-btn--secondary` et non "bouton-secondaire")
- Consulter `design.md` pour les variantes disponibles
- Ne pas suggérer de variantes non documentées

**Contextualiser les recommandations :**
- Expliquer pourquoi une approche est recommandée
- Mentionner les cas où un composant ne doit pas être utilisé
- Référencer les bonnes pratiques du DSFR

## Ressources externes

### Documentation officielle DSFR
- Site web : https://www.systeme-de-design.gouv.fr/
- GitHub : https://github.com/GouvernementFR/dsfr
- NPM : @gouvfr/dsfr

### Standards et références
- RGAA 4.1 : https://accessibilite.numerique.gouv.fr/
- WAI-ARIA : https://www.w3.org/WAI/ARIA/
- Documentation MDN (HTML/CSS/JS) : https://developer.mozilla.org/

### Outils de test d'accessibilité
- NVDA (lecteur d'écran Windows)
- JAWS (lecteur d'écran Windows)
- VoiceOver (lecteur d'écran macOS/iOS)
- Axe DevTools (extension navigateur)
- WAVE (extension navigateur)

## Notes importantes

### Ce qui N'EST PAS dans ce skill

Ce skill contient 23 composants prioritaires. Le DSFR complet contient plus de 60 composants. Si un utilisateur demande un composant non documenté ici (ex: stepper, sidemenu, quote, highlight, callout, upload, password, range, etc.), indiquer qu'il faut consulter la documentation officielle du DSFR : https://www.systeme-de-design.gouv.fr/composants-et-modeles/

### Versions et mises à jour

Ce skill est synchronisé avec la version du DSFR disponible dans le dépôt GitHub officiel à la date de dernière synchronisation. Consulter le fichier [`VERSION.md`](VERSION.md) pour connaître :
- La date de dernière synchronisation
- Le commit/tag DSFR source
- L'historique des mises à jour

### Personnalisation du DSFR

Le DSFR est conçu pour garantir une cohérence visuelle des services de l'État. Certaines personnalisations ne sont pas autorisées :
- Modification des couleurs de marque
- Changement des espacements standardisés
- Modification de la typographie (Marianne)

Les personnalisations autorisées sont documentées dans les fichiers `design.md` de chaque composant.

## Support et contribution

Pour toute question non couverte par cette documentation :
1. Consulter la documentation officielle : https://www.systeme-de-design.gouv.fr/
2. Poser une question sur le forum DSFR : https://github.com/GouvernementFR/dsfr/discussions
3. Signaler un bug : https://github.com/GouvernementFR/dsfr/issues
