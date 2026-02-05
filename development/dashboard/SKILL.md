---
name: dashboard
description: Create interactive analytics dashboards with React components from drizzle-cube/client. Use when building dashboards, configuring portlets, setting up grid layouts, or creating analytics UIs with drizzle-cube React components.
---

# Drizzle Cube Dashboard

This skill helps you create interactive analytics dashboards using Drizzle Cube's React components. Build complete dashboards with charts, KPIs, and data tables in a responsive grid layout.

## Core Concept

A Drizzle Cube dashboard consists of:
- **CubeProvider** - Context provider for API connection
- **AnalyticsDashboard** - Main dashboard container
- **Portlets** - Individual widgets (charts, KPIs, tables)
- **Grid Layout** - Responsive positioning system

## Installation

```bash
npm install drizzle-cube react react-dom
```

## Basic Dashboard Setup

### 1. Wrap App with CubeProvider

```typescript
import { CubeProvider } from 'drizzle-cube/client'

function App() {
  return (
    <CubeProvider
      apiOptions={{ apiUrl: '/cubejs-api/v1' }}
      token="your-auth-token"
    >
      <YourDashboard />
    </CubeProvider>
  )
}
```

### 2. Create Dashboard Component

```typescript
import { AnalyticsDashboard } from 'drizzle-cube/client'
import { useState } from 'react'

function YourDashboard() {
  const [config, setConfig] = useState({
    portlets: [
      {
        id: 'portlet-1',
        title: 'Employee Count by Department',
        query: JSON.stringify({
          measures: ['Employees.count'],
          dimensions: ['Departments.name']
        }),
        chartType: 'bar',
        chartConfig: {
          xAxis: ['Departments.name'],
          yAxis: ['Employees.count']
        },
        x: 0,
        y: 0,
        w: 6,
        h: 4
      }
    ]
  })

  return (
    <AnalyticsDashboard
      config={config}
      editable={true}
      onConfigChange={setConfig}
      onSave={async (newConfig) => {
        // Save to backend
        await saveDashboard(newConfig)
      }}
    />
  )
}
```

## CubeProvider Configuration

### Basic Configuration

```typescript
<CubeProvider
  apiOptions={{ apiUrl: '/cubejs-api/v1' }}
  token="auth-token"
  features={{ enableAI: true }}  // Optional: Enable AI features
>
  {children}
</CubeProvider>
```

**Props:**
- `apiOptions`: Object with `apiUrl` for Cube API endpoint
- `token`: Authentication token (optional)
- `features`: Optional features configuration (e.g., `{ enableAI: true }`)

### With Dynamic Token

```typescript
import { useState, useEffect } from 'react'
import { CubeProvider } from 'drizzle-cube/client'

function App() {
  const [token, setToken] = useState(null)

  useEffect(() => {
    // Fetch token from auth system
    const fetchToken = async () => {
      const authToken = await getAuthToken()
      setToken(authToken)
    }
    fetchToken()
  }, [])

  if (!token) return <div>Loading...</div>

  return (
    <CubeProvider
      apiOptions={{ apiUrl: '/cubejs-api/v1' }}
      token={token}
    >
      <Dashboard />
    </CubeProvider>
  )
}
```

### With Runtime Configuration Updates

```typescript
import { useCubeContext } from 'drizzle-cube/client'

function DashboardSettings() {
  const { updateApiConfig } = useCubeContext()

  const switchEnvironment = (env) => {
    const apiUrl = env === 'prod'
      ? '/api/cubejs-api/v1'
      : '/dev-api/cubejs-api/v1'

    const token = getTokenForEnvironment(env)

    updateApiConfig({ apiUrl }, token)
  }

  return (
    <div>
      <button onClick={() => switchEnvironment('dev')}>Dev</button>
      <button onClick={() => switchEnvironment('prod')}>Prod</button>
    </div>
  )
}
```

## Dashboard Configuration

### Dashboard Config Structure

