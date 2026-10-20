---
name: codebase-guard
description: A tag-indexed issue library. Run this to either archive a newly solved issue (Librarian mode) or audit code changes against existing issue tags (Reviewer mode).
---

# Unified Codebase Guard Router

You have two operational roles within this skill. Determine which role to execute based on the user's prompt.

---

## MODE 1: The Librarian (Write & Index)
**Trigger:** Activated when the user asks to archive, log, or save a newly discovered issue/bug from the current session.

### Protocol:
## MODE 1: The Librarian (Write & Index)
**Trigger:** Activated when the user asks to archive, log, or save a newly discovered issue/bug from the current session.

### Protocol:
1. **Analyze:** Extract the core architectural failure, symptoms, and resolution from the current chat history. Do not focus on local variable names or specific files; identify the core technical pattern.
2. **Deduplication Check (CRITICAL STEP):**
   - Open and read `./INDEX.md` completely.
   - Scan the `Tags` and `Issue Summary` columns for any existing rules addressing the same foundational problem (e.g., if archiving a hardcoded API endpoint, check if there is an existing rule for hardcoded environments, configuration coupling, or magic strings).
   - **Deep Review:** If a potential match is found, open that specific `./issues/ISSUE-[Number].md` file to evaluate its full description.
3. **Branching Decision:**
   * **Scenario A: Conceptual Overlap (Amending Mode)**
     If the current bug is simply a new symptom or variation of an existing rule, **do not create a new file or increment the index.** Instead:
     - Open the existing `./issues/ISSUE-[Number].md` file.
     - Add a new generalized category under the `## Symptoms` section describing this new variation.
     - If the fix introduces a new edge case, update the `## Working Fix / Mitigation` section.
     - Stop execution and inform the user: *"This issue matches ISSUE-XXX. I have updated that rule's symptoms to include this scenario rather than creating a duplicate."*
   * **Scenario B: Genuinely Unique (Creation Mode)**
     If no existing rule in `INDEX.md` structurally matches this failure:
     - Generate a new sequential number (e.g., `005`).
     - Write a new abstract markdown file to `./issues/ISSUE-[Number].md`.
     - Append a single new row to `./INDEX.md` with the new Number, Tags, and an abstract Summary.
     - Report the new Issue Number to the user.
4. **Write Atomic Issue File:** Create a new standalone markdown file inside `./issues/ISSUE-[Number].md` using these strict generalization constraints:
   - **Title:** Use high-level architectural terms, not specific feature names.
   - **Description:** Explain the underlying structural vulnerability. Avoid mentioning specific project-level domain objects unless as a generic example.
   - **Symptoms:** Group by *logical behavior* rather than concrete codebase paths. **Never include specific file paths (like `*.vue` files) or literal year constants (like `2023`) in the core rules.** Use placeholder descriptions instead.
   - **Anti-Pattern Code Blocks:** Convert the specific code into generic, abstract code blocks. Use generic object/property names (e.g., `record.name` or `item.label`) so the pattern matcher recognizes the syntax shape rather than the literal tokens.
   - **Remediation Code Blocks:** Show how to rewrite the abstract pattern safely using proper architectural patterns (e.g., schema fields, utility parsers).
5. **Update Index:** Append a single row to the table in `./INDEX.md` documenting only the new Issue Number, its tags, and a generalized summary.
6. **Report:** Provide the user with the new Issue Number and summary of what was archived.

---

## MODE 2: The Reviewer (Tag-Matched Audit)
**Trigger:** Activated when the user asks to review, audit, or check code changes, staging environments, or PRs.

### Protocol:
1. **Identify Target Tags:** Inspect the code changes in the active workspace to deduce the relevant technical domains (e.g., changing a Zod schema implies `validation` and `api`).
2. **Consult INDEX.md:** Open `./INDEX.md` and scan the tags column. Filter out and collect the **Issue Numbers** that match the target tags.
3. **Load Target Issues:** Dynamically construct the file path for each matched number as `./issues/ISSUE-[Number].md`. Open and read **only** those specific files.
4. **Verify Delta:** Check the workspace code changes against the "Anti-Pattern" section of each loaded issue file.
5. **Report Violations Only (Strict Silence for Non-Matches):**
   - **If a violation is found:**
     - Identify the exact file name and line numbers where the issue occurs.
     - **Explain the Contextual Manifestation:** Clearly describe *how* and *why* the user's specific code implementation replicates the historical bug.
   - **If NO violations are found:**
     - **Do not output anything.** Skip any mention of the clean files, passed rules, or success summaries. Produce absolute silence for any rule or file that passes cleanly.