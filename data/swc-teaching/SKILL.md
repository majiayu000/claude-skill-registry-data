---
name: swc-teaching
description: Manage Southwestern College Recording Arts & Technology teaching workflows - Canvas LMS integration, quiz/question management, Google Workspace sync, studio operations, and administrative tasks with future database-first architecture
---

# swc-teaching Skill

Teaches how to manage SWC RA&T teaching, student support, and program administration including current manual workflows and future automated database-first architecture.

## When to Use This Skill

Use this skill when the user mentions:
- swc, southwestern college, rat, recording arts
- canvas lms, canvas api, quiz creation, assignments
- google drive, google groups, roster management
- studio bookings, client work, live sound
- grading, announcements, modules, course management
- question banks, quiz deployment, assessments
- financial applications, service agreements, program review
- intern management, delegation, faculty meetings

## Current State vs Future Architecture

### ⚠️ PHASE 1: Current Manual Workflows (Documented Here)
- Manual Canvas API calls (Postman/curl)
- Course IDs hardcoded in vault documents
- Quiz questions manually created per course
- Google Drive audits via spreadsheets
- Studio bookings manual calendar sync

### 🚀 PHASE 2: Future Database-First Architecture (Roadmap)
- Registry database with courses, quizzes, questions tables
- MCP server for Canvas API integration
- Question bank with topics + difficulty tagging
- Multi-format export (Canvas + midimaze 2.0)
- Nested skills (question-creation, quiz-creation, quiz-deployment)
- Automated roster sync, Drive audits, anomaly detection

**This skill documents BOTH phases** to provide clear roadmap.

---

## Core Concepts (Current State)

### SWC RA&T Program

**Southwestern College Recording Arts & Technology Department**

**Courses taught:**
- RA&T 105 - Introduction to Recording Arts
- RA&T 120 - Audio Engineering Fundamentals (in-person)
- RA&T 120-501 - Audio Engineering Fundamentals (online)
- RA&T 121 - Intermediate Audio Production
- RA&T 122 - Advanced Recording Techniques
- RA&T 123 - Live Sound Reinforcement
- RA&T 171 - Studio Operations

**Teaching responsibilities:**
- Course delivery (lectures, labs, ensembles)
- Student support (office hours, interventions)
- Program administration (reviews, grants, compliance)
- Client work coordination (studio bookings, live events)
- Intern management (rotation schedules, equipment audits)

### Canvas LMS (Primary System)

**Canvas Instructure** - Learning Management System for all courses

**Current Course IDs (Fall 2025):**
- **120-501 (online):** 74904
- **120:** 76165
- **121:** 76169
- **123:** 76171
- **RA&T Students:** 67461

**Assignment Groups (per course):**
Each course has specific assignment group IDs for:
- Attendance
- Projects
- Discussions
- Assessments
- Office Hour Visits (121, 123)
- Sound Showcase (121, 123)
- Research Paper or Presentation (121, 123)

**Example (120 course):**
```
Course ID: 76165
  - Attendance: 191245
  - Projects: 179686
  - Discussions: 191244
  - Assessments: 191246
```

### Data Sources

**Canvas LMS:**
- Course content, assignments, quizzes
- Student enrollments, grades
- Discussions, announcements
- API for bulk operations

**Google Workspace:**
- Drive: Student submissions, shared materials
- Groups: Roster management, access control
- Sheets: RAT Classes Roster, attendance tracking

**Pronto & Email:**
- Primary communication channels
- Student interventions, escalations

**RAT Calendar / Internal Scheduler:**
- Studio bookings
- Client sessions
- Live sound events

**Finance Portals:**
- CE funding forms
- Mini-grant applications
- Procurement approvals

## Directory Structure (Vault)

**Location:** `~/Code/github.com/theslyprofessor/midimaze/_Nakul/3. SWC Actions/`

```
3. SWC Actions/
├── AGENTS.md                          # This context file
├── SWC Actions Planning.md            # Master workflow overview
│
├── 1. Daily and Weekly/
│   ├── Canvas Management Planning.md  # Canvas API, course IDs
│   ├── Intern Management Planning.md  # Rotation, mic locker
│   └── Course Archive/                # RA&T course blogs per semester
│       └── 25/25 Spring/              # Semester-specific archives
│
├── 2. Beginning of Semester/
│   ├── Calendar Planning.md           # Module unlocks, milestones
│   ├── Google Drive Access Planning.md # Drive permission audits
│   └── Course Archive Planning.md     # Roster reconciliation
│
├── 3. Clients/
│   ├── Checking Internal Scheduler.md # Studio booking approvals
│   ├── Extra Credit Events.md         # Event tracking, point values
│   └── Live Sound Recruiting.md       # Outreach, staffing
│
├── 4. Financial Applications/
│   └── Program Review/                # Annual review materials
│       └── Program Review Planning.md
│
├── 5. Service Agreements/
│   └── Carl Yanchar Service Agreements.md # Vendor paperwork
│
├── 6. Reviews and Reports/
│   ├── Biennial Review.md             # Accreditation requirements
│   └── Resources/myswccd/             # Evidence links, templates
│
├── 7. End of Semester/
│   └── Revoking Access.md             # Shutdown checklist
│
└── Faculty Meetings/                   # Dated notes with action items
```

