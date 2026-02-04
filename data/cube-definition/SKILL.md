---
name: cube-definition
description: Define semantic layer cubes with Drizzle ORM tables, including dimensions, measures, time dimensions, and security context. Use when creating analytics cubes, defining data models, setting up multi-tenant filtering, or working with drizzle-cube semantic layers.
---

# Drizzle Cube Definition

This skill helps you create semantic layer cubes using Drizzle Cube's `defineCube` function. Cubes provide a business-friendly abstraction over database tables with type-safe dimensions, measures, and built-in security.

## Core Concept

A **cube** in Drizzle Cube is:
- A semantic layer over one or more database tables
- Defined using Drizzle ORM table references
- **Always filtered by security context** (mandatory for multi-tenant isolation)
- Type-safe with full TypeScript support

## Basic Cube Structure

```typescript
import { defineCube } from 'drizzle-cube'
import { eq } from 'drizzle-orm'
import { employees } from './schema' // Your Drizzle schema

export const employeesCube = defineCube('Employees', {
  title: 'Employee Analytics', // Optional human-readable title
  description: 'Analytics for employee data', // Optional description

  // MANDATORY: Security context filtering for multi-tenant isolation
  sql: (ctx) => ({
    from: employees,
    where: eq(employees.organisationId, ctx.securityContext.organisationId)
  }),

  // Define dimensions (categorical/time fields for grouping/filtering)
  dimensions: {
    id: {
      title: 'Employee ID',
      type: 'number',
      sql: () => employees.id,
      primaryKey: true // Mark the primary key
    },
    name: {
      title: 'Employee Name',
      type: 'string',
      sql: () => employees.name
    },
    email: {
      title: 'Email Address',
      type: 'string',
      sql: () => employees.email
    },
    departmentId: {
      title: 'Department',
      type: 'number',
      sql: () => employees.departmentId
    },
    isActive: {
      title: 'Active Status',
      type: 'boolean',
      sql: () => employees.isActive
    },
    createdAt: {
      title: 'Created Date',
      type: 'time',
      sql: () => employees.createdAt
    }
  },

  // Define measures (aggregated numeric values)
  measures: {
    count: {
      title: 'Total Employees',
      type: 'count',
      sql: () => employees.id
    },
    totalSalary: {
      title: 'Total Salary',
      type: 'sum',
      sql: () => employees.salary
    },
    avgSalary: {
      title: 'Average Salary',
      type: 'avg',
      sql: () => employees.salary
    },
    minSalary: {
      title: 'Minimum Salary',
      type: 'min',
      sql: () => employees.salary
    },
    maxSalary: {
      title: 'Maximum Salary',
      type: 'max',
      sql: () => employees.salary
    }
  }
})
```

**Important**: The `defineCube` function takes two parameters:
1. **name** (string) - The cube name (e.g., 'Employees')
2. **definition** (object) - The cube configuration (sql, dimensions, measures, etc.)

## Dimension Types

Drizzle Cube supports four dimension types:

### 1. String Dimensions
```typescript
dimensions: {
  name: {
    title: 'Full Name',
    type: 'string',
    sql: () => employees.name
  },
  email: {
    type: 'string',
    sql: () => employees.email
  }
}
```

### 2. Number Dimensions
```typescript
dimensions: {
  id: {
    type: 'number',
    sql: () => employees.id,
    primaryKey: true
  },
  departmentId: {
    type: 'number',
    sql: () => employees.departmentId
  }
}
```

### 3. Time Dimensions
```typescript
dimensions: {
  createdAt: {
    title: 'Created Date',
    type: 'time',
    sql: () => employees.createdAt
  },
  updatedAt: {
    type: 'time',
    sql: () => employees.updatedAt
  }
}
```

### 4. Boolean Dimensions
```typescript
dimensions: {
  isActive: {
    title: 'Active',
    type: 'boolean',
    sql: () => employees.isActive
  },
  isRemote: {
    title: 'Remote Worker',
    type: 'boolean',
    sql: () => employees.isRemote
  }
}
```

## Measure Types

Drizzle Cube supports several aggregation types:

### 1. Count Measures
```typescript
measures: {
  count: {
    title: 'Total Count',
    type: 'count',
    sql: () => employees.id // Column to count
  },
  activeCount: {
    title: 'Active Employees',
    type: 'count',
    sql: () => employees.id,
    filters: [(ctx) => eq(employees.isActive, true)] // Filtered count
  }
}
```

