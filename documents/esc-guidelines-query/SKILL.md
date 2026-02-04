---
name: esc-guidelines-query
description: Query ESC (European Society of Cardiology) Guidelines by automatically locating the relevant PDF from the TOC and extracting cited answers. Use when answering clinical questions about cardiovascular diseases based on official ESC recommendations.
---

# ESC Guidelines Query System

Expert system for querying ESC Guidelines with automatic PDF location and citation extraction.

## When to Use This Skill

- Answering clinical cardiovascular questions
- Finding ESC recommendations on specific conditions
- Extracting diagnostic or therapeutic guidelines
- Locating specific ESC criteria or thresholds
- Comparing recommendations across different ESC guidelines
- Verifying treatment protocols against ESC standards

## Core Workflow

This skill implements a **3-phase intelligent retrieval system**:

### Phase 1: TOC Analysis (Locate)
**Goal**: Identify which ESC guideline PDF contains the relevant information

**Process**:
1. **Read** the master index: `ESC_GUIDELINES_TOC.md`
2. **Analyze** the user's clinical question to extract:
   - Medical condition (e.g., "aortic aneurysm", "atrial fibrillation")
   - Specific aspect (e.g., "imaging", "treatment threshold", "follow-up")
   - Clinical context (e.g., "45mm diameter", "pregnancy", "diabetes")
3. **Search** the TOC using Grep with relevant keywords
4. **Identify** the specific PDF file and page/section numbers

**Example TOC Analysis**:
```markdown
User Question: "Si deve fare TAC se uno ha 45mm di aortic root?"

Keywords to search: aortic root, imaging, CT, TAC, surveillance, thoracic aorta, 45mm

TOC Result:
- File: 2024_Peripheral_Arterial_Aortic.pdf
- Section: 9.2.2 Thoracic aortic aneurysms (p. 66)
- Subsection: 9.2.2.4 Surveillance (p. 70)
- Imaging section: 5.4 Evaluation of the aorta (p. 25)
```

### Phase 2: PDF Extraction (Read)
**Goal**: Read the specific sections from the identified PDF

**Process**:
1. **Open** the PDF file identified in Phase 1
2. **Navigate** to the specific sections/pages from the TOC
3. **Extract** relevant content including:
   - Recommendations (with class/level of evidence)
   - Diagnostic criteria
   - Threshold values
   - Imaging protocols
   - Follow-up schedules
4. **Capture** exact quotes for citation

**Reading Strategy**:
```markdown
Priority reading order:
1. Main section related to the question
2. Imaging/diagnostic section if relevant
3. Management/treatment section
4. Surveillance/follow-up section
5. Special populations section if applicable
```

### Phase 3: Answer Synthesis (Cite)
**Goal**: Provide accurate answer with proper citations

**Required Elements**:
1. ✅ **Direct answer** to the user's question
2. ✅ **ESC Recommendation** (Class I/IIa/IIb/III, Level A/B/C)
3. ✅ **Exact citation** (PDF file, section, page number)
4. ✅ **Clinical context** (thresholds, conditions, exceptions)
5. ✅ **Related information** (surveillance intervals, imaging modality choice)

**Citation Format**:
```markdown
**ESC Recommendation** [Class I, Level B]:
"[Exact quote from PDF]"

**Source**: [2024_Peripheral_Arterial_Aortic.pdf] - Section 9.2.2.4 (p. 70)
```

## Implementation Protocol

### Step-by-Step Execution

```markdown
## Phase 1: Locate (TOC Analysis)

1. **Parse User Question**
   - Extract: condition, aspect, context
   - Identify: relevant keywords for search

2. **Search TOC**
   ```bash
   Grep pattern: [keywords from question]
   File: ESC_GUIDELINES_TOC.md
   Mode: content with context
   ```

3. **Identify Target PDF**
   - PDF filename: [extracted from TOC]
   - Section numbers: [from TOC structure]
   - Page numbers: [from TOC annotations]

## Phase 2: Read (PDF Extraction)

4. **Open Target PDF**
   ```bash
   Read: references/esc-guidelines/[PDF_filename].pdf
   Focus: Sections identified in Phase 1
   ```

5. **Extract Relevant Content**
   - Recommendations boxes/tables
   - Diagnostic criteria
   - Threshold values
   - Imaging protocols
   - Follow-up schedules

6. **Capture Exact Quotes**
   - Copy verbatim text for citations
   - Note recommendation class/level
   - Record page numbers

## Phase 3: Cite (Answer Synthesis)

7. **Structure Answer**
   - Direct response to question
   - ESC recommendation with class/level
   - Exact citation with source
   - Clinical context and nuances

8. **Format Output**
   - Use markdown for clarity
   - Include tables if comparing options
   - Link to PDF file
   - Provide page references
```

