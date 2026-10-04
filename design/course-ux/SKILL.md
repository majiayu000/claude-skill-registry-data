---
name: course-ux
description: Audit and fix course player UX against LMS best practices — layout proportions, progressive disclosure, progress psychology, sidebar hierarchy, video sizing, light/dark harmony, sidebar naming & learning flow, cohort pacing, and AI integration points. Use when improving the learn experience.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, Agent
---

Audit and improve the course learn experience UX: $ARGUMENTS

$ARGUMENTS can be:
- `audit` — Full UX audit, report only (no changes)
- `audit [dimension]` — Audit a single dimension (e.g., `audit proportions`)
- `fix [dimension]` — Audit + apply fixes for a dimension
- `fix all` — Audit + apply all fixes (confirm with user before each change)
- Empty — defaults to `audit`

## Before Starting

Read these files to understand the current state:

1. `src/components/courses/learn/CourseLearnLayout.tsx` — layout structure (sidebar + content proportions)
2. `src/components/courses/learn/CourseLearnSidebar.tsx` — sidebar navigation, week grouping, progress display
3. `src/components/courses/learn/CourseTopbar.tsx` — progress bar, next section nav
4. `src/components/courses/learn/LessonPanel.tsx` — lesson content wrapper
5. `src/components/courses/learn/LessonContent.tsx` — content dispatcher
6. `src/components/courses/learn/LessonTabs.tsx` — tabbed content (overview, transcript, resources)
7. `src/components/courses/learn/LessonPanelFooter.tsx` — prev/next navigation
8. `src/components/courses/sections/VideoSection.tsx` — video section rendering
9. `src/components/content/VideoPlayer.tsx` — video player component
10. `src/app/globals.css` — CSS variables, light/dark mode tokens

Also read the course overview page if auditing course entry:
- `src/app/(public)/content/courses/[slug]/learn/page.tsx`

## Audit Dimensions

### 1. CONTENT AREA PROPORTIONS

**Best practice:** Video and primary content should occupy 70-75% of viewport width on desktop. Sidebar should be 25-30%.

Check:
- [ ] Sidebar width is 240-300px fixed (not percentage-based)
- [ ] Content area uses `flex-1` or equivalent to fill remaining space
- [ ] Video player stretches to full content-area width (no unnecessary padding/margins)
- [ ] On tablet (768-1024px), sidebar collapses to drawer — content goes full-width
- [ ] Reading content has a max-width constraint (65-75ch) but video does NOT
- [ ] No double-padding (layout padding + content padding stacking)

Common violations:
- Content area too narrow because sidebar is too wide
- Video constrained by a `max-w-*` meant for text content
- Padding stacking: layout adds `p-6` AND content area adds `p-6`

### 2. PROGRESSIVE DISCLOSURE

**Best practice:** Show learners only what they need now. Hide future complexity. "Bird by bird" — Anne Lamott principle applied to LMS.

Check:
- [ ] Total section count is NOT prominently displayed (no "0 of 69 sections")
- [ ] Progress shows week-level granularity: "Week 1 of 8" not "Section 3 of 69"
- [ ] Current week is expanded in sidebar; future weeks are collapsed by default
- [ ] Past weeks show completion state but are collapsed
- [ ] Only current + next section are emphasized in navigation
- [ ] Course overview does not overwhelm with full 8-week breakdown on first visit

Best-in-class pattern (Coursera/Thinkific):
- Sidebar: current week expanded, all others collapsed
- Progress: "Week N" with a small ring/bar, not raw fraction
- Topbar: "Next: [section name]" — single forward action

Violations to flag:
- Raw "0 / 69" displayed anywhere
- All weeks expanded simultaneously
- Section-level counting exposed to user
- Full course outline visible without interaction

### 3. PROGRESS BAR & MOTIVATION

**Best practice:** Progress UI should encourage, not overwhelm. Show momentum, not distance remaining.

Check:
- [ ] Progress indicator shows percentage OR visual fill — not raw fraction
- [ ] Week-level progress preferred over course-level on the topbar
- [ ] No "0%" displayed on first visit (use "Just getting started" or hide until >0)
- [ ] Progress bar has sufficient visual weight (not a tiny 2px line)
- [ ] Completion celebrations exist (checkmark, color change, subtle animation)
- [ ] Progress ring/bar uses `bg-primary` not hardcoded colors
- [ ] Topbar progress does not compete visually with main content