```typescript
interface DashboardConfig {
  portlets: PortletConfig[]
  layouts?: { [key: string]: any }  // Optional react-grid-layout layouts
  colorPalette?: string  // Optional color palette name (not limited to specific values)
}

interface PortletConfig {
  id: string                      // Unique identifier
  title: string                   // Display title
  query: string                   // JSON string of CubeQuery
  chartType: ChartType            // Chart type
  chartConfig?: ChartAxisConfig   // Axis configuration
  displayConfig?: ChartDisplayConfig // Visual settings
  x: number                       // Grid X position (0-based)
  y: number                       // Grid Y position (0-based)
  w: number                       // Grid width (columns)
  h: number                       // Grid height (rows)
}
```

### Complete Dashboard Example

```typescript
import { AnalyticsDashboard } from 'drizzle-cube/client'
import { useState } from 'react'

function EmployeeDashboard() {
  const [config, setConfig] = useState({
    colorPalette: 'ocean',
    portlets: [
      // KPI - Total Employees
      {
        id: 'kpi-total',
        title: 'Total Employees',
        query: JSON.stringify({
          measures: ['Employees.count']
        }),
        chartType: 'kpiNumber',
        displayConfig: {
          prefix: '',
          suffix: ' employees',
          decimals: 0
        },
        x: 0,
        y: 0,
        w: 3,
        h: 2
      },

      // KPI - Average Salary
      {
        id: 'kpi-salary',
        title: 'Average Salary',
        query: JSON.stringify({
          measures: ['Employees.avgSalary']
        }),
        chartType: 'kpiNumber',
        displayConfig: {
          prefix: '$',
          suffix: '',
          decimals: 2
        },
        x: 3,
        y: 0,
        w: 3,
        h: 2
      },

      // Bar Chart - Department Distribution
      {
        id: 'chart-departments',
        title: 'Employees by Department',
        query: JSON.stringify({
          measures: ['Employees.count'],
          dimensions: ['Departments.name'],
          order: { 'Employees.count': 'desc' }
        }),
        chartType: 'bar',
        chartConfig: {
          xAxis: ['Departments.name'],
          yAxis: ['Employees.count']
        },
        displayConfig: {
          showLegend: true,
          orientation: 'vertical'
        },
        x: 0,
        y: 2,
        w: 6,
        h: 4
      },

      // Line Chart - Hiring Trend
      {
        id: 'chart-hiring',
        title: 'Hiring Trend',
        query: JSON.stringify({
          measures: ['Employees.count'],
          timeDimensions: [{
            dimension: 'Employees.createdAt',
            granularity: 'month',
            dateRange: 'last 12 months'
          }]
        }),
        chartType: 'line',
        chartConfig: {
          xAxis: ['Employees.createdAt'],
          yAxis: ['Employees.count']
        },
        displayConfig: {
          showGrid: true,
          showTooltip: true
        },
        x: 6,
        y: 0,
        w: 6,
        h: 6
      },

      // Table - Employee List
      {
        id: 'table-employees',
        title: 'Recent Hires',
        query: JSON.stringify({
          dimensions: [
            'Employees.name',
            'Employees.email',
            'Departments.name',
            'Employees.createdAt'
          ],
          order: { 'Employees.createdAt': 'desc' },
          limit: 10
        }),
        chartType: 'table',
        x: 0,
        y: 6,
        w: 12,
        h: 4
      }
    ]
  })

  const handleSave = async (newConfig) => {
    try {
      await fetch('/api/dashboards/employees', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newConfig)
      })
      alert('Dashboard saved!')
    } catch (error) {
      alert('Failed to save dashboard')
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Employee Analytics</h1>
      <AnalyticsDashboard
        config={config}
        editable={true}
        onConfigChange={setConfig}
        onSave={handleSave}
      />
    </div>
  )
}
```

## Grid Layout System

The dashboard uses a 12-column responsive grid system.

### Grid Dimensions

- **Columns**: 12 columns total width
- **Rows**: Auto-height based on content
- **Units**: Each `w` = 1 column, each `h` = 60px

### Positioning Examples