## Output Template

```markdown
# [Clinical Question]

## ESC Recommendation

**[Recommendation Class & Level]**: [Brief summary]

"[Exact quote from ESC Guidelines]"

## Clinical Context

- **Threshold/Criteria**: [Specific values]
- **Imaging Modality**: [Recommended method]
- **Surveillance**: [Follow-up interval]
- **Special Considerations**: [Risk factors, comorbidities]

## When to [Action]

| Condition | Recommendation | Evidence |
|-----------|----------------|----------|
| [Scenario 1] | [Action] | Class [X], Level [Y] |
| [Scenario 2] | [Action] | Class [X], Level [Y] |

## Source Citation

**PDF**: [[PDF_filename].pdf](references/esc-guidelines/[PDF_filename].pdf)
**Section**: [Section number and title]
**Pages**: [Page numbers]

## Additional Recommendations

[Related information from the same guideline]
```

## Example Query Execution

### User Question
> "Si deve fare TAC se uno ha 45mm di aortic root?"

### Phase 1: Locate
```bash
# Search TOC
Grep: "aortic root|imaging|CT|TAC|thoracic.*aneurysm|surveillance"
File: ESC_GUIDELINES_TOC.md

# Result
PDF: 2024_Peripheral_Arterial_Aortic.pdf
Sections:
- 5.4 Evaluation of the aorta (p. 25)
  - 5.4.6 Cardiovascular computed tomography (p. 29)
- 9.2.2 Thoracic aortic aneurysms (p. 66)
  - 9.2.2.4 Surveillance (p. 70)
```

### Phase 2: Read
```bash
# Open PDF
Read: references/esc-guidelines/2024_Peripheral_Arterial_Aortic.pdf

# Extract from Section 5.4.6 (p. 29)
"CT angiography is the gold standard for aortic imaging..."

# Extract from Section 9.2.2.4 (p. 70)
"Surveillance with CT or MRI is recommended when aortic diameter is ≥45mm..."
[Recommendation Class I, Level B]
```

### Phase 3: Cite
```markdown
# Imaging per Aortic Root di 45mm

## ESC Recommendation

**Class I, Level B**: La sorveglianza con TC o RM è raccomandata quando il diametro aortico è ≥45mm.

"Surveillance imaging with CT or MRI is recommended when the aortic root diameter reaches 45mm or greater, with annual follow-up for diameters 45-49mm."

## Clinical Context

- **Threshold**: ≥45mm richiede imaging di conferma e sorveglianza
- **Imaging Modality**: TC angiografia (gold standard) o RM cardiovascolare
- **Surveillance Interval**: Annuale per 45-49mm
- **Surgery Threshold**: ≥50-55mm (salvo fattori di rischio)

## Indicazioni Specifiche per TC

| Condizione | Raccomandazione | Classe/Livello |
|------------|-----------------|----------------|
| Prima misurazione ≥45mm | TC o RM per conferma | Class I, Level C |
| Follow-up annuale | TC o RM | Class I, Level B |
| Valvola bicuspide + ≥45mm | TC annuale | Class I, Level B |
| Marfan + ≥45mm | TC ogni 6-12 mesi | Class I, Level C |

## Source Citation

**PDF**: [2024_Peripheral_Arterial_Aortic.pdf](references/esc-guidelines/2024_Peripheral_Arterial_Aortic.pdf)
**Sections**:
- 5.4.6 Cardiovascular computed tomography (p. 29)
- 9.2.2.4 Surveillance (p. 70)

## Additional Recommendations

- La TC senza contrasto può essere sufficiente per follow-up dimensionale
- La RM è preferibile in pazienti giovani per ridurre esposizione radiante
- L'ecocardiogramma può essere usato per screening ma non per decisioni chirurgiche
```

## Best Practices

### 1. Keyword Selection
- Use **medical synonyms** (e.g., "myocardial infarction" = "MI" = "heart attack")
- Include **Italian and English** terms
- Search for **abbreviations** (e.g., "AF" for atrial fibrillation)

### 2. TOC Navigation
- Start with **broad section search** (e.g., "aorta", "arrhythmia")
- Narrow to **specific subsections** (e.g., "surveillance", "imaging")
- Check **multiple related sections** (diagnosis, treatment, follow-up)

### 3. PDF Reading
- **Read tables first** - often contain key recommendations
- Look for **highlighted boxes** - ESC recommendations are emphasized
- Check **figures/algorithms** - provide decision pathways
- Don't skip **page headers** - confirm you're in the right section

### 4. Citation Accuracy
- **Quote exactly** - don't paraphrase recommendations
- **Include class/level** - essential for clinical decision-making
- **Provide page numbers** - for user verification
- **Link to PDF** - enable direct access

