---
name: law-machine-readable-interpreter
description: Interprets legal text in regelrecht YAML files and generates machine-readable execution logic with parameters, operations, outputs, and cross-law references. Use when user wants to make a law executable, add machine_readable sections, or interpret legal articles for computational execution.
allowed-tools: Read, Edit, Grep, Glob
---

# Law Machine-Readable Interpreter

Analyzes legal text in YAML files and generates complete machine_readable execution logic.

## What This Skill Does

1. Reads YAML law files from `regulation/nl/`
2. Analyzes each article's legal text
3. Identifies computational elements:
   - Input parameters (BSN, dates, amounts)
   - Constants and definitions
   - Conditions and logic
   - Cross-references to other laws/articles
   - Output values
4. Generates complete `machine_readable` sections with:
   - `competent_authority` - who has binding authority
   - `requires` - dependencies on other laws/regulations
   - `definitions` - constants and fixed values
   - `execution` section containing:
     - `produces` - legal character and decision type
     - `parameters` - caller-provided inputs
     - `input` - data from other sources
     - `output` - what this article produces
     - `actions` - operations and logic
5. Converts monetary amounts to eurocent (€ 795,47 → 79547)
6. Creates TODO comments for missing external law references
7. Uses aggressive AI interpretation (full automation)

## Important Principles

- **Aggressive interpretation**: Generate complete logic even if uncertain
- **Eurocent conversion**: Convert all monetary amounts (€ X,XX → eurocent)
- **Cross-references**: Detect references to other laws/articles
- **TODOs for missing refs**: Add TODO comments when external laws don't exist in repo
- **legal_basis**: Add traceability to specific law text where applicable

## Schema Structure Overview

The schema has NO `public` or `endpoint` fields. The `machine_readable` section structure is:

```yaml
machine_readable:
  competent_authority:        # Who has binding authority
    name: "Belastingdienst"
    type: "INSTANCE"          # or "CATEGORY" (default: INSTANCE)

  requires:                   # Dependencies (optional)
    - law: "Zorgverzekeringswet"
      values: ["is_verzekerd"]

  definitions:                # Constants (optional)
    VERMOGENSGRENS:
      value: 15485900

  execution:
    produces:                 # Legal character (optional)
      legal_character: "BESCHIKKING"  # or TOETS, WAARDEBEPALING, BESLUIT_VAN_ALGEMENE_STREKKING
      decision_type: "TOEKENNING"     # or AFWIJZING, GOEDKEURING, AANSLAG, etc.

    parameters:               # Caller-provided inputs
      - name: "bsn"
        type: "string"
        required: true

    input:                    # Data from other sources
      - name: "toetsingsinkomen"
        type: "amount"
        source:
          regulation: "awir"          # Name of the law/regulation
          output: "toetsingsinkomen"  # Output field to retrieve
          parameters:
            bsn: "$bsn"

    output:                   # What this produces
      - name: "heeft_recht"
        type: "boolean"

    actions:                  # Computation logic
      - output: "heeft_recht"
        operation: "GREATER_THAN_OR_EQUAL"
        subject: "$leeftijd"
        value: 18
```

## Step-by-Step Instructions

### Step 1: Identify Target Law File

When user asks to "interpret" or "make executable" a law:

1. Search `regulation/nl/` for the law file
2. If multiple versions exist, ask which date to use
3. Read the entire YAML file

### Step 2: Analyze Each Article

For each article in the `articles` array:

1. **Read the legal text** in the `text` field
2. **Identify if it's executable:**
   - Does it define a calculation, condition, or decision?
   - Does it provide a concrete output value?
   - If YES → Add `machine_readable` section
   - If NO (just definitions) → Skip or add minimal section

3. **Extract key elements:**
   - **Parameters**: What inputs are needed? (BSN, dates, amounts, etc.)
   - **Constants**: Fixed values defined in the text
   - **Conditions**: If/when/unless statements
   - **Calculations**: Mathematical operations
   - **References**: Mentions of other articles/laws
   - **Outputs**: What the article calculates/determines

### Step 3: Identify Competent Authority

Determine who has binding authority for the decision:

```yaml
competent_authority:
  name: "Belastingdienst/Toeslagen"
  type: "INSTANCE"   # Specific organization
```

Or for categories (must be resolved per context):
```yaml
competent_authority:
  name: "gemeente"
  type: "CATEGORY"   # Abstract category, resolved at runtime
```

