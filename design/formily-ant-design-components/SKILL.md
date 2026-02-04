---
name: Formily Ant Design Components
description: This skill should be used when the user asks to "use formily with ant design", "formily antd components", "formily ant design integration", "formily form layout", "formily form.item", "formily antd forms", or "integrate formily with ant design".
version: 1.0.0
---

# Formily Ant Design Components

This skill provides comprehensive guidance for integrating Formily with Ant Design components. Focus on form layouts, field components, validation, and common patterns when using Formily with Ant Design in TypeScript.

## Installation

Install Formily Ant Design packages:

```bash
npm install @formily/antd @formily/core @formily/react
npm install antd
```

Install required types for TypeScript:

```bash
npm install -D @types/react @types/react-dom
```

## Basic Setup

Configure Formily with Ant Design:

```typescript
import React from 'react'
import { createForm } from '@formily/core'
import { FormProvider, createSchemaField } from '@formily/react'
import { Form, FormItem, Input, Select, DatePicker } from '@formily/antd'

// Create schema field component
const SchemaField = createSchemaField({
  components: {
    Form,
    FormItem,
    Input,
    Select,
    DatePicker
  }
})

// Create form instance
const form = createForm()
```

## Form Layout Patterns

### Basic Form Layout

```typescript
import { Form } from '@formily/antd'

const BasicForm = () => {
  return (
    <Form form={form} labelCol={6} wrapperCol={16}>
      {/* Form fields */}
    </Form>
  )
}
```

### Grid Layout

```typescript
import { Form } from '@formily/antd'
import { Row, Col } from 'antd'

const GridLayout = () => {
  return (
    <Form form={form}>
      <Row gutter={16}>
        <Col span={12}>
          <SchemaField name="firstName">
            <FormItem label="First Name">
              <Input placeholder="Enter first name" />
            </FormItem>
          </SchemaField>
        </Col>
        <Col span={12}>
          <SchemaField name="lastName">
            <FormItem label="Last Name">
              <Input placeholder="Enter last name" />
            </FormItem>
          </SchemaField>
        </Col>
      </Row>
    </Form>
  )
}
```

### Tabs Layout

```typescript
import { Form } from '@formily/antd'
import { Tabs } from 'antd'

const { TabPane } = Tabs

const TabsLayout = () => {
  return (
    <Form form={form}>
      <Tabs defaultActiveKey="basic">
        <TabPane tab="Basic Info" key="basic">
          <SchemaField name="name">
            <FormItem label="Name">
              <Input />
            </FormItem>
          </SchemaField>
        </TabPane>
        <TabPane tab="Advanced" key="advanced">
          <SchemaField name="settings">
            <FormItem label="Settings">
              <Input />
            </FormItem>
          </SchemaField>
        </TabPane>
      </Tabs>
    </Form>
  )
}
```

## Common Ant Design Components

### Input Components

```typescript
// Text Input
<SchemaField name="username">
  <FormItem label="Username">
    <Input
      placeholder="Enter username"
      prefix={<UserOutlined />}
    />
  </FormItem>
</SchemaField>

// Password Input
<SchemaField name="password">
  <FormItem label="Password">
    <Input.Password
      placeholder="Enter password"
      visibilityToggle
    />
  </FormItem>
</SchemaField>

// Textarea
<SchemaField name="description">
  <FormItem label="Description">
    <Input.TextArea
      rows={4}
      placeholder="Enter description"
      showCount
      maxLength={500}
    />
  </FormItem>
</SchemaField>
```

### Select Components

```typescript
// Basic Select
<SchemaField name="country">
  <FormItem label="Country">
    <Select placeholder="Select country">
      <Select.Option value="us">United States</Select.Option>
      <Select.Option value="uk">United Kingdom</Select.Option>
      <Select.Option value="ca">Canada</Select.Option>
    </Select>
  </FormItem>
</SchemaField>

// Multi Select
<SchemaField name="skills">
  <FormItem label="Skills">
    <Select
      mode="multiple"
      placeholder="Select skills"
      options={[
        { label: 'JavaScript', value: 'js' },
        { label: 'TypeScript', value: 'ts' },
        { label: 'React', value: 'react' }
      ]}
    />
  </FormItem>
</SchemaField>

// Searchable Select
<SchemaField name="city">
  <FormItem label="City">
    <Select
      showSearch
      placeholder="Search city"
      filterOption={(input, option) =>
        option?.children.toLowerCase().includes(input.toLowerCase())
      }
    >
      <Select.Option value="nyc">New York</Select.Option>
      <Select.Option value="la">Los Angeles</Select.Option>
      <Select.Option value="chi">Chicago</Select.Option>
    </Select>
  </FormItem>
</SchemaField>
```

### Date and Time Components

