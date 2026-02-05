---
name: auth-personalization
description: Add Better Auth signup/signin, personalize chapter content, and persist user preferences. Use when implementing authentication, user sessions, or personalized content delivery.
---

# Auth Personalization Skill

## Instructions

1. **Auth plumbing**
   - Install Better Auth client/server SDKs
   - Configure redirect URIs and cookie/CSRF settings
   - In FastAPI, add auth dependency to protect endpoints
   - Verify tokens server-side

2. **Data model**
   - Neon tables:
     - `users(id, email, name, role)`
     - `preferences(user_id, difficulty, focus_tags, lang)`
   - Reuse `sessions` table if present from RAG service

3. **UX**
   - Docusaurus: add login/logout buttons
   - Display session state in header
   - Guard personalization features behind login
   - Provide preferences UI (dropdowns/tags) saved via backend

4. **Personalization logic**
   - Pass user prefs into RAG prompt context:
     - `difficulty` → adjust answer tone
     - `focus_tags` → rerank payload
   - Store last chapters read for resume suggestions

## Examples

```typescript
// Better Auth client setup
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});
```

```python
# FastAPI auth dependency
from fastapi import Depends, HTTPException

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify Better Auth token
    # Return user or raise 401
    pass
```

## Definition of Done

- Users can sign up/sign in via Better Auth; session recognized by backend
- Preferences persisted in Neon; API to update/fetch works
- RAG responses reflect preferences (tone/focus) when provided
- Basic UI for login + prefs exists in Docusaurus
