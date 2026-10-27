---
name: issue-md-writer
description: "Create and draft markdown-based issue documents (bug reports, feature plans, RFCs, ADRs, tasks, retrospectives) in the top-level `.issues/` folder. Use this skill whenever you need to document software issues, feature proposals, architectural decisions, work items, or post-mortems. Includes templates, metadata indexing, and structured YAML frontmatter. Different from issue tracker systems — this is for archival, decision-making, and knowledge base documents."
metadata: 
  version: 2.2.0
  author: arisng
---

# MD Issue Writer

## Overview

This skill enables the creation of concise, one-page technical documents for software issues, features, decisions, and work items. Each document follows a standardized YAML frontmatter and markdown structure, making them discoverable and indexable across the knowledge base.

## When to Use Each Document Type

Use this decision tree to select the right template:

| **Situation** | **Document Type** | **Purpose** |
|---|---|---|
| Something broke or isn't working | **Bug Report** | Root cause analysis, prevention, lessons learned |
| Build/ship a new capability | **Feature Plan** | Goals, requirements, implementation approach, risks |
| Need consensus on architectural direction | **RFC** | Proposal, motivation, design, alternatives, Q&A |
| Made a major technical decision | **ADR** | Document the decision, context, and consequences |
| Have specific work to accomplish | **Task** | Objectives, acceptance criteria, checklist |
| Learned something from an incident/project | **Retrospective** | What happened, what went well, lessons, actions |

## Workflow

1. **Choose the document type** using the decision tree above or by reviewing the templates in `templates/`.
2. **Gather required metadata**: title, description, severity (if applicable), status, author (if applicable).
3. **Generate the document** using the provided script or by copying a template into the new `.issues/` directory (it will be created automatically).
4. **Fill in the content** following the template structure.
5. **(Optional) Index all documents** by running the metadata extraction script to keep the central index current.

## Usage

Create a new issue document via script:

```bash
python scripts/create_issue.py --type "Bug" --title "Fix login timeout" --description "Users are logged out after 5 minutes" --severity "High"
```

Or copy a template directly:

```bash
cp templates/<type>.md .issues/<date>_<slug>.md
```

To extract metadata and regenerate the index of all issues:

```bash
python scripts/extract_issue_metadata.py
```

## Template Reference

Each issue type has its own reference file in `templates/`:

- **bug-report.md** — Incident analysis with root cause, solution, and prevention steps
- **feature-plan.md** — Feature proposal with goals, requirements, and implementation approach
- **rfc.md** — RFC proposal with motivation, design, alternatives, and open questions
- **adr.md** — Architecture decision record for major technical choices
- **task.md** — Work item with objectives, acceptance criteria, and references
- **retrospective.md** — Post-incident or post-project learning document

See `templates/index.md` for a complete overview and quick-reference guide.

## Resources

### scripts/
- `create_issue.py` — Generate issue documents based on templates
- `extract_issue_metadata.py` — Extract metadata and regenerate the index

### templates/
- `index.md` — Quick reference and overview of all template types
- `bug-report.md`, `feature-plan.md`, `rfc.md`, `adr.md`, `task.md`, `retrospective.md` — Individual templates
