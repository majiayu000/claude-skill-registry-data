---
name: deep-research-compilation
description: Compile multiple research reports (.docx/.md/.pdf/.pptx/.html/.txt/URLs) into one unified document (.docx, .pdf, or .md) with deduplicated inline [N].
---

# Deep Research Compilation

This skill is the agent-driven, template-matching playbook for compiling multi-source research into a single unified document. It replaces the older script-based approach: every invocation, **you (the agent) do the generation work yourself** -- inspect the template, synthesize content, write a throwaway python-docx program tailored to that template, run it, validate the output. No persistent generator exists and none should be written.

## When to Use This Skill

- The user has several research sources (Claude Desktop outputs, Gemini deep-research, ChatGPT reports, Word/PDF whitepapers, URLs, Markdown drafts) and wants them compiled into one coherent document.
- The user wants the output to visually match a specific Word template they supply or pick from the defaults.
- The output must carry clickable inline `[N]` citations that link to a References section whose entries are themselves clickable hyperlinks to external sources.
- One or more output formats is required: `.docx` (primary), `.pdf` (via conversion from `.docx`), or `.md` (lightweight variant).

**Trigger phrases**: "compile these reports", "merge this research", "combine these documents with references", "consolidate my deep research output", "build a unified report from these sources", "compile deep research", "merge my literature review", "merge into a Word doc matching this template".

## Core Principle

**You are the generator.** There is no `scripts/compile_deep_research.py`. There is no hardcoded Python function that emits docx. Per invocation, you:

1. Read the user's template and build a style profile from its actual XML.
2. Read each input document and normalize into a uniform representation.
3. Synthesize the merged content (deduplicating refs, renumbering citations, eliminating redundancy).
4. Write a one-shot python-docx program adapted to the template's own styles.
5. Run the program via Bash to produce the `.docx`.
6. Convert to `.pdf` (if requested) via `docx2pdf` / `libreoffice`, or emit `.md` directly via the Write tool.
7. Validate the output and iterate if anything fails.

The program you write in step 4 is saved to `<cache_dir>/generate.py` for user reproducibility but is not reused across invocations. Every invocation starts fresh from the current template + content.

### File layout (resolve these paths at the start of the run)

- `<final_dir>` = `<project_root>/docs/compiled/` -- user-facing final outputs only (`.docx`, `.pdf`, `.md`).
- `<cache_dir>` = `<project_root>/.cache/compile-deep-research/<ReportTitle>/` -- every intermediate artifact (`merged.md`, `refs.json`, `style_profile.json`, `generate.py`, `ingest.json`). Recommend the user gitignore `.cache/`.

Never mix the two. The final outputs must not share the directory with intermediates, and the `<Title>_` filename prefix is dropped on artifacts since the subdirectory scopes them.

The anti-patterns that will wreck the output:
- Using a hardcoded brand color (e.g., `#215868`), font (Consolas), or size from one specific source template -- every value must come from the template's own styles.xml.
- Using `paragraph.style = doc.styles["Heading 1"]` in python-docx -- this silently fails on templates where the style isn't already applied in the body. Always write `<w:pStyle w:val="StyleId">` directly into the paragraph's `<w:pPr>`.
- Flattening `[N]` citations to plain text -- they must be the 3-run superscript + internal-hyperlink pattern or Word won't navigate.
- Skipping the post-generation validation -- "Word found unreadable content" warnings and empty TOCs are caught here.

---

## Step 1: Inspect the .docx Template

Before synthesizing or generating anything, build a **style profile** of the selected template. Write it to `<cache_dir>/style_profile.json` so the user can review what you extracted.

### Procedure

```python
import json, re, zipfile
from pathlib import Path

TEMPLATE = Path(template_path)
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
from lxml import etree

with zipfile.ZipFile(TEMPLATE) as z:
    styles_xml  = z.read("word/styles.xml")
    theme_xml   = z.read("word/theme/theme1.xml")
    settings_xml = z.read("word/settings.xml")
    numbering_xml = z.read("word/numbering.xml") if "word/numbering.xml" in z.namelist() else None
    header_parts = [n for n in z.namelist() if n.startswith("word/header") and n.endswith(".xml")]
    footer_parts = [n for n in z.namelist() if n.startswith("word/footer") and n.endswith(".xml")]

styles_root = etree.fromstring(styles_xml)
```

### Styles to extract

For each of these `w:styleId`s in `styles.xml`, pull the resolved run + paragraph properties (font family, size in half-points, color hex, bold/italic, smallCaps, alignment, spacing before/after, line spacing, left/right indent, borders):

- `Title`, `Subtitle`
- `Heading1`, `Heading2`, `Heading3`, `Heading4`
- `Normal`, `ListParagraph`, `ListBullet`, `ListNumber`
- `Hyperlink`, `FollowedHyperlink`
- `TableGrid`
- `TOCHeading`, `TOC1`, `TOC2`, `TOC3`
- `Header`, `Footer`

Helper:

```python
def style_rpr(styles_root, style_id):
    w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    for s in styles_root.iter(f"{w}style"):
        if s.get(f"{w}styleId") == style_id:
            rpr = s.find(f"{w}rPr")
            ppr = s.find(f"{w}pPr")
            return rpr, ppr
    return None, None
```

Extract `rFonts@w:ascii`, `sz@w:val` (half-points), `color@w:val`, `b`, `i`, `smallCaps`, `u@w:val`; for paragraph: `jc@w:val`, `spacing@w:before/after/line`, `ind@w:left/right/hanging`, `pBdr>bottom/top@w:val/sz/color`. Treat missing values as inherited from the base style (follow `basedOn`).

