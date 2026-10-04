---
name: jkkn-terminologies
description: >
  JKKN Framework Terminology standardization skill for enforcing institution-specific
  terminology across all applications, documentation, UI/UX, code, and communications.
  This skill should be used when: (1) Writing any code, documentation, or content for
  JKKN projects, (2) Reviewing code or content for terminology compliance, (3) Creating
  database schemas, API endpoints, or UI labels, (4) Writing user-facing messages or
  communications, (5) Generating reports or documentation, (6) Creating dashboard analytics
  or reports. Automatically triggers when working on JKKN projects or when terminology
  standardization is mentioned.
---

# JKKN Framework Terminology Skill

This skill enforces JKKN institution-specific terminology standards across all development
and documentation activities. It ensures consistent, learner-centered language that aligns
with JKKN's educational philosophy.

## Core Philosophy

JKKN terminology reflects a learner-centered educational philosophy that:
- Emphasizes learning journeys over institutional processes
- Uses empowering, growth-oriented language
- Avoids deficit-based or punitive terminology
- Creates inclusive, supportive communication
- Focuses on continuous growth and improvement
- Celebrates achievements and progress

## Terminology Priority Levels

### Level 1: Critical (Zero Tolerance)
These terms MUST NEVER appear in any JKKN context. Automatic replacement required.

### Level 2: Highly Encouraged
These terms SHOULD be replaced for consistency and brand alignment.

### Level 3: Recommended
These terms are preferred but allow contextual flexibility.

## Critical Terminology Rules

### People & Community (ZERO TOLERANCE)

**Learner Community:**
- NEVER: students, pupils, kids, children, trainees, student body
- ALWAYS: learners (or "young learners" when age context needed)

**Teaching Staff (Academic):**
- NEVER: faculty, teachers, professors, instructors, tutors, educators
- ALWAYS: learning facilitators

**Non-Academic Staff:**
- NEVER: staff, employees, workers
- ALWAYS: team members

### Spaces & Facilities (ZERO TOLERANCE)

**Learning Spaces:**
- NEVER: classrooms, rooms
- ALWAYS: learning studios

**Large Venues:**
- NEVER: lecture halls, auditoriums
- ALWAYS: learning auditoriums

**Practical Spaces:**
- NEVER: labs, laboratories, workshops
- ALWAYS: learning labs

**Study Areas:**
- NEVER: study halls, study rooms
- ALWAYS: learning commons

### Academic Structures (ZERO TOLERANCE)

| Traditional | JKKN Standard |
|-------------|---------------|
| course outcomes | learning outcomes |
| teaching objectives | learning objectives |
| syllabus | learning pathway |
| curriculum | learning framework |
| grades, marks | learning assessments |

### Analytics & Reporting Terminology (CRITICAL)

**Dashboard & Reports:**
| Traditional | JKKN Standard |
|-------------|---------------|
| Student Performance Dashboard | Learner Performance Dashboard |
| Student Analytics | Learning Analytics |
| Student Performance Report | Learner Performance Report |
| Pass/Fail Statistics | Success/Needs Support Statistics |
| Student Count | Learner Count |
| Total Students | Total Learners |
| Students Appeared | Learners Appeared |
| Students Passed | Learners Passed |
| Students Failed | Learners Needing Support |
| Failed Students | Learners Requiring Remediation |
| Top Students | Top Performing Learners |
| Student Ranking | Learner Achievement Ranking |
| Student List | Learner Registry |

**Performance Metrics:**
| Traditional | JKKN Standard |
|-------------|---------------|
| Pass Rate | Success Rate |
| Failure Rate | Support Required Rate |
| Fail Percentage | Needs Improvement Percentage |
| Pass Percentage | Achievement Percentage |
| Student Pass % | Learner Success % |
| Pass % | Success % |
| Average Student Score | Average Learner Score |
| Difficulty Index | Support Index |
| Difficulty % | Support Needed % |

**Assessment Terminology:**
| Traditional | JKKN Standard |
|-------------|---------------|
| Test Results | Assessment Outcomes |
| Exam Results | Evaluation Results |
| Grade Report | Learning Assessment Report |
| Mark Sheet | Achievement Record |
| Result Card | Performance Record |
| Failed Subjects | Subjects Requiring Review |
| Backlog | Learning Gap |
| Backlogs | Learning Gaps |
| Arrear | Pending Assessment |

**Chart & Visualization Labels:**
| Traditional | JKKN Standard |
|-------------|---------------|
| Passed | Achieved |
| Failed | Needs Support |
| Pass/Fail Distribution | Achievement Distribution |
| Result Distribution | Achievement Distribution |
| Failure Analysis | Growth Opportunity Analysis |
| Difficult Subjects | Subjects Requiring Additional Support |
| High Failure Rate | High Support Rate |
| Student Records | Learner Records |
| Total Failures | Learners Needing Support |

### Positive Language Alternatives

Instead of deficit-based language, use growth-oriented alternatives:

| Avoid | Prefer |
|-------|--------|
| "X students failed" | "X learners need additional support" |
| "X% fail" | "X% needs support" |
| "Total Failures" | "Learners Needing Support" |
| "Failed to achieve" | "Working towards achieving" |
| "Below average" | "Developing" or "In progress" |
| "Poor performance" | "Opportunity for growth" |
| "Weak subjects" | "Areas for development" |
| "At-risk students" | "Learners requiring additional support" |
| "Struggling students" | "Learners on growth track" |
| "Low performers" | "Emerging learners" |
| "Remedial class" | "Learning enhancement session" |
| "Detention" | "Focused learning time" |
| "Difficult subjects" | "Subjects requiring additional support" |
| "Failure Analysis" | "Growth Opportunity Analysis" |

