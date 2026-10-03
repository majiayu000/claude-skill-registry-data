---
name: webapp-auth-csrf
description: "Webapp Auth Csrf."
domain: cybersecurity
---

-|
| CSRF Token | No | N/A |
| SameSite Cookie | Lax | Partial (GET bypass) |
| Origin Validation | No | N/A |
| Referer Validation | No | N/A |
| Custom Header Required | No | N/A |

### Impact
- Account takeover via email change + password reset chain
- Unauthorized fund transfers
- Settings modification (2FA disable, notification change)

### Recommendation
1. Implement synchronizer token pattern (anti-CSRF tokens) for all state-changing requests
2. Set SameSite=Strict on session cookies where possible
3. Validate Origin and Referer headers as defense-in-depth
4. Require re-authentication for sensitive operations (password change, fund transfer)
5. Use custom request headers (X-Requested-With) for AJAX endpoints
```
