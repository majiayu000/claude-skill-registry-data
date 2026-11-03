---
name: aegis-dept-11-vision-ocr
description: "Coding standards, operational procedures, and engineering rules for AEGIS Department 11: Autonomous Machine Vision & Optical Character Recognition"
---

# Department 11: Autonomous Machine Vision & Optical Character Recognition

> **Framework:** White Caves Engineering Matrix V2 (1-12-108 Software Core)  
> **Protocol:** Bhakti 1-12-108  
> **Director:** `@Rania` — Principal Computer Vision Systems Lead  
> **Tech Stack:** Tesseract.js, Sharp, Multer, TypeScript, PDF-parse, Canvas API  

---

## 9-Node Engineering Roster

| # | Agent | Role | Responsibility |
| :--- | :--- | :--- | :--- |
| 1 | `@Rania` *(Director)* | Principal Computer Vision Systems Lead | Owns binary file parsing systems, Live Tesseract OCR structures, and optical ingestion grids. |
| 2 | `@Dina` | Binary Byte Upload Chloroform Traffic Controller | Manages incoming multi-part byte stream buffers to isolate server memory from upload overflow crashes. |
| 3 | `@Vesta` | Media Asset Dimension Compression Developer | Scripts automated canvas image scaling filters to truncate binary file weights inside asset pipelines. |
| 4 | `@Henry` | PDF Tabular Matrix Data Extraction Specialist | Transforms unstructured document tabular streams into clean relational database array variables. |
| 5 | `@Fei_Fei_Li` | Image Object Identification Matrix Designer | Programs pattern recognition classification configurations to isolate critical data categories. |
| 6 | `@Carol_Shaw` | Raw Byte Mapping Matrix Programmer | Refines raw byte parsing logic arrays to achieve sub-millisecond data extraction performance. |
| 7 | `@Roberta_Williams` | Graphical Boundary Coordinate Mapper | Calculates spatial bounding box dimensions over blueprints to gather listing parameters. |
| 8 | `@Mary_Lou_Jepsen_Vision` | Template Image Graphic Layer Projector | Calculates precise coordinate layouts to output system values dynamically over document graphics. |
| 9 | `@Barbara_Grosz` | Natural Language Structural Field Compiler | Normalizes parsed text inputs into validated database configurations before data save updates. |

---

## Key Codebase Files & Directories

- `server/services/`
- `server/middleware/`
- `src/utils/imageOptimization.ts`

---

## Mandatory Coding Rules

1. File uploads: max 10MB per file, validate MIME type before processing
2. Image processing: use Sharp for resize/compress — never load full-res into memory
3. OCR: Tesseract.js for text extraction from Ejari documents and trade licenses
4. PDF parsing: extract tables into structured JSON arrays for database ingestion
5. Memory safety: stream large files — never buffer entire upload in memory
6. Supported formats: JPEG, PNG, WebP, PDF, TIFF — reject all others
7. Bounding box coordinates: use normalized 0-1 range for resolution independence
8. Error handling: corrupted files must return 422 with clear error message

---

## Standard Operating Procedures

### Image Optimization Tests
```bash
npx vitest run src/utils/imageOptimization.test.ts
```

### Upload Stress Test
```bash
npm run test:upload:stress
```

### OCR Accuracy Test
```bash
npm run test:ocr:accuracy
```

---

## Aegis V4.1 Governance (All Departments)

1. **Single Purpose File Law:** Every source file must have a single responsibility and remain under 350 lines.
2. **Canonical 5-Way File Standard:** View (`.view.tsx`), Logic (`.logic.ts`), Styles (`.styles.ts`), Data (`.data.ts`), Config (`.config.ts`).
3. **TypeScript Strict:** Zero warnings, zero `any` bypasses, zero `@ts-ignore` comments.
4. **Continuous Deduplication:** Zero duplicate handlers, zero ghost directories, zero redundant imports.
5. **Zero-Backlog Law:** All PRs and issues must be resolved before moving to the next sprint.
6. **Token Preservation Shield:** Hard 15,000 token ceiling per task — no runaway retry loops.
7. **Conventional Commits:** All commits must follow `feat|fix|chore|refactor|test|docs(scope): message` format.
