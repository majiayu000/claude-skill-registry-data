---
name: syncfusion-vue-diagram
description: Build interactive diagrams using Syncfusion Vue Diagram, including flowcharts, BPMN workflows, UML diagrams, Entity Relationship (ER) diagrams, swimlanes, and organizational charts. Trigger when working with Vue diagram components such as nodes, connectors, shapes, ports, labels, layouts, symbol palettes, serialization/deserialization with unsaved changes detection, Mermaid syntax support, data binding, interactive editing, and exporting diagrams for visualization and process flows.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Diagrams with Syncfusion Vue

The Syncfusion Vue Diagram component enables you to create interactive, customizable diagrams for visualizing complex processes, organizational hierarchies, workflows, and data relationships. From simple flowcharts to advanced BPMN diagrams and UML representations, the Diagram component provides comprehensive tools for visual communication.

## When to Use This Skill

- **Flowcharts & Process Diagrams** — Visualize workflows, decision trees, or procedural flows
- **Organizational Charts** — Represent hierarchical structures with automatic layouts
- **BPMN Workflows** — Design business process models with activities, gateways, and events
- **UML Diagrams** — Create class diagrams, sequence diagrams, and structured relationships
- **Mind Maps & Radial Trees** — Organize ideas and concepts hierarchically
- **Swimlane Diagrams** — Show processes across multiple actors or departments
- **Custom Shapes & Connectors** — Build tailored diagrams with styled nodes and labeled connections
- **Interactive Visualization** — Enable drag-drop, selection, pan/zoom, and user interaction

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and npm packages (Vue 2/3/Next.js/Preact)
- Project setup with Vite/CRA
- CSS imports and theme configuration
- Basic DiagramComponent usage
- Module injection basics

### Core Elements: Nodes
📄 **Read:** [references/nodes.md](references/nodes.md)
- Creating and adding nodes to diagrams
- Node positioning (offsetX/Y, width/height)
- Node shape types (Flow, Basic, Path)
- Styling nodes (fill, stroke, opacity, shadows)
- Node customization and templates
- Expand/collapse functionality
- Node events and callbacks

### Core Elements: Connectors
📄 **Read:** [references/connectors.md](references/connectors.md)
- Connector types (Straight, Orthogonal, Bezier)
- Segment configuration and routing
- Connecting nodes via sourceID/targetID
- Advanced segments and bezier curves
- Connector customization and styling
- Connector events and interaction

### Annotations: Labels & Text
📄 **Read:** [references/labels-and-annotations.md](references/labels-and-annotations.md)
- Adding labels to nodes and connectors
- Label styling (font, color, alignment, rotation)
- Label interaction (edit, drag, resize)
- Label positioning and offset
- Label events

### Connection Points: Ports
📄 **Read:** [references/ports.md](references/ports.md)
- Port types and connection points on nodes
- Port positioning and visibility
- Port appearance and styling
- Connecting connectors to specific ports
- Port interaction and events

### Shapes & Visual Styling
📄 **Read:** [references/shapes-and-styles.md](references/shapes-and-styles.md)
- Built-in shape types (Flow, Basic, Path, Image, HTML)
- Flow chart shape reference
- Style properties (fill, stroke, dash, shadow)
- CSS class customization
- Theme integration

### BPMN Diagrams
📄 **Read:** [references/bpmn-diagrams.md](references/bpmn-diagrams.md)
- BPMN module injection and setup
- BPMN shape overview and types
- Activities (task, subprocess, expanded subprocess)
- Events (start, end, intermediate)
- Gateways (exclusive, parallel, inclusive)
- Flows (sequence, message, association)
- Data objects and data sources
- Groups and text annotations

### UML Diagrams
📄 **Read:** [references/uml-diagrams.md](references/uml-diagrams.md)
- UML class diagrams
- Classifier shapes (class, interface, enumeration)
- UML relationships and associations
- UML sequence diagram elements and participants
- Participant stereotypes (Actor, Boundary, Control, Entity, Database, Default)
- Message types (Synchronous, Asynchronous, Reply, Create, Delete, Self)
- Activation boxes and lifelines
- Complete workflow examples

