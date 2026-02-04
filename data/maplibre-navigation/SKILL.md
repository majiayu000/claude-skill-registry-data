---
name: maplibre-navigation
description: Développement des fonctionnalités de navigation GPS avec MapLibre GL. Utiliser pour le code de carte, routing, géolocalisation, markers, et layers.
allowed-tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Bash
  - mcp__archon__rag_search_knowledge_base
  - mcp__archon__rag_search_code_examples
---

# MapLibre Navigation - MyGGV GPS

## Objectif

Développer et maintenir les fonctionnalités de navigation GPS avec MapLibre GL JS pour l'application MyGGV GPS.

## Périmètre

### Inclus

- Configuration et rendu de la carte MapLibre
- Gestion des layers (polygones, routes, markers)
- Géolocalisation et tracking GPS
- Calcul et affichage des itinéraires
- Gestion de l'orientation (boussole)
- Interactions utilisateur avec la carte

### Exclus

- Base de données → utiliser `supabase-database`
- Déploiement → utiliser `netlify-deploy`

## Architecture du Code

### Fichiers Principaux

```
src/
├── App.jsx                    # Composant principal avec Map
├── components/
│   ├── MapMarkers.jsx         # Markers de destination
│   ├── MapControls/           # Contrôles de carte
│   ├── RouteLayers.jsx        # Affichage des routes
│   ├── NavigationDisplay.jsx  # UI de navigation active
│   └── WelcomeModalMobile.jsx # Sélection destination
├── hooks/
│   ├── useMapConfig.js        # Configuration carte + GeoJSON
│   ├── useRouteManager.js     # Gestion des routes
│   ├── useNavigationState.js  # Machine d'état navigation
│   ├── useDeviceOrientation.js # Boussole
│   ├── useMapTransitions.js   # Animations flyTo/jumpTo
│   ├── useBlockPolygons.js    # Rendu des blocs
│   └── useAdaptivePitch.js    # Pitch adaptatif
├── lib/
│   └── navigation.js          # Logique routing (OSRM)
└── utils/
    ├── geoUtils.js            # Calculs géo (Haversine, etc.)
    └── mapTransitions.js      # Utilitaires transitions
```

## Hooks Clés

### useMapConfig

Configuration de la carte et génération du GeoJSON des blocs :

```javascript
const { initialViewState, blocksGeoJSON, mapStyle, getPolygonCenter } = useMapConfig(
  userLocation,
  navigationState,
  adaptivePitch,
  mapType,
);
```

### useRouteManager

Gestion complète des itinéraires :

```javascript
const { route, traveledRoute, createRoute, clearRoute } = useRouteManager({
  mapRef,
  destination,
  userLocation,
  navigationState,
  isMapReady,
});
```

### useNavigationState

Machine d'état pour le flux de navigation :

```javascript
// États possibles :
// gps-permission → welcome → orientation-permission → navigating → arrived → exit-complete
const { navigationState, setNavigationState, ... } = useNavigationState();
```

## APIs de MapLibre Utilisées

### Performance Native

```javascript
// Projection rapide (84% plus rapide que Haversine)
map.project([lng, lat]);

// Styling GPU-accelerated
map.setFeatureState({ source, id }, { selected: true });

// Détection optimisée
map.queryRenderedFeatures(point, { layers: ["blocks"] });

// Transitions fluides
map.flyTo({ center, zoom, duration: 1000 });
```

### Sources et Layers

```javascript
// Ajouter une source GeoJSON
map.addSource("route", {
  type: "geojson",
  data: routeGeoJSON,
});

// Ajouter un layer
map.addLayer({
  id: "route-line",
  type: "line",
  source: "route",
  paint: {
    "line-color": "#3b82f6",
    "line-width": 5,
  },
});
```

## Routing

### Service OSRM

Le routing utilise OSRM (Open Source Routing Machine) :

```javascript
// src/lib/navigation.js
const response = await fetch(
  `https://router.project-osrm.org/route/v1/driving/${start};${end}?geometries=geojson`,
);
```

### MapLibre Directions

Alternative avec le plugin directions :

```javascript
import MapLibreGlDirections from "@maplibre/maplibre-gl-directions";

const directions = new MapLibreGlDirections(map, {
  profile: "driving",
});
```

## Calculs Géographiques

### Avec Turf.js

```javascript
import * as turf from "@turf/turf";

// Distance entre deux points
const distance = turf.distance(point1, point2, { units: "meters" });

// Centre d'un polygone
const centroid = turf.centroid(polygon);

// Point sur une ligne
const along = turf.along(line, distance, { units: "meters" });

// Détection hors-route
const isOnRoute = turf.booleanPointOnLine(point, routeLine, { tolerance: 30 });
```

### Fonctions Utilitaires (src/utils/geoUtils.js)

```javascript
// Haversine distance
export function haversineDistance(lat1, lon1, lat2, lon2) { ... }

// Bearing entre deux points
export function calculateBearing(lat1, lon1, lat2, lon2) { ... }
```

## États de Navigation

```
┌─────────────────┐
│ gps-permission  │ ← Demande permission GPS
└────────┬────────┘
         ↓
┌─────────────────┐
│    welcome      │ ← Sélection destination
└────────┬────────┘
         ↓
┌─────────────────┐
│ orientation-    │ ← Demande permission boussole (iOS)
│   permission    │
└────────┬────────┘
         ↓
┌─────────────────┐
│   navigating    │ ← Navigation active
└────────┬────────┘
         ↓
┌─────────────────┐
│    arrived      │ ← Destination atteinte
└────────┬────────┘
         ↓
┌─────────────────┐
│  exit-complete  │ ← Sortie confirmée
└─────────────────┘
```

## Bonnes Pratiques

### Performance

1. **Utiliser les APIs natives MapLibre** plutôt que des calculs JS
2. **Éviter les re-renders** avec useMemo/useCallback
3. **Limiter queryRenderedFeatures** aux layers nécessaires

### Géolocalisation

1. **Utiliser GeolocateControl** de MapLibre (plus fiable)
2. **Gérer les erreurs** de permission proprement
3. **Fallback pour desktop** avec position par défaut

### Mobile

1. **Tester sur device réel** (GPS, boussole)
2. **iOS Safari** nécessite HTTPS pour geolocation
3. **DeviceOrientation** nécessite permission explicite sur iOS 13+

## Recherche Documentation

Pour chercher dans la documentation MapLibre :

```javascript
mcp__archon__rag_search_knowledge_base({
  query: "maplibre flyTo animation",
  match_count: 5,
});
```