### Header/footer detection

For each `word/header*.xml` and `word/footer*.xml`, capture: is it empty? does it have a `<w:pBdr>`? what are the three tab stops (left / center / right)? Does it reference `dc:title` or `dc:creator` via an `<w:sdt>` data-binding? This determines whether you need to populate header/footer text or rely on core-properties auto-population.

### Theme colors

Read `a:clrScheme` from `theme1.xml` to resolve any `w:themeColor="accentN"` references you see in styles.xml.

### Example style profile (what good output looks like)

```json
{
  "template": "branded-report-template.docx",
  "title": {"font": "Consolas", "size_pt": 32, "color": "#215868", "smallCaps": true, "align": "center", "border_bottom": {"sz_pt": 2.25, "color": "#244061"}},
  "subtitle": {"font": "Consolas", "size_pt": 26, "color": "#31849B", "smallCaps": true, "align": "center"},
  "heading1": {"font": "Calibri Light", "size_pt": 22, "color": "#215868", "bold": true, "smallCaps": true, "spacing_before_pt": 18, "spacing_after_pt": 12, "border_bottom": {"sz_pt": 1, "color": "#215868"}},
  "heading2": {"font": "Calibri Light", "size_pt": 16, "color": "#215868", "bold": true, "smallCaps": true, "spacing_before_pt": 12, "spacing_after_pt": 6},
  "heading3": {"font": "Calibri Light", "size_pt": 14, "color": "#215868", "bold": true, "smallCaps": true},
  "heading4": {"font": "Calibri Light", "size_pt": 12, "color": "#215868", "bold": true, "italic": true, "smallCaps": true},
  "normal":   {"font": "Calibri", "size_pt": 11, "color": "auto", "line_spacing": 1.15, "space_after_pt": 10},
  "hyperlink": {"color": "#2E74B5", "underline": "single"},
  "followed_hyperlink": {"color": "#800080", "underline": "single"},
  "table_grid": {"borders": "default"},
  "toc_heading": {"based_on": "Heading1"},
  "toc": {"levels": "1-3", "tab_leader": "dots"},
  "header": {"first_page_empty": true, "default": {"has_bottom_border": true, "tab_left": "{{dc:title}}", "tab_center": "", "tab_right": "{{user_supplied}}"}},
  "footer": {"first_page_empty": true, "default": {"has_top_border": true, "tab_left": "{{dc:creator}}", "tab_center": "Confidential - Do Not Distribute", "tab_right": "Page {PAGE} of {NUMPAGES}"}},
  "metadata_table": {"col1_in": 1.31, "col2_in": 5.38, "border_top_bottom_color": "#BFBFBF", "border_sides": "none"},
  "citation": {"size_pt": 9, "color_override": "#2E74B5", "vertAlign": "superscript"},
  "reference_entry": {"size_pt": 10, "hanging_in": 0.5, "spacing_before_pt": 3, "spacing_after_pt": 3, "url_size_pt": 9, "url_color": "#2E74B5"},
  "sectPr_preserved": true,
  "title_pg": true
}
```

Every number here must come from the template. A different template (e.g. a plain corporate white/blue) will produce a profile with different values, and your generated `.docx` must follow those values -- not the example values above.

### Summarize to the user

Before generation, describe the profile in plain language so the user can confirm it reads the template correctly:

> Template analyzed: `<name>`. Title style = Consolas 32 pt teal (`#215868`) smallCaps centered with a navy bottom rule. Body = Calibri 11 pt. H1-4 all Calibri Light smallCaps in the same teal; H1 adds a 1 pt teal underline. Hyperlinks render in medium blue (`#2E74B5`). Metadata table has light-gray row rules with no side borders. TOC uses levels 1-3, dots leader, headings are clickable.

If anything looks wrong, loop back and re-inspect before proceeding.

---

## Step 2: Ingest Input Documents

For each user-provided input, extract a normalized record:

```python
@dataclass
class ExtractedSource:
    source: str
    title: str
    sections: list[dict]    # [{"level": 1-4, "heading": str, "content_md": str}]
    references: list[dict]  # [{"local_num": int, "text": str, "url": str|None, "doi": str|None}]
    citations: list[dict]   # [{"section_idx": int, "char_offset": int, "local_num": int}]
```

### Per-format recipes

**.docx** -- use `python-docx` + raw zipfile XML for fidelity:

```python
import docx
from docx.oxml.ns import qn

d = docx.Document(path)
title = d.core_properties.title or Path(path).stem

sections = []
in_refs = False
ref_buf = []
for p in d.paragraphs:
    style_name = (p.style.name or "").strip()
    text = p.text.strip()
    if not text:
        continue
    if style_name.startswith("Heading"):
        if text.lower() == "references":
            in_refs = True; continue
        if in_refs: in_refs = False
        level = int(re.search(r"(\d)", style_name).group(1)) if re.search(r"\d", style_name) else 1
        sections.append({"level": level, "heading": text, "content_md": ""})
        continue
    if in_refs:
        # Look for external URL hyperlinks on this paragraph
        url = None
        for h in p._element.findall(qn("w:hyperlink")):
            rId = h.get(qn("r:id"))
            if rId and rId in d.part.rels and d.part.rels[rId].is_external:
                url = d.part.rels[rId].target_ref
                break
        ref_buf.append((text, url))
        continue
    if sections:
        sections[-1]["content_md"] += text + "\n\n"

# Citation discovery: superscript runs with bookmark-hyperlinks are true citations.
# Less-formatted docs just use [N] inline, which the regex below picks up.
```

