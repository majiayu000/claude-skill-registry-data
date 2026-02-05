---
name: vault-clusters
description: Find knowledge clusters (groups of highly connected notes). Triggers on "clusters", "knowledge clusters", "note clusters", "find clusters".
auto_trigger: true
trigger_keywords:
  - "clusters"
  - "knowledge clusters"
  - "note clusters"
  - "find clusters"
  - "show clusters"
  - "topic clusters"
  - "communities"
  - "note groups"
  - "knowledge areas"
  - "related groups"
  - "knowledge domains"
  - "topic areas"
  - "note neighborhoods"
  - "groupings"
  - "what topics exist"
allowed-tools: mcp__flywheel__get_backlinks, mcp__flywheel__get_forward_links, mcp__flywheel__find_hub_notes
---

# Knowledge Clusters

Find groups of notes that are densely connected (knowledge clusters).

## Purpose

Clusters are groups of notes that:
- Link heavily to each other
- Form cohesive topics or projects
- Represent distinct areas of knowledge

Identifying clusters helps:
- Understand vault organization
- Find topic boundaries
- Discover implicit categories
- Plan folder restructuring

## What is a Cluster?

A cluster is 3+ notes where:
- Each note links to at least 2 others in the group
- The group is more connected internally than externally
- Forms a cohesive topic/project

## Process

### 1. Find Hub Notes

```javascript
hubs = find_hub_notes(min_links=10)
  → Start with highly connected notes
```

### 2. Expand from Each Hub

```javascript
for hub in hubs:
  cluster = [hub]

  // Get all notes linking to/from hub
  connections = get_backlinks(hub) + get_forward_links(hub)

  // Find notes that also link to each other
  for note in connections:
    shared_links = count_shared_connections(note, cluster)
    if shared_links >= 2:
      cluster.append(note)
```

### 3. Score Cluster Cohesion

```javascript
cohesion = internal_links / (internal_links + external_links)
  → Higher cohesion = tighter cluster
```

### 4. Report Results

```
Knowledge Clusters
═══════════════════════════════════════════════
Found 12 knowledge clusters

🎯 Top Clusters by Size:

**Cluster 1: Data Platform** (23 notes, 89% cohesion)
Hub: [[Main Project]]
Notes: [[Database]], [[API]], [[Pipeline]], [[Data Quality]], ...

**Cluster 2: Development Tools** (18 notes, 76% cohesion)
Hub: [[Dev Environment]]
Notes: [[Git]], [[VS Code]], [[GitHub]], [[Python]], [[Node.js]], ...

**Cluster 3: Work Process** (15 notes, 82% cohesion)
Hub: [[Workflow]]
Notes: [[Deployments]], [[Releases]], [[Testing]], [[Change Management]], ...

📊 Cluster Statistics:
   • Total clusters: 12
   • Average size: 14.3 notes
   • Average cohesion: 78%
   • Unclustered notes: 200 (20% of vault)

💡 Insights:
   • 3 major topic areas dominate vault
   • Data platform cluster is largest and most cohesive
   • Consider creating MOC (Map of Content) for each cluster
   • Unclustered notes may need topic assignment

═══════════════════════════════════════════════
```

## Cluster Actions

**For each cluster:**
1. **Create MOC**: Make a Map of Content page linking to all cluster notes
2. **Tag consistently**: Apply cluster tag to all members
3. **Move to folder**: Consider organizing by cluster
4. **Strengthen links**: Add missing connections within cluster

**MOC Example:**
```markdown
# Data Platform MOC

Core Platform:
- [[Main Project]]
- [[Database]]
- [[Architecture]]

Data Sources:
- [[Source A]]
- [[Source B]]
- [[Data Quality]]

[... organized cluster view]
```

---

**Version:** 1.0.0
