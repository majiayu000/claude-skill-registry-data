---
name: kb-screenshot-automator
description: Automate screenshot capture and insertion for Scribe-formatted KB articles. Use this skill whenever someone uploads a KB article, SOP, or step-by-step guide that contains "Screenshot Placeholder" markers and wants real screenshots captured from a live application. Also triggers when someone says "screenshot this guide", "capture screenshots for this KB", "populate screenshots", "fill in the placeholders", "automate screenshots", "screenshot the steps", or asks to navigate an app and capture step-by-step screenshots for documentation. Works with Claude in Chrome to navigate live applications, or assembles pre-captured screenshots into documents. Chains with kb-to-scribe skill output.
metadata:
  version: "1.0.1"
---

## DEPENDENCY_DECLARATION

| Tool | Status | Required For |
|---|---|---|
| Claude in Chrome | SESSION_DEPENDENT | Mode A (Capture + Assemble) only |

**FAIL_IF (Mode A):** Claude in Chrome availability is session-dependent and cannot be guaranteed. If the Chrome connector is not active at intake, **do not ask the user to choose a mode** — silently auto-default to Mode B (Assemble Only). See intake routing below.

---

<essential_principles>

This skill automates the screenshot gap in KB article production. It reads Scribe-formatted documents, identifies steps that need screenshots, navigates the live application to capture them, and assembles the final document with real annotated screenshots replacing placeholders.

### 1. Two Operating Modes

**Mode A — Capture + Assemble (Chrome connector available)**
Claude reads the document, navigates the live app via Chrome, screenshots each step, and assembles the final output. This is the full pipeline.

**Mode B — Assemble Only (no Chrome connector)**
User provides pre-captured screenshots alongside the document. Claude matches screenshots to placeholder positions by step number and produces the final populated document.

### 2. Document-Driven Navigation

The uploaded document IS the instruction set. Claude reads step descriptions, identifies action verbs (click, navigate, select, type, scroll), target elements (button names, menu labels, field names), and expected UI states. No separate manifest or config needed.

### 3. Safety-First Execution

Claude NEVER clicks Save, Submit, Delete, Confirm, or any destructive/committing action unless explicitly told to by the user. Claude stops and asks before any state-changing operation. Documentation should capture the UI state, not change it.

### 4. App-Agnostic by Default

The skill works with any browser-based application. The only per-article variable is the starting URL. App-specific quirks (slow-loading modals, collapsing sidebars, non-standard dropdowns) are handled via optional APP NOTES provided by the user.

### 5. Output Matches Input Format

If the input is .docx, output is .docx with embedded images. If the input is .pdf, output is .docx with embedded images (PDF assembly is lossy). Screenshots are saved individually as numbered PNGs alongside the final document.

</essential_principles>

<intake>

**Detect the operating mode automatically:**

> **Chrome check (run first):** Before evaluating the table below, check whether the Claude in Chrome connector is active in this session. If it is not active, skip Mode A entirely — auto-default to Mode B without asking. This check runs once at intake and is not re-evaluated mid-session.

| Condition | Mode | Action |
|-----------|------|--------|
| Document uploaded + Chrome connector active | Mode A (Capture + Assemble) | Read `workflows/capture-screenshots.md`, then `workflows/assemble-document.md` |
| Document uploaded + screenshots uploaded (no Chrome) | Mode B (Assemble Only) | Read `workflows/assemble-document.md` |
| Document uploaded + Chrome **not active** + no screenshots | **Auto-default Mode B** | Inform user: "Chrome connector is not active this session — defaulting to Mode B (Assemble Only). Please upload your screenshots to continue." Do not ask whether to enable Chrome. |

**Pre-flight validation (both modes):**
1. Confirm document contains "Screenshot Placeholder" text (or similar markers like `[SCREENSHOT]`, `[IMAGE HERE]`)
2. Count total placeholders — report to user: "Found {N} screenshot placeholders across {S} sections."
3. Identify sections with independent step numbering (H1 boundaries reset step counts)
4. Extract the starting URL if mentioned in the document (Requirements section, header, or first step)

**If starting URL is not in the document, ask:**
"What's the URL I should navigate to? (e.g., https://app.kixie.com)"

</intake>

<routing>

