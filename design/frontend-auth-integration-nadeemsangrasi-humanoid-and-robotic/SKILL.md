---
name: Frontend Auth Integration
description: Integrates Better Auth client with ChatKit UI or custom Next/Vite UI. Adds login/logout buttons, protected routes, session hooks.
---

# Frontend Auth Integration

## Instructions

1. Integrate Better Auth client with frontend:
   - Set up authentication provider wrapper
   - Configure authentication hooks (useAuth, useSession)
   - Add login/logout functionality
   - Create protected route components

2. Integrate with ChatKit UI:
   - Wrap ChatKit with authentication provider
   - Add authentication checks before chat access
   - Create login overlay if not authenticated
   - Include user profile display

3. Create authentication UI components:
   - Login form with email/password
   - OAuth provider buttons
   - User profile dropdown
   - Loading and error states

4. Implement protected routes:
   - Create authentication middleware
   - Redirect unauthenticated users
   - Preserve redirect URLs
   - Handle session expiration

5. Follow Next.js/React best practices:
   - Use proper TypeScript types
   - Include proper error boundaries
   - Handle loading states
   - Follow accessibility standards

## Examples

Input: "Create protected chatbot route with Better Auth"
Output: Creates React code with:
```typescript
import { useAuth } from 'better-auth/react'

function ProtectedChatPage() {
  const { user, isPending } = useAuth()

  if (isPending) {
    return <div>Loading...</div>
  }

  if (!user) {
    return <div>Please log in to access the chatbot</div>
  }

  return <ChatKitPanel />
}
```