---
name: us-tax-code
description: Complete US Internal Revenue Code (Title 26) with 2,160 sections covering individual income tax, business deductions, corporate tax, partnerships, international tax, capital gains, and all federal tax provisions. Search by section number or topic.
---

# US Tax Code (Title 26 - Internal Revenue Code)

Access the complete Internal Revenue Code with intelligent search and navigation. Query specific sections (e.g., "Section 162") or search by topic (e.g., "depreciation", "capital gains", "S corporations").

## How to Use This Skill

When the user asks about tax code sections:

1. **For specific sections** (e.g., "What does Section 162 say?"):
   - Read the file: `~/.claude/skills/us_tax_code_skill/data/section_162.md`
   - Section files are named: `section_{number}.md`

2. **For topic searches** (e.g., "What sections cover depreciation?"):
   - Read the index: `~/.claude/skills/us_tax_code_skill/data/index.json`
   - Search the `search_index` field for keywords
   - The index contains section numbers, headings, and cross-references

3. **For browsing**:
   - Use Glob to find sections: `~/.claude/skills/us_tax_code_skill/data/section_*.md`
   - Read the index.json to see all 2,160 sections with their headings

## Statistics
- **Total Sections**: 2,160
- **Coverage**: Complete Title 26 USC (Internal Revenue Code)
- **Last Updated**: September 2025

### Navigation Structure
The code is organized hierarchically:
- **Subtitles**: Major divisions (A through K)
- **Chapters**: Subdivisions within subtitles
- **Subchapters**: Further subdivisions
- **Parts**: Groupings of related sections
- **Sections**: Individual provisions of the law

## Common Sections Reference

### Individual Income Tax
- Section 1: Tax imposed (tax rates)
- Section 61: Gross income defined
- Section 62: Adjusted gross income defined
- Section 63: Taxable income defined
- Section 151-152: Personal exemptions

### Deductions
- Section 162: Trade or business expenses
- Section 163: Interest deduction
- Section 164: Taxes (SALT deduction)
- Section 165: Losses
- Section 167: Depreciation
- Section 168: Accelerated cost recovery system (MACRS)
- Section 170: Charitable contributions
- Section 179: Election to expense certain property

### Business Entities
- Section 301-385: Corporate distributions and adjustments
- Section 701-777: Partners and partnerships
- Section 1361-1379: S Corporations

### International Tax
- Section 482: Transfer pricing
- Section 861-865: Source rules
- Section 901-909: Foreign tax credits
- Section 951-965: Subpart F (CFC rules)

### Capital Gains
- Section 1001-1092: Determination of capital gains and losses
- Section 1221-1223: Capital assets defined
- Section 1231: Property used in trade or business

## Search Index
The skill includes a pre-built search index for common tax terms. Access via:
```python
index = load_index()
```

## Cross-Reference Resolution
Sections often reference other sections. Use:
```python
refs = get_cross_references("482")
```

## Notes
- This skill contains the complete Internal Revenue Code as of the last download
- The tax code is complex and interrelated - always check cross-references
- For regulatory guidance, see Treasury Regulations (not included)
- For current year changes, check recent legislation

## File Structure
```
us_tax_code_skill/
├── SKILL.md (this file)
├── data/
│   ├── section_*.md (individual sections)
│   └── index.json (master index)
├── scripts/
│   ├── search.py (search functionality)
│   └── loader.py (section loader)
└── references/
    └── common_forms.md (mapping to IRS forms)
```
