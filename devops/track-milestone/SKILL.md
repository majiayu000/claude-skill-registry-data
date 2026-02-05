---
name: track-milestone
description: Track and manage project milestones, deliverables, and deadlines. Use when user mentions "milestone", "deadline", "deliverable", "release", "target date", or wants to track major project achievements and dependencies between milestones.
---

# Track Milestone Skill

## When to use this Skill

Activate when the user:
- Mentions creating, updating, or checking milestones
- Uses keywords: "milestone", "deadline", "deliverable", "release", "target", "due date"
- Wants to track major project achievements
- References project timeline or roadmap
- Needs to manage milestone dependencies
- Wants to see progress toward goals

## Workflow

### Phase 1: Context Discovery & Intent Recognition

**Objective**: Understand project structure and user's specific milestone intent.

**Steps**:

1. **Locate project RULE.md** and **milestones.yaml**:
   ```bash
   ls RULE.md milestones.yaml
   ```

2. **Read both files**:
   - RULE.md: Project methodology, milestone tracking preferences
   - milestones.yaml: Existing milestones and structure

3. **Detect user intent**:
   - **Create milestone**: "create milestone", "add milestone", "new milestone"
   - **Update milestone**: "update milestone", "milestone progress", "mark complete"
   - **Check status**: "milestone status", "show milestones", "timeline"
   - **Manage dependencies**: "milestone depends on", "blocking milestone"

4. **Route to appropriate workflow**:
   - Create → Workflow A
   - Update → Workflow B
   - Status → Workflow C
   - Dependencies → Workflow D

### Workflow A: Create Milestone

**Objective**: Add a new milestone to the project timeline.

**Steps**:

1. **Gather milestone details**:

   **Name**:
   ```
   Milestone name?
   Example: "Beta Release", "MVP Launch", "Security Audit Complete"
   ```

   **Description**:
   ```
   Brief description of what this milestone represents?
   ```

   **Target date**:
   ```
   Target completion date? (YYYY-MM-DD or relative like "end of Q2")
   ```

   **Deliverables**:
   ```
   What needs to be delivered for this milestone?
   - Deliverable 1
   - Deliverable 2
   ```

   **Owner** (optional):
   ```
   Who's responsible for this milestone? (@name or "Team")
   ```

   **Dependencies** (optional):
   ```
   Does this milestone depend on any other milestones?
   Example: "After Alpha Release" or "After milestones 1 and 2"
   ```

   **Related sprints/phases** (optional):
   ```
   Which sprints/phases contribute to this milestone?
   ```

2. **Generate milestone ID**:
   ```
   milestone-{number} or {name-slug}
   Example: milestone-1 or beta-release
   ```

3. **Read current milestones.yaml**:
   ```
   Read milestones.yaml
   ```

4. **Add new milestone entry**:
   ```yaml
   milestones:
     - id: {milestone-id}
       name: "{Milestone Name}"
       description: "{Description}"
       target_date: YYYY-MM-DD
       actual_date: null
       status: planned
       dependencies: [{dependent-milestone-ids}]
       deliverables:
         - Deliverable 1
         - Deliverable 2
       owner: "@{name}"
       related_sprints: [{sprint-numbers}]
       completion_criteria:
         - Criterion 1
         - Criterion 2
       notes: ""
   ```

5. **Validate dependencies**:
   - Check that referenced milestones exist
   - Detect circular dependencies
   - Warn if dependency order seems wrong

6. **Update milestones.yaml** using Edit tool:
   ```
   Edit milestones.yaml
   Add new milestone entry in appropriate location (sorted by target date)
   ```

7. **Update governance**:
   - Update project README.md (add to timeline section)
   - Add "Recent Activity" entry
   - Link to related sprints if applicable

