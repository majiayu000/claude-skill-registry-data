---
name: sf-metadata-parser
description: "Use this skill whenever the user wants to parse, analyze, document, or export SAP SuccessFactors OData metadata ($metadata XML). Triggers include: any mention of 'metadata', '$metadata', 'OData entities', 'entity fields', 'SF metadata', 'SuccessFactors schema', 'data dictionary', or requests to understand, compare, or export the structure of SF entities. Also use when generating field-level documentation, creating data mapping sheets, building configuration workbooks, producing entity relationship diagrams, comparing metadata between instances, or converting raw $metadata XML into human-readable formats (Excel, Word, CSV, HTML). If the user uploads a $metadata XML file or pastes OData entity definitions and wants them parsed or documented, use this skill. Do NOT use for runtime OData queries, live API calls, or non-metadata SF tasks."
license: MIT
---

# SAP SuccessFactors OData Metadata Parser

## Overview

This skill parses SAP SuccessFactors OData `$metadata` XML documents and transforms them into user-friendly, organizational-ready outputs. The raw `$metadata` is a massive XML schema document (often 50,000+ lines) containing entity definitions, field types, navigation properties, associations, and constraints — virtually unreadable for business users, HR admins, and even many consultants. This tool makes it accessible.

## Why This Tool Exists

In every SAP SuccessFactors implementation, consultants and admins face these recurring pain points:

1. **Field Discovery** — "What fields exist on EmpJob? Which are required? What's the max length?"
2. **Data Mapping** — "Map SF fields to our payroll system — we need entity, field, type, and constraints in Excel."
3. **Configuration Documentation** — "Generate a data dictionary for our instance for audit/compliance."
4. **Instance Comparison** — "Did someone add custom fields in production that aren't in our test environment?"
5. **Integration Planning** — "Which navigation properties connect User to EmpEmployment? What's the cardinality?"

Raw `$metadata` XML answers all of these — but no human should have to read 50K lines of XML to find them.

---

## Input Sources

The tool accepts metadata from multiple sources:

### 1. Uploaded $metadata XML File
```
User uploads: metadata.xml (or .edmx)
Location: /mnt/user-data/uploads/metadata.xml
```

### 2. Pasted XML Content
User pastes raw XML into the chat. Extract and save to a working file before processing.

### 3. Live API Fetch (if SF MCP tools are available)
Use the `sf-mcp:get_configuration` tool to fetch entity metadata directly from a live instance:
```
sf-mcp:get_configuration(instance, entity, data_center, environment, auth_user_id, auth_password)
```

### 4. Multiple Files for Comparison
User uploads two metadata files (e.g., `metadata_dev.xml` and `metadata_prod.xml`) for cross-instance comparison.

---

## Core Parsing Logic

### Step 1: Parse the $metadata XML

Use Python's `lxml` or `xml.etree.ElementTree` with proper OData namespace handling.

```python
import xml.etree.ElementTree as ET

# OData EDMX namespaces (SuccessFactors uses EDMX + CSDL)
NAMESPACES = {
    'edmx': 'http://schemas.microsoft.com/ado/2007/06/edmx',
    'edm': 'http://schemas.microsoft.com/ado/2008/09/edm',
    'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata',
    'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices',
    # SF may also use newer namespace versions:
    'edm2009': 'http://schemas.microsoft.com/ado/2009/11/edm',
}

def parse_metadata(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Auto-detect namespace version from root element
    ns = detect_namespaces(root)

    entities = {}
    associations = {}
    entity_sets = {}

    # Parse EntityTypes
    for schema in root.iter(f'{{{ns["edm"]}}}Schema'):
        namespace = schema.get('Namespace', '')

        for entity_type in schema.findall(f'{ns_prefix}EntityType', ns):
            name = entity_type.get('Name')
            base_type = entity_type.get('BaseType', '')
            entities[name] = {
                'name': name,
                'namespace': namespace,
                'base_type': base_type,
                'keys': extract_keys(entity_type, ns),
                'properties': extract_properties(entity_type, ns),
                'navigation_properties': extract_nav_properties(entity_type, ns),
            }

        # Parse Associations
        for assoc in schema.findall(f'{ns_prefix}Association', ns):
            associations[assoc.get('Name')] = extract_association(assoc, ns)

        # Parse EntitySets (EntityContainer)
        for container in schema.findall(f'{ns_prefix}EntityContainer', ns):
            for es in container.findall(f'{ns_prefix}EntitySet', ns):
                entity_sets[es.get('Name')] = es.get('EntityType')

    return entities, associations, entity_sets
```

