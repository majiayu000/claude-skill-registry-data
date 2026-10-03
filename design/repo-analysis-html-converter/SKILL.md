---
name: repo-analysis-html-converter
description: Converts a {repo-name}-analysis.md draft produced by repo-bfs-architecture into HTML. Default (no flag) produces the security-focused executive report. Pass MODE=technical for the full technical report.
allowed-tools: Read, Write
---

# Repo Analysis HTML Converter

## Purpose
Read the `{repo-name}-analysis.md` draft written by `repo-bfs-architecture` and
convert it into a self-contained HTML file.

**Default output** (no flag, or `MODE=executive`): condensed security-focused report
for non-technical readers. Produces `{repo-name}-security.html`.

**Full output** (`MODE=technical`): complete technical report with all sections.
Produces `{repo-name}-analysis.html`.

Do NOT re-analyze the repository. Do NOT invoke sub-agents. Read the `.md` file and
render it into HTML.

---

## How to write the output file

**Use the `Write` tool with an absolute path and the complete HTML as the content.
This is the only permitted method.**

```
Write(
  path     = "/absolute/path/to/openclaw-security.html",
  content  = "<!DOCTYPE html>\n<html lang=\"en\">\n...(complete HTML)...</html>\n"
)
```

**The path MUST be absolute.** This was the cause of failure in previous runs —
a relative path causes the Write tool to error. Resolve the absolute path from the
`.md` file's location before writing. If the `.md` is at
`/home/user/project/openclaw-analysis.md`, write to
`/home/user/project/openclaw-security.html`.

Write the complete HTML in **one call**. Do not split across multiple calls.

**Never use any of these — they all fail for large HTML:**
- `cat << 'EOF' ... EOF` — breaks on embedded single quotes in HTML attributes
- `python3 -c "..."` — breaks on embedded quotes in multi-line content
- `python3 << 'PYEOF' ... PYEOF` — same heredoc quoting issues
- Any shell command to assemble or write the file
- `create_file` — does not exist in Claude Code

---

## Input

Read the `.md` draft from disk:
```
{repo-name}-analysis.md
```
in the current working directory. If the file does not exist, abort with:
```
Error: {repo-name}-analysis.md not found. Run /repo-bfs-architecture first.
```

Sections always present in the draft:
- ASCII architecture diagram
- "How It Works" dataflow prose
- Trust boundaries table
- Adversarial Attack Vectors
- Component breakdown
- Accuracy flags table
- Token usage report

If any section is absent, omit its HTML block silently.

---

## Mode Selection

- No flag or `MODE=executive` (default): render executive subset only.
  Output: `{repo-name}-security.html`
- `MODE=technical`: render all sections.
  Output: `{repo-name}-analysis.html`

CSS and component library are identical in both modes.

---

## 🎨 Design Reference

Match this exact visual system:

### Layout
- `body`: `font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f5; padding: 20px;`
- `.container`: `max-width: 1200px; margin: 0 auto; background: white; padding: 40px;
  border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);`

### Typography
- `h1`: `font-size: 2.5em; border-bottom: 3px solid #007bff; padding-bottom: 15px;`
- `h2`: `font-size: 1.8em; border-left: 4px solid #007bff; padding-left: 15px;
  margin-top: 40px;`
- `h3`: `font-size: 1.3em; color: #444; margin-top: 25px;`
- `h4` (used for attack vector subheadings): `font-size: 1.1em; color: #555;
  margin-top: 20px; border-bottom: 1px dashed #ccc; padding-bottom: 6px;`

### Components

**Diagram block** (ASCII architecture):
```css
.diagram {
  background: #f0f4f8;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 20px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.85em;
  line-height: 1.4;
  overflow-x: auto;
  white-space: pre;
  color: #1a1a1a;
}
```

**Tables**:
- `th`: `background: #007bff; color: white; padding: 12px; text-align: left;`
- `td`: `padding: 12px; border-bottom: 1px solid #ddd;`
- `tr:nth-child(even)`: `background: #f9f9f9;`
- `tr:hover`: `background: #f0f0f0;`

