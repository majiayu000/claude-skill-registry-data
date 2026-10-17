---
name: design-harness-agent-skill
description: Turn scattered research and ideas into traceable system designs using markdown cards, evidence linking, and a visual canvas
triggers:
  - "file these sources onto the design board"
  - "create idea cards from this thinking"
  - "assemble the design from surviving ideas"
  - "build the canvas for this workspace"
  - "link this idea to supporting evidence"
  - "show me the provenance chain"
  - "archive this rejected idea"
  - "sync the output back to idea cards"
---

# design-harness Agent Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

An agent skill that helps you turn scattered papers, blog posts, and half-formed ideas into a traceable system design. Every design decision links back through idea cards to the sources that earned it. Markdown keeps the record; a visual canvas makes it readable.

## What design-harness Does

**Three card types, one workflow:**

1. **Sources** (agent creates) — papers, repos, blog posts filed with quality grades
2. **Ideas** (human creates) — your judgments, linked to evidence, clustered by the agent
3. **Output** (agent assembles) — the deliverable synthesized from surviving ideas

**Core principles:**
- Only humans create idea cards; agents file sources and link evidence
- Everything is append-only; rejected ideas are archived, never deleted
- Every output element must trace back to sources through ideas
- Markdown is truth; the canvas is a projection rebuilt from markdown

## Installation

The user should install this skill into their agent:

**Claude Code:**
```
/plugin marketplace add tigerless-labs/design-harness
/plugin install design-harness@design-harness
```

**Codex:**
```
codex plugin marketplace add tigerless-labs/design-harness
```
Then install from `/plugins` in CLI or desktop app.

**Manual (SKILL.md-compatible agents):**
```bash
git clone https://github.com/tigerless-labs/design-harness
cp -r design-harness/plugins/design-harness/skills/design-harness \
  ~/.claude/skills/
```

## Workspace Structure

A design-harness workspace has three markdown folders:

```
your-workspace/
├── sources/           # Agent-created source cards
├── ideas/             # Human-created idea cards
├── output/            # Agent-assembled deliverables
├── target.md          # Declares what to assemble
└── archive/           # Rejected ideas (append-only)
```

## Key Workflows

### 1. Filing Sources

When the user says "file these papers" or drops URLs/PDFs:

**What you do:**
1. Read the source material
2. Create a markdown card in `sources/` with:
   - Bibliographic metadata
   - Quality grade (A/B/C/D based on rigor, relevance, recency)
   - Key claims extracted
   - Source URL or file reference

**Source card template:**
```markdown
---
id: smith2024-distributed
type: source
grade: A
created: 2026-07-15T10:30:00Z
---

# Distributed Systems Patterns (Smith 2024)

**Authors:** Jane Smith, Bob Chen  
**Published:** 2024-03-15  
**URL:** https://example.com/paper.pdf  
**Grade:** A (peer-reviewed, recent, directly relevant)

## Key Claims

1. **Event sourcing improves auditability** — append-only log preserves full history
2. **CQRS separates read/write concerns** — enables independent scaling
3. **Saga pattern manages distributed transactions** — compensating actions vs 2PC

## Assessment

Rigorous empirical study with production data from 12 companies. Directly applicable
to our decision-support use case.

## Log

- 2026-07-15T10:30:00Z: Filed by agent from user-provided PDF
```

**Quality grading:**
- **A**: Peer-reviewed, recent (<2 years), directly relevant, rigorous methodology
- **B**: Credible source, somewhat dated or tangential, solid evidence
- **C**: Blog post or opinion piece, useful perspective but not authoritative
- **D**: Questionable source, outdated, or weak evidence

### 2. Creating Idea Cards

**Only humans create idea cards.** When the user shares a judgment or design decision:

**What you do:**
1. Confirm this is a new idea (not already captured)
2. Draft the idea card structure
3. **Ask the user to approve before creating**
4. Link to supporting sources
5. Save in `ideas/` with empty `## Evidence` section for you to populate

