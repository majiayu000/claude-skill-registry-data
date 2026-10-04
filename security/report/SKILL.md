---
name: report
description: Generate a NullPointer Studio styled PDF penetration test report from findings.json. Produces a professional dark-themed PDF with executive summary, risk dashboard, per-finding cards with business risk, remediation summary, and clean controls section.
argument-hint: "[target name] [optional: findings.json path] [optional: output path]"
user-invocable: true
---

# NullPointer Studio Pentest Report Generator

## Purpose

Read `findings.json` from the current pentest session and generate a complete, client-ready penetration test report as a styled PDF. The report follows the NullPointer Studio dark theme with healthcare-aware business risk language per finding.

Load `refs/style.md` for the full CSS specification and color palette before writing any HTML.

---

## Tools Available

| Tool | Use for |
|------|---------|
| `Read` | Read findings.json, session.json, pocs/*.http files |
| `Bash` | Run `python3 report_generator.py` to produce the PDF |
| `Write` | Write the generated Python script |
| `report(action="note", ...)` | Log generation decisions |

---

## Workflow

### Step 0 — Collect inputs

1. Determine the `findings.json` path:
   - If `$ARGUMENTS` provides a path, use it
   - Otherwise use `./findings.json` (repo root)

2. Read `findings.json` — extract all entries where `type == "finding"` (skip `diagram` and `note` entries). For each finding, capture:
   - `id`, `title`, `severity`, `target`, `description`, `evidence`, `tool_used`
   - `reproduction` (command + steps) if present
   - `remediation` (diff / before / after / verification) if present
   - `cve` if present

3. Read `session.json` if it exists — extract:
   - `target` (base URL)
   - `depth`
   - `start_time` (format as date for report)
   - `skill` (used as engagement type)

4. Scan `pocs/` for `.http` files — map each file to its finding by matching filename keywords against finding titles.

5. Call `report(action="note", ...)` with: finding count by severity, target, output path.

---

### Step 1 — Deduplicate and classify findings

Group findings by severity. Within each group, deduplicate on normalized title (same title = same finding, keep the one with more evidence). Sort order for report:

```
CRITICAL → HIGH → MEDIUM → LOW → INFO
```

Compute stat box counts:
- Count findings in each severity bucket
- Total = sum of all

---

### Step 2 — Write the generator script

Write a Python script `report_generator.py` to the repo root. The script must:

1. Import `json`, `base64`, `html`, `pathlib.Path`, `datetime`, `weasyprint`

2. Embed the NullPointer Studio CSS from `refs/style.md` verbatim as `CSS_STR`

3. Load the logo:
   ```python
   LOGO_PATH = Path("/Users/riccardo.tencate/Desktop/agent-smith/templates/FullLogo_Transparent.png")
   with open(LOGO_PATH, "rb") as f:
       LOGO_SRC = "data:image/png;base64," + base64.b64encode(f.read()).decode()
   ```

4. Define `SEV_META` dict:
   ```python
   SEV_META = {
       "critical": {"label": "CRITICAL", "color": "#ff4d6d", "bg": "rgba(255,77,109,0.12)", "border": "#ff4d6d"},
       "high":     {"label": "HIGH",     "color": "#ff8c42", "bg": "rgba(255,140,66,0.12)",  "border": "#ff8c42"},
       "medium":   {"label": "MEDIUM",   "color": "#ffd166", "bg": "rgba(255,209,102,0.1)",  "border": "#ffd166"},
       "low":      {"label": "LOW",      "color": "#5bf29b", "bg": "rgba(91,242,155,0.08)",  "border": "#5bf29b"},
       "info":     {"label": "INFO",     "color": "#7b78ff", "bg": "rgba(123,120,255,0.08)", "border": "#7b78ff"},
   }
   ```

5. Define helper functions:
   ```python
   def esc(s): return html.escape(str(s))
   def badge(sev): ...   # colored inline badge span
   def code(text): ...   # <pre class="code-block"><code>...</code></pre>
   ```

6. Define `finding_section(np_id, severity, title, owasp, asvs, endpoint, auth, confirmed, description, business_risk, evidence, steps, remediation)` — see `refs/style.md` for the exact HTML structure.

7. Build the full HTML document (cover page → stat boxes → exec summary → scope → risk dashboard → findings → remediation table → clean controls) and write it via `weasyprint`.

**Script skeleton:**

```python
#!/usr/bin/env python3
import json, base64, html as html_mod, datetime
from pathlib import Path
from weasyprint import HTML as WeasyprintHTML

BASE_DIR = Path(".")
OUTPUT   = BASE_DIR / "report_{target_slug}_{date}.pdf"

# ... helpers, CSS, content sections ...

if __name__ == "__main__":
    html_content = build_html()
    Path("report.html").write_text(html_content, encoding="utf-8")
    WeasyprintHTML(string=html_content, base_url=str(BASE_DIR)).write_pdf(str(OUTPUT))
    print(f"PDF → {OUTPUT}")
```

---

### Step 3 — Populate report sections

#### Cover page

```
[Logo — 180px height]
CONFIDENTIAL  (red monospace badge)
Penetration Test Report  (28pt Chakra Petch bold)
{target domain}  (14pt green Chakra Petch)
───────────────────────────────
Client      | {client name}
Target      | {base URL}
Test type   | Web App Pentest + White-Box Code Review
Framework   | {detected framework if known}
Test date   | {date}
Report date | {today}
Prepared by | NullPointer Studio
Version     | 1.0
```

#### Stat boxes (one per severity)

Show counts for CRITICAL, HIGH, MEDIUM, LOW, INFO, and Total. Color each number with the severity accent color. Only include severity boxes that have at least 1 finding — always show Total.

#### Executive Summary

Write a 3–4 paragraph summary covering:
1. What was tested, what methodology, what environment
2. The most critical finding(s) — name them by NP-ID and title, explain the real impact in one sentence each
3. Medium/Low/Info summary in aggregate (count + theme)
4. What was found to be solid (clean controls) — 1–2 sentences

Do NOT use generic templates — derive every sentence from the actual findings in `findings.json`. Healthcare impact language where relevant.

#### Risk Dashboard table

Columns: ID | Severity | Title | OWASP | Status

Show all findings in severity order. Use `badge(sev)` for the severity cell. Status = "Confirmed" for all non-info findings, "Informational" for info.

#### Finding cards

For each finding, render a card using `finding_section(...)`. Map `findings.json` fields as follows:

| Card field | Source |
|---|---|
| np_id | Assign sequentially: NP-001, NP-002, ... in severity order |
| severity | `finding.severity` |
| title | `finding.title` |
| owasp | `finding.owasp` if present, else derive from category (see mapping below) |
| asvs | `finding.asvs` if present, else `"—"` |
| endpoint | `finding.target` (strip base URL if possible) |
| auth | Infer from description ("Yes" if mentions session/auth, "No" if unauthenticated) |
| confirmed | "Yes — live PoC" if poc file exists, "Yes — code review" if code-only, else "Yes" |
| description | `finding.description` — wrap in `<p>` tags, convert code blocks to `code()` helper |
| business_risk | `<div class='risk-box'><strong>Impact:</strong> ...</div>` — derive from description; if healthcare context: reference GDPR/AVG, WBGO, PHI, care continuity |
| evidence | `finding.evidence` + PoC file content if available |
| steps | `finding.reproduction.steps` if present, else derive 3-step reproduction from description |
| remediation | `finding.remediation` code/diff if present, else derive from description |

**OWASP category mapping** (use if not explicit in finding):

| Keywords in title/description | OWASP |
|---|---|
| injection, sqli, xss, ssti, xxe | A03:2021 — Injection |
| auth, password, session, token, mfa, 2fa | A07:2021 — Identification and Authentication Failures |
| access control, idor, privilege, admin | A01:2021 — Broken Access Control |
| rate limit, config, header, tls, cors | A05:2021 — Security Misconfiguration |
| upload, file, deserialization | A04:2021 — Insecure Design |
| api, endpoint, no auth | API2:2023 — Broken Authentication |
| crypto, hash, weak | A02:2021 — Cryptographic Failures |

#### Remediation Summary table

Columns: ID | Severity | Title | Priority | Effort | Fix (one-line)

Assign priority based on severity:
- CRITICAL → P0 — Immediate
- HIGH → P0 — Immediate
- MEDIUM → P2 — Next sprint (or P1 — This sprint for the most impactful)
- LOW → P3 — Milestone or P4 — Backlog
- INFO → — (no priority)

Effort: Low (config change, 1-liner fix), Medium (refactor needed), High (architecture change).

#### Clean controls

If `session.json` or the findings list contains explicit "tested clean" notes, include a "Controls Tested — No Issues Found" table. If no clean controls are documented, omit this section.

---

### Step 4 — Generate the PDF

```bash
python3 report_generator.py
```

If weasyprint is not installed: `pip install weasyprint` first.

After generation, print:
```
Report generated:
  PDF  → ./report_{target}_{date}.pdf
  HTML → ./report_{target}_{date}.html
  Findings: {N} total ({crit} critical, {high} high, {med} medium, {low} low, {info} info)
```

---

## Rules

- **Never invent findings** — only include what is in `findings.json`
- **Business risk is mandatory for every finding** — derive from the actual finding; never write "could potentially" — write what an attacker concretely achieves
- **NP-IDs must be sequential** in severity order (NP-001 = most severe)
- **INFO findings** get a simplified card: Description + Business Risk + Recommendations only (no Evidence/Steps headers unless evidence is meaningful)
- **Logo path** is always `/Users/riccardo.tencate/Desktop/agent-smith/templates/FullLogo_Transparent.png`
- **Output filename**: `report_{target_slug}_{YYYY-MM-DD}.pdf` where target_slug = domain with dots replaced by underscores
- **weasyprint** is the only supported PDF engine — do not use pdfkit, xhtml2pdf, or headless Chrome
- Load `refs/style.md` before writing any HTML or CSS — never invent new colors or fonts