### Step 4: Identify and Define Parameters

Look for inputs that must be provided by the caller:

**Common parameters:**
- `bsn` (string) - Citizen service number
- `peildatum` (date) - Reference date
- `jaar` (number) - Year
- `bedrag` (amount) - Amount

**Example from text:**
```
"Een persoon heeft recht op zorgtoeslag indien hij de leeftijd van 18 jaar heeft bereikt"
```
→ Needs `bsn` to look up person's age

**YAML output:**
```yaml
parameters:
  - name: "bsn"
    type: "string"
    required: true
    description: "Burgerservicenummer van de persoon"
```

### Step 5: Extract Constants and Definitions

Look for fixed values mentioned in the text:

**Example from text:**
```
"De grens bedraagt € 154.859 voor een alleenstaande"
```

**YAML output:**
```yaml
definitions:
  VERMOGENSGRENS_ALLEENSTAANDE:
    value: 15485900  # Converted to eurocent!
    description: "Vermogensgrens voor alleenstaande personen"
```

**Monetary Conversion Rules:**
- € 154.859 → 15485900 (eurocent)
- € 2.112 → 211200 (eurocent)
- € 795,47 → 79547 (eurocent)
- Always use integer eurocent values

### Step 6: Identify Cross-Law References (Input Sources)

Look for references to other laws or articles:

**Patterns to detect:**
- "ingevolge de [Law Name]"
- "bedoeld in artikel X"
- "genoemd in [regulation]"
- Markdown links: `[text](https://wetten.overheid.nl/BWBR...)`

**Source Structure:**
```yaml
input:
  - name: "is_verzekerd"
    type: "boolean"
    source:
      regulation: "zorgverzekeringswet"  # Law identifier
      output: "is_verzekerd"             # Output field name
      parameters:
        bsn: "$bsn"
      description: "Verzekerd ingevolge de Zorgverzekeringswet"
```

**For external data (not from another law):**
```yaml
input:
  - name: "geboortedatum"
    type: "date"
    source:
      output: "geboortedatum"  # No regulation = external data source
      description: "Geboortedatum uit BRP"
```

**If external law not found in repo:**
```yaml
input:
  - name: "is_verzekerd"
    type: "boolean"
    source:
      # TODO: Implement zorgverzekeringswet
      regulation: "zorgverzekeringswet"
      output: "is_verzekerd"
      parameters:
        bsn: "$bsn"
```

### Step 7: Define Outputs

Identify what the article produces:

**Data types available:**
- `string` - Text values
- `number` - Numeric values
- `boolean` - True/false
- `amount` - Monetary values (in eurocent)
- `date` - Date values
- `object` - Complex structures
- `array` - Lists

**With type specifications:**
```yaml
output:
  - name: "zorgtoeslag_bedrag"
    type: "amount"
    type_spec:
      unit: "eurocent"
    description: "Het bedrag van de zorgtoeslag"
```

**With temporal metadata:**
```yaml
output:
  - name: "toetsingsinkomen"
    type: "amount"
    temporal:
      type: "period"
      period_type: "year"
```

### Step 8: Interpret Conditions and Logic (Actions)

Convert legal conditions to operations:

**Available Operations:**

| Category | Operations |
|----------|------------|
| Arithmetic | `ADD`, `SUBTRACT`, `MULTIPLY`, `DIVIDE`, `MIN`, `MAX` |
| Comparison | `EQUALS`, `NOT_EQUALS`, `GREATER_THAN`, `LESS_THAN`, `GREATER_THAN_OR_EQUAL`, `LESS_THAN_OR_EQUAL` |
| Logical | `AND`, `OR`, `NOT` |
| Membership | `IN`, `NOT_IN` |
| Null check | `NOT_NULL` |
| Conditional | `IF` |
| Iteration | `FOREACH` |
| Date | `SUBTRACT_DATE` |
| String | `CONCAT` |

**Common Legal Patterns → Operations:**

| Legal Text | Operation |
|------------|-----------|
| "heeft bereikt de leeftijd van 18 jaar" | `GREATER_THAN_OR_EQUAL`, subject: $leeftijd, value: 18 |
| "niet meer bedraagt dan X" | `LESS_THAN_OR_EQUAL` |
| "ten minste X" | `GREATER_THAN_OR_EQUAL` |
| "indien ... en ..." | `AND` with values array |
| "indien ... of ..." | `OR` with values array |
| "niet ..." | `NOT` |
| "gelijk aan" | `EQUALS` |

