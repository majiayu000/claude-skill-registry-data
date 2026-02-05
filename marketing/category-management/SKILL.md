---
name: category-management
description: Manage blog categories including CRUD operations, slug generation, and category assignment. Use when working with categories, category forms, slugs, or organizing blog content by category.
---

# Category Management

## Overview
This skill helps you work with blog category management features. Categories organize blog posts and include automatic slug generation from titles.

## Key Files and Components

### Category Pages
- `src/app/admin/categories/page.tsx` - Category listing page
- `src/app/admin/categories/create/page.tsx` - Create new category page
- `src/app/admin/categories/edit/page.tsx` - Edit existing category page
- `src/app/admin/categories/category-form.tsx` - Main category form component

### Domain & Infrastructure
- `src/domains/category.ts` - Category model and types
- `src/infrastructure/das/categories.das.ts` - Category data access service
- `src/models/CreateCategoryModel.ts` - Create category model
- `src/models/UpdateCategoryModel.ts` - Update category model

### GraphQL Integration
- `src/infrastructure/graphQL/queries/categories/get-categories.ts` - Fetch categories
- `src/infrastructure/graphQL/queries/categories/get-blog-category-ids.ts` - Fetch category IDs
- `src/infrastructure/graphQL/graphql-client.ts` - Apollo client setup

## Category Structure

A category includes:
- **id**: Unique identifier (GUID)
- **name**: Category display name
- **slug**: URL-friendly identifier (auto-generated)
- **description**: Optional category description
- **rowVersion**: For optimistic locking

## Slug Generation

The project uses the `slugify` package for automatic slug generation:
```typescript
import slugify from 'slugify';

const slug = slugify(name, {
  lower: true,
  strict: true,
  trim: true
});
```

Slugs are:
- Lowercase
- Hyphen-separated
- URL-safe (special characters removed)
- Automatically generated from the name field

## API Integration

Categories support both REST and GraphQL:

### REST API Endpoints
- `GET /categories` - List all categories
- `GET /categories/:id` - Get single category
- `POST /categories` - Create new category
- `PUT /categories/:id` - Update existing category
- `DELETE /categories/:id` - Delete category

### GraphQL Queries
- `GET_CATEGORIES` - Fetch all categories with posts
- `GET_BLOG_CATEGORY_IDS` - Fetch category IDs for blog post filtering

All API calls require Bearer token authentication.

## Common Tasks

### Creating a Category

1. User enters category name
2. Slug is auto-generated from name
3. Optional description can be added
4. Submit creates category via REST API
5. Navigate back to category list

### Editing a Category

1. Fetch existing category by ID
2. Populate form with current data
3. Allow name, slug, and description edits
4. Include rowVersion for optimistic locking
5. Submit updates category via REST API
6. Navigate back to category list

### Listing Categories

1. Fetch categories from REST API or GraphQL
2. Display in table or grid format
3. Show name, slug, and action buttons
4. Support edit and delete operations

### Category Selection

When assigning categories to blog posts:
1. Fetch all categories
2. Display in dropdown/select component
3. Store selected categoryId with post

## Data Access Patterns

### Using REST API
```typescript
import { getApiUrl, authenticatedFetch } from '@/config/api.config';

// Fetch categories
const response = await authenticatedFetch(
  getApiUrl('/categories'),
  token
);
const data = await response.json();
```

### Using GraphQL
```typescript
import { graphqlClient } from '@/infrastructure/graphQL/graphql-client';
import { GET_CATEGORIES } from '@/infrastructure/graphQL/queries/categories/get-categories';

const { data } = await graphqlClient.query({
  query: GET_CATEGORIES
});
```

## Best Practices

1. **Always generate slugs** from names automatically
2. **Validate uniqueness** of slugs before submission
3. **Handle rowVersion** for update operations
4. **Check authentication** before API calls
5. **Show loading states** during data fetching
6. **Handle errors gracefully** with user feedback
7. **Use TypeScript types** from domain models
8. **Cache category lists** where appropriate (Apollo handles this for GraphQL)

## TypeScript Types

Always use the domain types:
```typescript
import type { CategoryModel } from '@/domains/category';
import type { CreateCategoryModel } from '@/models/CreateCategoryModel';
import type { UpdateCategoryModel } from '@/models/UpdateCategoryModel';
```

## Debugging Tips

If you encounter issues:
1. Verify slug generation is working correctly
2. Check API endpoints are reachable
3. Validate authentication token
4. Review GraphQL query syntax
5. Check Apollo cache for stale data
6. Verify rowVersion matches for updates
7. Test category assignment in blog posts

## Integration with Blog Posts

Categories are referenced in blog posts:
- Blog posts have a `categoryId` field
- Categories can have multiple posts
- Use category data for filtering and organization
- Display category name with blog post metadata

## Example Workflow

When implementing category features:

1. Read category domain model
2. Review existing category-form.tsx
3. Check API configuration (REST and GraphQL)
4. Test slug generation
5. Implement changes following patterns
6. Validate with TypeScript
7. Test CRUD operations in dev server
