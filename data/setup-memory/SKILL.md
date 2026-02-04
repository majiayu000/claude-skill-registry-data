---
name: setup-memory
description: "Configure Nexus memory with your role, goals, and preferences. Load when user wants to personalize the system or teach Nexus about themselves. Keywords: setup memory, personalize, configure, my goals, my role, about me, preferences. 8 min."
onboarding: true
priority: critical
---

## 🎯 AI Proactive Triggering (ONBOARDING SKILL - CRITICAL PRIORITY)

**This is the FIRST onboarding skill with CRITICAL priority. Suggest early and often.**

### When to Proactively Suggest (AI MUST check user-config.yaml)

Check `learning_tracker.completed.setup_goals` AND `goals.md` for `smart_default: true`. If not personalized:

**PROACTIVELY SUGGEST when user:**
1. **FIRST SESSION**: Always suggest during first interaction if goals not set
2. Asks for help with work that would benefit from context (AI can personalize better after setup)
3. Uses Nexus for meaningful work but hasn't personalized yet
4. Mentions their role, job, or what they do
5. Expresses frustration that AI doesn't understand their context
6. At menu display when `goals_personalized: false` - PROMINENTLY highlight

**Suggestion Pattern (first session):**
```
💡 Welcome to Nexus! I'm currently using smart defaults. To help you most
effectively, I'd love to learn about:
- Your role and work context
- Your goals (short-term and long-term)
- Your preferences

This takes about 8 minutes and dramatically improves our collaboration.
Say 'setup goals' to personalize, or continue with defaults.
```

**Suggestion Pattern (returning user, still on defaults):**
```
💡 I notice you're still using Nexus defaults. Personalizing takes 8 minutes
and helps me understand your work context, goals, and preferences.

Ready to 'setup goals'? (This is a one-time setup that improves every session)
```

**Menu Integration:**
When displaying menu with `goals_personalized: false`:
```
🧠 MEMORY
   ⚠️ Not personalized ▸ 'setup goals' (8 min, highly recommended)
```

**DO NOT suggest if:**
- `learning_tracker.completed.setup_goals: true`
- `goals.md` no longer has `smart_default: true`
- User explicitly declined personalization multiple times

---

# Setup Goals

Guide user through goal definition and system personalization.

## Purpose

Transform smart default templates into meaningful, personalized context that improves AI collaboration quality. Captures user's role, short-term goals (3 months), long-term vision (1-3 years), and work preferences.

**Time Estimate**: 8-10 minutes

---

## Workflow

### Step 1: Welcome & Language

**Display**:
```
━━━ SETUP GOALS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Let's personalize Nexus to understand your work context.
This takes about 8-10 minutes and improves AI collaboration.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Ask**: "What language would you like me to use? (English is default)"

**Action**: Store preference in user-config.yaml, switch all communication.

---

### Step 2: Role Discovery

**Ask**: "What do you do? Tell me about your current role or situation."

**AI Suggestion Pattern**: Listen, then offer 2-3 refined versions. Let user pick or refine.

**Store**: Update `## Current Role` in goals.md

---

### Step 3: Short-Term Goal

**Ask**: "What's the ONE thing you want to achieve in the next 3 months?"

**Help make it specific and measurable**. Capture:
- The goal itself
- Why it matters (motivation)
- 2-3 success metrics

**Store**: Update `## Short-Term Goal (3 months)` in goals.md

---

### Step 4: Long-Term Vision

**Ask**: "Where do you want to be in 1-3 years?"

Connect to short-term goal to show trajectory.

**Store**: Update `## Long-Term Vision (1-3 years)` in goals.md

---

### Step 5: Work Preferences

Quick questions:
1. "When do you do best work?" (morning/afternoon/evening)
2. "Typical session length?" (30min, 1hr, 2hrs+)
3. "What types of work?" (writing, coding, research, planning...)

**Store**: Update `## Work Style & Preferences` in goals.md

---

### Step 6: Finalize

**Actions** (MUST complete all):

1. **Remove `smart_default: true`** from goals.md YAML frontmatter (if present)

2. **Update `Last Updated`** timestamp in goals.md

3. **Mark skill complete** in user-config.yaml:
   ```yaml
   learning_tracker:
     completed:
       setup_goals: true  # ADD THIS LINE
   ```

4. **Update language** in user-config.yaml (if user specified):
   ```yaml
   user_preferences:
     language: "{user's language}"
   ```

5. **Display completion**:
   ```
   ✅ Setup Goals Complete!

   Captured:
   • Your role and work context
   • Short-term goal (3 months) with success metrics
   • Long-term vision (1-3 years)
   • Work style preferences

   Nexus now understands you. Context loads every session.

   Next steps:
   • 'setup workspace' - Organize your folders
   • 'learn projects' - Understand project workflow
   • 'create project' - Start working
   ```

---

### Step 7: Close-Session Practice

**Display**:
```
━━━ IMPORTANT HABIT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
When done working, always say "done" or "close session".
This saves progress and helps me remember context.
Let's practice - say "done" now!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wait for "done", then trigger close-session.

---

## Success Criteria

- [ ] Language preference captured in user-config.yaml
- [ ] Role clearly defined in goals.md
- [ ] Short-term goal specific and measurable
- [ ] Success metrics defined
- [ ] Long-term vision captured
- [ ] `smart_default: true` removed from goals.md
- [ ] `learning_tracker.completed.setup_goals: true` in user-config.yaml
- [ ] User practiced close-session
