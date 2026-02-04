---
name: vault-link-density
description: Analyze link density patterns across vault. Triggers on "link density", "link analysis", "linking patterns", "link stats".
auto_trigger: true
trigger_keywords:
  - "link density"
  - "link analysis"
  - "linking patterns"
  - "link statistics"
  - "link stats"
  - "analyze links"
  - "link distribution"
  - "connectivity"
  - "graph density"
  - "link metrics"
  - "how much linking"
  - "linking behavior"
  - "connection stats"
  - "vault connectivity"
allowed-tools: mcp__flywheel__get_vault_stats, mcp__flywheel__get_folder_structure, mcp__flywheel__search_notes
---

# Link Density Analysis

Analyze linking patterns and density across your vault.

## Purpose

Link density analysis reveals:
- **Over-linked notes**: May need splitting
- **Under-linked notes**: May need connection
- **Folder patterns**: Which areas are well-connected
- **Optimal density**: Balance for your vault

## Metrics

**Link Density** = Total Links / Total Notes

**Optimal ranges:**
- **10-20 links/note**: Well-connected knowledge graph
- **5-10 links/note**: Moderate connection
- **(5 links/note**: Under-connected (isolated knowledge)
- **)20 links/note**: May be over-linking or need restructuring

## Process

### 1. Get Vault Statistics

```javascript
stats = get_vault_stats()
  → total_notes, total_links, avg_links_per_note
```

### 2. Analyze by Folder

```javascript
folder_structure = get_folder_structure()

for folder in folders:
  notes = search_notes({folder: folder.path})
  folder.link_density = calculate_density(notes)
```

### 3. Find Outliers

```javascript
// Notes with extreme link counts
over_linked = notes where link_count > (avg * 3)
under_linked = notes where link_count < (avg / 3)
```

### 4. Report Results

```
Link Density Analysis
═══════════════════════════════════════════════
📊 Vault Overview:
   • Total Notes: 1,000
   • Total Links: 15,000
   • Average Density: 15 links/note
   • Status: ✅ Well-connected

📁 Density by Folder:
   • work/projects/ - 22 links/note (high)
   • tech/ - 18 links/note (optimal)
   • personal/ - 8 links/note (moderate)
   • templates/ - 2 links/note (low, expected)

🔝 Over-Linked Notes (>40 links):
   • [[Main Hub]] - 127 links (consider splitting)
   • [[Core Tech]] - 89 links (central hub)
   • [[Key Project]] - 76 links (central hub)

📉 Under-Linked Notes (<3 links):
   • 150 notes (15% of vault)
   • Mostly in: personal/, daily-notes/

💡 Insights:
   • Work projects are well-integrated
   • Personal notes could use more connections
   • Consider splitting [[Main Hub]] into sub-topics
   • Daily notes intentionally have fewer links (normal)

═══════════════════════════════════════════════
```

## Link Density Patterns

**High Density (Good):**
- Project notes linking to tech, people, processes
- Hub notes connecting multiple concepts
- Index pages organizing topics

**High Density (Bad):**
- Single note trying to cover too much
- Needs splitting into sub-topics
- List pages that should be structured differently

**Low Density (Good):**
- Reference pages (people, companies)
- Daily notes (historical record)
- Atomic concepts (glossary terms)

**Low Density (Bad):**
- Project notes with no context
- Technical docs without links to implementations
- Isolated knowledge islands

---

**Version:** 1.0.0