Kajabi pattern: percentage badge + thin progress bar, warm color fill
Thinkific pattern: circular progress ring per module, checkmarks on completion

### 4. SIDEBAR HIERARCHY & BALANCE

**Best practice:** Sidebar should feel like a table of contents, not a wall of text. Visual weight draws the eye to "where you are now."

Check:
- [ ] Active section has strong visual indicator (background highlight + left border or accent)
- [ ] Inactive sections are visually recessed (muted text, no background)
- [ ] Week headers are visually distinct from section items (bolder, larger, or different style)
- [ ] Completed sections show a subtle checkmark or muted state
- [ ] Section type icons are present and consistent (video icon, reading icon, etc.)
- [ ] Sidebar has its own scroll independent of main content (sticky with overflow-y-auto)
- [ ] Vertical spacing between items is consistent (not cramped, not too loose)
- [ ] Sidebar header area (course title, overall progress) does not take excessive vertical space

Visual weight check:
- [ ] Course title/progress area: ~15% of sidebar height
- [ ] Navigation items: ~85% of sidebar height
- [ ] No large empty gaps or unbalanced whitespace

### 5. VIDEO PLAYER SIZING

**Best practice:** Video is the primary content type in most LMS sections. It should be the hero element, not squeezed.

Check:
- [ ] Video player fills full content-area width (minus reasonable padding: 16-24px each side)
- [ ] Video maintains 16:9 aspect ratio via `aspect-video` or equivalent
- [ ] No max-width constraint narrower than the content area on video
- [ ] Video section has minimal chrome above/below — section title, then video, then transcript
- [ ] Transcript accordion/dropdown sits directly below video, same width
- [ ] No duplicate transcript rendering (both accordion AND tab)
- [ ] "Video coming soon" placeholder is styled and sized to match video dimensions

### 6. TRANSCRIPT & SUPPLEMENTARY CONTENT

**Best practice:** Transcript should be accessible but not compete with video. Single rendering, clear hierarchy.

Check:
- [ ] Transcript appears in ONE location only (either tabs OR accordion — not both)
- [ ] If using tabs: "Overview" is default tab, "Transcript" is secondary
- [ ] If using accordion: collapsed by default, below video
- [ ] Transcript text has readable typography (16px+, good line-height, max-width ~75ch)
- [ ] Resources tab/section exists if the lesson has resources
- [ ] Tabs/accordion use same width as the video player (visual alignment)

Preferred pattern: Tabs below video (Overview | Transcript | Resources)
- This is the pattern used by Coursera, Udemy, and most modern LMS platforms

### 7. LIGHT/DARK MODE HARMONY

**Best practice:** Both modes must feel intentional, not like one is an afterthought.

Check:
- [ ] Scan all course learn components for color token usage
- [ ] No hardcoded colors (grep for hex, rgb, `bg-{color}-{shade}`)
- [ ] Background layers create clear depth separation:
  - Dark: sidebar slightly lighter than main bg, or subtle border separation
  - Light: sidebar slightly tinted or bordered, not flat white-on-white
- [ ] Text contrast meets WCAG AA in BOTH modes
- [ ] Interactive elements (buttons, links, active states) are visible in both modes
- [ ] Video player area has neutral dark background in both modes (video always looks best on dark)
- [ ] Progress indicators have sufficient contrast in light mode
- [ ] Card/surface backgrounds use `bg-card` not `bg-background` for elevated elements

Light mode specific checks:
- [ ] Primary accent color is not too dark/heavy for light backgrounds
- [ ] Sidebar does not feel washed out or invisible
- [ ] Borders/dividers provide structure without heaviness

### 8. SPACING & VERTICAL RHYTHM

**Best practice:** Consistent spacing creates visual calm. Inconsistent spacing creates unease.

