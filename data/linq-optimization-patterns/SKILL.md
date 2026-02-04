---
name: linq-optimization-patterns
description: "Master LINQ and EF Core query optimization including N+1 prevention, eager loading, projections, and performance patterns. Use when: (1) fixing N+1 queries, (2) optimizing slow queries, (3) implementing efficient data access, (4) reducing database load."
layer: 2
tech_stack: [dotnet, csharp, efcore]
topics: [query-optimization, n-plus-one, eager-loading, projections, performance]
depends_on: []
complements: [efcore-patterns]
keywords: [Include, ThenInclude, Select, AsNoTracking, AsSplitQuery, WhereIf, N+1]
---

# LINQ Optimization Patterns

Optimize LINQ queries and EF Core data access for high-performance ABP applications.

## When to Use

- Fixing N+1 query problems
- Optimizing slow repository queries
- Implementing efficient pagination
- Reducing database round trips
- Improving API response times

## N+1 Query Prevention

### Problem: N+1 Queries

```csharp
// BAD: N+1 queries - executes 1 + N queries
public async Task<List<DoctorDto>> GetDoctorsWithAppointmentsAsync()
{
    var doctors = await _doctorRepository.GetListAsync();

    var dtos = new List<DoctorDto>();
    foreach (var doctor in doctors)
    {
        // Each iteration executes a query!
        var appointments = await _appointmentRepository
            .GetListAsync(a => a.DoctorId == doctor.Id);

        dtos.Add(new DoctorDto
        {
            Id = doctor.Id,
            Name = doctor.FullName,
            AppointmentCount = appointments.Count
        });
    }
    return dtos;
}
```

### Solution 1: Eager Loading with Include

```csharp
// GOOD: Single query with Include
public async Task<List<DoctorDto>> GetDoctorsWithAppointmentsAsync()
{
    var query = await _doctorRepository.GetQueryableAsync();

    var doctors = await query
        .Include(d => d.Appointments)
        .ToListAsync();

    return doctors.Select(d => new DoctorDto
    {
        Id = d.Id,
        Name = d.FullName,
        AppointmentCount = d.Appointments.Count
    }).ToList();
}
```

### Solution 2: Projection (Best for DTOs)

```csharp
// BETTER: Project to DTO directly - only selects needed columns
public async Task<List<DoctorDto>> GetDoctorsWithAppointmentsAsync()
{
    var query = await _doctorRepository.GetQueryableAsync();

    return await query
        .Select(d => new DoctorDto
        {
            Id = d.Id,
            Name = d.FullName,
            AppointmentCount = d.Appointments.Count
        })
        .ToListAsync();
}
```

### Solution 3: Batch Loading

```csharp
// GOOD: Two queries instead of N+1
public async Task<List<DoctorDto>> GetDoctorsWithAppointmentsAsync()
{
    var doctors = await _doctorRepository.GetListAsync();
    var doctorIds = doctors.Select(d => d.Id).ToList();

    var appointmentCounts = await (await _appointmentRepository.GetQueryableAsync())
        .Where(a => doctorIds.Contains(a.DoctorId))
        .GroupBy(a => a.DoctorId)
        .Select(g => new { DoctorId = g.Key, Count = g.Count() })
        .ToDictionaryAsync(x => x.DoctorId, x => x.Count);

    return doctors.Select(d => new DoctorDto
    {
        Id = d.Id,
        Name = d.FullName,
        AppointmentCount = appointmentCounts.GetValueOrDefault(d.Id, 0)
    }).ToList();
}
```

## Eager Loading Patterns

### Include and ThenInclude

```csharp
var query = await _appointmentRepository.GetQueryableAsync();

// Single level include
var appointments = await query
    .Include(a => a.Patient)
    .Include(a => a.Doctor)
    .ToListAsync();

// Nested include
var doctors = await (await _doctorRepository.GetQueryableAsync())
    .Include(d => d.Appointments)
        .ThenInclude(a => a.Patient)
    .Include(d => d.Specializations)
        .ThenInclude(s => s.Specialization)
    .ToListAsync();
```

### WithDetails (ABP Extension)

