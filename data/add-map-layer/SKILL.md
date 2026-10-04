---
name: add-map-layer
description: Add a data visualization layer to the Mapbox GL map page (heatmap, markers, clusters, isochrones). Use when building geospatial features like price heat maps or catchment analysis.
---

# add-map-layer

Adds a new data layer to the existing map page. Supports heatmaps, clustered markers, polygon overlays, and isochrone areas.

## Inputs to gather

- **Layer type** — heatmap, markers, clusters, polygons, isochrone
- **Data source** — API endpoint that returns GeoJSON or coordinate data
- **Visual encoding** — what property maps to color/size (e.g., price → heat intensity)
- **Toggle** — should the user be able to show/hide this layer?

## Steps

1. **Create the data API endpoint:**
   ```typescript
   router.get("/analytics/geo/{layer-name}", authenticateToken, async (req, res) => {
     const data = await prisma.properties.findMany({
       where: { latitude: { not: null } },
       select: { id: true, latitude: true, longitude: true, price: true, type: true },
     });
     // Return as GeoJSON FeatureCollection
     res.json({
       type: "FeatureCollection",
       features: data.map(p => ({
         type: "Feature",
         geometry: { type: "Point", coordinates: [p.longitude, p.latitude] },
         properties: { id: p.id, price: Number(p.price), type: p.type },
       })),
     });
   });
   ```

2. **Add the layer to the map component** at `apps/web/src/pages/map/index.tsx`:
   ```typescript
   // After map loads:
   map.addSource("price-heatmap", { type: "geojson", data: geojsonData });
   map.addLayer({
     id: "price-heatmap-layer",
     type: "heatmap",
     source: "price-heatmap",
     paint: {
       "heatmap-weight": ["interpolate", ["linear"], ["get", "price"], 0, 0, 5000000, 1],
       "heatmap-intensity": 1,
       "heatmap-radius": 30,
       "heatmap-color": [
         "interpolate", ["linear"], ["heatmap-density"],
         0, "rgba(0,0,0,0)", 0.2, "#ffffb2", 0.4, "#fd8d3c", 0.6, "#f03b20", 0.8, "#bd0026",
       ],
     },
   });
   ```

3. **Add layer toggle** in the map toolbar:
   ```tsx
   <Button variant={showHeatmap ? "default" : "outline"} onClick={() => toggleLayer("price-heatmap")}>
     خريطة الأسعار
   </Button>
   ```

4. **Add click interaction** — click on area → tooltip with aggregated stats.

5. **Use react-query** to fetch GeoJSON data with `/add-react-query`.

## Verification checklist

- [ ] Layer renders correctly on the map
- [ ] Data points are positioned accurately
- [ ] Toggle shows/hides the layer
- [ ] Click interaction shows correct data
- [ ] Performance: handles 5K+ points without lag
- [ ] `/typecheck` passes

## Anti-patterns

- Don't load all data at once for large datasets — use viewport-based loading or clustering
- Don't use Google Maps — project uses Mapbox GL JS (free tier: 50K loads/month)
- Don't hardcode map styles — use the existing map configuration
- Don't block the main thread — fetch GeoJSON async, add layer after load
