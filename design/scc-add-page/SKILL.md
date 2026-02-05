---
name: scc-add-page
description: Add new pages to SCC Admin project (Next.js 14 App Router). Use when implementing new admin pages for accessibility management, quest management, challenge management, or other features. Covers route group selection, page structure, React Query integration, form handling, navigation setup, and styling with Tailwind CSS and shadcn/ui. Use for tasks like "Add new page for X", "Create admin interface for Y", or "Implement listing/detail page for Z".
---

# SCC Admin Page Creation

Add new pages to the SCC Admin dashboard following Next.js 14 App Router conventions with proper authentication, data fetching, and styling patterns.

## Workflow Decision Tree

Start here to determine the type of page to create:

1. **Does the page require authentication?**
   - Yes → Use `(private)` route group → See [Private Page Creation](#private-page-creation)
   - No → Use `(public)` route group → See [Public Page Creation](#public-page-creation)

2. **What type of authenticated page?**
   - List with search/filtering → [List Page Pattern](#list-page-pattern)
   - Detail view with editing → [Detail Page Pattern](#detail-page-pattern)
   - Create new item → [Create Page Pattern](#create-page-pattern)
   - Custom layout → Combine patterns as needed

## Private Page Creation

For authenticated admin pages (most common use case).

### Step 1: Create Directory Structure

```bash
mkdir -p app/(private)/[feature-name]
```

**Naming conventions:**
- Use lowercase kebab-case: `accessibility`, `quest`, `challenge`
- Singular or plural based on existing patterns (check `app/(private)/` directory)

### Step 2: Choose Page Type and Create Files

Based on requirements, create one or more page types:

**For List Page:**
```bash
# Main listing page
touch app/(private)/[feature-name]/page.tsx
touch app/(private)/[feature-name]/query.ts
```

**For Detail Page (with dynamic ID):**
```bash
mkdir -p app/(private)/[feature-name]/[id]
touch app/(private)/[feature-name]/[id]/page.tsx
# Use existing query.ts or create if not exists
```

**For Create Page:**
```bash
mkdir -p app/(private)/[feature-name]/create
touch app/(private)/[feature-name]/create/page.tsx
# Use existing query.ts or create if not exists
```

### Step 3: Implement Page Components

Use the template files from this skill's `assets/` directory as starting points:

- `assets/list-page.tsx` → Copy to `app/(private)/[feature-name]/page.tsx`
- `assets/detail-page.tsx` → Copy to `app/(private)/[feature-name]/[id]/page.tsx`
- `assets/create-page.tsx` → Copy to `app/(private)/[feature-name]/create/page.tsx`
- `assets/query.ts` → Copy to `app/(private)/[feature-name]/query.ts`

**Important customizations needed in each template:**
1. Replace all `TODO` comments with actual implementation
2. Update type definitions to match your data model
3. Replace API calls with actual endpoints from the generated client
4. Update query keys (e.g., `["@features"]` → `["@yourFeature"]`)
5. Update navigation paths (e.g., `/feature` → `/your-feature`)

### Step 4: Implement Data Fetching

Edit `query.ts` to add React Query hooks:

```typescript
import { useInfiniteQuery, useQuery } from "@tanstack/react-query"
import { api } from "@/lib/apis/api"

// For list pages with pagination
export function useFeatureList(params?: SearchParams) {
  return useInfiniteQuery({
    queryKey: ["@features", params],
    queryFn: ({ pageParam }) =>
      api.default.getFeatures(pageParam, "100", params)
        .then((res) => res.data),
    initialPageParam: null as string | null,
    getNextPageParam: (lastPage) => lastPage.cursor,
  })
}

// For detail pages
export function useFeature({ id }: { id: string }) {
  return useQuery({
    queryKey: ["@feature", id],
    queryFn: () => api.default.getFeature(id).then((res) => res.data),
  })
}
```

**Query key naming:** Use `@` prefix and descriptive names: `["@features"]`, `["@feature", id]`

### Step 5: Add Navigation Entry

If the page should appear in the sidebar menu, edit `app/constants/menu.ts`:

```typescript
import { IconName } from "lucide-react"

export const menuItems: MenuItem[] = [
  // ... existing items
  {
    title: "Feature Display Name",
    url: "/feature-name",
    icon: IconName, // Choose from lucide-react
  },
]
```

**Common icons:** `MapPin`, `ClipboardList`, `Users`, `Settings`, `Bell`, `Layout`

### Step 6: Verify and Test

1. **Run development server:**
   ```bash
   pnpm dev
   ```

2. **Check for errors:**
   - TypeScript errors: Run `pnpm typecheck`
   - Lint errors: Run `pnpm lint`

3. **Test authentication:**
   - Verify redirect to login when not authenticated
   - Test that authenticated users can access the page

4. **Test data flow:**
   - Verify API calls are working
   - Check loading states
   - Test error handling
   - Verify mutations invalidate queries correctly

## Public Page Creation

For pages that don't require authentication (login, guides, public views).

### Structure

```bash
mkdir -p app/(public)/[feature-name]
touch app/(public)/[feature-name]/page.tsx
```

### Key Differences

- No authentication check (accessible without token)
- Uses minimal layout without sidebar
- Typically simpler than private pages

### Example Use Cases

- Login page: `app/(public)/account/login/page.tsx`
- Public guides: `app/(public)/public/guide/page.tsx`
- Public quest viewing: `app/(public)/public/quest/[id]/page.tsx`

## Page Type Patterns

### List Page Pattern

**Use for:** Browsing collections with search, filtering, and pagination

**Key features:**
- Search/filter form with React Hook Form
- DataTable component with column filtering
- Infinite scroll pagination with React Query
- Optional expandable rows for inline details

**Template:** `assets/list-page.tsx`

**Reference:** See `references/page-patterns.md` § List Page with Pagination

### Detail Page Pattern

**Use for:** Viewing and editing individual items

**Key features:**
- Dynamic route with `[id]` parameter
- View/edit mode toggle
- Form sync with fetched data
- Confirmation dialogs for destructive actions
- Query invalidation after mutations

**Template:** `assets/detail-page.tsx`

**Reference:** See `references/page-patterns.md` § Detail Page with Edit Mode

### Create Page Pattern

**Use for:** Creating new items

**Key features:**
- Form with default values
- Redirect to list after creation
- Query invalidation to refresh parent list

**Template:** `assets/create-page.tsx`

**Reference:** See `references/page-patterns.md` § Create Page

## Styling Guidelines

**IMPORTANT**: For new files, use only **Tailwind CSS** and **shadcn/ui** components. Do not use Panda CSS styled-components.

### Layout Components

Use appropriate layout wrapper:

```typescript
import { Contents } from "@/components/layout/Contents"

// Standard single-column layout (uses Tailwind internally)
<Contents.Normal>
  {/* Page content */}
</Contents.Normal>

// Two-column layout
<Contents.Columns>
  <div>{/* Left column */}</div>
  <div>{/* Right column */}</div>
</Contents.Columns>

// Custom layout with Tailwind
<main className="w-full p-8">
  {/* Custom content */}
</main>
```

### Card Components

Organize content in cards using shadcn/ui:

```typescript
import { Card } from "@/components/ui/card"

<Card className="p-6">
  {/* Card content */}
</Card>
```

### Tailwind CSS Styling

Use Tailwind utility classes for all styling:

```typescript
// Spacing and layout
<div className="p-4 m-2 space-y-4">

// Flexbox and grid
<div className="flex gap-4 items-center">
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

// Colors and backgrounds
<div className="bg-white text-gray-900 border border-gray-200">

// Responsive design
<div className="w-full md:w-1/2 lg:w-1/3">

// Hover and focus states
<button className="hover:bg-gray-100 focus:ring-2">
```

### Using shadcn/ui Components

Leverage shadcn/ui components for consistent UI:

```typescript
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card } from "@/components/ui/card"

<Card className="p-6">
  <Label htmlFor="name">Name</Label>
  <Input id="name" placeholder="Enter name" className="mt-2" />
  <Button className="mt-4">Submit</Button>
</Card>
```

### Combining Classes with cn Utility

Use the `cn` utility from shadcn to combine classes conditionally:

```typescript
import { cn } from "@/lib/utils"

<div className={cn(
  "base-class",
  condition && "conditional-class",
  className // Allow external className override
)} />
```

## API Integration

### Using Generated Client

The project uses a generated TypeScript client from OpenAPI specs:

```typescript
import { api } from "@/lib/apis/api"

// GET
const data = await api.default.getItems().then(res => res.data)

// POST
await api.default.createItem({ name: "Example" })

// PUT
await api.default.updateItem(id, { name: "Updated" })

// DELETE
await api.default.deleteItem(id)
```

### Regenerating API Client

If the API changes:

```bash
pnpm codegen
```

This regenerates the client from `subprojects/scc-api/admin-api-spec.yaml`

## Common Patterns

### Form Handling

```typescript
import { useForm } from "react-hook-form"
import { TextInput } from "@reactleaf/input"

interface FormValues {
  name: string
  description: string
}

const form = useForm<FormValues>({ defaultValues })

<form onSubmit={form.handleSubmit(onSubmit)}>
  <TextInput {...form.register("name")} label="Name" />
  <Button type="submit">Submit</Button>
</form>
```

### Query Invalidation

After mutations, invalidate queries to refresh data:

```typescript
import { useQueryClient } from "@tanstack/react-query"

const queryClient = useQueryClient()

// After create/update/delete
await queryClient.invalidateQueries({ queryKey: ["@features"] })
await queryClient.invalidateQueries({ queryKey: ["@feature", id] })
```

### Toast Notifications

```typescript
import { toast } from "react-toastify"

toast.success("Operation successful")
toast.error("Operation failed")
```

### Confirmation Dialogs

```typescript
if (!window.confirm("Are you sure you want to delete this?")) {
  return
}
// Proceed with operation
```

## Additional Resources

For detailed patterns, examples, and conventions, see:

- **references/page-patterns.md** - Comprehensive reference for all page patterns, data fetching, forms, styling, and navigation
- **assets/*.tsx** - Template files ready to copy and customize
- **assets/query.ts** - React Query hooks template

## Troubleshooting

### TypeScript Errors

- Run `pnpm typecheck` to see all errors
- Ensure types match the generated API client
- Check that all imports are correct

### Authentication Not Working

- Verify page is in `(private)` route group
- Check that token exists in localStorage
- Review `app/(private)/layout.tsx` for auth logic

### API Calls Failing

- Verify API endpoint exists in generated client
- Check network tab for actual errors
- Ensure `NEXT_PUBLIC_DEPLOY_TYPE` is set correctly
- Try regenerating API client: `pnpm codegen`

### Styling Not Applied

- Verify Tailwind CSS is properly configured
- Check that className props are passed correctly
- Ensure shadcn/ui components are installed
- Clear build cache: `rm -rf .next` and rebuild

### Data Not Updating

- Check query invalidation after mutations
- Verify query keys match between hooks
- Ensure React Query DevTools shows correct cache state