```csharp
// ABP provides WithDetails for common includes
public class DoctorRepository : EfCoreRepository<ClinicDbContext, Doctor, Guid>, IDoctorRepository
{
    public async Task<Doctor> GetWithAppointmentsAsync(Guid id)
    {
        var query = await GetQueryableAsync();

        return await query
            .IncludeDetails() // Uses default includes from repository
            .FirstOrDefaultAsync(d => d.Id == id);
    }

    public override async Task<IQueryable<Doctor>> WithDetailsAsync()
    {
        return (await GetQueryableAsync())
            .Include(d => d.Appointments)
            .Include(d => d.Specializations);
    }
}
```

### Split Queries (Multiple Collections)

```csharp
// Avoid Cartesian explosion with multiple collections
var doctors = await (await _doctorRepository.GetQueryableAsync())
    .Include(d => d.Appointments)
    .Include(d => d.Schedules)
    .Include(d => d.Specializations)
    .AsSplitQuery() // Executes 4 queries instead of 1 with Cartesian product
    .ToListAsync();
```

## AsNoTracking for Read-Only

```csharp
// GOOD: Read-only queries should use AsNoTracking
public async Task<List<PatientDto>> GetPatientsAsync()
{
    var query = await _patientRepository.GetQueryableAsync();

    return await query
        .AsNoTracking() // Skip change tracking - faster
        .Select(p => new PatientDto
        {
            Id = p.Id,
            FullName = $"{p.FirstName} {p.LastName}",
            Email = p.Email
        })
        .ToListAsync();
}

// Note: Projections with Select() are automatically NoTracking
// AsNoTracking is implicit when projecting to non-entity types
```

## Projection Patterns

### Select Only Needed Columns

```csharp
// BAD: Loads entire entity
var patients = await query.ToListAsync();
var emails = patients.Select(p => p.Email);

// GOOD: Only loads Email column from database
var emails = await query
    .Select(p => p.Email)
    .ToListAsync();
```

### Project to DTO

```csharp
// GOOD: Project to DTO in query
public async Task<PagedResultDto<PatientListDto>> GetListAsync(GetPatientListInput input)
{
    var query = await _patientRepository.GetQueryableAsync();

    var totalCount = await query.CountAsync();

    var patients = await query
        .WhereIf(!input.Filter.IsNullOrWhiteSpace(),
            p => p.FirstName.Contains(input.Filter) ||
                 p.LastName.Contains(input.Filter) ||
                 p.Email.Contains(input.Filter))
        .OrderBy(input.Sorting ?? nameof(Patient.LastName))
        .PageBy(input)
        .Select(p => new PatientListDto
        {
            Id = p.Id,
            FullName = $"{p.FirstName} {p.LastName}",
            Email = p.Email,
            DateOfBirth = p.DateOfBirth,
            AppointmentCount = p.Appointments.Count
        })
        .ToListAsync();

    return new PagedResultDto<PatientListDto>(totalCount, patients);
}
```

### Conditional Projection

```csharp
// Include related data only when needed
public async Task<PatientDto> GetAsync(Guid id, bool includeAppointments = false)
{
    var query = await _patientRepository.GetQueryableAsync();

    if (includeAppointments)
    {
        return await query
            .Where(p => p.Id == id)
            .Select(p => new PatientDto
            {
                Id = p.Id,
                FullName = $"{p.FirstName} {p.LastName}",
                Appointments = p.Appointments.Select(a => new AppointmentDto
                {
                    Id = a.Id,
                    Date = a.AppointmentDate,
                    Status = a.Status
                }).ToList()
            })
            .FirstOrDefaultAsync();
    }

    return await query
        .Where(p => p.Id == id)
        .Select(p => new PatientDto
        {
            Id = p.Id,
            FullName = $"{p.FirstName} {p.LastName}"
        })
        .FirstOrDefaultAsync();
}
```

## Efficient Pagination

### Cursor-Based Pagination (Best for Large Data)

