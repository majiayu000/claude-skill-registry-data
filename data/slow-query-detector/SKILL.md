---
name: slow-query-detector
description: Detect slow queries and performance issues in Entity Framework Core codebases. Use when analyzing database performance, finding N+1 queries, identifying missing indexes, reviewing repository patterns, or optimizing EF Core queries. Triggers on requests like "find slow queries", "check for N+1 problems", "analyze database performance", "review query performance", or "optimize EF Core queries".
---

# Slow Query Detector

Analyze EF Core codebases to detect slow queries and performance anti-patterns.

## Quick Start

1. Run the analysis script to scan for common issues:
   ```bash
   python3 .claude/skills/slow-query-detector/scripts/analyze_efcore.py src
   ```

2. Review detected issues by severity (Critical > Warning > Info)

3. For each issue, check the suggested fix in [references/patterns.md](references/patterns.md)

## Detection Workflow

### Step 1: Automated Scan

Run the analysis script on the repository:

```bash
python3 .claude/skills/slow-query-detector/scripts/analyze_efcore.py src
```

The script detects:
- N+1 query patterns (loops with await queries)
- ToListAsync followed by in-memory operations
- Missing AsNoTracking on read-only queries
- Unbounded queries (no Take/Skip)

### Step 2: Manual Review

After automated scan, manually check:

1. **Query Handlers** - Search for `QueryHandler.cs` files and review foreach loops
2. **Repository Methods** - Check for methods that load all records
3. **Include Chains** - Look for missing `.Include()` calls

Use grep patterns:
```bash
# Find foreach with await inside
grep -rn "foreach.*await" --include="*.cs"

# Find ToListAsync followed by LINQ
grep -rn "ToListAsync.*\." --include="*.cs"

# Find queries without AsNoTracking
grep -rn "await.*context\." --include="*.cs" | grep -v "AsNoTracking"
```

### Step 3: Validate with EF Core Logging

Enable query logging in development to capture actual SQL:

```csharp
// In Program.cs or DbContext configuration
optionsBuilder
    .UseNpgsql(connectionString)
    .LogTo(Console.WriteLine, LogLevel.Information)
    .EnableSensitiveDataLogging();
```

## Common Patterns & Fixes

See [references/patterns.md](references/patterns.md) for detailed patterns including:
- N+1 Query Problem (Critical)
- Memory-based Aggregation (Critical)
- Missing Index Hints (Warning)
- Unbounded Result Sets (Warning)

## Project-Specific Checks

For this university management system:

### Known Issue Locations

1. **GetStudentEnrollmentsQueryHandler** - N+1 problem fetching course offerings per enrollment
2. **SelectCourseOfferingsBySemesterQueryHandler** - N+1 problem fetching courses per offering
3. **CourseOfferingRepository.GetNextOfferingIdAsync** - Loads all records for Max calculation
4. **ClassSessionRepository.GetNextSessionIdAsync** - Loads all records for Max calculation

### Repository Pattern Review

Check all `*Repository.cs` files in:
- `src/StudentRegistrations/Infrastructure/Persistence/Repositories/`
- `src/Enrollments/Infrastructure/Persistence/Repositories/`
- `src/Attendance/Infrastructure/Persistence/Repositories/`

### Index Verification

Review index definitions in:
- `src/*/Infrastructure/Persistence/Configurations/*Configuration.cs`
- `src/*/Infrastructure/Persistence/Migrations/*.sql`

## Resources

### scripts/
- `analyze_efcore.py` - Automated scanner for EF Core anti-patterns

### references/
- `patterns.md` - Detailed slow query patterns with examples and fixes
