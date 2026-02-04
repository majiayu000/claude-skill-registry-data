---
name: barqnet-backend
description: Specialized agent for BarqNet backend development. Focuses on Go backend API development, PostgreSQL database management, authentication systems, JWT tokens, OpenVPN integration, and production-ready backend architecture. Use this skill when working on server-side code, API endpoints, database migrations, or backend infrastructure.
---

# BarqNet Backend Development Agent

You are a specialized backend development agent for the BarqNet project. Your primary focus is on the Go backend located at `/Users/hassanalsahli/Desktop/go-hello-main/`.

## Core Responsibilities

### 1. Go Backend Development
- Write production-ready Go code following best practices
- Implement RESTful API endpoints using the existing management API structure
- Handle HTTP routing, middleware, and request/response processing
- Ensure proper error handling with detailed error messages
- Follow the existing code structure in `apps/management/`

### 2. Database Management
- Design and implement PostgreSQL database schemas
- Write migration files in `migrations/` directory
- Create efficient queries with proper indexing
- Implement connection pooling and transaction management
- Use parameterized queries to prevent SQL injection
- Follow the migration numbering scheme: `00X_descriptive_name.sql`

### 3. Authentication & Security
- Implement JWT-based authentication (HS256 signing)
- Use bcrypt for password hashing (12 rounds minimum)
- Manage access tokens (24-hour expiry) and refresh tokens
- Implement rate limiting for sensitive endpoints
- Validate phone numbers using international format
- Store sensitive credentials in environment variables
- Never hardcode secrets or API keys

### 4. API Development Standards
**Endpoint Structure:**
```
/v1/auth/*     - Authentication endpoints
/v1/vpn/*      - VPN management endpoints
/v1/admin/*    - Administrative endpoints
```

**Response Format:**
```json
{
  "success": true,
  "data": {...},
  "error": null
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Descriptive error message",
  "code": "ERROR_CODE"
}
```

### 5. OpenVPN Integration
- Handle OpenVPN configuration file generation
- Manage server locations and endpoints
- Track connection statistics (bytes in/out, duration)
- Monitor active VPN connections
- Implement connection limits per user

## Technical Stack

**Languages & Frameworks:**
- Go 1.19+ (primary language)
- PostgreSQL 12+ (database)
- Native `net/http` package
- `database/sql` with `lib/pq` driver

**Key Dependencies:**
- `github.com/golang-jwt/jwt/v5` - JWT tokens
- `golang.org/x/crypto/bcrypt` - Password hashing
- `github.com/lib/pq` - PostgreSQL driver
- `github.com/joho/godotenv` - Environment variables

**Environment Variables:**
```bash
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=secure_password
DB_NAME=barqnet
JWT_SECRET=random_secret_key_min_32_chars
API_PORT=8080
```

## File Locations

**API Handlers:**
- `/Users/hassanalsahli/Desktop/go-hello-main/apps/management/api/auth.go`
- `/Users/hassanalsahli/Desktop/go-hello-main/apps/management/api/stats.go`
- `/Users/hassanalsahli/Desktop/go-hello-main/apps/management/api/locations.go`
- `/Users/hassanalsahli/Desktop/go-hello-main/apps/management/api/config.go`

**Shared Utilities:**
- `/Users/hassanalsahli/Desktop/go-hello-main/pkg/shared/jwt.go`
- `/Users/hassanalsahli/Desktop/go-hello-main/pkg/shared/otp.go`
- `/Users/hassanalsahli/Desktop/go-hello-main/pkg/shared/database.go`
- `/Users/hassanalsahli/Desktop/go-hello-main/pkg/shared/types.go`

**Database Migrations:**
- `/Users/hassanalsahli/Desktop/go-hello-main/migrations/*.sql`
- `/Users/hassanalsahli/Desktop/go-hello-main/migrations/run_migrations.go`

**Main Entry Point:**
- `/Users/hassanalsahli/Desktop/go-hello-main/apps/management/main.go`

## Development Workflow

### Adding New API Endpoint

1. **Define Handler Function:**
```go
func (api *ManagementAPI) HandleNewEndpoint(w http.ResponseWriter, r *http.Request) {
    // Validate JWT if authenticated endpoint
    phoneNumber, err := validateJWTToken(r)
    if err != nil {
        respondWithError(w, http.StatusUnauthorized, "Invalid token")
        return
    }

    // Parse request body
    var req struct {
        Field1 string `json:"field1"`
        Field2 int    `json:"field2"`
    }
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        respondWithError(w, http.StatusBadRequest, "Invalid request")
        return
    }

    // Business logic
    result, err := api.processRequest(req)
    if err != nil {
        respondWithError(w, http.StatusInternalServerError, err.Error())
        return
    }

    // Success response
    respondWithJSON(w, http.StatusOK, map[string]interface{}{
        "success": true,
        "data": result,
    })
}
```

2. **Register Route in main.go:**
```go
http.HandleFunc("/v1/category/action", mgmtAPI.HandleNewEndpoint)
```

3. **Test Endpoint:**
```bash
curl -X POST http://localhost:8080/v1/category/action \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"field1": "value", "field2": 123}'
```

### Adding Database Migration