## Canvas LMS Workflows (Current Manual)

### Course IDs & Assignment Groups

**Documented in:** `Canvas Management Planning.md`

**Update each semester:**
1. Get new course IDs from Canvas
2. Update Canvas Management Planning.md
3. Get assignment group IDs per course
4. Document in planning file

**API to get assignment groups:**
```http
GET https://swccd.instructure.com/api/v1/courses/COURSE_ID/assignment_groups
```

### Quiz Creation (Manual Canvas API)

**Endpoint:**
```http
POST https://swccd.instructure.com/api/quiz/v1/courses/COURSE_ID/quizzes
```

**Headers:**
```
Authorization: Bearer YOUR_CANVAS_API_TOKEN
Content-Type: application/json
```

**Body:**
```json
{
  "title": "Quiz 1: Microphone Types",
  "instructions": "<p>Quiz instructions go here.</p>",
  "assignment_group_id": 191246,
  "published": true,
  "grading_type": "points",
  "due_at": "2025-03-01T23:59:00Z",
  "quiz_settings": {
    "shuffle_answers": true,
    "time_limit": 30,
    "allowed_attempts": 3,
    "scoring_policy": "keep_highest",
    "one_question_at_a_time": true,
    "lock_questions_after_answering": true
  }
}
```

**Quiz settings:**
- `shuffle_answers: true` - Randomize answer order
- `time_limit: 30` - Minutes to complete
- `allowed_attempts: 3` - Number of tries
- `scoring_policy: "keep_highest"` - Best score counts
- `one_question_at_a_time: true` - Single question display
- `lock_questions_after_answering: true` - Prevent navigation back

### Adding Quiz Questions (Manual)

**Endpoint:**
```http
POST /api/v1/courses/:course_id/quizzes/:quiz_id/questions
```

**Question format:**
```json
{
  "question_name": "Microphone Type Identification",
  "question_text": "Which microphone type uses a conductive ribbon?",
  "question_type": "multiple_choice_question",
  "points_possible": 1,
  "answers": [
    {
      "answer_text": "Dynamic",
      "answer_weight": 0
    },
    {
      "answer_text": "Ribbon",
      "answer_weight": 100
    },
    {
      "answer_text": "Condenser",
      "answer_weight": 0
    },
    {
      "answer_text": "Contact",
      "answer_weight": 0
    }
  ]
}
```

**Supported question types:**
- `multiple_choice_question`
- `true_false_question`
- `short_answer_question`
- `essay_question`
- `matching_question`
- `multiple_answers_question`

**Current workflow:**
1. Create quiz (get quiz ID from response)
2. Manually craft question JSON
3. POST each question to quiz
4. Repeat for all questions (20-30 per quiz)

**Pain point:** Extremely manual, no question reuse across courses

### Getting Quiz ID

**Option 1 (Manual):**
- Open quiz in Canvas browser
- Check URL: `...quizzes/QUIZ_ID/edit`

**Option 2 (API):**
```http
GET /api/v1/courses/:course_id/quizzes
```
Returns list of all quizzes with IDs

### Module Unlocking

**Scheduled in:** `Calendar Planning.md`

**Manual process:**
1. Pre-semester: Build module schedule
2. Each week: Manually unlock next module in Canvas
3. Update announcements with module content

**Future:** Automate via Canvas API module unlock endpoints

### Announcements

**Templates stored in:** `Canvas Management Planning.md`

**Cadence:**
- Thursday announcements - Weekend prep
- Sunday announcements - Week ahead

**Manual process:**
1. Draft announcement in planning doc
2. Copy to Canvas per course
3. Post to all relevant sections

## Google Workspace Integration (Current Manual)

### Drive Access Audits

**Goal:** Verify students have submitted Drive access forms and have correct permissions

**Current workflow:**
1. Maintain spreadsheet of student submissions
2. Manually check Drive sharing permissions
3. Flag missing/incorrect access
4. Email students with issues

**Documented in:** `Google Drive Access Planning.md`

**Pain point:** Manual spreadsheet reconciliation

