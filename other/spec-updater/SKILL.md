---
name: spec-updater
description: Apply feedback-driven changes to a UX spec and update it in Confluence
version: 1.0.0
author: Mattermost Design Team
tags: [ux, spec, confluence, feedback, update, maintenance]
disable-model-invocation: true
---

# Spec Updater

## Write-Safety Gate (READ FIRST — non-negotiable)

This skill writes to Confluence via `updateConfluencePage`. Confluence writes are a hard-stop gate. Follow this every run, no exceptions:

1. **Dry-run first, always.** `dry_run` defaults to **TRUE**. The first action is always a preview: show the full BEFORE/AFTER diff per affected section and state **exactly what will be written and to which page** (page title + ID/URL). No write happens on this pass.
2. **Wait for explicit confirmation.** Do not write to Confluence until the user gives a clear "yes" / "go ahead" in chat. Silence, "looks good?", or an ambiguous reply is not consent. Re-run with `dry_run: false` only after that explicit yes.
3. **Draft only by default.** Create/update the page as a **DRAFT**. Never publish in the same step. **Publishing requires a SECOND explicit confirmation** — surface it as its own ask after the draft write succeeds.
4. **Label AI content.** All AI-generated or AI-modified content is labeled **`[AI DRAFT]`** until a human has reviewed it. Carry the label through the draft; it is removed only on human sign-off.
5. **Never auto-write.** No code path may call `updateConfluencePage` (or any Confluence write) without steps 1–3 satisfied. If in doubt, stop and ask.

> This mirrors the `defense-ux-context` skill's Output Rules (Confluence) verbatim in intent: confirm → draft → second confirm to publish → `[AI DRAFT]`. If this skill's behavior ever diverges from `defense-ux-context`, `defense-ux-context` wins.

## Claude Code model (Phase 8)

Invoke with **`claude-sonnet-4-6`**. Phase 8 is targeted diff work — not full-pipeline reasoning. Escalate to Opus only if feedback requires re-scoping or threat-model re-evaluation.

## Purpose

Takes feedback (review comments, stakeholder notes, Jira tickets, or direct instructions) and applies targeted changes to an existing UX spec in Confluence. This is the Phase 8 (Spec Maintenance) workhorse — the skill you use when the spec already exists and needs to evolve.

This skill handles the full loop: read the current spec from Confluence, understand the requested changes, generate the updated content, and write it back to Confluence with a version message.

## When to Use

- A stakeholder reviewed the spec and left feedback (in Confluence comments, Slack, email, or Jira)
- Engineering found an issue during implementation that requires a spec update
- A design review produced MUST-FIX items that need to be applied
- PM changed scope or requirements after spec approval
- You completed a Phase 7 gate and need to apply Edge Case Hunter findings
- You need to add/update a single section without regenerating the entire spec
- Any time someone says "update the spec to reflect..."

## When NOT to Use

- The spec doesn't exist yet (use the full Phase 1–7 pipeline instead)
- You need to create a brand new spec from scratch (use spec-writer-agent)
- The feedback is vague and needs synthesis first (use feedback-synthesizer first, then this skill)

## How It Works

### Step 1: Read the Current Spec

The skill reads the existing spec from Confluence using the page ID or URL you provide.

### Step 2: Parse the Feedback

The skill accepts feedback in any format:
- Raw text ("change the error message in Section 4 to say...")
- Structured feedback table (output from feedback-synthesizer)
- Confluence inline comments (read via Confluence API)
- Jira ticket descriptions
- A list of changes

### Step 3: Generate Targeted Updates

For each change, the skill:
1. Identifies which spec section(s) are affected
2. Reads the current content of those sections
3. Generates the updated content following the same prescriptive style as the original
4. Preserves all content that isn't being changed
5. Adds a note to the Revision History section (located by heading, not a fixed number)

### Step 4: Write Back to Confluence (gated)