### Step 2: Extract Field-Level Details

For each entity, extract these critical attributes per field:

| Attribute | Source in XML | Business Meaning |
|-----------|--------------|-----------------|
| `Name` | `Property/@Name` | Technical field name |
| `Type` | `Property/@Type` | Data type (Edm.String, Edm.DateTime, etc.) |
| `Nullable` | `Property/@Nullable` | Is the field required? (false = required) |
| `MaxLength` | `Property/@MaxLength` | Character limit for strings |
| `Label` | `sap:label` attribute | Human-readable field label |
| `Creatable` | `sap:creatable` | Can be set on insert? |
| `Updatable` | `sap:updatable` | Can be modified on update? |
| `Filterable` | `sap:filterable` | Can be used in $filter? |
| `Sortable` | `sap:sortable` | Can be used in $orderby? |
| `Unicode` | `Property/@Unicode` | Unicode support flag |
| `DefaultValue` | `Property/@DefaultValue` | Default value if any |

**SAP-specific attributes** (critical for SF):
```python
SAP_ATTRIBUTES = [
    'sap:label',           # Display label
    'sap:creatable',       # Insert permission
    'sap:updatable',       # Update permission
    'sap:filterable',      # Filter capability
    'sap:sortable',        # Sort capability
    'sap:required-in-filter',  # Must be in $filter
    'sap:display-format',  # Date/time display format
    'sap:field-control',   # Dynamic field control
    'sap:visible',         # UI visibility
    'sap:semantics',       # Semantic meaning (e.g., email, tel)
]
```

### Step 3: Extract Navigation Properties & Relationships

```python
def extract_nav_properties(entity_type, ns):
    nav_props = []
    for nav in entity_type.findall(f'.//NavigationProperty', ns):
        nav_props.append({
            'name': nav.get('Name'),
            'relationship': nav.get('Relationship'),
            'from_role': nav.get('FromRole'),
            'to_role': nav.get('ToRole'),
            'cardinality': determine_cardinality(nav, associations)  # 1:1, 1:N, N:1
        })
    return nav_props
```

---

## Output Formats

### Output 1: Excel Data Dictionary (Primary Deliverable)

**This is the most commonly requested output.** Generate a multi-sheet Excel workbook.

#### Sheet Structure:

| Sheet Name | Contents |
|-----------|----------|
| **Summary** | Entity list with field count, key fields, nav property count |
| **All Fields** | Master flat list of every field across all entities |
| **{EntityName}** | One sheet per entity with full field details (create for top entities or all) |
| **Navigation Properties** | All relationships between entities |
| **Associations** | Cardinality and role mappings |
| **Enums / ComplexTypes** | Picklist values and complex type definitions |
| **Comparison** | (If two files provided) Side-by-side diff |

#### Excel Formatting Standards:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Color scheme (SAP-inspired)
HEADER_FILL = PatternFill('solid', fgColor='1B3A5C')      # Dark SAP blue
HEADER_FONT = Font(name='Arial', bold=True, color='FFFFFF', size=11)
SUBHEADER_FILL = PatternFill('solid', fgColor='4A90D9')    # Medium blue
KEY_FIELD_FILL = PatternFill('solid', fgColor='FFF3CD')    # Yellow highlight for key fields
REQUIRED_FILL = PatternFill('solid', fgColor='F8D7DA')     # Light red for required fields
READONLY_FILL = PatternFill('solid', fgColor='E2E3E5')     # Gray for read-only fields
NAV_PROP_FILL = PatternFill('solid', fgColor='D4EDDA')     # Green for navigation properties
CUSTOM_FIELD_FILL = PatternFill('solid', fgColor='D6EAF8') # Light blue for custom (cust_) fields
ALT_ROW_FILL = PatternFill('solid', fgColor='F8F9FA')      # Alternating row color

