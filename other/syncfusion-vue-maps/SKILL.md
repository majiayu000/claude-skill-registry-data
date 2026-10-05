---
name: syncfusion-vue-maps
description: Implement Syncfusion Vue Maps component for geographical data visualization. Always use this skill when users need to display maps, geographical data, show location-based information, markers, bubbles, or navigation lines, integrate map providers like Bing or OpenStreetMap, render GeoJSON shapes, zooming and panning, data labels or legends to maps, color-code regions based on data values, or create any map-based visualization in Vue applications.
metadata:
  author: "Syncfusion Inc"
  category: "Data Visualization"
  version: "34.1.29"
---

# Implementing Syncfusion Vue Maps

A comprehensive skill for implementing the Syncfusion Vue Maps component to visualize geographical data with rich interactivity, multiple layers, markers, bubbles, legends, and map provider integration.

## When to Use This Skill

Use this skill when you need to:
- **Display geographical data** on interactive maps
- **Visualize location-based information** with markers, bubbles, or data labels
- **Create choropleth maps** with color-coded regions based on data values
- **Integrate map providers** like Bing Maps, OpenStreetMap, or Azure Maps
- **Render custom shapes** from GeoJSON data files
- **Build multi-layer maps** with overlays and sublayers
- **Add navigation lines** to show routes or connections between locations
- **Implement zooming and panning** for map exploration
- **Display statistical data** on geographical regions
- **Create interactive legends** for data interpretation
- **Support multiple projections** (Mercator, Miller, Eckert, etc.)
- **Handle user interactions** like tooltips, selection, and highlighting

## Component Overview

The Syncfusion Vue Maps component is a powerful data visualization tool that renders geographical data using Scalable Vector Graphics (SVG). It supports:

- **Any number of layers and sublayers** for complex visualizations
- **GeoJSON data binding** for custom shape rendering
- **Map providers** (Bing, OpenStreetMap, Azure) as base layers
- **6 types of projections** for different map representations
- **Visual elements**: Markers, Bubbles, Navigation Lines, Annotations, Data Labels, Legends
- **Interactive features**: Zooming, Panning, Tooltips, Selection, Highlighting
- **Accessibility**: WCAG 2.1 compliant with keyboard navigation
- **Globalization**: RTL support, internationalization, localization

## Key Capabilities

### Data Visualization Elements
- **Markers**: Pin locations with custom shapes, templates, and clustering
- **Bubbles**: Display data magnitude with size-based bubbles
- **Data Labels**: Show information directly on map shapes
- **Color Mapping**: Apply colors based on data values (equal, range, desaturation)
- **Navigation Lines**: Draw connections between locations with curves and arrows
- **Legends**: Provide visual keys for data interpretation

### Layer Architecture
- **Main Layer**: Base map from GeoJSON or map provider
- **Sublayers**: Overlay additional shapes on top of main layer
- **Multi-layer Support**: Stack multiple layers for rich visualizations

### Map Providers
- **Bing Maps**: Satellite, aerial, and road views
- **OpenStreetMap**: Free tile layer provider
- **Azure Maps**: Microsoft's map service
- **Hybrid Approach**: Combine GeoJSON shapes with provider tiles

### User Interactions
- **Zooming**: Mouse wheel, double-click, pinch, toolbar controls
- **Panning**: Drag to explore different regions
- **Tooltips**: Show data on hover
- **Selection**: Highlight shapes on click
- **Reset**: Return to initial view

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference-complete.md](references/api-reference-complete.md)

Headings:

- Properties
- Data Models
- Events
- Methods
- Enums
- Child Directives
- Modules / Services
- Common Usage Patterns
- Additional Resources

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package dependencies
- Basic Maps component implementation
- GeoJSON data structure and binding
- CSS theme imports
- Vue 2 vs Vue 3 setup
- First world map example
- Data source binding with shapeDataPath and shapePropertyPath

### Layers and Structure
📄 **Read:** [references/layers-and-sublayers.md](references/layers-and-sublayers.md)
- Understanding layer architecture
- Main layer vs sublayer differences
- Creating multi-layer maps
- Layer types and stacking order
- Layer-specific settings and configuration
- When to use multiple layers

### Markers
📄 **Read:** [references/markers.md](references/markers.md)
- Adding markers to pinpoint locations
- Marker data source structure (latitude, longitude)
- Marker shapes and custom templates
- Marker clustering for dense data
- Dynamic marker updates
- Interactive markers with click events
- Marker tooltips and labels

### Data Visualization Elements
📄 **Read:** [references/data-visualization.md](references/data-visualization.md)
- Bubble visualization for data magnitude
- Configuring bubble size and colors
- Data label setup and formatting
- Smart label modes (trim, hide, none)
- Label templates for custom content
- Navigation lines for connections and routes
- Combining multiple visual elements