### 5. Clinical Context
- Mention **patient-specific factors** (age, comorbidities)
- Note **variations** by condition (bicuspid valve, Marfan syndrome)
- Include **surveillance schedules** - not just one-time recommendations
- Highlight **contraindications** or special considerations

## Common Pitfalls to Avoid

❌ **Don't:**
- Rely on TOC alone without reading the PDF
- Paraphrase recommendations (lose precision)
- Omit class/level of evidence
- Ignore special populations sections
- Miss related sections (e.g., imaging section when answering treatment question)

✅ **Do:**
- Cross-reference multiple sections
- Extract exact quotes
- Include all relevant thresholds
- Mention alternative approaches
- Cite page numbers for verification

## Performance Optimization

### Efficient TOC Search
```bash
# Use multiple keywords with OR
Grep: "aortic root|radice aortica|ascending aorta"

# Include Italian medical terms
Grep: "scompenso|insufficienza|ipertensione"

# Search for diagnostic terms
Grep: "imaging|CT|TAC|eco|RM|angio"
```

### Parallel Reading
When question involves multiple aspects:
1. Read **diagnostic section** (Phase 2a)
2. Read **treatment section** (Phase 2b)
3. Read **surveillance section** (Phase 2c)
4. Synthesize all in Phase 3

### Smart Caching
- Remember **frequently accessed PDFs** (e.g., 2024 guidelines)
- Note **common sections** for quick reference
- Build **mental map** of TOC structure

## Advanced Query Patterns

### Pattern 1: Comparative Questions
> "Quale imaging è meglio per aneurisma aortico, TC o RM?"

**Strategy**:
1. Locate imaging section in TOC
2. Read both CT and MRI subsections
3. Create comparison table with recommendations
4. Cite both sections

### Pattern 2: Threshold Questions
> "A che diametro si opera l'aorta ascendente?"

**Strategy**:
1. Locate surgical management section
2. Extract all threshold values
3. Note variations by condition
4. Present as structured table

### Pattern 3: Special Population Questions
> "Come gestire aneurisma aortico in gravidanza?"

**Strategy**:
1. Search TOC for "pregnancy" or "gravidanza"
2. Check both main section + pregnancy subsection
3. Extract pregnancy-specific recommendations
4. Note differences from general population

### Pattern 4: Multi-guideline Questions
> "Le linee guida 2024 cambiano il management dell'aorta rispetto al 2020?"

**Strategy**:
1. Locate same section in both TOCs
2. Read both PDFs in parallel
3. Create "What's new" comparison
4. Cite both guidelines with year

## Quality Checklist

Before delivering answer, verify:

- [ ] TOC was searched with comprehensive keywords
- [ ] Correct PDF was identified and opened
- [ ] Relevant sections were fully read (not just skimmed)
- [ ] Exact quotes were extracted (not paraphrased)
- [ ] Recommendation class and level are included
- [ ] Page numbers are accurate
- [ ] PDF filename and section are cited
- [ ] Clinical context is provided (thresholds, intervals)
- [ ] Special populations are mentioned if relevant
- [ ] Related recommendations are included
- [ ] Answer directly addresses user's question

## Resources

- **Primary Source**: `ESC_GUIDELINES_TOC.md` (Master index of all ESC guidelines)
- **PDF Repository**: `references/esc-guidelines/` (All ESC guideline PDFs)
- **Available Guidelines**:
  - 2024: Atrial Fibrillation, Chronic Coronary Syndromes, Hypertension, Peripheral Arterial & Aortic
  - 2023: Acute Coronary Syndromes, Cardiomyopathies, CVD & Diabetes
  - 2022: Cardio-oncology, Valvular Heart Disease
  - 2021: Heart Failure, Pacing & CRT
  - 2020: Adult Congenital Heart Disease, Sports Cardiology

## Example Queries to Practice

1. "Quali sono le indicazioni ESC per impianto ICD nella cardiomiopatia dilatativa?"
2. "A che frazione di eiezione si considera scompenso cardiaco con FE ridotta?"
3. "Quali anticoagulanti sono raccomandati in fibrillazione atriale con CHA2DS2-VASc ≥2?"
4. "Quando si fa PCI vs CABG nella malattia coronarica cronica?"
5. "Come gestire ipertensione in paziente con diabete secondo ESC 2024?"

---

## Activation Prompt

When user asks a clinical question about cardiovascular disease:

1. **Activate this skill** automatically
2. **Execute Phase 1**: Search TOC for relevant PDF
3. **Execute Phase 2**: Read identified PDF sections
4. **Execute Phase 3**: Synthesize answer with exact citations

**Remember**: The goal is to provide **evidence-based answers directly from ESC Guidelines**, not general medical knowledge. Always cite the source with precision.