For citation extraction, regex-scan each section's `content_md` for `\[(\d+(?:\s*,\s*\d+)*)\]` patterns. Also, Word's Gemini-style docs often render citations as small superscript text without bookmarks -- when you see a superscript run containing only digits, treat each digit as a citation local_num.

**.md** -- stdlib regex:

```python
CITATION_RE = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")
REF_LINK_RE = re.compile(r"^\[(\d+)\]:\s*(https?://\S+)\s*$", re.MULTILINE)
REF_HDG_RE  = re.compile(r"^#+\s*references\s*$", re.IGNORECASE | re.MULTILINE)

body, refs_text = split_on(REF_HDG_RE, raw)
sections = parse_headings(body)       # split on ^#{1,4}\s+...$
inline_cites = CITATION_RE.findall(body)
refs = parse_refs_block(refs_text)    # see Step 4 "Reference block parser"
```

**.pdf** -- `pypdf`:

```python
import pypdf
reader = pypdf.PdfReader(path)
full = "\n\n".join(p.extract_text() or "" for p in reader.pages)
if not full.strip():
    raise RuntimeError(f"{path}: no text layer -- OCR is out of scope")
```

Then apply the same heading heuristic as `.txt` (ALL-CAPS or underlined short lines).

**.pptx** -- `python-pptx`, one slide per section:

```python
from pptx import Presentation
prs = Presentation(path)
for idx, slide in enumerate(prs.slides, start=1):
    heading = (slide.shapes.title.text_frame.text.strip()
               if slide.shapes.title and slide.shapes.title.has_text_frame
               else f"Slide {idx}")
    body = "\n\n".join(s.text_frame.text for s in slide.shapes
                       if s != slide.shapes.title and s.has_text_frame)
```

**.html + URL** -- `beautifulsoup4` + `httpx`:

```python
import httpx
from bs4 import BeautifulSoup
html = (httpx.get(url, timeout=30, follow_redirects=True,
                  headers={"User-Agent": "compile-deep-research/1.0"}).text
        if url.startswith("http") else Path(url).read_text())
soup = BeautifulSoup(html, "html.parser")
for tag in soup(["script", "style", "noscript"]): tag.decompose()
# headings from <h1-h3>, paragraphs from <p>, refs from <a href> inside a section
# whose heading text contains "reference"
```

**.txt** -- regex heuristics:

- Heading pattern 1: ALL-CAPS short line (len 4-80, no terminal period).
- Heading pattern 2: any short line followed immediately by a line of `=` or `-` (underline style).
- References: everything after an isolated line `References` (case-insensitive).

### Parsing the References block (applies to every format)

References come in many forms. Use this layered approach:

1. **Line-anchored numbered**: each line starts with `[N]`, `N.`, or `N)`. Group continuation lines (no such prefix) into the prior entry.
2. **Markdown reference-link syntax**: `^\[N\]:\s*(https?://\S+)$` -- extract directly.
3. **Fallback**: split on blank lines; treat each paragraph as one entry.

For each entry text, run `URL_RE` and `DOI_RE` over it to pull structured values:

```python
URL_RE = re.compile(r"https?://[^\s\)\]\">]+", re.IGNORECASE)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s\"',<>]+", re.IGNORECASE)
```

---

## Step 3: Synthesize Unified Content

This is intellectual work, not mechanical. Write the merged markdown yourself after reading every extracted section from every source.

### Rules

1. **No redundancy.** If three inputs each describe "market size" or "competitive landscape", produce *one* paragraph that integrates what each says, with citations to each contributing source. Do not emit three separate paragraphs that say the same thing.
2. **Preserve specificity.** Given two versions of a fact, keep the one with concrete numbers, names, and dates.
3. **Stitch cross-references.** If input A defines a term and input B uses it, keep the definition near its first use in the merged document.
4. **Name body sections after actual themes.** Not "Background / Analysis / Conclusion" but "Clinical Evidence / Competitive Landscape / Regulatory Roadmap / Strategic Positioning" -- whatever the material actually covers.
5. **Propose the section list to the user.** Before writing the merged markdown, show the planned outline (H1s + H2s + optional H3s). Offer up to 3 edit iterations.
6. **Prefer tables over multi-column bullets** for comparative data. Limit tables to 15 rows x 5 columns.
7. **Illustrate sparingly.** Insert `[Figure N: title]` placeholders with a caption sentence where a diagram would add clarity. Do not try to generate actual figures in the `.docx` -- placeholders are intentional.

### Mandated structure

```
(Title page)
# Document's Purpose            -- one paragraph, then metadata table
(TOC inserted here)
# Executive Summary             -- 300-500 words, self-contained
  ## <H2 per body theme>
# <Body H1 #1>                  -- 3-10 H2 subsections
  ## <subtopic>
# <Body H1 #2>
  ...
# <Body H1 #N>                  -- 3-7 body H1s total
# Conclusion                    -- 1-3 paragraphs synthesizing takeaways
# References                    -- emitted from canonical ref list
```

### Write the merged markdown

Save to `<cache_dir>/merged.md`. Every sentence that carried a citation in the source retains one, with the canonical `[N]` number. No `# Table of Contents` heading. Wrap Document's Purpose in `<!-- PRE-TOC -->...<!-- /PRE-TOC -->` so the generator knows where the TOC inserts.

