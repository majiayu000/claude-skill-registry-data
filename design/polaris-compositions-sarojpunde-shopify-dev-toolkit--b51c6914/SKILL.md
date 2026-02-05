---
name: polaris-compositions
description: Polaris composition patterns and page templates for common Shopify app layouts. Provides index tables, settings pages, dashboards, and resource management patterns. Auto-invoked when building page layouts.
allowed-tools: [Read, Grep, Glob]
documentation_path: ../../../polaris-web-components/patterns
---

# Polaris Compositions Skill

## Purpose
Provides complete page templates and composition patterns for common Shopify app layouts using Polaris Web Components.

## When This Skill Activates
- Creating new pages or views
- Building index/list pages
- Implementing settings interfaces
- Designing dashboards
- Creating resource management UIs

## Available Patterns

Reference: `polaris-web-components/patterns/compositions/`

### Composition Patterns

1. **App Card** - Application summary cards with actions
2. **Resource List** - Filterable, sortable resource lists
3. **Settings** - Settings page layouts with sections
4. **Callout Card** - Promotional or informational cards
5. **Account Connection** - Third-party service integrations
6. **Details** - Detailed information displays
7. **Index Table** - Data tables with bulk actions
8. **Metrics Card** - Statistics and KPI displays
9. **Setup Guide** - Onboarding checklists
10. **Homepage** - App homepage/dashboard layouts
11. **Sticky Pagination** - Persistent pagination controls
12. **Interstitial Nav** - Multi-step navigation flows
13. **Footer Help** - Contextual help sections
14. **Media Card** - Rich media content cards
15. **Empty State** - No content placeholders

## Complete Page Templates

### Index/List Page Template

**Use for**: Products, Orders, Customers, Collections

```tsx
<s-page
  heading="Products"
  primaryAction={{ content: "Add Product", url: "/products/new" }}
>
  {/* Stats Cards */}
  <s-section>
    <s-grid columns="1" md-columns="3" gap="400">
      <s-box border="base" borderRadius="base" padding="400">
        <s-stack gap="200" direction="vertical">
          <s-text variant="headingMd">Total Products</s-text>
          <s-text variant="heading2xl">{stats.total}</s-text>
        </s-stack>
      </s-box>

      <s-box border="base" borderRadius="base" padding="400">
        <s-stack gap="200" direction="vertical">
          <s-text variant="headingMd">Active</s-text>
          <s-text variant="heading2xl">{stats.active}</s-text>
          <s-badge tone="success">+12%</s-badge>
        </s-stack>
      </s-box>

      <s-box border="base" borderRadius="base" padding="400">
        <s-stack gap="200" direction="vertical">
          <s-text variant="headingMd">Draft</s-text>
          <s-text variant="heading2xl">{stats.draft}</s-text>
        </s-stack>
      </s-box>
    </s-grid>
  </s-section>

  {/* Filters */}
  <s-section>
    <s-card>
      <s-stack gap="300" alignment="space-between">
        <s-search-field
          placeholder="Search products..."
          value={searchQuery}
        />
        <s-select
          label="Status"
          options={[
            { label: "All", value: "all" },
            { label: "Active", value: "active" },
            { label: "Draft", value: "draft" },
          ]}
        />
      </s-stack>
    </s-card>
  </s-section>

  {/* Data Table */}
  <s-section>
    {products.length === 0 ? (
      <s-card>
        <s-empty-state
          heading="No products found"
          image="https://cdn.shopify.com/..."
        >
          <s-text>Try adjusting your filters or add a new product</s-text>
          <s-button variant="primary" url="/products/new">
            Add Product
          </s-button>
        </s-empty-state>
      </s-card>
    ) : (
      <s-card>
        <s-table>
          <s-table-head>
            <s-table-row>
              <s-table-cell as="th">Product</s-table-cell>
              <s-table-cell as="th">Status</s-table-cell>
              <s-table-cell as="th">Inventory</s-table-cell>
              <s-table-cell as="th">Price</s-table-cell>
              <s-table-cell as="th">Actions</s-table-cell>
            </s-table-row>
          </s-table-head>
          <s-table-body>
            {products.map(product => (
              <s-table-row key={product.id}>
                <s-table-cell>
                  <s-stack gap="200">
                    <s-thumbnail source={product.image} size="small" />
                    <s-text>{product.title}</s-text>
                  </s-stack>
                </s-table-cell>
                <s-table-cell>
                  <s-badge tone={product.active ? "success" : undefined}>
                    {product.active ? "Active" : "Draft"}
                  </s-badge>
                </s-table-cell>
                <s-table-cell>{product.inventory} in stock</s-table-cell>
                <s-table-cell>${product.price}</s-table-cell>
                <s-table-cell>
                  <s-button-group>
                    <s-button variant="plain" url={`/products/${product.id}`}>
                      Edit
                    </s-button>
                    <s-button variant="plain" tone="critical">
                      Delete
                    </s-button>
                  </s-button-group>
                </s-table-cell>
              </s-table-row>
            ))}
          </s-table-body>
        </s-table>

        {/* Pagination */}
        <s-box padding="400">
          <s-stack gap="200" alignment="center">
            <s-button disabled={page === 1}>Previous</s-button>
            <s-text>Page {page} of {totalPages}</s-text>
            <s-button disabled={page === totalPages}>Next</s-button>
          </s-stack>
        </s-box>
      </s-card>
    )}
  </s-section>
</s-page>
```

