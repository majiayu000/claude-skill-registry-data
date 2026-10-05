---
name: login-flow
mode: prototype
preview: html
inputs:
  - name: brandName
    type: string
    label: Brand Name
parameters:
  - name: radius
    type: number
    min: 0
    max: 24
    label: Border Radius
outputs:
  primary: index.html
---

# Login & Auth Flow Skill

Generate a complete authentication flow with login, signup, and forgot password screens.

## Rules
- Clean, minimal design
- Form validation with visual feedback
- Password strength indicator
- Social login buttons (Google, GitHub)
- Smooth transitions between screens
- NO generic placeholders — use realistic form labels
- Accessible form markup with proper labels

## Screens
1. Login (email + password + social)
2. Signup (name + email + password + confirm)
3. Forgot password (email + success state)
4. Reset password (new password + confirm)

## Technical
- Single-file HTML with view-state switching (no routing)
- CSS transitions for screen changes
- Form validation logic in vanilla JS
- Password visibility toggle