This `merged.md` is an intermediate. The final user-facing `.md` output (when the user requests Markdown) lives at `<final_dir>/<ReportTitle>.md` and is produced in Step 6 by wrapping this file with a title heading, a manual linked TOC, `<sup>[[N]](#refN)</sup>` citation anchors, and a References section with `<a id="refN">` anchors.

Target: 700-1300 lines.

---

## Step 4: Reference Management

After ingesting, consolidate references across all inputs.

### Deduplication

Priority order:

1. **DOI** -- case-insensitive exact match.
2. **Normalized URL** -- lowercase host, strip `www.`, strip fragment, drop `utm_*` / `fbclid` / `gclid` / `ref*` query params, strip trailing slash.
3. **Title fuzzy match** -- `rapidfuzz.fuzz.token_set_ratio >= 85` on the first 80 chars of the entry text (lowercased, punctuation-stripped). Fallback to `difflib.SequenceMatcher.ratio()` if `rapidfuzz` is missing.

```python
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
TRACK = {"utm_source","utm_medium","utm_campaign","utm_term","utm_content","fbclid","gclid","ref","ref_src","ref_url"}
def norm_url(u):
    if not u: return None
    p = urlparse(u.strip())
    host = p.netloc.lower().removeprefix("www.")
    q = urlencode([(k,v) for k,v in parse_qsl(p.query) if k.lower() not in TRACK])
    return urlunparse(((p.scheme or "https").lower(), host, p.path.rstrip("/"), "", q, ""))
```

### Renumbering

Build `canonical: [{num, text, url, doi}]` (1-indexed) and `renumbering: {source_path: {local_num: canonical_num}}`. Then rewrite every `[N_local]` in every `content_md` to `[N_canonical]` using the per-source renumbering map.

For a paragraph that had `[1,3]` in source A and source B's `[1]` maps to canonical 4, the merged paragraph reads `[1,3,4]` (sorted, deduped).

### Present to the user

> Reference deduplication: 34 input references across 3 sources -> 28 canonical (6 duplicates collapsed). Proceed? [Y/edit]

Allow the user to challenge a specific collapse if they believe two cited works are actually distinct.

---

## Step 5: Write the Python-Docx Generation Program

This is the heart of the skill. You author `<cache_dir>/generate.py` per invocation, adapted to the style profile from Step 1 and the merged markdown from Step 3. Save it, then run it via Bash. The generator writes its output to `<final_dir>/<ReportTitle>.docx`.

### Proven OOXML patterns (copy-adapt these; do not reinvent)

#### A. Open the template and clear the body while preserving sectPr

```python
import docx
from docx.oxml.ns import qn

def clear_body(doc):
    body = doc.element.body
    sectpr_found = False
    for child in list(body):
        if child.tag == qn("w:sectPr"):
            sectpr_found = True
        else:
            body.remove(child)
    assert sectpr_found, "Template missing sectPr -- invalid template"

doc = docx.Document(template_path)
clear_body(doc)
doc.core_properties.title = title
doc.core_properties.author = author
doc.core_properties.last_modified_by = author
doc.core_properties.subject = subtitle
```

#### B. Apply a paragraph style by writing `<w:pStyle>` directly (critical)

**Do not** use `paragraph.style = doc.styles["Heading 1"]`. On a freshly-loaded template with an empty body, python-docx's style collection often does not expose template-defined styles, and the assignment silently falls back to Normal. Write the XML directly:

```python
from docx.oxml import OxmlElement

_STYLE_ID = {
    "Title": "Title", "Subtitle": "Subtitle",
    "Heading 1": "Heading1", "Heading 2": "Heading2",
    "Heading 3": "Heading3", "Heading 4": "Heading4",
    "Normal": "Normal", "Hyperlink": "Hyperlink",
    "Table Grid": "TableGrid", "List Paragraph": "ListParagraph",
    "TOC Heading": "TOCHeading",
}

def apply_style(paragraph, style_name):
    style_id = _STYLE_ID.get(style_name, style_name.replace(" ", ""))
    p = paragraph._p
    pPr = p.find(qn("w:pPr")) or OxmlElement("w:pPr")
    if pPr.getparent() is None:
        p.insert(0, pPr)
    for existing in pPr.findall(qn("w:pStyle")):
        pPr.remove(existing)
    el = OxmlElement("w:pStyle")
    el.set(qn("w:val"), style_id)
    pPr.insert(0, el)

def apply_table_style(table, style_name):
    style_id = _STYLE_ID.get(style_name, style_name.replace(" ", ""))
    tblPr = table._tbl.tblPr
    for existing in tblPr.findall(qn("w:tblStyle")):
        tblPr.remove(existing)
    el = OxmlElement("w:tblStyle")
    el.set(qn("w:val"), style_id)
    tblPr.insert(0, el)
```

#### C. Run builder with direct XML properties