### Settings Page Template

```tsx
<s-page heading="Settings">
  {/* General Settings */}
  <s-section>
    <s-card>
      <s-stack gap="400" direction="vertical">
        <s-heading>General</s-heading>

        <s-text-field
          label="Store Name"
          value={settings.storeName}
          helpText="This appears in your emails and online store"
        />

        <s-text-field
          label="Contact Email"
          type="email"
          value={settings.contactEmail}
        />

        <s-text-field
          label="Customer Support Email"
          type="email"
          value={settings.supportEmail}
        />
      </s-stack>
    </s-card>
  </s-section>

  {/* Notifications */}
  <s-section>
    <s-card>
      <s-stack gap="400" direction="vertical">
        <s-heading>Notifications</s-heading>
        <s-text tone="subdued">
          Choose which notifications you want to receive
        </s-text>

        <s-divider />

        <s-checkbox
          label="Email notifications"
          checked={settings.emailNotifications}
          helpText="Receive updates via email"
        />

        <s-checkbox
          label="Order notifications"
          checked={settings.orderNotifications}
          helpText="Get notified about new orders"
        />

        <s-checkbox
          label="Customer messages"
          checked={settings.customerMessages}
          helpText="Receive customer inquiries"
        />
      </s-stack>
    </s-card>
  </s-section>

  {/* Advanced Settings */}
  <s-section>
    <s-card>
      <s-stack gap="400" direction="vertical">
        <s-heading>Advanced</s-heading>

        <s-banner tone="warning">
          <s-text>
            These settings can affect your store's functionality.
            Change with caution.
          </s-text>
        </s-banner>

        <s-divider />

        <s-checkbox
          label="Enable API access"
          checked={settings.apiEnabled}
        />

        <s-checkbox
          label="Debug mode"
          checked={settings.debugMode}
        />
      </s-stack>
    </s-card>
  </s-section>

  {/* Save Section */}
  <s-section>
    <s-stack gap="300" alignment="trailing">
      <s-button>Reset to Defaults</s-button>
      <s-button variant="primary">Save Settings</s-button>
    </s-stack>
  </s-section>
</s-page>
```

### Dashboard/Homepage Template