### Color Mapping
📄 **Read:** [references/color-mapping.md](references/color-mapping.md)
- Color mapping types (equal, range, desaturation)
- Applying colors based on data values
- Setting up colorValuePath
- Creating choropleth maps
- Multiple color mapping rules
- Custom color schemes
- Visual data representation strategies

### Legend
📄 **Read:** [references/legend.md](references/legend.md)
- Enabling and configuring legends
- Positioning strategies (absolute, dock)
- Legend alignment options (near, center, far)
- Interactive legends
- Legend modes (default, interactive)
- Customizing legend appearance
- Syncing legends with color mapping

### Map Providers and Sources
📄 **Read:** [references/map-providers.md](references/map-providers.md)
- Overview of supported providers
- When to use GeoJSON vs map providers
- Bing Maps setup and API keys
- OpenStreetMap integration (free)
- Azure Maps configuration
- Tile layer types (satellite, aerial, road)
- Hybrid approaches (GeoJSON overlays on provider tiles)

### User Interactions
📄 **Read:** [references/user-interactions.md](references/user-interactions.md)
- Enabling and configuring zooming
- Zoom factor and toolbar controls
- Panning functionality
- Tooltip configuration and templates
- Selection and highlighting shapes
- Mouse wheel and double-click zoom
- Pinch zoom for touch devices
- Event handling and listeners

### Customization and Advanced Features
📄 **Read:** [references/customization-advanced.md](references/customization-advanced.md)
- Map projections (Mercator, Miller, Eckert, Winkel Tripel, Aitoff, Equirectangular)
- Title and subtitle configuration
- Border and background styling
- Annotations and custom overlays
- Internationalization (i18n)
- Localization (l10n)
- Accessibility (WCAG compliance, keyboard navigation)
- State persistence across sessions
- Printing and export functionality
- Performance optimization techniques

## Quick Start Example

```vue
<template>
  <div id="map-container">
    <ejs-maps>
      <e-layers>
        <e-layer :shapeData="shapeData" :dataSource="dataSource" :shapeDataPath="shapeDataPath" :shapePropertyPath="shapePropertyPath"
          :shapeSettings="shapeSettings">
        </e-layer>
      </e-layers>
    </ejs-maps>
  </div>
</template>

<script>
import { MapsComponent, LayersDirective, LayerDirective, Inject, Legend } from '@syncfusion/ej2-vue-maps';
import { world_map } from './world-map'; // GeoJSON data

export default {
  components: {
    'ejs-maps': MapsComponent,
    'e-layers': LayersDirective,
    'e-layer': LayerDirective
  },
  provide: {
    maps: [Legend]
  },
  data() {
    return {
      shapeData: world_map,
      dataSource: [
        { Country: 'United States', Population: 331000000 },
        { Country: 'Russia', Population: 145900000 },
        { Country: 'China', Population: 1439000000 }
      ],
      shapeDataPath: 'Country',
      shapePropertyPath: 'name',
      shapeSettings: {
        colorValuePath: 'Population',
        colorMapping: [
          { value: 331000000, color: '#D84444' },
          { value: 145900000, color: '#316DB5' }
        ]
      }
    };
  }
};
</script>
```

## Module Injection Guide

Maps features are modular. Inject only the modules you need via the `provide` option:

```javascript
provide: {
  maps: [
    Legend,           // For legends
    DataLabel,        // For data labels
    Marker,           // For markers
    Bubble,           // For bubbles
    MapsTooltip,      // For tooltips
    Zoom,             // For zooming and panning
    Highlight,        // For highlighting shapes
    Selection,        // For selecting shapes
    NavigationLine,   // For navigation lines
    Annotations,      // For annotations
    Polygon           // For polygons
  ]
}
```

**Only inject modules for features you're using** to minimize bundle size.

## Common Use Cases

### Choropleth Map (Color-Coded Regions)
**Goal**: Display statistical data with color-coded countries/regions

**Approach**:
1. Bind data source with `dataSource`, `shapeDataPath`, `shapePropertyPath`
2. Configure `shapeSettings.colorValuePath` to specify data field
3. Set up `colorMapping` with value-color pairs
4. Add `Legend` for interpretation

**Example**: Population density map, election results, COVID-19 statistics

---

### Location Markers Map
**Goal**: Show specific locations with custom markers

**Approach**:
1. Add `MarkersDirective` inside `LayerDirective`
2. Provide marker data with latitude/longitude
3. Customize marker shapes, sizes, and templates
4. Add tooltips for marker information

**Example**: Store locator, branch offices, tourist attractions