```typescript
// Full width portlet
{
  x: 0,  // Start at left
  y: 0,  // Start at top
  w: 12, // Full width (12 columns)
  h: 4   // 320px height (h × 80px rowHeight)
}

// Half width portlets side-by-side
[
  {
    x: 0,  // Left half
    y: 0,
    w: 6,  // Half width (6 columns)
    h: 4
  },
  {
    x: 6,  // Right half
    y: 0,
    w: 6,  // Half width
    h: 4
  }
]

// Three equal columns
[
  { x: 0, y: 0, w: 4, h: 3 }, // Left third
  { x: 4, y: 0, w: 4, h: 3 }, // Middle third
  { x: 8, y: 0, w: 4, h: 3 }  // Right third
]

// Dashboard header row + main content
[
  { x: 0, y: 0, w: 3, h: 2 }, // KPI 1
  { x: 3, y: 0, w: 3, h: 2 }, // KPI 2
  { x: 6, y: 0, w: 3, h: 2 }, // KPI 3
  { x: 9, y: 0, w: 3, h: 2 }, // KPI 4
  { x: 0, y: 2, w: 12, h: 6 } // Full-width chart below
]
```

### Responsive Breakpoints

The grid automatically adapts to screen sizes:

- **Large (≥1200px)**: 12 columns
- **Medium (≥996px)**: 10 columns
- **Small (≥768px)**: 6 columns
- **XSmall (≥480px)**: 4 columns
- **XXSmall (<480px)**: 2 columns

## Editable vs Read-Only

### Editable Dashboard

```typescript
<AnalyticsDashboard
  config={config}
  editable={true}              // Enable editing
  onConfigChange={setConfig}   // Handle layout changes
  onSave={handleSave}          // Save button handler
/>
```

Features in edit mode:
- Drag and drop portlets
- Resize portlets
- Edit chart configurations
- Add/remove portlets
- Save button appears

### Read-Only Dashboard

```typescript
<AnalyticsDashboard
  config={config}
  editable={false}  // Disable editing
/>
```

Features disabled:
- No drag and drop
- No resize handles
- No edit buttons
- No save button
- View-only mode

## Persisting Dashboard Configuration

### Save to Backend

```typescript
function Dashboard() {
  const [config, setConfig] = useState(null)
  const [isDirty, setIsDirty] = useState(false)

  // Load dashboard on mount
  useEffect(() => {
    const loadDashboard = async () => {
      const response = await fetch('/api/dashboards/my-dashboard')
      const data = await response.json()
      setConfig(data)
    }
    loadDashboard()
  }, [])

  const handleSave = async (newConfig) => {
    try {
      await fetch('/api/dashboards/my-dashboard', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newConfig)
      })
      setIsDirty(false)
      console.log('Dashboard saved successfully')
    } catch (error) {
      console.error('Failed to save dashboard:', error)
      throw error // AnalyticsDashboard will handle error display
    }
  }

  if (!config) return <div>Loading...</div>

  return (
    <AnalyticsDashboard
      config={config}
      editable={true}
      onConfigChange={setConfig}
      onSave={handleSave}
      onDirtyStateChange={setIsDirty}
    />
  )
}
```

### Local Storage Persistence

```typescript
function Dashboard() {
  const [config, setConfig] = useState(() => {
    // Load from localStorage on mount
    const saved = localStorage.getItem('dashboard-config')
    return saved ? JSON.parse(saved) : defaultConfig
  })

  const handleSave = async (newConfig) => {
    // Save to localStorage
    localStorage.setItem('dashboard-config', JSON.stringify(newConfig))
  }

  const handleConfigChange = (newConfig) => {
    setConfig(newConfig)
    // Auto-save to localStorage
    localStorage.setItem('dashboard-config', JSON.stringify(newConfig))
  }

  return (
    <AnalyticsDashboard
      config={config}
      editable={true}
      onConfigChange={handleConfigChange}
      onSave={handleSave}
    />
  )
}
```

## Using Dashboard Hooks

### useCubeQuery Hook

Execute queries programmatically:

