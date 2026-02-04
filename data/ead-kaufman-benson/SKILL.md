---
name: ead-kaufman-benson
description: Specialized skill for editing and refining EAD2002 finding aids for the Terrence Kaufman Papers at the Archive of Indigenous Languages of Latin America (AILLA), Lillas Benson Latin American Studies and Collections, University of Texas at Austin. Use when working with KaufmanEAD.xml, implementing staff feedback, validating against EAD2002 standards, or referencing institutional finding aid examples.
---

# EAD Finding Aid Editor - Kaufman Papers (AILLA/Benson)

This skill provides specialized guidance for creating and editing the preliminary EAD2002 finding aid for the Terrence Kaufman Papers collection at AILLA/Lillas Benson, UT Austin.

## Project Context

**Collection**: Terrence Kaufman Papers  
**Institution**: Archive of Indigenous Languages of Latin America (AILLA), Lillas Benson Latin American Studies and Collections, University of Texas at Austin  
**Status**: Pre-processed materials, preliminary finding aid in progress  
**Standard**: EAD2002  
**Primary File**: KaufmanEAD.xml

## Workflow

When working on the Kaufman finding aid:

1. **Review Current State**: Load and analyze KaufmanEAD.xml to understand the current structure
2. **Implement Feedback**: Apply staff feedback from Benson archivists systematically
3. **Validate Structure**: Check against EAD2002 schema (schema2.xsl) and institutional standards
4. **Reference Examples**: Consult institutional EAD examples in references/ for consistency
5. **Preserve Context**: Maintain AILLA-specific metadata and indigenous language documentation standards

## Key EAD2002 Elements for Archival Collections

### Critical Structural Elements

- `<ead>` - Root element
- `<eadheader>` - Header with metadata about the finding aid itself
- `<archdesc>` - Main archival description (level="collection" or "fonds")
- `<did>` - Descriptive identification (required in archdesc and component levels)
- `<dsc>` - Description of subordinate components (series, subseries, files, items)

### Common Components in <did>

- `<unittitle>` - Title of the unit
- `<unitid>` - Unique identifier
- `<unitdate>` - Date(s) of materials
- `<physdesc>` - Physical description including `<extent>`
- `<repository>` - Holding institution
- `<langmaterial>` - Language of materials (important for AILLA multilingual collections)
- `<origination>` - Creator information

### Important Descriptive Elements

- `<bioghist>` - Biographical/historical note
- `<scopecontent>` - Scope and content note
- `<arrangement>` - Organization of materials
- `<accessrestrict>` - Access restrictions
- `<userestrict>` - Use restrictions
- `<prefercite>` - Preferred citation
- `<controlaccess>` - Controlled access terms (subjects, names, etc.)

### Component Structure (<c> or <c01>-<c12>)

For series/subseries/file organization:
- Use `<c>` elements or numbered `<c01>`, `<c02>`, etc.
- Each component has `level` attribute: "series", "subseries", "file", "item"
- Each component typically contains its own `<did>` and may have additional descriptive elements

## AILLA-Specific Considerations

- **Indigenous Language Materials**: Ensure proper language codes in `<langmaterial>`
- **Cultural Sensitivity**: Review access restrictions for culturally sensitive materials
- **Documentation Standards**: Follow AILLA metadata standards for linguistic materials
- **Researcher Context**: Include sufficient detail for linguists and indigenous language researchers

## Reference Files

The skill includes institutional EAD examples demonstrating Benson standards:

- **references/carlosmorton.xml** - Carlos Morton Papers EAD example
- **references/ailla.xml** - AILLA collection EAD example  
- **references/pirapirana.xml** - Pirapirana collection EAD example
- **references/ead2002-elements.md** - Quick reference for EAD2002 element usage

Consult these files when questions arise about:
- Proper element nesting and hierarchy
- Institutional description conventions
- Container notation standards
- Subject heading formatting

## Validation

Use schema2.xsl to validate the finding aid structure. Common validation steps:

1. Check XML well-formedness
2. Validate against EAD2002 DTD/schema
3. Verify required elements are present
4. Ensure proper nesting and hierarchy
5. Check controlled vocabulary terms

## Best Practices for This Project

1. **Consistency**: Match formatting and description style from reference EADs
2. **Completeness**: Ensure all required EAD2002 elements are present
3. **Clarity**: Write descriptions for researchers unfamiliar with the collection
4. **Accuracy**: Verify dates, extent, and other factual information
5. **Standards Compliance**: Follow both EAD2002 and Benson institutional guidelines
