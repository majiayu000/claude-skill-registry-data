---
name: diataxis-categorizer
description: Classify documentation files into domain-based sub-categories within Diátaxis top-level categories (tutorials, how-to, reference, explanation). Use when organizing wiki files into sub-folders like ralph/, copilot/, sdk/ within a Diátaxis category, determining where a file belongs using the three-rule heuristic (keyword extraction → reuse check → create check → fallback), reclassifying research/ staging files into standard categories, or performing batch wiki reorganization. Supplements the `diataxis` skill which handles top-level classification — this skill adds sub-category depth.
metadata: 
  version: 1.0.0
  author: arisng
---

# Diátaxis Categorizer — Domain-Based Sub-Category Classification

This skill adds **sub-category classification** to the Diátaxis framework. While the `diataxis` skill determines *which top-level category* a file belongs in (tutorials, how-to, reference, explanation), this skill determines *which domain sub-folder* within that category.

## Relationship to `diataxis` Skill

| Concern | `diataxis` skill | `diataxis-categorizer` skill |
|---------|------------------|------------------------------|
| Top-level classification | ✅ Owns | ❌ Defers |
| Sub-category placement | ❌ Not covered | ✅ Owns |
| Templates & language patterns | ✅ Owns | ❌ Defers |
| Domain taxonomy | ❌ Not covered | ✅ Owns |
| Batch reorganization | ❌ Not covered | ✅ Owns |

## Domain Taxonomy Convention

Sub-categories are **domain-based folders** inside each Diátaxis top-level category:

```
.docs/
├── tutorials/
│   └── ralph/               # ≥3 ralph-related tutorials
├── how-to/
│   ├── ralph/               # ≥3 ralph-related how-to guides
│   └── copilot/             # ≥3 copilot-related how-to guides
├── reference/
│   ├── ralph/               # ≥3 ralph-related reference docs
│   └── copilot/             # ≥3 copilot-related reference docs
├── explanation/
│   ├── ralph/               # ≥3 ralph-related explanations
│   └── copilot/             # ≥3 copilot-related explanations
└── index.md
```

**Naming convention**: `<category>/<domain>/filename.md`

- Domain folder names: lowercase kebab-case (e.g., `ralph`, `copilot`, `blazor-agui`)
- Each domain sub-folder is independent per category — `reference/ralph/` can exist without `tutorials/ralph/`
- Cross-domain files (spanning multiple domains) remain at the category root

### Known Domains

Primary domains for this workspace:

| Domain | Keyword patterns | Description |
|--------|-----------------|-------------|
| `ralph` | ralph, session, orchestrator, executor, reviewer, librarian, subagent | Ralph v2 orchestration system |
| `copilot` | copilot, copilot-fc, vscode, extension, agent, custom instruction | GitHub Copilot customization |
| `sdk` | sdk, copilot-sdk, acp, client | Copilot SDK / Agent Communication Protocol |
| `blazor` | blazor, ag-ui, blueprint, razor | Blazor UI framework |

Domains are extensible — new domains emerge when files naturally cluster around a keyword.

## Three-Rule Heuristic

Given a file path and its content, determine the target sub-category:

### Rule 1 — Keyword Extraction

Extract the primary domain keyword from the file using this priority chain:

1. **Filename prefix**: `ralph-subagent-contracts.md` → `ralph`
2. **Frontmatter `category` field**: `category: copilot` → `copilot`
3. **H1 title scan**: `# Ralph v2 State Machine` → `ralph`
4. **Content body scan**: Count domain keyword occurrences; dominant domain wins (must be >2× runner-up)

If no single domain dominates, the file is **cross-domain** → stays at category root.

### Rule 2 — Reuse Check

If an existing sub-category folder matches the extracted domain keyword:
- **Recommend placing the file there**
- Example: `reference/ralph/` exists and file domain is `ralph` → target is `reference/ralph/filename.md`

### Rule 3 — Create Check (≥3 Threshold)

If no matching sub-category folder exists:
- Count files at the category root (and in the current batch) that share the same domain keyword
- If **≥3 files** share the domain → **recommend creating the sub-category** and moving all matching files
- If **<3 files** → **fallback**: leave at category root (flat)

The ≥3 threshold prevents premature sub-folder creation for one-off files.

### Fallback

File stays at the category root when:
- No single domain keyword dominates (cross-domain)
- Fewer than 3 peers share the domain and no existing sub-folder matches
- Domain extraction yields no confident result

### Decision Flowchart