```typescript
import { DatePicker, TimePicker, RangePicker } from '@formily/antd'

// Date Picker
<SchemaField name="birthDate">
  <FormItem label="Birth Date">
    <DatePicker
      style={{ width: '100%' }}
      format="YYYY-MM-DD"
    />
  </FormItem>
</SchemaField>

// Date Range Picker
<SchemaField name="dateRange">
  <FormItem label="Date Range">
    <RangePicker
      style={{ width: '100%' }}
      format="YYYY-MM-DD"
    />
  </FormItem>
</SchemaField>

// Time Picker
<SchemaField name="appointmentTime">
  <FormItem label="Appointment Time">
    <TimePicker
      style={{ width: '100%' }}
      format="HH:mm"
    />
  </FormItem>
</SchemaField>
```

### Checkbox and Radio Components

```typescript
// Single Checkbox
<SchemaField name="agreeToTerms">
  <FormItem>
    <Checkbox>
      I agree to the terms and conditions
    </Checkbox>
  </FormItem>
</SchemaField>

// Checkbox Group
<SchemaField name="interests">
  <FormItem label="Interests">
    <Checkbox.Group>
      <Checkbox value="sports">Sports</Checkbox>
      <Checkbox value="music">Music</Checkbox>
      <Checkbox value="travel">Travel</Checkbox>
    </Checkbox.Group>
  </FormItem>
</SchemaField>

// Radio Group
<SchemaField name="gender">
  <FormItem label="Gender">
    <Radio.Group>
      <Radio value="male">Male</Radio>
          <Radio value="female">Female</Radio>
          <Radio value="other">Other</Radio>
        </Radio.Group>
      </FormItem>
    </SchemaField>
```

### Number Input

```typescript
import { InputNumber } from '@formily/antd

<SchemaField name="age">
  <FormItem label="Age">
    <InputNumber
      style={{ width: '100%' }}
      min={0}
      max={120}
      placeholder="Enter age"
    />
  </FormItem>
</SchemaField>

<SchemaField name="price">
  <FormItem label="Price">
    <InputNumber
      style={{ width: '100%' }}
      min={0}
      precision={2}
      prefix="$"
      placeholder="0.00"
    />
  </FormItem>
</SchemaField>
```

### Switch and Slider

```typescript
import { Switch, Slider } from '@formily/antd

// Switch
<SchemaField name="notifications">
  <FormItem label="Email Notifications">
    <Switch />
  </FormItem>
</SchemaField>

// Slider
<SchemaField name="volume">
  <FormItem label="Volume">
    <Slider
      min={0}
      max={100}
      marks={{
        0: '0',
        50: '50',
        100: '100'
      }}
    />
  </FormItem>
</SchemaField>
```

## Form Validation with Ant Design

### Built-in Validation

```typescript
const form = createForm({
  schema: {
    type: 'object',
    properties: {
      email: {
        type: 'string',
        title: 'Email',
        'x-decorator': 'FormItem',
        'x-component': 'Input',
        'x-validator': [
          { required: true, message: 'Email is required' },
          { format: 'email', message: 'Invalid email format' }
        ]
      },
      password: {
        type: 'string',
        title: 'Password',
        'x-decorator': 'FormItem',
        'x-component': 'Input.Password',
        'x-validator': [
          { required: true, message: 'Password is required' },
          { min: 8, message: 'Password must be at least 8 characters' }
        ]
      }
    }
  }
})
```

### Custom Validation Messages

```typescript
const validationSchema = {
  username: {
    required: true,
    message: 'Username is required'
  },
  email: {
    type: 'email',
    message: 'Please enter a valid email address'
  },
  phone: {
    pattern: /^[0-9]{10}$/,
    message: 'Phone number must be 10 digits'
  }
}
```

## Schema-Driven Forms

### Complete Schema Example

```typescript
import React from 'react'
import { createForm } from '@formily/core'
import { FormProvider, createSchemaField } from '@formily/react'
import { Form, FormItem, Input, Select, DatePicker, Button } from '@formily/antd'

const schema = {
  type: 'object',
  properties: {
    basicInfo: {
      type: 'object',
      title: 'Basic Information',
      'x-decorator': 'FormItem',
      'x-component': 'Card',
      properties: {
        firstName: {
          type: 'string',
          title: 'First Name',
          'x-decorator': 'FormItem',
          'x-component': 'Input',
          'x-validator': [{ required: true, message: 'Required' }]
        },
        lastName: {
          type: 'string',
          title: 'Last Name',
          'x-decorator': 'FormItem',
          'x-component': 'Input',
          'x-validator': [{ required: true, message: 'Required' }]
        },
        email: {
          type: 'string',
          title: 'Email',
          'x-decorator': 'FormItem',
          'x-component': 'Input',
          'x-validator': [
            { required: true, message: 'Required' },
            { format: 'email', message: 'Invalid email' }
          ]
        },
        birthDate: {
          type: 'string',
          title: 'Birth Date',
          'x-decorator': 'FormItem',
          'x-component': 'DatePicker'
        }
      }
    },
    preferences: {
      type: 'object',
      title: 'Preferences',
      'x-decorator': 'FormItem',
      'x-component': 'Card',
      properties: {
        language: {
          type: 'string',
          title: 'Language',
          'x-decorator': 'FormItem',
          'x-component': 'Select',
          'x-component-props': {
            options: [
              { label: 'English', value: 'en' },
              { label: 'Spanish', value: 'es' },
              { label: 'French', value: 'fr' }
            ]
          }
        },
        timezone: {
          type: 'string',
          title: 'Timezone',
          'x-decorator': 'FormItem',
          'x-component': 'Select',
          'x-component-props': {
            showSearch: true,
            options: [
              { label: 'UTC-8 (PST)', value: 'utc-8' },
              { label: 'UTC-5 (EST)', value: 'utc-5' },
              { label: 'UTC+0 (GMT)', value: 'utc-0' }
            ]
          }
        }
      }
    }
  }
}

const SchemaForm = () => {
  const form = createForm()
  const SchemaField = createSchemaField({
    components: {
      Form,
      FormItem,
      Input,
      Select,
      DatePicker,
      Card,
      Button
    }
  })

  return (
    <FormProvider form={form}>
      <Form labelCol={6} wrapperCol={16}>
        <SchemaField schema={schema} />
        <Form.Item wrapperCol={{ offset: 6, span: 16 }}>
          <Button type="primary" onClick={() => form.submit()}>
            Submit
          </Button>
        </Form.Item>
      </Form>
    </FormProvider>
  )
}
```