## Workflows

### Workflow 1: Code Development

When writing code for JKKN projects:

1. **Variable/Field Naming:**
   ```
   // Use learner-centered naming
   learnerId, learnerName, learnerList
   facilitatorId, facilitatorName
   learningStudioId, learningStudioName
   assessmentValue, learningLevel
   ```

2. **Database Tables:**
   ```sql
   -- Correct table names
   learners, learning_facilitators, team_members
   learning_studios, learning_labs, learning_commons
   learning_assessments, learning_outcomes
   ```

3. **API Endpoints:**
   ```
   /api/learners
   /api/learning-facilitators
   /api/learning-studios
   /api/learning-assessments
   ```

4. **UI Labels:**
   - "Learner Dashboard" (not "Student Dashboard")
   - "Learning Facilitator Portal" (not "Teacher Portal")
   - "Learning Assessment Report" (not "Grade Report")

### Workflow 2: Content Review & Validation

When reviewing existing code or documentation:

1. **Search for prohibited terms:**
   - Search for: student, teacher, faculty, classroom, syllabus, grade, homework
   - Flag all occurrences for replacement

2. **Validate replacements:**
   - Ensure context-appropriate JKKN term is used
   - Verify consistency across related files

3. **Update related artifacts:**
   - Database migrations if schema changes
   - API documentation if endpoints change
   - UI strings and translations

### Workflow 3: Documentation Writing

When creating documentation:

1. **Apply terminology before writing:**
   - Review terminology dictionary before starting
   - Use JKKN terms from the first draft

2. **Consistency check:**
   - Verify all people references use: learners, learning facilitators, team members
   - Verify all space references use: learning studios, learning labs, etc.
   - Verify all academic references use: learning outcomes, learning pathway, etc.

3. **Message framing:**
   - Use growth-oriented language
   - Avoid deficit terminology (failed → did not meet learning outcomes)
   - Use collaborative framing (parent-teacher → learning partner conference)

### Workflow 4: UI/UX Design

When designing interfaces:

1. **Labels and headings:**
   - All user-facing text must use JKKN terminology
   - Button labels, menu items, page titles

2. **Error messages:**
   - "Learner did not meet learning outcomes" (not "Student failed")
   - "Learning facilitator not found" (not "Teacher not found")

3. **Notifications:**
   - "New learning task assigned" (not "New assignment")
   - "Learning assessment available" (not "Test available")

### Workflow 5: Communication Templates

When creating email templates, notifications, or communications:

1. **Greetings:** Address learners, learning facilitators, team members appropriately
2. **Body:** Use JKKN terminology throughout
3. **Sign-offs:** Reference JKKN community appropriately

## Terminology Reference

For the complete terminology dictionary with all mappings, context notes, and examples:

```
references/terminology-dictionary.md
```

This reference includes:
- Complete prohibited → approved term mappings
- Context-specific guidelines
- Code naming conventions
- Quick reference cheat sheet

## Validation Checklist

Before finalizing any JKKN project deliverable, verify:

### Core Terminology
- [ ] No instances of "student/students" (use learner/learners)
- [ ] No instances of "teacher/teachers" (use learning facilitator)
- [ ] No instances of "classroom" (use learning studio)
- [ ] No instances of "syllabus" (use learning pathway)
- [ ] No instances of "curriculum" (use learning framework)
- [ ] No instances of "grades" (use learning assessments)
- [ ] No instances of "failed/failure" (use "did not meet learning outcomes" or "needs support")
- [ ] No instances of "homework" (use independent learning activities)
- [ ] No instances of "assignment" (use learning task)

### Analytics & Dashboard Terminology
- [ ] No "Student Dashboard" (use Learner Dashboard)
- [ ] No "Students Appeared" (use Learners Appeared)
- [ ] No "Students Passed" (use Learners Passed)
- [ ] No "Students Failed" (use Learners Needing Support / Needs Support)
- [ ] No "Pass Rate" in negative contexts (use Success Rate)
- [ ] No "Failure Rate" (use Support Required Rate)
- [ ] No "Top Students" (use Top Performing Learners)
- [ ] No "Failed Subjects" (use Subjects Requiring Review)
- [ ] No "Backlog" (use Learning Gap)
- [ ] No deficit-based language in insights or recommendations

### Technical Implementation
- [ ] All database tables follow JKKN naming
- [ ] All API endpoints follow JKKN naming
- [ ] All UI labels use JKKN terminology
- [ ] All chart labels use learner-centered language
- [ ] All tooltips and descriptions use JKKN terminology
- [ ] All error messages use supportive language

## Adding New Terminology

To extend the terminology standards:

1. Identify the traditional term to replace
2. Determine the appropriate priority level (Critical/Encouraged/Recommended)
3. Create the JKKN equivalent following the naming philosophy
4. Add to `references/terminology-dictionary.md`
5. Update relevant validation checklists

## Exception Handling

### Legal/Regulatory Requirements
Some official documents may require traditional terminology for legal compliance.
In such cases, use traditional terms with JKKN equivalents in parentheses.

### External System Integration
When interfacing with external systems using traditional terminology:
- Maintain JKKN terminology in all user-facing elements
- Map terminology internally at the integration layer
- Document the mapping in integration code comments