```python
def add_run(paragraph, text, *, bold=False, italic=False, font=None,
            size_half_pt=None, color_hex=None, superscript=False,
            underline=False, rstyle=None):
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    if rstyle:
        el = OxmlElement("w:rStyle"); el.set(qn("w:val"), rstyle); rPr.append(el)
    if bold:   rPr.append(OxmlElement("w:b"))
    if italic: rPr.append(OxmlElement("w:i"))
    if font:
        el = OxmlElement("w:rFonts")
        for a in ("w:ascii","w:hAnsi","w:cs"):
            el.set(qn(a), font)
        rPr.append(el)
    if size_half_pt is not None:
        for tag in ("w:sz","w:szCs"):
            el = OxmlElement(tag); el.set(qn("w:val"), str(size_half_pt)); rPr.append(el)
    if color_hex:
        el = OxmlElement("w:color"); el.set(qn("w:val"), color_hex); rPr.append(el)
    if underline:
        el = OxmlElement("w:u"); el.set(qn("w:val"), "single"); rPr.append(el)
    if superscript:
        el = OxmlElement("w:vertAlign"); el.set(qn("w:val"), "superscript"); rPr.append(el)
    if len(rPr):
        r.append(rPr)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    r.append(t)
    paragraph._p.append(r)
    return r
```

#### D. Internal hyperlink (for citations: target = bookmark `_RefN`)

```python
def add_internal_link(paragraph, anchor, text, *, color_hex, superscript=True, size_half_pt=18):
    hyp = OxmlElement("w:hyperlink")
    hyp.set(qn("w:anchor"), anchor)
    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    for tag, attr in [("w:rStyle","Hyperlink")]:
        el = OxmlElement(tag); el.set(qn("w:val"), attr); rPr.append(el)
    el = OxmlElement("w:color"); el.set(qn("w:val"), color_hex); rPr.append(el)
    el = OxmlElement("w:u"); el.set(qn("w:val"), "single"); rPr.append(el)
    for tag in ("w:sz","w:szCs"):
        el = OxmlElement(tag); el.set(qn("w:val"), str(size_half_pt)); rPr.append(el)
    if superscript:
        el = OxmlElement("w:vertAlign"); el.set(qn("w:val"), "superscript"); rPr.append(el)
    r.append(rPr)
    t = OxmlElement("w:t"); t.text = text; r.append(t)
    hyp.append(r)
    paragraph._p.append(hyp)
```

#### E. External hyperlink (for reference URLs)

```python
from docx.opc.constants import RELATIONSHIP_TYPE as RT

def add_external_link(paragraph, url, text, *, color_hex, size_half_pt=None, underline=True):
    rId = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyp = OxmlElement("w:hyperlink"); hyp.set(qn("r:id"), rId)
    r = OxmlElement("w:r"); rPr = OxmlElement("w:rPr")
    el = OxmlElement("w:rStyle"); el.set(qn("w:val"), "Hyperlink"); rPr.append(el)
    el = OxmlElement("w:color"); el.set(qn("w:val"), color_hex); rPr.append(el)
    if underline:
        el = OxmlElement("w:u"); el.set(qn("w:val"), "single"); rPr.append(el)
    if size_half_pt is not None:
        for tag in ("w:sz","w:szCs"):
            el = OxmlElement(tag); el.set(qn("w:val"), str(size_half_pt)); rPr.append(el)
    r.append(rPr)
    t = OxmlElement("w:t"); t.text = text; r.append(t)
    hyp.append(r); paragraph._p.append(hyp)
```

#### F. Bookmark wrapping a paragraph

```python
def add_bookmark(paragraph, name, bookmark_id):
    start = OxmlElement("w:bookmarkStart")
    start.set(qn("w:id"), str(bookmark_id))
    start.set(qn("w:name"), name)
    end = OxmlElement("w:bookmarkEnd"); end.set(qn("w:id"), str(bookmark_id))
    paragraph._p.insert(0, start)
    paragraph._p.append(end)
```

Use a single monotonic counter for bookmark IDs across the whole document.

#### G. Settings: make TOC refresh on open

```python
def set_update_fields(doc):
    settings = doc.settings.element
    existing = settings.find(qn("w:updateFields"))
    if existing is None:
        el = OxmlElement("w:updateFields"); el.set(qn("w:val"), "true")
        settings.append(el)
    else:
        existing.set(qn("w:val"), "true")
```

#### H. TOC as an SDT + field code

```python
def insert_toc(doc):
    p_h = doc.add_paragraph()
    apply_style(p_h, "TOC Heading")
    add_run(p_h, "Table of Contents")

    p = doc.add_paragraph()
    # field begin
    r = OxmlElement("w:r"); el = OxmlElement("w:fldChar")
    el.set(qn("w:fldCharType"), "begin"); el.set(qn("w:dirty"), "true")
    r.append(el); p._p.append(r)
    # instruction
    r = OxmlElement("w:r"); el = OxmlElement("w:instrText")
    el.set(qn("xml:space"), "preserve"); el.text = 'TOC \\o "1-3" \\h \\z \\u'
    r.append(el); p._p.append(r)
    # separator
    r = OxmlElement("w:r"); el = OxmlElement("w:fldChar")
    el.set(qn("w:fldCharType"), "separate"); r.append(el); p._p.append(r)
    # placeholder text shown before F9/auto-refresh
    r = OxmlElement("w:r"); t = OxmlElement("w:t")
    t.text = "Right-click and select Update Field to refresh the Table of Contents."
    r.append(t); p._p.append(r)
    # field end
    r = OxmlElement("w:r"); el = OxmlElement("w:fldChar")
    el.set(qn("w:fldCharType"), "end"); r.append(el); p._p.append(r)
```

#### I. Title page (driven by the style profile, not hardcoded values)