Check:
- [ ] Topbar height is consistent and not cramped (48-56px)
- [ ] Gap between topbar and content is intentional (16-24px)
- [ ] Section title to content gap is consistent across section types
- [ ] Sidebar item padding is uniform (12-16px vertical, 16-20px horizontal)
- [ ] Content area has symmetric horizontal padding
- [ ] Footer navigation (prev/next) has clear separation from content above
- [ ] No spacing jumps between different section types
- [ ] Typography margins follow a consistent scale (use Tailwind spacing)

Scan for spacing antipatterns:
- Arbitrary values: `p-[13px]`, `mt-[7px]`, `gap-[11px]`
- Inconsistent padding between similar elements
- Missing gap between video and transcript
- Topbar content not vertically centered

### 9. CONTEXT DISCOVERY FLOW

**Best practice:** Onboarding should be structured (form), not open-ended (chat). Reduce cognitive load at course entry.

Check:
- [ ] Context Discovery section uses a structured form, not a chat interface
- [ ] Form is <=10 minutes estimated completion time
- [ ] Form collects: learner background, goals, experience level, context
- [ ] Form exists as a reusable component (shared with AI Lab intro if applicable)
- [ ] After form completion, transitions to lesson content — not more questions
- [ ] If chat IS used, it's positioned AFTER form completion, not as the entry point

Components to check:
- Any ContextDiscovery* or Intake* components in `src/components/courses/`
- The section type mapping for context_discovery in SectionContent.tsx

### 10. AI INTEGRATION POINTS

**Best practice:** AI assistance should be contextually relevant, not omnipresent. It should enhance learning, not distract from it.

Check:
- [ ] AI Lab drawer/button is present but non-intrusive (bottom-right FAB or sidebar icon)
- [ ] AI drawer is contextually aware of current lesson (passes lesson context)
- [ ] AI is NOT auto-opened or auto-prompted on lesson load
- [ ] During video playback, AI button does not overlay video controls
- [ ] AI availability respects feature flags (`tenant.features.chat`)
- [ ] Consider: should AI be hidden during certain section types (e.g., reflection, journaling)?

### 11. SIDEBAR NAMING & LEARNING FLOW

**Best practice:** Sidebar titles should guide learner action, not describe content. The sidebar answers "What should I do next?" — not "What is this about?" This is the Kajabi/Teachable guided-journey pattern vs the Udemy table-of-contents pattern.

**Two-title system:**
- **Sidebar titles** = action-based CTAs (verbs). Guide learner flow. These are navigation labels.
- **Content page titles** = topic-based. Describe the lesson content. Editable by course creator.
- Sidebar title does NOT need to match content page title.

Check:
- [ ] Sidebar items use action/verb language, not topic nouns
- [ ] Content page titles remain subject-matter titles (unchanged by this dimension)
- [ ] Sidebar title and content title are stored/rendered independently
- [ ] No sidebar item reads like a chapter heading (e.g., "Recovering Apostolic Genius" should be "Watch the Introduction")

**Standard weekly flow (Weeks 2–7):**

Each week follows a consistent 7-step rhythm. Learners should recognize this pattern week to week:

1. **Watch the Introduction** — weekly video intro
2. **Begin the Conversation** — AI Interaction 1: Dissonance conversation (~10 min). Provokes curiosity, introduces tension.
3. **Explore the Week's Content** — teaching content (video, reading, articles). Flexible per week.
4. **Discern Your Next Step** — AI Interaction 2: Discernment conversation (~10 min). Connects content to a concrete micro-practice.
5. **Reflect on the Week** — AI Interaction 3: Reflection (~10 min). Processes insights, integrates learning.
6. **Meet with Your Cohort** — synchronous cohort gathering.
7. **Close Out the Week** — exit ticket / closing activity.

**Week 1 variant (onboarding):**

1. Watch the Introduction
2. Get Oriented
3. Introduce Yourself
4. Begin the Conversation
5. Close Out the Week

**Week 8 variant (closing):**
- May differ from Weeks 2–7. Audit should flag if Week 8 uses a non-standard flow and confirm it's intentional.

**AI interaction naming rules:**
- Sidebar CTAs do NOT explicitly reference "AI" — the AI is the facilitator, not the feature.
- "Begin the Conversation" not "Chat with AI about dissonance"
- "Discern Your Next Step" not "AI-guided practice selection"