THIN_BORDER = Border(
    left=Side(style='thin', color='CCCCCC'),
    right=Side(style='thin', color='CCCCCC'),
    top=Side(style='thin', color='CCCCCC'),
    bottom=Side(style='thin', color='CCCCCC'),
)
```

#### Column Layout for Entity Field Sheets:

```
A: Field Name (technical)
B: Label (sap:label — human-readable)
C: Data Type (simplified: String, Integer, DateTime, Boolean, Decimal, etc.)
D: Max Length
E: Required (Yes/No — derived from Nullable=false)
F: Key Field (Yes/No)
G: Creatable (Yes/No)
H: Updatable (Yes/No)
I: Filterable (Yes/No)
J: Sortable (Yes/No)
K: Default Value
L: Description / Notes
M: Custom Field (Yes/No — detected by 'cust_' prefix)
```

#### Summary Sheet Layout:

```
A: Entity Name
B: Entity Label (if available)
C: Total Fields
D: Key Fields (count)
E: Required Fields (count)
F: Custom Fields (count — cust_ prefix)
G: Navigation Properties (count)
H: Creatable Fields (count)
I: Updatable Fields (count)
J: Category (Employee, Talent, Foundation, Platform, MDF, Custom)
```

**Auto-categorization logic:**
```python
def categorize_entity(name):
    name_lower = name.lower()
    if name_lower.startswith('cust_'):
        return 'Custom MDF'
    elif any(name_lower.startswith(p) for p in ['emp', 'perhire', 'perpersonal', 'peremail', 'perphone']):
        return 'Employee Central'
    elif any(name_lower.startswith(p) for p in ['goal', 'form', 'competency']):
        return 'Talent / Performance'
    elif any(name_lower.startswith(p) for p in ['jobrecreq', 'jobreq', 'candidate', 'jobapp']):
        return 'Recruiting'
    elif any(name_lower.startswith(p) for p in ['fo_', 'picklistoption', 'picklistlabel']):
        return 'Foundation Objects'
    elif any(name_lower.startswith(p) for p in ['user', 'dynamicgroup', 'rbp']):
        return 'Platform / Security'
    elif any(name_lower.startswith(p) for p in ['position', 'budget']):
        return 'Position Management'
    elif any(name_lower.startswith(p) for p in ['timeaccount', 'employeetime', 'timemanagement']):
        return 'Time Management'
    else:
        return 'Other'
```

#### Applying Formatting:

```python
def format_entity_sheet(ws, data_rows):
    # Freeze top row
    ws.freeze_panes = 'A2'

    # Auto-filter on headers
    ws.auto_filter.ref = ws.dimensions

    # Column widths (optimized for readability)
    COLUMN_WIDTHS = {
        'A': 35,  # Field Name
        'B': 35,  # Label
        'C': 18,  # Data Type
        'D': 12,  # Max Length
        'E': 10,  # Required
        'F': 10,  # Key Field
        'G': 12,  # Creatable
        'H': 12,  # Updatable
        'I': 12,  # Filterable
        'J': 12,  # Sortable
        'K': 18,  # Default Value
        'L': 45,  # Description
        'M': 14,  # Custom Field
    }
    for col, width in COLUMN_WIDTHS.items():
        ws.column_dimensions[col].width = width

    # Conditional formatting
    for row_idx, row_data in enumerate(data_rows, start=2):
        # Highlight key fields
        if row_data.get('is_key'):
            for col in range(1, 14):
                ws.cell(row=row_idx, column=col).fill = KEY_FIELD_FILL
        # Highlight required fields
        elif row_data.get('required'):
            ws.cell(row=row_idx, column=5).fill = REQUIRED_FILL
        # Highlight custom fields
        elif row_data.get('is_custom'):
            ws.cell(row=row_idx, column=1).fill = CUSTOM_FIELD_FILL
        # Alternating rows
        elif row_idx % 2 == 0:
            for col in range(1, 14):
                ws.cell(row=row_idx, column=col).fill = ALT_ROW_FILL
```

### Output 2: Word Document (Data Dictionary Report)

For formal documentation deliverables. Use the `docx` skill for creation.

**Document Structure:**
1. **Cover Page** — Title, instance name, generation date, author
2. **Table of Contents**
3. **Executive Summary** — Total entities, fields, custom objects count
4. **Entity Catalog** — Grouped by category (EC, Talent, Recruiting, etc.)
5. **Entity Detail Pages** — One section per entity with field table
6. **Navigation Property Map** — Entity relationship documentation
7. **Appendix: Data Type Reference** — Edm type to business type mapping
8. **Appendix: SAP Attribute Legend** — What each sap:* attribute means

### Output 3: CSV / Flat File Export

For integration with other tools, data governance platforms, or quick lookups:

```python
import csv

