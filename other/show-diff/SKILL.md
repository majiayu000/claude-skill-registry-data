---
name: show-diff
description: Render git diff as a beautiful HTML5 page and host it on a local server for visual review
---

# Show Git Diff as HTML

Convert raw `git diff` output into a styled HTML5 page and serve it via a local HTTP server.

## Prerequisites

- Git repository in current directory
- Python 3.x (for conversion script + HTTP server)
- No external dependencies needed

## Steps

1. **Generate and convert diff to HTML**
   ```bash
   cd /home/chihmin/Assetsentry/AssetSentry
   python3 /home/chihmin/.hermes/skills/devops/show-diff/scripts/diff2html.py
   ```
   Or with a specific diff file:
   ```bash
   python3 /home/chihmin/.hermes/skills/devops/show-diff/scripts/diff2html.py /tmp/my-diff.patch
   ```

2. **Start HTTP server**
   ```bash
   cd /tmp && python3 -m http.server 8899
   ```

3. **Open URL**
   - Local: `http://aya.crayfish-monitor.ts.net:8899/git-diff.html`

## Notes

- The HTML output uses GitHub-dark theme styling
- Syntax highlighting for additions (green) and deletions (red)
- File sections are collapsible
- Print-friendly layout included
- Server runs on port 8899 (change if needed)

## Script Location

The conversion script is at `scripts/diff2html.py` within this skill directory.