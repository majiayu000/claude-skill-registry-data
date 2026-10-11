---
name: antd
description: Ant Design — enterprise React UI with forms, tables; official MCP.
---

## Detection Signals

- `antd` in `package.json`
- `@ant-design/icons` dependency
- `ConfigProvider` at app root
- `@ant-design/pro-components` (ProTable, ProForm) in larger projects
- `dayjs` for date components (antd v5 dropped moment.js)

## MCP Setup

Ant Design has an official MCP server with real-time documentation, code examples, and API references.

**Add to `.claude/settings.json`**:

```json
{
  "mcpServers": {
    "antd": {
      "command": "npx",
      "args": ["-y", "@ant-design/mcp@latest"]
    }
  }
}
```

> If auto-configuration fails, ask the user to add the entry manually in their CLI's MCP settings (**Claude Code → Settings → MCP Servers**, the `mcp` block of `opencode.json`, or Codex CLI's MCP config), or run `npm install -g @ant-design/cli` and use `antd mcp` as the command.

## Core Concepts

| Concept | Detail |
|---------|--------|
| **ConfigProvider** | Global config: locale, theme tokens, component defaults |
| **Design tokens** | Theme via `theme.token` and `theme.components` in ConfigProvider |
| **Form + `useForm`** | Built-in validation, async rules, field state management |
| **Table** | Column definitions, `dataSource`, `rowKey`, pagination, sort, filter |
| **ProComponents** | `@ant-design/pro-components` — high-level ProTable, ProForm for CRUD |
| **Tree-shaking** | Import from individual paths or use with a bundler that supports it |

## Component Patterns

```tsx
// ConfigProvider is mandatory — without it, some labels default to Chinese
import { ConfigProvider } from 'antd'
import enUS from 'antd/locale/en_US'

<ConfigProvider locale={enUS} theme={{ token: { colorPrimary: '#1677ff' } }}>
  <App />
</ConfigProvider>

// Form — always use Form.useForm(); never manage field state manually
const [form] = Form.useForm()
<Form form={form} onFinish={handleSubmit} layout="vertical">
  <Form.Item name="email" rules={[{ required: true, type: 'email' }]}>
    <Input />
  </Form.Item>
  <Button htmlType="submit">Submit</Button>
</Form>

// Table — define columns separately for readability
const columns = [
  { title: 'Name', dataIndex: 'name', sorter: true },
  { title: 'Status', dataIndex: 'status', filters: [...] },
]
<Table columns={columns} dataSource={data} rowKey="id" />
```

## Critical Rules

- **ConfigProvider at root** — without locale config, date pickers and some labels render in Chinese
- **Always use `Form.useForm()`** — never build form state manually alongside antd Form; the two fight each other
- **Use `dayjs`**, not `moment` — antd v5 migrated; importing moment causes peer dep warnings and bundle bloat
- **Import selectively** — `import { Button } from 'antd'` is fine with tree-shaking; avoid importing everything
- **ProComponents for complex CRUD** — if `@ant-design/pro-components` is present, prefer ProTable/ProForm over building custom table+form combos
- **Theme via tokens** — customize through `ConfigProvider`'s `theme` prop, not CSS overrides; token changes cascade automatically
