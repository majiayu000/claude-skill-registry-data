---
name: construction-bd-skill
description: >-
  Construction business development knowledge — proposal summarization,
  quotations with cost categories, industry terminology, Atlassian workflows.
license: Apache-2.0
compatibility: opencode
category: Startup/Business
---

# Construction Business Development Skill

## Proposal Summarization Workflow

When summarizing construction proposals, extract and organize information by the following categories:

1. **Project Overview and Objectives**
   - Project type (commercial, residential, industrial, infrastructure)
   - Primary goals and success criteria
   - Scope of work boundaries
   - Client expectations and deliverables

2. **Technical Specifications and Requirements**
   - Architectural and engineering specifications
   - Building codes and compliance requirements
   - Quality standards and certifications (LEED, OSHA, etc.)
   - Technical constraints and site conditions

3. **Material and Resource Needs**
   - Primary materials (concrete, steel, lumber, fixtures, etc.)
   - Equipment requirements (cranes, excavators, specialized tools)
   - Labor classifications (skilled, unskilled, supervision)
   - Subcontractor needs (electrical, plumbing, HVAC, MEP)

4. **Timeline and Milestones**
   - Project phases and sequencing
   - Critical path and dependencies
   - Mobilization and demobilization schedules
   - Delivery deadlines and milestone dates

5. **Stakeholders and Responsibilities**
   - Client representatives
   - Project managers and superintendents
   - Subcontractors and vendors
   - Regulatory bodies and permitting authorities

6. **Risk Factors and Mitigation Strategies**
   - Site-specific risks (weather, access, soil conditions)
   - Supply chain considerations
   - Regulatory and permitting risks
   - Safety and compliance concerns

## Quotation Preparation Workflow

### Cost Category Breakdown

When preparing construction quotations, organize costs into these standard categories:

1. **Materials**
   - Raw materials (concrete, steel, lumber, aggregates)
   - Finished products (windows, doors, fixtures)
   - Specialized components (MEP systems, FF&E)
   - Quantity takeoffs and unit pricing

2. **Labor**
   - Skilled trades (carpenters, electricians, plumbers, welders)
   - Unskilled labor
   - Supervision (foremen, superintendents, project managers)
   - Man-hour estimates by trade

3. **Equipment**
   - Rental costs (cranes, excavators, scaffolding)
   - Purchase costs for permanent equipment
   - Fuel and maintenance
   - Mobilization and demobilization fees

4. **Subcontractors**
   - Electrical work
   - Plumbing and mechanical
   - HVAC systems
   - Specialized trades (fire protection, elevators)

5. **Permits and Inspections**
   - Building permits
   - Environmental assessments
   - Inspection fees
   - Plan review costs

6. **Insurance and Bonding**
   - General liability insurance
   - Workers' compensation
   - Performance bonds
   - Bid bonds

7. **Overhead**
   - Office operations
   - Administrative support
   - Utilities and facilities
   - Project management software

8. **Markup and Profit**
   - Standard markup (typically 15-25%)
   - Contingency (typically 10-20%)
   - Profit margin calculations
   - Per Diem rates for travel

### Pricing Standards

- Use current market rates obtained via web search
- Research regional pricing variations
- Consider prevailing wage requirements
- Include appropriate unit price or lump sum structures
- Apply mobilization/demobilization costs separately

## Construction Industry Terminology

### Procurement and Bidding Terms
- **RFI (Request for Information)**: Formal request for clarification on project specifications
- **RFP (Request for Proposal)**: Detailed solicitation for vendor proposals
- **RFQ (Request for Quotation)**: Request for pricing on specific materials or services

### Contract Management Terms
- **Change Order**: Formal modification to contract scope, price, or schedule
- **Punch List**: Final list of items requiring correction before project acceptance
- **Submittal**: Formal submission of materials, samples, or drawings for approval
- **Shop Drawings**: Detailed drawings prepared by contractors showing specific installation details
- **Value Engineering**: Systematic review to reduce costs without compromising quality

### Certification and Compliance Terms
- **LEED Certification**: Leadership in Energy and Environmental Design green building certification
- **OSHA Compliance**: Occupational Safety and Health Administration safety standards
- **Prevailing Wage**: Government-mandated wage rates for public projects

### Construction Methods Terms
- **Crane Lift Plans**: Detailed engineering plans for heavy lifting operations
- **Shoring/Underpinning**: Temporary support structures for excavation or foundation work
- **MEP (Mechanical, Electrical, Plumbing)**: Building systems integration
- **HVAC (Heating, Ventilation, Air Conditioning)**: Climate control systems
- **FF&E (Furniture, Fixtures, Equipment)**: Non-permanent building components

### Delivery Methods Terms
- **Turnkey Delivery**: Contractor handles all aspects from design to completion
- **Design-Bid-Build**: Traditional sequential delivery method
- **Design-Build**: Integrated design and construction approach
- **CM at Risk (Construction Manager at Risk)**: Construction manager with guaranteed maximum price
- **GMP (Guaranteed Maximum Price)**: Fixed price contract with shared savings potential

### Pricing Structure Terms
- **Unit Price**: Price based on quantity of work (e.g., per linear foot)
- **Lump Sum**: Fixed price for entire scope of work
- **Mobilization/Demobilization**: Costs associated with bringing equipment to/from site
- **Per Diem**: Daily allowance for travel and living expenses

## Atlassian Integration Workflow

### JIRA Ticket Creation

Create JIRA tickets with the following field mapping:

1. **Basic Fields**
   - Project: BD (Business Development)
   - Issue Type: Task or Story
   - Summary: "[Proposal/Quotation] - Client Name - Project Name"
   - Description: Include comprehensive summary with:
     * Document overview
     * Key specifications extracted
     * Cost breakdown summary
     * Timeline and milestones
     * Stakeholder information
   - Priority: Set based on urgency and deal value
   - Labels: Add relevant tags (construction, proposal, quotation, client-name)

