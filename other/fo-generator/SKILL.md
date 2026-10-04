---
name: fo-generator
description: Generates a Functional Design (FO) document from a ZIB FHIR profile. Use this when asked to create or update an FO based on technical FHIR specifications for the Zorgviewer project.
---

# FO Generator

This skill automates the creation of Functional Design (FO) documents based on ZIB FHIR profiles, following the project's standardized template.

### Constraints
- Laat zibs.nl en simplifier gebruiken voor definities.
- Gebruik Zibs 2017 STU3 of als STU3 niet bestaat dan zibs 2020 R4.
- Laat alleen de templated files maken.
- De kolommen in het schermontwerp in het FO document moet precies overeenkomen met de kolommen en volgorde in de UI Wireframe.
- Gebruik bij Gegevensherkomst link naar de IG de '#kolomdefinities' variant.

## Workflow

### 1. Research phase
- **Fetch FHIR Profile**: Use `web_fetch` to read the FHIR profile (e.g., from the [RIVO-Noord IG](https://build.fhir.org/ig/RIVO-Noord/zorgviewer-ig/artifacts.html)).
- **Identify ZIB**: Find which ZIB (Zorginformatiebouwsteen) the profile maps to. This is usually in the "Mappings" section or the description.
- **Get ZIB Details**: Search for the ZIB definition on [zibs.nl](https://zibs.nl/wiki/ZIB_Hoofdpagina) to get the "Concept" description and version.

### 2. Strategy phase
- Map FHIR elements to user-facing labels (e.g., `code` -> `Stof`, `clinicalStatus` -> `Status`).
- Identify which elements are critical for the "Tijdlijn" (Timeline) card summary.

### 3. Execution phase (Generation)
- Use the provided [template.md](references/template.md) as a structure.
- Follow the style and level of detail in [example.md](references/example.md).
- **Sections to populate**:
    - **Header Table**: Versie, Documentatie (links), Work items (placeholder).
    - **Algemeen**: "Wat zijn [ZIB Naam]?" using the ZIB concept description.
    - **Functionele wens**: A concise user story: "Als zorgverlener wil ik [concept] van een patiënt kunnen raadplegen...".
    - **Gegevensbronnen**: Links to the specific ZIB and the FHIR profile.
    - **Schermontwerp**:
        - **Icoon**: Search for a relevant icon on [Google Fonts Icons](https://fonts.google.com/icons).
        - **Gegevensherkomst**: List ZIB elements used in the UI.
        - **Table**: Create a mockup table with realistic example data based on the FHIR profile.
    - **Tijdlijn**:
        - Propose a card design showing the most important 2-3 fields.
    - **Usecases/Testcases**: Draft standard CRUD/View use cases and a test patient setup table.

## Guidelines
- **Language**: Always write in **Dutch**, as per project conventions.
- **Consistency**: Ensure terminology matches the ZIB and the IG.
- **Completeness**: Include all sections from the template, even if some are marked "n.v.t." (not applicable).
- **Links**: Ensure all links to the IG and ZIBs are functional.

## References
- [Template](references/template.md) - The base structure for the FO.
- [Example](references/example.md) - A completed FO for AllergyIntolerance for reference.