### 2. Count Distinct Measures
```typescript
measures: {
  uniqueDepartments: {
    title: 'Unique Departments',
    type: 'countDistinct',
    sql: () => employees.departmentId
  }
}
```

### 3. Sum Measures
```typescript
measures: {
  totalSalary: {
    title: 'Total Salary',
    type: 'sum',
    sql: () => employees.salary
  }
}
```

### 4. Average Measures
```typescript
measures: {
  avgSalary: {
    title: 'Average Salary',
    type: 'avg',
    sql: () => employees.salary
  }
}
```

### 5. Min/Max Measures
```typescript
measures: {
  minSalary: {
    title: 'Minimum Salary',
    type: 'min',
    sql: () => employees.salary
  },
  maxSalary: {
    title: 'Maximum Salary',
    type: 'max',
    sql: () => employees.salary
  }
}
```

### 6. Calculated Measures
```typescript
measures: {
  salaryPercentage: {
    title: 'Salary as Percentage',
    type: 'calculated',
    calculatedSql: '{totalSalary} / NULLIF({departmentBudget}, 0) * 100'
  }
}
```

## SQL Property Patterns

The `sql` property in dimensions and measures can be defined in two ways:

### 1. Direct Column Reference (Recommended)
```typescript
dimensions: {
  name: {
    type: 'string',
    sql: () => employees.name  // Function returning column
  }
}
```

### 2. Direct Column (Also Valid)
```typescript
dimensions: {
  name: {
    type: 'string',
    sql: employees.name  // Direct column reference
  }
}
```

**Best Practice**: Use the function form `() => employees.column` for consistency and to access the QueryContext if needed.

## Advanced Patterns

### Filtered Measures

Add filters to measures for conditional aggregation:

```typescript
measures: {
  activeEmployees: {
    title: 'Active Employees',
    type: 'count',
    sql: () => employees.id,
    filters: [
      (ctx) => eq(employees.isActive, true)
    ]
  },
  seniorEmployees: {
    title: 'Senior Employees',
    type: 'count',
    sql: () => employees.id,
    filters: [
      (ctx) => {
        const { gte } = ctx.imports
        return gte(employees.yearsOfService, 5)
      }
    ]
  },
  highEarners: {
    title: 'High Earners',
    type: 'count',
    sql: () => employees.id,
    filters: [
      (ctx) => {
        const { gt } = ctx.imports
        return gt(employees.salary, 100000)
      }
    ]
  }
}
```

### Computed Dimensions

Use SQL expressions for computed values:

```typescript
import { sql } from 'drizzle-orm'

dimensions: {
  fullName: {
    title: 'Full Name',
    type: 'string',
    sql: () => sql`${employees.firstName} || ' ' || ${employees.lastName}`
  },
  seniorityLevel: {
    title: 'Seniority',
    type: 'string',
    sql: () => sql`CASE
      WHEN ${employees.yearsOfService} < 2 THEN 'Junior'
      WHEN ${employees.yearsOfService} < 5 THEN 'Mid-level'
      ELSE 'Senior'
    END`
  }
}
```

## Security Context (MANDATORY)

**Every cube MUST filter by security context** to ensure multi-tenant data isolation:

```typescript
// ✅ CORRECT - Security context filtering
sql: (ctx) => ({
  from: employees,
  where: eq(employees.organisationId, ctx.securityContext.organisationId)
})

// ✅ CORRECT - Multiple security conditions
sql: (ctx) => ({
  from: employees,
  where: and(
    eq(employees.organisationId, ctx.securityContext.organisationId),
    eq(employees.tenantId, ctx.securityContext.tenantId)
  )
})

// ❌ WRONG - No security filtering (data leak!)
sql: (ctx) => ({
  from: employees
  // Missing where clause - SECURITY VIOLATION
})
```

**Note**: The `sql` function receives a `QueryContext` object (abbreviated as `ctx`), which contains:
- `ctx.securityContext` - The security context with tenant/organization information
- `ctx.imports` - Drizzle ORM operators and functions

## Complete Example