| Trigger | Workflow |
|---------|----------|
| Document with placeholders + Chrome available | `workflows/capture-screenshots.md` → `workflows/assemble-document.md` |
| Document with placeholders + screenshots provided | `workflows/assemble-document.md` |
| "How does this skill work?" / "what can you do with screenshots?" | Summarize this SKILL.md |
| User provides APP NOTES or app-specific instructions | Store in context, apply during `capture-screenshots` workflow |

**After reading the workflow, follow it exactly.**

</routing>

<screenshot_naming_convention>

Screenshots follow a strict naming pattern for reliable matching:

**Single-section documents:**
`step_01.png`, `step_02.png`, `step_03.png`

**Multi-section documents (step numbering resets per section):**
Use a slugified section name prefix derived from the H1 heading:
`voicemail_setup_step_01.png`, `vm_drop_step_01.png`, `checking_voicemails_step_01.png`

**Rules:**
- Always zero-pad step numbers (01, 02... not 1, 2)
- Lowercase, underscores only, no spaces
- Section prefix derived from first 3–4 meaningful words of the H1
- If ambiguous, ask user to confirm section slug names before capturing

</screenshot_naming_convention>

<pacing_protocol>

**Step-by-step mode (default):**
After each screenshot capture, report:
- What step was just completed
- What the next step is
- Any issues encountered (element not found, unexpected UI state)

Wait for user confirmation ("continue", "next", "go") before proceeding.

**Auto-run mode:**
User says "auto-run" or "go ahead and do the rest" — Claude proceeds through remaining steps without pausing, UNLESS it hits a stop condition:
- Destructive action (Save, Submit, Delete)
- Login screen or authentication prompt
- File upload or microphone/hardware interaction required
- Element not found after 2 attempts
- Unexpected error or page crash

**Resumable:**
If stopped mid-capture, Claude reports which step it stopped at. User can say "continue from step {N}" to resume without re-capturing earlier steps.

</pacing_protocol>

<reference_index>

| Reference | Purpose |
|-----------|---------|
| `references/screenshot-standards.md` | Image quality, annotation, sizing, and capture timing rules |
| `references/app-notes-template.md` | Template for users to provide app-specific navigation quirks |

</reference_index>

<workflows_index>

| Workflow | Purpose |
|----------|---------|
| `workflows/capture-screenshots.md` | Mode A: Navigate live app via Chrome, capture screenshots per step |
| `workflows/assemble-document.md` | Mode B / Stage 2: Replace placeholders in document with captured images, output final .docx |

</workflows_index>

<chaining>

This skill is designed to chain with other Loxihart documentation skills:

**Upstream:** `kb-to-scribe` → produces Scribe-formatted .docx with "Screenshot Placeholder" markers → feeds directly into this skill

**Downstream:** `loxihart-doc-generator` or `[client]-doc-generator` → if the final output needs additional Loxihart/[CLIENT] branding applied after screenshots are inserted

**Typical full pipeline:**
1. User uploads raw KB article
2. `kb-to-scribe` converts to Scribe format with placeholders
3. User uploads Scribe output to new session with Chrome connector
4. `kb-screenshot-automator` captures screenshots and assembles final doc
5. (Optional) `loxihart-doc-generator` applies final branding pass

</chaining>

<troubleshooting>

| Problem | Cause | Fix |
|---------|-------|-----|
| Chrome connector not detected | Extension not installed or connector not enabled for this session | User enables in Settings → Connectors → Claude in Chrome |
| Claude clicks wrong element | Ambiguous element description in source doc | Add APP NOTES with specificity: "The 'Save' button is in the modal footer, not the top nav" |
| Screenshots are blank or black | App blocks screenshots or hardware acceleration issue | Disable hardware acceleration in Chrome settings, retry |
| Dropdown not captured in open state | Kixie/app-specific dropdown closes on blur | Switch to step-by-step pacing for dropdown steps; capture immediately after click |
| Step numbering mismatch | Multi-section doc with independent numbering not detected | Verify H1 section boundaries; manually confirm section slugs |
| Element not found | Element below the fold or behind a loading spinner | Add APP NOTES: "Scroll down after opening [page]" or "Wait 5 seconds after clicking [button]" |
| Login screen appears | Session expired during capture | User logs back in manually, then says "continue from step {N}" |

</troubleshooting>