```csharp
// Better than Skip/Take for large datasets
public async Task<List<PatientDto>> GetPatientsAfterAsync(
    DateTime? lastCreatedAt,
    Guid? lastId,
    int take = 20)
{
    var query = await _patientRepository.GetQueryableAsync();

    if (lastCreatedAt.HasValue && lastId.HasValue)
    {
        query = query.Where(p =>
            p.CreationTime < lastCreatedAt.Value ||
            (p.CreationTime == lastCreatedAt.Value && p.Id.CompareTo(lastId.Value) < 0));
    }

    return await query
        .OrderByDescending(p => p.CreationTime)
        .ThenByDescending(p => p.Id)
        .Take(take)
        .Select(p => new PatientDto { /* ... */ })
        .ToListAsync();
}
```

### Offset Pagination with Count Optimization

```csharp
// Only count when needed (first page or explicitly requested)
public async Task<PagedResultDto<PatientDto>> GetListAsync(
    GetPatientListInput input,
    bool includeCount = true)
{
    var query = await _patientRepository.GetQueryableAsync();
    query = ApplyFilters(query, input);

    long totalCount = 0;
    if (includeCount)
    {
        totalCount = await query.LongCountAsync();
    }

    var patients = await query
        .OrderBy(input.Sorting ?? "LastName")
        .PageBy(input)
        .Select(p => new PatientDto { /* ... */ })
        .ToListAsync();

    return new PagedResultDto<PatientDto>(totalCount, patients);
}
```

## Filtering Patterns

### ABP WhereIf Extension

```csharp
public async Task<List<AppointmentDto>> GetListAsync(GetAppointmentListInput input)
{
    var query = await _appointmentRepository.GetQueryableAsync();

    return await query
        .WhereIf(input.DoctorId.HasValue, a => a.DoctorId == input.DoctorId)
        .WhereIf(input.PatientId.HasValue, a => a.PatientId == input.PatientId)
        .WhereIf(input.Status.HasValue, a => a.Status == input.Status)
        .WhereIf(input.FromDate.HasValue, a => a.AppointmentDate >= input.FromDate)
        .WhereIf(input.ToDate.HasValue, a => a.AppointmentDate <= input.ToDate)
        .WhereIf(!input.Filter.IsNullOrWhiteSpace(),
            a => a.Patient.FirstName.Contains(input.Filter) ||
                 a.Patient.LastName.Contains(input.Filter))
        .OrderByDescending(a => a.AppointmentDate)
        .Select(a => new AppointmentDto { /* ... */ })
        .ToListAsync();
}
```

### Search with Full-Text (PostgreSQL)

```csharp
// Use EF.Functions for database-specific operations
var patients = await query
    .Where(p => EF.Functions.ILike(p.FirstName, $"%{searchTerm}%") ||
                EF.Functions.ILike(p.LastName, $"%{searchTerm}%"))
    .ToListAsync();
```

## Aggregation Patterns

### Efficient Counting

```csharp
// BAD: Loads all entities to count
var count = (await _patientRepository.GetListAsync()).Count;

// GOOD: Count at database level
var query = await _patientRepository.GetQueryableAsync();
var count = await query.CountAsync();

// GOOD: Count with filter
var activeCount = await query
    .Where(p => p.Status == PatientStatus.Active)
    .CountAsync();
```

### Grouped Aggregations

```csharp
// Get appointment counts by status
var query = await _appointmentRepository.GetQueryableAsync();

var statusCounts = await query
    .GroupBy(a => a.Status)
    .Select(g => new
    {
        Status = g.Key,
        Count = g.Count()
    })
    .ToDictionaryAsync(x => x.Status, x => x.Count);
```

### Existence Checks

```csharp
// BAD: Loads entity to check existence
var patient = await _patientRepository.FirstOrDefaultAsync(p => p.Email == email);
var exists = patient != null;

// GOOD: Use Any() - stops at first match
var query = await _patientRepository.GetQueryableAsync();
var exists = await query.AnyAsync(p => p.Email == email);
```

## Raw SQL (When Necessary)

