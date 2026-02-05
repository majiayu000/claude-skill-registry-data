---
name: polaris-ui-patterns
description: Build consistent UI using Polaris Web Components patterns for common page layouts like index pages, detail pages, forms, and empty states. Use this skill when creating new pages or refactoring existing UI components.
allowed-tools: [Read, Edit, Write, Grep, Glob]
---

# Polaris UI Patterns Skill

## Purpose
This skill provides reusable UI patterns and templates for common page layouts in Shopify apps using Polaris Web Components.

## When to Use This Skill

- Creating new pages (index, detail, form)
- Implementing common UI patterns
- Building consistent layouts
- Adding empty states
- Creating modals and forms
- Implementing tables with actions

## Core Patterns

### Pattern 1: Index/List Page

**Use for**: Products, Orders, Customers, Custom Entities

```tsx
import type { LoaderFunctionArgs } from "react-router";
import { useLoaderData } from "react-router";
import { authenticate } from "../shopify.server";
import { db } from "../db.server";
import { json } from "@remix-run/node";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const shop = await db.shop.findUnique({
    where: { shopDomain: session.shop }
  });

  const items = await db.item.findMany({
    where: { shopId: shop.id },
    orderBy: { createdAt: 'desc' },
    take: 50,
  });

  const stats = {
    total: items.length,
    active: items.filter(i => i.isActive).length,
  };

  return json({ items, stats });
};

export default function ItemsIndexPage() {
  const { items, stats } = useLoaderData<typeof loader>();

  return (
    <s-page heading="Items">
      {/* Stats Section */}
      <s-section>
        <s-grid columns="3">
          <s-box border="base" borderRadius="base" padding="400">
            <s-stack gap="200" direction="vertical">
              <s-text variant="headingMd" as="h3">Total Items</s-text>
              <s-text variant="heading2xl" as="p">{stats.total}</s-text>
            </s-stack>
          </s-box>
          <s-box border="base" borderRadius="base" padding="400">
            <s-stack gap="200" direction="vertical">
              <s-text variant="headingMd" as="h3">Active</s-text>
              <s-text variant="heading2xl" as="p">{stats.active}</s-text>
            </s-stack>
          </s-box>
        </s-grid>
      </s-section>

      {/* Table Section */}
      <s-section>
        <s-card>
          <s-table>
            <s-table-head>
              <s-table-row>
                <s-table-cell as="th">Name</s-table-cell>
                <s-table-cell as="th">Status</s-table-cell>
                <s-table-cell as="th">Created</s-table-cell>
                <s-table-cell as="th">Actions</s-table-cell>
              </s-table-row>
            </s-table-head>
            <s-table-body>
              {items.map(item => (
                <s-table-row key={item.id}>
                  <s-table-cell>{item.name}</s-table-cell>
                  <s-table-cell>
                    <s-badge tone={item.isActive ? "success" : undefined}>
                      {item.isActive ? "Active" : "Inactive"}
                    </s-badge>
                  </s-table-cell>
                  <s-table-cell>{new Date(item.createdAt).toLocaleDateString()}</s-table-cell>
                  <s-table-cell>
                    <s-button-group>
                      <s-button variant="plain">Edit</s-button>
                      <s-button variant="plain" tone="critical">Delete</s-button>
                    </s-button-group>
                  </s-table-cell>
                </s-table-row>
              ))}
            </s-table-body>
          </s-table>
        </s-card>
      </s-section>
    </s-page>
  );
}
```

### Pattern 2: Detail/Edit Page