2. **Custom Fields**
   - Client Name: Text field
   - Estimated Value: Currency field
   - Project Type: Dropdown (commercial, residential, industrial, infrastructure)
   - Due Date: Date picker
   - Document Type: Dropdown (proposal, quotation, RFQ, RFP)
   - Status: Dropdown (draft, submitted, under-review, awarded, lost)

3. **Attachments**
   - Generated .docx files
   - Generated .md files
   - Original technical documents
   - Supporting calculations and schedules

### Confluence Page Creation

Create Confluence pages with proper structure:

1. **Page Setup**
   - Space: BD (Business Development) or client-specific space
   - Title: "Client Name - Project Name - Proposal/Quotation"
   - Parent Page: Organize by client or project phase

2. **Content Structure**
   - Executive Summary
   - Project Overview
   - Technical Specifications
   - Cost Breakdown Table
   - Timeline and Milestones
   - Stakeholder Information
   - Risk Assessment
   - Supporting Documents section with links

3. **Linking and Metadata**
   - Link to JIRA ticket using JIRA macro
   - Add appropriate labels for filtering
   - Set page restrictions as needed
   - Include version history for tracking changes

4. **Document Formatting**
   - Use table of contents macro for navigation
   - Include expand/collapse sections for detailed specifications
   - Use status macros to track document state
   - Add page properties macro for metadata

## Document Generation Specifications

### Word (.docx) Format Requirements

1. **Document Structure**
   - Cover page with company branding
   - Executive summary
   - Table of contents
   - Main content sections
   - Appendices for technical details
   - Terms and conditions

2. **Formatting Standards**
   - Professional header/footer with company logo
   - Consistent font styling (headings, body text)
   - Proper table formatting with borders and shading
   - Numbered sections and subsections
   - Page numbering

3. **Content Elements**
   - Professional tables for cost breakdowns
   - Inserted images (plans, drawings, charts)
   - Multi-level lists for specifications
   - Bold emphasis for key terms and figures
   - Professional terminology throughout

### Markdown (.md) Format Requirements

1. **Document Structure**
   - Heading hierarchy (H1, H2, H3)
   - Code blocks for technical specifications
   - Tables for cost breakdowns
   - List items for requirements

2. **Formatting Standards**
   - Consistent heading levels
   - Proper table formatting with alignment
   - Links to external references
   - Emphasis (bold, italic) for key points

3. **Content Elements**
   - Markdown tables for itemized costs
   - Code blocks for technical specifications
   - Ordered lists for requirements
   - Checklists for deliverables
   - Links to supporting documents

## Web Search Usage for Market Rates

When researching construction pricing:

1. **Search Strategies**
   - Use specific queries: "material prices [region] [year]"
   - Include units: "concrete per cubic yard [city]"
   - Search by trade: "electrical labor rates [state]"
   - Include timeframe: "current steel prices 2026"

2. **Data Sources**
   - Industry publications and databases
   - Government cost indices
   - Supplier price lists
   - Regional contractor associations

3. **Validation Steps**
   - Cross-reference multiple sources
   - Verify regional applicability
   - Check for recent market fluctuations
   - Consider bulk vs. retail pricing

4. **Documentation**
   - Note sources and dates
   - Record geographic scope
   - Track price trends
   - Maintain pricing database

## Error Handling

### Web Search Errors

- **No pricing data found**: Document the gap and suggest manual research
- **Conflicting information**: Note discrepancies and recommend verification
- **Outdated data**: Check dates and flag for updates
- **Regional mismatch**: Specify location constraints

### JIRA Integration Errors

- **Field mapping failures**: Provide clear error messages with field names
- **Attachment size limits**: Suggest splitting documents or using cloud storage
- **Permission issues**: Recommend user authentication checks
- **API rate limits**: Suggest batching or retry with delays
- **Manual workaround**: Provide step-by-step instructions for manual ticket creation

### Confluence Integration Errors

- **Space access issues**: Verify permissions and suggest alternative spaces
- **Page title conflicts**: Recommend adding dates or unique identifiers
- **Formatting failures**: Suggest markdown-only fallback
- **Link creation errors**: Provide manual linking instructions

### Document Generation Errors

- **Word formatting issues**: Fall back to markdown-only format
- **Table rendering problems**: Use simplified table structures
- **Image insertion failures**: Provide alternative text descriptions
- **File size limits**: Compress images or split into multiple documents

### General Error Recovery

- Always preserve original technical documents
- Maintain error logs for troubleshooting
- Provide clear user-facing error messages
- Offer alternative workflows when automated steps fail
- Document manual steps as fallback procedures
- Validate data integrity before finalizing
- Maintain version control for all generated documents

## Best Practices

1. **Accuracy and Quality**
   - Double-check all calculations
   - Verify technical specifications against source documents
   - Use current market rates and validate sources
   - Maintain professional formatting and branding

2. **Consistency and Standardization**
   - Use consistent terminology throughout all documents
   - Follow standard construction cost categorization
   - Maintain uniform document structures
   - Apply consistent pricing methodologies

3. **Communication and Tracking**
   - Include clear disclaimers and terms of service
   - Track all documents in Atlassian systems
   - Provide complete audit trails
   - Maintain version history for revisions

4. **Documentation Management**
   - Store all source documents for reference
   - Maintain organized file naming conventions
   - Keep pricing research records
   - Archive completed projects appropriately

5. **Industry Compliance**
   - Adhere to local building codes and regulations
   - Follow safety standards (OSHA, etc.)
   - Comply with prevailing wage requirements
   - Include necessary permit and inspection information