8. **Report creation**:
   ```
   ✅ Milestone Created!

   🎯 {Milestone Name}
   📅 Target: {target_date}
   📦 Deliverables: {count}
   👤 Owner: @{name}

   [If dependencies:]
   🔗 Dependencies:
   - {Dependent milestone names}

   [If related sprints:]
   🏃 Related Sprints: {sprint numbers}

   📄 Added to: milestones.yaml

   💡 Track progress with:
   "Update milestone {name}"
   "Milestone status"
   ```

### Workflow B: Update Milestone

**Objective**: Update milestone status, progress, or completion.

**Steps**:

1. **Identify target milestone**:
   - Extract name/ID from user message
   - Or ask: "Which milestone?"

2. **Read milestones.yaml**:
   ```
   Read milestones.yaml
   Find milestone entry
   ```

3. **Determine update type**:
   - **Status change**: planned → in_progress → completed → delayed
   - **Progress update**: Update notes or deliverables status
   - **Date change**: Update target or actual date
   - **Completion**: Mark as completed with date

4. **Execute update**:

   **For status change**:
   ```yaml
   status: {new_status}
   ```

   **For completion**:
   ```yaml
   status: completed
   actual_date: {YYYY-MM-DD}
   ```

   **For progress/notes**:
   ```yaml
   notes: "{Updated notes about progress}"
   ```

   **For deliverable tracking**:
   ```yaml
   deliverables:
     - [X] Deliverable 1 (completed)
     - [ ] Deliverable 2 (in progress)
   ```

5. **Check impact**:
   - **If milestone completed**: Check dependent milestones (can they start?)
   - **If milestone delayed**: Check impacted milestones (cascade delays?)

6. **Update milestones.yaml** using Edit tool

7. **Generate milestone report** (if completed):
   ```markdown
   # Milestone Completion Report: {Milestone Name}

   **Completed**: {actual_date}
   **Target**: {target_date} ({"On Time" | "Early" | "Delayed by X days"})

   ## Deliverables
   - [X] Deliverable 1
   - [X] Deliverable 2

   ## Contributing Sprints
   - Sprint {X}
   - Sprint {Y}

   ## Metrics
   - Duration: {calculation}
   - Team: {involved team members}
   - Key Achievements: {summary}

   ## Impact
   - Enabled milestones: {dependent milestones}
   - Next milestone: {next in timeline}

   ## Lessons Learned
   {Notes from milestone execution}

   ---
   Generated: {YYYY-MM-DD} by ProjectMaster
   ```

8. **Save report** (if generated):
   ```
   Write to: reports/milestone-{id}-completion.md
   ```

9. **Update governance**:
   - Update project README.md
   - Add Recent Activity entry
   - Link report to milestone in yaml

10. **Report update**:
    ```
    ✅ Milestone Updated!

    🎯 {Milestone Name}
    📊 Status: {old_status} → {new_status}

    [If completed:]
    🎉 Milestone Completed!
    📅 Completed: {actual_date} ({on_time_status})
    📦 Deliverables: All {count} delivered
    📄 Report: reports/milestone-{id}-completion.md

    🔓 Unblocked Milestones:
    - {Dependent milestone names}

    💡 Next Milestone: {Next in timeline}

    [If delayed:]
    ⚠️ Milestone Delayed
    📅 Was: {original_target} → Now: {new_target}
    ⚠️ Impacted Milestones:
    - {Affected milestones}

    📄 Updated: milestones.yaml
    ```

### Workflow C: Status Report

**Objective**: Show project milestone status and timeline.

**Steps**:

1. **Read milestones.yaml**:
   ```
   Read milestones.yaml
   Parse all milestones
   ```

2. **Categorize milestones**:
   - Completed
   - In Progress
   - Planned
   - Delayed/At Risk

3. **Calculate metrics**:
   - Total milestones
   - Completion rate
   - On-time rate
   - Average delay (if any)
   - Next milestone due date

4. **Check dependencies**:
   - Any blocked milestones?
   - Ready to start milestones?

