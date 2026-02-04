---
name: serena-edit
description: Édition de code par symboles avec Serena MCP. Utiliser pour modifier des fonctions, hooks, ou composants de manière précise sans réécrire des fichiers entiers.
allowed-tools:
  - mcp__serena__find_symbol
  - mcp__serena__replace_symbol_body
  - mcp__serena__insert_after_symbol
  - mcp__serena__insert_before_symbol
  - mcp__serena__get_symbols_overview
  - mcp__serena__find_referencing_symbols
---

# Serena Edit - Édition Symbolique

## Objectif

Modifier le code du projet MyGGV GPS de manière précise en ciblant des symboles spécifiques plutôt que de réécrire des fichiers entiers.

## Périmètre

### Inclus
- Remplacer le corps d'une fonction/hook
- Renommer un symbole (avec mise à jour des références)
- Ajouter un nouveau symbole
- Supprimer un symbole

### Exclus
- Exploration de code → utiliser `serena-explore`
- Mémoire projet → utiliser `serena-memory`
- Création de nouveaux fichiers → utiliser `Write`

## Outils Disponibles

### 1. replace_symbol_body
Remplacer le contenu d'une fonction :
```javascript
mcp__serena__replace_symbol_body({
  symbol_name: "getPolygonCenter",
  file_path: "src/hooks/useMapConfig.js",
  new_body: `
    if (!coords || coords.length === 0) return [0, 0];
    const polygon = turf.polygon([coords]);
    const centroid = turf.centroid(polygon);
    return centroid.geometry.coordinates;
  `
})
```

### 2. rename_symbol
Renommer un symbole partout dans le projet :
```javascript
mcp__serena__rename_symbol({
  old_name: "handleArrival",
  new_name: "onDestinationReached",
  scope: "project"  // ou "file" pour limiter
})
```

### 3. add_symbol
Ajouter une nouvelle fonction/constante :
```javascript
mcp__serena__add_symbol({
  file_path: "src/utils/geoUtils.js",
  symbol_type: "function",
  symbol_name: "calculateMidpoint",
  body: `
    export function calculateMidpoint(coord1, coord2) {
      return [
        (coord1[0] + coord2[0]) / 2,
        (coord1[1] + coord2[1]) / 2
      ];
    }
  `,
  position: "end"  // ou "after:haversineDistance"
})
```

### 4. delete_symbol
Supprimer un symbole :
```javascript
mcp__serena__delete_symbol({
  symbol_name: "unusedHelper",
  file_path: "src/utils/geoUtils.js"
})
```

## Workflow d'Édition

### Modifier une fonction existante
```
1. find_symbol → Vérifier la signature actuelle
2. replace_symbol_body → Appliquer les changements
3. Vérifier le build (npm run build)
```

### Refactoring avec renommage
```
1. get_symbol_references → Voir l'impact
2. rename_symbol → Renommer partout
3. Vérifier les imports
```

### Ajouter une nouvelle fonctionnalité
```
1. get_symbols_overview → Voir la structure du fichier
2. add_symbol → Ajouter le nouveau code
3. Mettre à jour les exports si nécessaire
```

## Exemples Pratiques

### Exemple 1 : Corriger un calcul
```javascript
// Trouver la fonction
mcp__serena__find_symbol({ symbol_name: "haversineDistance" })

// Modifier le corps
mcp__serena__replace_symbol_body({
  symbol_name: "haversineDistance",
  file_path: "src/utils/geoUtils.js",
  new_body: `
    const R = 6371e3; // Rayon Terre en mètres
    const φ1 = lat1 * Math.PI / 180;
    const φ2 = lat2 * Math.PI / 180;
    const Δφ = (lat2 - lat1) * Math.PI / 180;
    const Δλ = (lon2 - lon1) * Math.PI / 180;

    const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ/2) * Math.sin(Δλ/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    return R * c;
  `
})
```

### Exemple 2 : Ajouter un hook
```javascript
mcp__serena__add_symbol({
  file_path: "src/hooks/useOfflineStatus.js",
  symbol_type: "function",
  symbol_name: "useOfflineStatus",
  body: `
    import { useState, useEffect } from 'react';

    export function useOfflineStatus() {
      const [isOffline, setIsOffline] = useState(!navigator.onLine);

      useEffect(() => {
        const handleOnline = () => setIsOffline(false);
        const handleOffline = () => setIsOffline(true);

        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);

        return () => {
          window.removeEventListener('online', handleOnline);
          window.removeEventListener('offline', handleOffline);
        };
      }, []);

      return isOffline;
    }
  `,
  position: "start"
})
```

## Bonnes Pratiques

1. **Toujours find_symbol avant replace** pour vérifier la version actuelle
2. **Tester après chaque modification** avec `npm run build`
3. **Utiliser rename_symbol** plutôt que rechercher-remplacer manuel
4. **Préserver les exports** lors de modifications

## Précautions

### Avant de modifier
- Vérifier que le symbole existe : `find_symbol`
- Vérifier les dépendances : `get_related_symbols`
- Vérifier les usages : `get_symbol_references`

### Après modification
- Vérifier la syntaxe : `npm run build`
- Vérifier les tests : `npm test` (si disponible)
- Vérifier le lint : `npm run lint`

## Anti-Patterns

❌ **Ne pas faire :**
```javascript
// Réécrire tout le fichier pour changer une fonction
Write({
  file_path: "src/utils/geoUtils.js",
  content: "... 200 lignes ..."
})
```

✅ **Faire :**
```javascript
// Cibler précisément
mcp__serena__replace_symbol_body({
  symbol_name: "targetFunction",
  new_body: "... juste le nouveau corps ..."
})
```
