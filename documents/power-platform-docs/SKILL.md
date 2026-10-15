---
name: power-platform-docs
description: "Generate IT documentation for Power Platform solutions: user guides (Canvas/Model-driven app end users) and technical guides (admins, developers) for apps, flows, Dataverse. Triggers: app documentation, user manual, technical spec, deployment guide, flow or data model docs."
---

# Power Platform Documentation Generator

Generate professional documentation for Power Platform solutions applying Microsoft Writing Style Guide, Diátaxis framework, C4 model, and accessibility standards.

## Parameters

Gather these before generating:

| Parameter | Required | Values | Default |
|-----------|----------|--------|---------|
| `document_type` | Yes | `user_guide`, `technical_guide` | - |
| `solution_name` | Yes | string | - |
| `target_audience` | Yes | `end_user`, `it_admin`, `developer`, `all` | - |
| `app_type` | If user_guide | `canvas_app`, `model_driven_app`, `mixed` | - |
| `includes_flows` | Recommended | boolean | true |
| `includes_dataverse` | If technical_guide | boolean | true |
| `technical_depth` | If technical_guide | `overview`, `standard`, `detailed` | `standard` |
| `version` | No | string | "1.0" |

## Decision Logic

```
IF document_type == "user_guide":
    → Load references/user-guide-standards.md
    IF app_type == "canvas_app":
        → Screen-by-screen navigation structure
        → Annotated screenshot placeholders per screen
        → Procedural how-to focus
    ELIF app_type == "model_driven_app":
        → Business-process-oriented structure
        → Data entry and workflow procedures
        → Site map navigation reference
    
    IF includes_flows:
        → Add "What happens automatically" section
        → Document triggers users should know about
    
    ALWAYS include: Quick Start, Troubleshooting, FAQ, Contact Support

IF document_type == "technical_guide":
    → Load references/technical-guide-standards.md
    IF technical_depth == "overview":
        → Context diagram only
        → High-level component descriptions
    ELIF technical_depth == "standard":
        → Context + Container diagrams
        → Configuration reference
        → Deployment procedures
    ELIF technical_depth == "detailed":
        → Full C4 diagram set
        → API reference if applicable
        → Code samples, performance tuning
    
    IF includes_dataverse:
        → Load references/power-platform-specifics.md (Dataverse section)
        → Data model section with ERD placeholder
        → Table/column documentation templates
        → Security model section
    
    IF includes_flows:
        → Load references/power-platform-specifics.md (Flow section)
        → Flow documentation with error handling
    
    ALWAYS include: Architecture, Configuration, Deployment, Change Log
```

## Generation Workflow

1. **Gather parameters** - Ask only what's needed based on document_type
2. **Load relevant references** - Read only the reference files needed per decision logic
3. **Generate metadata block** - Use YAML frontmatter format from standards
4. **Generate structure** - Apply mandatory sections from standards
5. **Apply writing rules** - Active voice, present tense, ≤20 word sentences
6. **Insert placeholders** - Screenshots, diagrams, tables per standards
7. **Validate** - Run through references/quality-checklist.md

## Output Format

Always start with metadata block:

```markdown
---
title: [Document Title]
version: [X.Y.Z]
status: Draft
created: [YYYY-MM-DD]
modified: [YYYY-MM-DD]
author: [Name]
audience: [End User | IT Admin | Developer]
---
```

## Writing Rules (Always Apply)

- **Voice**: Second person ("you"), active voice, present tense
- **Sentences**: ≤20 words, one idea per sentence
- **Procedures**: ≤12 steps, conditions before instructions
- **Headings**: Sentence case only
- **UI elements**: Bold (Click **Save**)
- **Technical terms**: Code font (`tableName`)
- **Readability**: Grade 7-9 Flesch-Kincaid for user guides

## Terminology (Power Platform)

| Use | Not |
|-----|-----|
| Canvas app | Canvas Power App |
| Model-driven app | Model-driven Power App |
| Dataverse | CDS, Common Data Service |
| Power Automate | Flow (in new docs) |
| Environment | Instance, tenant |

## References

Load as needed per decision logic:

- `references/user-guide-standards.md` - Sections, troubleshooting format, FAQ structure
- `references/technical-guide-standards.md` - C4 model, configuration, deployment, versioning
- `references/power-platform-specifics.md` - Canvas, model-driven, flows, Dataverse patterns
- `references/quality-checklist.md` - Validation before delivery