```tsx
export const loader = async ({ params, request }: LoaderFunctionArgs) => {
  const { session } = await authenticate.admin(request);
  const shop = await db.shop.findUnique({
    where: { shopDomain: session.shop }
  });

  const item = await db.item.findUnique({
    where: {
      id: params.id,
      shopId: shop.id,
    },
  });

  if (!item) {
    throw new Response("Not Found", { status: 404 });
  }

  return json({ item });
};

export const action = async ({ params, request }: ActionFunctionArgs) => {
  const formData = await request.formData();
  const name = formData.get("name");
  const description = formData.get("description");

  await db.item.update({
    where: { id: params.id },
    data: { name, description },
  });

  return redirect("/app/items");
};

export default function ItemDetailPage() {
  const { item } = useLoaderData<typeof loader>();

  return (
    <s-page heading={item.name} backUrl="/app/items">
      <form method="post">
        <s-card>
          <s-stack gap="400" direction="vertical">
            <s-text-field
              label="Name"
              name="name"
              defaultValue={item.name}
              required
            />
            <s-text-field
              label="Description"
              name="description"
              defaultValue={item.description}
              multiline={4}
            />
            <s-button-group>
              <s-button type="submit" variant="primary">Save</s-button>
              <s-button url="/app/items">Cancel</s-button>
            </s-button-group>
          </s-stack>
        </s-card>
      </form>
    </s-page>
  );
}
```

### Pattern 3: Modal Pattern

```tsx
function ItemModal({ item, onClose }) {
  const submit = useSubmit();

  function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    submit(formData, { method: "post" });
    onClose();
  }

  return (
    <s-modal open onClose={onClose} title="Edit Item">
      <form onSubmit={handleSubmit}>
        <s-modal-section>
          <s-stack gap="400" direction="vertical">
            <s-text-field
              label="Name"
              name="name"
              defaultValue={item?.name}
            />
            <s-text-field
              label="Description"
              name="description"
              defaultValue={item?.description}
              multiline={3}
            />
          </s-stack>
        </s-modal-section>
        <s-modal-footer>
          <s-button-group>
            <s-button onClick={onClose}>Cancel</s-button>
            <s-button type="submit" variant="primary">Save</s-button>
          </s-button-group>
        </s-modal-footer>
      </form>
    </s-modal>
  );
}
```

### Pattern 4: Empty State

```tsx
{items.length === 0 ? (
  <s-card>
    <s-empty-state
      heading="No items yet"
      image="https://cdn.shopify.com/..."
    >
      <s-text variant="bodyMd">
        Start by adding your first item
      </s-text>
      <s-button variant="primary" url="/app/items/new">
        Add Item
      </s-button>
    </s-empty-state>
  </s-card>
) : (
  // Item list
)}
```

### Pattern 5: Loading State

```tsx
import { useNavigation } from "@remix-run/react";

export default function ItemsPage() {
  const navigation = useNavigation();
  const isLoading = navigation.state === "loading";

  return (
    <s-page heading="Items">
      {isLoading ? (
        <s-card>
          <s-stack gap="400" direction="vertical">
            <s-skeleton-display-text />
            <s-skeleton-display-text />
            <s-skeleton-display-text />
          </s-stack>
        </s-card>
      ) : (
        // Content
      )}
    </s-page>
  );
}
```

### Pattern 6: Form with Validation

```tsx
export const action = async ({ request }: ActionFunctionArgs) => {
  const formData = await request.formData();
  const name = formData.get("name");

  const errors = {};
  if (!name) errors.name = "Name is required";
  if (name.length < 3) errors.name = "Name must be at least 3 characters";

  if (Object.keys(errors).length > 0) {
    return json({ errors }, { status: 400 });
  }

  await db.item.create({ data: { name } });
  return redirect("/app/items");
};

export default function NewItemPage() {
  const actionData = useActionData<typeof action>();

  return (
    <form method="post">
      <s-text-field
        label="Name"
        name="name"
        error={actionData?.errors?.name}
        required
      />
      <s-button type="submit" variant="primary">Save</s-button>
    </form>
  );
}
```

## Best Practices

1. **Consistent Layouts** - Use the same page structure across the app
2. **Loading States** - Always show skeleton loaders during data fetching
3. **Empty States** - Provide clear guidance when no data exists
4. **Error Handling** - Show user-friendly error messages
5. **Form Validation** - Validate on submit, show inline errors
6. **Responsive Design** - Test on mobile, tablet, and desktop
7. **Accessibility** - Use semantic HTML and ARIA attributes
8. **SSR Compatibility** - Avoid hydration mismatches
9. **Performance** - Lazy load components when appropriate
10. **User Feedback** - Show success/error toasts after actions

---

**Remember**: Consistent UI patterns create a professional, predictable user experience.
