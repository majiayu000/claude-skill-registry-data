---
name: CA Lobby Phase Planning
description: Enforce CA Lobby phase planning protocol following master project plan. Use when starting new CA Lobby phases, planning implementations, or user says "start phase" or "plan phase". Ensures master plan consultation and proper CA Lobby documentation structure.
extends: generic-skills/phase-planning
version: 1.0.0
---

# CA Lobby Phase Planning

## Project Configuration

**CA Lobby Specific Paths:**
- PROJECT_MASTER_PLAN_PATH: `Documentation/General/MASTER_PROJECT_PLAN.md`
- PROJECT_DOCS_PATH: `Documentation/PhaseX/Plans/`
- PROJECT_PHASE_FORMAT: `PHASE_[X]_[NAME]_PLAN.md`
- PROJECT_REPORT_PATH: `Documentation/PhaseX/Reports/`

## CA Lobby Specific Requirements

### Additional Sections (Beyond Generic 10)

11. **Demo Data Considerations**
    - Impact on demo mode vs backend mode
    - Sample data generation requirements
    - REACT_APP_USE_BACKEND_API flag considerations

12. **Vercel Deployment Impact**
    - Build size implications
    - Environment variable changes needed
    - Deployment testing strategy

13. **BigQuery Integration Points**
    - Backend API changes required
    - Data service modifications
    - BLN API schema considerations

14. **Clerk Authentication Implications**
    - User management impact
    - Authentication flow changes
    - Role/permission updates

## CA Lobby Phase Planning Steps

### Step 1: MANDATORY Master Plan Consultation
**CRITICAL:** Always read `Documentation/General/MASTER_PROJECT_PLAN.md` FIRST

**Verify:**
- Current project phase and status
- Previous phase completion
- Prerequisites met
- Dependencies resolved

### Step 2: Verify Previous Phase Completion Report
**Location:** `Documentation/PhaseX/Reports/`

**Check:**
- Previous phase has completion report
- Report includes all 12 required sections (CA Lobby specific)
- Master plan updated with previous phase status

**If Missing:**
→ **BLOCK:** "Previous phase missing completion report. Must create completion report before planning new phase."

### Step 3: Load CA Lobby Phase Plan Template
Use generic template + CA Lobby sections (11-14 above)

### Step 4: Gather Phase Information
Standard generic collection + CA Lobby specifics:
- Demo data impact
- Vercel deployment considerations
- BigQuery/backend changes
- Clerk authentication impact

### Step 5: Define Micro Save Points
CA Lobby standard: 30-45 minute increments
Format: `MSP-[Phase].[Number]: Description`
Example: `MSP-2g.1: Create component structure`

### Step 6: Write Phase Plan
**Location:** `Documentation/Phase[X]/Plans/PHASE_[X]_[NAME]_PLAN.md`

**Example:** `Documentation/Phase2/Plans/PHASE_2G_VISUALIZATION_PLAN.md`

### Step 7: Update Master Plan Reference
Add phase to master plan's phase list with status: 🔄 IN PROGRESS

---

## CA Lobby Integration Points

**Triggers After:**
- completion-report skill (verifies previous phase complete)

**Triggers Before:**
- Implementation begins

**Works With:**
- Master plan update workflows
- Documentation structure

---

## Example Usage

**User Says:**
```
"Let's start planning Phase 2g for enhanced visualizations"
```

**Skill Executes:**
1. Reads `Documentation/General/MASTER_PROJECT_PLAN.md`
2. Verifies Phase 2f.2 complete with completion report
3. Loads CA Lobby phase plan template (14 sections)
4. Gathers Phase 2g information:
   - Objectives: Enhanced visualization with charts
   - Deliverables: Recharts integration, activity timeline
   - Demo data: Ensure charts work with sample data
   - Vercel: Monitor bundle size impact
   - BigQuery: No backend changes needed
   - Clerk: No auth changes needed
5. Creates micro save points (30-45 min each)
6. Writes to `Documentation/Phase2/Plans/PHASE_2G_ENHANCED_VISUALIZATION_PLAN.md`
7. Updates master plan with new phase status

---

## Notes

- **MANDATORY:** Always consult master plan FIRST
- **MANDATORY:** Verify previous completion report exists
- **CA Lobby Standard:** 12-section completion reports (not generic 10)
- **CA Lobby Standard:** Demo data must be considered in all phases
- **Micro Save Points:** 30-45 minute increments (CA Lobby commitment strategy)

---

## Changelog

### Version 1.0.0 (2025-10-20)
- Initial CA Lobby implementation
- Extends generic-skills/phase-planning
- Adds CA Lobby 14-section requirements
- Enforces master plan consultation
- Verifies completion report from previous phase

---

**End of Skill**
