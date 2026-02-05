---
name: inbox-processor
description: This skill should be used when processing files in the inbox/ directory, organizing unstructured input, classifying content, or extracting actionable information. Triggered by requests like "process inbox", "organize inbox files", "classify this memo", or "inbox を整理".
---

# Inbox Processor

## Overview

Processes and organizes unstructured input files from the `inbox/` directory. Classifies content, extracts actionable information, and suggests appropriate destinations for integration into the research workflow.

## Core Capabilities

### 1. File Classification

Classify inbox files into categories based on content.

**Categories**:

1. **Meeting Notes**: Discussion records, decisions, action items
2. **Protocols**: Experimental procedures, SOPs
3. **Ideas**: Research ideas, hypotheses, brainstorming
4. **Data**: Raw data files, datasets
5. **Literature**: Papers, references, reading notes
6. **Miscellaneous**: Unclear or mixed content

**Workflow**:
1. Read file from `inbox/`
2. Analyze content to determine category
3. Extract key information
4. Suggest destination
5. Optionally move/process file

### 2. Information Extraction

Extract actionable information from unstructured content.

**What to extract**:

**From Meeting Notes**:
- Decisions made
- Action items (who, what, when)
- Key discussion points
- Follow-up questions

**From Protocols**:
- Procedure steps
- Required materials
- Expected outcomes
- Citations/sources

**From Ideas**:
- Core hypothesis
- Experimental approach
- Required resources
- Potential experiments

**From Literature**:
- Key findings
- Relevant methods
- Citations
- Relevance to current work

### 3. Destination Suggestions

Recommend where content should be integrated.

**Classification Rules** (from `references/classification-rules.md`):

| Content Type | Suggested Destination | Rationale |
|--------------|----------------------|-----------|
| Meeting notes | `notebook/knowledge/meeting_YYYY-MM-DD.md` | Reusable context |
| Protocol | `notebook/knowledge/protocol_[name].md` | Reusable procedure |
| Experiment idea | Create new lab notebook via `/research-exp` | Start experiment |
| Research hypothesis | Refine with `hypothesis-driven` skill | Improve quality |
| Raw data file | `data/raw/[filename]` | Data storage |
| Literature notes | `notebook/knowledge/literature_[topic].md` | Reference material |

### 4. Integration Actions

After classification, take appropriate action.

**Possible actions**:

1. **Move to knowledge/**:
   ```bash
   mv inbox/meeting_notes.txt notebook/knowledge/meeting_2025-01-15.md
   ```

2. **Create experiment**:
   ```
   Content suggests new experiment → Use /research-exp
   ```

3. **Add to STEERING.md**:
   ```
   Important decisions → Update priorities in STEERING.md
   ```

4. **Add to tasks.md**:
   ```
   Action items → Add to notebook/tasks.md
   ```

5. **Process for report**:
   ```
   Relevant findings → Note in ongoing report
   ```

6. **Archive**:
   ```bash
   mv inbox/old_file.txt inbox/archive/
   ```

## Usage Workflow

### Typical Usage

1. **User adds file to inbox/**:
   ```
   User: "I put meeting notes in inbox/team_meeting.md"
   ```

2. **Classify content**:
   ```
   Assistant reads file, determines category: Meeting Notes
   ```

3. **Extract information**:
   ```
   Decisions:
   - Approved Exp04 (ATAC-seq analysis)
   - Prioritize cell cycle validation

   Action items:
   - [User] Design primers for qPCR by Friday
   - [Collaborator] Share ChIP-seq data next week

   Discussion:
   - Considered three-prime seq vs bulk RNA-seq
   - Decided bulk more appropriate for current question
   ```

4. **Suggest destination**:
   ```
   Suggested destination: notebook/knowledge/meeting_2025-01-15.md
   Suggested actions:
   - Add primer design to tasks.md
   - Update STEERING.md with Exp04 approval
   - Plan to receive ChIP-seq data
   ```

5. **Implement (with user approval)**:
   ```
   Move file, update tasks.md, update STEERING.md
   ```

### Batch Processing

Process multiple inbox files:

```
User: "Process all files in inbox/"