This step never runs unconfirmed. The skill first produces a **dry-run preview** (default `dry_run: true`), states exactly what will change and on which page, and waits for the user's explicit "yes". Only then does it update the page **as a draft** (content labeled `[AI DRAFT]`) with a version message summarizing what changed. **Publishing is a separate action requiring a second explicit confirmation.** See the Write-Safety Gate at the top of this skill.

---

## Input

```json
{
  "confluence_page_id": "string (the page ID of the spec to update)",
  "confluence_cloud_id": "string (your Atlassian cloud ID)",
  "feedback": "string (the changes to apply — any format)",
  "feedback_source": "string (optional — where the feedback came from: 'review', 'jira', 'slack', 'inline_comments', 'direct')",
  "dry_run": "boolean (optional, default TRUE — when true (the safe default), show the BEFORE/AFTER changes and the target page WITHOUT writing to Confluence. Only set to false AFTER the user gives explicit confirmation on the dry-run preview)",
  "update_revision_history": "boolean (optional, default true — add entry to the Revision History section, located by heading)"
}
```

## Output

```json
{
  "sections_modified": ["string (section numbers/names that were changed)"],
  "changes_summary": "string (human-readable summary of all changes made)",
  "revision_entry": "string (the entry added to the Revision History section)",
  "confluence_url": "string (link to the updated page)",
  "warnings": ["string (any issues encountered — ambiguous feedback, sections not found, etc.)"]
}
```

---

## System Prompt

```
You are a senior UX spec editor for Mattermost, a security-focused collaboration platform used by DoD and defense contractors.

Your task is to apply targeted changes to an existing UX spec based on the provided feedback. You must:

1. READ the current spec content carefully before making any changes.
2. IDENTIFY which sections are affected by each piece of feedback.
3. APPLY changes precisely — modify only what needs to change, preserve everything else.
4. MAINTAIN the prescriptive style of the spec:
   - Use "must", "will", "does not" — never "should", "could", "may"
   - Every setting must have: label text, help text, default value, behavior
   - Every error state must have: exact trigger condition and exact error message text
   - Mobile behavior must be explicitly stated for every flow
5. FLAG anything ambiguous with [TBD: reason] — never guess at UI specifics.
6. UPDATE the Revision History with a dated entry describing the changes.
7. PRESERVE deprecated explorations — if removing a previously specified approach, move it
   to the Deprecated Explorations section with strikethrough and reason, don't delete it.

Reference sections BY NAME, not by fixed number — the template's optional sections shift
the numbering between specs, so a hardcoded "Section 13" is unreliable. Locate sections by
their heading text (e.g. "Roles & Permissions", "Edge Cases", "Accessibility", "Revision
History", "Deprecated Explorations").

Rules:
- Never delete content without moving it to the Deprecated Explorations section first.
- If feedback contradicts an existing section, flag the contradiction and ask for resolution
  rather than silently overwriting.
- If feedback requires changes to the Roles & Permissions matrix, the Edge Cases table, or
  the Compliance appendix, update those sections too — don't just update the prose.
- If the change affects mobile behavior, explicitly update mobile documentation.
- If the change affects accessibility, update the Accessibility section.
- WRITE-SAFETY: never call updateConfluencePage without satisfying the Write-Safety Gate
  (dry-run preview → explicit user confirmation → draft only → second confirm to publish →
  [AI DRAFT] label). dry_run is TRUE until the user confirms the preview.

Output format:
For each section you modify, show:
[SECTION: Section Name]   ← identify by heading text, not a fixed number
[BEFORE]: (relevant excerpt of current content)
[AFTER]: (updated content)
[REASON]: (which feedback item drove this change)

This is the DRY-RUN PREVIEW. Also state plainly: the target page (title + ID/URL) and that
nothing has been written yet. Then STOP and wait for the user's explicit "yes" before any
write. Only after that confirmation do you provide the full updated page content for the
Confluence draft write-back (and request a second confirmation before any publish).
```

