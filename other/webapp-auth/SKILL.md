---
name: webapp-auth
description: "| | /admin/dashboard | 200 | No | Full admin panel | | /admin/users | 200 | No | User management | | /actuator/env | 200 | No | Environment variables | | /config."
domain: cybersecurity
---

|
| /admin/dashboard | 200 | No | Full admin panel |
| /admin/users | 200 | No | User management |
| /actuator/env | 200 | No | Environment variables |
| /config.php.bak | 200 | No | Database credentials |
| /.git/HEAD | 200 | No | Git repository metadata |

### Impact
- Unauthenticated access to administrative functions
- Ability to create, modify, and delete user accounts
- Exposure of database credentials and API keys
- Full source code disclosure via exposed Git repository

### Recommendation
1. Implement authentication checks at the server/middleware level for all admin routes
2. Remove backup files, debug endpoints, and version control metadata from production
3. Configure web server to deny access to sensitive file extensions (.bak, .old, .env, .git)
4. Implement IP-based access restrictions for administrative interfaces
5. Use a reverse proxy to restrict access to internal-only endpoints
```