**Simple comparison:**
```yaml
actions:
  - output: "is_volwassen"
    operation: "GREATER_THAN_OR_EQUAL"
    subject: "$leeftijd"
    value: 18
```

**Multiple conditions (AND/OR):**
```yaml
actions:
  - output: "voldoet_aan_voorwaarden"
    operation: "AND"
    values:
      - operation: "EQUALS"
        subject: "$is_verzekerd"
        value: true
      - operation: "GREATER_THAN_OR_EQUAL"
        subject: "$leeftijd"
        value: 18
```

**Conditional with if-then-else (using conditions array):**
```yaml
actions:
  - output: "toeslag_percentage"
    conditions:
      - test:
          operation: "EQUALS"
          subject: "$huishouden_type"
          value: "alleenstaand"
        then: 100
        else: 50
```

**Conditional with IF operation:**
```yaml
actions:
  - output: "resultaat"
    operation: "IF"
    test:
      operation: "GREATER_THAN"
      subject: "$inkomen"
      value: 50000
    then: 0
    else: "$berekend_bedrag"
```

**Calculation chain:**
```yaml
actions:
  - output: "premie_basis"
    operation: "MULTIPLY"
    values:
      - "$standaardpremie"
      - "$percentage"

  - output: "premie_na_korting"
    operation: "SUBTRACT"
    values:
      - "$premie_basis"
      - "$korting"
```

**Date calculation:**
```yaml
actions:
  - output: "leeftijd"
    operation: "SUBTRACT_DATE"
    values:
      - "$peildatum"
      - "$geboortedatum"
```

**Resolve from ministeriele regeling:**
```yaml
actions:
  - output: "standaardpremie"
    resolve:
      type: "ministeriele_regeling"
      output: "standaardpremie"
      match:
        output: "jaar"
        value: "$jaar"
```

### Step 9: Add Legal Basis (Traceability)

For important computations, add legal_basis to trace back to the law:

```yaml
actions:
  - output: "heeft_recht"
    operation: "AND"
    values:
      - "$is_verzekerd"
      - "$is_volwassen"
    legal_basis:
      law: "Wet op de zorgtoeslag"
      bwb_id: "BWBR0018451"
      article: "2"
      paragraph: "1"
      url: "https://wetten.overheid.nl/BWBR0018451#Artikel2"
      explanation: "Lid 1 bepaalt de voorwaarden voor recht op zorgtoeslag"
```

### Step 10: Set Produces (Legal Character)

If the article produces a formal decision:

```yaml
execution:
  produces:
    legal_character: "BESCHIKKING"  # Individual decision
    decision_type: "TOEKENNING"     # Grant/approval
```

**Legal character options:**
- `BESCHIKKING` - Individual administrative decision
- `TOETS` - Check/verification
- `WAARDEBEPALING` - Value determination
- `BESLUIT_VAN_ALGEMENE_STREKKING` - General binding decision

**Decision type options:**
- `TOEKENNING` - Grant
- `AFWIJZING` - Rejection
- `GOEDKEURING` - Approval
- `AANSLAG` - Tax assessment
- `ALGEMEEN_VERBINDEND_VOORSCHRIFT` - General binding regulation
- `BELEIDSREGEL` - Policy rule
- `VOORBEREIDINGSBESLUIT` - Preparatory decision
- `ANDERE_HANDELING` - Other action

### Step 11: Complete Example

**Legal text:**
```
Artikel 2
1. Een persoon heeft recht op zorgtoeslag indien hij:
   a. de leeftijd van 18 jaar heeft bereikt;
   b. verzekerd is ingevolge de Zorgverzekeringswet.
```

