---
name: cube-joins
description: Configure cube relationships and joins in drizzle-cube, including belongsTo, hasOne, hasMany, and belongsToMany relationships. Use when connecting cubes, setting up relationships, creating many-to-many joins, or working with multi-cube queries in drizzle-cube.
---

# Drizzle Cube Joins

This skill helps you configure relationships between cubes using Drizzle Cube's join system. Joins enable cross-cube queries and automatic relationship handling.

## Core Concept

Cubes can define relationships to other cubes using the `joins` property. Drizzle Cube supports four relationship types:

- **`belongsTo`** - Many-to-one (INNER JOIN) - e.g., Employee → Department
- **`hasOne`** - One-to-one (LEFT JOIN) - e.g., User → Profile
- **`hasMany`** - One-to-many with pre-aggregation (LEFT JOIN) - e.g., Department → Employees
- **`belongsToMany`** - Many-to-many through junction table (LEFT JOIN) - e.g., Employee ↔ Department via TimeEntries

## Basic Join Structure

```typescript
import { defineCube } from 'drizzle-cube'
import { eq } from 'drizzle-orm'

export const employeesCube = defineCube({
  name: 'Employees',

  sql: (ctx) => ({
    from: employees,
    where: eq(employees.organisationId, ctx.securityContext.organisationId)
  }),

  // Define relationships to other cubes
  joins: {
    Departments: {
      targetCube: () => departmentsCube, // Lazy reference to avoid circular deps
      relationship: 'belongsTo',
      on: [
        { source: employees.departmentId, target: departments.id }
      ]
    }
  },

  dimensions: { /* ... */ },
  measures: { /* ... */ }
})
```

## Relationship Types

### 1. belongsTo (Many-to-One)

Use when many records of this cube relate to one record in the target cube.

**Example: Employee belongs to Department**

```typescript
export const employeesCube = defineCube({
  name: 'Employees',

  sql: (ctx) => ({
    from: employees,
    where: eq(employees.organisationId, ctx.securityContext.organisationId)
  }),

  joins: {
    Departments: {
      targetCube: () => departmentsCube,
      relationship: 'belongsTo', // Many employees → one department
      on: [
        { source: employees.departmentId, target: departments.id }
      ]
    }
  },

  dimensions: {
    id: { name: 'id', type: 'number', sql: employees.id, primaryKey: true },
    name: { name: 'name', type: 'string', sql: employees.name },
    departmentId: { name: 'departmentId', type: 'number', sql: employees.departmentId }
  },

  measures: {
    count: { name: 'count', type: 'count', sql: employees.id }
  }
})

// Query across the relationship
const result = await semanticLayer.execute({
  measures: ['Employees.count'],
  dimensions: ['Departments.name'] // Access department name through join
}, securityContext)
```

### 2. hasOne (One-to-One)

Use when one record of this cube relates to exactly one record in the target cube.

**Example: User has one Profile**

```typescript
export const usersCube = defineCube({
  name: 'Users',

  sql: (ctx) => ({
    from: users,
    where: eq(users.organisationId, ctx.securityContext.organisationId)
  }),

  joins: {
    Profiles: {
      targetCube: () => profilesCube,
      relationship: 'hasOne', // One user → one profile
      on: [
        { source: users.id, target: profiles.userId }
      ]
    }
  },

  dimensions: {
    id: { name: 'id', type: 'number', sql: users.id, primaryKey: true },
    email: { name: 'email', type: 'string', sql: users.email }
  },

  measures: {
    count: { name: 'count', type: 'count', sql: users.id }
  }
})
```

### 3. hasMany (One-to-Many)

Use when one record of this cube relates to multiple records in the target cube.

**Example: Department has many Employees**

```typescript
export const departmentsCube = defineCube({
  name: 'Departments',

  sql: (ctx) => ({
    from: departments,
    where: eq(departments.organisationId, ctx.securityContext.organisationId)
  }),

  joins: {
    Employees: {
      targetCube: () => employeesCube,
      relationship: 'hasMany', // One department → many employees
      on: [
        { source: departments.id, target: employees.departmentId }
      ]
    }
  },

  dimensions: {
    id: { name: 'id', type: 'number', sql: departments.id, primaryKey: true },
    name: { name: 'name', type: 'string', sql: departments.name }
  },

  measures: {
    count: { name: 'count', type: 'count', sql: departments.id }
  }
})

// Query aggregates across hasMany relationships
const result = await semanticLayer.execute({
  measures: ['Departments.count', 'Employees.count'], // Automatic pre-aggregation
  dimensions: ['Departments.name']
}, securityContext)
```

