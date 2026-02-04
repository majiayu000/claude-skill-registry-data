---
name: training-designer
description: This skill should be used when designing training programs, individual workshop sessions, or learning modules using evidence-based frameworks. Use this skill to structure sessions with TBR 4Cs (Connection, Concepts, Concrete Practice, Conclusion), create learning objectives, apply brain-friendly principles, and design session flow.
---

# Training Designer

## Overview

The Training Designer skill helps create high-quality training programs and workshops using evidence-based instructional frameworks. It guides the design of individual sessions using the TBR (Training from the Back of the Room) 4Cs framework and applies brain-friendly learning principles to maximize learner engagement and retention.

## When to Use This Skill

Use Training Designer when:
- Designing individual workshop or training sessions
- Creating learning objectives and session flow
- Planning session timing and activities
- Applying the TBR 4Cs framework to training content
- Ensuring brain-friendly principles (10-1 rule, chunking, active learning)
- Structuring Connection, Concept, Practice, and Conclusion components

## Core Design Principles

### The 4Cs Framework (TBR)

Structure every training session using these four components:

1. **Connection (10-15% of time)**: Activate prior knowledge, build relationships, create psychological safety
2. **Concepts (30-40% of time)**: Deliver content in small chunks (10-15 min max) with processing activities between chunks
3. **Concrete Practice (40-50% of time)**: Hands-on practice starting guided → collaborative → independent
4. **Conclusion (5-10% of time)**: Learner-generated summary, commitments, celebration

### Brain-Friendly Principles

- **10-1 Rule**: 10 minutes of content delivery, 1 minute of processing/activity (minimum)
- **Chunking**: Break content into small, manageable pieces (7-15 minute chunks max)
- **Active Learning**: Learners must talk, teach, and do—not just listen
- **Real Work**: Practice on actual work scenarios, not simulated exercises
- **Multiple Modalities**: Mix lecture, discussion, hands-on, visual, kinesthetic

## Workflow: Session Design Process

Follow this workflow to design training sessions:

### Step 1: Define Session Objectives
- What will learners DO differently after this session?
- What specific skills or knowledge will they gain?
- How will this connect to their real work?

### Step 2: Design Connection Activity (10-15 min)
- Activate relevant prior knowledge
- Build psychological safety and relationships
- Reference existing templates in `references/connection-activities.md`

### Step 3: Design Concept Chunks (30-40% of total time)
- Break content into 10-15 minute chunks maximum
- Add processing activity after each chunk (reflection, discussion, Q&A)
- Reference concept chunk template in `references/concept-chunks.md`

### Step 4: Design Concrete Practice (40-50% of total time)
- Start with guided practice (instructor provides direction)
- Progress to collaborative practice (small groups)
- End with independent practice (solo work)
- Ensure practice mirrors real work scenarios
- Reference practice progression template in `references/practice-activities.md`

### Step 5: Design Conclusion (5-10% of time)
- Facilitate learner-generated summary (not your summary)
- Create commitment to action
- Celebrate progress and learning
- Reference conclusion template in `references/conclusion-activities.md`

### Step 6: Plan Facilitator Notes
- Include exact timing for each section
- Add transition language and key discussion questions
- Include energy management techniques
- Note where flexibility exists for longer discussions

## Concept Chunk Guidelines

When designing concept delivery:

**Chunk Length**: Maximum 10-15 minutes of content
**Processing After Each Chunk**: Minimum 1-2 minutes
**Processing Activities**:
  - Think-Pair-Share discussions
  - Quick reflective writing
  - Small group discussion
  - Q&A with group response
  - Application to real work scenario

**Content Selection**:
  - Focus on "just enough" (not comprehensive coverage)
  - Identify essential concepts vs. nice-to-know
  - Use real work examples
  - Connect to prior knowledge

## Practice Progression Framework

Design practice activities in progression:

**Guided Practice** (Learners with instructor support):
- Instructor models the skill or process
- Learners follow along with the model
- Instructor provides immediate feedback

**Collaborative Practice** (Learners in small groups):
- Groups apply skill to new scenario
- Peer learning and problem-solving
- Shared responsibility

**Independent Practice** (Learners solo):
- Learners apply skill to their own real work
- Minimal support (available if requested)
- Self-assessment and reflection

## Time Allocation Example

For a 4-hour workshop:

- Connection: 20-30 minutes (5-7% of 4 hours is minimum; 10-15% is generous)
- Concepts: 60-90 minutes of content + processing (30-40% = ~70-90 min total)
- Concrete Practice: 90-120 minutes of hands-on work (40-50% = ~100-120 min total)
- Conclusion: 10-15 minutes (5-10% is adequate)
- Breaks: 30-40 minutes total

## Resources

This skill includes templates and guidance for each phase of training design:

### references/
- `connection-activities.md` - Activities to activate prior knowledge and build relationships
- `concept-chunks.md` - Template for designing concept delivery and processing
- `practice-activities.md` - Practice progression from guided → collaborative → independent
- `conclusion-activities.md` - Conclusion strategies and learner-generated summary techniques
- `session-design-template.md` - Complete template for full session design
- `facilitator-notes-template.md` - Template for creating facilitator guides

### scripts/
- `session_planner.py` - Script to generate session timing and component breakdown
- `activity_generator.py` - Script to suggest activities for different content types

### assets/
- `timing-calculator.md` - Quick reference for calculating time allocations

## Integration with Learning Journeys

This skill focuses on individual session design. For complete learning ecosystem design:
- Use **learning-journey-builder** skill for 70:20:10 program design
- Use **coaching-materials-creator** for post-workshop support
- Use **training-reviewer** to validate session design

## Key Reminders

✅ **Do**:
- Design 40-50% of session as hands-on practice
- Use real work scenarios, not simulated exercises
- Build processing time into every concept chunk
- Facilitate learner-generated conclusions (don't provide summary)
- Plan for different learning preferences

❌ **Don't**:
- Lecture for more than 15 minutes straight
- Skip Connection (it's critical for psychological safety)
- End with "Good luck applying this" (plan for follow-up)
- Make practice activities too simplified or artificial
- Forget to include timing in facilitator notes