```typescript
import { useCubeQuery } from 'drizzle-cube/client'

function CustomWidget() {
  const { resultSet, isLoading, error } = useCubeQuery({
    measures: ['Employees.count'],
    dimensions: ['Departments.name']
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      {resultSet.tablePivot().map(row => (
        <div key={row['Departments.name']}>
          {row['Departments.name']}: {row['Employees.count']}
        </div>
      ))}
    </div>
  )
}
```

### useCubeMeta Hook

Access cube metadata:

```typescript
import { useCubeMeta } from 'drizzle-cube/client'

function MetadataExplorer() {
  const { meta, loading, error } = useCubeMeta()

  if (loading) return <div>Loading metadata...</div>
  if (error) return <div>Error loading metadata</div>

  return (
    <div>
      <h2>Available Cubes</h2>
      {meta.cubes.map(cube => (
        <div key={cube.name}>
          <h3>{cube.title || cube.name}</h3>
          <p>Measures: {cube.measures.length}</p>
          <p>Dimensions: {cube.dimensions.length}</p>
        </div>
      ))}
    </div>
  )
}
```

### useCubeContext Hook

Access provider context:

```typescript
import { useCubeContext } from 'drizzle-cube/client'

function ApiSettings() {
  const {
    cubeApi,
    meta,
    metaLoading,
    updateApiConfig,
    refetchMeta
  } = useCubeContext()

  const switchServer = () => {
    updateApiConfig(
      { apiUrl: '/new-api/cubejs-api/v1' },
      'new-token'
    )
    refetchMeta() // Reload metadata from new server
  }

  return (
    <div>
      <p>API URL: {cubeApi.apiUrl}</p>
      <p>Cubes loaded: {meta?.cubes.length || 0}</p>
      <button onClick={switchServer}>Switch Server</button>
      <button onClick={refetchMeta}>Refresh Metadata</button>
    </div>
  )
}
```

## Color Palettes

Built-in color palettes for consistent theming:

```typescript
// Available palettes
const palettes = [
  'default',  // Blue-green gradient
  'ocean',    // Blue tones
  'sunset',   // Orange-red gradient
  'forest'    // Green tones
]

// Usage
<AnalyticsDashboard
  config={{
    ...config,
    colorPalette: 'ocean'
  }}
/>
```

## Complete Application Example

```typescript
// App.tsx
import { CubeProvider, AnalyticsDashboard } from 'drizzle-cube/client'
import { useState, useEffect } from 'react'

function App() {
  const [token, setToken] = useState(null)
  const [config, setConfig] = useState(null)

  useEffect(() => {
    // Initialize auth and load dashboard
    const initialize = async () => {
      const authToken = await getAuthToken()
      setToken(authToken)

      const dashboard = await fetch('/api/dashboards/main', {
        headers: { Authorization: `Bearer ${authToken}` }
      }).then(r => r.json())

      setConfig(dashboard)
    }

    initialize()
  }, [])

  const handleSave = async (newConfig) => {
    await fetch('/api/dashboards/main', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(newConfig)
    })
  }

  if (!token || !config) {
    return <div>Loading...</div>
  }

  return (
    <CubeProvider
      apiOptions={{ apiUrl: '/cubejs-api/v1' }}
      token={token}
    >
      <div className="min-h-screen bg-gray-100">
        <header className="bg-white shadow px-4 py-6">
          <h1 className="text-3xl font-bold">Analytics Dashboard</h1>
        </header>

        <main className="container mx-auto p-4">
          <AnalyticsDashboard
            config={config}
            editable={true}
            onConfigChange={setConfig}
            onSave={handleSave}
          />
        </main>
      </div>
    </CubeProvider>
  )
}

export default App
```

## Programmatic Dashboard Filters

Dashboard filters can be applied programmatically by passing them through the `dashboardFilters` prop. This is useful for embedding dashboards with pre-configured filters from your application.

### Filter Structure