```
Input: file path + metadata
         │
    ┌────▼────┐
    │ Rule 1: │
    │ Extract  │
    │ keyword  │
    └────┬────┘
         │
    keyword found?
    ├── NO ──────────────────────────────► FALLBACK: category root
    │
    YES
    │
    ┌────▼────┐
    │ Rule 2: │
    │ Reuse   │
    │ check   │
    └────┬────┘
         │
    sub-folder exists?
    ├── YES ─────────────────────────────► TARGET: <category>/<domain>/file.md
    │
    NO
    │
    ┌────▼────┐
    │ Rule 3: │
    │ Create  │
    │ check   │
    └────┬────┘
         │
    ≥3 peers share domain?
    ├── YES ─────────────────────────────► CREATE sub-folder + move all peers
    │
    NO ──────────────────────────────────► FALLBACK: category root
```

## Research Staging Convention

The `research/` folder is a **staging area**, not a permanent 5th Diátaxis category.

### Rules

- New research files land in `research/` during active investigation
- The categorizer treats `research/` files as **candidates for reclassification**
- Mature research files must be reclassified into a standard category within 1-2 iterations
- When reclassifying: apply the same three-rule heuristic to determine both the category (using `diataxis` skill) and the sub-category (using this skill)

### Maturity Signals

A research file is ready for reclassification when:
- It has a clear single-purpose alignment (tutorial, how-to, reference, or explanation)
- It no longer references in-progress investigation or speculative content
- It can stand alone without session-specific context

## Integration Point: Librarian PROMOTE Step 6.75

This skill is designed to be invoked **inline** by the Librarian's PROMOTE workflow at **Step 6.75 — Sub-Category Resolution**, after top-level Diátaxis classification (Step 6) and content transformation (Step 6.5).

### Contract

**Input**:
```
file_path: string       # e.g., "reference/ralph-subagent-contracts.md"
metadata:
  title: string          # H1 or frontmatter title
  category: string       # Already determined by diataxis skill (Step 6)
  frontmatter: object    # Full frontmatter if available
  body_preview: string   # First 500 chars of body (for keyword scan)
```

**Output**:
```
target_path: string      # e.g., "reference/ralph/ralph-subagent-contracts.md"
action: "place" | "create_and_place" | "stay"
domain: string | null    # Extracted domain keyword, null if cross-domain
reason: string           # Human-readable explanation
peers: string[]          # Other files that share the domain (for create_and_place)
```

### Behavior

- **Pure classification function**: returns a recommendation, no side effects
- The **caller** (Librarian) executes the actual file move
- If `action` is `create_and_place`, the caller should also move the listed `peers`

## Batch Reorganization Workflow

For retroactive reorganization of an existing `.docs/` wiki:

### Steps

1. **Scan**: Enumerate all `.md` files in a target category (e.g., `reference/`)
2. **Classify**: Apply the three-rule heuristic to each file
3. **Manifest**: Output a JSON manifest of proposed moves:

```json
{
  "category": "reference",
  "scan_date": "2026-03-01",
  "proposed_moves": [
    {
      "source": "reference/ralph-subagent-contracts.md",
      "target": "reference/ralph/ralph-subagent-contracts.md",
      "domain": "ralph",
      "action": "create_and_place",
      "reason": "5 files share domain 'ralph' — creating sub-folder"
    },
    {
      "source": "reference/copilot-cli-help.md",
      "target": "reference/copilot/copilot-cli-help.md",
      "domain": "copilot",
      "action": "create_and_place",
      "reason": "4 files share domain 'copilot' — creating sub-folder"
    }
  ],
  "staying": [
    {
      "file": "reference/urls.md",
      "domain": null,
      "reason": "Cross-domain — no single domain dominates"
    }
  ]
}
```

4. **Review**: Human reviews the manifest and approves/rejects individual moves
5. **Execute**: Script executes approved moves (create folders, `mv` files)
6. **Regenerate**: Run `python skills/diataxis/scripts/generate_index.py` to update `index.md`

### Batch Scan Command (Pseudocode)

```
For each category in [tutorials, how-to, reference, explanation]:
  files = list .md files at category root (not in sub-folders)
  domain_counts = {}
  For each file in files:
    domain = extract_domain(file)  # Rule 1
    domain_counts[domain] += 1
  For each file in files:
    domain = extract_domain(file)
    if sub-folder exists for domain:      # Rule 2
      propose move → <category>/<domain>/file
    elif domain_counts[domain] >= 3:      # Rule 3
      propose create + move → <category>/<domain>/file
    else:
      mark as staying                     # Fallback
  Output manifest JSON
```
