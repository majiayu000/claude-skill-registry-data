---
name: visa
description: Visa application guidance with document tracking and timeline management. Use when user mentions travel visas, visa applications, visa documents, consulate interviews, or entry requirements. Identifies correct visa type, builds document checklists, manages timelines, prepares for interviews, and tracks application status. NEVER guarantees visa approval.
---

# Visa

Visa navigation system. Get the right visa, get it right.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All visa data stored locally only**: `memory/visa/`
- **No government systems** connected
- **No document uploads** to external services
- **No application submission** through this skill
- User controls all data retention and deletion

### Safety Boundaries
- ✅ Identify visa types and requirements
- ✅ Build document checklists
- ✅ Track application timelines
- ✅ Prepare for interviews
- ❌ **NEVER guarantee** visa approval
- ❌ **NEVER replace** licensed immigration attorneys
- ❌ **NEVER submit** applications on your behalf

### Data Structure
Visa data stored locally:
- `memory/visa/applications.json` - Active applications
- `memory/visa/documents.json` - Document checklist and status
- `memory/visa/timelines.json` - Application timelines and deadlines
- `memory/visa/interview_prep.json` - Interview preparation
- `memory/visa/requirements.json` - Country-specific requirements

## Core Workflows

### Identify Visa Type
```
User: "What visa do I need for Germany?"
→ Use scripts/identify_visa.py --country Germany --purpose work --duration 6months
→ Analyze situation, recommend visa category
```

### Build Document Checklist
```
User: "What documents do I need for Schengen visa?"
→ Use scripts/build_checklist.py --visa schengen --nationality US
→ Generate complete document list with specifications
```

### Track Timeline
```
User: "Track my visa application"
→ Use scripts/track_timeline.py --application-id "VISA-123"
→ Show deadlines, upcoming actions, document expiry alerts
```

### Prepare for Interview
```
User: "Prep me for my visa interview"
→ Use scripts/prep_interview.py --visa-type work --country Canada
→ Generate likely questions and recommended responses
```

### Log Application
```
User: "I submitted my application today"
→ Use scripts/log_application.py --country Japan --visa-type tourist --submission-date 2024-03-01
→ Track application with timeline and reminders
```

## Module Reference
- **Visa Types**: See [references/visa-types.md](references/visa-types.md)
- **Document Checklists**: See [references/documents.md](references/documents.md)
- **Timeline Management**: See [references/timelines.md](references/timelines.md)
- **Interview Preparation**: See [references/interview.md](references/interview.md)
- **Denied Applications**: See [references/denials.md](references/denials.md)
- **Entry Requirements**: See [references/entry-requirements.md](references/entry-requirements.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `identify_visa.py` | Identify correct visa type |
| `build_checklist.py` | Generate document checklist |
| `track_timeline.py` | Track application timeline |
| `prep_interview.py` | Prepare for visa interview |
| `log_application.py` | Log new application |
| `check_deadlines.py` | Check upcoming deadlines |
| `compare_visas.py` | Compare visa options |
| `document_status.py` | Check document status |