```typescript
interface DashboardFilter {
  id: string        // Unique identifier
  label: string     // Display label
  filter: Filter    // Filter definition (SimpleFilter or GroupFilter)
}

// Simple filter
interface SimpleFilter {
  member: string           // Field name (e.g., 'Employees.department')
  operator: FilterOperator // equals, notEquals, contains, gt, lt, etc.
  values: any[]           // Filter values
}

// Group filter (AND/OR logic)
interface GroupFilter {
  type: 'and' | 'or'
  filters: Filter[]       // Array of SimpleFilter or GroupFilter
}
```

### Basic Programmatic Filter Example

```typescript
import { AnalyticsDashboard } from 'drizzle-cube/client'
import { useState } from 'react'

function DashboardWithFilters() {
  const [config, setConfig] = useState({
    portlets: [
      {
        id: 'portlet-1',
        title: 'Employee Count',
        query: JSON.stringify({
          measures: ['Employees.count'],
          dimensions: ['Departments.name']
        }),
        chartType: 'bar',
        chartConfig: {
          xAxis: ['Departments.name'],
          yAxis: ['Employees.count']
        },
        // Map which dashboard filters apply to this portlet
        dashboardFilterMapping: ['filter-1', 'filter-2'],
        x: 0,
        y: 0,
        w: 12,
        h: 4
      }
    ]
  })

  // Define programmatic filters
  const dashboardFilters = [
    {
      id: 'filter-1',
      label: 'Active Employees Only',
      filter: {
        member: 'Employees.isActive',
        operator: 'equals',
        values: [true]
      }
    },
    {
      id: 'filter-2',
      label: 'Engineering Department',
      filter: {
        member: 'Departments.name',
        operator: 'equals',
        values: ['Engineering']
      }
    }
  ]

  return (
    <AnalyticsDashboard
      config={config}
      dashboardFilters={dashboardFilters}  // Pass programmatic filters
      editable={false}
      onConfigChange={setConfig}
    />
  )
}
```

### Dynamic Filters from URL Parameters

```typescript
import { AnalyticsDashboard } from 'drizzle-cube/client'
import { useSearchParams } from 'react-router-dom'
import { useMemo } from 'react'

function DashboardWithURLFilters() {
  const [searchParams] = useSearchParams()
  const [config, setConfig] = useState(dashboardConfig)

  // Build filters from URL parameters
  const dashboardFilters = useMemo(() => {
    const filters = []

    // Department filter from ?department=Engineering
    const department = searchParams.get('department')
    if (department) {
      filters.push({
        id: 'url-department',
        label: `Department: ${department}`,
        filter: {
          member: 'Departments.name',
          operator: 'equals',
          values: [department]
        }
      })
    }

    // Date range filter from ?startDate=2024-01-01&endDate=2024-12-31
    const startDate = searchParams.get('startDate')
    const endDate = searchParams.get('endDate')
    if (startDate && endDate) {
      filters.push({
        id: 'url-daterange',
        label: 'Custom Date Range',
        filter: {
          member: 'Employees.createdAt',
          operator: 'inDateRange',
          values: [startDate, endDate]
        }
      })
    }

    // Status filter from ?status=active
    const status = searchParams.get('status')
    if (status === 'active') {
      filters.push({
        id: 'url-status',
        label: 'Active Only',
        filter: {
          member: 'Employees.isActive',
          operator: 'equals',
          values: [true]
        }
      })
    }

    return filters
  }, [searchParams])

  return (
    <AnalyticsDashboard
      config={config}
      dashboardFilters={dashboardFilters}
      editable={false}
      onConfigChange={setConfig}
    />
  )
}
```

### User-Based Filters

