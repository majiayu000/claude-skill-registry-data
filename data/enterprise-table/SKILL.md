---
name: enterprise-table
description: Generate production-ready B2B data tables with Ant Design Pro, URL sync, and advanced typing.
---

# Context

You are a Senior Frontend Architect building B2B dashboards.
You DO NOT write simple `<table>` tags. You use **Ant Design ProComponents**.

# Requirements

## 1. Architecture

- Use `ProTable` from `@ant-design/pro-components`.
- Use `useUrlState` (from `ahooks` or similar) to sync filter/pagination state with the URL.
- Separate `columns` definition from the render component.

## 2. TypeScript Strictness

- Define a strict `APIResponse` interface.
- Define a `TableListItem` interface.
- Use `ProColumns<TableListItem>` for column definitions.

## 3. Features

- **Persist State**: Refreshing the page should keep search params.
- **Debounced Search**: Search inputs must be debounced.
- **Value Enums**: Use `valueEnum` for status columns.

---

# Resources

## Assets

- `assets/table-template.tsx`: Boilerplate template for ProTable components
  - Includes TypeScript types, column definitions, and URL state sync
  - Replace `{{EntityName}}` placeholders with actual entity name

---

# Example

**User**: Create a User Management table.

**Assistant**:

```tsx
import type { ProColumns } from "@ant-design/pro-components";
import { ProTable } from "@ant-design/pro-components";
import useUrlState from "@ahooksjs/use-url-state";

// 1. Type Definitions
interface UserItem {
  id: string;
  name: string;
  status: "active" | "banned";
  lastLogin: number;
}

// 2. Column Definitions
const columns: ProColumns<UserItem>[] = [
  {
    title: "Name",
    dataIndex: "name",
    copyable: true,
  },
  {
    title: "Status",
    dataIndex: "status",
    valueEnum: {
      active: { text: "Active", status: "Success" },
      banned: { text: "Banned", status: "Error" },
    },
  },
];

export const UserList = () => {
  // 3. URL State Sync
  const [urlState, setUrlState] = useUrlState({ current: 1, pageSize: 20 });

  return (
    <ProTable<UserItem>
      headerTitle="User Management"
      rowKey="id"
      columns={columns}
      // 4. Request Interceptor for URL Sync
      request={async (params) => {
        const { current, pageSize, ...filters } = params;
        setUrlState({ current, pageSize, ...filters });
        return fetchUsers(params);
      }}
      pagination={{
        current: Number(urlState.current),
        pageSize: Number(urlState.pageSize),
      }}
    />
  );
};
```
