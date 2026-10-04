---
name: audit-design-system
description: Audit a Figma screen or component for design-system integration drift, including missing shared components, local overrides, and unbound tokens.
---

# Audit Design System

Review a Figma node for evidence that the design is not properly integrated with the design system.

This skill is read-only. When the user wants a write action afterward, downstream skills should use `use_figma` through a `figma-use`-style helper when the host environment requires one.

## Output Format Selection

- **Explicit user request wins**:
  - If the user asks for `--json` or JSON, output raw JSON (no markdown fences, no prose).
  - If the user asks for `--markdown`, markdown, or a specific human-readable format, output the human-readable markdown report.
- **Codex Desktop app**: Output raw JSON by default.
- **Codex CLI and other chat-style environments**: Output the human-readable markdown report by default.
- **Machine-consumed review surfaces**: Output raw JSON by default.
- **Ambiguous environment**: If the environment is unclear, output markdown by default.

## Workflow

1. Parse the Figma input.
   Accept a full Figma URL, or a `fileKey` and `nodeId`.
   Normalize node IDs from `72-293` to `72:293` when needed.

2. Pull the minimum required evidence with Figma MCP read tools.
   Call `get_design_context` for the exact node under review.
   Call `get_screenshot` for visual confirmation.
   Call `get_variable_defs` to see which variables are actually bound.
   Call `get_code_connect_map` when relevant.
   Call `get_metadata` when the reviewed node is large, repeated, or board-like and you need to map nested instances before drilling in.
   Call `search_design_system` when you have identified a likely non-systemized primitive and there is a realistic chance of suggesting a concrete replacement from the audited design system.

3. Review for systemization failures, not visual taste.
   Look for places where the design should probably inherit from the design system but is locally constructed instead.
   Base every finding on structure visible in Figma: instances, duplicated frames, raw values, variant drift, or missing token bindings.
   Prefer omissions over weak findings.

4. When the evidence is strong enough, suggest a replacement candidate.
   After identifying a likely custom primitive, use `search_design_system` to find the closest matching component family from the audited design system.
   Include a candidate only when the match is credible from structure and naming, not just screenshot similarity.
   If search results are noisy or ambiguous, omit the candidate instead of guessing.

5. Present findings in the appropriate format based on the environment.
   Use JSON for Codex Desktop and machine-consumed review surfaces, markdown for Claude Code CLI and other chat-style environments (see Output Format Selection above).

6. When the user wants a fix, route to the right downstream skill.
   Prefer [fix-design-system-finding](../fix-design-system-finding/SKILL.md) when one specific offending node should be repaired.
   Prefer [apply-design-system](../apply-design-system/SKILL.md) when the user wants a broader screen-wide pass, multiple sections need coordinated remediation, or the review is being used to define scope before writing.

## What To Flag

- Shared UI primitives recreated as ad-hoc frames instead of component instances.
  Common targets: buttons, icon buttons, cards, alerts, pills, chips, avatars, stat tiles, tab bars, nav bars, FABs, list rows.

- Repeated sibling structures that should clearly collapse into one reusable primitive.
  Example: three nearly identical stat tiles with different content.

- Hard-coded visual values where the rest of the design system uses variables.
  Common targets: fills, strokes, text colors, radius, spacing, typography, shadows.
  Only flag this when the evidence is concrete, such as a raw hex value or bespoke geometry sitting beside tokenized peers.

- Global navigation or other high-leverage patterns built from custom frames instead of system components.
  Flag these aggressively because drift there scales across many screens.

- Variant drift inside a nominal component.
  Example: a local edit button with unusual size, stroke width, or radius that does not match the expected icon-button primitive.

## What Not To Flag

- Purely aesthetic preferences.
- Copywriting or product decisions.
- Layout choices that can reasonably remain screen-specific.
- One-off compositions when the underlying primitives are already componentized and tokenized.
- Claims that require undocumented assumptions about a design library.

## Evidence Standard

Every finding must answer both questions:

1. What concrete Figma evidence shows this is not systemized correctly?
2. Why does that matter for propagation, consistency, theming, or maintenance?

Good evidence includes:

- a node is a plain frame when it should be an instance
- several siblings duplicate the same structure
- raw color or geometry values appear where variables or standard primitives should apply
- a global pattern is custom-built

Weak evidence includes:

- "this looks custom"
- "I would normally make this a component"
- any statement based only on screenshot aesthetics without structural support

## Replacement Suggestion Rule

When a finding is about a missing shared primitive, try to attach one likely replacement suggestion.