---

## Usage Examples

### Example 1: Direct instruction to change specific text

**Input:**
```
feedback: "Change the error message when a user is denied channel access from
'You do not have permission to view this channel' to 'Channel access restricted.
Contact your administrator to request access.' Also add a 'Request Access' button
that opens a pre-filled message to the channel admin."

confluence_page_id: "123456789"
```

**What happens:**
1. Reads the spec from Confluence
2. Finds the End-User UX Flows section (by heading) where the denied access flow is documented
3. Updates the error message text
4. Adds the new "Request Access" button to the UI Component Specifications section
5. Updates the Edge Cases table if the button introduces new states
6. Adds a Revision History entry
7. Shows the dry-run preview (target page + diff), waits for explicit confirmation, then writes back as a `[AI DRAFT]` draft

### Example 2: Apply feedback-synthesizer output

**Input:**
```
feedback: |
  MUST-FIX:
  1. Missing loading state for attribute sync operation (Section 3.1)
  2. Error message for LDAP timeout doesn't specify retry behavior (Section 4.2)

  SHOULD-FIX:
  3. Add keyboard shortcut for toggling attribute panel (Section 5)

  OUT OF SCOPE:
  4. Batch attribute editing for multiple channels — defer to Phase 2

confluence_page_id: "123456789"
feedback_source: "review"
```

**What happens:**
1. Processes all MUST-FIX items as mandatory changes
2. Processes SHOULD-FIX items as changes
3. Moves OUT OF SCOPE item to the Future Considerations section, and to Deprecated Explorations if it was previously in scope (both located by heading text, not a fixed number)
4. Updates affected sections with full detail
5. Shows the dry-run preview and waits for confirmation, then writes the draft with version message: "Applied 3 changes from design review: added loading state for attribute sync, specified retry behavior for LDAP timeout, added keyboard shortcut for attribute panel"

### Example 3: Dry run to preview changes (the default flow)

**Input:**
```
feedback: "Remove the auto-translation toggle from the channel header and move it to channel settings instead"
confluence_page_id: "987654321"
# dry_run omitted → defaults to TRUE; no write happens on this pass
```

**What happens:**
1. Reads the spec
2. Generates all the changes (locating affected sections by heading: channel-header behavior, channel-settings flow, the relevant UI component spec, and the Edge Cases table)
3. Shows the BEFORE/AFTER diff for each section and names the target page (title + ID)
4. Does NOT write to Confluence
5. Designer reviews, says "looks good, apply it" → re-run with `dry_run: false` to write the `[AI DRAFT]` draft; publishing then needs a second explicit confirmation

---

## Execution Flow (How to Use with Confluence MCP)

Here is the concrete sequence of tool calls this skill makes:

```
Step 1: Read the spec
→ getConfluencePage(cloudId, pageId, contentFormat: "markdown")

Step 2: Parse and plan changes
→ (Internal — analyze feedback against spec content)
→ If feedback_source is "inline_comments":
  → getConfluencePageInlineComments(cloudId, pageId)

Step 3: Generate updates + DRY-RUN PREVIEW (default; no write)
→ (Internal — produce BEFORE/AFTER for each section, located by heading text)
→ Present preview: name the target page (title + ID/URL), show the diff, label content [AI DRAFT]
→ STOP. Wait for the user's explicit "yes" before any write.

Step 4: Write back as DRAFT — ONLY after explicit confirmation (dry_run: false)
→ updateConfluencePage(cloudId, pageId, body: updatedContent,  // draft, content carries [AI DRAFT]
     versionMessage: "[AI DRAFT] Spec update: [summary of changes]")
→ Do NOT publish in this step.

Step 5: Publish — ONLY on a SECOND explicit confirmation
→ Surface publishing as its own ask; never auto-publish.

Step 6: Resolve inline comments (if feedback came from comments)
→ (Designer manually resolves comments after reviewing the update)
```

