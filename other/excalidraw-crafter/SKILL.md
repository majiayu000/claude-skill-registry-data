---
name: excalidraw-crafter
description: Utiliza este skill cuando el usuario pida dibujar pizarras, diagramas de arquitectura, bocetos UI o esquemas de cajas libres que requieran geometría manual 2D y un alto grado de personalización posterior. Genera el código fuente JSON de Excalidraw (.excalidraw) para importación directa.
collection: smart-money-activity
promotable: true
---

# Excalidraw Crafter

This skill empowers Claude to author raw, editable `.excalidraw` whiteboard files. Because Excalidraw relies on a strict JSON payload describing coordinates, dimensions, types, and groupings, you must structure the data carefully rather than relying on Markdown text.

## When to Use This Skill

- The user asks for a flowchart, architecture diagram, wireframe, or whiteboard layout.
- The user specifically mentions "Excalidraw" or "editable whiteboard file."
- The output needs to be a file that the user can later move objects around in visually via `excalidraw.com` or a VS Code extension, rather than a frozen image or a strict radial mind map.

## 🛑 REQUIRED INTERACTIVE WORKFLOW (DO NOT SKIP)

**Under no circumstances generate the JSON code immediately if the user hasn't explicitly specified a layout type.** 
When a user requests an Excalidraw diagram, you MUST STOP and present the following 5 options with their descriptions, asking the user to choose one:

1. **🌳 Árbol Jerárquico Horizontal**: Nodo raíz situado a la izquierda con ramas que se abren secuencialmente hacia la derecha. *(Ideal para: desglosar temarios de cursos, organigramas o índices de libros).*
2. **🌟 Mapa Mental Radial**: Un núcleo central en medio del lienzo del que orbitan las ideas principales y secundarias en forma de estrella. *(Ideal para: lluvia de ideas creativas, conceptos no lineales y explorar conexiones orgánicas).*
3. **⬇️ Flujo Descendente (Flowchart)**: Cajas y rombos geométricos conectados de arriba hacia abajo en forma de cascada. *(Ideal para: diagramas de flujo, embudos de conversión, algoritmos o paso a paso de procesos).*
4. **🗂️ Tablero en Matriz (Grid / Kanban)**: Distribución tipo tarjetas alineadas en columnas y filas exactas, sin conectores complejos. *(Ideal para: comparativas, dashboards estructurales, o agrupar conceptos por categorías estrictas).*
5. **🐟 Diagrama Raspa de Pez (Fishbone / Timeline)**: Una espina dorsal horizontal (eje principal o temporal) de la que salen ramas oblicuas hacia arriba y abajo. *(Ideal para: análisis de causa, líneas de tiempo o hitos secuenciales).*

**Style Options:** Along with the 5 layouts, always ask if they want the **Standard Corporate Style** (clean lines, solid fills, standard fonts) or the **Sketch/Hand-Drawn Style** (marker look, `virgil` font, `hachure` fills, imperfect `roughness`).

Wait for the user's reply before proceeding to step 1.

## Excalidraw File Format Architecture

An `.excalidraw` file is strictly a JSON document. To write one, generate the content to match this schema and save the file with the `.excalidraw` extension (e.g., `system_architecture.excalidraw`).

### Base Structure
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    // Your drawing nodes go here
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

## How to Execute the Workflow

### 1. Conceptualize the Grid
Before writing the JSON, calculate rough X and Y coordinates. A typical bounding box for a rectangle might have a `width` of 150-200 and a `height` of 50-80. Space them out using multiples of 300 for `x` and 150 for `y` to prevent overlapping.

### 2. Craft the Elements Array
Populate the `elements` array. You must provide a valid 8-10 character alphanumeric string for each element's `id`.

**Rectangle Example:**
```json
{
  "id": "box123456",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 180,
  "height": 60,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#e0eaff",
  "fillStyle": "hachure",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100
}
```

**Text Example:**
*(To attach text to a rectangle, give the text element the exact same `x`, `y`, `width`, and `height` as the container box and rely on `textAlign: "center"`)*
```json
{
  "id": "text12345",
  "type": "text",
  "x": 100,
  "y": 120, // slightly offset to center vertically inside a 60px height box
  "width": 180,
  "height": 20,
  "angle": 0,
  "strokeColor": "#000000",
  "backgroundColor": "transparent",
  "fillStyle": "hachure",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "text": "Database Server",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle"
}
```

### 3. Connect Elements with Arrows
To draw an arrow from `box123456` to another element, map the start and end coordinates.
```json
{
  "id": "arrow123",
  "type": "arrow",
  "x": 280, // Right edge of box1
  "y": 130, // Middle of box1
  "width": 120,
  "height": 0,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "hachure",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "points": [
    [0, 0], // Start relative to arrow x/y
    [120, 0] // End relative to arrow x/y
  ],
  "startBinding": { "elementId": "box123456", "focus": -0.5, "gap": 15 },
  "endBinding": { "elementId": "anotherBoxId", "focus": -0.5, "gap": 15 }
}
```

### 4. Provide the File
Write the final JSON string into your `.excalidraw` file using the `write_to_file` tool. **Important: ALWAYS save the file inside the `diagrams/` folder of this skill** (e.g., `diagrams/system_architecture.excalidraw`).
Tell the user that they can now open this file entirely using the VS Code Excalidraw plugin or by dragging it into Excalidraw's web interface.