Use `search_design_system` after you already know what category of thing is missing, for example:
- custom avatar cluster
- bespoke stat tile
- local alert card
- hand-built navigation item

Only suggest a replacement when:
- the node's role is clear
- the search result belongs to the relevant library or audited file context
- the candidate is structurally plausible for the finding

Good suggestion language:
- `This custom avatar frame could likely be replaced with Avatar from library X.`
- `These repeated stat tiles appear to map to Metric item from library X.`

Do not overstate:
- do not claim the suggested component is definitely correct unless the evidence is explicit
- do not force a replacement candidate into every finding
- do not recommend a component from an unrelated library just because search returned it first

## Output Format

### JSON Output

When the selected output format is JSON, return this exact JSON shape with no markdown fences and no extra prose:

```json
{
  "findings": [
    {
      "title": "<= 80 chars, imperative>",
      "body": "<valid Markdown explaining why this is a problem>",
      "confidence_score": 0.0,
      "priority": 0,
      "code_location": {
        "absolute_file_path": "/figma/<fileKey>/nodes/<nodeId>",
        "line_range": {
          "start": 1,
          "end": 1
        }
      }
    }
  ],
  "overall_correctness": "patch is correct" | "patch is incorrect",
  "overall_explanation": "<1-3 sentence summary>",
  "overall_confidence_score": 0.0
}
```

Schema notes:

- Use `overall_correctness: "patch is incorrect"` whenever you found one or more design-system integration issues.
- Use `overall_correctness: "patch is correct"` only when there are no findings.
- For each finding, set `code_location.absolute_file_path` to `/figma/<fileKey>/nodes/<nodeId>` using the most specific offending node.
- Always set `line_range.start` and `line_range.end` to `1`.

### Human-Readable Markdown Report

When the selected output format is markdown, present a formatted markdown report with:

1. **Header section:**
   - File name and node being reviewed
   - Overall verdict: ✅ Passes / ⚠️ Needs Work / ❌ Significant Issues
   - Confidence percentage

2. **Summary:** 2-3 sentences explaining the overall state

3. **Findings table:** Quick overview with priority indicators
   - 🔴 Critical (priority 3): severe library-level or navigation-level issues
   - 🟠 High (priority 2): important reusable primitive or tokenization issues
   - 🟡 Medium (priority 1): moderate system drift
   - ⚪ Low (priority 0): nits or low-impact consistency issues

4. **Details section:** Expand each finding with:
   - What's wrong (concrete evidence from Figma structure)
   - Why it matters (maintenance, consistency, theming impact)
   - Likely replacement, when supported by `search_design_system`
   - Affected node IDs for reference

5. **Recommendations:** Prioritized action items

### Output Rules

- Keep findings focused on the highest-signal issues. Usually 0-6 findings.
- Keep titles imperative and under 80 characters.
- Always anchor each finding to a specific node ID so users can locate it in Figma.
- For JSON output, do not invent filesystem paths. Use `/figma/<fileKey>/nodes/<nodeId>` exactly.
- When a replacement suggestion is credible, include it in the finding body.

## Review Heuristics

Use `priority` like this:

- `0`: nit or low-impact consistency issue
- `1`: moderate system drift
- `2`: important reusable primitive or tokenization issue
- `3`: severe library-level or navigation-level issue likely to propagate widely

Use `confidence_score` like this:

- `0.9-1.0`: direct structural evidence
- `0.7-0.89`: strong inference from repetition and nearby token usage
- `0.5-0.69`: plausible but incomplete evidence; prefer omitting instead

## Board And Screen Scope

For a single screen:

- inspect the root node
- drill into repeated or high-leverage children
- anchor findings to the most specific offending node

For a board or larger page:

- use `get_metadata` first to identify candidate screens or repeated modules
- review only the most relevant nodes instead of trying to audit everything
- keep findings scoped and evidence-backed

## Example Trigger Phrases

- "Review this Figma screen for design-system integration"
- "Audit this board for missing component usage"
- "Check whether this design uses tokens correctly"
- "/audit-design-system https://figma.com/design/..."
- "/audit-design-system --json https://figma.com/design/..." (for JSON output)

## Handoff Guidance

Use this routing rule after the review:
- one concrete finding with a narrow write scope: use [fix-design-system-finding](../fix-design-system-finding/SKILL.md)
- several findings that collapse into a broader screen or section reconciliation pass: use [apply-design-system](../apply-design-system/SKILL.md)

Do not force every review result through the single-finding fix skill. Some reviews are better used as scope discovery for a broader apply pass.