### Google Groups (Roster Management)

**Purpose:** Control access to shared drives, calendars, resources

**Current workflow:**
1. Export Canvas roster
2. Manually add/remove from Google Groups
3. Verify group membership matches enrollment

**Groups used:**
- RAT Students (all enrolled)
- Course-specific groups (120, 121, 123, etc.)

**Pain point:** Manual sync, risk of access gaps

### RAT Classes Roster (Google Sheet)

**Shared spreadsheet** with:
- Student names, emails
- Course enrollments
- Attendance tracking
- Contact information

**Manual updates** throughout semester

## Studio & Client Operations (Current Manual)

### Internal Scheduler → RAT Calendar Sync

**Systems:**
- Internal scheduler (booking requests)
- RAT shared calendar (public schedule)

**Current workflow:**
1. Review booking requests in scheduler
2. Approve/deny based on availability
3. Manually add to RAT calendar
4. Confirm with client

**Pain point:** Dual-entry, risk of conflicts

### Live Sound Events

**Documented in:** `Live Sound Recruiting.md`

**Workflow:**
- Outreach to students for event staffing
- Shadowing opportunities
- Extra credit tracking
- Post-event submissions

### Extra Credit Events

**Documented in:** `Extra Credit Events.md`

**Tracking:**
- Approved events list
- Point values per event
- Student submission verification

## Operating Rhythms

### Daily Operations

**Canvas Dashboard Review:**
- Check all course sections (120-501, 120, 121, 123)
- Review grading queues
- Respond to discussion posts
- Log tasks in Canvas Management Planning

**Communications:**
- Check Pronto for student escalations
- Review email for urgent items
- Route follow-ups to appropriate planning docs

**Studio Operations:**
- Approve new bookings in internal scheduler
- Verify bookings appear on RAT calendar
- Address equipment issues

**Documentation:**
- Capture decisions in Daily Journal
- Link back during weekly review

### Weekly Operations

**Early Week:**
- Confirm upcoming Canvas modules
- Schedule quiz unlocks
- Prep announcements
- Prepare lab/ensemble deliverables

**Midweek:**
- Audit intern assignments
- Studio maintenance checks
- Inventory tasks (mic locker, equipment)
- Log accountability notes

**End of Week:**
- Update course archives
- Send wrap-up announcements
- Reconcile attendance spreadsheets
- Flag grade anomalies

### Semester Milestones

**Pre-Semester (6-2 weeks out):**
- Complete calendar build
- Update syllabi
- Refresh Google Group rosters
- Use Beginning of Semester checklists

**Week 0-1:**
- Onboard students
- Verify Drive access submissions
- Publish introductory content
- First day materials

**Midterm:**
- Gather program review data
- Check financial application timelines
- Schedule faculty syncs
- Mid-semester interventions

**Final Two Weeks:**
- Execute revocation checklist
- Finalize grades
- Close out client work
- Queue post-semester surveys

## Delegation Guidelines

### Safe for Interns/Assistants

**Physical tasks:**
- Room resets after sessions
- Equipment audits
- Mic locker inventory checks

**Administrative:**
- Posting pre-approved announcements
- Updating attendance spreadsheets
- Logging studio bookings

**Student support:**
- Basic tech support
- Equipment checkout/return
- Scheduling office hours

### Requires Faculty Approval

**Academic:**
- Grade changes
- Deadline extensions
- Attendance policy exceptions

**Financial:**
- Financial application submissions
- Budget approvals
- Procurement decisions

**External:**
- Client communications
- Service agreement modifications
- External partnerships

## Credential Management

**⚠️ SECURITY: DO NOT EXPOSE IN FILES**

**Canvas API tokens:**
- Store in environment variables
- Use secure credential store
- Rotate regularly

**Google Workspace:**
- Service account references only
- No inline credentials

**Studio scheduler:**
- Check with faculty before automating
- Secure credential storage

## Current Automation Targets (Not Yet Implemented)

From AGENTS.md, these are **desired automations:**

### 1. Google Drive Access Audits
**Goal:** Automated permission reconciliation

**Workflow:**
- Query Canvas roster
- Check Google Drive sharing permissions
- Flag missing/incorrect access
- Generate report with action items

**Status:** Manual spreadsheet work (to be automated)

### 2. Quiz Generation from Question Banks
**Goal:** Bulk quiz creation via Canvas API

**Workflow:**
- Maintain question bank (topics, difficulty)
- Select questions for quiz
- Generate Canvas API payloads
- Bulk upload to course

**Status:** Manual question creation (to be automated)

### 3. Roster Reconciliation
**Goal:** Sync Canvas enrollments with Google Groups