```tsx
<s-page heading="Dashboard">
  {/* Welcome Message */}
  <s-section>
    <s-banner tone="info">
      <s-stack gap="200" direction="vertical">
        <s-text variant="headingMd">Welcome back!</s-text>
        <s-text>
          You have 3 orders to fulfill and 2 customer messages.
        </s-text>
      </s-stack>
    </s-banner>
  </s-section>

  {/* Key Metrics */}
  <s-section>
    <s-grid columns="1" md-columns="2" lg-columns="4" gap="400">
      <s-box border="base" borderRadius="base" padding="400">
        <s-stack gap="200" direction="vertical">
          <s-text variant="headingMd">Today's Sales</s-text>
          <s-text variant="heading2xl">$2,453</s-text>
          <s-badge tone="success">+15% from yesterday</s-badge>
        </s-stack>
      </s-box>

      <s-box border="base" borderRadius="base" padding="400">
        <s-stack gap="200" direction="vertical">
          <s-text variant="headingMd">Orders</s-text>
          <s-text variant="heading2xl">34</s-text>
          <s-badge>5 pending</s-badge>
        </s-stack>
      </s-box>

      <s-box border="base" borderRadius="base" padding="400">
        <s-stack gap="200" direction="vertical">
          <s-text variant="headingMd">Conversion Rate</s-text>
          <s-text variant="heading2xl">3.2%</s-text>
          <s-badge tone="success">+0.3%</s-badge>
        </s-stack>
      </s-box>

      <s-box border="base" borderRadius="base" padding="400">
        <s-stack gap="200" direction="vertical">
          <s-text variant="headingMd">Average Order</s-text>
          <s-text variant="heading2xl">$72.15</s-text>
          <s-badge tone="warning">-2%</s-badge>
        </s-stack>
      </s-box>
    </s-grid>
  </s-section>

  {/* Quick Actions */}
  <s-section>
    <s-grid columns="1" md-columns="3" gap="400">
      <s-card>
        <s-stack gap="300" direction="vertical">
          <s-heading>Orders</s-heading>
          <s-text tone="subdued">5 orders need fulfillment</s-text>
          <s-button url="/orders">Manage Orders</s-button>
        </s-stack>
      </s-card>

      <s-card>
        <s-stack gap="300" direction="vertical">
          <s-heading>Products</s-heading>
          <s-text tone="subdued">3 products low in stock</s-text>
          <s-button url="/products">View Inventory</s-button>
        </s-stack>
      </s-card>

      <s-card>
        <s-stack gap="300" direction="vertical">
          <s-heading>Customers</s-heading>
          <s-text tone="subdued">2 messages waiting</s-text>
          <s-button url="/customers">View Messages</s-button>
        </s-stack>
      </s-card>
    </s-grid>
  </s-section>

  {/* Recent Activity */}
  <s-section>
    <s-card>
      <s-stack gap="400" direction="vertical">
        <s-heading>Recent Orders</s-heading>
        <s-table>
          <s-table-head>
            <s-table-row>
              <s-table-cell as="th">Order</s-table-cell>
              <s-table-cell as="th">Customer</s-table-cell>
              <s-table-cell as="th">Total</s-table-cell>
              <s-table-cell as="th">Status</s-table-cell>
            </s-table-row>
          </s-table-head>
          <s-table-body>
            {recentOrders.map(order => (
              <s-table-row key={order.id}>
                <s-table-cell>#{order.number}</s-table-cell>
                <s-table-cell>{order.customer}</s-table-cell>
                <s-table-cell>${order.total}</s-table-cell>
                <s-table-cell>
                  <s-badge tone={order.fulfilled ? "success" : "warning"}>
                    {order.fulfilled ? "Fulfilled" : "Pending"}
                  </s-badge>
                </s-table-cell>
              </s-table-row>
            ))}
          </s-table-body>
        </s-table>
      </s-stack>
    </s-card>
  </s-section>
</s-page>
```

## Pattern Components Reference

For detailed pattern documentation, see:
- `polaris-web-components/patterns/compositions/` - All composition patterns
- `polaris-web-components/patterns/templates/` - Complete page templates

### Quick Pattern Reference

| Pattern | File | Use Case |
|---------|------|----------|
| Index Table | `index-table.md` | Product lists, order lists |
| Settings | `settings.md` | App configuration pages |
| Homepage | `homepage.md` | Dashboard layouts |
| Empty State | `empty-state.md` | No content states |
| Metrics Card | `metrics-card.md` | KPI displays |
| Resource List | `resource-list.md` | Filterable lists |
| Setup Guide | `setup-guide.md` | Onboarding flows |

## Best Practices

1. **Follow Templates** - Use established templates for common pages
2. **Consistent Layout** - Maintain consistent structure across pages
3. **Progressive Disclosure** - Show advanced options only when needed
4. **Clear Hierarchy** - Use sections to organize content logically
5. **Actionable CTAs** - Make primary actions obvious
6. **Empty States** - Always provide guidance when no data exists
7. **Loading States** - Show skeletons during data fetch
8. **Error Handling** - Display clear, actionable error messages
9. **Mobile Responsive** - All patterns work on mobile devices
10. **Accessibility** - Ensure keyboard navigation and screen readers work

---

**Remember**: Using established patterns improves UX consistency and reduces development time.