### Entity Relationship Diagrams
📄 **Read:** [references/implementing-entity-relationship-diagrams.md](references/entity-relationship-diagrams.md)
- Entity Relationship (ER) diagram concepts and models
- ER shape configuration with fields and properties
- Field constraints (NotNull, Unique, Primary Key, Foreign Key)
- Relationship types and multiplicities (One, OneAndOnlyOne, Many, ZeroOrOne, OneOrMany, ZeroOrMany)
- ER connectors and relationship configuration
- Runtime field management and manipulation

### Automatic Layouts
📄 **Read:** [references/layouts.md](references/layouts.md)
- Hierarchical tree layout
- Organizational chart layout
- Mindmap layout
- Radial tree layout
- Flowchart layout
- Complex hierarchical configurations
- Layout customization and spacing
- Layout events and callbacks

### Swimlanes & Phases
📄 **Read:** [references/swimlanes.md](references/swimlanes.md)
- Swimlane structure and overview
- Creating lanes and phases
- Swimlane children and header configuration
- Swimlane palette
- Swimlane interaction

### Grouping & Containers
📄 **Read:** [references/groups-and-containers.md](references/groups-and-containers.md)
- Grouping nodes together
- Group operations (add/remove children)
- Container nodes and nesting
- Padding and layout within containers

### Symbol Palette
📄 **Read:** [references/symbol-palette.md](references/symbol-palette.md)
- SymbolPaletteComponent setup
- Defining palette symbols
- Drag & drop to diagram
- Palette customization (icons, search, size)
- Palette events and interactions

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- DataManager and dataSourceSettings
- id/parentId mapping for hierarchies
- Rendering org-charts from JSON data
- Remote data via DataManager (OData/Web API/REST)
- setNodeTemplate for data-driven rendering

### Interaction & Tools
📄 **Read:** [references/interaction-and-tools.md](references/interaction-and-tools.md)
- Selection, drag, resize interactions
- Tool modes (pointer, draw, pan)
- Constraints (node, connector, diagram)
- Commands and keyboard shortcuts
- Undo/Redo functionality
- Context menus
- User handles

### Serialization & Export
📄 **Read:** [references/serialization-and-export.md](references/serialization-and-export.md)
- Save/load diagrams as JSON
- Export to image (PNG, SVG, JPG) — use `exportDiagram` (inject PrintAndExport)
- Print functionality
- Visio file import/export (experimental; inject ImportAndExportVisio)
- Mermaid syntax support with `saveDiagramAsMermaid()` and `loadDiagramFromMermaid()`
- Change detection with `isModified` property for unsaved changes tracking
- EJ1 migration serialization

### Diagram Settings & Configuration
📄 **Read:** [references/diagram-settings.md](references/diagram-settings.md)
- Layers (add, lock, visibility, selection)
- Virtualization (performance optimization)
- Grid lines (snapping, dots/lines)
- Ruler (horizontal/vertical)
- Scroll settings
- Page settings (size, orientation, margins)
- Tooltip configuration
- Overview panel
- Localization and accessibility

## Quick Start

```vue
<template>
  <div id="app">
    <ejs-diagram 
      id="diagram"
      :width="width"
      :height="height"
      :nodes="nodes"
      :connectors="connectors"
      :snapSettings="snapSettings"
    ></ejs-diagram>
</div>
</template>
<script>
import { DiagramComponent,SnapConstraints } from '@syncfusion/ej2-vue-diagrams';
export default {
  name: "App",
  components: {
      "ejs-diagram": DiagramComponent
  },
  data() {
      return {
          width: "100%",
          height: "590px",
          nodes: [
            {
              id: 'node1',
              width: 100,
              height: 100,
              offsetX: 250,
              offsetY: 250,
              style: { fill: '#6BA3D5' },
              annotations: [{ content: 'Node 1' }]
            },
            {
              id: 'node2',
              width: 100,
              height: 100,
              offsetX: 450,
              offsetY: 250,
              style: { fill: '#6BA3D5' },
              annotations: [{ content: 'Node 2' }]
            }
          ],
          connectors: [
            {
              id: 'connector1',
              sourceID: 'node1',
              targetID: 'node2',
              type: 'Orthogonal'
            }
          ],
          snapSettings: {
            constraints: SnapConstraints.None
          }
      }
    }
}
</script>

<style>
@import '../node_modules/@syncfusion/ej2-vue-diagrams/styles/material.css';
</style>
```

