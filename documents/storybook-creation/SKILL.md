---
name: "storybook-creation"
description: "Creating Storybook documentation with proper stories, argTypes, model instances, and variations"
---

# Storybook Creation Skill

## Purpose

Create interactive documentation and examples for components using Storybook.

## Basic Template

```typescript
import { Store } from "@/models/store/Store";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { ComponentName } from "./ComponentName";

const meta: Meta<typeof ComponentName> = {
  title: "{Category}/Components/{Path}/ComponentName",
  component: ComponentName,
  argTypes: {
    // Type definitions here
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    // Default args
  },
};
```

## Title Categories

Use these categories for organizing stories:

- `Customer/Components/{path}` - Customer-facing components
- `Common/Components/{path}` - Shared components
- `Admin/Components/{path}` - Admin-specific components

Example paths:
```
"Customer/Components/Table/DataTable"
"Common/Components/Form/FormFieldText"
"Admin/Components/Dashboard/StatsCard"
```

## Creating Model Instances

Use Store to create model instances (snake_case model names):

```typescript
import { Store } from "@/models/store/Store";

// Correct - snake_case
const account = Store.account.create({
  id: "123",
  name: "Test Account",
  email: "test@example.com",
});

const organization = Store.organization.create({
  id: "456",
  name: "Test Org",
});

// Incorrect - not account_model
const account = Store.account_model.create({...}); // Wrong!
```

## Simple Component Story

```typescript
import type { Meta, StoryObj } from "@storybook/react-vite";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Common/Components/UI/Button",
  component: Button,
  argTypes: {
    variant: {
      control: "select",
      options: ["primary", "secondary", "outline", "ghost"],
    },
    size: {
      control: "select",
      options: ["sm", "default", "lg"],
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: "Click Me",
    variant: "primary",
    size: "default",
  },
};

export const Secondary: Story = {
  args: {
    children: "Secondary Button",
    variant: "secondary",
  },
};

export const Outline: Story = {
  args: {
    children: "Outline Button",
    variant: "outline",
  },
};
```

## Story with Model Data

```typescript
import { Store } from "@/models/store/Store";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { AssetCard } from "./AssetCard";

const meta: Meta<typeof AssetCard> = {
  title: "Customer/Components/Asset/AssetCard",
  component: AssetCard,
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    asset: Store.asset.create({
      id: "1",
      name: "Test Asset",
      description: "This is a test asset",
      status: 1,
      organization_id: "org-1",
    }),
  },
};

export const WithOrganization: Story = {
  args: {
    asset: Store.asset.create({
      id: "2",
      name: "Asset with Org",
      description: "Asset with organization data",
      status: 1,
      organization_id: "org-1",
      organization: Store.organization.create({
        id: "org-1",
        name: "Acme Corp",
      }),
    }),
  },
};
```

## Story with Render Function (Stateful)

Only use render when the component needs state updates:

```typescript
import { Store } from "@/models/store/Store";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { observer } from "mobx-react-lite";
import { AssetForm } from "./AssetForm";

const meta: Meta<typeof AssetForm> = {
  title: "Customer/Components/Asset/AssetForm",
  component: AssetForm,
};

export default meta;
type Story = StoryObj<typeof meta>;

export const CreateNew: Story = {
  render: () => {
    const asset = Store.asset.create({
      name: "",
      description: "",
      status: 1,
    });

    return <AssetForm asset={asset} />;
  },
};

export const EditExisting: Story = {
  render: () => {
    const asset = Store.asset.create({
      id: "123",
      name: "Existing Asset",
      description: "Edit this asset",
      status: 1,
    });

    return <AssetForm asset={asset} />;
  },
};
```

## ArgTypes Examples

```typescript
argTypes: {
  // String
  label: {
    control: "text",
    description: "Label text",
  },

  // Number
  size: {
    control: "number",
    description: "Size in pixels",
  },

  // Boolean
  disabled: {
    control: "boolean",
    description: "Whether the component is disabled",
  },

  // Select
  variant: {
    control: "select",
    options: ["primary", "secondary", "outline"],
    description: "Visual variant",
  },

  // Radio
  alignment: {
    control: "radio",
    options: ["left", "center", "right"],
  },

  // Color
  color: {
    control: "color",
  },

  // Date
  date: {
    control: "date",
  },

  // Range
  opacity: {
    control: { type: "range", min: 0, max: 1, step: 0.1 },
  },

  // Object
  config: {
    control: "object",
  },

  // Action (for callbacks)
  onClick: {
    action: "clicked",
  },
}
```

## What NOT to Include

1. **Don't add variants to the component** - Only create Storybook file
2. **Don't create mock services** - Use real Store methods
3. **Don't wrap with state unless asked** - Keep it simple
4. **Don't add implicit variations** - Only explicit prop variations
5. **Don't use Modal service** - Display component directly
6. **Don't handle loading states** unless asked

## Story Variations

Only create variations for:
- Explicit prop differences (primary vs secondary)
- Different data states (empty, with data, error)
- Meaningful visual differences
- Common use cases

Don't create variations for:
- className differences (not explicit)
- Generic styling changes
- Every possible prop combination

## Complete Example

```typescript
import { Store } from "@/models/store/Store";
import type { Meta, StoryObj } from "@storybook/react-vite";
import { DataTable } from "./DataTable";
import { assetColumns } from "./columns";
import { assetFilters } from "./filters";

const meta: Meta<typeof DataTable> = {
  title: "Common/Components/Table/DataTable",
  component: DataTable,
  argTypes: {
    showFilters: {
      control: "boolean",
      description: "Show filter panel",
    },
    showActions: {
      control: "boolean",
      description: "Show action buttons",
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const assets = [
  Store.asset.create({
    id: "1",
    name: "Asset One",
    description: "First asset",
    status: 1,
    organization_id: "org-1",
  }),
  Store.asset.create({
    id: "2",
    name: "Asset Two",
    description: "Second asset",
    status: 2,
    organization_id: "org-1",
  }),
];

export const Default: Story = {
  args: {
    data: assets,
    columns: assetColumns,
    showFilters: true,
    showActions: true,
  },
};

export const WithoutFilters: Story = {
  args: {
    data: assets,
    columns: assetColumns,
    showFilters: false,
    showActions: true,
  },
};

export const Empty: Story = {
  args: {
    data: [],
    columns: assetColumns,
    showFilters: true,
    showActions: true,
  },
};
```

## Key Rules

1. **Use Store for model creation** - `Store.{snake_case_model}.create()`
2. **Don't modify the component** - Only create Storybook file
3. **Use clear, descriptive story names** - Default, WithData, Empty, etc.
4. **Only add render when state is needed** - Most stories don't need it
5. **Organize by category** - Customer/Common/Admin
6. **Document argTypes** - Add descriptions for controls
7. **Create meaningful variations** - Not every possible combination
8. **Don't use mock services** - Use real Store/model instances
9. **Keep it simple** - Complexity should match component complexity

## Checklist Before Creating

- [ ] Is render function needed? (Only for stateful components)
- [ ] Are model instances using Store with snake_case?
- [ ] Are variations meaningful and explicit?
- [ ] Is the title categorized correctly?
- [ ] Are argTypes documented?
- [ ] Am I only creating the story file (not modifying component)?
