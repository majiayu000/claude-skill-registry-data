---
name: serena-memory
description: Gestion de la mémoire projet avec Serena MCP. Utiliser pour stocker et récupérer des informations persistantes sur le projet, les décisions architecturales, et le contexte entre sessions.
allowed-tools:
  - mcp__serena__write_memory
  - mcp__serena__read_memory
  - mcp__serena__edit_memory
  - mcp__serena__list_memories
  - mcp__serena__delete_memory
  - mcp__serena__check_onboarding_performed
---

# Serena Memory - Mémoire Projet

## Objectif

Maintenir une mémoire persistante du projet MyGGV GPS entre les sessions : décisions architecturales, patterns utilisés, problèmes résolus, et contexte important.

## Périmètre

### Inclus

- Stocker des décisions architecturales
- Mémoriser les patterns et conventions du projet
- Garder trace des bugs résolus et solutions
- Conserver le contexte entre sessions

### Exclus

- Exploration de code → utiliser `serena-explore`
- Édition de code → utiliser `serena-edit`
- Documentation formelle → utiliser `archon-project`

## Outils Disponibles

### 1. store_memory

Stocker une information :

```javascript
mcp__serena__store_memory({
  key: "routing_service",
  value: "OSRM via router.project-osrm.org",
  category: "architecture",
  tags: ["navigation", "api", "routing"],
});
```

### 2. recall_memory

Récupérer une information :

```javascript
mcp__serena__recall_memory({
  key: "routing_service",
});
// ou par catégorie
mcp__serena__recall_memory({
  category: "architecture",
});
```

### 3. list_memories

Lister toutes les mémoires :

```javascript
mcp__serena__list_memories({
  category: "bugs", // optionnel, filtre par catégorie
});
```

### 4. delete_memory

Supprimer une mémoire obsolète :

```javascript
mcp__serena__delete_memory({
  key: "old_pattern",
});
```

## Catégories Recommandées

### architecture

Décisions structurelles du projet :

```javascript
mcp__serena__store_memory({
  key: "state_management",
  value: "React hooks + useContext, pas de Redux. TanStack Query pour les données serveur.",
  category: "architecture",
});
```

### patterns

Patterns et conventions de code :

```javascript
mcp__serena__store_memory({
  key: "hook_naming",
  value: "Tous les hooks custom commencent par 'use' et sont dans src/hooks/",
  category: "patterns",
});
```

### bugs

Bugs résolus et solutions :

```javascript
mcp__serena__store_memory({
  key: "ios_orientation_permission",
  value: "iOS 13+ requiert DeviceOrientationEvent.requestPermission() appelé sur user gesture",
  category: "bugs",
  tags: ["ios", "compass", "permission"],
});
```

### decisions

Choix techniques et leur justification :

```javascript
mcp__serena__store_memory({
  key: "why_turf_not_openlayers",
  value:
    "Turf.js choisi pour les calculs géo car plus léger (~50KB vs ~500KB pour OpenLayers). MapLibre gère déjà le rendu.",
  category: "decisions",
});
```

### context

Contexte projet général :

```javascript
mcp__serena__store_memory({
  key: "target_users",
  value:
    "Résidents et visiteurs de Garden Grove Village, Philippines. Accès via QR code à l'entrée.",
  category: "context",
});
```

## Mémoires Essentielles pour MyGGV GPS

### Architecture

```javascript
// Stack technique
{ key: "tech_stack", value: "React 19 + Vite + MapLibre GL + Supabase", category: "architecture" }

// Structure navigation
{ key: "navigation_states", value: "gps-permission → welcome → orientation-permission → navigating → arrived → exit-complete", category: "architecture" }

// Sources de données
{ key: "data_sources", value: "Supabase pour locations/POIs, OSRM pour routing, OSM/Esri pour tuiles", category: "architecture" }
```

### Patterns

```javascript
// Hooks
{ key: "map_hooks", value: "useMapConfig (config), useRouteManager (routes), useNavigationState (états), useMapTransitions (animations)", category: "patterns" }

// Composants
{ key: "modal_pattern", value: "Tous les modals utilisent Radix Dialog via src/components/ui/dialog.jsx", category: "patterns" }
```

### Bugs Connus

```javascript
// iOS
{ key: "ios_geolocation", value: "Requiert HTTPS. Utiliser GeolocateControl de MapLibre, pas navigator.geolocation directement.", category: "bugs" }

// Race condition
{ key: "style_loading", value: "Attendre isStyleLoaded() avant d'ajouter des sources/layers custom", category: "bugs" }
```

## Workflow

### Début de session

```
1. check_onboarding_performed → Vérifier si Serena est initialisé
2. list_memories → Voir le contexte existant
3. recall_memory(category: "context") → Charger le contexte projet
```

### Après une décision importante

```
1. Documenter la décision
2. store_memory avec catégorie appropriée
3. Ajouter des tags pour faciliter la recherche
```

### Après résolution d'un bug

```
1. store_memory avec category: "bugs"
2. Inclure : symptôme, cause, solution
3. Tagger avec les technologies concernées
```

## Bonnes Pratiques

1. **Clés descriptives** : `ios_orientation_permission` plutôt que `bug1`
2. **Valeurs complètes** : Inclure le contexte et la solution, pas juste le problème
3. **Tags pertinents** : Faciliter la recherche future
4. **Catégorisation cohérente** : Utiliser les catégories standard

## Exemple Complet

```javascript
// Après avoir résolu un bug de routing
mcp__serena__store_memory({
  key: "route_recalculation_threshold",
  value: `
    Problème: Route recalculée trop fréquemment sur petits écarts GPS.
    Cause: Seuil de déviation trop sensible (10m).
    Solution: Augmenté à 30m et ajouté debounce de 2s.
    Fichier: src/lib/navigation.js, fonction checkRouteDeviation
  `,
  category: "bugs",
  tags: ["routing", "gps", "performance", "navigation"],
});
```
