---
name: create-test-lane
description: This skill should be used when creating new test lanes for the XML test data generator. A test lane consists of an XSD schema file paired with a meta.yaml configuration file. This skill guides the process of creating both files with proper semantic type mappings, distribution settings, and field overrides. Use when users request new test lanes, want to generate test data configurations, or need help setting up XSD + meta.yaml pairs for the testgen CLI tool.
---

# Create Test Lane

## Overview

This skill creates test lanes for the ceremony-field-catalog test data generator. Each test lane is a paired XSD schema + meta.yaml configuration that defines how to generate realistic test XML data for a specific business context.

## Workflow

### Step 1: Gather Requirements

Collect the following information:

1. **Context details**: What business domain/context is this for? (e.g., loans, deposits, payments)
2. **Data structure**: What elements and hierarchy should the XML have?
3. **Required metadata**: What metadata keys identify this data type?
4. **Data realism needs**: Which fields need realistic data (names, addresses, SSNs, etc.)?

### Step 2: Create the XSD Schema

Create the XSD file at `sdks/python/test_lanes/<context>/<lane_name>.xsd`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="Root">
        <xs:complexType>
            <xs:sequence>
                <!-- Define elements here -->
                <xs:element name="FieldName" type="xs:string"/>
                <xs:element name="Amount" type="xs:decimal"/>
                <xs:element name="OptionalField" type="xs:string" minOccurs="0"/>
                <xs:element name="RepeatingItem" maxOccurs="unbounded">
                    <!-- Nested structure -->
                </xs:element>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>
```

Key XSD patterns:
- `minOccurs="0"` for optional elements
- `maxOccurs="unbounded"` for repeating elements
- `nillable="true"` for elements that can be nil
- `<xs:restriction>` with `<xs:enumeration>` for fixed value lists

**Important: Optional enum elements must be nillable**

When an element uses an enumeration type AND is optional (`minOccurs="0"`), you MUST also add `nillable="true"`. This is because the generator's `emptyRate` setting can produce empty values, but empty strings are not valid enum values. Making the element nillable allows it to be represented as `xsi:nil="true"` instead of an empty string.

```xml
<!-- WRONG: Will fail validation if emptyRate produces empty value -->
<xs:element name="Status" type="StatusEnum" minOccurs="0"/>

<!-- CORRECT: Can be nil when empty -->
<xs:element name="Status" type="StatusEnum" minOccurs="0" nillable="true"/>
```

This applies to all optional elements with enumeration types (Gender, Status, Type, Category, etc.).

### Step 3: Generate or Create the Meta File

**Option A: Use init-meta command** (for existing XSD):
```bash
cd sdks/python
python -m testgen.cli init-meta --xsd test_lanes/<context>/<lane>.xsd --context <context_id>
```

**Option B: Create manually** at `sdks/python/test_lanes/<context>/<lane_name>.meta.yaml`:

Refer to `references/meta-format.md` for the complete meta.yaml format specification.

### Step 4: Configure Semantic Types

Map field paths to semantic types for realistic data. Common mappings:

| Field Pattern | Semantic Type |
|--------------|---------------|
| FirstName, GivenName | `person.first_name` |
| LastName, Surname | `person.last_name` |
| SSN, SocialSecurity | `ssn` |
| Email, EmailAddress | `email` |
| Phone, PhoneNumber | `phone_number` |
| Street, Address1 | `address.street` |
| City | `address.city` |
| State | `address.state_abbr` |
| Zip, ZipCode | `address.zipcode` |
| Amount, Balance, Price | `decimal(min, max, decimals)` |
| Date, EffectiveDate | `date.past` or `date.future` |
| VIN | `vehicle.vin` |
| AccountNumber | `pattern:ACC-{######}` |

### Step 5: Configure Field Overrides

Customize generation for specific fields:

```yaml
fieldOverrides:
  "/Root/OptionalSection":    # Optional element
    fillRate: 0.3             # Include 30% of the time
  "/Root/Items/Item":         # Repeating element
    repeatRange: [2, 10]      # Generate 2-10 items
```

### Step 6: Validate the Test Lane

```bash
cd sdks/python

# Dry run to verify generation works
python -m testgen.cli run ./test_lanes/ -l <context>/<lane_name> --dry-run -n 5 --output-dir ./test_output/

# Inspect generated XML
cat ./test_output/*.xml
```

## File Locations

- XSD schemas: `sdks/python/test_lanes/<context>/<lane_name>.xsd`
- Meta configs: `sdks/python/test_lanes/<context>/<lane_name>.meta.yaml`
- CLI module: `sdks/python/testgen/cli.py`

## Resources

This skill includes reference documentation:

### references/
- `meta-format.md` - Complete meta.yaml format specification with all semantic types and options
