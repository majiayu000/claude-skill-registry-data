---
name: report-architecture-analysis
description: Specialized skill for conducting detailed architectural analysis of lunar rover systems and subsystems.
---

# Architecture Analysis Reporter Skill

## Domain Knowledge
- **Source Document**: `LORS_ Lunar Rover Standard proposition.md`
- **Primary Data Sources**:
  - `rovers/` (directory of rover profiles)
  - `landers/` (directory of lander profiles)
  - `SPACE_ENTITIES.MD`
  - `missions/`
  - `LUNAR_MISSIONS.MD` (Index)
  - `STUDENT_ROVER_TEAMS.MD`
  - `ROVER_COMMANDS.MD`
  - `ROVER_SOFTWARE_PROPOSAL.MD`
  - `STANDARDS_AND_DOCS.MD`
- **Dynamic Data Sources**:
  - Technical PDFs (Payload User Guides - PUGs) located in `data/` or workspace.
  - HTML/Text data exports in `data/`.

## Instructions
1. **Data Discovery**:
   - Critically important: Search the `data/` directory and broader workspace for detailed technical documents (PDF PUGs, specifications). Use `find` or similar tools to locate them.
   - Extract technical specs (voltage, data rates, pinouts) from these documents to support the analysis.

2. **Technical Architecture Breakdown**:
   - For each profiled rover project (8-10 total), decompose the system into key subsystems:
     - **Mobility**: Locomotion type, wheel design, suspension.
     - **Power**: Solar, battery, distribution, charging interfaces.
     - **Communication**: Freq bands (S-band, X-band), protocols, lander-to-rover links.
     - **Computing & Software**: Onboard avionics, operating systems (e.g., ROS, cFS). Reference `ROVER_SOFTWARE_PROPOSAL.MD`.
     - **Payload**: Mechanical and data interfaces for instruments.

3. **Interface Analysis**:
   - Analyze the physical and data interfaces between the rover and the lander (deployment mechanisms, power transfer).
   - Analyze interfaces between the rover and payloads.
   - Check `ROVER_COMMANDS.MD` for command and control interface patterns.

4. **Gap & Standardization Analysis**:
   - Identify technical disparities (e.g., proprietary connectors, incompatible comms).
   - Highlight specific areas where lack of standardization hinders interoperability.
   - Pinpoint successful patterns that could serve as a basis for LORS, using `STANDARDS_AND_DOCS.MD` as a baseline.

5. **Report Writing Standards**:
   - **Academic/Scientific Rigor**: Reports should be analytical and evidence-based, using technical terminology appropriately.
   - **Simplicity & Accessibility**: Write clearly and concisely. Avoid unnecessary jargon. Explain complex concepts in straightforward language.
   - **References**: Use standard Markdown footnotes for all citations.
     - **Strict Format**: `[^1]: <Description>, [<Filename>](../<path_to_file>)`
     - **Example**: `[^1]: Astrobotic Griffin PUG, [landers/GRIFFIN.MD](../landers/GRIFFIN.MD)`
   - **Structure**: Use clear headings, bullet points, and tables to enhance readability.
   - **Evidence-Based**: Every conclusion should be supported by data from the primary sources.

6. **Analysis Output**:
   - **Target Output File**: `reports/ARCHITECTURE_ANALYSIS.MD`
   - Generate detailed technical comparison tables and architectural diagrams (descriptions).
   - Include a references section listing all sources consulted.
   - This analysis supports the "detailed architectural analysis" requirement of Objective #1.
