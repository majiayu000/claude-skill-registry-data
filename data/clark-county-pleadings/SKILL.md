---
name: clark-county-pleadings
description: Create, edit, and convert legal pleadings for Clark County District Court and Justice Court, Nevada. Handles specialized .doc/.docx format with line numbering (1-28), proper caption formatting, document codes (District Court), criminal/civil motion templates, and PDF conversion. Use for drafting motions to suppress, discovery requests, continuances, oppositions, and other court documents for both Nevada District and Justice Courts.
---

# Clark County Legal Pleadings (District & Justice Court)

Create professional legal pleadings in proper Clark County format with automated line numbering, caption formatting, document codes, and court-specific document structure.

## Capabilities

### Dual Court Support
- **District Court**: Full EDCR 7.20 compliance with document codes
- **Justice Court**: JCRLV compliant format
- Automatic formatting based on court type
- Court-specific captions and requirements

### Document Creation
- Generate new pleadings from scratch in DOCX format
- Use pre-built templates for common criminal motions
- Automated line numbering (1-28) in left margin
- Proper caption and case heading formatting
- Document codes (District Court only)
- Certificate of mailing/service generation
- Declaration under penalty of perjury (NRS 53.045)

### Document Conversion
- Convert DOCX to PDF (court-ready format)
- Parse existing pleadings to extract information
- Read and analyze .doc files (RTF format)

### Specialized Criminal Motion Templates
- Motion to Suppress Evidence (Edwards v. Arizona violations)
- Motion to Suppress Evidence (Fourth Amendment violations)
- Motion for Discovery (comprehensive Brady/Giglio requests)
- Custom motion generation for any criminal procedure issue

## Quick Start

### Selecting Your Court

**District Court** - Use for:
- Felonies
- Gross misdemeanors (initial filing)
- Civil cases over $15,000
- Formal proceedings requiring EDCR compliance

**Justice Court** - Use for:
- Misdemeanors
- Preliminary hearings (felonies)
- Civil cases under $15,000
- Small claims
- Traffic violations

### Creating a New Pleading

Use the `create_pleading.py` script:

```python
from scripts.create_pleading import create_pleading

case_info = {
    'party_name': 'John Doe',
    'party_address': '123 Main St',
    'party_city_state_zip': 'Las Vegas, NV 89101',
    'party_phone': '(702) 555-1234',
    'party_email': 'john.doe@example.com',
    'party_type': 'defendant',  # or 'plaintiff'
    'case_number': '25-CR-062245-001',
    'dept_number': '5',
    'plaintiff_name': 'STATE OF NEVADA',
    'defendant_name': 'JOHN DOE',
    'document_title': 'MOTION TO SUPPRESS EVIDENCE',
    'court_type': 'district',  # or 'justice' - NEW PARAMETER
    'document_code': 'MOTN'     # Required for District Court
}

content = [
    "COMES NOW, the Defendant and respectfully submits this Motion...",
    "",
    "I. STATEMENT OF FACTS",
    "",
    "On [date], officers...",
]

service_addresses = [
    {'name': 'Clark County District Attorney', 
     'address': '200 Lewis Ave, Las Vegas, NV 89101'}
]

create_pleading(case_info, content, service_addresses, 'motion_suppress.docx')
```

### District Court Document Codes

**Required on Line 1 for District Court filings:**

| Code | Document Type |
|------|---------------|
| MOTN | Motion |
| OPPS | Opposition |
| RPLY | Reply |
| AFFT | Affidavit |
| NOTC | Notice |
| ORDM | Order/Minute Order |
| STIP | Stipulation |
| PLNT | Complaint/Petition |
| ANSW | Answer |
| DCVR | Discovery |
| MEMO | Memorandum of Points and Authorities |
| APPL | Application |
| HRNG | Hearing |
| EXPT | Ex Parte |
| CERT | Certificate |

### Using Templates

Templates are located in `assets/` directory:

1. **Edwards Violation Template**: `motion_suppress_edwards_template.docx`
   - Pre-formatted for Fifth Amendment / Edwards v. Arizona violations
   - Includes legal argument structure
   - Fill in bracketed placeholders
   - Works for both courts (specify court_type)

2. **Fourth Amendment Template**: `motion_suppress_4th_amendment_template.docx`
   - Pre-formatted for illegal stop/search/seizure
   - Multiple grounds (stop, arrest, search, warrant)
   - Fruit of poisonous tree analysis
   - Compatible with both courts

3. **Discovery Template**: `motion_discovery_template.docx`
   - Comprehensive Brady/Giglio requests
   - All standard discovery items
   - Legal authorities included
   - Adaptable for both courts

### Converting to PDF