def export_flat_csv(entities, output_path):
    headers = [
        'Entity', 'Field_Name', 'Label', 'Data_Type', 'Max_Length',
        'Required', 'Key_Field', 'Creatable', 'Updatable', 'Filterable',
        'Sortable', 'Default_Value', 'Custom_Field', 'Category'
    ]
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:  # BOM for Excel compat
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for entity_name, entity in entities.items():
            category = categorize_entity(entity_name)
            for prop in entity['properties']:
                writer.writerow({
                    'Entity': entity_name,
                    'Field_Name': prop['name'],
                    'Label': prop.get('label', ''),
                    'Data_Type': simplify_type(prop['type']),
                    'Max_Length': prop.get('max_length', ''),
                    'Required': 'Yes' if not prop.get('nullable', True) else 'No',
                    'Key_Field': 'Yes' if prop['name'] in entity['keys'] else 'No',
                    'Creatable': prop.get('creatable', ''),
                    'Updatable': prop.get('updatable', ''),
                    'Filterable': prop.get('filterable', ''),
                    'Sortable': prop.get('sortable', ''),
                    'Default_Value': prop.get('default_value', ''),
                    'Custom_Field': 'Yes' if prop['name'].startswith('cust_') else 'No',
                    'Category': category,
                })
```

### Output 4: HTML Interactive Data Dictionary

Generate a single-file HTML with search, filter, and entity navigation.

```html
<!-- Features to include: -->
<!-- 1. Sidebar with entity list (collapsible by category) -->
<!-- 2. Search bar filtering entities and fields -->
<!-- 3. Field table with sortable columns -->
<!-- 4. Color coding matching Excel scheme -->
<!-- 5. Entity relationship links (click nav property → jump to target entity) -->
<!-- 6. Export to CSV button (client-side) -->
<!-- 7. Stats dashboard at top (total entities, fields, custom fields) -->
```

### Output 5: Instance Comparison Report

When two metadata files are provided:

```python
def compare_metadata(entities_a, entities_b, label_a='Instance A', label_b='Instance B'):
    comparison = {
        'only_in_a': [],        # Entities only in first instance
        'only_in_b': [],        # Entities only in second instance
        'in_both': [],          # Entities in both
        'field_differences': {} # Per-entity field-level diffs
    }

    all_entities = set(entities_a.keys()) | set(entities_b.keys())

    for entity_name in sorted(all_entities):
        in_a = entity_name in entities_a
        in_b = entity_name in entities_b

        if in_a and not in_b:
            comparison['only_in_a'].append(entity_name)
        elif in_b and not in_a:
            comparison['only_in_b'].append(entity_name)
        else:
            comparison['in_both'].append(entity_name)
            # Compare fields
            fields_a = {p['name'] for p in entities_a[entity_name]['properties']}
            fields_b = {p['name'] for p in entities_b[entity_name]['properties']}
            only_a = fields_a - fields_b
            only_b = fields_b - fields_a
            if only_a or only_b:
                comparison['field_differences'][entity_name] = {
                    f'only_in_{label_a}': sorted(only_a),
                    f'only_in_{label_b}': sorted(only_b),
                }

    return comparison
```

---

## Data Type Mapping Reference

Always simplify OData Edm types to business-friendly names:

```python
TYPE_MAP = {
    'Edm.String': 'Text',
    'Edm.Int16': 'Integer (16-bit)',
    'Edm.Int32': 'Integer',
    'Edm.Int64': 'Long Integer',
    'Edm.Decimal': 'Decimal',
    'Edm.Double': 'Double',
    'Edm.Single': 'Float',
    'Edm.Boolean': 'Yes/No',
    'Edm.DateTime': 'Date & Time',
    'Edm.DateTimeOffset': 'Date & Time (UTC)',
    'Edm.Time': 'Time',
    'Edm.Binary': 'Binary',
    'Edm.Byte': 'Byte',
    'Edm.Guid': 'GUID',
    'Edm.SByte': 'Signed Byte',
}

def simplify_type(edm_type):
    if edm_type in TYPE_MAP:
        return TYPE_MAP[edm_type]
    # Handle complex types and enums
    if '.' in edm_type:
        return edm_type.split('.')[-1]  # Return just the type name
    return edm_type