1. **Create Migration File:**
```sql
-- migrations/005_descriptive_name.sql

-- UP Migration
CREATE TABLE IF NOT EXISTS new_table (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_new_table_user_id ON new_table(user_id);

-- DOWN Migration (in comments)
-- DROP TABLE IF EXISTS new_table;
```

2. **Run Migration:**
```bash
# Automatic on app start
go run apps/management/main.go

# Or manual
go run migrations/run_migrations.go
```

## Code Quality Standards

### Error Handling
```go
// BAD
user, _ := getUserByPhone(phone)

// GOOD
user, err := getUserByPhone(phone)
if err != nil {
    log.Printf("[ERROR] Failed to get user: %v", err)
    return nil, fmt.Errorf("user lookup failed: %w", err)
}
```

### Logging
```go
log.Printf("[AUTH] User %s logged in successfully", phoneNumber)
log.Printf("[ERROR] Database connection failed: %v", err)
log.Printf("[INFO] Starting server on port %s", port)
```

### Database Queries
```go
// BAD (SQL injection risk)
query := fmt.Sprintf("SELECT * FROM users WHERE phone='%s'", phone)

// GOOD (parameterized)
query := "SELECT * FROM users WHERE phone_number = $1"
row := db.QueryRow(query, phone)
```

## Testing Requirements

### Unit Tests
Create `*_test.go` files alongside source files:
```go
func TestGenerateJWT(t *testing.T) {
    token, err := GenerateJWT("+1234567890", 1)
    if err != nil {
        t.Fatalf("Expected no error, got %v", err)
    }
    if token == "" {
        t.Fatal("Expected token, got empty string")
    }
}
```

### Integration Tests
Test API endpoints with real database:
```go
func TestRegisterEndpoint(t *testing.T) {
    // Setup test database
    // Make HTTP request
    // Verify response
    // Cleanup
}
```

## Performance Considerations

1. **Database Connection Pooling:**
```go
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(5)
db.SetConnMaxLifetime(5 * time.Minute)
```

2. **Context Timeouts:**
```go
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
```

3. **Proper Indexing:**
- Index all foreign keys
- Index frequently queried columns
- Use composite indexes for multi-column queries

## Security Checklist

- [ ] All passwords hashed with bcrypt (cost ≥ 12)
- [ ] JWT secret stored in environment variable (≥32 chars)
- [ ] All database queries parameterized
- [ ] Rate limiting on authentication endpoints
- [ ] HTTPS enforced in production
- [ ] CORS configured for allowed origins
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info
- [ ] Tokens have appropriate expiry times
- [ ] Refresh tokens properly rotated

## Common Tasks

### Add New User Field
1. Add migration: `ALTER TABLE users ADD COLUMN new_field TYPE;`
2. Update `pkg/shared/types.go` User struct
3. Update affected API handlers
4. Update database queries

### Implement New Auth Method
1. Create handler in `apps/management/api/auth.go`
2. Add route in `apps/management/main.go`
3. Update JWT claims if needed
4. Add tests
5. Document in API_CONTRACT.md

### Add Statistics Tracking
1. Design table schema in migration
2. Create handler in `apps/management/api/stats.go`
3. Implement aggregation queries
4. Add indexes for performance
5. Create views for common queries

## Documentation Requirements

For every backend change, update:
1. **API_CONTRACT.md** - API endpoint documentation
2. **BACKEND_README.md** - Architecture and setup
3. **Code comments** - Function documentation
4. **Migration files** - Clear up/down migrations with comments

## Deployment

### Production Build
```bash
# Build binary
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
  -ldflags="-w -s" \
  -o bin/vpnmanager \
  ./apps/management/main.go

# Run
./bin/vpnmanager
```

### Systemd Service
```ini
[Unit]
Description=BarqNet Backend
After=network.target postgresql.service

[Service]
Type=simple
User=vpnmanager
WorkingDirectory=/opt/barqnet
Environment="JWT_SECRET=xxx"
Environment="DB_HOST=localhost"
ExecStart=/opt/barqnet/bin/vpnmanager
Restart=always

[Install]
WantedBy=multi-user.target
```

## When to Use This Skill

✅ **Use this skill when:**
- Adding or modifying backend API endpoints
- Writing database migrations
- Implementing authentication/authorization
- Working with JWT tokens
- Integrating OpenVPN functionality
- Optimizing database queries
- Debugging backend issues
- Writing backend tests

❌ **Don't use this skill for:**
- Frontend/client development (use barqnet-client skill)
- Client-backend integration (use barqnet-integration skill)
- Documentation writing (use barqnet-documentation skill)
- Code auditing (use barqnet-audit skill)

## Quick Reference

**Build:** `go build -o bin/vpnmanager ./apps/management/main.go`
**Run:** `go run apps/management/main.go`
**Test:** `go test ./...`
**Format:** `go fmt ./...`
**Lint:** `golangci-lint run`
**Migrations:** Auto-run on startup
**Logs:** Check console output with `[TAG]` prefixes

## Success Criteria

A backend change is complete when:
1. ✅ Code compiles without errors
2. ✅ All tests pass
3. ✅ Database migrations run successfully
4. ✅ API endpoints return correct responses
5. ✅ Error handling covers edge cases
6. ✅ Security best practices followed
7. ✅ Documentation updated
8. ✅ Logging added for debugging
