---
name: investor-report
description: >
  Generate concise investor reports for Solum Health. Pulls metrics from Google Sheets,
  analyzes customer conversations from Fireflies, and produces a structured DOCX report
  matching the investor update template. Use this skill when the user says "investor
  report", "investor update", "monthly report for investors", "board update", "generate
  investor deck", "how are we doing this month", or any variation of wanting a periodic
  investor-facing summary. Default period: previous calendar month. User can specify a
  different period.
---

# Investor Report

Generate a concise, data-driven investor report for Solum Health. Pulls metrics from
Google Sheets and customer conversation insights from Fireflies. Outputs a DOCX file
matching the investor update template.

## Template Structure

The DOCX template lives at:
`~/Documents/Claude/Agents/Investor Report/Investor Update Template.docx`

The report follows this EXACT structure. No headings, no markdown. Just bold section
labels followed by bullet lists. Font is Arial 11pt, US Letter, 1" margins.

```
Subject: Solum Health Investor Update: {Month} {Year}

{1-2 sentence exec summary of the month. Written by the founder. Conversational.}

Metrics:
  * Revenue: ${MRR} MRR / ${ARR} ARR ({direction} from ${prev} last month, {+/-pct}%)
  * Clients: {live} live, {signed} signed ({direction} from {prev} last month)
  * Cash: ${cash}
  * Burn: ${burn}/mo
  * Runway: {months} months

{Optional: chart image if available}

Asks:
  * {Specific request to investors: intros, hires, advice}
  * {Another ask}

Highlights:
  * {Win 1 in founder voice}
  * {Win 2 in founder voice}
  * {Win 3 in founder voice}

Lowlights:
  * {Challenge 1 with context}
  * {Challenge 2 with context}

Shout outs:
  * {Thank specific investors or people who helped}

Goals/priorities for next month:
  * {Goal 1 with specific target}
  * {Goal 2 with specific target}
  * {Goal 3 with specific target}
```

## DOCX Generation

Generate the report as a `.docx` file using `docx-js`. Match the template exactly:

- Font: Arial 11pt (22 half-points)
- Page: US Letter (12240 x 15840 DXA), 1" margins
- Line spacing: 1.15 (276 twips)
- Section labels: Bold, no colon space after
- Bullet items: Standard bullet list with 720 indent, 360 hanging
- Metric labels (Revenue:, Cash:, etc.): Bold within the bullet
- Empty paragraph between sections
- No headings, no horizontal rules, no tables for metrics

Save output to: `~/Documents/Claude/Agents/Investor Report/Solum Health Investor Update {Month} {Year}.docx`

## Data Sources

### 1. Google Sheets (KPI Dashboard)

**Spreadsheet ID:** `1zjXHQGdQXerCsWJ9fNZGaNoS-U8vwXHt`
**Sheet GID:** `1150083451`

Try reading via `gws sheets +read`. If unavailable, ask the user to paste metrics or
provide them inline. Never block the report on a single data source.

Core metrics to extract:
- Clients (Live) and Clients (Signed)
- ARR and MRR
- Cash on Hand
- Monthly Burn
- Runway (Months)
- MoM deltas for all

### 2. Fireflies (Customer Conversations)

Pull customer-facing calls from the reporting period.

```
fireflies_get_transcripts: mine=true, fromDate={periodStart}, toDate={periodEnd}, limit=50, format=json
```

If period has 50+ meetings, paginate with a second call for the earlier half.

**Filter to customer calls only:**

KEEP calls where:
- Title contains a company name + "Solum" (e.g., "TRAAC X Solum Health")
- Title contains "Assessment", "FUP", "Onboarding", "Demo", "Touchpoint", "Alignment"
- At least one participant is NOT @getsolum.com

EXCLUDE calls where:
- All participants are @getsolum.com (internal)
- Title contains "Daily", "Weekly Master-Room", "Roman Coliseum", "CEO Operations",
  "Growth Solum", "Product Operations", "Standup", "Interview"
- Title suggests personal/non-business meetings

For calls with summaries, extract:
- Customer name and topics discussed
- Expansion signals (new locations, more services, referrals)
- Risk signals (pricing concerns, churn, competitor mentions)
- Key themes across all calls

## Writing Rules

These are non-negotiable:

1. **Use the founder's actual words.** If the user provides bullet points or notes, use
   their phrasing. Clean up typos and grammar but do NOT rewrite their voice.
2. **No AI language.** Ban: "significant progress", "gaining traction", "we're excited",
   "leveraging", "streamlining", "driving growth", "robust". If it sounds like ChatGPT
   wrote it, rewrite it.
3. **No em dashes.** Use commas or periods instead.
4. **Short sentences.** 2-3 sentences per bullet max.
5. **Specific over vague.** Name the client, name the number, name the action.
6. **First person.** "We" not "the company" or "Solum Health".
7. **Conversational.** Like you're writing to people who already know the business.
8. **Honest about lows.** Say what went wrong, say why, say what you're doing. No spin.

## Workflow

1. **Determine period:** Default = previous calendar month. Parse user input for custom range.
2. **Collect metrics:** Try Google Sheet first. Fall back to user-provided data.
3. **Pull Fireflies data:** Get customer calls for the period. Fetch summaries. Analyze themes.
4. **Ask the user for their input:** Before generating, ask for:
   - Any specific highlights they want to include
   - Any lowlights or challenges
   - Asks for investors
   - Shout outs
   - Goals for next month
   If the user already provided this info, skip asking.
5. **Generate the DOCX:** Use docx-js to create the file matching the template format exactly.
6. **Validate:** Run `python scripts/office/validate.py` on the output.
7. **Tell the user** where the file was saved.

## DOCX Code Reference

Use this structure for generating the document with docx-js:

```javascript
const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat } = require('docx');
const fs = require('fs');

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: "\u2022",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
      }]
    }]
  },
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 22 }  // 11pt
      }
    }
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      // Subject line: "Subject:" bold + rest normal
      new Paragraph({
        children: [
          new TextRun({ text: "Subject:", bold: true }),
          new TextRun(" Solum Health Investor Update: {Month} {Year}")
        ]
      }),
      // Empty line
      new Paragraph({}),
      // Exec summary
      new Paragraph({ children: [new TextRun("{exec summary}")] }),
      // Empty line
      new Paragraph({}),
      // Metrics header
      new Paragraph({ children: [new TextRun({ text: "Metrics:", bold: true })] }),
      // Metric bullets with bold labels
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({ text: "Revenue:", bold: true }),
          new TextRun(" ${value} ({delta})")
        ]
      }),
      // ... more metrics
      // Empty line
      new Paragraph({}),
      // Asks header
      new Paragraph({ children: [new TextRun({ text: "Asks:", bold: true })] }),
      // Ask bullets (normal text)
      // ... same pattern for Highlights, Lowlights, Shout outs, Goals
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
});
```

Each section follows the same pattern:
1. Bold label paragraph (e.g., "Highlights:")
2. Bullet list items using numbering reference
3. Empty paragraph separator

## Integration Notes

- Depends on: Fireflies MCP, docx npm package (install globally: `npm install -g docx`)
- Optional: Google Sheets via gws CLI
- Template reference: `~/Documents/Claude/Agents/Investor Report/Investor Update Template.docx`
- Output goes to same directory with month/year in filename
