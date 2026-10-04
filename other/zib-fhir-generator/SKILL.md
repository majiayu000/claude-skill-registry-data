---
name: zib-fhir-generator
description: Generates ViewDefinition, StructureDefinition (must-support), and markdown intro files from a ZIB FHIR profile URL or canonical (e.g. zib-Alert). Use this when asked to create technical artifacts for Zorginformatiebouwstenen (ZIBs) in FHIR.
---

# ZIB FHIR Generator

## Overview

This skill automates the creation of Zorgviewer-specific FHIR artifacts based on Nictiz ZIB profiles. It ensures consistency across ViewDefinitions, StructureDefinitions with Must-Support flags, and documentation intros.

## Constraints

* Only search for definitions on zibs.nl and simplifier.net.
* Use FHIR STU3 as the base version for all generated artifacts and FHIR R4 when a STU3 version is not available.
* Generate only the templated files for the specified ZIB, without creating or changing additional includes or unrelated artifacts.
* Use only the codes defined in the ZIB profiles for mapping.
* Ensure that query code parameters are included in the ViewDefinition's `where` clause for accurate data retrieval.
* Retrieve example instances from simplifier.net and save them in `input/examples/<ZibName>-Nictiz.json` for reference.

## Workflow

When given a ZIB FHIR profile (e.g., `http://nictiz.nl/fhir/StructureDefinition/zib-Alert`):

1.  **Identify the ZIB and Base Resource**: Determine the ZIB name (e.g., Alert) and the underlying FHIR resource type (e.g., Flag).
2.  **Map ZIB Elements to FHIR Paths**: Identify the key elements in the ZIB and their corresponding FHIR paths in the Nictiz profile.
3.  **Generate Artifacts**:
    *   **StructureDefinition**: Create a JSON file that inherits from the Nictiz profile and adds `mustSupport: true` to the key ZIB elements.
    *   **ViewDefinition**: Create a JSON file using the SQL-on-FHIR `ViewDefinition` resource, mapping FHIR paths to ZIB elements for the Zorgviewer UI.
    *   **Markdown Intro**: Create a markdown file following the standard template with links to the ZIB wiki and the ViewDefinition.

## Artifact Guidelines

Refer to [references/templates.md](references/templates.md) for the exact structure and placeholders for each file.

### Mapping Principles

*   **StructureDefinition**: Use `derivation: constraint` and set `mustSupport: true` only for elements that are essential for the Zorgviewer display.
*   **ViewDefinition**: 
    *   Always include the "Bron" (Source) column as the first column.
    *   Use `iif(exists(...), ...)` or `|` (choice) for flexible path mapping (e.g., `code.text | code.coding[0].display`).
    *   Include ZIB element names in the `tag` field for traceability.

### File Naming Convention

*   `input/profiles/StructureDefinition-<ZibName>.json`
*   `input/images/ViewDefinition-<ZibName>.json`
*   `input/intro-notes/StructureDefinition-<ZibName>-intro.md`

Where `<ZibName>` is the name of the Zorginformatiebouwsteen (e.g., Alert, Mobiliteit, Probleem).

## Example: zib-Alert

**User Request**: "Maak de bestanden voor zib-Alert"

**Output Files**:
*   `input/profiles/StructureDefinition-Alert.json`
*   `input/images/ViewDefinition-Alert.json`
*   `input/intro-notes/StructureDefinition-Alert-intro.md`
