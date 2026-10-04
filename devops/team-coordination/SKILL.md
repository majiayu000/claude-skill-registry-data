---
name: team-coordination
description: Multi-person projects - shared state, todo claiming, handoffs
when-to-use: When multiple developers are working on the same repo
user-invocable: false
effort: low
---

# Team Coordination Skill


**Purpose:** Enable multiple Claude Code sessions across a team to coordinate and work together without conflicts. Manages shared state, todo claiming, decision syncing, and session awareness.

---

## Core Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│  TEAM CLAUDE CODE                                               │
│  ─────────────────────────────────────────────────────────────  │
│  Multiple devs, multiple Claude sessions, one codebase.         │
│  Coordination > Speed. Communication > Assumptions.             │
│                                                                 │
│  Before you start: Check who's working on what.                 │
│  Before you claim: Make sure nobody else has it.                │
│  Before you decide: Check if it's already decided.              │
│  Before you push: Pull and sync state.                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Team State Structure

When a project becomes multi-person, create this structure:

```
_project_specs/
├── team/
│   ├── state.md              # Who's working on what right now
│   ├── contributors.md       # Team members and their focus areas
│   └── handoffs/             # Notes when passing work to others
│       └── [feature]-handoff.md
├── session/
│   ├── current-state.md      # YOUR session state (personal)
│   ├── decisions.md          # SHARED - architectural decisions
│   └── code-landmarks.md     # SHARED - important code locations
└── todos/
    ├── active.md             # SHARED - with claim annotations
    ├── backlog.md            # SHARED
    └── completed.md          # SHARED
```

---

## Team State File

**`_project_specs/team/state.md`:**

```markdown
# Team State

*Last synced: [timestamp]*

## Active Sessions

| Contributor | Working On | Started | Files Touched | Status |
|-------------|------------|---------|---------------|--------|
| @alice | TODO-042: Add auth | 2024-01-15 10:30 | src/auth/* | 🟢 Active |
| @bob | TODO-038: Fix checkout | 2024-01-15 09:00 | src/cart/* | 🟡 Paused |
| - | - | - | - | - |

## Claimed Todos

| Todo | Claimed By | Since | ETA |
|------|------------|-------|-----|
| TODO-042 | @alice | 2024-01-15 | Today |
| TODO-038 | @bob | 2024-01-14 | Tomorrow |

## Recently Completed (Last 48h)

| Todo | Completed By | When | PR |
|------|--------------|------|-----|
| TODO-037 | @alice | 2024-01-14 | #123 |

## Conflicts to Watch

| Area | Contributors | Notes |
|------|--------------|-------|
| src/auth/* | @alice, @carol | Carol needs auth for TODO-045, coordinate |

## Announcements

- [2024-01-15] @alice: Refactoring auth module, avoid touching until EOD
- [2024-01-14] @bob: New env var required: STRIPE_WEBHOOK_SECRET
```

---

## Contributors File

**`_project_specs/team/contributors.md`:**

```markdown
# Contributors

## Team Members

| Handle | Name | Focus Areas | Timezone | Status |
|--------|------|-------------|----------|--------|
| @alice | Alice Smith | Backend, Auth | EST | Active |
| @bob | Bob Jones | Frontend, Payments | PST | Active |
| @carol | Carol White | DevOps, Infra | GMT | Part-time |

## Ownership

| Area | Primary | Backup | Notes |
|------|---------|--------|-------|
| Authentication | @alice | @bob | All auth changes need @alice review |
| Payments | @bob | @alice | Stripe integration |
| Infrastructure | @carol | @alice | Deploy scripts, CI/CD |
| Database | @alice | @carol | Migrations need sign-off |

## Communication

- Slack: #project-name
- PRs: Always tag area owner for review
- Urgent: DM on Slack

## Working Hours Overlap

```
EST:  |████████████████████|
PST:  |   ████████████████████|
GMT:  |████████████|
      6am        12pm       6pm       12am EST

Best overlap: 9am-12pm EST (all three)
```
```

---

## Workflow

### Starting a Session

```
┌─────────────────────────────────────────────────────────────────┐
│  START SESSION CHECKLIST                                        │
│  ─────────────────────────────────────────────────────────────  │
│  1. git pull origin main                                        │
│  2. Read _project_specs/team/state.md                           │
│  3. Check claimed todos - don't take what's claimed             │
│  4. Claim your todo in active.md                                │
│  5. Update state.md with your session                           │
│  6. Push state changes before starting work                     │
│  7. Start working                                               │
└─────────────────────────────────────────────────────────────────┘
```

### Claiming a Todo

In `active.md`, add claim annotation:

```markdown
## [TODO-042] Add email validation

**Status:** in-progress
**Claimed:** @alice (2024-01-15 10:30 EST)
**ETA:** Today

...
```

### During Work

- Update `state.md` if you touch new files
- Check `decisions.md` before making architectural choices
- If you make a decision, add it to `decisions.md` immediately
- Push state updates every 1-2 hours (keeps team in sync)

### Ending a Session

```
┌─────────────────────────────────────────────────────────────────┐
│  END SESSION CHECKLIST                                          │
│  ─────────────────────────────────────────────────────────────  │
│  1. Commit your work (even if WIP)                              │
│  2. Update your current-state.md                                │
│  3. Update team state.md (status → Paused or Done)              │
│  4. If passing to someone: create handoff note                  │
│  5. Unclaim todo if abandoning                                  │
│  6. Push everything                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Creating a Handoff

When passing work to another team member, create:

**`_project_specs/team/handoffs/auth-feature-handoff.md`:**

```markdown
# Handoff: Auth Feature (TODO-042)

**From:** @alice
**To:** @bob
**Date:** 2024-01-15

