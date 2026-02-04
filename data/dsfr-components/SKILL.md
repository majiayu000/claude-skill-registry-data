---
name: dsfr-components
description: Création d'interfaces web conformes au Design System de l'État Français (DSFR). Utiliser ce skill pour générer des pages HTML avec les composants officiels du gouvernement français, créer des formulaires administratifs, des tableaux de bord, ou tout site web respectant les standards de l'État.
---

# Skill Composants DSFR

Générez rapidement des interfaces web conformes au Design System de l'État Français.

## Vue d'ensemble

Ce skill fournit tout le nécessaire pour créer des sites web gouvernementaux français :
- Générateur de composants DSFR (boutons, alertes, formulaires, etc.)
- Générateur de pages complètes (landing, formulaire, tableau de bord)
- Documentation complète des composants et classes utilitaires
- Templates HTML prêts à l'emploi

## Utilisation rapide

### Générer une page complète
```bash
python3 scripts/generate_page.py --type landing --title "Mon Service Public" --output page.html
```

### Générer un composant
```bash
python3 scripts/generate_component.py button --config '{"variant": "primary", "size": "lg"}'
```

## Workflow recommandé

### 1. Création d'une nouvelle page
Commencer par générer une page de base :
```bash
python3 scripts/generate_page.py --type [standard|landing|form|dashboard] --output index.html
```

### 2. Ajout de composants
Utiliser le générateur de composants pour créer les éléments nécessaires :
```bash
# Bouton
python3 scripts/generate_component.py button --config '{"variant": "secondary"}'

# Alerte
python3 scripts/generate_component.py alert --config '{"type": "info", "title": "Information"}'

# Carte
python3 scripts/generate_component.py card --config '{"title": "Ma carte", "description": "Description"}'
```

### 3. Personnalisation
- Copier le template de base depuis `assets/template-base.html`
- Intégrer les composants générés
- Ajuster les classes utilitaires selon les besoins

## Composants disponibles

### Composants de base
- **Boutons** : Primaire, secondaire, tertiaire, avec icônes
- **Alertes** : Info, succès, avertissement, erreur
- **Badges** : Statuts et étiquettes colorées
- **Cartes** : Présentation de contenu avec image optionnelle

### Navigation
- **Fil d'Ariane** : Navigation hiérarchique
- **Menu** : Navigation principale et secondaire
- **Pagination** : Navigation entre pages
- **Onglets** : Organisation du contenu

### Formulaires
- **Champs de saisie** : Texte, email, mot de passe, etc.
- **Cases à cocher** : Sélection multiple
- **Boutons radio** : Sélection unique
- **Sélecteurs** : Listes déroulantes

### Affichage de données
- **Tableaux** : Présentation structurée de données
- **Accordéons** : Contenu repliable
- **Modales** : Fenêtres de dialogue

## Classes utilitaires principales

### Grille responsive
- `fr-container` : Container principal
- `fr-grid-row` : Ligne de grille
- `fr-col-*` : Colonnes (1-12)
- `fr-col-md-*` : Colonnes medium (≥768px)
- `fr-col-lg-*` : Colonnes large (≥992px)

### Espacements
- `fr-mt-*` : Marge top (1w = 0.5rem, 2w = 1rem, etc.)
- `fr-mb-*` : Marge bottom
- `fr-py-*` : Padding vertical
- `fr-px-*` : Padding horizontal

### Typographie
- `fr-text--lg` : Texte large
- `fr-text--bold` : Texte gras
- `fr-text--lead` : Texte d'introduction

## Options des scripts

### generate_page.py
- `--type` : Type de page (standard, landing, form, dashboard)
- `--title` : Titre de la page
- `--content` : Contenu HTML personnalisé
- `--dark` : Mode sombre
- `--no-header` : Sans en-tête
- `--no-footer` : Sans pied de page
- `--output` : Fichier de sortie

### generate_component.py
- `component` : Type de composant à générer
- `--config` : Configuration JSON du composant

## Documentation de référence

### Composants détaillés
Voir `references/components.md` pour :
- Syntaxe HTML complète de chaque composant
- Variantes et modificateurs disponibles
- Exemples d'utilisation avancée

### Classes utilitaires
Voir `references/utilities.md` pour :
- Système de grille complet
- Classes d'espacement
- Modificateurs typographiques
- Classes de couleur
- Helpers d'accessibilité

## Ressources officielles

- [Documentation DSFR](https://www.systeme-de-design.gouv.fr/)
- [Storybook des composants](https://storybook.systeme-de-design.gouv.fr/)
- [GitHub du DSFR](https://github.com/GouvernementFR/dsfr)

## Conformité et accessibilité

Tous les composants générés respectent :
- Les standards WCAG 2.1 niveau AA
- Le RGAA (Référentiel Général d'Amélioration de l'Accessibilité)
- Les bonnes pratiques du W3C
- La charte graphique de l'État français