```

---

## Common SuccessFactors Entity Groups

When generating the Summary sheet, group entities into these categories for readability:

| Category | Key Entities | Description |
|----------|-------------|-------------|
| **Employee Central** | User, EmpEmployment, EmpJob, EmpCompensation, PerPersonal, PerEmail, PerPhone, PerNationalId | Core employee data |
| **Position Management** | Position, PositionCompetencyMappingEntity, PositionMatrixRelationship | Org structure positions |
| **Recruiting** | JobRequisition, JobApplication, Candidate, JobOffer | Talent acquisition |
| **Onboarding** | ONB2Process, ONB2EquipmentActivity | New hire onboarding |
| **Performance & Goals** | FormTemplate, FormHeader, FormContent, Goal_*, CompetencyEntity | PM & Goal plans |
| **Compensation** | EmpPayCompRecurring, EmpPayCompNonRecurring, PayScaleGroup | Pay components |
| **Time Management** | EmployeeTime, TimeAccount, TimeAccountType, TimeType | Leave & attendance |
| **Learning** | LMSLearningItem, LMSAssignment, LMSCurriculum | LMS entities |
| **Foundation Objects** | FOCompany, FODepartment, FODivision, FOLocation, FOJobCode, FOCostCenter, FOPayGrade | Org building blocks |
| **Platform / Security** | RBPRole, DynamicGroup, Permission, Todo | Security & workflow |
| **MDF / Custom** | cust_* | Customer-created generic objects |

---

## Workflow Summary

### Quick Parse (Single Entity)
```
1. User asks about a specific entity (e.g., "What fields are on EmpJob?")
2. If metadata file is uploaded → Parse XML, extract that entity
3. If SF MCP tools available → Call get_configuration(entity="EmpJob")
4. Display field list in a clean table (in chat or Excel)
```

### Full Data Dictionary Generation
```
1. User uploads $metadata XML or requests full parse
2. Parse entire metadata document
3. Generate multi-sheet Excel workbook following formatting standards above
4. Save to /mnt/user-data/outputs/SF_Data_Dictionary.xlsx
5. Present to user with summary stats
```

### Instance Comparison
```
1. User uploads two metadata files
2. Parse both files independently
3. Run comparison logic
4. Generate comparison Excel with:
   - Summary sheet (counts, match %)
   - Entities only in Instance A
   - Entities only in Instance B
   - Field-level differences for shared entities
5. Color-code: Green = match, Red = only in A, Blue = only in B
```

---

## Error Handling & Edge Cases

### Namespace Detection
SF instances may use different OData/EDMX namespace versions. Always auto-detect:
```python
def detect_namespaces(root):
    tag = root.tag
    # Extract namespace from root tag
    if '{' in tag:
        edmx_ns = tag.split('}')[0].strip('{')
    # Look for Schema namespace in children
    for child in root.iter():
        if 'Schema' in child.tag:
            edm_ns = child.tag.split('}')[0].strip('{')
            break
    return {'edmx': edmx_ns, 'edm': edm_ns}
```

### Large Metadata Files
Some SF instances have 500+ entities and 10,000+ fields. Strategies:
- **Stream parse** with `iterparse` for files > 50MB
- **Limit entity sheets** — only create per-entity sheets for the top 50 most important entities; keep the flat "All Fields" sheet for everything
- **Chunk Excel writes** — write in batches to avoid memory issues

### Missing SAP Attributes
Not all instances expose `sap:label`, `sap:creatable`, etc. Gracefully default:
```python
def get_sap_attr(element, attr_name, default='N/A'):
    return element.get(f'{{http://www.sap.com/Protocols/SAPData}}{attr_name}', default)
```

### Custom Fields (cust_*)
Always flag custom fields with visual indicators. These are the fields customers added via MDF and are critical for:
- Migration planning
- Instance comparison (custom drift)
- Integration mapping

---

## Dependencies

- **Python stdlib**: `xml.etree.ElementTree` for XML parsing
- **lxml** (optional): For XPath and better namespace handling (`pip install lxml --break-system-packages`)
- **openpyxl**: For Excel generation (pre-installed)
- **pandas**: For data analysis and CSV export (pre-installed)
- **docx skill**: For Word document generation (reference `/mnt/skills/public/docx/SKILL.md`)
- **xlsx skill**: For Excel best practices (reference `/mnt/skills/public/xlsx/SKILL.md`)

---

## Best Practices

1. **Always simplify data types** — Business users don't know what `Edm.DateTimeOffset` means. Show "Date & Time (UTC)".
2. **Highlight what matters** — Key fields, required fields, and custom fields should visually pop.
3. **Include field counts** — Every summary should show total fields, required, custom, and navigations.
4. **Group by category** — Never dump 500 entities in a flat list. Always categorize.
5. **Add legends** — Every Excel output needs a legend sheet explaining colors and abbreviations.
6. **Use freeze panes** — Always freeze the header row and optionally the entity name column.
7. **Auto-filter everything** — Users will want to filter by type, required, category, etc.
8. **UTF-8 with BOM for CSV** — Ensures Excel opens CSVs correctly with special characters.
9. **Name sheets carefully** — Excel sheet names have a 31-character limit. Truncate long entity names.
10. **Test with real data** — SF metadata varies significantly between instances. Always validate parsing against the actual uploaded file structure.