**Workflow:**
- Export Canvas roster via API
- Compare with Google Groups membership
- Auto-add new students
- Auto-remove dropped students
- Generate sync report

**Status:** Manual sync (to be automated)

### 4. Grade Anomaly Detection
**Goal:** Flag missing assignments or unusual patterns

**Workflow:**
- Query Canvas gradebook via API
- Detect patterns:
  - Missing multiple assignments
  - Sudden grade drops
  - Attendance issues
- Generate intervention list

**Status:** Manual review (to be automated)

### 5. Studio Booking Sync
**Goal:** Auto-sync internal scheduler → RAT calendar

**Workflow:**
- Poll internal scheduler for new bookings
- Validate against availability
- Auto-add to RAT calendar
- Send confirmations

**Status:** Manual calendar updates (to be automated)

---

## Future Architecture: Database-First (Phase 2)

### Registry Database Schema

**New tables needed in Registry (Convex):**

#### courses Table
```typescript
{
  _id: Id<"courses">,
  tenantId: Id<"tenants">,
  
  // Canvas integration
  canvasId: number,           // e.g., 76165
  canvasCourseCode: string,   // e.g., "RA&T 120"
  
  // Course metadata
  courseNumber: string,       // "120"
  courseName: string,         // "Audio Engineering Fundamentals"
  semester: string,           // "Fall 2025"
  section: string,            // "02" or "501"
  isOnline: boolean,
  
  // Canvas assignment groups
  assignmentGroups: {
    attendance?: number,
    projects?: number,
    discussions?: number,
    assessments?: number,
    officeHours?: number,
    showcase?: number,
    research?: number
  },
  
  // Relationships
  studentIds: Id<"people">[],
  quizIds: Id<"quizzes">[],
  instructorId: Id<"people">,
  
  // Status
  status: "planning" | "active" | "completed" | "archived",
  
  // Timestamps
  startDate: string,
  endDate: string,
  createdAt: number,
  updatedAt: number
}
```

#### quizzes Table
```typescript
{
  _id: Id<"quizzes">,
  tenantId: Id<"tenants">,
  
  // Quiz metadata
  title: string,              // "Quiz 1: Microphone Types"
  instructions: string,       // HTML
  
  // Course relationship
  courseId: Id<"courses">,
  
  // Question relationships
  questionIds: Id<"questions">[],  // Ordered list
  
  // Canvas integration
  canvasQuizId?: number,      // Once deployed
  assignmentGroupId: number,  // From course.assignmentGroups
  
  // Quiz settings
  settings: {
    timeLimit?: number,
    allowedAttempts: number,
    scoringPolicy: "keep_highest" | "keep_latest" | "average",
    shuffleAnswers: boolean,
    oneQuestionAtATime: boolean,
    lockQuestionsAfterAnswering: boolean,
    showCorrectAnswers?: boolean,
    showCorrectAnswersAt?: string  // ISO date
  },
  
  // Scheduling
  publishedAt?: string,       // ISO date
  dueAt?: string,
  availableFrom?: string,
  availableUntil?: string,
  
  // Status
  status: "draft" | "ready" | "deployed" | "closed",
  deployed: boolean,
  deployedAt?: number,
  
  // Timestamps
  createdAt: number,
  updatedAt: number
}
```

#### questions Table (THE SOURCE OF TRUTH)
```typescript
{
  _id: Id<"questions">,
  tenantId: Id<"tenants">,
  
  // Question content
  name: string,               // "Microphone Type Identification"
  text: string,               // Question text (HTML supported)
  
  // Categorization
  topic: string,              // "microphone-types" | "signal-flow" | etc.
  difficulty: "easy" | "medium" | "hard",
  tags: string[],             // ["audio-basics", "transducers"]
  
  // Question type
  type: "multiple_choice" | "true_false" | "short_answer" | 
        "essay" | "matching" | "multiple_answers",
  
  // Points
  pointsPossible: number,     // Default: 1
  
  // Multi-format storage (KEY INNOVATION)
  format_canvas: {
    // Canvas API compatible format
    question_name: string,
    question_text: string,
    question_type: string,
    points_possible: number,
    answers: Array<{
      answer_text: string,
      answer_weight: number,  // 100 for correct, 0 for incorrect
      comments?: string
    }>
  },
  
  format_midimaze: {
    // midimaze 2.0 compatible format (future)
    question: string,
    options: string[],
    correctIndex: number,
    explanation?: string,
    mediaUrl?: string        // Audio/video examples
  },
  
  // Usage tracking
  usedInQuizzes: Id<"quizzes">[],
  timesUsed: number,
  averageScore?: number,      // Performance analytics
  
  // Authorship
  createdBy: Id<"people">,
  reviewedBy?: Id<"people">,
  
  // Status
  status: "draft" | "reviewed" | "active" | "retired",
  
  // Timestamps
  createdAt: number,
  updatedAt: number
}
```

