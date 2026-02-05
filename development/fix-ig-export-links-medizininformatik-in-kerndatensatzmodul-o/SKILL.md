---
name: fix-ig-export-links
description: Fix broken Simplifier resolve links in downloaded MII Onkologie Implementation Guide exports. Use when downloading an IG from Simplifier and links are broken, preparing an IG export for offline use, or making links work both locally and on the official MII page. Handles MII Onko profiles/ValueSets/CodeSystems, FHIR R4 core links, MII dependency modules, German base profiles, and artifacts/package/ paths.
---

# Fix IG Export Links

Fix broken `/resolve?` links in Simplifier IG exports to work offline and on official MII pages.

## Link Categories and Targets

| Category | Source Pattern | Target |
|----------|---------------|--------|
| **MII Onko Canonical** | `/resolve?&scope=...onkologie...&canonical=https://...modul-onko/...` | `https://simplifier.net/resolve?canonical=...&fhirVersion=R4` |
| **FHIR R4 Base** (Basis column) | `/resolve?&scope=...&canonical=http://hl7.org/fhir/StructureDefinition/...` | `https://hl7.org/fhir/R4/....html` |
| **FHIR R4 Core** (filepath) | `simplifier.net/resolve?...hl7.fhir.r4.core...filepath=...` | `https://hl7.org/fhir/R4/...` |
| **HL7 Terminology (THO)** | `simplifier.net/resolve?...hl7.terminology.r4...` | `https://terminology.hl7.org/...` |
| **German base profiles** | `simplifier.net/resolve?...de.basisprofil.r4...` | `https://simplifier.net/packages/de.basisprofil.r4/.../files/...` |
| **de.fhir.medication** | `simplifier.net/resolve?...de.fhir.medication...` | `https://simplifier.net/packages/de.fhir.medication/.../files/...` |
| **MII Base Module** | `simplifier.net/resolve?...kerndatensatz.base...` | `https://simplifier.net/packages/.../files/...` |
| **MII Medikation** | `simplifier.net/resolve?...kerndatensatz.medikation...` | `https://simplifier.net/packages/.../files/...` |
| **MII MolGen** | `simplifier.net/resolve?...kerndatensatz.molgen...` | `https://simplifier.net/packages/.../files/...` |
| **MII Core Canonical** | `/resolve?...canonical=https://...core/modul-diagnose/...` | `https://simplifier.net/resolve?canonical=...&fhirVersion=R4` |
| **Internal Profiles** | `artifacts/package/StructureDefinition-mii-pr-onko-*.json` | Local HTML page |
| **Internal ValueSets** | `artifacts/package/ValueSet-mii-vs-onko-*.json` | `https://simplifier.net/resolve?canonical=...&fhirVersion=R4` |
| **Internal CodeSystems** | `artifacts/package/CodeSystem-mii-cs-onko-*.json` | `https://simplifier.net/resolve?canonical=...&fhirVersion=R4` |
| **Internal Extensions** | `artifacts/package/StructureDefinition-mii-ex-onko-*.json` | `https://simplifier.net/resolve?canonical=...&fhirVersion=R4` |
| **Old guide URLs** | `mii-ig-modul-onkologie-2024-de` | Updated guide URL |
| **.page.md broken link** | `*.page.md` | Correct HTML page |

## Procedure

1. Download and extract the IG ZIP from Simplifier to a working directory
2. Navigate to the extracted directory containing HTML files
3. Run the fix script:
   ```bash
   cd /path/to/extracted-ig
   bash /path/to/fix-links.sh
   ```
4. Verify remaining resolve links (should only be intentional Simplifier links):
   ```bash
   grep -c "resolve?" *.html | grep -v ":0$"
   ```

## Script Location

The fix script is located at: `.claude/skills/fix-ig-export-links/scripts/fix-links.sh`

## Technical Notes

### HTML Encoding Variants
The script handles two encoding patterns:
- **Single-quoted href with `&`**: Used in FQL canonical box tables (`href='...'`)
- **Double-quoted href with `&amp;`**: Used elsewhere (`href="..."`)

### Link Pattern Types
- **`?canonical=`**: Links to profile canonical URLs (should resolve via Simplifier)
- **`?filepath=`**: Links to package files (should resolve to official spec URLs or Simplifier packages)

### ValueSet and CodeSystem Handling
Unlike simpler IGs, Onkologie defines ~97 ValueSets and ~43 CodeSystems that are referenced in binding tables. These are transformed to Simplifier resolve links with the canonical URL pattern:
```
https://simplifier.net/resolve?canonical=https://www.medizininformatik-initiative.de/fhir/ext/modul-onko/ValueSet/{id}&fhirVersion=R4
```

### Expected Remaining Links
After running the script, these Simplifier resolve links are intentional:
- MII Onko profile/ValueSet/CodeSystem canonical URLs -> `https://simplifier.net/resolve?canonical=...&fhirVersion=R4`
- CapabilityStatement canonical -> remains as Simplifier resolve

## Example Usage

```bash
# Extract the downloaded IG
unzip "MII-IG-Onkologie-DE-v2026@current.zip" -d ig-export

# Run the fix script
cd ig-export
bash ~/.claude/skills/fix-ig-export-links/scripts/fix-links.sh

# Verify - count should show only intentional Simplifier links
grep -o "simplifier.net/resolve" *.html | wc -l

# Check a specific high-traffic page
grep "resolve?" MIIIGModulOnkologie-TechnischeImplementierung-FHIR-Profile-Diagnose-Diagnose-Condition.html | head -5
```

## Package Information

- **Package Name**: `de.medizininformatikinitiative.kerndatensatz.onkologie`
- **Current Version**: `2026.0.0`
- **Canonical Base**: `https://www.medizininformatik-initiative.de/fhir/ext/modul-onko`
- **Guide Name**: `mii-ig-modul-onkologie-v2026-de`

## Dependencies Handled

| Package | Version | Link Target |
|---------|---------|-------------|
| hl7.fhir.r4.core | 4.0.1 | hl7.org/fhir/R4/ |
| hl7.terminology.r4 | 7.0.0 | terminology.hl7.org/ |
| de.basisprofil.r4 | 1.5.4 | Simplifier packages |
| de.fhir.medication | 1.0.3 | Simplifier packages |
| de.medizininformatikinitiative.kerndatensatz.base | 2026.0.0 | Simplifier packages |
| de.medizininformatikinitiative.kerndatensatz.medikation | 2026.0.0 | Simplifier packages |
| de.medizininformatikinitiative.kerndatensatz.molgen | 2026.0.4 | Simplifier packages |
