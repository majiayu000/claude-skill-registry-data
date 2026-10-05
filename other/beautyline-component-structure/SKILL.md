---
name: beautyline-component-structure
description: >-
  File and folder naming, barrel exports, and import paths for React
  components in the Beautyline webapp. Use when adding components, renaming
  files, or choosing between admin vs marketing folder conventions.
---

# Beautyline: component structure

## Default pattern (marketing / shared sections)

- **Folder**: **PascalCase** matching the feature or component concept (e.g. `AcademicPathsSection`, `CourseDetailView`).
- **Main file**: **kebab-case** `.tsx` (e.g. `academic-paths-section.tsx`, `course-detail-view.tsx`).
- **Export**: Named export matching the PascalCase component name.

## Admin and small utilities

- Under `src/components/admin/`, **`PascalCase.tsx`** filenames are acceptable and already used (`CourseTypeSelect.tsx`, `ImageUpload.tsx`). Keep this area consistent with existing neighbors in the same folder.

## Barrel `index.ts`

- Some feature folders expose a public API via **`index.ts`** (`CourseDetailView/index.ts`). Add a barrel when multiple files coexist in one folder **and** importers should import from `@/components/FeatureName` without reaching into internal filenames.
- If the folder contains only **one** main component file, a barrel is optional unless re-exports consolidate subcomponents used outside the folder.

## Imports

- Use **`@/components/...`** and **`@/lib/...`** — avoid deep relative chains like `../../../` when crossing `src/` boundaries.

## Naming alignment

- **Props**: `interface ComponentNameProps` in the component file (`ComponentNameProps`, not generic `Props` at module scope unless the file exports a single component).
