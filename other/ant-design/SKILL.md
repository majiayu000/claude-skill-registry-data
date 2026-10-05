---
name: ant-design
description: Use when ant Design React component library — enterprise UI, forms, tables,
  charts, theming, ProComponents. Use when working with ant design.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- ant
- content-creation
- design
- digital-content
- media
version: 1.0.0
category: content
---




## Overview

Ant Design is an enterprise-grade React UI library with 60+ components, a design system, and ProComponents for advanced business scenarios. Widely used for admin dashboards, CMS, and data-heavy applications.

## Capabilities

- 60+ polished components with consistent design language
- ConfigProvider for global theming (colors, locale, prefixCls)
- Form component with validation, dependencies, dynamic fields
- Table with sorting, filtering, pagination, virtual scroll
- ProComponents: ProTable, ProForm, ProLayout, ProDescriptions
- Day.js integration for date components
- Ant Design Icons (300+)

## When to Use
**Trigger phrases:**
- "ant design"
- "Ant Design React component library — enterprise UI, forms, tables, charts, themi"


- Building enterprise admin dashboards and CMS
- Need advanced form handling with complex validation
- Want a complete design system with minimal customization
- Building data-heavy applications with tables, charts, filters

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The ant-design workflow follows a standard pipeline pattern.

Core flow:
```
# ant-design primary flow
input = prepare(raw_data)
result = process(input, config={ant, charts, component, design, enterprise})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# ant-design primary flow
input = prepare(raw_data)
result = process(input, config={ant, charts, component, design, enterprise})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Installation
```bash
npm install antd @ant-design/icons
# ProComponents for advanced patterns
npm install @ant-design/pro-components
```

### Theme Configuration
```tsx
import { ConfigProvider } from "antd"

function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#1677ff",
          borderRadius: 6,
          fontFamily: "Inter, sans-serif",
        },
      }}
    >
      <YourApp />
    </ConfigProvider>
  )
}
```

### Form with Validation
```tsx
import { Form, Input, Select, Button, message } from "antd"

export function UserForm() {
  const [form] = Form.useForm()
  const onFinish = (values) => {
    message.success("Saved!")
    console.log(values)
  }

  return (
    <Form form={form} layout="vertical" onFinish={onFinish}>
      <Form.Item name="name" label="Name" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Form.Item name="role" label="Role" rules={[{ required: true }]}>
        <Select options={[{ value: "admin" }, { value: "user" }]} />
      </Form.Item>
      <Button type="primary" htmlType="submit">Save</Button>
    </Form>
  )
}
```

### ProTable
```tsx
import { ProTable } from "@ant-design/pro-components"

const columns = [
  { title: "Name", dataIndex: "name", sorter: true },
  { title: "Status", dataIndex: "status", valueEnum: { active: "Active", inactive: "Inactive" } },
  { title: "Created", dataIndex: "createdAt", valueType: "date" },
]

export function UserTable() {
  return (
    <ProTable
      columns={columns}
      request={async (params) => {
        const data = await fetchUsers(params)
        return { data: data.list, total: data.total }
      }}
      search={{ labelWidth: "auto" }}
      pagination={{ pageSize: 20 }}
    />
  )
}
```

## Common Patterns

- **ConfigProvider locale**: `<ConfigProvider locale={zhCN}>` for i18n
- **Form dependencies**: `shouldUpdate={(prev, cur) => prev.field !== cur.field}` for conditional fields
- **Table virtual scroll**: `virtual` prop for 1000+ row performance
- **message/notification**: `message.success()`, `notification.error()` for feedback
- **Responsive Grid**: `<Row gutter={[16, 16]}><Col xs={24} md={12}>...</Col></Row>`

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |