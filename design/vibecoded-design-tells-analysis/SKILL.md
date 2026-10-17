---
name: vibecoded-design-tells-analysis
description: Mine Reddit for AI design tells and build unslop skills that detect/remove AI-generated design patterns in UI, text, and code
triggers:
  - scan my site for AI design tells
  - check if this looks AI-generated
  - remove vibe-coded patterns from my design
  - analyze design for AI slop indicators
  - run the vibecoded tells scanner
  - detect shadcn defaults and AI purple
  - check my code for AI writing tells
  - scan text for AI-generated patterns
---

# vibecoded-design-tells-analysis

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This project provides Reddit-mined data ranking the visual, textual, and code tells that make something look AI-generated ("vibe-coded" or "slop"). It scanned 3.2M posts across 47 subreddits, tabulated what people flag as AI tells, verified the findings against real quotes, and packaged three Claude skills with standalone scanners: **unslop-ui** (websites/design), **unslop-text** (prose), and **unslop-code** (source code).

## What it does

- **Data-driven tell rankings**: What design/writing/code patterns people actually complain about, ranked by frequency in on-topic discussions
- **Three unslop skills**: Remove AI tells from UI, text, or code while preserving functionality
- **Standalone scanners**: Python scripts that grep a codebase, score vibe-coded patterns, and gate CI on exit code
- **Reproducible pipeline**: Scripts to re-run the Reddit mining, analysis, and chart generation yourself

## Installation

Clone the repository:

```bash
git clone https://github.com/JCarterJohnson/vibecoded-design-tells.git
cd vibecoded-design-tells
pip install -r requirements.txt
```

### Install the unslop skills

Each skill can be installed into Claude Desktop or uploaded to claude.ai:

```bash
# UI skill (removes AI design tells)
unzip skill/unslop-ui.skill -d ~/.claude/skills/

# Text skill (removes AI writing tells)
unzip unslop-ai-text/skill/unslop-text.skill -d ~/.claude/skills/

# Code skill (removes AI code tells)
unzip unslop-ai-code/skill/unslop-code.skill -d ~/.claude/skills/
```

Or upload the `.skill` files directly in the claude.ai skills UI.

## Using the standalone scanners

Each skill includes a Python scanner that checks your project and exits non-zero if tells are found.

### UI scanner

```bash
cd skill/scripts
python3 devibe_scan.py /path/to/your/website
```

Example output:

```
Scanning: /Users/dev/my-site
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 Vibe score: 42/100

Found 5 tells:
  • shadcn/Tailwind defaults (3 files)
    - src/components/Button.tsx: className="rounded-lg"
    - src/App.tsx: className="container mx-auto"
  
  • AI purple gradient (2 files)
    - styles.css: background: linear-gradient(to right, #667eea, #764ba2)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ CI gate: FAIL (score < 80)
```

### Text scanner

```bash
cd unslop-ai-text/skill/scripts
python3 scan_text.py /path/to/docs
```

Flags tells like "it's not just X, it's Y", em dashes, "delve", "leverage", etc.

### Code scanner

```bash
cd unslop-ai-code/skill/scripts
python3 scan_code.py /path/to/src
```

Flags leftover chat artifacts, placeholder comments, emoji in code, swallowed errors, etc.

## Reproducing the study

Run the pipeline in order. Each script is resumable and writes outputs to the current folder.

```bash
cd unslop-ai-ui

# Phase 1-2: Aggregate stats
python3 collect.py

# Phase 3: Harvest on-topic posts (pass target count)
python3 harvest.py 3000

# Phase 4: Harvest comments from canonical threads
python3 harvest_comments.py

# Phase 5: Analyze posts for tells
python3 analyze.py

# Phase 6: Analyze comments for tells (cleaner signal)
python3 analyze_comments.py

# Phase 7-8: Generate charts
python3 make_charts.py
python3 make_charts2.py
```

### Key scripts

**collect.py**: Queries Arctic Shift for per-subreddit totals and matched-by-year aggregates. No auth required.

```python
import urllib.request
import json

url = "https://arctic-shift.photon-reddit.com/api/stats"
params = {"subreddit": "webdev", "term": "AI slop"}
req = urllib.request.Request(f"{url}?{urllib.parse.urlencode(params)}")
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())
    print(data["total_posts"])
```

**harvest.py**: Pulls full post text for on-topic submissions. Resumes from checkpoint.

```python
python3 harvest.py 5000  # Target 5000 on-topic posts
```

**analyze.py**: Detects tells via synonym lexicon, counts occurrences, writes `tell_counts.csv` and `tell_examples.md`.

```python
TELLS = {
    "shadcn_tailwind": ["shadcn", "default tailwind", "tw-"],
    "ai_purple": ["purple gradient", "#667eea", "purple-blue"],
    # ...
}
```

**analyze_comments.py**: Same as `analyze.py` but for comments (cleaner signal). Produces `comment_tell_counts.csv`.

## Key outputs

All data lives in `unslop-ai-ui/`, `unslop-ai-text/`, and `unslop-ai-code/`:

- **corpus.jsonl.gz**: 46,971 on-topic posts (UI study)
- **comments.jsonl**: 3,033 comments from 125 canonical threads
- **tell_counts.csv** / **comment_tell_counts.csv**: Ranked tells with counts and percentages
- **tell_examples.md**: Verbatim quotes with permalinks
- **Charts**: PNG files for growth, ranking, scale, co-occurrence, sentiment

Example `comment_tell_counts.csv`:

```csv
tell,count,total_comments,share
shadcn_tailwind,421,3033,0.1388
ai_purple_gradient,389,3033,0.1282
gradient_hero_text,312,3033,0.1029
neon_glow,287,3033,0.0946
emoji_as_icons,245,3033,0.0808
```

## Common patterns

### Add the UI scanner to CI

```yaml
# .github/workflows/vibe-check.yml
name: Vibe Check
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: |
          pip install -r requirements.txt
          python3 skill/scripts/devibe_scan.py . --threshold 80
```

### Programmatically check a file

```python
import re

TELLS = {
    "shadcn": r"(shadcn|cn\(|class.*rounded-lg)",
    "ai_purple": r"(#667eea|#764ba2|purple.*gradient)",
}

def scan_file(path):
    with open(path) as f:
        content = f.read()
    found = {}
    for tell, pattern in TELLS.items():
        if re.search(pattern, content, re.I):
            found[tell] = re.findall(pattern, content, re.I)
    return found

results = scan_file("src/App.tsx")
if results:
    print(f"Found tells: {list(results.keys())}")
```

### Query Arctic Shift for custom terms

```python
import urllib.request
import json

def query_arctic(subreddit, term, year=None):
    url = "https://arctic-shift.photon-reddit.com/api/stats"
    params = {"subreddit": subreddit, "term": term}
    if year:
        params["year"] = year
    req = urllib.request.Request(f"{url}?{urllib.parse.urlencode(params)}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

data = query_arctic("webdev", "bento grid", year=2024)
print(f"Posts mentioning 'bento grid' in r/webdev (2024): {data['total_posts']}")
```

## Configuration

The studies use hardcoded subreddit lists and keyword lexicons. To customize:

**Edit the subreddit list** in `collect.py`:

```python
SUBREDDITS = [
    "webdev", "web_design", "SaaS", "Entrepreneur",
    # Add your own
]
```

**Edit the tell lexicon** in `analyze.py` or `analyze_comments.py`:

```python
TELLS = {
    "your_tell": [
        "keyword1",
        "keyword2",
        r"regex.*pattern",  # prefix with r for regex
    ],
}
```

**Adjust scanner thresholds** in `devibe_scan.py`:

```python
# Line ~15
THRESHOLD = 80  # Fail CI if vibe score < 80
WEIGHTS = {
    "shadcn_tailwind": 15,
    "ai_purple_gradient": 12,
    # Adjust weights per tell
}
```

## Troubleshooting

**"No posts found" when harvesting**: The term or subreddit may have no matches. Check `scanned_totals_by_sub.csv` to verify the subreddit was indexed by Arctic Shift.

**Scanner false positives**: The lexicon uses keywords and regex. Refine patterns in `TELLS` dict. Example: exclude "purple" alone, require "purple gradient".

**Resuming harvest after interrupt**: The harvest scripts checkpoint by post ID. Just re-run; they skip already-fetched posts.

**Charts not generating**: Ensure `matplotlib` is installed and `tell_counts.csv` exists. Run `analyze.py` before `make_charts.py`.

**Memory issues with large corpus**: The text corpus can be large. Use `corpus.jsonl.gz` (committed snapshot) or stream-process with:

```python
import gzip
import json

with gzip.open("corpus.jsonl.gz", "rt") as f:
    for line in f:
        post = json.loads(line)
        # Process one at a time
```

**Arctic Shift API rate limits**: The free endpoint has no auth but may throttle. The scripts sleep 0.5s between requests. If you hit limits, increase the sleep in `harvest.py`.

## Real-world usage

**Before deploying a new landing page**, run the UI scanner:

```bash
python3 skill/scripts/devibe_scan.py ./public
```

If score < 80, review flagged tells and replace with deliberate choices.

**In a pre-commit hook**:

```bash
#!/bin/sh
python3 skill/scripts/devibe_scan.py . --threshold 80 || exit 1
```

**To audit AI-written docs**:

```bash
python3 unslop-ai-text/skill/scripts/scan_text.py ./docs
```

**To clean AI-generated code**:

```bash
python3 unslop-ai-code/skill/scripts/scan_code.py ./src
```

Review output, manually fix or prompt an AI to rewrite flagged sections without the tells.

## Advanced: Adding a new tell

1. Add to the lexicon in `analyze_comments.py`:

```python
TELLS = {
    # ...
    "your_new_tell": [
        "keyword phrase",
        r"regex.*pattern",
    ],
}
```

2. Re-run analysis:

```bash
python3 analyze_comments.py
python3 make_charts.py
```

3. Verify against quote bank in `comment_tell_examples.md`.

4. Add to scanner in `skill/scripts/devibe_scan.py`:

```python
PATTERNS = {
    # ...
    "your_new_tell": {
        "pattern": r"keyword.*pattern",
        "weight": 8,
        "label": "Your Tell Label",
    },
}
```

5. Test:

```bash
python3 skill/scripts/devibe_scan.py /path/to/test/project
```