**Complete machine_readable section:**
```yaml
machine_readable:
  competent_authority:
    name: "Belastingdienst/Toeslagen"

  requires:
    - law: "Zorgverzekeringswet"
      values: ["is_verzekerd"]

  execution:
    produces:
      legal_character: "BESCHIKKING"
      decision_type: "TOEKENNING"

    parameters:
      - name: "bsn"
        type: "string"
        required: true
        description: "Burgerservicenummer"

      - name: "peildatum"
        type: "date"
        required: true
        description: "Datum waarop het recht wordt getoetst"

    input:
      - name: "geboortedatum"
        type: "date"
        source:
          output: "geboortedatum"
          description: "Geboortedatum uit BRP"

      - name: "is_verzekerd"
        type: "boolean"
        source:
          # TODO: Implement zorgverzekeringswet
          regulation: "zorgverzekeringswet"
          output: "is_verzekerd"
          parameters:
            bsn: "$bsn"

    output:
      - name: "leeftijd"
        type: "number"
        type_spec:
          unit: "years"

      - name: "heeft_recht"
        type: "boolean"
        description: "Geeft aan of de persoon recht heeft op zorgtoeslag"

    actions:
      - output: "leeftijd"
        operation: "SUBTRACT_DATE"
        values:
          - "$peildatum"
          - "$geboortedatum"
        legal_basis:
          article: "2"
          paragraph: "1"
          explanation: "Leeftijd bepaald op peildatum"

      - output: "heeft_recht"
        operation: "AND"
        values:
          - operation: "GREATER_THAN_OR_EQUAL"
            subject: "$leeftijd"
            value: 18
          - operation: "EQUALS"
            subject: "$is_verzekerd"
            value: true
        legal_basis:
          article: "2"
          paragraph: "1"
          explanation: "Voorwaarden a en b van lid 1"
```

### Step 12: Apply Changes to YAML

For each article that needs a `machine_readable` section:

1. Use the Edit tool to add the section after the `url` field
2. Maintain proper YAML indentation (2 spaces per level)
3. Add comments for TODOs and clarifications
4. Convert all monetary amounts to eurocent

### Step 13: Validate Against Schema and Lint

Before reporting, validate the updated YAML:

**Step 13a: Run YAML linting**
```bash
uv run yamllint {LAW_FILE_PATH}
```

This checks for:
- Line length (max 125 chars - wrap long text!)
- Proper indentation
- Quote usage
- YAML formatting

**Step 13b: Run schema validation**
```bash
uv run python script/validate.py {LAW_FILE_PATH}
```

This validates against the JSON schema.

**If validation fails:**
- Review schema errors carefully
- Common issues with machine_readable sections:
  - Missing required `output` field in source
  - Wrong operation types (check enum values)
  - Missing required fields in parameters/input/output
  - Incorrect nesting or indentation
- Fix errors and re-validate
- Continue until both lint and validation pass

### Step 14: Reverse Validation (Hallucination Check)

After schema validation passes, verify that every element in the `machine_readable` section can be traced back to the original legal text.

**For each element, check:**

1. **Definitions/Constants:**
   - Is this value explicitly mentioned in the article text?
   - If NOT → Remove it from the YAML
   - If needed for logic but not in text → Add to "Assumptions" in report

2. **Input fields:**
   - Is this data source referenced in the article text?
   - Look for phrases like "ingevolge", "bedoeld in", "genoemd in"
   - If NOT traceable → Remove or mark as assumption

3. **Output fields:**
   - Does the article actually produce this output?
   - Is it stated or clearly implied in the legal text?
   - If NOT → Remove it

4. **Actions/Operations:**
   - Does the legal text contain the logic for this operation?
   - Can you point to specific sentences that justify this action?
   - If NOT → Remove or simplify

5. **Conditions:**
   - Are these conditions explicitly stated in the article?
   - Watch for invented edge cases not in the law
   - If NOT → Remove

**Decision matrix:**

| Traceable in text? | Needed for logic? | Action |
|-------------------|-------------------|--------|
| YES | YES | Keep |
| YES | NO | Keep (may be informational) |
| NO | YES | Report as assumption |
| NO | NO | **Remove** |

**Example check:**

```yaml
# Article text: "Een persoon heeft recht indien hij 18 jaar is"

# GOOD - traceable:
- output: "heeft_recht"        # ✓ "heeft recht" in text
  operation: "GREATER_THAN_OR_EQUAL"
  subject: "$leeftijd"
  value: 18                    # ✓ "18 jaar" in text

# BAD - not traceable (hallucinated):
- output: "woont_in_nederland"  # ✗ Not mentioned in article
  operation: "EQUALS"
  subject: "$woonland"
  value: "NL"
# → REMOVE THIS
```

**After reverse validation:**
- Remove all non-traceable elements that aren't needed
- Add "Assumptions" section to report for elements that are:
  - Not explicitly in text
  - But required to make the logic complete
  - These need user review

### Step 15: Report Results

After successful validation:

1. **Count processed articles:**
   - How many articles total?
   - How many now have machine_readable sections?