---

### Multi-Layer Overlay
**Goal**: Highlight specific regions on a base map

**Approach**:
1. First layer: Base map (e.g., entire country)
2. Additional layers with type="SubLayer": Highlighted regions
3. Style sublayers distinctly (different colors, borders)
4. Control layer visibility and order

**Example**: State highlights on country map, sales regions

---

### Route Visualization
**Goal**: Show connections or routes between locations

**Approach**:
1. Add markers for start/end points
2. Use `NavigationLineDirective` to draw lines
3. Configure line curves, arrows, and styling
4. Optionally animate lines

**Example**: Flight routes, shipping lanes, migration patterns

---

### Map Provider Integration
**Goal**: Use real-world satellite/street map as base

**Approach**:
1. Configure layer with `urlTemplate` for provider
2. Set up API keys (Bing, Azure) if required
3. Overlay GeoJSON shapes as sublayers if needed
4. Add markers and labels on top

**Example**: Real estate map, delivery tracking, ride-sharing app

## Decision Trees

### Should I Use GeoJSON or Map Provider?

**Use GeoJSON when**:
- You need custom shapes or boundaries
- Data is region/country-based (choropleth maps)
- No real-world street-level detail needed
- Offline capability required
- Full control over styling and data binding

**Use Map Provider when**:
- Need real-world satellite/aerial imagery
- Street-level detail required
- Real-time map updates desired
- Users expect familiar map interface (like Google Maps)

**Use Both (Hybrid) when**:
- Need real-world base with custom shape overlays
- Combining statistical regions with street context

---

### Which Color Mapping Type?

**Equal Color Mapping**: 
- Use when data has discrete categories (e.g., Membership: Permanent/Non-Permanent)
- Each unique value gets a specific color

**Range Color Mapping**:
- Use when data is numeric and continuous (e.g., Population: 0-1M, 1M-10M, 10M+)
- Values within ranges get assigned colors

**Desaturation Color Mapping**:
- Use for gradient effects based on numeric values
- Single color with varying saturation levels

---

### How Many Layers Should I Use?

**Single Layer**:
- Simple visualizations with one data dimension
- Basic country/region maps
- When all data fits one layer

**Multiple Layers**:
- Highlighting specific regions on base map
- Combining different data sources
- Creating visual depth with overlays
- Showing borders, rivers, cities separately

## Key Props Reference

### MapsComponent
- `titleSettings`: Configure title and subtitle
- `legendSettings`: Legend visibility, position, alignment
- `zoomSettings`: Enable zooming, set initial zoom factor
- `layers`: Array of layer configurations

### LayerDirective
- `shapeData`: GeoJSON data for shapes
- `dataSource`: Data to bind to shapes
- `shapeDataPath`: Field in dataSource matching shapes
- `shapePropertyPath`: Field in GeoJSON matching dataSource
- `shapeSettings`: Fill, border, color mapping
- `type`: "Layer" (main) or "SubLayer" (overlay)
- `markerSettings`: Marker configurations
- `bubbleSettings`: Bubble visualizations
- `dataLabelSettings`: Label configurations
- `tooltipSettings`: Tooltip customization
- `navigationLineSettings`: Line visualizations

### Common Patterns
- **Module Injection**: Only inject needed services to reduce bundle size
- **Data Binding**: Use shapeDataPath + shapePropertyPath for automatic matching
- **Progressive Enhancement**: Start with basic map, add features incrementally
- **Responsive Design**: Maps auto-resize, but test on different viewports

## Troubleshooting Quick Checks

❌ **Map not displaying**: 
- Verify GeoJSON data is correctly imported
- Check console for errors
- Ensure CSS is imported

❌ **Colors not applied**:
- Confirm `shapeDataPath` matches data field name
- Verify `shapePropertyPath` matches GeoJSON property
- Check `colorValuePath` points to correct data field

❌ **Markers not showing**:
- Inject `Marker` service
- Set `visible={true}` in MarkerDirective
- Verify latitude/longitude values are valid

❌ **Zoom not working**:
- Inject `Zoom` service
- Set `enable={true}` in zoomSettings
- Check if `enablePanning` is needed

❌ **Legend not appearing**:
- Inject `Legend` service
- Set `visible={true}` in legendSettings
- Ensure color mapping is configured

## Next Steps

1. **Start Simple**: Begin with getting-started.md for basic map
2. **Add Data**: Follow data-visualization.md for markers/bubbles
3. **Style It**: Use color-mapping.md for choropleth effects
4. **Make Interactive**: Implement user-interactions.md for zoom/pan
5. **Enhance**: Add advanced features as needed

Choose the reference documentation that matches your current implementation phase and specific requirements.