### MCP Server Architecture (Future)

**Option 1: Extend registry-mcp**
```typescript
// Add to existing registry MCP server
registry_get_course({ code: "RA&T 120", semester: "Fall 2025" })
registry_create_quiz({ courseId, title, questionIds, settings })
registry_deploy_quiz_to_canvas({ quizId })
registry_get_questions({ topic: "signal-flow", difficulty: "easy", limit: 10 })
```

**Option 2: Separate swc-canvas-mcp**
```typescript
// Dedicated SWC/Canvas MCP server
swc_canvas_create_quiz({ canvasQuizPayload })
swc_canvas_upload_questions({ quizId, questions })
swc_canvas_sync_roster({ courseId })
swc_canvas_get_grades({ courseId })
```

**Recommendation:** Start with registry-mcp extension, split later if needed

### Nested Skills Architecture (Future)

```
swc-teaching (orchestrator - THIS SKILL)
  ├── question-creation
  │     └── Create questions in Registry
  │         - Input: topic, difficulty, text, answers
  │         - Generates both format_canvas and format_midimaze
  │         - Tags appropriately
  │
  ├── quiz-creation
  │     └── Assemble questions into quizzes
  │         - Query question bank by topic/difficulty
  │         - Create quiz in Registry
  │         - Set schedule, settings
  │
  ├── quiz-deployment
  │     └── Deploy Registry quiz → Canvas
  │         - Read quiz + questions from Registry
  │         - Generate Canvas API payloads
  │         - POST to Canvas API
  │         - Update Registry with canvasQuizId
  │
  ├── course-management
  │     └── Canvas sync, rosters, grading
  │         - Sync enrollments → Registry
  │         - Update Google Groups
  │         - Grade anomaly detection
  │
  └── studio-operations (possible future split)
        └── Bookings, client work, intern management
```

### Workflow Examples (Future)

#### Creating Questions (Database-First)

```typescript
// User: "Create 10 easy microphone questions"

// 1. Create in Registry via MCP
registry_create_question({
  name: "Ribbon Microphone Identification",
  text: "Which microphone type uses a conductive ribbon?",
  topic: "microphone-types",
  difficulty: "easy",
  type: "multiple_choice",
  answers: [
    { text: "Dynamic", correct: false },
    { text: "Ribbon", correct: true },
    { text: "Condenser", correct: false },
    { text: "Contact", correct: false }
  ]
})

// MCP generates both formats automatically:
// format_canvas: { Canvas API compatible }
// format_midimaze: { midimaze 2.0 compatible }
```

#### Creating Quiz from Question Bank

```typescript
// User: "Create Quiz 3 for RA&T 120 with 15 easy signal-flow questions"

// 1. Get course from Registry
const course = registry_get_course({ 
  code: "RA&T 120", 
  semester: "Fall 2025" 
})

// 2. Query question bank
const questions = registry_get_questions({
  topic: "signal-flow",
  difficulty: "easy",
  limit: 15,
  excludeUsedIn: course.quizIds  // Don't reuse in same course
})

// 3. Create quiz in Registry
const quiz = registry_create_quiz({
  courseId: course._id,
  title: "Quiz 3: Signal Flow",
  questionIds: questions.map(q => q._id),
  assignmentGroupId: course.assignmentGroups.assessments,
  settings: {
    timeLimit: 30,
    allowedAttempts: 3,
    scoringPolicy: "keep_highest"
  },
  dueAt: "2025-10-15T23:59:00Z"
})
```

#### Deploying Quiz to Canvas

```typescript
// User: "Deploy Quiz 3 to Canvas"

// 1. Get quiz + questions from Registry
const quiz = registry_get_quiz({ quizId })
const questions = registry_get_quiz_questions({ quizId })

// 2. Generate Canvas API payloads
const canvasQuiz = {
  title: quiz.title,
  assignment_group_id: quiz.assignmentGroupId,
  quiz_settings: quiz.settings,
  // ... (uses format_canvas from questions)
}

// 3. POST to Canvas
const response = canvas_api_create_quiz({
  courseId: course.canvasId,
  payload: canvasQuiz
})

// 4. Upload questions
questions.forEach(q => {
  canvas_api_add_question({
    quizId: response.id,
    payload: q.format_canvas  // Use Canvas-compatible format
  })
})

// 5. Update Registry
registry_update_quiz({
  quizId: quiz._id,
  canvasQuizId: response.id,
  deployed: true,
  deployedAt: Date.now()
})
```