5. **Generate status report**:
   ```
   📊 Project Milestone Status

   **Project**: {Project Name}
   **Total Milestones**: {count}
   **Completed**: {X}/{total} ({percentage}%)
   **On Track**: {Y}
   **At Risk**: {Z}

   🎉 Completed Milestones:
   ✅ {Milestone 1} - {actual_date} ({"On Time" | "Early" | "Delayed"})
   ✅ {Milestone 2} - {actual_date}
   ...

   🔄 In Progress:
   - {Milestone Name} - Target: {target_date} ({days_remaining} days)
     Status: {On Track | At Risk}
     Progress: {notes or deliverables status}

   📅 Upcoming:
   - {Milestone Name} - Target: {target_date} ({days_until} days)
     [If blocked:] ⚠️ Blocked by: {dependency names}

   ⚠️ Delayed:
   - {Milestone Name} - Was: {original} Now: {revised}
     Delay: {days} days
     Impact: {affected milestones}

   📈 Timeline Health: {Overall Assessment}
   [If at risk:] ⚠️ {count} milestones at risk of delay

   🎯 Next Milestone: {Name} - {target_date} ({days_remaining} days)

   📄 Full timeline: milestones.yaml
   ```

6. **Include visual timeline** (text-based):
   ```
   📅 Timeline:

   Q1 2025
   ├── [✅] Alpha Release (2025-02-15) ← Completed
   └── [🔄] Beta Release (2025-03-31) ← In Progress

   Q2 2025
   ├── [📅] Public Launch (2025-04-30)
   └── [⏸️] Feature Freeze (2025-05-15) ← Blocked by Beta

   Q3 2025
   └── [📅] 1.0 Release (2025-07-31)
   ```

### Workflow D: Manage Dependencies

**Objective**: Define or update milestone dependencies.

**Steps**:

1. **Identify milestones involved**:
   - Primary milestone
   - Dependent milestone(s)

2. **Read milestones.yaml**

3. **Update dependency**:

   **Adding dependency**:
   ```yaml
   milestones:
     - id: milestone-2
       dependencies: [milestone-1]  # milestone-2 depends on milestone-1
   ```

   **Removing dependency**:
   ```yaml
   dependencies: []  # or remove the dependency from list
   ```

4. **Validate**:
   - Check for circular dependencies
   - Verify dependency exists
   - Check timeline logic (dependent milestone should be after dependency)

5. **Update milestones.yaml**

6. **Report**:
   ```
   ✅ Dependency Updated!

   🎯 {Milestone Name}
   🔗 Now depends on:
   - {Dependency 1}
   - {Dependency 2}

   ⚠️ {Milestone Name} cannot start until dependencies complete.

   [If circular dependency detected:]
   ❌ Error: Circular dependency detected!
   {Milestone A} → {Milestone B} → {Milestone A}
   Please review dependencies.

   [If timeline conflict:]
   ⚠️ Warning: {Milestone Name} target ({date1}) is before
   dependency {Dependency Name} target ({date2}).
   Consider adjusting dates.
   ```

## Special Cases

### Case 1: Milestone with multiple dependencies

```yaml
milestones:
  - id: public-launch
    name: "Public Launch"
    dependencies: [beta-complete, security-audit, marketing-ready]
    status: planned
```

Report readiness:
```
🎯 Public Launch Readiness:

Dependencies:
✅ Beta Complete (2025-03-15) ← Done
✅ Security Audit (2025-03-20) ← Done
🔄 Marketing Ready (2025-04-01) ← In Progress (90%)

Status: Waiting on 1 dependency
Can start: After 2025-04-01
```

### Case 2: Milestone delayed - cascade impact

If milestone delayed, check cascade:

```
⚠️ Milestone Delay Impact Analysis

{Delayed Milestone} delayed from {old_date} to {new_date}

Directly Impacted:
- {Milestone A} (depends on this) - May delay
- {Milestone B} (depends on this) - May delay

Cascade Impact:
- {Milestone C} (depends on Milestone A) - Potential delay
- {Milestone D} (depends on Milestone B) - Potential delay

Recommendation:
Review timeline for {count} affected milestones.
Consider:
1. Adjusting target dates
2. Removing dependencies if possible
3. Allocating more resources
```