2. **List TODOs:**
   - Which external laws need to be downloaded?
   - Any ambiguous interpretations?

3. **List Assumptions (from reverse validation):**
   - Elements not explicitly in text but needed for logic
   - These require user verification

4. **Report to user:**
```
Interpreted {LAW_NAME}

  Articles processed: {TOTAL}
  Made executable: {EXECUTABLE_COUNT}
  Schema validation: PASSED
  Reverse validation: PASSED

  Assumptions (need review):
  - Article 2: Added "peildatum" parameter (implied but not stated)
  - Article 3: Assumed "inkomen" refers to toetsingsinkomen

  TODOs remaining:
  - Download and interpret: {external_law_1}
  - Clarify calculation in article {X}

  The law is now executable via the engine!
```

## Common Patterns

### Pattern 1: Age Check
```yaml
input:
  - name: "geboortedatum"
    type: "date"
    source:
      output: "geboortedatum"
      description: "Geboortedatum uit BRP"

actions:
  - output: "leeftijd"
    operation: "SUBTRACT_DATE"
    values:
      - "$peildatum"
      - "$geboortedatum"

  - output: "is_volwassen"
    operation: "GREATER_THAN_OR_EQUAL"
    subject: "$leeftijd"
    value: 18
```

### Pattern 2: Income Threshold
```yaml
definitions:
  INKOMENSGRENS:
    value: 7954700  # € 79.547 in eurocent

input:
  - name: "toetsingsinkomen"
    type: "amount"
    source:
      regulation: "awir"
      output: "toetsingsinkomen"
      parameters:
        bsn: "$bsn"
        jaar: "$jaar"

actions:
  - output: "onder_inkomensgrens"
    operation: "LESS_THAN_OR_EQUAL"
    subject: "$toetsingsinkomen"
    value: "$INKOMENSGRENS"
```

### Pattern 3: Multiple Conditions (AND)
```yaml
actions:
  - output: "voldoet_aan_voorwaarden"
    operation: "AND"
    values:
      - operation: "EQUALS"
        subject: "$is_verzekerd"
        value: true
      - operation: "GREATER_THAN_OR_EQUAL"
        subject: "$leeftijd"
        value: 18
      - operation: "EQUALS"
        subject: "$woont_in_nederland"
        value: true
```

### Pattern 4: Calculation Chain
```yaml
actions:
  - output: "premie_basis"
    operation: "MULTIPLY"
    values:
      - "$standaardpremie"
      - "$percentage"

  - output: "premie_na_korting"
    operation: "SUBTRACT"
    values:
      - "$premie_basis"
      - "$korting"

  - output: "premie_finaal"
    operation: "MAX"
    values:
      - 0
      - "$premie_na_korting"
```

### Pattern 5: Conditional Value
```yaml
actions:
  - output: "vermogensgrens"
    conditions:
      - test:
          operation: "EQUALS"
          subject: "$heeft_partner"
          value: true
        then: "$VERMOGENSGRENS_PARTNERS"
        else: "$VERMOGENSGRENS_ALLEENSTAANDE"
```

### Pattern 6: Lookup from Ministeriele Regeling
```yaml
actions:
  - output: "standaardpremie"
    resolve:
      type: "ministeriele_regeling"
      output: "standaardpremie"
      match:
        output: "jaar"
        value: "$jaar"
```

## Tips for Success

1. **Be aggressive**: Generate complete logic even if uncertain
2. **Use descriptive names**: `toetsingsinkomen` not `income`
3. **Always eurocent**: Never use decimal euro amounts
4. **Check for existing laws**: Use Glob to search `regulation/nl/`
5. **Break down complex logic**: Multiple simple actions > one complex action
6. **Add descriptions**: Help future readers understand the logic
7. **Mark TODOs clearly**: Use `# TODO:` comments for missing refs
8. **Validate types**: Ensure type consistency (boolean, number, string, date, amount)
9. **Document assumptions**: Add comments when interpretation is unclear
10. **Add legal_basis**: Trace important computations back to the law text

## Error Handling

**If legal text is ambiguous:**
- Make best guess with TODO comment
- Explain uncertainty to user
- Suggest manual review

**If external law not found:**
- Create TODO placeholder in source
- Add to list of missing dependencies
- Continue with other articles

**If operation unclear:**
- Use simpler operations
- Break into multiple steps
- Add explanatory comments