Violations to flag:
- Sidebar items using topic-based language (nouns, chapter titles)
- Inconsistent flow order between weeks (e.g., reflection before content)
- AI interactions surfaced as "AI Chat" or "Talk to AI" in sidebar
- Week 1 using the standard Weeks 2–7 flow instead of onboarding flow
- Missing steps in the weekly flow

### 12. COHORT PACING & WEEK VISIBILITY

**Best practice:** Cohort-paced courses should focus the learner on the current week. Showing the full 8-week structure creates cognitive noise and undermines the guided-journey feel. Kajabi's "drip content" and Teachable's "scheduled publishing" patterns apply here.

This course is cohort-paced and facilitator-guided — learners progress together week by week and cannot jump ahead arbitrarily.

Check:
- [ ] Current week is prominently expanded in sidebar
- [ ] Future weeks are collapsed, locked, or visually de-emphasized
- [ ] Past weeks are accessible but collapsed (learners can review)
- [ ] No "browse all 8 weeks" view by default — the sidebar is not a course catalog
- [ ] Week header shows week number + title (e.g., "Week 3 — Jesus-Shaped Gospel")
- [ ] Locked/future weeks show a lock icon or muted state — not just collapsed

**Acceptable implementation approaches (lightest to heaviest):**
1. Visually de-emphasize future weeks (muted text, reduced opacity)
2. Collapse future weeks with no expand affordance (or expand shows "Available [date]")
3. Accordion with future weeks locked (click shows "Opens with your cohort on [date]")
4. Hide future weeks entirely from sidebar

**Implementation constraint:** Prefer the lightest approach that achieves focus. Do NOT introduce heavy cohort-management infrastructure for this dimension — visual treatment in the sidebar component is sufficient.

**Interaction with progressive disclosure (Dimension 2):**
- Dimension 2 says "current week expanded, others collapsed" — this dimension adds the **why** (cohort pacing) and the **lock/gate** behavior for future weeks specifically.
- Dimension 2 is about reducing visual noise. This dimension is about enforcing a pacing model.

Violations to flag:
- All 8 weeks visible and expandable simultaneously
- No visual distinction between current, past, and future weeks
- Future weeks fully navigable (learner can click into Week 8 content on day 1)
- No indication of cohort schedule or week availability

## Output Format

```
## Course UX Audit: [slug or "Learn Infrastructure"]

### Overall: X/12 dimensions passing

### Summary
[2-3 sentence executive summary of the biggest UX issues]

### 1. Content Area Proportions: PASS/WARN/FAIL
- Current state: [what it is now]
- Issue: [if any]
- Fix: [specific file:line and what to change]

### 2. Progressive Disclosure: PASS/WARN/FAIL
- Current state: [what's exposed to user]
- Issue: [if any]
- Fix: [specific change]

[... repeat for all 12 dimensions ...]

### Priority Fixes (ordered by user impact)
1. [HIGH] — [description] — [file:line]
2. [HIGH] — [description] — [file:line]
3. [MEDIUM] — [description] — [file:line]
4. [LOW] — [description] — [file:line]

### Quick Wins (< 30 min each)
- [ ] [description] — [file:line]
- [ ] [description] — [file:line]
```

## Fix Mode

When invoked with `fix [dimension]` or `fix all`:

1. Run the audit first — present findings to user
2. For each fix:
   - Show the specific file and current code
   - Explain what changes and why (reference LMS best practice)
   - Apply the edit
3. After all fixes, re-audit the affected dimension to confirm resolution
4. Do NOT touch generated files — if a fix requires a generated file change, note it and suggest regeneration

## Rules

- 8 weeks, numbered 1-8. No Week 0.
- Read actual code — do not assume from file names
- Reference specific LMS platforms (Coursera, Thinkific, Kajabi, Teachable) when citing best practices
- Every issue must include a file path and line number
- Distinguish between layout/structural issues and cosmetic polish
- Do not modify `src/components/ui/*` — fix at the correct layer (layout, section, or globals.css)
- Use semantic color tokens — never introduce hardcoded colors
- This skill audits UX patterns and visual harmony — for code quality use `/course-audit`, for content validation use `/course-validate`
- When fixing, prefer minimal changes that address the specific issue — do not refactor surrounding code