```bash
python3 scripts/convert_to_pdf.py motion_suppress.docx -o motion_suppress.pdf
```

Or use the Python API:

```python
from scripts.convert_to_pdf import convert_to_pdf

convert_to_pdf('motion_suppress.docx', 'motion_suppress.pdf', method='auto')
```

## Format Requirements

### District Court (EDCR 7.20)

| Element | Requirement |
|---------|-------------|
| **Line Numbering** | 1-28, left margin, restart each page |
| **Margins** | 1" all sides (left initially, space for numbers) |
| **Font** | 12pt computer type or 10 pica typewriter |
| **Document Code** | Required on line 1 (MOTN, OPPS, etc.) |
| **Caption** | DISTRICT COURT / CLARK COUNTY, NEVADA |
| **Holes** | 2 centered holes, 2¾" apart |
| **Spacing** | Double-spaced lines |

### Justice Court (JCRLV)

| Element | Requirement |
|---------|-------------|
| **Line Numbering** | Required in left margin, continuous |
| **Margins** | 1.5" left, 1" right/top/bottom |
| **Font** | 12pt Times New Roman (preferred) |
| **Document Code** | Not required |
| **Caption** | JUSTICE COURT, TOWNSHIP OF [X] |
| **Spacing** | Double-spaced between paragraphs |

### Common Elements (Both Courts)
- **Declaration**: NRS 53.045 penalty of perjury clause
- **Certificate**: Certificate of mailing for all served documents
- **Case Number Format**: 
  - District: Various formats
  - Justice: YY-CR-NNNNNN-NNN (criminal)

## Criminal Case Format

### District Court
- Case number: Varies by year/type
- Plaintiff: `STATE OF NEVADA`
- Caption: `DISTRICT COURT` / `CLARK COUNTY, NEVADA`
- Document codes required
- Formal EDCR compliance

### Justice Court
- Case number: `YY-CR-NNNNNN-NNN` (e.g., 25-CR-062245-001)
- Plaintiff: `STATE OF NEVADA`
- Caption: `JUSTICE COURT, TOWNSHIP OF [X]` / `CLARK COUNTY, NEVADA`
- No document codes
- "In Proper Person" designation for pro se litigants

## Criminal Motions Guide

See `references/criminal_motions.md` for detailed guidance on:

### Motion Types (Both Courts)
- **Suppression**: Evidence obtained via constitutional violations
- **Dismissal**: Speedy trial, statute of limitations, due process
- **Discovery**: Brady, Giglio, police reports, bodycam footage
- **Continuance**: Time to prepare, discovery pending
- **Opposition/Reply**: Responding to State's motions

### Key Legal Standards

**Fourth Amendment (Search & Seizure)**:
- Warrantless searches presumptively unreasonable
- Exceptions: consent, search incident to arrest, exigent circumstances
- Terry stops require reasonable suspicion
- Arrests require probable cause

**Fifth Amendment (Self-Incrimination)**:
- Miranda warnings required for custodial interrogation
- Edwards v. Arizona: No re-interrogation after invocation
- Statements must be voluntary

**Discovery (JCRCP 16.1 / NRCP 16)**:
- State must disclose all Brady material (exculpatory)
- State must disclose all Giglio material (impeachment)
- Bodycam footage, police reports, witness statements
- Continuing duty to supplement

### Filing Deadlines
- **Opposition**: 10 judicial days after motion served
- **Reply**: 5 judicial days after opposition served
- **Notice of hearing**: 14 calendar days minimum

## Workflow Examples

### Example 1: Edwards Violation Suppression Motion (District Court)

Your case: Officers continued interrogation after you invoked right to counsel.

**Steps**:
1. Open `assets/motion_suppress_edwards_template.docx`
2. Add document code `MOTN` on line 1
3. Fill in case caption with District Court heading
4. Replace bracketed sections with:
   - Detailed facts (when, where, exact words of invocation)
   - Time between invocation and re-interrogation
   - Statements obtained
5. Add legal analysis applying Edwards to your facts
6. Save and convert to PDF for e-filing

**Key Facts to Include**:
- Exact quote of rights invocation
- Officer's response or lack thereof
- How much time passed
- Who initiated subsequent contact
- Evidence that you did not reinitiate

### Example 2: Fourth Amendment Illegal Stop (Justice Court)

Your case: Officer stopped you without reasonable suspicion at preliminary hearing.

**Steps**:
1. Open `assets/motion_suppress_4th_amendment_template.docx`
2. Use Justice Court caption (no document code needed)
3. Fill in case information
4. Statement of Facts: Chronological narrative
   - Dispatch call or officer observation that led to stop
   - Your actions (walking, driving, etc.)
   - No criminal activity observed
   - Vague or generic justification by officer
