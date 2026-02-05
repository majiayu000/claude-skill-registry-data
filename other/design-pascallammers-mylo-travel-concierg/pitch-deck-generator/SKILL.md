---
name: pitch-deck-generator
description: Guides through AI pitch deck generation workflow and troubleshooting. Use when creating pitch decks, debugging wizard errors, troubleshooting Edge Functions, or working with the PitchDeckWizard component.
version: 1.0.0
---

# Pitch Deck Generator Skill

## Purpose
Guide Claude through the pitch deck generation workflow using the project's architecture (React + Supabase + OpenAI Edge Functions).

---

## Architecture Overview

**Frontend**: `/src/pages/PitchDeckWizard.tsx`
**Backend**: `/supabase/functions/pitch-deck-assistant/index.ts`
**Database**: `pitch_conversations` table (stores chat history)
**Tables**: `presentations`, `profiles`, `pitch_conversations`

---

## Workflow Steps

### 1. User Journey
```
User → Chat Interface → Edge Function → OpenAI API → Stream Response
     ↓
Progress Tracking (0-100%)
     ↓
Generate Deck Button (appears at 80%+)
     ↓
Create Presentation → Redirect to /presentations/{id}/outline
```

### 2. Key Files to Check

**Frontend Chat**:
- `src/pages/PitchDeckWizard.tsx` - Main wizard interface
- `src/hooks/usePresentations.ts` - Data fetching logic

**Backend**:
- `supabase/functions/pitch-deck-assistant/index.ts` - Chat endpoint
- `supabase/functions/generate-pitch-deck/index.ts` - Deck generation

**Database**:
- `pitch_conversations` - Stores chat progress
- `presentations` - Stores generated decks

---

## Common Issues & Fixes

### Issue 1: AI Not Responding
**Symptom**: Chat message sent but no response
**Check**:
```bash
# Verify Edge Function is deployed
supabase functions list | grep pitch-deck-assistant

# Check function logs
supabase functions logs pitch-deck-assistant --tail
```
**Fix**: Redeploy if not active
```bash
cd supabase/functions/pitch-deck-assistant
supabase functions deploy pitch-deck-assistant
```

### Issue 2: Progress Not Updating
**Symptom**: Progress bar stuck at same percentage
**Check Database**:
```sql
SELECT id, completeness, collected_data
FROM pitch_conversations
ORDER BY created_at DESC LIMIT 1;
```
**Fix**: Ensure `completeness` field updates in Edge Function

### Issue 3: Generate Button Not Appearing
**Symptom**: Chat completes but no button
**Check**:
- Frontend: `PitchDeckWizard.tsx` line ~120 (button visibility logic)
- Condition: `completeness >= 80`
**Fix**: Verify progress reaches 80%+ in database

### Issue 4: RLS Policy Blocking Access
**Symptom**: 401 errors when fetching presentations
**Check**:
```sql
-- Verify RLS is enabled
SELECT tablename, rowsecurity FROM pg_tables
WHERE tablename = 'presentations';

-- Check if presentation is public or owned by user
SELECT id, is_public, profile_id
FROM presentations
WHERE id = '{presentation_id}';
```
**Fix**: Set `is_public = true` for test presentations

---

## Testing Checklist

### Quick Test (2 minutes)
```bash
# 1. Start dev server
pnpm dev

# 2. Navigate to wizard
# http://localhost:8080/pitch-deck-wizard

# 3. Send test message
# "I want to create a pitch deck for TestCorp, an AI company"

# 4. Verify response appears
# ✅ AI responds
# ✅ Progress bar updates
# ✅ No console errors
```

### Full E2E Test (5 minutes)
1. Open wizard: `/pitch-deck-wizard`
2. Complete conversation (3-4 messages)
3. Verify progress reaches 80%+
4. Click "Generate Deck"
5. Wait for redirect to `/presentations/{id}/outline`
6. Verify all 10 slides render

---

## Edge Function Structure

### Request Format
```json
{
  "conversationId": "uuid",
  "message": "User message text",
  "messages": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ]
}
```

### Response Format (Streaming)
```typescript
data: {"type":"progress","completeness":20,"message":"AI response chunk"}
data: {"type":"message","content":"More text"}
data: {"type":"complete"}
```

---

## Environment Variables

**Required in Edge Function** (Supabase secrets):
- `OPENAI_API_KEY` - OpenAI API key
- `SUPABASE_URL` - Project URL
- `SUPABASE_ANON_KEY` - Public key

**Check secrets**:
```bash
supabase secrets list
```

**Set secret**:
```bash
supabase secrets set OPENAI_API_KEY=sk-...
```

---

## Debugging Commands

### Check Edge Function Status
```bash
supabase functions list
```

### View Live Logs
```bash
supabase functions logs pitch-deck-assistant --tail
```

### Test Edge Function Directly
```bash
curl -X POST \
  "https://dhesktsqhcxhqfjypulk.supabase.co/functions/v1/pitch-deck-assistant" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
  -d '{"message":"Test message"}'
```

### Check Database State
```sql
-- Latest conversations
SELECT id, completeness, created_at
FROM pitch_conversations
ORDER BY created_at DESC LIMIT 5;

-- Recent presentations
SELECT id, title, created_at
FROM presentations
ORDER BY created_at DESC LIMIT 5;
```

---

## Performance Optimization

### Frontend
- Use React.memo for chat messages
- Debounce progress updates (max 1/second)
- Stream responses (don't wait for complete response)

### Backend
- Use OpenAI streaming API
- Return chunks immediately (don't buffer)
- Update database in background

### Database
- Add index on `pitch_conversations.profile_id`
- Add index on `presentations.profile_id`

---

## Security Checklist

- [ ] RLS enabled on `pitch_conversations` ✅
- [ ] RLS enabled on `presentations` ✅
- [ ] API keys only in Edge Functions (never frontend) ✅
- [ ] User can only access own conversations ✅
- [ ] Public presentations accessible to all ✅

---

## Quick Reference

**Start Development**:
```bash
pnpm dev
```

**Deploy Edge Function**:
```bash
supabase functions deploy pitch-deck-assistant
```

**Check Logs**:
```bash
supabase functions logs pitch-deck-assistant --tail
```

**Test Locally**:
- Open: http://localhost:8080/pitch-deck-wizard
- Send message
- Verify response

---

*This skill guides Claude through the complete pitch deck generation workflow, from frontend to backend to database.*
