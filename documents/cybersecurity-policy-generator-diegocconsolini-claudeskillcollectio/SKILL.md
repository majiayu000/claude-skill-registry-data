---
name: cybersecurity-policy-generator
description: Generate enterprise cybersecurity policies from 51 professional templates (SANS, CIS Controls) for ISO 27001, SOC 2, NIST, and CIS Controls compliance in Markdown, Word, HTML, and PDF formats
license: MIT
---

# Cybersecurity Policy Generator

## Purpose

Generate professional, framework-compliant cybersecurity policies using 51 industry-standard templates from SANS and CIS Controls. Creates complete policy documents customized for your organization in 4 formats: Markdown, Word, HTML, and PDF.

**Key capabilities:**
1. Browse 51 professional policy templates across 15 security categories
2. Interactive customization using AskUserQuestion for beautiful UI
3. Map policies to ISO 27001, SOC 2, NIST CSF, CIS Controls v8, and GDPR
4. Generate professional policy documents in 4 formats
5. Support compliance requirements for security program development

## When to Use This Skill

Use this skill when:
- Starting a security program and need foundational policies (Acceptable Use, Password Policy, etc.)
- Preparing for compliance audits (ISO 27001, SOC 2, NIST CSF, CIS Controls)
- Updating outdated security policies with current best practices
- Creating incident response, data protection, or access control policies
- Building policy documentation for framework compliance
- Need professional policy templates instead of starting from scratch