5. Legal Argument:
   - Terry standard (reasonable, articulable suspicion)
   - Apply to facts (no suspicion existed)
   - Bodycam shows lack of reasonable suspicion
6. List evidence to suppress (statements, physical evidence)

### Example 3: Comprehensive Discovery Request (Both Courts)

**Steps**:
1. Open `assets/motion_discovery_template.docx`
2. Specify court type:
   - District: Add document code `MOTN` or `DCVR`
   - Justice: No code needed
3. Adjust caption for court type
4. Review 15-point discovery list
5. Add case-specific requests:
   - Specific bodycam footage (dates, officers)
   - Specific forensic reports
   - Specific witness statements
6. Emphasize Brady/Giglio obligations
7. Request deadline for compliance (typically 14 days)

## Court Comparison Chart

| Feature | District Court | Justice Court |
|---------|----------------|---------------|
| **Criminal Jurisdiction** | Felonies | Misdemeanors, preliminary hearings |
| **Civil Jurisdiction** | Over $15,000 | Under $15,000 |
| **Document Codes** | Required (MOTN, OPPS, etc.) | Not required |
| **Caption Heading** | DISTRICT COURT | JUSTICE COURT, TOWNSHIP OF [X] |
| **Line Number Limit** | 28 lines per page | No specific limit |
| **Left Margin** | 1" (with numbering space) | 1.5" |
| **E-Filing System** | efilenv.com | efilenv.com |
| **Rules** | EDCR, NRCP | JCRCP, JCRLV |
| **Format Strictness** | Very strict (EDCR 7.20) | Moderate |

## E-Filing in Clark County

### Both Courts Use efilenv.com

**Registration**: Required for all e-filers
**File Format**: PDF only
**Size Limit**: 25MB per document
**Service**: Electronic if parties consent

**District Court Additional Requirements**:
- Document codes mandatory
- Strict EDCR 7.20 formatting
- Cover sheet for new cases
- May require specific metadata

**Justice Court Requirements**:
- No document codes
- Standard formatting
- Certificate of service required

## Tips for Pro Se Litigants

### Choosing the Right Court
- Felonies → District Court (after preliminary hearing)
- Misdemeanors → Justice Court (complete case)
- Civil over $15K → District Court
- Civil under $15K → Justice Court

### Document Preparation
1. **Always specify court type**: Ensures proper format
2. **Use document codes** (District Court only)
3. **Line numbering is mandatory**: Script handles this automatically
4. **Certificate of service required**: For all served documents
5. **Keep it professional**: Stick to facts and law, no emotional arguments

### Common Mistakes to Avoid
- Wrong court designation in caption
- Missing document codes (District Court)
- Improper service (must serve all parties)
- Generic motions (be specific with facts and law)
- No legal citations (always cite applicable statutes/cases)
- Missing certificate of service
- Improper formatting (use this skill to avoid)

### Evidence Matters
- **Bodycam footage**: Request immediately, crucial for suppression
- **Transcripts**: Get verbatim record of interrogations
- **Police reports**: Often contradict video evidence
- **Dispatch logs**: Show timeline and basis for stop
- **Witness statements**: Independent corroboration

### At Hearings
- Arrive 15 minutes early
- Bring organized exhibits (tabbed)
- Have extra copies of motion/opposition for court
- Professional dress and demeanor
- Address judge as "Your Honor"
- Stay focused on strongest legal arguments

## Advanced Usage

### Custom Motion Creation

For motions not covered by templates:

```python
from scripts.create_pleading import create_pleading

case_info = {
    # Standard case info
    'court_type': 'district',  # or 'justice'
    'document_code': 'MOTN',    # District only
    # ... other info
}

content = [
    "MOTION TO [TITLE]",
    "",
    "COMES NOW, the Defendant and respectfully moves...",
    "",
    "I. FACTUAL BACKGROUND",
    "[Your facts]",
    "",
    "II. LEGAL ARGUMENT",
    "[Your legal analysis with citations]",
    "",
    "III. CONCLUSION",
    "[Request for relief]"
]

create_pleading(case_info, content, service_addresses, 'custom_motion.docx')
```

### Batch Processing

Convert multiple documents:

```bash
for file in *.docx; do
    python3 scripts/convert_to_pdf.py "$file"
done
```

### Integration with Case Management

Organize by court and case number:

```
/case_documents/
    district_court/
        25-CR-001234/
            motions/
                01_motion_suppress_edwards.docx
                01_motion_suppress_edwards.pdf
    justice_court/
        25-CR-062245-001/
            motions/
                01_motion_suppress.docx
            discovery/
                bodycam_footage.mp4
```

