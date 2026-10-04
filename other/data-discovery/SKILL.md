---
name: data-discovery
description: "Assists with discovering and verifying geospatial datasets, particularly for open data portals, OSM, Copernicus, and Bhuvan."
---

# Geospatial Data Discovery Skill

Use this skill when you need to verify the availability, accessibility, and metadata of geospatial datasets before downloading them.

## Best Practices

1. **Verify HTTP Status & Headers First:** Don't download a massive GeoTIFF or shapefile just to see if it exists. Use HTTP HEAD requests or range requests to check the file size and server response.
2. **OpenCity / Local Data:** When checking sites like `data.opencity.in`, parse the HTML for `.kml`, `.geojson`, or `.shp.zip` links.
3. **Copernicus Data Space:** GLO-30 is a DSM available via Copernicus. It often requires OData API queries or STAC API (`https://catalogue.dataspace.copernicus.eu/stac`).
4. **OSM Overpass:** Use the Overpass API to check for `building:levels` in a specific bounding box.
5. **Bhuvan NRSC:** Bhuvan requires login for CartoDEM downloads. If it requires authentication, mark it as requiring manual download.