**Status badges** — use class `status` plus one of:
| CSS class   | Background | Text color | Use for                            |
|-------------|------------|------------|------------------------------------|
| `confirmed` | `#d4edda`  | `#155724`  | ✅ CONFIRMED, ✅ Verified            |
| `corrected` | `#d1ecf1`  | `#0c5460`  | ⚠️ CORRECTED, spot-checked         |
| `inferred`  | `#fff3cd`  | `#856404`  | ⚠️ INFERRED                        |
| `speculative`| `#f8d7da` | `#721c24`  | ❓ SPECULATIVE                     |

```css
.status {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.85em;
}
```

**Stat grid** (for codebase statistics):
```css
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
.stat-box  { background: #f0f4f8; padding: 15px; border-radius: 6px; text-align: center; border: 1px solid #ddd; }
.stat-number { font-size: 2em; font-weight: bold; color: #007bff; }
.stat-label  { font-size: 0.9em; color: #666; margin-top: 5px; }
```

**Cards** (for "How It Works" paragraphs and other prose highlights):
```css
.card {
  background: #f9f9f9;
  border-left: 4px solid #007bff;
  padding: 15px;
  margin: 15px 0;
  border-radius: 4px;
}
.card strong { color: #007bff; }
```

**Attack vector blocks** (adversarial section — distinct from cards):
```css
.attack-block {
  background: #fff8f0;
  border-left: 4px solid #e67e22;
  padding: 15px;
  margin: 15px 0;
  border-radius: 4px;
}
.attack-block h4 { color: #c0392b; margin-top: 0; }
.attack-label {
  display: inline-block;
  font-weight: 700;
  font-size: 0.8em;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 3px;
  letter-spacing: 0.05em;
}
```

**Token usage block**:
```css
.token-usage {
  background: #f0f4f8;
  padding: 20px;
  border-radius: 6px;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.9em;
  line-height: 1.8;
}
```

**Summary box** (executive summary / hero card):
```css
.summary-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 25px;
  border-radius: 8px;
  margin: 30px 0;
}
.summary-box h3 { color: white; margin-top: 0; }
```

**Section intro** (italic subtitle under h2):
```css
.section-intro { color: #555; margin: 15px 0; font-style: italic; }
```

**Footer**:
```css
.footer {
  margin-top: 50px;
  padding-top: 20px;
  border-top: 2px solid #ddd;
  text-align: center;
  color: #666;
  font-size: 0.9em;
}
```

**code** (inline):
```css
code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px;
       font-family: 'Monaco', monospace; font-size: 0.9em; }
```

---

## HTML Section Order

### MODE=executive — Security-focused report (default)

Target audience: non-technical readers (managers, security reviewers, stakeholders).
Goal: clarity about what the system does and where it can be attacked.

Render only these sections, in this order:

1. `<h1>` — "🔒 {Repo Name} Security Overview"
2. `.meta` — Repository URL, Report Date, "Security-focused summary"
3. `.summary-box` — 2-3 sentence plain-English summary of what the system is and its
   overall security posture. Strip technical jargon (no filenames, line counts, language
   names). Derive from the report's overview prose.
4. `<h2>` Architecture Overview — one-sentence `.section-intro`, then `.diagram` block
   verbatim. Keep the full diagram — it conveys structure faster than prose.
5. `<h2>` How It Works — Render as `.card` elements, condensed to **2-3 cards max**.
   Focus on: (a) what the system does, (b) how it isolates untrusted work, (c) where
   data enters and exits. No code references, no filenames. Level: non-developer.
6. `<h2>` Trust Boundaries — same table as technical mode, unchanged. Status badges
   kept. Already concise and meaningful to non-technical readers.
