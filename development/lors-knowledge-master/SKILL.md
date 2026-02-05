---
name: lors-knowledge-master
description: Primary entry point for the Lunar Open-source Rover Standard (LORS). Use this to find specialized information about rovers, landers, missions, and companies.
---

# LORS Knowledge Master Skill

This skill allows the AI to navigate and synthesize the LORS documentation and data registry.

## Core Data Philosophy
The LORS registry is a **unified data collection framework** using Markdown with YAML metablocks.
- **Primary Goal**: High-precision collection of technical specifications and mission outcomes.
- **Data Integrity**: Prioritize raw data from Payload User Guides (PUGs) and official mission reporting.
- **Provenance**: Always preserve and link to original sources (URLs, PDFs, official press releases) to maintain data validity.

## Specialized Experts
When asked about specific categories, use these sub-skills for data retrieval:
- **Rovers/Mobility**: `lunar-rovers-expert` (collecting mobility and proximity comms data)
- **Landers/Interfaces**: `lunar-landers-expert` (collecting electrical, data, and mechanical specs)
- **Missions/Outcomes**: `lunar-missions-expert` (collecting timeline and manifest data)
- **Entities/Heritage**: `space-entities-expert` (collecting entity capabilities and flight history)

## Data Operations
1. **Raw Retrieval**: Extract ` ```yaml ` blocks for machine-readable fields.
2. **Source Maintenance**: Ensure every data entry is accompanied by its source link or reference document to preserve the "Link to Truth."
3. **Cross-Referencing**: Link entities to landers, and landers to mission manifests to ensure data consistency.