```python
def emit_title_page(doc, profile, title, subtitle, date):
    # leading blank Title paragraphs for the style's border-rule rhythm
    for _ in range(2):
        p = doc.add_paragraph(); apply_style(p, "Title")
        p.alignment = 1  # center

    p = doc.add_paragraph(); apply_style(p, "Title"); p.alignment = 1
    tp = profile["title"]
    add_run(p, title,
            font=tp["font"],
            size_half_pt=int(tp["size_pt"]*2),
            color_hex=tp["color"].lstrip("#"))

    if subtitle:
        for _ in range(2):
            p = doc.add_paragraph(); apply_style(p, "Subtitle"); p.alignment = 1
        p = doc.add_paragraph(); apply_style(p, "Subtitle"); p.alignment = 1
        sp = profile["subtitle"]
        add_run(p, subtitle,
                font=sp["font"],
                size_half_pt=int(sp["size_pt"]*2),
                color_hex=sp["color"].lstrip("#"))

    for _ in range(3):
        p = doc.add_paragraph(); apply_style(p, "Subtitle"); p.alignment = 1

    if date:
        p = doc.add_paragraph(); apply_style(p, "Subtitle"); p.alignment = 1
        # date is typically smaller + gray; if profile doesn't carry explicit
        # date styling, derive: 18 pt, #808080
        add_run(p, date,
                font=profile["subtitle"]["font"],
                size_half_pt=36, color_hex="808080", italic=True)

    # Hard page break to start the body on page 2
    p = doc.add_paragraph()
    r = OxmlElement("w:r"); br = OxmlElement("w:br"); br.set(qn("w:type"), "page")
    r.append(br); p._p.append(r)
```

Note: every value (font, size, color) comes from `profile`. A different template with a red/black corporate look produces `profile["title"] = {"font": "Arial Black", "size_pt": 44, "color": "#CC0000", ...}` and the generated `.docx` matches that.

#### J. Metadata table with borderless outer + light-gray row rules

```python
from docx.shared import Inches

def emit_metadata_table(doc, profile, author, last_updated):
    table = doc.add_table(rows=2, cols=2)
    apply_table_style(table, "Table Grid")
    mt = profile["metadata_table"]
    table.columns[0].width = Inches(mt["col1_in"])
    table.columns[1].width = Inches(mt["col2_in"])

    tblPr = table._tbl.tblPr
    for existing in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(existing)
    borders = OxmlElement("w:tblBorders")
    specs = [
        ("w:top",    "single", "4", "808080"),
        ("w:left",   "nil",    None, None),
        ("w:bottom", "single", "4", "808080"),
        ("w:right",  "nil",    None, None),
        ("w:insideH","single", "4", mt["border_top_bottom_color"].lstrip("#")),
        ("w:insideV","nil",    None, None),
    ]
    for tag, val, sz, clr in specs:
        el = OxmlElement(tag); el.set(qn("w:val"), val)
        if sz:  el.set(qn("w:sz"), sz)
        if clr: el.set(qn("w:color"), clr)
        borders.append(el)
    tblPr.append(borders)

    rows = [("Authors", author or ""), ("Last Updated", last_updated or "")]
    for i, (label, value) in enumerate(rows):
        lp = table.rows[i].cells[0].paragraphs[0]
        add_run(lp, label, bold=True)
        vp = table.rows[i].cells[1].paragraphs[0]
        add_run(vp, value)
```

#### K. Citation run pattern (the 3-run superscript + internal-hyperlink block)

```python
CITATION_RE = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")

def render_inline(paragraph, text, profile):
    # Minimal tokenizer: extract citations first, then bold/italic/code/link.
    cit_color = profile["citation"]["color_override"].lstrip("#")
    cit_sz = int(profile["citation"]["size_pt"] * 2)

    pos = 0
    for m in CITATION_RE.finditer(text):
        if m.start() > pos:
            _render_runs(paragraph, text[pos:m.start()], profile)  # bold/italic/code/link
        nums = [int(n.strip()) for n in m.group(1).split(",")]
        add_run(paragraph, " [", superscript=True, size_half_pt=cit_sz)
        for i, n in enumerate(nums):
            if i > 0:
                add_run(paragraph, ",", superscript=True, size_half_pt=cit_sz)
            add_internal_link(paragraph, f"_Ref{n}", str(n),
                              color_hex=cit_color, size_half_pt=cit_sz, superscript=True)
        add_run(paragraph, "]", superscript=True, size_half_pt=cit_sz)
        pos = m.end()
    if pos < len(text):
        _render_runs(paragraph, text[pos:], profile)
```

`_render_runs` walks markdown-style inline tokens (`**bold**`, `*italic*`, `` `code` ``, `[link](url)`) and emits a run for each. Citations are stripped first so the markdown-link regex cannot eat a `[N]` by mistake.

#### L. References section (one entry per paragraph with hanging indent, bookmark-wrapped)

```python
def emit_references(doc, canonical, profile):
    h = doc.add_paragraph(); apply_style(h, "Heading 1")
    add_run(h, "References")

    re_style = profile["reference_entry"]
    url_color = re_style["url_color"].lstrip("#")

    for idx, ref in enumerate(canonical, start=1):
        p = doc.add_paragraph(); apply_style(p, "Normal")

        # spacing before/after + hanging indent
        pPr = p._p.find(qn("w:pPr"))
        sp = OxmlElement("w:spacing")
        sp.set(qn("w:before"), str(int(re_style["spacing_before_pt"]*20)))
        sp.set(qn("w:after"),  str(int(re_style["spacing_after_pt"]*20)))
        pPr.append(sp)
        ind = OxmlElement("w:ind")
        twips = int(re_style["hanging_in"] * 1440)
        ind.set(qn("w:left"), str(twips))
        ind.set(qn("w:hanging"), str(twips))
        pPr.append(ind)

        add_bookmark(p, f"_Ref{ref['num']}", bookmark_id=1000 + idx)

        add_run(p, f"[{ref['num']}] ", bold=True,
                size_half_pt=int(re_style["size_pt"]*2))

        text = (ref.get("text") or "").strip()
        url = ref.get("url")
        if url and url in text:
            text = text.replace(url, "").rstrip(" .,;")
        if text:
            add_run(p, text + (" " if url else ""),
                    size_half_pt=int(re_style["size_pt"]*2))
        if url:
            add_external_link(p, url, url,
                              color_hex=url_color,
                              size_half_pt=int(re_style["url_size_pt"]*2))
```