**Idea card template:**
```markdown
---
id: use-event-sourcing
type: idea
status: active
created: 2026-07-15T11:00:00Z
---

# Use event sourcing for decision provenance

## Claim

Every design decision should be recorded as an immutable event with timestamp,
rationale, and links to supporting evidence.

## Evidence

**Supports:**
- [[smith2024-distributed#claim-1]] — append-only log preserves full history
- [[jones2023-auditability]] — audit requirements in regulated industries

**Conflicts:**
- [[chen2024-complexity]] — warns about operational complexity of event stores

## Synthesis

The auditability benefit outweighs complexity concerns for our use case (decision
support in research workflows). We can start simple with file-based logs before
scaling to a proper event store.

## Log

- 2026-07-15T11:00:00Z: Created by human, linked to sources by agent
- 2026-07-15T14:20:00Z: Added conflict from chen2024 after user flagged it
```

**Status values:**
- `active` — under consideration
- `accepted` — incorporated into output
- `rejected` — archived with rationale

### 3. Assembling Output

When the user says "assemble the design":

**What you do:**
1. Read `target.md` to understand what to build
2. Gather all `active` ideas from `ideas/`
3. Synthesize them into the output format specified
4. Create markdown in `output/` with provenance links
5. Update idea cards to `status: accepted`

**target.md example:**
```markdown
---
output_type: system_design
format: markdown
deliverable: output/architecture.md
---

# Target: System Architecture for Design Harness

Assemble a system design document covering:
- Data model (card types, schemas)
- Storage layer (markdown as source of truth)
- Projection layer (canvas rendering)
- Agent interaction patterns

Every architectural decision must link back to idea cards.
```

**Output with provenance:**
```markdown
# System Architecture

## Data Model

### Card Types

We use three card types stored as markdown files ([[use-markdown-storage]]):

1. **Source cards** — filed by agent with quality grades ([[grade-sources]])
2. **Idea cards** — created by human only ([[human-creates-ideas]])
3. **Output cards** — assembled by agent ([[agent-assembles-output]])

Each card has YAML frontmatter for metadata and append-only log entries
([[use-event-sourcing]]).

## Storage Layer

Markdown files in git provide version control and human readability
([[markdown-as-truth]]). The filesystem structure separates concerns:

```
workspace/
├── sources/    # Evidence base
├── ideas/      # Design decisions  
├── output/     # Synthesized deliverables
└── archive/    # Rejected ideas (never deleted)
```

...
```

### 4. Building the Canvas

When the user says "build the canvas" or "show me the board":

**What you do:**
```bash
python3 plugins/design-harness/skills/design-harness/scripts/build_canvas.py \
  path/to/workspace -o /tmp/canvas

# For deployment:
python3 plugins/design-harness/skills/design-harness/scripts/build_canvas.py \
  path/to/workspace -o docs
```

Then tell the user:
- Local path: `file:///tmp/canvas/canvas.html`
- If `-o docs`: commit `docs/canvas.html` and enable GitHub Pages for sharing

**Canvas features:**
- Self-contained HTML (no server needed)
- Five visual styles (Pin & Paper, Notebook Tabs, Swiss Modern, BlockFrame, 8-Bit Orbit)
- Click any card to see its markdown source
- Hover links to trace evidence chains
- Dark/light mode for all styles except 8-Bit Orbit

## Common Patterns

### Pattern: Link Conflict Discovery

When you find conflicting evidence while researching:

```markdown
## Evidence

**Supports:**
- [[source-a#claim-2]] — microservices improve team autonomy

**Conflicts:**
- [[source-b#claim-5]] — microservices increase operational complexity
- [[source-c#claim-1]] — distributed systems harder to debug

## Synthesis

The conflict is real. For our small team, we accept the autonomy benefit is
outweighed by operational burden. Recommend monolith-first approach
([[prefer-monolith]]).
```

**What you do:**
1. Surface the conflict explicitly
2. Don't pick a side — let the human decide
3. Link both supporting and conflicting sources
4. Update the idea card's evidence section

### Pattern: Syncing Output Back to Ideas

If the user edits `output/architecture.md` directly:

**What you do:**
1. Detect which sections changed
2. Trace back through `[[idea-card]]` links
3. Ask: "This output edit affects idea card X. Should I update the idea, or create a new idea card for this change?"
4. Append to the idea card's log with the change and timestamp