> No `updateConfluencePage` call may execute until Step 3's preview has been confirmed by the user. Publishing requires the additional confirmation in Step 5.

---

## Markdown → Confluence Export (Phase 7 spec & Phase 8 maintenance ONLY)

This is the conversion contract for getting a finished spec out of markdown and into Confluence. The publish allowlist is exactly two things: the canonical Phase-7 spec (`07-spec.md`) and Phase-8 maintenance updates to it. **Nothing else publishes.** Pre-spec artifacts (Phases 1–6) and the internal validation siblings (`07-spec-edge-cases.md`, `07-spec-traceability.md`) stay **local** — only `07-spec.md` publishes.

### Conversion approach: markdown → Confluence storage format

Confluence stores pages as **XHTML "storage format,"** not markdown. Two supported paths, in order of preference:

1. **Let the Confluence API do the conversion (preferred).** `updateConfluencePage` / `createConfluencePage` accept a `markdown` body representation — pass the markdown directly and let Confluence convert to storage format. This is the path the Execution Flow above uses (`getConfluencePage(..., contentFormat: "markdown")` round-trips cleanly). Use it whenever the spec's markdown is within the subset Confluence converts losslessly.
2. **Pre-convert to storage format (fallback) when fidelity matters.** When the markdown uses constructs the API's markdown path mangles (panels, status lozenges, nested tables, wide code blocks), emit Confluence **storage-format XHTML** for those blocks and submit that representation instead. Convert deterministically per the element map below; never hand-wave the mapping.

### Element mapping (markdown construct → Confluence storage format)

| Markdown construct | Confluence storage-format target | Notes |
|---|---|---|
| Headings `#`–`######` | `<h1>`–`<h6>` | The spec's skim-layer H1/H2/H3 carry over; keep the `[AI DRAFT]` label in the title and lead. |
| Paragraphs, bold, italic, inline `code` | `<p>`, `<strong>`, `<em>`, `<code>` | Straightforward. |
| Tables (traceability matrix, roles/permissions, decisions) | `<table><tbody><tr><th>/<td>` | Header row → `<th>`. Confluence renders these as native sortable tables. Keep self-resolving glosses inline (`FR-10 (admins bulk-assign…)`), never bare codes. |
| Fenced code blocks ` ``` ` | `<ac:structured-macro ac:name="code">` with `<ac:plain-text-body><![CDATA[ … ]]>` | Set the `language` parameter when known. CDATA-wrap to preserve `<`, `>`, `&`. |
| Callouts / admonitions (BLUF, `[VERIFY WITH PM]`, blockers) | `<ac:structured-macro ac:name="info">` / `name="note"` / `name="warning"` | BLUF → `info`; `[VERIFY WITH PM]` and open questions → `note`; P1 blockers → `warning`. Pin these near the top so the skim layer survives. |
| Status badges (P1/P2/P3, draft) | `<ac:structured-macro ac:name="status">` with a `colour` + `title` param | Always pair colour with the text title (P1/P2/P3) — never colour alone (carries the WCAG color+text rule into Confluence). |
| Links (Figma, sibling specs, Jira) | `<a href="…">` or `<ac:link>` for intra-Confluence | Figma/external → plain `<a>`. Cross-spec → `<ac:link><ri:page ri:content-title="…"/></ac:link>`. |
| **Repository-relative links** (dedup citations like `../02-research.md#anchor`, `05-flows/x.md`) | `<ac:link>` to the published page, OR delinked plain text | These point at **local, unpublished** pre-spec artifacts — a raw relative href is a dead link in Confluence. Rewrite each: if the target maps to a published Confluence page, emit `<ac:link><ri:page ri:content-title="…"/>` (optionally `#anchor`); otherwise **strip the link** and keep the quoted gist as plain text. Never emit a repository-relative `<a href>`. |
| Images / diagram exports | `<ac:image><ri:attachment ri:filename="…"/></ac:image>` | Any diagram or image that the published `07-spec.md` references is attached as an image export (PNG/SVG) — Confluence renders the static attachment. |