#### M. Saving

```python
doc.save(output_path)
```

No `.close()`. python-docx handles the file lifecycle via the context of save.

### Assembly

The overall generator program body:

```python
def main():
    with open(style_profile_path) as f:
        profile = json.load(f)
    merged = Path(merged_md_path).read_text(encoding="utf-8")
    refs = json.load(open(refs_json_path)) if refs_json_path else {"canonical": []}

    doc = docx.Document(template_path)
    clear_body(doc)
    set_update_fields(doc)
    doc.core_properties.title = title
    doc.core_properties.author = author
    doc.core_properties.last_modified_by = author
    doc.core_properties.subject = subtitle

    emit_title_page(doc, profile, title, subtitle, date)

    # Parse merged markdown into (pre_toc_blocks, main_blocks) on PRE-TOC markers
    pre_toc, main = parse_merged_md(merged)

    # Pre-TOC: Document's Purpose + prose, then metadata table
    for blk in pre_toc: render_block(doc, blk, profile)
    emit_metadata_table(doc, profile, author, last_updated=date)

    # TOC then page break
    insert_toc(doc)
    page_break_paragraph(doc)

    # Body: render every block except any `# References` (we emit from refs.json)
    for blk in strip_references_section(main):
        render_block(doc, blk, profile)

    # Hard page break + References
    if refs.get("canonical"):
        page_break_paragraph(doc)
        emit_references(doc, refs["canonical"], profile)

    doc.save(output_path)
    print(f"Wrote {output_path}")

if __name__ == "__main__":
    main()