#### Reusing Questions Across Courses

```typescript
// User: "Use the same microphone questions in RA&T 121"

// 1. Query questions used in 120
const questions = registry_get_questions({
  topic: "microphone-types",
  usedInCourse: "RA&T 120"
})

// 2. Create quiz in 121 with same questions
registry_create_quiz({
  courseId: rat121CourseId,
  title: "Quiz 1: Microphones",
  questionIds: questions.map(q => q._id)  // Reuse!
})

// Question bank enables cross-course reuse
```

### Multi-Format Export (Future)

**Canvas deployment:**
```typescript
// Uses format_canvas field
question.format_canvas = {
  question_name: "...",
  question_type: "multiple_choice_question",
  answers: [...]
}
```

**midimaze 2.0 deployment:**
```typescript
// Uses format_midimaze field
question.format_midimaze = {
  question: "...",
  options: ["A", "B", "C", "D"],
  correctIndex: 1,
  explanation: "Ribbon mics use a thin conductive ribbon...",
  mediaUrl: "https://midimaze.com/audio/ribbon-mic-example.mp3"
}
```

**Key benefit:** Questions created ONCE, deployed to MULTIPLE platforms

## Migration Path: Phase 1 → Phase 2

### Step 1: Registry Schema Design (Not Yet Started)

**Tasks:**
- [ ] Design courses table schema
- [ ] Design quizzes table schema
- [ ] Design questions table schema
- [ ] Add to Registry `convex/schema.ts`
- [ ] Deploy schema changes

### Step 2: MCP Server Tools (Not Yet Started)

**Tasks:**
- [ ] Add course CRUD tools to registry-mcp
- [ ] Add quiz CRUD tools
- [ ] Add question CRUD tools
- [ ] Add Canvas deployment tool
- [ ] Test MCP tools in OpenCode

### Step 3: Question Bank Migration (Not Yet Started)

**Tasks:**
- [ ] Extract existing quiz questions from Canvas
- [ ] Tag with topics + difficulty
- [ ] Generate both Canvas + midimaze formats
- [ ] Import to Registry questions table
- [ ] Verify format compatibility

### Step 4: Course Data Population (Not Yet Started)

**Tasks:**
- [ ] Add current courses to Registry
- [ ] Link Canvas course IDs
- [ ] Add assignment group IDs
- [ ] Import student rosters
- [ ] Test course queries

### Step 5: Nested Skills Development (Not Yet Started)

**Tasks:**
- [ ] Create question-creation skill
- [ ] Create quiz-creation skill
- [ ] Create quiz-deployment skill
- [ ] Update swc-teaching to route to nested skills
- [ ] Test skill orchestration

### Step 6: Automation Implementation (Not Yet Started)

**Tasks:**
- [ ] Build Drive access audit automation
- [ ] Build roster reconciliation automation
- [ ] Build grade anomaly detection
- [ ] Build studio booking sync
- [ ] Test end-to-end workflows

---

## Common Tasks (Current Manual Workflows)

### Task 1: Create Quiz for New Week

**Current manual workflow:**

1. **Determine quiz content**
   - Review week's topics
   - Decide question count, difficulty
   - Check syllabus for due date

2. **Craft questions manually**
   - Write question text
   - Create answer options
   - Mark correct answers
   - Format as Canvas API JSON

3. **Create quiz in Canvas**
   ```bash
   # POST quiz creation
   curl -X POST \
     https://swccd.instructure.com/api/quiz/v1/courses/76165/quizzes \
     -H "Authorization: Bearer TOKEN" \
     -d '{
       "title": "Quiz 3: Signal Flow",
       "assignment_group_id": 191246,
       "due_at": "2025-10-15T23:59:00Z",
       "quiz_settings": {...}
     }'
   ```

4. **Upload questions one by one**
   ```bash
   # For each question:
   curl -X POST \
     /api/v1/courses/76165/quizzes/QUIZ_ID/questions \
     -H "Authorization: Bearer TOKEN" \
     -d '{ question JSON }'
   ```

5. **Verify in Canvas UI**
   - Check question display
   - Test quiz preview
   - Publish when ready

**Pain points:**
- 20-30 questions = 20-30 API calls
- No question reuse across courses
- Easy to make JSON formatting errors
- No tracking of question performance

### Task 2: Semester Setup

**Current manual workflow:**

1. **Get new course IDs**
   - Login to Canvas
   - Navigate to each course
   - Extract course ID from URL
   - Update `Canvas Management Planning.md`

2. **Get assignment group IDs**
   ```bash
   curl https://swccd.instructure.com/api/v1/courses/COURSE_ID/assignment_groups
   ```
   - Parse response
   - Update planning doc with IDs