```csharp
// For complex queries that can't be expressed in LINQ
public async Task<List<DoctorAvailabilityDto>> GetDoctorAvailabilityAsync(DateTime date)
{
    var context = await _dbContextProvider.GetDbContextAsync();

    return await context.Database
        .SqlQuery<DoctorAvailabilityDto>($@"
            SELECT d.Id, d.FullName, COUNT(a.Id) as AppointmentCount
            FROM Doctors d
            LEFT JOIN Appointments a ON d.Id = a.DoctorId
                AND a.AppointmentDate::date = {date:yyyy-MM-dd}
                AND a.IsDeleted = false
            WHERE d.IsDeleted = false
            GROUP BY d.Id, d.FullName
            ORDER BY AppointmentCount ASC")
        .ToListAsync();
}
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| N+1 queries | Multiple round trips | Use Include or projection |
| `ToList()` then `Where()` | Loads all data to memory | Filter in query |
| `Select *` equivalent | Loads unnecessary columns | Project to DTO |
| Tracking read-only data | Overhead for change tracking | Use AsNoTracking |
| Large OFFSET pagination | Slow for large offsets | Use cursor-based pagination |
| `Count()` after `ToList()` | Loads all data | Use `CountAsync()` |
| Multiple `SaveChangesAsync()` | Multiple transactions | Batch changes |
| **`Count()` after pagination** | Double query execution | Count BEFORE `ToListAsync()` |
| **`GetListAsync()` for validation** | Loads entire table | Use filtered `AnyAsync()` or `GetQueryableAsync()` |
| **In-memory joins for bulk ops** | Memory explosion | Use `IQueryable` joins, filter server-side |

### Critical: Count After Pagination (Double Query)

```csharp
// ❌ BAD: Executes query TWICE (one for data, one for count)
var dtos = await AsyncExecuter.ToListAsync(
    queryable
    .OrderBy(input.Sorting)
    .Skip(input.SkipCount)
    .Take(input.MaxResultCount)
);
var totalCount = queryable.Count(); // Second execution on same queryable!

// ✅ GOOD: Count FIRST, then paginate
var totalCount = await AsyncExecuter.CountAsync(queryable);
var dtos = await AsyncExecuter.ToListAsync(
    queryable
    .OrderBy(input.Sorting)
    .Skip(input.SkipCount)
    .Take(input.MaxResultCount)
);
```

### Critical: Loading Full Tables for Validation

```csharp
// ❌ BAD: Loads ALL records to memory for validation
var _projects = await _projectRepository.GetListAsync();
var _customers = await _customerRepository.GetListAsync();
var _licensePlates = await _licensePlateRepository.GetListAsync();

// Then validates with in-memory LINQ
foreach (var item in input)
{
    var project = _projects.FirstOrDefault(p => p.Code == item.ProjectCode);
    // ...
}

// ✅ GOOD: Only load what you need based on input
var projectCodes = input.Select(x => x.ProjectCode).Distinct().ToList();
var customerNames = input.Select(x => x.CustomerName).Distinct().ToList();

var projects = await (await _projectRepository.GetQueryableAsync())
    .Where(p => projectCodes.Contains(p.ProjectCode))
    .ToDictionaryAsync(p => p.ProjectCode, p => p);

var customers = await (await _customerRepository.GetQueryableAsync())
    .Where(c => customerNames.Contains(c.CustomerName))
    .ToDictionaryAsync(c => c.CustomerName, c => c);

// Validate using dictionaries (O(1) lookup)
foreach (var item in input)
{
    if (!projects.TryGetValue(item.ProjectCode, out var project))
    {
        validations.Add($"Invalid project code: {item.ProjectCode}");
    }
}
```

## Performance Checklist

- [ ] No N+1 queries (check with logging)
- [ ] Projections used for DTOs
- [ ] AsNoTracking for read-only queries
- [ ] Appropriate indexes exist for filters
- [ ] Pagination uses cursor or optimized offset
- [ ] Counts done at database level
- [ ] Include only loads needed relations
- [ ] Split queries for multiple collections

## Debugging Queries

```csharp
// Enable EF Core logging in appsettings.Development.json
{
  "Logging": {
    "LogLevel": {
      "Microsoft.EntityFrameworkCore.Database.Command": "Information"
    }
  }
}

// Or use ToQueryString() to see generated SQL
var query = await _patientRepository.GetQueryableAsync();
var sql = query
    .Where(p => p.Status == PatientStatus.Active)
    .ToQueryString();

_logger.LogInformation("Generated SQL: {Sql}", sql);
```

## Integration Points

This skill is used by:
- **abp-developer**: Efficient data access implementation
- **abp-code-reviewer**: Query performance validation
- **debugger**: Performance issue diagnosis