## Vue 2 vs Vue 3 Decision Guide

**⚠️ CRITICAL:** Syncfusion Diagram works with both Vue 2 and Vue 3, but patterns differ significantly.

### Quick Decision Tree

```
┌─ Do you have an existing Vue project?
│
├─ YES, it's Vue 3 (Vite, create-vue, etc.)
│  └─ Use: Composition API with <script setup>
│     ✅ Modern, performant, recommended
│     📄 Read: getting-started.md (Vue 3 Composition API section)
│
├─ YES, it's Vue 2 (Vue CLI, legacy projects)
│  └─ Use: Options API with export default
│     ✅ Compatible, but consider migrating
│     📄 Read: getting-started.md (Vue 2 section)
│
└─ NO, starting fresh
   └─ Recommended: Vue 3 with Vite
      ✅ Fastest, most modern
      📄 Read: getting-started.md (Vite + Vue 3 setup)
```

### Version Signatures

**Vue 3 Composition API (Recommended):**
```javascript
import { ref } from 'vue';
import { DiagramComponent } from '@syncfusion/ej2-vue-diagrams';

const nodes = ref([...]);  // ← Use ref()
```

**Vue 2 Options API:**
```javascript
import { DiagramComponent } from '@syncfusion/ej2-vue-diagrams';

export default {
  data() {
    return {
      nodes: [...]  // ← Use data()
    }
  }
}
```

**⚡ Pro Tip:** If you're unsure, default to Vue 3 Composition API—it's the industry standard for new Syncfusion projects.

## Common Patterns

### Pattern 1: Creating Flowchart with Auto Layout
```javascript
// Use hierarchical layout with nodes and connectors
const layout = {
  type: 'HierarchicalTree',
  orientation: 'TopToBottom',
  horizontalSpacing: 50,
  verticalSpacing: 50,
  getLayoutInfo: (node, options) => {
    // Customize layout per node
  }
};
diagram.layout = layout;
diagram.doLayout();
```

### Pattern 2: Data-Driven Organization Chart
```javascript
// Render org chart from JSON data with DataManager
const dataSettings = {
  id: 'id',
  parentId: 'manager',
  dataSource: new DataManager(employeeData)
};
diagram.dataSourceSettings = dataSettings;
```

### Pattern 3: Interactive Node Selection
```javascript
// Handle node selection events
diagram.selectionChange = (args) => {
  console.log('Selected:', args.newItems);
};

// In Vue: bind the selectionChange event and read newValue/oldValue
// <ejs-Diagram :selectionChange="onSelectionChange" ... />
const onSelectionChange = (args) => {
  console.log('Selected:', args.newItems);
};
```

### Pattern 4: Export & Persistence (Advanced)
```javascript
// Save state and export
const jsonData = diagram.saveDiagram();
localStorage.setItem('diagram', jsonData);

// Later: Load from storage
const saved = localStorage.getItem('diagram');
diagram.loadDiagram(saved);

// Export as PNG
diagram.export({ format: 'PNG', fileName: 'diagram' });
```

## Key Props

| Prop | Type | Purpose |
|------|------|---------|
| `nodes` | Array | Collection of diagram nodes |
| `connectors` | Array | Collection of connectors linking nodes |
| `layout` | Object | Automatic layout configuration |
| `dataSourceSettings` | Object | Data binding and source configuration |
| `snapSettings` | Object | Snap constraints and guidelines |
| `pageSettings` | Object | Page size, orientation, margins |
| `scrollSettings` | Object | Pan and scroll behavior |
| `constraints` | Object | Diagram-level interaction constraints |
| `contextMenuSettings` | Object | Right-click menu configuration |
| `undoRedoSettings` | Object | Undo/redo behavior |

## Related Skills

- BPMN process modeling with Syncfusion workflows
- Data visualization layouts and hierarchies
- Interactive flowchart design