## Reference Documents

### Formatting Rules
See `references/formatting_rules.md` for:
- Complete page setup specifications for both courts
- Caption formatting details (District vs Justice)
- Font and spacing requirements
- Declaration and certificate templates
- Service requirements (JCRCP 5 / NRCP 5)
- Electronic filing guidelines

### Document Codes Reference
See `references/document_codes.md` for:
- Complete list of District Court codes
- Usage guidelines
- Code selection for different document types
- When codes are required vs optional

### Criminal Motions Guide
See `references/criminal_motions.md` for:
- Detailed motion structures for all types
- Legal standards (Terry, Miranda, Edwards, Brady)
- Nevada-specific statutes and cases
- Court-specific considerations
- Hearing preparation checklist
- Sample legal arguments

### Court Differences Guide
See `references/court_differences.md` for:
- Side-by-side comparison of requirements
- When to file in which court
- Jurisdictional considerations
- Format requirement differences

## Scripts Reference

### create_pleading.py
Create formatted pleadings programmatically with court selection.

**New Parameters**:
- `court_type`: 'district' or 'justice' (required)
- `document_code`: Document code for District Court (required for District)

**Functions**:
- `create_pleading()`: Main function, creates complete document
- `add_caption()`: Add court-specific case caption
- `add_document_code()`: Add code to line 1 (District only)
- `add_declaration()`: Add penalty of perjury clause
- `add_certificate_of_mailing()`: Add service certificate
- `setup_page()`: Configure margins and line numbering

### document_codes.py
Document code management for District Court.

**Functions**:
- `get_code()`: Get code for document type
- `validate_code()`: Verify code is valid
- `get_code_description()`: Get full description

### convert_to_pdf.py
Convert DOCX to PDF for court filing.

**Methods**:
- `auto`: Try LibreOffice first, fall back to docx2pdf
- `libreoffice`: Use LibreOffice (better quality)
- `docx2pdf`: Use docx2pdf library (requires Windows/macOS)

**Usage**: `python3 convert_to_pdf.py input.docx -o output.pdf -m auto`

## Dependencies

Required Python packages:
- `python-docx`: DOCX creation and manipulation
- `striprtf`: Read .doc files (RTF format)
- `docx2pdf`: PDF conversion (optional, fallback)

Install with:
```bash
pip install python-docx striprtf docx2pdf
```

LibreOffice (recommended for PDF conversion):
- Linux: `sudo apt install libreoffice`
- macOS: `brew install --cask libreoffice`
- Windows: Download from libreoffice.org

## Support and Resources

### Clark County Court Resources
- District Court: clarkcountycourts.us
- Justice Court: lvjustice.court.nv.gov
- E-Filing: efilenv.com
- Civil Law Self-Help Center: civillawselfhelpcenter.org

### Nevada Legal Resources
- Nevada Revised Statutes: leg.state.nv.us/nrs
- Court Rules: leg.state.nv.us/courtrules
- EDCR (District): clarkcountycourts.us
- JCRLV (Justice): Available online

### Key Statutes (Both Courts)
- NRS 53.045: Declaration under penalty of perjury
- NRS 171.123: Duty to identify statute
- NRS 174.125: Motion to suppress evidence
- NRS 178.556: Speedy trial requirements
- JCRCP/NRCP 16.1: Discovery in criminal cases

### Key Cases (Both Courts)
- Edwards v. Arizona, 451 U.S. 477 (1981)
- Miranda v. Arizona, 384 U.S. 436 (1966)
- Terry v. Ohio, 392 U.S. 1 (1968)
- Brady v. Maryland, 373 U.S. 83 (1963)
- Mapp v. Ohio, 367 U.S. 643 (1961)

## Validation and Testing

### Before Filing
1. **Verify court type**: Matches your case venue
2. **Check document code**: Required for District, not Justice
3. **Validate caption**: Correct court name and case number
4. **Line numbering**: Properly formatted (1-28)
5. **Certificate of service**: Present and accurate
6. **Font and spacing**: Meets court requirements

### Test Checklist
```python
# Use validation function
from scripts.validate_pleading import validate_pleading

errors = validate_pleading('motion.docx', court_type='district')
if errors:
    print("Errors found:", errors)
else:
    print("Document valid for filing")
```

## Updates and Maintenance

**Version**: 2.0 (Dual Court Support)
**Last Updated**: October 2024
**Changes**:
- Added District Court support
- Implemented document codes
- Court-specific formatting
- Updated documentation
- Enhanced validation

This skill now provides comprehensive support for both Clark County District Court and Justice Court proceedings, ensuring proper formatting and compliance with all applicable rules.