### Pattern: Archiving Rejected Ideas

When an idea is rejected:

**What you do:**
1. Move card from `ideas/` to `archive/rejected/`
2. Update status to `rejected`
3. Append log entry with rejection rationale
4. Keep all links intact (archived ideas remain traceable)

**Example log entry:**
```markdown
## Log

- 2026-07-15T11:00:00Z: Created by human
- 2026-07-20T16:45:00Z: Rejected — operational complexity outweighs benefits for 
  our team size; conflicts with [[prefer-simplicity]] principle
```

### Pattern: Batch Filing Sources

When the user drops 10+ papers:

**What you do:**
1. File each as a source card
2. Grade each independently
3. Extract 3-5 key claims per source
4. Report summary: "Filed 12 sources: 3 grade A, 6 grade B, 3 grade C"
5. Suggest: "Would you like me to cluster related claims across sources?"

## Agent Interaction Guidelines

### You Create Source Cards

When the user provides research material:
- Extract bibliographic info
- Grade quality rigorously
- Capture key claims with direct quotes when possible
- Link to URL or file path

### Human Creates Idea Cards

When the user expresses a design decision:
- Draft the card structure
- **Ask for approval before creating**
- Say: "This sounds like a new idea: [title]. Should I create an idea card?"
- After approval, create card and link evidence

### You Link Evidence

After creating an idea card:
- Search `sources/` for supporting claims
- Note conflicts explicitly
- Ask: "I found 3 supporting sources and 1 conflicting source. Want me to link them?"

### You Assemble on Command

Only assemble output when explicitly asked:
- "assemble the design"
- "build the architecture doc"
- "synthesize ideas into the deliverable"

Never assemble preemptively. Always check `target.md` first.

## Troubleshooting

### Canvas won't open / shows blank page

**Check:**
1. Was `build_canvas.py` run on the correct workspace path?
2. Are markdown files valid (YAML frontmatter parseable)?
3. Browser console errors (open DevTools)

**Fix:**
```bash
# Validate workspace structure
ls -R workspace/  # should show sources/, ideas/, output/

# Re-run canvas build with verbose output
python3 scripts/build_canvas.py workspace/ -o /tmp/test --verbose
```

### Links between cards aren't rendering

**Cause:** Wikilink format mismatch

**Fix:** Use `[[card-id]]` not `[[card-id.md]]`
```markdown
# Correct
See [[use-event-sourcing]] for rationale

# Wrong
See [[use-event-sourcing.md]]
```

### Idea card rejected but still shows in output

**Cause:** Status not updated or output not rebuilt

**Fix:**
1. Verify idea card has `status: rejected` in frontmatter
2. Re-run assembly: "assemble the design again"
3. Check `output/` timestamp is after rejection timestamp

### Source quality grades inconsistent

**Grading rubric:**

| Grade | Peer Review | Recency | Relevance | Rigor |
|-------|-------------|---------|-----------|-------|
| A | Yes | <2yr | Direct | High |
| B | Credible | <5yr | Related | Solid |
| C | Opinion | Any | Tangential | Weak |
| D | Questionable | >10yr | Irrelevant | Poor |

When in doubt, grade **B** and explain reasoning in card.

## Canvas Customization

### Deploying Canvas to GitHub Pages

```bash
# Build into docs/ folder
python3 scripts/build_canvas.py workspace/ -o docs

# Commit
git add docs/canvas.html
git commit -m "Update design canvas"
git push

# Enable Pages: Settings → Pages → Source: main branch, /docs folder
```

URL will be `https://username.github.io/repo-name/`

### Changing Default Style

Edit `target.md` (or create if missing):
```markdown
---
canvas_style: swiss-modern
---
```

Styles: `pin-and-paper` (default), `notebook-tabs`, `swiss-modern`, `block-frame`, `8-bit-orbit`

## Code Examples

### Parsing a Source Card in Python

