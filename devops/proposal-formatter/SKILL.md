---
name: proposal-formatter
description: Format trading proposals with timestamped headers and disciplined bullet structure. Use when a persona must deliver a single consolidated proposal with Schwab timestamps, bold parent bullets, and one-metric-per-line nested bullets.
---

# Proposal Formatter

Use this skill to present trading output in a concise, scan-friendly proposal. It supports any persona that needs to deliver a Schwab-timestamped summary with consistent structure.

## Instructions

1. **Header**
   - Start responses with `### Proposal ({HH:MM} ET | {HH:MM} UTC)`.
   - Source both timestamps from Schwab data (`schwab-data-sweep` cache, `mcp__schwab__get_datetime`, or another broker response). Never rely on local system time.

2. **Parent Bullets**
   - Organize the body with bold parent bullets (`- **Section Name**`).
   - Choose section names appropriate to the persona (e.g., `Prereqs`, `Capital`, `Market`, `Indicators`, `Structure`, `Plan`, `Next`, `Notes`). Keep them concise and stable so users can scan quickly.

3. **Nested Lines**
   - Under each parent bullet, indent every metric with two leading spaces before `-`.
   - Each nested bullet must present exactly one metric or directive, formatted as `Emoji Label: brief result`.
   - Lead with the status emoji (`✅`, `⚠️`, `❌`); add one space after ✅/❌ and two spaces after ⚠️ to offset its narrower width (`✅ Macro calendar: Clear`, `⚠️  Margin headroom: Tight`).

4. **Context Add-ons**
   - Only add a follow-up nested bullet when absolutely necessary to clarify the prior line. Cap it at ~6 words.
   - Avoid multi-column tables, inline slash-separated metrics, or long paragraphs. The goal is rapid comprehension.

5. **Numerics & Units**
   - Apply consistent number formatting: thousands separators (`6,874.47`), percentage symbols with two decimals when precision matters (`0.75%`), and currency symbols for dollar values (`$7,946`).
   - If a guardrail is breached, follow the emoji with a concise reason (`⚠️  Margin headroom: $750, below floor`). Skip redundant commentary when the emoji speaks for itself.

6. **Closing Line**
   - End the proposal with the next required decision or acknowledgement so the workflow keeps moving (`Need confirmation to stage order`, `Monitoring until 14:00 ET`, etc.).

## Examples

- **0DTE Iron Condor**
  - Parent bullets: `Prereqs`, `Market`, `Indicators`, `Sizing`, `Structure`, `Plan`.
  - Metrics: `✅ Macro calendar: Clear`, `✅ Margin headroom: $142,000`.

- **Wheel Cycle**
  - Parent bullets: `Prereqs`, `Capital`, `Market`, `Indicators`, `Entry Score`, `Orders`, `Plan`, `Next`.
  - Metrics: `⚠️  Net Liq: $512,430, 26% wheels`, followed by optional mitigation bullet.

Use this skill whenever a persona produces proposal-style output so formatting stays uniform across strategies.