```

Save this program to `<cache_dir>/generate.py`, embedding the canonical refs + style profile either as `open(...)` reads against the sibling JSON artifacts (`refs.json`, `style_profile.json`), or inlined as literals for full single-file reproducibility. Either is acceptable. Hard-code the `<final_dir>/<ReportTitle>.docx` output path inside the script so the user can re-run it without re-deriving paths.

### Run the program

```bash
python "<cache_dir>/generate.py"
```

If any import fails, the program prints a clear `pip install <pkg>` hint and exits. Dependencies beyond `python-docx` are lazy-imported inside the per-format parsers so the generator runs with just `python-docx` in the typical case.

---

## Step 6: Markdown Output

If the user requested `.md` (alone or with other formats), author it directly with the Write tool at `<final_dir>/<ReportTitle>.md` -- no Python needed. Read the intermediate synthesis from `<cache_dir>/merged.md` and transform it by prepending the title heading, inserting the manual TOC, wrapping each `[N]` as `<sup>[[N]](#refN)</sup>`, and emitting the References section with anchor targets.

Structure:

```markdown
# <Title>

*<Subtitle>*

*<Date>*

---

## Document's Purpose

<prose paragraph>

|  |  |
| --- | --- |
| **Authors** | <Author> |
| **Last Updated** | <Date> |

## Table of Contents

1. [Executive Summary](#executive-summary)
   1.1. [Topic A](#topic-a)
   1.2. [Topic B](#topic-b)
2. [Body Section 1](#body-section-1)
   ...

## Executive Summary

<prose> <sup>[[1](#ref1),[2](#ref2)]</sup>.

...

## References

<a id="ref1"></a>**[1]** Author. "Title." Venue, Date. [https://example.com](https://example.com)

<a id="ref2"></a>**[2]** ...
```

Slug rules for TOC anchors: lowercase, non-word chars -> space, spaces -> `-`, collapse runs, strip leading/trailing `-`. GitHub-compatible.

Citation rendering: replace every `[N]` in the body with `<sup>[[N]](#refN)</sup>`. Multi-citations `[N,M]` become `<sup>[[N](#refN),[M](#refM)]</sup>`.

---

## Step 7: PDF Output

Always via `.docx` -> converter. Do not try to author PDF directly. The PDF output lands at `<final_dir>/<ReportTitle>.pdf`.

```python
def build_pdf(docx_path, pdf_path):
    # Primary: docx2pdf (wraps MS Word on Windows, Word/LibreOffice on macOS)
    try:
        from docx2pdf import convert
        convert(str(docx_path), str(pdf_path))
        if pdf_path.exists():
            return
    except Exception as e:
        print(f"[warn] docx2pdf failed: {e}")

    # Fallback: libreoffice --headless
    import shutil, subprocess
    libre = shutil.which("libreoffice") or shutil.which("soffice")
    if libre:
        try:
            result = subprocess.run(
                [libre, "--headless", "--convert-to", "pdf",
                 "--outdir", str(pdf_path.parent), str(docx_path)],
                timeout=120, capture_output=True, text=True,
            )
            produced = pdf_path.parent / (docx_path.stem + ".pdf")
            if produced.exists():
                if produced != pdf_path:
                    produced.replace(pdf_path)
                return
            print(f"[warn] libreoffice produced no output: {result.stderr}")
        except Exception as e:
            print(f"[warn] libreoffice failed: {e}")

    raise RuntimeError(
        "PDF conversion requires docx2pdf (pip install docx2pdf) or "
        "libreoffice on PATH. Install one and re-run; the .docx is kept for manual export."
    )
```

If only `.pdf` was requested (not `.docx`), delete the intermediate `.docx` after successful conversion. Otherwise keep both.

---

## Step 8: Validate + Iterate

After generating the `.docx`, open it via zipfile and run these checks:

```python
def validate_docx(path):
    import zipfile, re
    with zipfile.ZipFile(path) as z:
        doc = z.read("word/document.xml").decode("utf-8")
    anchors = set(re.findall(r'w:hyperlink w:anchor="(_Ref\d+)"', doc))
    bookmarks = set(re.findall(r'w:bookmarkStart[^/]*w:name="(_Ref\d+)"', doc))
    broken = sorted(anchors - bookmarks)
    orphan = sorted(bookmarks - anchors)

    pstyles = set(re.findall(r'w:pStyle w:val="([^"]+)"', doc))
    heading_styles = {s for s in pstyles if s.startswith("Heading") or s == "Title"}
    toc_present = "TOC " in doc and "w:fldChar" in doc

    issues = []
    if broken: issues.append(f"broken citation anchors: {broken}")
    if not heading_styles: issues.append("no heading styles applied -- TOC will be empty")
    if not toc_present: issues.append("TOC field missing")
    if orphan: issues.append(f"orphan bookmarks: {orphan}")  # warning only, not fatal
    return issues
```

For `.md`:

```python
def validate_md(path):
    text = Path(path).read_text(encoding="utf-8")
    anchors_used = set(re.findall(r"\(#(ref\d+)\)", text))
    anchor_defs = set(re.findall(r'<a id="(ref\d+)"', text))
    broken = sorted(anchors_used - anchor_defs)
    return [f"broken anchors: {broken}"] if broken else []
```

If any **fatal** issue is reported (broken citation anchors, missing heading styles, missing TOC field), diagnose:

- Broken anchors: a citation references a number outside the canonical list. Re-check the renumbering map.
- Missing heading styles: you forgot `apply_style()` on a heading -- check `render_block` for the heading branch.
- Missing TOC: `insert_toc()` wasn't called or its XML is malformed.

Edit `<cache_dir>/generate.py` and re-run. Maximum 3 iterations; if still failing, stop and report the failure to the user with the raw issue list.

---

## Common OOXML Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Word dialog: "Word found unreadable content" | Empty `<w:t>` tags, bad `<w:rPr>` child ordering, missing xml:space="preserve" | Ensure every run's `<w:t>` has text (even if ""); emit `<w:rPr>` children in canonical order (rStyle -> b -> i -> smallCaps -> rFonts -> sz -> szCs -> color -> u -> vertAlign); add `xml:space="preserve"` to every `<w:t>` |
| Headings render as Normal; TOC empty | `paragraph.style = doc.styles["Heading 1"]` silent fail | Always use the `apply_style()` helper that writes `<w:pStyle>` directly via `OxmlElement` |
| Word dialog: "Start by applying a heading style" when refreshing TOC | No paragraphs carry heading styles | Same fix as above |
| Citation hyperlinks don't navigate | Anchor name doesn't match bookmark name | Ensure bookmark is exactly `_RefN` and anchor is exactly `_RefN`; validate post-generation |
| Citation anchors valid but not clickable | Citation emitted as plain text run, not hyperlink | Use the 3-run pattern in Section K |
| References section URLs are blue text but not clickable | External hyperlink created without `RT.HYPERLINK` rel | Always use `paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)` |
| Metadata table keeps the source-template look when applied to a different target template | Hardcoded `#BFBFBF` instead of profile value | Pull border colors from `profile["metadata_table"]` |
| Title page text is the wrong font/size/color | Style profile not used; hardcoded Consolas/Calibri/32pt | Every run-level property must come from `profile[<style_name>]` |
| Page 1 shows the header/footer that should only appear page 2+ | sectPr's `<w:titlePg/>` was dropped during body clearing | `clear_body` must preserve the final `<w:sectPr>` byte-for-byte |
| Duplicate bookmark IDs (Word opens but TOC is broken) | Bookmark ID counter collides with Word's auto-generated IDs | Use IDs >= 1000 for your own bookmarks; never reuse IDs |

---

## Critical Rules

- **Never fabricate citations.** A sentence that had no citation in the source material gets no citation in the merged document.
- **Never silently drop references.** Every canonical reference appears in the final References section even if its inline citation count is zero (it might have been cut during editing -- preserve it for the user to decide).
- **Never hardcode output format.** The command always asks.
- **Always ask for the template.** Silently defaulting is the v1 bug; the command's Phase 2 must be honored.
- **Always validate after generation.** Broken citations and empty TOCs are the common failure modes; catch them before handing off.
- **Every style value comes from the profile.** No hardcoded fonts, colors, or sizes in the generator. When a new template is supplied, the output must visually match it -- never the previous template.
- **Save the generator script.** `<cache_dir>/generate.py` is kept so the user can re-run or tweak it without invoking the command.
- **Separate final outputs from intermediates.** Final outputs live in `<final_dir>` (`docs/compiled/`). Intermediate artifacts live in `<cache_dir>` (`.cache/compile-deep-research/<ReportTitle>/`). Never put intermediates in `docs/`.
