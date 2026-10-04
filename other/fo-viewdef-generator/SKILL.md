---
name: fo-viewdef-generator
description: Generates a Functional Design (FO) document in Markdown format based on a specific ViewDefinition-*.json file (supporting single or multiple profiles/unions) and template.md. This is distinct from ZIB-only FO generation.
---

# FO ViewDefinition Generator (fo-viewdef-generator)

This skill automates the creation of Functional Design (FO) documents *specifically* derived from `ViewDefinition-*.json` files located in `input/images/`, following the project's standardized `template.md`. 

This is distinct from other FO generators because it maps the exact technical queries, SQL-on-FHIR pathways, and union configurations declared in the ViewDefinition directly onto UI elements and mock data tables.

## Workflow

### 1. Research & Parsing Phase
- **Locate Target ViewDefinition**: Find the target `input/images/ViewDefinition-<Domain>.json` file based on the user's request.
- **Analyze ViewDefinition Structure**:
  - Check if the ViewDefinition is a **single-source query** (contains a top-level `select` list with a `forEach` filter) or a **union query** (contains a `select[].unionAll` array).
- **Identify All Profiles & Resources**:
  - Extract the top-level `"profile"` field if it exists (e.g. `http://nictiz.nl/fhir/StructureDefinition/zib-Mobility`).
  - Search for profile references embedded inside filter expressions or paths (e.g., `meta.profile='...'` inside `forEach` or `where` statements).
  - Identify the primary resource types involved (e.g., `Observation`, `Consent`, `Encounter`, `Appointment`).
- **Resolve Corresponding ZIBs**:
  - Map each profile URI to its official Dutch Zorginformatiebouwsteen (ZIB) name (e.g., `zib-TreatmentDirective` -> Behandelaanwijzing, `gp-LaboratoryResult` -> Huisarts Labuitslag, `zib-Mobility` -> Mobiliteit).
  - Look up the ZIB descriptions, versions, and standard definitions on [zibs.nl](https://zibs.nl/wiki/ZIB_Hoofdpagina) (defaulting to the 2017 publication unless specified otherwise).

### 2. Strategy & Alignment Phase
- **Column Analysis**:
  - Extract the list of columns (`column[].name`) and their mappings to ZIB elements (`tag[name="Zib element"].value`).
  - **Union Handling**: If `unionAll` is used, align the columns from different sub-queries. Identify if a column maps to different paths or different ZIB elements depending on the underlying resource (e.g., "Begin" mapped to `period.start` for `Encounter` vs `start` for `Appointment`).
- **Formulate Functional Intent**:
  - Combine the distinct ZIB concepts into a cohesive user-facing description under "Wat zijn [ZIBs]?" and "Functionele wens".

### 3. Execution Phase (Generation)
Generate the FO document in **Dutch**, adhering strictly to the layout of `template.md` and the style of `example.md`:

- **Header Metadata**:
  - Set `Titel` to the `title` of the ViewDefinition.
  - Provide documentation and work item links/placeholders.
- **Aanleiding & context**:
  - Detail why these medical details are being shown in the Zorgviewer.
  - Insert the formal ZIB concept descriptions for **all** mapped ZIBs.
- **Gegevensbronnen**:
  - If multiple profiles are involved, list **each** ZIB, standard version, and profile in a clean tabular format.
  - Link the FHIR Resource/profile to its exact page in the RIVO-Noord IG: `https://build.fhir.org/ig/RIVO-Noord/zorgviewer-ig/StructureDefinition-<ProfileLastPart>.html`.
- **Schermontwerp**:
  - Set `Naam gegevensscherm` & `Naam menu item` to the ViewDefinition `title`.
  - Link a fitting Material Icon from [Google Fonts](https://fonts.google.com/icons).
  - In `Gegevensherkomst`, link to the IG page(s) using the `#kolomdefinities` anchor.
  - **Schermontwerp Table**: Create a mock data table where the headers **exactly** match the column names defined in the ViewDefinition JSON in their exact original order.
  - **Mock Data Rows**: Populate the table with 3 realistic Dutch example rows. **Crucial**: Include rows that represent different profile sources in the case of a union (e.g., one row for `Encounter` and one for `Appointment`).
- **Schermgedrag**:
  - Detail standard and non-standard sorting, filtering, and exceptions. 
  - Document specific filter rules derived from the JSON filter paths (e.g., filtering out certain statuses).
- **Tijdlijn**:
  - Detail card layout and expansion behavior. If multiple resources are used, describe which resources appear on the timeline (e.g., Encounter vs. Appointment).

### 4. Quality Rules
- **Dutch Language**: Write everything exclusively in Dutch.
- **Header Alignment**: Ensure columns match the ViewDefinition JSON's `column[].name` perfectly.
- **Multi-source Traceability**: Clearly distinguish which field/value originates from which resource/profile when explaining behavior.