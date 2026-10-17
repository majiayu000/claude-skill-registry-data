---
name: draw-tldraw
description: Create .tldr files from shape descriptions
argument-hint: "[description]"
related:
  - draw-excalidraw

---
## Goal

Create a `.tldr` file from a drawing or diagram description

## Scope

- Generate JSON per the tldraw schema
- Supports shapes: geo, text, draw, arrow, line, note
- Creates files openable in the tldraw app or VS Code extension

## Execute

### 1. Parse Description

> Goal: Understand the drawing

1. Take the description from the user
2. Identify the shapes and text to create
3. Set the page size and positions
4. If complex → create a simple layout first

### 2. Generate Schema

> Goal: Build the JSON per tldraw

1. Use the schema:
   ```json
   {
     "tldrawFileFormatVersion": 1,
     "schema": {
       "schemaVersion": 2,
       "sequences": {
         "com.tldraw.store": 5,
         "com.tldraw.page": 1,
         "com.tldraw.shape.geo": 11,
         "com.tldraw.shape.text": 4,
         "com.tldraw.shape.arrow": 8,
         "com.tldraw.shape.draw": 4,
         "com.tldraw.shape.line": 5,
         "com.tldraw.shape.note": 10,
         "com.tldraw.shape.group": 0
       }
     },
     "records": []
   }
   ```
2. Create records for `document`, `page`, and each shape
3. Each shape record must have `id`, `typeName: "shape"`, `parentId`, `pageId`, `index`, `type`, `x`, `y`, `props`

### 3. Save File

> Goal: Save the file

1. Save as `<name>.tldr`
2. Validate the JSON
3. Report the path

## Rules

### 1. Schema

- Must have `tldrawFileFormatVersion`, `schema`, `records`
- `schemaVersion` should be 2
- `records` must contain `document`, `page`, and shapes

### 2. Shape Types

- `geo` for rectangle, ellipse, triangle, diamond
- `text` for labels
- `arrow` for connecting shapes
- `draw` for freehand
- `note` for sticky notes

### 3. Simple First

- Create a simple drawing first
- Add detail gradually if the user wants it

- Use /draw-excalidraw if needed

## Expected Outcome

- A `.tldr` file openable in tldraw
- Contains complete records
- JSON valid and schema-correct