```typescript
import { defineCube } from 'drizzle-cube'
import { eq, sql, and, gte } from 'drizzle-orm'
import { employees } from './schema'

export const employeesCube = defineCube('Employees', {
  title: 'Employee Analytics',
  description: 'Comprehensive employee data and metrics',

  // Security context filtering (MANDATORY)
  sql: (ctx) => ({
    from: employees,
    where: eq(employees.organisationId, ctx.securityContext.organisationId)
  }),

  dimensions: {
    id: {
      title: 'Employee ID',
      type: 'number',
      sql: () => employees.id,
      primaryKey: true
    },
    name: {
      title: 'Name',
      type: 'string',
      sql: () => employees.name
    },
    email: {
      title: 'Email',
      type: 'string',
      sql: () => employees.email
    },
    department: {
      title: 'Department',
      type: 'string',
      sql: () => employees.departmentName
    },
    isActive: {
      title: 'Active',
      type: 'boolean',
      sql: () => employees.isActive
    },
    createdAt: {
      title: 'Hire Date',
      type: 'time',
      sql: () => employees.createdAt
    },
    // Computed dimension
    seniorityLevel: {
      title: 'Seniority Level',
      type: 'string',
      sql: () => sql`CASE
        WHEN ${employees.yearsOfService} < 2 THEN 'Junior'
        WHEN ${employees.yearsOfService} < 5 THEN 'Mid-level'
        ELSE 'Senior'
      END`
    }
  },

  measures: {
    count: {
      title: 'Total Employees',
      type: 'count',
      sql: () => employees.id
    },
    activeCount: {
      title: 'Active Employees',
      type: 'count',
      sql: () => employees.id,
      filters: [(ctx) => eq(employees.isActive, true)]
    },
    totalSalary: {
      title: 'Total Salary',
      type: 'sum',
      sql: () => employees.salary
    },
    avgSalary: {
      title: 'Average Salary',
      type: 'avg',
      sql: () => employees.salary
    },
    minSalary: {
      title: 'Minimum Salary',
      type: 'min',
      sql: () => employees.salary
    },
    maxSalary: {
      title: 'Maximum Salary',
      type: 'max',
      sql: () => employees.salary
    },
    uniqueDepartments: {
      title: 'Unique Departments',
      type: 'countDistinct',
      sql: () => employees.departmentId
    },
    // Filtered measure
    seniorEmployees: {
      title: 'Senior Employees',
      type: 'count',
      sql: () => employees.id,
      filters: [(ctx) => gte(employees.yearsOfService, 5)]
    }
  }
})
```

## Registering Cubes

Once defined, register cubes with the semantic layer compiler:

```typescript
import { SemanticLayerCompiler } from 'drizzle-cube'
import { drizzle } from 'drizzle-orm/postgres-js'
import { employeesCube } from './cubes/employees'

const db = drizzle(process.env.DATABASE_URL)

const compiler = new SemanticLayerCompiler({
  drizzle: db,
  schema: schema
})

// Register your cube
compiler.registerCube(employeesCube)
```

## Best Practices

1. **Always include security context filtering** - This is mandatory for multi-tenant isolation
2. **Use meaningful names** - Cube names and dimension/measure keys should be clear and descriptive
3. **Add titles** - Provide human-readable titles for UI display
4. **Mark primary keys** - Set `primaryKey: true` on ID dimensions
5. **Type safety** - Use Drizzle ORM table references for compile-time validation
6. **Filtered measures** - Use filters for conditional aggregations instead of creating separate cubes
7. **Use function form for sql** - Prefer `sql: () => column` over direct `sql: column` for consistency

## Common Pitfalls

- **Wrong defineCube signature** - Remember: name is first parameter, NOT inside the object
  ```typescript
  // ❌ WRONG
  defineCube({ name: 'Employees', sql: ... })

  // ✅ CORRECT
  defineCube('Employees', { sql: ... })
  ```
- **Missing security context** - Every cube must filter by security context
- **Wrong SQL syntax** - Use Drizzle ORM operators (eq, and, or), not raw SQL strings
- **Incorrect types** - Ensure dimension/measure types match the actual data types
- **Missing imports** - Import necessary operators from drizzle-orm
- **Redundant name fields** - Don't add `name:` property to dimensions/measures (the key IS the name)

## Next Steps

- Learn about **cube joins** with the `cube-joins` skill
- Build **queries** using your cubes with the `queries` skill
- Set up **server APIs** with the `server-setup` skill
