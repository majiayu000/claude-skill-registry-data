---
name: postgis-spatial
description: >-
  Use when working with geographic queries, geometry filtering, ST_* functions,
  or region-based candidate filtering. Load for PostGIS spatial operations,
  polygon intersections, distance calculations, or geographic bounds. Covers
  ST_Intersects, ST_Contains, GiST indexes, and geometry storage patterns.
---

# PostGIS Spatial

Geographic query patterns for place and region filtering.

> **Announce:** "I'm using postgis-spatial to implement geographic queries correctly."

## Geometry Storage

Places store their geometry as PostGIS geometry:

```sql
CREATE TABLE places (
  id uuid PRIMARY KEY,
  name text NOT NULL,
  geom geometry(Geometry, 4326),  -- Can be Point, Polygon, or MultiPolygon
  -- SRID 4326 = WGS84 (standard lat/lng)
);

-- GiST index for spatial queries
CREATE INDEX idx_places_geom ON places USING gist (geom);
```

Geographic regions for questions:

```sql
CREATE TABLE geographic_regions (
  id uuid PRIMARY KEY,
  name text NOT NULL,
  region_type text,  -- 'continent', 'country', 'subregion'
  geom geometry(MultiPolygon, 4326)
);

CREATE INDEX idx_geographic_regions_geom 
ON geographic_regions USING gist (geom);
```

## Core Functions

### ST_Intersects - Overlap Check

```sql
-- Does place intersect with region?
SELECT p.id, p.name
FROM places p
JOIN geographic_regions r ON ST_Intersects(p.geom, r.geom)
WHERE r.name = 'Europe';
```

### ST_Contains - Fully Inside

```sql
-- Is place fully contained within region?
SELECT p.id, p.name
FROM places p
JOIN geographic_regions r ON ST_Contains(r.geom, p.geom)
WHERE r.name = 'France';
```

### ST_DWithin - Distance Check

```sql
-- Places within 100km of a point
SELECT p.id, p.name
FROM places p
WHERE ST_DWithin(
  p.geom::geography,
  ST_Point(2.3522, 48.8566)::geography,  -- Paris
  100000  -- 100km in meters
);
```

## Geographic Candidate Filtering

The game uses geographic questions to narrow candidates:

```sql
-- Filter candidates by answered geographic questions
CREATE FUNCTION filter_geographic_candidates(
  p_session_id uuid,
  p_include_regions uuid[],  -- Must intersect ALL of these
  p_exclude_regions uuid[]   -- Must NOT intersect ANY of these
)
RETURNS TABLE (place_id uuid) AS $$
BEGIN
  RETURN QUERY
  SELECT p.id
  FROM places p
  WHERE 
    -- Include logic: Must intersect ALL confirmed regions
    (p_include_regions IS NULL OR (
      SELECT COUNT(*) FROM unnest(p_include_regions) AS r(rid)
      JOIN geographic_regions gr ON gr.id = r.rid
      WHERE ST_Intersects(p.geom, gr.geom)
    ) = array_length(p_include_regions, 1))
    
    -- Exclude logic: Must NOT intersect ANY excluded region
    AND (p_exclude_regions IS NULL OR NOT EXISTS (
      SELECT 1 FROM unnest(p_exclude_regions) AS r(rid)
      JOIN geographic_regions gr ON gr.id = r.rid
      WHERE ST_Intersects(p.geom, gr.geom)
    ));
END;
$$ LANGUAGE plpgsql;
```

**Logic:**
- Include = AND (must be in ALL confirmed regions)
- Exclude = OR (must not be in ANY excluded region)

## Split Quality for Questions

Geographic questions are ranked by how well they split candidates:

```sql
-- Calculate how evenly a region splits current candidates
SELECT 
  r.id,
  r.name,
  COUNT(*) FILTER (WHERE ST_Intersects(p.geom, r.geom)) AS yes_count,
  COUNT(*) FILTER (WHERE NOT ST_Intersects(p.geom, r.geom)) AS no_count,
  -- Split quality: 1.0 = perfect 50/50, 0.5 = all one side
  1.0 - ABS(0.5 - (
    COUNT(*) FILTER (WHERE ST_Intersects(p.geom, r.geom))::float / COUNT(*)
  )) AS split_quality
FROM candidate_places p
CROSS JOIN geographic_regions r
GROUP BY r.id, r.name
ORDER BY split_quality DESC;
```

## Geometry Types

Handle different geometry types:

```sql
-- Extract centroid for any geometry type
SELECT 
  id,
  ST_X(ST_Centroid(geom)) AS lng,
  ST_Y(ST_Centroid(geom)) AS lat
FROM places;

-- Get bounding box
SELECT 
  id,
  ST_XMin(geom) AS min_lng,
  ST_YMin(geom) AS min_lat,
  ST_XMax(geom) AS max_lng,
  ST_YMax(geom) AS max_lat
FROM places;
```

## Anti-Patterns

### DON'T: Forget Geography Cast for Distance

```sql
-- WRONG: Distance in degrees (meaningless)
SELECT ST_Distance(a.geom, b.geom) FROM ...

-- CORRECT: Cast to geography for meters
SELECT ST_Distance(a.geom::geography, b.geom::geography) FROM ...
```

### DON'T: Skip GiST Index

Without index, spatial queries do sequential scan:

```sql
-- ALWAYS create GiST index on geometry columns
CREATE INDEX idx_table_geom ON table USING gist (geom);
```

### DON'T: Mix SRIDs

```sql
-- WRONG: Different SRIDs
ST_Intersects(geom_4326, geom_3857)

-- CORRECT: Transform to same SRID
ST_Intersects(geom_4326, ST_Transform(geom_3857, 4326))
```

## Creating Points from Lat/Lng

```sql
-- Create point geometry from coordinates
-- NOTE: ST_Point takes (longitude, latitude) - X, Y order!
SELECT ST_SetSRID(ST_Point(longitude, latitude), 4326) AS geom;

-- WRONG: Lat/Lng order
ST_Point(48.8566, 2.3522)  -- This puts Paris in the wrong place!

-- CORRECT: Lng/Lat order
ST_Point(2.3522, 48.8566)  -- Paris
```

## References

See `references/spatial-queries.md` for more examples.