## Status

70% complete. Core auth flow works, need to add:
- [ ] Password reset flow
- [ ] Email verification

## What's Done

- Login/logout working
- JWT tokens implemented
- Session management done

## What's Left

1. Password reset - see src/auth/reset.ts (skeleton exists)
2. Email verification - need to integrate SendGrid

## Key Decisions Made

- Using JWT not sessions (see decisions.md)
- Tokens expire in 7 days
- Refresh tokens stored in httpOnly cookies

## Watch Out For

- The `validateToken` function has a weird edge case with expired tokens
- Don't touch `authMiddleware.ts` - it's fragile rn

## Files to Start With

1. src/auth/reset.ts - password reset
2. src/email/verification.ts - email flow
3. tests/auth.test.ts - add tests here

## Questions?

Slack me @alice if stuck
```

---

## Conflict Prevention

### File-Level Awareness

Before modifying a file, check state.md for who's touching what:

```markdown
## Active Sessions

| Contributor | Working On | Started | Files Touched | Status |
|-------------|------------|---------|---------------|--------|
| @alice | TODO-042 | ... | src/auth/*, src/middleware/* | 🟢 Active |
```

If you need to touch `src/auth/*` and Alice is working there:
1. Check if it's truly conflicting (same file? same functions?)
2. Coordinate via Slack before proceeding
3. Add a note to "Conflicts to Watch" section

### Pre-Push Check

Before pushing, always:

```bash
git pull origin main
# Resolve any conflicts
git push
```

### PR Tagging

Always tag area owners in PRs:

```markdown
## PR: Add password reset flow

Implements TODO-042

cc: @alice (auth owner), @bob (reviewer)

### Changes
- Added password reset endpoint
- Added email templates

### Testing
- [ ] Unit tests pass
- [ ] Manual testing done
```

---

## Decision Syncing

### Before Making a Decision

1. Pull latest `decisions.md`
2. Check if decision already exists
3. If similar decision exists, follow it (consistency > preference)
4. If new decision needed, add it and push immediately

### Decision Format

```markdown
## [2024-01-15] JWT vs Sessions for Auth (@alice)

**Decision:** Use JWT tokens
**Context:** Need auth for API and mobile app
**Options:**
1. Sessions - simpler, server-side state
2. JWT - stateless, works for mobile
**Choice:** JWT
**Reasoning:** Mobile app needs stateless auth, JWT works across platforms
**Trade-offs:** Token revocation is harder, need refresh token strategy
**Approved by:** @bob, @carol
```

---

## Commands

### Check Team State

```bash
# See who's working on what
cat _project_specs/team/state.md

# Quick active sessions check
grep "🟢 Active" _project_specs/team/state.md
```

### Claim a Todo

1. Edit `_project_specs/todos/active.md`
2. Add claim annotation to todo
3. Update `_project_specs/team/state.md`
4. Commit and push

### Release a Claim

1. Remove claim annotation from todo
2. Update state.md (remove from Claimed Todos)
3. Commit and push

---

## Git Hooks for Teams

### Pre-Push Hook Addition

Add team state sync check to pre-push:

```bash
# In .git/hooks/pre-push (add to existing)

# Check if team state is current
echo "🔄 Checking team state..."
git fetch origin main --quiet

LOCAL_STATE=$(git show HEAD:_project_specs/team/state.md 2>/dev/null | md5)
REMOTE_STATE=$(git show origin/main:_project_specs/team/state.md 2>/dev/null | md5)

if [ "$LOCAL_STATE" != "$REMOTE_STATE" ]; then
    echo "⚠️  Team state has changed on remote!"
    echo "   Run: git pull origin main"
    echo "   Then check _project_specs/team/state.md for updates"
    # Warning only, don't block
fi
```

---

## Claude Instructions

### At Session Start

When user starts a session in a team project:

1. Check for `_project_specs/team/state.md`
2. If exists, read it and report:
   - Who's currently active
   - What todos are claimed
   - Any conflicts to watch
   - Recent announcements

3. Ask what they want to work on
4. Check if it's already claimed
5. Help them claim and update state

### During Session

- Before touching files, check if someone else is working there
- Before making decisions, check decisions.md
- Remind user to update state periodically

### At Session End

- Prompt user to update state.md
- Ask if they need to create a handoff
- Remind them to push state changes

---

## Single → Multi-Person Conversion

When a project needs team coordination:

1. Run `/check-contributors`
2. Create `_project_specs/team/` structure
3. Initialize `state.md` and `contributors.md`
4. Add claim annotations to active todos
5. Update CLAUDE.md to reference team-coordination.md skill

---

## Quick Reference

### Status Icons

```
🟢 Active - Currently working
🟡 Paused - Stepped away, will return
🔴 Blocked - Needs help/waiting on something
⚪ Offline - Not working today
```

### Claim Format

```markdown
**Claimed:** @handle (YYYY-MM-DD HH:MM TZ)
```

### Daily Standup Template

```markdown
## Standup [DATE]

### @alice
- Yesterday: Finished TODO-042 auth flow
- Today: Starting TODO-045 password reset
- Blockers: None

### @bob
- Yesterday: Fixed checkout bug
- Today: Payment webhook integration
- Blockers: Need STRIPE_WEBHOOK_SECRET from @carol
```

---

## Checklist

### Starting Work
- [ ] `git pull origin main`
- [ ] Read `team/state.md`
- [ ] Check todo not claimed
- [ ] Claim todo in `active.md`
- [ ] Update `state.md`
- [ ] Push state changes

### Ending Work
- [ ] Commit all changes
- [ ] Update `current-state.md`
- [ ] Update `team/state.md`
- [ ] Create handoff if needed
- [ ] Push everything
