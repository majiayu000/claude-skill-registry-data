---
name: obsi-concept-distiller
description: Standards for extracting atomic concepts using AI and ensuring bidirectional linking.
---

# Concept Distiller Standards

## Purpose
To enable **"Precision Learning"** by breaking down massive notes into atomic, reusable concepts.

## Extraction Standards
1.  **Atomicity**: One note = One Concept. Do not mix unrelated topics.
2.  **Reusability**: Is this concept useful in a different context/project? If yes, extract it.
3.  **De-duplication**: Check `find_by_name` before creating. If exists, Append/Improve instead of creating duplicates.

## Linking Policy
- **Bidirectional**: The Source must link to Concept (`[[Concept]]`), and Concept must link to Source (`Source: [[Source]]`).
- **Contextual Replacement**: Replace the plain text keyword in the source file with the Wikilink.