3. **Build calendar**
   - Open `Calendar Planning.md`
   - Map weeks to topics
   - Schedule module unlocks
   - Set quiz due dates

4. **Update Google Groups**
   - Export Canvas roster (CSV)
   - Manually add to Google Groups
   - Verify access permissions

5. **Prepare Drive**
   - Create semester folder structure
   - Set sharing permissions
   - Share with student group

**Pain points:**
- Repetitive manual updates
- Risk of copy-paste errors
- Time-consuming roster sync

### Task 3: Midterm Grade Review

**Current manual workflow:**

1. **Export gradebook from Canvas**
   - Per course section
   - CSV format

2. **Open in spreadsheet**
   - Calculate grade distributions
   - Flag missing assignments (manual)
   - Identify students at risk

3. **Draft intervention emails**
   - Manually craft per student
   - CC relevant advisors
   - Track follow-ups in planning doc

**Pain points:**
- Manual anomaly detection
- No automated flagging
- Time-consuming per-student review

### Task 4: End of Semester Cleanup

**Current manual workflow:**

1. **Revoke Google Group access**
   - Manually remove dropped students
   - Archive semester group

2. **Archive Canvas course**
   - Export course content
   - Store in vault Course Archive
   - Write course blog summary

3. **Update equipment inventory**
   - Audit mic locker
   - Check studio gear
   - Log any issues

**Pain points:**
- Easy to miss access revocations
- Manual archival process

## Future Task Examples (Database-First)

### Task 1: Create Quiz (Future Automated)

**User request:** "Create Quiz 3 for RA&T 120 with 15 easy signal-flow questions, due Oct 15"

**Automated workflow:**
```typescript
// 1. Agent queries Registry question bank
const questions = registry_get_questions({
  topic: "signal-flow",
  difficulty: "easy",
  limit: 15,
  status: "active"
})

// 2. Agent gets course info
const course = registry_get_course({
  code: "RA&T 120",
  semester: "Fall 2025"
})

// 3. Agent creates quiz in Registry
const quiz = registry_create_quiz({
  courseId: course._id,
  title: "Quiz 3: Signal Flow",
  questionIds: questions.map(q => q._id),
  assignmentGroupId: course.assignmentGroups.assessments,
  dueAt: "2025-10-15T23:59:00Z",
  settings: { /* defaults */ }
})

// 4. Agent deploys to Canvas
registry_deploy_quiz_to_canvas({ quizId: quiz._id })

// Done! 15 questions deployed in seconds
```

**Time saved:** 30-60 minutes → 30 seconds

### Task 2: Cross-Course Question Reuse (Future)

**User request:** "Use the same microphone basics questions in both 120 and 121"

**Automated workflow:**
```typescript
// 1. Get questions from 120
const questions = registry_get_questions({
  topic: "microphone-basics",
  usedInCourse: "RA&T 120"
})

// 2. Create quiz in 121 with same questions
registry_create_quiz({
  courseId: rat121CourseId,
  title: "Quiz 1: Microphone Fundamentals",
  questionIds: questions.map(q => q._id)  // Reuse!
})

// Questions automatically available in 121
```

**Benefit:** Question consistency across courses, no duplication

### Task 3: Grade Anomaly Detection (Future)

**User request:** "Check for students at risk in all courses"

**Automated workflow:**
```typescript
// Agent queries Registry + Canvas
const anomalies = registry_detect_grade_anomalies({
  courses: ["RA&T 120", "RA&T 121", "RA&T 123"],
  criteria: {
    missingAssignments: ">= 3",
    attendanceBelow: 80,
    gradeDrop: ">= 15"  // 15% drop from previous average
  }
})

// Returns:
// [
//   {
//     student: "John Doe",
//     course: "RA&T 120",
//     issues: ["Missing 4 assignments", "Attendance: 65%"],
//     suggestedAction: "Schedule intervention meeting"
//   }
// ]
```

**Time saved:** 2-3 hours of manual review → instant report

## Best Practices (Current)

### Documentation

1. **Update planning docs immediately**
   - Don't wait until weekly review
   - Capture decisions in Daily Journal
   - Link to relevant planning docs

2. **Maintain course IDs**
   - Update Canvas Management Planning each semester
   - Verify assignment group IDs haven't changed
   - Test API calls with new IDs

3. **Track automation ideas**
   - Note repetitive tasks as automation targets
   - Document desired workflows
   - Estimate time savings

### API Usage

1. **Test in Postman first**
   - Verify payload structure
   - Check response format
   - Save successful requests

2. **Use environment variables**
   - Never hardcode API tokens
   - Rotate tokens regularly
   - Store in secure credential manager