### 4. belongsToMany (Many-to-Many)

Use when records can relate to multiple records on both sides through a junction table.

**Example: Employee works in many Departments (via TimeEntries)**

```typescript
export const employeesCube = defineCube({
  name: 'Employees',

  sql: (ctx) => ({
    from: employees,
    where: eq(employees.organisationId, ctx.securityContext.organisationId)
  }),

  joins: {
    DepartmentsViaTimeEntries: {
      targetCube: () => departmentsCube,
      relationship: 'belongsToMany', // Many-to-many relationship
      on: [], // IGNORED for belongsToMany - use 'through' configuration instead
      through: {
        table: timeEntries, // Junction table
        sourceKey: [
          { source: employees.id, target: timeEntries.employeeId }
        ],
        targetKey: [
          { source: timeEntries.departmentId, target: departments.id }
        ],
        // Optional: Security context for junction table
        securitySql: (securityContext) =>
          eq(timeEntries.organisationId, securityContext.organisationId)
      }
    }
  },

  dimensions: {
    id: { name: 'id', type: 'number', sql: employees.id, primaryKey: true },
    name: { name: 'name', type: 'string', sql: employees.name }
  },

  measures: {
    count: { name: 'count', type: 'count', sql: employees.id }
  }
})

// Query across many-to-many relationship
const result = await semanticLayer.execute({
  measures: ['Employees.count'],
  dimensions: ['Departments.name'] // Uses the many-to-many join automatically
}, securityContext)
```

## When to Use Each Relationship Type

### belongsTo vs hasMany

**Use belongsTo when:**
- The foreign key is in THIS cube's table
- Many records here → one record there
- Example: Employee.departmentId → Department.id

**Use hasMany when:**
- The foreign key is in the TARGET cube's table
- One record here → many records there
- Example: Department.id ← Employee.departmentId

### belongsToMany vs hasMany

**Use belongsToMany when:**
- Both sides can have multiple related records
- A junction table connects the two cubes
- Example: Employee ↔ Department (via TimeEntries)

**Use hasMany when:**
- Only one side has multiple related records
- Direct foreign key relationship
- Example: Department → Employees (one department, many employees)

## Multi-Column Joins

Joins can use multiple columns for composite keys:

```typescript
joins: {
  RelatedCube: {
    targetCube: () => relatedCube,
    relationship: 'belongsTo',
    on: [
      { source: table.orgId, target: relatedTable.orgId },
      { source: table.deptId, target: relatedTable.deptId }
    ]
  }
}
```

## Complete Example: Multi-Cube System