**Do NOT use for:**
- Legal advice (templates require review by qualified legal counsel)
- Website privacy policies (this creates corporate security policies)
- Compliance certification (policies support but don't guarantee certification)
- Custom policy authoring from scratch (uses existing templates)
- Policy enforcement or monitoring (generates documents only)

## Workflow

### Phase 1: Policy Selection

**Step 1 - Ask How Many Policies:**

Use AskUserQuestion to ask:
- "How many policies would you like to generate?"
- Header: "Quantity"
- Options: 1 policy, 3 policies, 5 foundational policies, 10 comprehensive set, Custom number

If user selects "Custom number", they can specify via "Other" option.

**Step 2 - Browse Available Policies:**

Run browse_policies.py to show the 51 available policies. Optionally filter by user's industry or compliance needs:

```bash
# Show all policies with categories
python3 scripts/browse_policies.py

# Or filter by their compliance framework
python3 scripts/browse_policies.py --framework "ISO 27001"
```

**Step 3 - Let User Select Specific Policies:**

Use AskUserQuestion with multiSelect: true to let user choose policies:

Example for governance policies:
- "Which policies would you like to generate?" (multiSelect: true)
- Header: "Policies"
- Options: Present top 4 most relevant policies based on their needs, user can select multiple

**Repeat** AskUserQuestion for different categories if generating multiple policies:
- Governance policies (if needed)
- Identity & Access policies (if needed)
- Data Protection policies (if needed)
- etc.

**Alternative for 5/10 policy sets:** If user selected pre-defined sets (like "5 foundational"), automatically select the appropriate policies without asking individually.

**Recommended Policy Sets:**
- **5 Foundational:** Information Security, Acceptable Use, Password, Data Classification, Data Recovery
- **10 Comprehensive:** Above 5 + Access Control, Incident Response, Remote Access, Security Awareness, Vulnerability Management

### Phase 2: Output Format Selection

Use AskUserQuestion to ask about output preferences:

**Question Set 1 - Output Formats:**

- "Which output formats do you need?" (multiSelect: true)
- Header: "Formats"
- Options:
  1. Markdown (.md) - For documentation systems
  2. Microsoft Word (.docx) - For legal review and editing
  3. HTML (.html) - For intranet publishing
  4. PDF (.pdf) - For distribution and printing

**Question Set 2 - Customization Level:**

- "Do you want to customize the document appearance?"
- Header: "Branding"
- Options:
  1. Standard - Use default professional formatting
  2. Custom - Add company logo and brand colors
  3. Minimal - Plain text, no styling
  4. Skip - Just generate policies quickly

If user selects "Custom", ask follow-up questions:
- "Do you have a company logo file?" (Yes - will provide path / No - use company name)
- "What are your brand colors?" (Provide hex codes or skip for defaults)
- "Any specific formatting preferences?" (Free text input)

### Phase 3: Organization Information

Use the **AskUserQuestion tool** to collect organization-specific information with beautiful multiple-choice UI.

**Question Set 1 - Organization Basics:**

Use AskUserQuestion to ask:
1. "What is your organization's legal name?" (Let user type via "Other" option, provide 2 dummy options to meet minimum)
2. "What industry does your organization operate in?" (header: "Industry", options: Technology, Finance, Healthcare, Government, Manufacturing, Retail)
3. "How many employees does your organization have?" (header: "Size", options: <50, 50-500, 500-1000, 1000+)

**Question Set 2 - Governance:**

Use AskUserQuestion to ask:
1. "Who is the executive responsible for these policies?" (header: "Officer", options: CISO, CTO, CRO, VP InfoSec, IT Director)
2. "Which department owns these policies?" (header: "Department", options: InfoSec, IT, Risk, Compliance)
3. "What is the contact email for policy questions?" (header: "Contact", let user type via "Other")

**Question Set 3 - Lifecycle:**

Use AskUserQuestion to ask:
1. "When should these policies take effect?" (header: "Effective Date", provide common options like "Next month", "Start of quarter", "Custom date")
2. "How often will these policies be reviewed?" (header: "Review", options: Quarterly, Semi-annually, Annually, Bi-annually)

**Question Set 4 - Compliance:**

Use AskUserQuestion to ask (multiSelect: true):
1. "Which compliance frameworks must you meet?" (header: "Frameworks", options: ISO 27001, SOC 2, NIST CSF, CIS Controls v8, GDPR, HIPAA, PCI-DSS)
2. "Are there specific regulatory requirements?" (header: "Regulations", options: None, GDPR, HIPAA, PCI-DSS, SOX, GLBA, FERPA)

**Step 4:** Save answers to customizations.json file:
```json
{
  "company_name": "Acme Corporation Inc.",
  "industry": "Technology",
  "organization_size": "50-500 employees",
  "responsible_officer": "Chief Information Security Officer (CISO)",
  "responsible_department": "Information Security Department",
  "contact_email": "security@acme.com",
  "effective_date": "2025-11-01",
  "review_schedule": "Annually",
  "version": "1.0",
  "frameworks": ["ISO 27001", "SOC 2"],
  "regulations": ["None"]
}
```

### Phase 4: Generate Policy Documents

For EACH selected policy, follow this process:

**Step 1 - Generate Markdown (Base Format):**

Create professional Markdown `.md` file directly with:
- Company header with metadata
- Table of contents
- All policy sections (Purpose, Scope, Policy, Compliance, etc.)
- Compliance framework mappings
- Approval section

Save as: `output/markdown/{PolicyNumber}-{PolicyName}.md`

**Step 2 - Convert to Requested Formats:**

Based on user's format selections from Phase 2, **call specialized skills/agents** for each format:

**If Word (.docx) selected:**

**USE THE SKILL TOOL** to call document conversion:
```
Skill(command: "word-converter")
OR
Skill(command: "docx")
OR
Task(subagent_type: "document-converter", prompt: "Convert markdown to Word...")
```

Pass the markdown file path and request:
- Professional formatting (headers, footers)
- Company branding (if custom selected)
- Table of contents
- Styled sections
- Ready for legal review

**If HTML (.html) selected:**

**USE THE SKILL TOOL** to call HTML conversion:
```
Skill(command: "html-converter")
OR
Skill(command: "markdown-to-html")
```

Pass the markdown file and request:
- Responsive CSS styling
- Company colors (if custom branding)
- Clean, printable format
- Navigation-friendly structure

**If PDF (.pdf) selected:**

**USE THE SKILL TOOL** to call PDF conversion:
```
Skill(command: "pdf")
OR
Skill(command: "pdf-converter")
OR
Task(subagent_type: "document-converter", prompt: "Convert markdown to PDF...")
```

Pass the markdown file and request:
- Distribution-ready formatting
- Company logo (if provided)
- Professional appearance
- Locked/final format

**IMPORTANT:**
- **DO NOT** use system commands (pandoc, wkhtmltopdf, etc.) directly
- **DO NOT** install Python packages yourself
- **ALWAYS** delegate format conversion to specialized skills/agents
- If a required skill is not available, inform the user and recommend installation

**Step 3 - Apply Customization Options:**

**If user selected "Standard" branding:**
- Use professional default formatting
- Company name in headers
- Clean, readable layout

**If user selected "Custom" branding:**
- Add company logo to header (if provided logo path)
- Apply brand colors to:
  - Headers (primary color)
  - Accents (secondary color)
  - Tables and borders
- Custom fonts (if specified)

**If user selected "Minimal" branding:**
- Plain text formatting
- No colors or styling
- Focus on content only

**Step 4 - Organize Output Files:**

Create organized output directory structure:
```
output/
├── markdown/
│   ├── 1-AcceptableUsePolicy.md
│   ├── 2-PasswordPolicy.md
│   └── ...
├── word/
│   ├── AcceptableUsePolicy.docx
│   ├── PasswordPolicy.docx
│   └── ...
├── html/
│   ├── AcceptableUsePolicy.html
│   ├── PasswordPolicy.html
│   └── ...
├── pdf/
│   ├── AcceptableUsePolicy.pdf
│   ├── PasswordPolicy.pdf
│   └── ...
└── SUMMARY.md (generation summary with all policies listed)
```

**Step 5 - Present Results:**

Show user:
1. Total policies generated
2. Formats created for each policy
3. File locations
4. File sizes
5. Next steps (legal review, approval, distribution)

**Example Output Summary:**
```
✅ 5 Policies Generated for [Company Name]

Generated Policies:
1. Acceptable Use Policy (Governance) - 2,100 words
2. Password Policy (Identity & Access) - 1,800 words
3. Data Classification Policy (Data Protection) - 2,700 words
4. Data Recovery Policy (Resilience) - 2,400 words
5. Information Security Policy (Governance) - 3,200 words

Formats Created:
✓ Markdown (.md) - 5 files
✓ Microsoft Word (.docx) - 5 files
✓ HTML (.html) - 5 files
✓ PDF (.pdf) - 5 files

Output Location: /path/to/output/
Total Size: ~15 MB

Next Steps:
1. Review policies for accuracy
2. Submit to legal counsel for review
3. Obtain executive approval
4. Distribute to employees
5. Schedule annual policy review
```

## Reference Materials

**Primary References:**
- `references/policies.json` - 51 complete policy templates (320KB, SANS + CIS)
- `references/buildingBlocks.json` - 169 reusable policy clauses
- `references/framework_mappings.md` - Complete guide to ISO 27001, SOC 2, NIST, CIS, GDPR mappings
- `references/policy_categories.md` - Descriptions of all 15 policy categories (51 policies organized)

**Supporting Materials:**
- `references/customization_guide.md` - Advanced customization techniques and best practices

## Output Format

**Generated Policy Document Structure:**

```markdown
# [Policy Title]

**Company:** [Organization Name]
**Version:** 1.0
**Effective Date:** [Date]
**Review Schedule:** [Frequency]
**Responsible Officer:** [Executive]
**Department:** [Department Name]
**Contact:** [Email]

---

## Purpose

[Customized purpose statement explaining why this policy exists]

## Scope

[Customized scope defining who and what this policy applies to]

## Policy

[Detailed policy content with organization-specific requirements]

### [Subsection 1]
[Policy details...]

### [Subsection 2]
[Policy details...]

## Compliance

This policy supports compliance with:
- ISO 27001: [Specific controls]
- SOC 2: [Trust Service Criteria]
- [Other applicable frameworks]

## Management Support

[Executive commitment statement]

## Review Schedule

This policy will be reviewed [frequency] by [responsible party].

## Exceptions

[Exception handling process]

## Responsibility

[Roles and responsibilities for policy enforcement]

---

**Approved by:** [Responsible Officer]
**Approval Date:** [Date]
**Next Review:** [Date]
```

**Additional Formats:**
- **Word (.docx):** Professional formatting with headers, footers, TOC
- **HTML (.html):** Styled for intranet with responsive CSS
- **PDF (.pdf):** Distribution-ready, archival quality

## Defensive Security Note

This skill generates **defensive security policy documentation**:
- ✅ Creates policies to protect organizational assets
- ✅ Supports compliance with security frameworks
- ✅ Promotes ethical security practices
- ✅ Helps establish security program foundation
- ❌ Does NOT create policies for offensive security
- ❌ Does NOT authorize penetration testing
- ❌ Does NOT promote malicious activities

All policies encourage responsible security practices, data protection, and compliance with regulations.

## Tools Available

**Scripts (Python 3.8+):**
- `scripts/browse_policies.py` - Browse, filter, search 51 policy templates
- `scripts/apply_customizations.py` - Replace placeholders with organization values
- `scripts/generate_markdown.py` - Create Markdown policy document
- `scripts/generate_docx_html_pdf.py` - Create Word, HTML, PDF documents

**All scripts analyze static template files only** and do NOT:
- Connect to live systems or networks
- Execute code or make network requests
- Access databases or servers
- Require credentials or system access

## Example Usage

### Example 1: Startup Needs Security Policies

```
User: "I'm a startup and need security policies for SOC 2 compliance"

Claude (using this skill):
1. Runs browse_policies.py --framework "SOC 2"
2. Shows 36 SANS policies that support SOC 2
3. Recommends starting with 5 foundational policies
4. Uses AskUserQuestion to collect company info
5. Generates all 5 policies in 4 formats each
6. Explains these form the foundation for SOC 2
```

### Example 2: Specific Policy Need

```
User: "I need an Incident Response Policy for ISO 27001"

Claude (using this skill):
1. Runs browse_policies.py --search "incident"
2. Shows Incident Response Management Policy (CIS)
3. Explains it covers ISO 27001 A.16 and CIS Control 17
4. Uses AskUserQuestion for customization
5. Generates policy in all 4 formats
6. Suggests related policies (Audit Log, Data Recovery)
```

### Example 3: Framework Compliance

```
User: "What policies do I need for CIS Controls?"

Claude (using this skill):
1. Runs browse_policies.py --source CIS
2. Shows all 15 CIS policies mapped to CIS Controls v8
3. References framework_mappings.md for control details
4. Helps prioritize by Implementation Group (IG1/IG2/IG3)
5. Generates policies in priority order
6. Provides framework compliance documentation
```

## Policy Selection Guidance

**For Security Program Foundation (Priority 1):**
1. Information Security Policy (Governance)
2. Acceptable Use Policy (Governance)
3. Password Policy (Identity and Access)
4. Data Classification Policy (Data Protection)
5. Data Recovery Policy (Resilience)

**For Compliance Projects:**
- **ISO 27001:** All 51 policies support ISO 27001
- **SOC 2:** 36 SANS policies cover all Trust Service Criteria
- **CIS Controls:** 15 CIS policies map directly to Controls v8
- **NIST CSF:** 15 CIS + 21 SANS policies cover all 5 functions

**By Category:** Governance (13), Identity and Access (8), Application (7), Compute (6), Network (4), Data Protection (2), and 9 others

## Limitations

- **Not legal advice:** Templates must be reviewed by qualified legal counsel
- **No compliance guarantee:** Policies support but don't certify compliance
- **Template-based only:** Uses existing templates, not custom authoring
- **No policy enforcement:** Generates documents only, doesn't implement controls
- **No automated updates:** Policies must be manually updated when regulations change
- **Requires professional review:** Legal, compliance, and executive approval needed
- **Static templates:** Based on SANS/CIS templates current as of 2023-2025

**When to consult professionals:** Legal review, compliance certification, custom requirements, industry-specific regulations, multi-jurisdictional compliance