3. **Validate before bulk operations**
   - Test with single item first
   - Verify in Canvas UI
   - Then proceed with batch

### Delegation

1. **Document delegation boundaries clearly**
   - Safe tasks list for interns
   - Approval-required tasks list
   - Escalation procedures

2. **Track intern assignments**
   - Log who's responsible
   - Set deadlines
   - Verify completion

3. **Provide templates**
   - Announcement templates
   - Email templates
   - Checklist templates

## Integration Points

### With Registry Database (Future)

**courses table:**
- Stores Canvas IDs, assignment groups
- Links to students, quizzes
- Tracks semester status

**quizzes table:**
- Quiz metadata, settings
- Links to questions, courses
- Deployment status tracking

**questions table:**
- Question bank (source of truth)
- Multi-format storage (Canvas + midimaze)
- Topic/difficulty tagging
- Usage analytics

### With Canvas API (Current & Future)

**Current:** Manual API calls via Postman/curl

**Future:** Automated via MCP server
- Course sync
- Quiz deployment
- Roster management
- Grade queries

### With Google Workspace (Current Manual, Future Auto)

**Current:**
- Manual Drive audits
- Manual Groups sync
- Spreadsheet tracking

**Future:**
- Automated permission checks
- Auto-sync Canvas → Groups
- API-driven roster updates

### With midimaze 2.0 (Future)

**Question deployment to website:**
- Use `format_midimaze` from Registry
- Public quiz pages
- Educational content
- Analytics tracking

## Security & Credentials

**Canvas API Tokens:**
- Generate in Canvas → Settings → Approved Integrations
- Store in environment variables: `CANVAS_API_TOKEN`
- Never commit to git/vault
- Rotate every semester

**Google Workspace:**
- Service account for automation
- Reference by name only in docs
- OAuth for interactive operations

**Internal Scheduler:**
- Check with faculty before automation
- Separate credentials per user
- Audit access regularly

## Troubleshooting (Current)

### Canvas API Errors

**401 Unauthorized:**
- Check API token validity
- Verify token has correct permissions
- Regenerate if expired

**422 Unprocessable Entity:**
- Validate JSON payload structure
- Check required fields present
- Verify data types match API spec

**404 Not Found:**
- Verify course ID correct
- Check quiz ID exists
- Confirm endpoint URL correct

### Google Workspace Issues

**Permission Denied:**
- Check service account permissions
- Verify domain delegation
- Confirm API enabled in console

**Group Not Found:**
- Verify group email correct
- Check group exists
- Confirm access permissions

## Related Documentation

**Vault context:**
- `~/Code/github.com/theslyprofessor/midimaze/_Nakul/3. SWC Actions/AGENTS.md`
- `~/Code/github.com/theslyprofessor/midimaze/_Nakul/3. SWC Actions/SWC Actions Planning.md`

**Registry integration (future):**
- `~/Code/github.com/theslyprofessor/registry/AGENTS.md`

**Canvas API:**
- [Canvas LMS REST API Documentation](https://canvas.instructure.com/doc/api/)
- [Quiz API](https://canvas.instructure.com/doc/api/quizzes.html)
- [Assignment API](https://canvas.instructure.com/doc/api/assignments.html)

## See Also

- **Related Skills:**
  - `registry-database` - Database platform (future courses/quizzes/questions tables)
  - `obsidian-workflows` - Vault management, planning docs
  
- **Future Nested Skills:**
  - `question-creation` - Create questions in Registry
  - `quiz-creation` - Assemble quizzes from question bank
  - `quiz-deployment` - Deploy Registry → Canvas
  - `course-management` - Roster sync, grading automation

## Quick Reference

### Current Course IDs (Fall 2025)

```
120-501: 74904
120:     76165
121:     76169
123:     76171
```

### Canvas API Endpoints

```http
# Quiz creation
POST /api/quiz/v1/courses/:course_id/quizzes

# Add questions
POST /api/v1/courses/:course_id/quizzes/:quiz_id/questions

# Get assignment groups
GET /api/v1/courses/:course_id/assignment_groups

# Get quizzes
GET /api/v1/courses/:course_id/quizzes
```

### Key Concepts

- **Phase 1 (Current):** Manual Canvas API, hardcoded IDs, per-course questions
- **Phase 2 (Future):** Database-first, question bank, multi-format export, nested skills
- **Question bank:** Reusable across courses, tagged by topic/difficulty
- **Multi-format:** `format_canvas` + `format_midimaze` in single question
- **Nested skills:** question-creation, quiz-creation, quiz-deployment
- **MCP integration:** registry-mcp extension for Canvas operations
