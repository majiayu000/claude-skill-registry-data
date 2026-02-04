---
name: draftify-ppt
description: This skill generates planning documents (기획서) in PowerPoint format from analyzed screen data and project artifacts. It should be used by the auto-draft-orchestrator agent during Phase 4 to create the final PPT output. Not intended for direct user invocation.
---

# Draftify PPT Generator

## Overview

This skill transforms analyzed project data into a structured PowerPoint planning document (기획서) following the standard 10-section format. It is invoked by the auto-draft-orchestrator during Phase 4 of the document generation workflow.

## Input Requirements

The skill expects the following files to exist in the project's output directory:

```
outputs/<project-name>/
├─ screenshots/                    # Captured screen images
├─ analysis/
│  └─ analyzed-structure.json      # Consolidated analysis data
├─ sections/
│  ├─ 05-glossary.md               # 용어 정의
│  ├─ 06-policy-definition.md      # 정책 정의
│  ├─ 07-process-flow.md           # 프로세스 흐름
│  └─ 08-screen-definition.md      # 화면 정의
└─ validation/
   └─ validation-report.md         # Quality validation results
```

## Output

Generates `final-draft.pptx` in the project output directory:

```
outputs/<project-name>/
└─ final-draft.pptx
```

## Document Structure

The generated PPT follows the 10-section structure defined in `references/auto-draft-guideline.md`:

| Section | Content |
|---------|---------|
| 1. 표지 | Cover with project metadata |
| 2. 변경 이력 | Revision history table |
| 3. 목차 | Table of contents with screen IDs |
| 4. 섹션 타이틀 | Section divider pages |
| 5. 용어 정의 | Glossary terms from `05-glossary.md` |
| 6. 정책 정의 | Policies with POL-* IDs from `06-policy-definition.md` |
| 7. 프로세스 흐름 | Process flow from `07-process-flow.md` |
| 8. 화면 정의 | Screen definitions with SCR-* IDs from `08-screen-definition.md` |
| 9. 참고 문헌 | Reference documents |
| 10. EOD | End of document marker |

## Generation Workflow

1. **Read analyzed data**: Load `analyzed-structure.json` and section markdown files
2. **Parse screen definitions**: Extract screen metadata, screenshots, and element definitions
3. **Generate cover slide**: Use project name, version, and current date
4. **Generate TOC**: Create clickable table of contents
5. **Generate section slides**: Process each section markdown into slides
6. **Insert screenshots**: Embed captured screenshots in screen definition slides
7. **Apply template styling**: Use `assets/ppt_template.pptx` as base
8. **Save output**: Write `final-draft.pptx`

## ID Scheme Compliance

All IDs must follow the scheme defined in the guideline:

- **Policy IDs**: `POL-{CATEGORY}-{SEQ}` (e.g., POL-AUTH-001)
- **Screen IDs**: `SCR-{SEQ}` (e.g., SCR-001)
- **Element IDs**: `{TYPE}-{SEQ}` (e.g., BTN-001, FORM-001)
- **API IDs**: `API-{SEQ}` (e.g., API-001)

## Screen Definition Slide Layout

Each screen definition uses 1-2 slides with this structure:

**Slide 1 (Required)**:
- Screen ID and name (header)
- Screenshot image (left 60%)
- Basic info panel (right 40%): purpose, entry/exit conditions

**Slide 2 (If needed)**:
- UI element table
- Process flow within screen
- Related policies (POL-* references)

## Usage by Orchestrator

The auto-draft-orchestrator invokes this skill via Task tool:

```
Task: Generate final PPT document
Input: outputs/<project-name>/ directory path
Timeout: 10 minutes
```

## Error Handling

- **Missing section files**: Generate placeholder slide with warning
- **Missing screenshots**: Use placeholder image with screen ID
- **Invalid IDs**: Log warning, continue generation
- **Template errors**: Fall back to basic slide layout

## Resources

### scripts/
- `generate_ppt.py`: Main PPT generation script using python-pptx

### references/
- `auto-draft-guideline.md`: Complete specification for document structure and ID schemes

### assets/
- `ppt_template.pptx`: PowerPoint template with predefined layouts and styling
- `JOURNEYITSELF-BOLD 3.TTF`: Bold font for headers
- `JOURNEYITSELF-REGULAR 3.TTF`: Regular font for body text
- `JOURNEYITSELF-LIGHT 3.TTF`: Light font for captions

## Dependencies

- Python 3.8+
- python-pptx library
- Pillow (for image processing)