```typescript
import { AnalyticsDashboard } from 'drizzle-cube/client'
import { useAuth } from './auth'

function UserDashboard() {
  const { user } = useAuth()
  const [config, setConfig] = useState(dashboardConfig)

  // Apply filters based on user role/permissions
  const dashboardFilters = useMemo(() => {
    const filters = []

    // Department managers only see their department
    if (user.role === 'department_manager') {
      filters.push({
        id: 'user-department',
        label: `Your Department: ${user.department}`,
        filter: {
          member: 'Departments.name',
          operator: 'equals',
          values: [user.department]
        }
      })
    }

    // Regional managers see their region
    if (user.role === 'regional_manager') {
      filters.push({
        id: 'user-region',
        label: `Your Region: ${user.region}`,
        filter: {
          member: 'Employees.region',
          operator: 'equals',
          values: [user.region]
        }
      })
    }

    // All users see only active employees by default
    filters.push({
      id: 'default-active',
      label: 'Active Employees',
      filter: {
        member: 'Employees.isActive',
        operator: 'equals',
        values: [true]
      }
    })

    return filters
  }, [user])

  return (
    <AnalyticsDashboard
      config={config}
      dashboardFilters={dashboardFilters}
      editable={false}
      onConfigChange={setConfig}
    />
  )
}
```

### Complex Group Filters

```typescript
function DashboardWithComplexFilters() {
  const [config, setConfig] = useState(dashboardConfig)

  const dashboardFilters = [
    {
      id: 'complex-filter',
      label: 'Engineering or High Salary',
      filter: {
        type: 'or',
        filters: [
          {
            member: 'Departments.name',
            operator: 'equals',
            values: ['Engineering']
          },
          {
            member: 'Employees.salary',
            operator: 'gte',
            values: [100000]
          }
        ]
      }
    },
    {
      id: 'date-and-status',
      label: 'Recent Active Hires',
      filter: {
        type: 'and',
        filters: [
          {
            member: 'Employees.isActive',
            operator: 'equals',
            values: [true]
          },
          {
            member: 'Employees.createdAt',
            operator: 'afterDate',
            values: ['2024-01-01']
          }
        ]
      }
    }
  ]

  return (
    <AnalyticsDashboard
      config={config}
      dashboardFilters={dashboardFilters}
      editable={false}
      onConfigChange={setConfig}
    />
  )
}
```

### Mapping Filters to Specific Portlets

By default, programmatic filters are NOT applied to any portlets. You must explicitly map which filters apply to which portlets using the `dashboardFilterMapping` array:

```typescript
const config = {
  portlets: [
    {
      id: 'portlet-1',
      title: 'All Employees',
      query: JSON.stringify({
        measures: ['Employees.count']
      }),
      chartType: 'kpiNumber',
      // This portlet uses both filters
      dashboardFilterMapping: ['filter-active', 'filter-department'],
      x: 0,
      y: 0,
      w: 4,
      h: 2
    },
    {
      id: 'portlet-2',
      title: 'All Departments (Unfiltered)',
      query: JSON.stringify({
        measures: ['Departments.count']
      }),
      chartType: 'kpiNumber',
      // This portlet uses NO filters (empty array or omit property)
      dashboardFilterMapping: [],
      x: 4,
      y: 0,
      w: 4,
      h: 2
    },
    {
      id: 'portlet-3',
      title: 'Active Employees Only',
      query: JSON.stringify({
        measures: ['Employees.count']
      }),
      chartType: 'kpiNumber',
      // This portlet uses only the active filter
      dashboardFilterMapping: ['filter-active'],
      x: 8,
      y: 0,
      w: 4,
      h: 2
    }
  ]
}

const dashboardFilters = [
  {
    id: 'filter-active',
    label: 'Active Only',
    filter: {
      member: 'Employees.isActive',
      operator: 'equals',
      values: [true]
    }
  },
  {
    id: 'filter-department',
    label: 'Engineering',
    filter: {
      member: 'Departments.name',
      operator: 'equals',
      values: ['Engineering']
    }
  }
]
```

### Available Filter Operators

```typescript
// String operators
'equals'       // Exact match
'notEquals'    // Not equal
'contains'     // Contains substring
'notContains'  // Does not contain substring
'startsWith'   // Starts with
'endsWith'     // Ends with

// Numeric operators
'gt'           // Greater than
'gte'          // Greater than or equal
'lt'           // Less than
'lte'          // Less than or equal

// Null operators
'set'          // Is not null
'notSet'       // Is null

// Date operators
'inDateRange'  // Between two dates (values: [startDate, endDate])
'beforeDate'   // Before a date (values: [date])
'afterDate'    // After a date (values: [date])
```