```python
import yaml
import re
from pathlib import Path

def parse_source_card(card_path: Path) -> dict:
    """Parse a source card and extract metadata + claims."""
    content = card_path.read_text()
    
    # Extract YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        raise ValueError(f"Invalid card format: {card_path}")
    
    frontmatter = yaml.safe_load(match.group(1))
    body = match.group(2)
    
    # Extract claims section
    claims_match = re.search(r'## Key Claims\n\n(.*?)(?=\n##|$)', body, re.DOTALL)
    claims = claims_match.group(1).strip() if claims_match else ""
    
    return {
        'id': frontmatter['id'],
        'grade': frontmatter['grade'],
        'created': frontmatter['created'],
        'body': body,
        'claims': claims
    }

# Usage
source = parse_source_card(Path('workspace/sources/smith2024.md'))
print(f"Grade: {source['grade']}")
```

### Finding Evidence Links in Idea Cards

```python
import re
from pathlib import Path
from typing import List, Tuple

def extract_evidence_links(idea_card_path: Path) -> Tuple[List[str], List[str]]:
    """Extract supporting and conflicting source links."""
    content = idea_card_path.read_text()
    
    # Find Evidence section
    evidence_match = re.search(
        r'## Evidence\n\n(.*?)(?=\n##|$)', 
        content, 
        re.DOTALL
    )
    if not evidence_match:
        return [], []
    
    evidence_section = evidence_match.group(1)
    
    # Extract wikilinks
    supports = re.findall(
        r'\*\*Supports:\*\*\n(.*?)(?=\n\*\*|$)',
        evidence_section,
        re.DOTALL
    )
    conflicts = re.findall(
        r'\*\*Conflicts:\*\*\n(.*?)(?=\n\*\*|$)',
        evidence_section,
        re.DOTALL
    )
    
    def parse_links(section: str) -> List[str]:
        return re.findall(r'\[\[([^\]]+)\]\]', section)
    
    support_links = parse_links(supports[0]) if supports else []
    conflict_links = parse_links(conflicts[0]) if conflicts else []
    
    return support_links, conflict_links

# Usage
supports, conflicts = extract_evidence_links(
    Path('workspace/ideas/use-event-sourcing.md')
)
print(f"Supported by {len(supports)} sources")
print(f"Conflicts with {len(conflicts)} sources")
```

### Appending to Card Log

```python
from datetime import datetime
from pathlib import Path

def append_log_entry(card_path: Path, entry: str) -> None:
    """Append a timestamped entry to a card's log."""
    content = card_path.read_text()
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    log_entry = f"- {timestamp}: {entry}\n"
    
    # Find or create Log section
    if '## Log' in content:
        content = content.rstrip() + '\n' + log_entry
    else:
        content = content.rstrip() + '\n\n## Log\n\n' + log_entry
    
    card_path.write_text(content)

# Usage
append_log_entry(
    Path('workspace/ideas/use-markdown-storage.md'),
    'Updated evidence section with new conflicting source'
)
```

## Real-World Example: Filing a Paper

**User says:** "File this paper onto the board: https://example.com/distributed-systems.pdf"

**You respond:**

```markdown
I'll download and file this paper. One moment...

[After reading the PDF]

**Filed:** Distributed Systems at Scale (Martinez et al. 2024)

**Grade:** A
- Peer-reviewed ACM conference paper
- Published March 2024 (recent)
- Directly relevant to our event-sourcing decision
- Empirical study with production data

**Key claims extracted:**
1. Event sourcing reduces bug reproduction time by 60%
2. Append-only logs enable time-travel debugging
3. Storage overhead is 2-3x compared to mutable state

**Source card created:** `sources/martinez2024-distributed.md`

Would you like me to link this to any existing idea cards? I see potential
connections to:
- [[use-event-sourcing]] — supports claim about debugging benefits
- [[storage-efficiency-concerns]] — conflicts with our storage constraints
```

## Summary

When helping users with design-harness:

1. **File sources** automatically when given research material
2. **Draft idea cards** but always ask for human approval before creating
3. **Link evidence** by searching sources for supporting/conflicting claims
4. **Assemble output** only on explicit command, following `target.md`
5. **Build canvas** to give visual projection of the workspace
6. **Preserve provenance** — every output element must trace to sources through ideas
7. **Archive, don't delete** — rejected ideas move to `archive/` with rationale
8. **Markdown is truth** — the canvas is rebuilt from markdown, never the source

The human decides what's true. You file the evidence and run the errands.