### Case 3: Sprint-to-milestone tracking

Link sprints to milestone progress:

```markdown
## Milestone: Beta Release

**Target**: 2025-03-31
**Status**: In Progress (75%)

### Contributing Sprints:
- Sprint 3: User Authentication ✅ Complete
- Sprint 4: Profile Management ✅ Complete
- Sprint 5: Settings & Preferences 🔄 In Progress (Day 8/14)
- Sprint 6: Final Polish 📅 Planned

### Deliverables Status:
- [X] Core Features (Sprints 3-4)
- [🔄] Additional Features (Sprint 5) - 80% complete
- [ ] Bug Fixes & Polish (Sprint 6)

**Progress**: 75% (3 of 4 sprints complete)
**On Track**: Yes, 2 weeks remaining
```

### Case 4: Milestone-based releases

For release milestones, include version info:

```yaml
milestones:
  - id: v1-0-release
    name: "Version 1.0 Release"
    type: release
    version: "1.0.0"
    target_date: 2025-07-31
    release_notes: "reports/v1.0-release-notes.md"
    deliverables:
      - All MVP features complete
      - Security audit passed
      - Documentation published
      - Marketing materials ready
```

## Error Handling

### Error: milestones.yaml not found

```
⚠️ No milestones.yaml found.

This project hasn't initialized milestone tracking.

Options:
1. Create milestones.yaml now
2. Initialize project with: "Initialize project"
3. Cancel

What would you like to do?
```

If user chooses 1, create template milestones.yaml.

### Error: Invalid date format

```
⚠️ Invalid date format: "{input}"

Please use YYYY-MM-DD format.
Example: 2025-12-31

Or relative dates:
- "end of Q2" → 2025-06-30
- "next month" → 2025-12-01
```

### Error: Circular dependency

```
❌ Cannot create dependency: Circular reference detected!

Dependency chain:
{Milestone A} → {Milestone B} → {Milestone C} → {Milestone A}

Please remove one dependency to break the cycle.
```

### Error: Milestone not found

```
⚠️ Milestone "{name}" not found in milestones.yaml.

Available milestones:
- {Milestone 1}
- {Milestone 2}
- {Milestone 3}

Did you mean one of these?
```

## Integration with Other Skills

### With manage-sprint Skill

Sprints contribute to milestones:
- Link sprints to milestones in metadata
- Update milestone progress when sprint completes
- Show milestone context in sprint planning

### With track-meeting Skill

Milestone reviews create meetings:
- Milestone completion meeting
- Milestone checkpoint meeting
- Link meeting notes to milestone

### With AkashicRecords

Milestone artifacts:
- Decision records leading to milestone
- Documentation created for milestone
- Knowledge captured during milestone work

## Best Practices

### 1. Define clear deliverables

Each milestone should have specific, measurable deliverables.

### 2. Set realistic dates

Use team velocity and sprint history to set achievable targets.

### 3. Track dependencies explicitly

Don't assume implicit dependencies - document them.

### 4. Review timeline regularly

Monthly or per-sprint review of milestone status keeps project on track.

### 5. Celebrate completions

Acknowledge milestone achievements with team.

### 6. Learn from delays

Document reasons for delays to improve future planning.

### 7. Link to work items

Connect milestones to sprints, stories, and tasks for full traceability.

### 8. Update proactively

Update milestone status before it becomes "delayed".

## Notes

- Milestones provide high-level project visibility for stakeholders.
- Dependency tracking prevents surprises and enables proactive planning.
- Milestone completion reports create valuable project history.
- Integration with sprints connects strategy (milestones) with execution (sprints).
- The milestones.yaml becomes the project timeline source of truth.

---

Well-managed milestones turn long-term goals into achievable checkpoints. This Skill makes milestone tracking systematic and insightful.
