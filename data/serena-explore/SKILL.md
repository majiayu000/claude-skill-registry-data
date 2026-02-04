---
name: serena-explore
description: Exploration symbolique du code avec Serena MCP. Utiliser pour naviguer dans le code par symboles (fonctions, classes, hooks), trouver des définitions, et comprendre l'architecture sans lire des fichiers entiers.
allowed-tools:
  - mcp__serena__get_symbols_overview
  - mcp__serena__find_symbol
  - mcp__serena__search_for_pattern
  - mcp__serena__check_onboarding_performed
  - mcp__serena__find_referencing_symbols
  - mcp__serena__list_dir
---

# Serena Explore - Navigation Symbolique

## Objectif

Explorer le code du projet MyGGV GPS de manière efficace en utilisant la navigation symbolique plutôt que la lecture de fichiers entiers. Économise les tokens et améliore la précision.

## Périmètre

### Inclus
- Vue d'ensemble des symboles d'un fichier
- Recherche de symboles par nom ou pattern
- Navigation vers les définitions
- Trouver les références d'un symbole
- Comprendre les relations entre symboles

### Exclus
- Modification de code → utiliser `serena-edit`
- Mémoire projet → utiliser `serena-memory`
- Lecture de fichiers complets → éviter, utiliser les symboles

## Pourquoi Serena ?

### Avantages vs Read Tool
| Approche | Tokens | Précision |
|----------|--------|-----------|
| `Read` fichier entier | ~1000+ tokens | Bruit inutile |
| `Serena` symbole ciblé | ~100-200 tokens | Exactement ce qu'il faut |

### Exemple
```javascript
// MAUVAIS - Lire tout le fichier
Read({ file_path: "/src/hooks/useRouteManager.js" })
// → 500+ lignes, beaucoup de bruit

// BON - Cibler le symbole
mcp__serena__find_symbol({ symbol_name: "useRouteManager" })
// → Juste la fonction et sa signature
```

## Outils Disponibles

### 1. get_symbols_overview
Vue d'ensemble des symboles d'un fichier :
```javascript
mcp__serena__get_symbols_overview({
  file_path: "src/hooks/useRouteManager.js"
})
// Retourne : liste des fonctions, constantes, exports
```

### 2. find_symbol
Trouver un symbole spécifique :
```javascript
mcp__serena__find_symbol({
  symbol_name: "useNavigationState"
})
// Retourne : définition, signature, fichier source
```

### 3. search_for_pattern
Recherche par pattern regex :
```javascript
mcp__serena__search_for_pattern({
  pattern: "use.*Map.*",  // Tous les hooks liés à Map
  file_types: ["js", "jsx"]
})
```

### 4. get_related_symbols
Trouver les symboles liés (imports, dépendances) :
```javascript
mcp__serena__get_related_symbols({
  symbol_name: "useMapConfig"
})
// Retourne : blocksGeoJSON, getPolygonCenter, etc.
```

### 5. get_symbol_references
Où un symbole est-il utilisé ?
```javascript
mcp__serena__get_symbol_references({
  symbol_name: "haversineDistance"
})
// Retourne : tous les fichiers qui l'importent/utilisent
```

## Workflow d'Exploration

### Comprendre un fichier
```
1. get_symbols_overview → Liste des symboles
2. find_symbol → Détails d'un symbole intéressant
3. get_related_symbols → Dépendances
```

### Trouver où modifier
```
1. search_for_pattern → Trouver les candidats
2. get_symbol_references → Voir l'impact
3. find_symbol → Détails précis avant modification
```

### Comprendre un bug
```
1. find_symbol → Localiser la fonction suspecte
2. get_related_symbols → Voir les dépendances
3. get_symbol_references → Tracer les appels
```

## Structure du Projet MyGGV GPS

### Hooks Principaux
```
src/hooks/
├── useMapConfig.js        → Configuration carte, GeoJSON blocs
├── useRouteManager.js     → Gestion routes, recalcul
├── useNavigationState.js  → Machine d'état navigation
├── useDeviceOrientation.js → Boussole
├── useMapTransitions.js   → Animations flyTo
├── useBlockPolygons.js    → Rendu polygones
├── useAdaptivePitch.js    → Pitch caméra
├── useSymbolLayerInteractions.js → Clicks sur layers
└── useLocations.js        → Fetch Supabase
```

### Composants Clés
```
src/components/
├── MapMarkers.jsx         → Markers destination
├── RouteLayers.jsx        → Affichage routes
├── NavigationDisplay.jsx  → UI navigation active
├── MapControls/           → Contrôles carte
└── WelcomeModalMobile.jsx → Sélection destination
```

### Utilitaires
```
src/lib/navigation.js      → Logique routing (OSRM)
src/utils/geoUtils.js      → Calculs géo
src/utils/mapTransitions.js → Transitions carte
```

## Bonnes Pratiques

1. **Toujours commencer par get_symbols_overview** avant de chercher dans un fichier
2. **Utiliser des patterns précis** pour search_for_pattern
3. **Éviter Read pour les gros fichiers** - préférer la navigation symbolique
4. **Vérifier les références** avant de modifier un symbole public

## Anti-Patterns

❌ **Ne pas faire :**
```javascript
// Lire un fichier entier pour trouver une fonction
Read({ file_path: "src/lib/navigation.js" })  // 1248 lignes !
```

✅ **Faire :**
```javascript
// Cibler directement
mcp__serena__find_symbol({ symbol_name: "createRoute" })
```