Pre-export preflight: scan the draft for repository-relative links (`../NN-*.md`, `NN-*/...md`, `#anchor` into a sibling file) and resolve every one per the Repository-relative links row **before the dry-run preview** — rewrite to an `<ac:link>` where a published target exists, otherwise delink to plain text. The preview must show the already-converted content, so the user approves exactly what gets written. A draft still carrying an unresolved repository-relative link is not export-ready.

Round-trip rule: read the existing page with `contentFormat: "markdown"`, edit in markdown, write back via the markdown representation when path (1) is lossless; switch to storage-format XHTML only for the blocks in the table that need it. Locate sections by heading text (never a fixed number), per the system prompt.

### Safety gates — UNCHANGED (Milestone A)

The export changes only the *format conversion*, never the *write safety*. Every Milestone-A gate from the **Write-Safety Gate** section above still applies verbatim, in order:

1. **Dry-run preview first** (`dry_run: true` default) — show BEFORE/AFTER per section and name the target page (title + ID/URL); for a NEW publish, show the full converted page and the target space/parent. No write on this pass.
2. **Wait for explicit confirmation** — a clear "yes"/"go ahead" in chat. Ambiguity is not consent.
3. **DRAFT only** — `createConfluencePage`/`updateConfluencePage` writes a draft; never publish in the same step.
4. **Second explicit confirmation to publish** — surfaced as its own ask after the draft write succeeds.
5. **`[AI DRAFT]` label** — carried through title, lead, and version message until human sign-off removes it.

All format conversion — including the repository-relative-link rewrite/delink above — is performed while generating the content, **before the dry-run preview**. The preview therefore shows the fully converted result, and the draft write persists that exact same content, so the user approves precisely what is written to Confluence.

---

## Integration with Other Skills

| Scenario | Workflow |
|---|---|
| Got raw feedback from a review session | Run `feedback-synthesizer` first → pipe its output as the `feedback` input to `spec-updater` |
| Need to check if update introduced new edge cases | Run `edge-case-hunter` on the updated spec after applying changes |
| Need to verify update didn't break PRD traceability | Run `traceability-checker` on the updated spec after applying changes |
| Feedback includes security concerns | Run `threat-modeler` on the affected sections before applying changes |
| Multiple rounds of feedback on the same spec | Run `spec-updater` sequentially — each run reads the latest version from Confluence |

---

## Validation Rules

1. Every modified section must maintain the prescriptive language standard (no "should", "could", "may")
2. If an error message was changed, the Edge Cases table must also be checked for consistency
3. If a permission was changed, the Roles & Permissions matrix must be updated
4. If mobile behavior was affected, the mobile documentation must be explicitly updated
5. The Revision History entry must include: date, author, and a one-line summary per change
6. No content is ever permanently deleted — deprecated content moves to the Deprecated Explorations section
7. Sections are always located by heading text, never by a fixed number (optional sections shift numbering)
8. `dry_run` defaults to TRUE; no Confluence write executes until the user explicitly confirms the dry-run preview
9. Writes create/update a DRAFT only; publishing requires a separate, second explicit confirmation
10. All AI-generated/modified content is labeled `[AI DRAFT]` until human-reviewed

---

## Related Skills

- **feedback-synthesizer** — Pre-processes raw feedback into categorized, actionable items before spec-updater applies them
- **edge-case-hunter** — Run after updates to verify no new gaps were introduced
- **traceability-checker** — Run after updates to verify PRD coverage wasn't degraded
- **section-writer** — If a section needs to be substantially rewritten (not just patched), delegate to section-writer with the updated context, then use spec-updater to write the result to Confluence
