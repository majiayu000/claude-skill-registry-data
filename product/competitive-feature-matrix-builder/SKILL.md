---
name: competitive-feature-matrix-builder
description: "Build a comparative feature matrix and gap analysis from a folder of competitor notes (md/txt). Works fully offline — no web access needed. Use when preparing roadmap reviews, competitive analysis sessions, or feature prioritization. Triggers: 'build feature matrix', 'competitive feature matrix', 'compare competitors from notes', 'составь feature matrix', 'матрица фич конкурентов'."
version: 1.0.0
---

# Competitive Feature Matrix Builder

This skill reads a folder of competitor notes (md or txt files) and produces a comparative feature matrix with a gap analysis and recommendations. No web access or API required — fully file-based, designed for Cowork.

**Input:**
- Folder path containing competitor notes (one file per competitor recommended; md or txt format)
- Optional: a file named `your-product.md` or `own-product.md` for self-comparison

**Output:**
- Markdown response with three sections: Feature Matrix (table), Gap Analysis, and Recommendations

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that the user provided a folder path.
   - If no path given: stop and respond: "Provide the path to a folder containing competitor notes in md or txt format."

2. Scan the folder for md and txt files.
   - If folder is empty or does not exist: stop and respond: "No files found at the provided path. Provide a folder path containing competitor notes in md or txt format."
   - Report the number of files found: "Found N files: [list filenames]."

3. Check if any file is named `your-product.md` or `own-product.md`.
   - If found: include as "Your Product" column in the matrix.
   - If not found: proceed without self-comparison column; add a closing note: "Add a file named `your-product.md` to enable self-comparison and gap analysis."

### Step 2: Extract Competitor Names and Features

1. For each file (excluding `your-product.md`/`own-product.md` if present):
   - **Competitor name:** Use the first-level heading (# Name) if present; otherwise use the filename without extension (e.g., `salesforce-notes.md` → "Salesforce").
   - **Feature extraction:** Scan the file for product features, capabilities, and attributes using these signals:
     - Explicit feature lists (bullet points, numbered lists, tables)
     - Sentences with action verbs: "supports", "offers", "includes", "has", "provides", "enables"
     - Comparison language: "unlike X, they have…", "also includes…", "unique to them…"
     - Section headings describing product areas (e.g., "Integrations", "Analytics", "Pricing")

2. For `your-product.md`/`own-product.md` (if present):
   - Apply the same extraction logic.
   - Label column as "Your Product" in the matrix.

3. If a file contains no extractable product features (e.g., meeting notes, financial data, contact list):
   - Skip the file and log: "Skipped [filename] — no product features found."
   - If all files are skipped: stop and respond: "No product features could be extracted from the provided files. Ensure your notes describe competitor product capabilities, features, or attributes."

### Step 3: Normalize the Feature List

1. Compile all extracted features into a single master list.

2. Deduplicate and normalize:
   - Group features that describe the same capability under different names (e.g., "REST API", "API access", "API integration" → group as "API / Integrations").
   - Use the most descriptive name for the grouped row.
   - Keep a footnote listing original terms grouped together (append after the matrix).

3. Sort features: group by product area if discernible (e.g., "Core Features", "Integrations", "Analytics", "Pricing/Packaging"), then alphabetically within groups.

### Step 4: Build the Feature Matrix

1. Create a markdown table:
   - Rows: one per normalized feature
   - Columns: one per competitor + "Your Product" (if present)

2. For each cell, assign a symbol:
   - **✓** — feature explicitly mentioned as present
   - **✗** — feature explicitly mentioned as absent or not supported
   - **?** — not mentioned in the notes (unknown)

3. Add a legend line below the table:
   `*Legend: ✓ = confirmed present, ✗ = confirmed absent, ? = not mentioned in notes*`

**Edge Cases:**
- If only one competitor file is present: build a single-column matrix; add note: "Gap analysis requires 2+ competitors — only the feature list is generated here."
- If files contain mostly unstructured prose (no lists or headings): extract features from paragraph context; flag: "Features extracted from unstructured text — review for accuracy before sharing."

### Step 5: Gap Analysis

1. Identify **gaps in Your Product** (only if `your-product.md` was provided):
   - Feature gaps = features where 2+ competitors have ✓ and Your Product has ✗ or ?
   - Sort by number of competitors with the feature (descending = highest priority first)
   - Assign priority: High (all competitors have it), Medium (majority), Low (minority but 2+)

2. Identify **unique competitor differentiators**:
   - Features that only one competitor has (✓ in exactly one column) — these are niche signals to monitor, not immediate gaps

3. Identify **your differentiators** (only if `your-product.md` was provided):
   - Features where Your Product has ✓ and all competitors have ✗ or ? — these are unique advantages

4. If no `your-product.md`: list features present in 2+ competitors as "Common features across the competitive landscape" (ordered by coverage breadth).

### Step 6: Recommendations

1. Write 2–4 short recommendation bullets based on the gap analysis:
   - High-priority gaps: suggest evaluating for next roadmap cycle
   - Watch-list items: suggest monitoring for adoption trends
   - Differentiators: suggest protecting and amplifying

2. Keep recommendations specific to feature names found — do not generate generic advice.

### Step 7: Output

Assemble and output the full response in three sections: Feature Matrix → Gap Analysis → Recommendations.

Add an opening line: "Processed N files: [competitor list]. Matrix covers M features."

---

## Negative Cases

- **Empty folder or invalid path:** Stop with message: "No files found at the provided path. Provide a folder path containing competitor notes in md or txt format."
- **All files non-feature content:** Stop with message: "No product features could be extracted from the provided files."
- **Single file, no your-product.md:** Build feature list only; note gap analysis is not possible with one competitor.

---

## Output Format

```
Processed N files: Competitor A, Competitor B, Competitor C. Matrix covers M features.

## Feature Matrix

| Feature | Competitor A | Competitor B | Competitor C | Your Product |
|---------|:---:|:---:|:---:|:---:|
| API / Integrations | ✓ | ✓ | ✗ | ✓ |
| Mobile App | ✓ | ✗ | ✓ | ✗ |
| Analytics Dashboard | ? | ✓ | ✓ | ✗ |

*Legend: ✓ = confirmed present, ✗ = confirmed absent, ? = not mentioned in notes*

---

## Gap Analysis

**Gaps in Your Product (features 2+ competitors have that you don't):**

| Feature | Competitors With It | Priority |
|---------|---------------------|---------|
| Mobile App | Competitor A, Competitor C | High |
| Analytics Dashboard | Competitor B, Competitor C | Medium |

**Unique Competitor Differentiators (only one competitor has):**
- [Feature X]: only Competitor B — monitor for broader adoption

**Your Differentiators:**
- [Feature Y]: unique to your product — protect and amplify

---

## Recommendations

1. **High priority:** Mobile App — 2/3 competitors have it. Evaluate for next planning cycle.
2. **Medium priority:** Analytics Dashboard — 2/3 competitors have it. Gather user demand signal before committing.
3. **Watch:** [Feature X] — niche differentiator for Competitor B; track if others adopt it.
```