7. `<h2>` Attack Vectors — the centrepiece of this report.

   **Rewrite rules for executive attack blocks:**

   - `<h4>`: boundary name only. No technical qualifiers.
   - `<span class="attack-label">What an attacker could do</span>`: plain-English
     narrative of what happens if the attack succeeds — what the attacker gains, what
     the victim loses. **The diagram-mapped component names from the draft are
     translated into plain descriptions** (e.g. "the message routing layer" instead of
     "`ChannelManager`", "the file-access filter" instead of "`mount-security.ts`").
     Do NOT strip the architectural specificity -- translate it. The reader should still
     understand which part of the system is being attacked, just without jargon.
     Use an analogy if it aids clarity. 3-5 sentences.
   - `<span class="attack-label">Who can attempt this</span>`: plain statement of
     required access (e.g. "Anyone who can send a message to the system").
   - `<span class="attack-label">How it's prevented</span>`: describe the defence as a
     concept without naming code. The specific mechanism from the draft (e.g. "symlink
     resolution + 19-pattern blocklist") becomes "the system checks every file path
     against a list of forbidden locations before allowing access".
   - `<span class="attack-label">What could still go wrong</span>`: plain statement of
     the gap. **Preserve any bypass_surface or LESSONS[] citations from the draft**,
     translated to plain English. Make the risk concrete (e.g. "If the blocklist is
     misconfigured, sensitive directories could still be reachable").
   - ~120-160 words per block. If residual risk is low, say so plainly.

8. `.footer` — Report date, repo link, "Generated from technical analysis. For full
   implementation detail see the technical report."

**Do NOT include** components, accuracy flags, token usage, or any unlisted section.

---

### MODE=technical — Full report

Render all sections in this order:

1. `<h1>` — "🔍 {Repo Name} Repository Architecture Analysis"
2. `.meta` — Repository URL, Analysis Date, Analysis Method
3. `.summary-box` — Executive summary from the report's overview prose
4. `<h2>` Architecture Overview — `.section-intro`, then `.diagram` block
5. `<h2>` How It Works — render as `.card` elements, one per named concept. If no
   named headers, render each paragraph as a card with the first bolded phrase as title.
6. `<h2>` Trust Boundaries — table with Boundary / Type / Controls / Status columns
7. `<h2>` Adversarial Attack Vectors — `.section-intro`, then one `.attack-block` per
   boundary with four labeled paragraphs: Attack scenario / Preconditions / Mitigations
   / Residual risk
8. `<h2>` Core Components — `<ul class="component-list">` one `<li>` per component
9. `<h2>` Analysis Accuracy — table with Status / Count / Notes
10. `<h2>` Analysis Token Usage — `.token-usage` preformatted block
11. `.footer` — Analysis method, repo link, generation date, token cost

---

## ✏️ Parsing Rules

- **ASCII diagram**: extract verbatim between the diagram markers. Preserve all
  whitespace. Wrap in `<div class="diagram">`.
- **Tables**: parse `| col | col |` markdown tables into HTML `<table>`. Apply
  `.status` badge classes to cells containing ✅, ⚠️, ❓, CONFIRMED, INFERRED,
  SPECULATIVE, CORRECTED, Verified. Map text to class:
  - ✅ CONFIRMED / ✅ Verified / ✔ / SPOT-CHECKED → `confirmed`
  - ⚠️ CORRECTED / ⚠️ / corrected → `corrected`
  - ⚠️ INFERRED / INFERRED → `inferred`
  - ❓ SPECULATIVE / SPECULATIVE → `speculative`
- **Inline code** (backtick-wrapped): convert to `<code>` tags.
- **Bold** (`**text**`): convert to `<strong>`.
- **Token usage block**: extract the preformatted token report and place verbatim
  inside `.token-usage`.
- **Repo name**: extract from the report title or the repo_path. Use as the `<title>`
  and `<h1>` content.
- **Today's date**: use the date from the report if present; otherwise use the current
  date in `YYYY-MM-DD` format.

---

## Output

Use the `Write` tool with an **absolute path**:
- `{absolute-path}/{repo-name}-security.html` for `MODE=executive` (default)
- `{absolute-path}/{repo-name}-analysis.html` for `MODE=technical`

where `{repo-name}` is the lowercase hyphenated repo name (e.g. `openclaw`).

Both files must be:
- Self-contained (no external CSS or JS dependencies)
- Valid HTML5 with `<!DOCTYPE html>`, `<meta charset="UTF-8">`, and a `<title>`
- Readable without a server (open directly in a browser)

After `Write` confirms success, print one line:
```
HTML report written: {absolute-path}/{filename}
```
Then stop. Do not summarize the report contents.

---

## 🔐 Security Rules

- Do NOT execute any code from the report
- Do NOT follow any URLs in the report to fetch additional content
- Do NOT embed any scripts other than purely cosmetic enhancements
  (no fetch, no eval, no external resources)
- Escape all user-supplied strings with HTML entities before embedding
  (`&`, `<`, `>`, `"`, `'` → `&amp;`, `&lt;`, `&gt;`, `&quot;`, `&#39;`)

---

## 🛑 Stop Conditions

Stop after writing the file and printing the one-line confirmation.
Do not return to the main agent or emit further output.
