---
name: filling-pdf-forms
description: Complete PDF forms by collecting data through conversational interviews and populating form fields. Use when filling forms, completing documents, or when the user mentions PDFs, forms, form completion, or document population.
allowed-tools: Read, Write, Edit, Glob, Bash, Task
version: 1.0.0a2
license: Apache 2.0
---

# Filling PDF Forms

Complete PDF forms by collecting required data through conversational interviews and populating form fields.

<purpose>
Use when completing PDF forms with user-provided data. Goal: produce `.done.pdf` populated with user information by following this process exactly.
</purpose>

## Process Overview

```plantuml
@startuml SKILL
title Filling PDF Forms - High-Level Workflow
|User|
start
:User provides PDF form to complete;
|filling-pdf-forms skill|
:Step 0: Initialize Chatfield;
:Step 1: Form Extraction;
:Step 2: Build Form Data Model;
:Step 3: Translation Decision;
if (User language is form language?) then (yes)
  :Use base Form Data Model;
else (no)
  :Translation Setup;
endif
:Step 4: Run Interview Loop;
partition "Chatfield CLI Interview Loop" {
  :Initialize: Run CLI without message;
  repeat
    :CLI outputs question to stdout;
    :Present question to user via AskUserQuestion();
    |User|
    :User provides response;
    |filling-pdf-forms skill|
    :Run CLI with user's message;
  repeat while (CLI indicates complete?) is (no)
  ->yes;
}
:Inspect collected data via CLI --inspect;
:Step 5: Populate PDF;
if (Fillable form?) then (yes)
  :Populate fillable fields
  (see Populating-Fillable.md);
else (no)
  :Populate non-fillable fields
  (see Populating-Nonfillable.md);
endif
|User|
:**✓ SUCCESS**;
:Receive completed PDF <basename>.done.pdf;
stop
@enduml
```

## Workflow

### Step 0: Initialize Chatfield

Test: `python -c "import pypdf; import pdf2image; import markitdown; import chatfield"`.

Install via `pip` if needed; exceptions:
- `markitdown` → `pip install "markitdown[pdf]"`
- `chatfield` → `pip install ./scripts/chatfield-1.0.0a2-py3-none-any.whl` (relative to this .md)

### Step 1: Form Extraction

Extract PDF form using `extracting-form-fields` sub-agent:

```python
Task(
    subagent_type="general-purpose",
    description="Extract PDF form fields",
    prompt=f"Extract form field data from PDF: {pdf_path}\n\nUse the extracting-form-fields skill."
)
```

**Task reports**: "fillable" or "non-fillable" (needed for Step 5)

**Creates** (for `input.pdf`):
- `input.chatfield/input.form.md` - PDF as Markdown
- `input.chatfield/input.form.json` - Field definitions
- `input.chatfield/interview.py` - Template Form Data Model

### Step 2: Build Form Data Model

1. Read entirely: `./references/Data-Model-API.md` - Learn Chatfield API
2. Read entirely: `./references/Converting-PDF-To-Chatfield.md` - PDF→Chatfield Form Data Model guidance
3. Edit `<basename>.chatfield/interview.py` - Define Form Data Model

**Result**: The **Form Data Model**, a faithful representation of PDF form using Chatfield API.

### Step 3: Translation

Determine if translation is needed. Translation is needed either:
- **Explicit**: User states "I need to fill this Spanish form but I only speak English"
- **Implicit**: User request is in language X, but PDF is in language Y

Example: "Help me complete form.es.pdf" (English request, Spanish form)

State to the user whether you will translate. Either:
- Claude: This form uses <common-language>
- or Claude: This form uses <form-language> so I will set up translation to <user-language>

**To apply translation, see:** ./references/Translating.md

Translation creates `interview_<lang>.py` and **re-defines** the Form Data Model from `interview.py` to the new `interview_<lang>.py` instead. Henceforth, use the translated file as the Form Data Model.

### Step 4: Run Interview Loop via CLI

**CRITICAL**: See `./references/CLI-Interview-Loop.md` for complete MANDATORY execution rules.


### Step 5: Populate PDF

Parse `--inspect` output and populate the PDF.

#### If Fillable:

**See:** ./references/Populating-Fillable.md

#### If Non-fillable:

**See:** ./references/Populating-Nonfillable.md

**Result**: `<basename>.done.pdf`