```typescript
import { defineCube } from 'drizzle-cube'
import { eq } from 'drizzle-orm'
import { employees, departments, timeEntries, projects } from './schema'

// Department Cube
export const departmentsCube = defineCube({
  name: 'Departments',

  sql: (ctx) => ({
    from: departments,
    where: eq(departments.organisationId, ctx.securityContext.organisationId)
  }),

  joins: {
    Employees: {
      targetCube: () => employeesCube,
      relationship: 'hasMany',
      on: [{ source: departments.id, target: employees.departmentId }]
    }
  },

  dimensions: {
    id: { name: 'id', type: 'number', sql: departments.id, primaryKey: true },
    name: { name: 'name', type: 'string', sql: departments.name }
  },

  measures: {
    count: { name: 'count', type: 'count', sql: departments.id },
    totalBudget: { name: 'totalBudget', type: 'sum', sql: departments.budget }
  }
})

// Employee Cube
export const employeesCube = defineCube({
  name: 'Employees',

  sql: (ctx) => ({
    from: employees,
    where: eq(employees.organisationId, ctx.securityContext.organisationId)
  }),

  joins: {
    // Many-to-one: Employee belongs to Department
    Departments: {
      targetCube: () => departmentsCube,
      relationship: 'belongsTo',
      on: [{ source: employees.departmentId, target: departments.id }]
    },
    // Many-to-many: Employee works on many Projects
    Projects: {
      targetCube: () => projectsCube,
      relationship: 'belongsToMany',
      on: [],
      through: {
        table: timeEntries,
        sourceKey: [{ source: employees.id, target: timeEntries.employeeId }],
        targetKey: [{ source: timeEntries.projectId, target: projects.id }],
        securitySql: (ctx) => eq(timeEntries.organisationId, ctx.organisationId)
      }
    }
  },

  dimensions: {
    id: { name: 'id', type: 'number', sql: employees.id, primaryKey: true },
    name: { name: 'name', type: 'string', sql: employees.name },
    email: { name: 'email', type: 'string', sql: employees.email }
  },

  measures: {
    count: { name: 'count', type: 'count', sql: employees.id },
    avgSalary: { name: 'avgSalary', type: 'avg', sql: employees.salary }
  }
})

// Project Cube
export const projectsCube = defineCube({
  name: 'Projects',

  sql: (ctx) => ({
    from: projects,
    where: eq(projects.organisationId, ctx.securityContext.organisationId)
  }),

  joins: {
    Employees: {
      targetCube: () => employeesCube,
      relationship: 'belongsToMany',
      on: [],
      through: {
        table: timeEntries,
        sourceKey: [{ source: projects.id, target: timeEntries.projectId }],
        targetKey: [{ source: timeEntries.employeeId, target: employees.id }],
        securitySql: (ctx) => eq(timeEntries.organisationId, ctx.organisationId)
      }
    }
  },

  dimensions: {
    id: { name: 'id', type: 'number', sql: projects.id, primaryKey: true },
    name: { name: 'name', type: 'string', sql: projects.name },
    status: { name: 'status', type: 'string', sql: projects.status }
  },

  measures: {
    count: { name: 'count', type: 'count', sql: projects.id }
  }
})
```

## Querying Across Joins

Once joins are defined, you can query across cubes seamlessly:

```typescript
// Query employee count by department name
const result1 = await semanticLayer.execute({
  measures: ['Employees.count'],
  dimensions: ['Departments.name'] // Automatic JOIN
}, securityContext)

// Query across many-to-many
const result2 = await semanticLayer.execute({
  measures: ['Employees.count', 'Projects.count'],
  dimensions: ['Projects.name'] // Automatic many-to-many JOIN
}, securityContext)

// Multi-level joins
const result3 = await semanticLayer.execute({
  measures: ['Employees.count'],
  dimensions: ['Departments.name', 'Projects.name'] // Multiple JOINs
}, securityContext)
```

## Security Context in Joins

**Security context is automatically applied to:**
- All base tables in the query
- All JOIN conditions
- All junction tables in belongsToMany relationships

```typescript
// Security context in belongsToMany
through: {
  table: timeEntries,
  sourceKey: [{ source: employees.id, target: timeEntries.employeeId }],
  targetKey: [{ source: timeEntries.departmentId, target: departments.id }],
  // This ensures junction table is also filtered by security context
  securitySql: (securityContext) =>
    eq(timeEntries.organisationId, securityContext.organisationId)
}
```

## Performance Considerations

### Junction Tables (belongsToMany)

- Add indexes on both foreign key columns
- Consider composite indexes on (sourceKey, targetKey)
- Ensure junction table has security context filtering
- Monitor query performance on large datasets

### Join Optimization

- Use `belongsTo` instead of `hasMany` when possible (more efficient)
- Limit dimensions from joined cubes in large queries
- Add appropriate database indexes on foreign keys

## Best Practices

1. **Use lazy references** - `targetCube: () => cube` prevents circular dependencies
2. **Name joins semantically** - Use descriptive names like "Departments" not "dept_join"
3. **Security on junction tables** - Always add `securitySql` to belongsToMany relationships
4. **Index foreign keys** - Ensure database has indexes on join columns
5. **Test multi-cube queries** - Validate security isolation across joins

## Common Pitfalls

- **Circular dependencies** - Always use lazy references `() => cube`
- **Missing security context** - Junction tables need security filtering too
- **Wrong relationship type** - belongsTo vs hasMany depends on where the foreign key is
- **Missing indexes** - Joins without indexes cause performance issues

## Next Steps

- Build **queries** across joined cubes with the `queries` skill
- Create **dashboards** showing multi-cube data with the `dashboard` skill
- Learn about **cube definitions** with the `cube-definition` skill