### Filter Merging Behavior

Filters are merged with portlet queries using AND logic:

```typescript
// Portlet query
{
  measures: ['Employees.count'],
  filters: [{
    member: 'Employees.salary',
    operator: 'gte',
    values: [50000]
  }]
}

// Dashboard filter applied
{
  member: 'Employees.isActive',
  operator: 'equals',
  values: [true]
}

// Final merged query (automatic)
{
  measures: ['Employees.count'],
  filters: {
    and: [
      {
        member: 'Employees.isActive',
        operator: 'equals',
        values: [true]
      },
      {
        member: 'Employees.salary',
        operator: 'gte',
        values: [50000]
      }
    ]
  }
}
```

### Hiding Filter UI in Edit Mode

Programmatic filters are always hidden from the filter panel UI. They are applied silently in the background and cannot be edited by users through the dashboard interface. This is useful for:

- Security filtering (user can only see their data)
- Environment filtering (production vs staging)
- Application-level filtering (tenant isolation)
- URL parameter filtering (dashboard embedding)

### Complete Example: Multi-Tenant Dashboard

```typescript
import { AnalyticsDashboard } from 'drizzle-cube/client'
import { useAuth } from './auth'
import { useSearchParams } from 'react-router-dom'

function TenantDashboard() {
  const { user } = useAuth()
  const [searchParams] = useSearchParams()
  const [config, setConfig] = useState(dashboardConfig)

  // Combine tenant isolation + URL filters
  const dashboardFilters = useMemo(() => {
    const filters = []

    // REQUIRED: Tenant isolation (security)
    filters.push({
      id: 'tenant-isolation',
      label: `Organization: ${user.organizationName}`,
      filter: {
        member: 'Employees.organisationId',
        operator: 'equals',
        values: [user.organizationId]
      }
    })

    // OPTIONAL: URL department filter
    const department = searchParams.get('department')
    if (department) {
      filters.push({
        id: 'url-department',
        label: `Department: ${department}`,
        filter: {
          member: 'Departments.name',
          operator: 'equals',
          values: [department]
        }
      })
    }

    // OPTIONAL: URL date range
    const dateRange = searchParams.get('range')
    if (dateRange === 'last30days') {
      filters.push({
        id: 'url-daterange',
        label: 'Last 30 Days',
        filter: {
          member: 'Employees.createdAt',
          operator: 'inDateRange',
          values: ['2024-01-01', '2024-01-31']
        }
      })
    }

    return filters
  }, [user, searchParams])

  return (
    <AnalyticsDashboard
      config={config}
      dashboardFilters={dashboardFilters}
      editable={user.canEditDashboards}
      onConfigChange={setConfig}
    />
  )
}
```

## Best Practices

1. **Wrap with CubeProvider** - All dashboard components need CubeProvider
2. **Persist configuration** - Save dashboard config to backend/localStorage
3. **Handle errors gracefully** - Show user-friendly error messages
4. **Use appropriate grid sizes** - Consider mobile responsiveness
5. **Limit portlet count** - Too many portlets impact performance
6. **Cache query results** - Use React Query or similar for caching
7. **Validate queries** - Ensure query strings are valid JSON
8. **Use programmatic filters for security** - Apply tenant/user isolation via dashboardFilters
9. **Map filters explicitly** - Use dashboardFilterMapping to control which portlets get which filters

## Common Pitfalls

- **Missing CubeProvider** - Dashboard components require provider context
- **Invalid query JSON** - Query must be valid JSON string
- **Grid overlaps** - Ensure portlet positions don't overlap
- **Missing security token** - API calls require authentication
- **Large initial queries** - Use filters to limit initial data load

## Next Steps

- Configure **chart types** with the specific chart skills
- Build **queries** with the `queries` skill
- Set up **server APIs** with the `server-setup` skill
- Learn about **cube definitions** with the `cube-definition` skill