## Form Actions

### Submit and Reset

```typescript
import { Button, Space } from 'antd'

const FormActions = () => {
  const handleSubmit = async () => {
    try {
      await form.validate()
      const values = form.values
      console.log('Form submitted:', values)
    } catch (errors) {
      console.error('Validation errors:', errors)
    }
  }

  const handleReset = () => {
    form.reset()
  }

  return (
    <Form.Item wrapperCol={{ offset: 6, span: 16 }}>
      <Space>
        <Button type="primary" onClick={handleSubmit}>
          Submit
        </Button>
        <Button onClick={handleReset}>
          Reset
        </Button>
      </Space>
    </Form.Item>
  )
}
```

## Advanced Patterns

### Dynamic Form Sections

```typescript
const DynamicForm = () => {
  const form = createForm({
    effects: () => {
      onFieldChange('hasExperience', ['value'], (field) => {
        form.setFieldState('experienceDetails', state => {
          state.display = field.value
        })
      })
    }
  })

  return (
    <Form form={form}>
      <SchemaField name="hasExperience">
        <FormItem>
          <Checkbox>Has relevant experience</Checkbox>
        </FormItem>
      </SchemaField>

      <SchemaField name="experienceDetails" style={{ display: 'none' }}>
        <FormItem label="Experience Details">
          <Input.TextArea rows={4} />
        </FormItem>
      </SchemaField>
    </Form>
  )
}
```

### Array Fields

```typescript
import { ArrayCards } from '@formily/antd

const ArrayForm = () => {
  const schema = {
    type: 'object',
    properties: {
      contacts: {
        type: 'array',
        title: 'Emergency Contacts',
        'x-decorator': 'FormItem',
        'x-component': 'ArrayCards',
        'x-component-props': {
          title: 'Contact',
          addition: 'Add Contact'
        },
        items: {
          type: 'object',
          properties: {
            name: {
              type: 'string',
              title: 'Name',
              'x-decorator': 'FormItem',
              'x-component': 'Input'
            },
            phone: {
              type: 'string',
              title: 'Phone',
              'x-decorator': 'FormItem',
              'x-component': 'Input'
            },
            relationship: {
              type: 'string',
              title: 'Relationship',
              'x-decorator': 'FormItem',
              'x-component': 'Select',
              'x-component-props': {
                options: [
                  { label: 'Parent', value: 'parent' },
                  { label: 'Sibling', value: 'sibling' },
                  { label: 'Spouse', value: 'spouse' }
                ]
              }
            }
          }
        }
      }
    }
  }

  const SchemaField = createSchemaField({
    components: {
      Form,
      FormItem,
      Input,
      Select,
      ArrayCards
    }
  })

  return (
    <FormProvider form={form}>
      <Form>
        <SchemaField schema={schema} />
      </Form>
    </FormProvider>
  )
}
```

## Additional Resources

### Example Files
- **`examples/antd-form-layouts.tsx`** - Complete form layout examples
- **`examples/validation-patterns.tsx`** - Advanced validation patterns

### Reference Files
- **`references/component-mapping.md`** - Ant Design component mapping reference
- **`references/styling-guide.md`** - Form styling and theming guide

### Common Ant Design Components
- Input, Input.Password, Input.TextArea
- Select, Select.OptGroup
- DatePicker, DatePicker.RangePicker, TimePicker
- Checkbox, Checkbox.Group
- Radio, Radio.Group, Radio.Button
- Switch, Slider, InputNumber
- Upload, Rate, Mentions

## Best Practices

1. **Use consistent spacing** with `labelCol` and `wrapperCol` props
2. **Group related fields** using Card or Divider components
3. **Provide clear labels and placeholders** for better UX
4. **Use proper validation messages** that guide users
5. **Leverage Form.Item** for consistent label positioning and error display
6. **Use Grid system** for complex multi-column layouts
7. **Implement loading states** for async operations
8. **Test responsive behavior** on different screen sizes