---
name: Formily Migration Guide
description: This skill should be used when the user asks to "convert to formily", "formily migration", "migrate forms to formily", "convert react forms to formily", "formily vs other form libraries", or "replace existing forms with formily".
version: 1.0.0
---

# Formily Migration Guide

This skill provides comprehensive guidance for converting existing React forms to Formily. Focus on migration strategies, common patterns, and step-by-step conversion processes for different form libraries and vanilla React forms with TypeScript.

## Migration Overview

### Why Migrate to Formily?

1. **Better TypeScript support** - Type-safe form management
2. **Schema-driven approach** - Declarative form definitions
3. **Improved performance** - Efficient reactivity and minimal re-renders
4. **Powerful validation** - Built-in validation with custom rules
5. **Better developer experience** - Less boilerplate, more maintainability

### Migration Strategies

1. **Incremental migration** - Convert forms one at a time
2. **Parallel development** - Build new forms with Formily while maintaining existing ones
3. **Complete rewrite** - Replace entire form system at once

## From Vanilla React Forms

### Before: Vanilla React Form

```typescript
import React, { useState, FormEvent } from 'react'

interface ContactForm {
  name: string
  email: string
  message: string
}

const VanillaContactForm: React.FC = () => {
  const [formData, setFormData] = useState<ContactForm>({
    name: '',
    email: '',
    message: ''
  })

  const [errors, setErrors] = useState<Partial<ContactForm>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    // Clear error when user starts typing
    if (errors[name as keyof ContactForm]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Partial<ContactForm> = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required'
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format'
    }

    if (!formData.message.trim()) {
      newErrors.message = 'Message is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()

    if (!validateForm()) {
      return
    }

    setIsSubmitting(true)

    try {
      // Submit form data
      await submitForm(formData)
      alert('Form submitted successfully!')
      setFormData({ name: '', email: '', message: '' })
    } catch (error) {
      console.error('Submission error:', error)
      alert('Submission failed. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name:</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
        />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>

      <div>
        <label>Email:</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div>
        <label>Message:</label>
        <textarea
          name="message"
          value={formData.message}
          onChange={handleChange}
        />
        {errors.message && <span className="error">{errors.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  )
}
```

### After: Formily Version

```typescript
import React from 'react'
import { createForm } from '@formily/core'
import { FormProvider, createSchemaField } from '@formily/react'
import { Form, FormItem, Input, Button } from '@formily/antd'

interface ContactForm {
  name: string
  email: string
  message: string
}

const FormilyContactForm: React.FC = () => {
  const form = createForm<ContactForm>({
    initialValues: {
      name: '',
      email: '',
      message: ''
    },
    validateFirst: true
  })

  const schema = {
    type: 'object',
    properties: {
      name: {
        type: 'string',
        title: 'Name',
        required: true,
        'x-decorator': 'FormItem',
        'x-component': 'Input',
        'x-validator': [
          { required: true, message: 'Name is required' }
        ]
      },
      email: {
        type: 'string',
        title: 'Email',
        required: true,
        'x-decorator': 'FormItem',
        'x-component': 'Input',
        'x-validator': [
          { required: true, message: 'Email is required' },
          { format: 'email', message: 'Invalid email format' }
        ]
      },
      message: {
        type: 'string',
        title: 'Message',
        required: true,
        'x-decorator': 'FormItem',
        'x-component': 'Input.TextArea',
        'x-validator': [
          { required: true, message: 'Message is required' }
        ]
      }
    }
  }

  const SchemaField = createSchemaField({
    components: {
      Form,
      FormItem,
      Input,
      Button
    }
  })

  const handleSubmit = async () => {
    try {
      await form.validate()
      const values = form.values
      await submitForm(values)
      alert('Form submitted successfully!')
      form.reset()
    } catch (error) {
      console.error('Validation errors:', error)
    }
  }

  return (
    <FormProvider form={form}>
      <Form labelCol={6} wrapperCol={16}>
        <SchemaField schema={schema} />
        <FormItem wrapperCol={{ offset: 6, span: 16 }}>
          <Button type="primary" onClick={handleSubmit}>
            Submit
          </Button>
        </FormItem>
      </Form>
    </FormProvider>
  )
}
```

## From Formik

### Before: Formik Form

```typescript
import React from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'

const FormikExample: React.FC = () => {
  const initialValues = {
    firstName: '',
    lastName: '',
    email: '',
    age: ''
  }

  const validationSchema = Yup.object({
    firstName: Yup.string().required('First name is required'),
    lastName: Yup.string().required('Last name is required'),
    email: Yup.string().email('Invalid email').required('Email is required'),
    age: Yup.number().min(18, 'Must be at least 18').required('Age is required')
  })

  const handleSubmit = (values: any, { setSubmitting }: any) => {
    submitForm(values)
    setSubmitting(false)
  }

  return (
    <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={handleSubmit}
    >
      {({ isSubmitting }) => (
        <Form>
          <div>
            <label>First Name</label>
            <Field name="firstName" type="text" />
            <ErrorMessage name="firstName" component="div" />
          </div>

          <div>
            <label>Last Name</label>
            <Field name="lastName" type="text" />
            <ErrorMessage name="lastName" component="div" />
          </div>

          <div>
            <label>Email</label>
            <Field name="email" type="email" />
            <ErrorMessage name="email" component="div" />
          </div>

          <div>
            <label>Age</label>
            <Field name="age" type="number" />
            <ErrorMessage name="age" component="div" />
          </div>

          <button type="submit" disabled={isSubmitting}>
            Submit
          </button>
        </Form>
      )}
    </Formik>
  )
}
```

### After: Formily Version

```typescript
import React from 'react'
import { createForm } from '@formily/core'
import { FormProvider, createSchemaField } from '@formily/react'
import { Form, FormItem, Input, InputNumber, Button } from '@formily/antd'

const FormilyFormikExample: React.FC = () => {
  const form = createForm({
    initialValues: {
      firstName: '',
      lastName: '',
      email: '',
      age: undefined
    }
  })

  const schema = {
    type: 'object',
    properties: {
      firstName: {
        type: 'string',
        title: 'First Name',
        required: true,
        'x-decorator': 'FormItem',
        'x-component': 'Input',
        'x-validator': [{ required: true, message: 'First name is required' }]
      },
      lastName: {
        type: 'string',
        title: 'Last Name',
        required: true,
        'x-decorator': 'FormItem',
        'x-component': 'Input',
        'x-validator': [{ required: true, message: 'Last name is required' }]
      },
      email: {
        type: 'string',
        title: 'Email',
        required: true,
        'x-decorator': 'FormItem',
        'x-component': 'Input',
        'x-validator': [
          { required: true, message: 'Email is required' },
          { format: 'email', message: 'Invalid email format' }
        ]
      },
      age: {
        type: 'number',
        title: 'Age',
        required: true,
        'x-decorator': 'FormItem',
        'x-component': 'InputNumber',
        'x-validator': [
          { required: true, message: 'Age is required' },
          { minimum: 18, message: 'Must be at least 18' }
        ]
      }
    }
  }

  const SchemaField = createSchemaField({
    components: {
      Form,
      FormItem,
      Input,
      InputNumber,
      Button
    }
  })

  const handleSubmit = async () => {
    try {
      await form.validate()
      const values = form.values
      await submitForm(values)
      form.reset()
    } catch (error) {
      console.error('Validation errors:', error)
    }
  }

  return (
    <FormProvider form={form}>
      <Form labelCol={6} wrapperCol={16}>
        <SchemaField schema={schema} />
        <FormItem wrapperCol={{ offset: 6, span: 16 }}>
          <Button type="primary" onClick={handleSubmit}>
            Submit
          </Button>
        </FormItem>
      </Form>
    </FormProvider>
  )
}
```

## From React Hook Form

### Before: React Hook Form

```typescript
import React from 'react'
import { useForm, SubmitHandler } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as Yup from 'yup'

interface FormData {
  username: string
  email: string
  password: string
  confirmPassword: string
}

const schema = Yup.object({
  username: Yup.string().required('Username is required'),
  email: Yup.string().email('Invalid email').required('Email is required'),
  password: Yup.string().min(8, 'Password must be at least 8 characters').required('Password is required'),
  confirmPassword: Yup.string().oneOf([Yup.ref('password')], 'Passwords must match').required('Confirm password is required')
})

const ReactHookFormExample: React.FC = () => {
  const { register, handleSubmit, formState: { errors }, watch } = useForm<FormData>({
    resolver: yupResolver(schema)
  })

  const watchedPassword = watch('password')

  const onSubmit: SubmitHandler<FormData> = (data) => {
    console.log(data)
    // Submit logic
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Username</label>
        <input {...register('username')} />
        {errors.username && <span>{errors.username.message}</span>}
      </div>

      <div>
        <label>Email</label>
        <input type="email" {...register('email')} />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <label>Password</label>
        <input type="password" {...register('password')} />
        {errors.password && <span>{errors.password.message}</span>}
      </div>

      <div>
        <label>Confirm Password</label>
        <input type="password" {...register('confirmPassword')} />
        {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}
      </div>

      <button type="submit">Submit</button>
    </form>
  )
}
```

### After: Formily Version

```typescript
import React from 'react'
import { createForm } from '@formily/core'
import { FormProvider, createSchemaField } from '@formily/react'
import { Form, FormItem, Input, Button } from '@formily/antd'

interface FormData {
  username: string
  email: string
  password: string
  confirmPassword: string
}

const FormilyReactHookFormExample: React.FC = () => {
  const form = createForm<FormData>({
    initialValues: {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    },
    effects() {
      // Custom validation for password match
      onFieldChange('confirmPassword', ['value'], (field) => {
        const password = form.values.password
        const confirmPassword = field.value

        if (confirmPassword && password !== confirmPassword) {
          field.errors = ['Passwords must match']
        } else {
          field.errors = []
        }
      })
    }
  })

  const schema = {
    type: 'object',
    properties: {
      username: {
        type: 'string',
        title: 'Username',
        required: true,
        'x-decorator': 'FormItem',
        'x-component': 'Input',
        'x-validator': [{ required: true, message: 'Username is required' }]
      },
      email: {
        type: 'string',
        title: 'Email',
        required: true,
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
        required: true,
        'x-decorator': 'FormItem',
        'x-component': 'Input.Password',
        'x-validator': [
          { required: true, message: 'Password is required' },
          { min: 8, message: 'Password must be at least 8 characters' }
        ]
      },
      confirmPassword: {
        type: 'string',
        title: 'Confirm Password',
        required: true,
        'x-decorator': 'FormItem',
        'x-component': 'Input.Password',
        'x-validator': [{ required: true, message: 'Please confirm your password' }]
      }
    }
  }

  const SchemaField = createSchemaField({
    components: {
      Form,
      FormItem,
      Input,
      Button
    }
  })

  const handleSubmit = async () => {
    try {
      await form.validate()
      const values = form.values
      console.log(values)
      // Submit logic
      form.reset()
    } catch (error) {
      console.error('Validation errors:', error)
    }
  }

  return (
    <FormProvider form={form}>
      <Form labelCol={6} wrapperCol={16}>
        <SchemaField schema={schema} />
        <FormItem wrapperCol={{ offset: 6, span: 16 }}>
          <Button type="primary" onClick={handleSubmit}>
            Submit
          </Button>
        </FormItem>
      </Form>
    </FormProvider>
  )
}
```

## Migration Checklist

### Pre-Migration Preparation

1. **Analyze existing forms**
   - [ ] Count total forms to migrate
   - [ ] Identify form complexity levels
   - [ ] Document validation logic
   - [ ] Note custom components used

2. **Set up Formily**
   - [ ] Install Formily packages
   - [ ] Configure TypeScript types
   - [ ] Set up Ant Design integration
   - [ ] Create basic form components

3. **Plan migration strategy**
   - [ ] Choose incremental vs complete rewrite
   - [ ] Define migration timeline
   - [ ] Assign team responsibilities
   - [ ] Set up testing strategy

### Migration Steps

1. **Convert form structure**
   - [ ] Replace useState with createForm
   - [ ] Convert field definitions to schema
   - [ ] Update validation logic
   - [ ] Replace onChange handlers

2. **Update validation**
   - [ ] Convert Yup schemas to Formily validators
   - [ ] Implement custom validation rules
   - [ ] Set up async validation
   - [ ] Configure error messages

3. **Migrate components**
   - [ ] Replace Formik/React Hook Form components
   - [ ] Update Ant Design integration
   - [ ] Convert custom field components
   - [ ] Update form submission logic

4. **Test migration**
   - [ ] Unit test individual forms
   - [ ] Integration test form workflows
   - [ ] Test validation scenarios
   - [ ] Performance test large forms

### Post-Migration

1. **Validation**
   - [ ] All forms render correctly
   - [ ] Validation works as expected
   - [ ] Form submission functions properly
   - [ ] TypeScript types are correct

2. **Optimization**
   - [ ] Remove unused dependencies
   - [ ] Optimize form performance
   - [ ] Update documentation
   - [ ] Train team on Formily

## Common Migration Patterns

### State Management Migration

```typescript
// Before: Multiple useState hooks
const [name, setName] = useState('')
const [email, setEmail] = useState('')
const [errors, setErrors] = useState({})

// After: Single form instance
const form = createForm({
  initialValues: { name: '', email: '' }
})
```

### Validation Migration

```typescript
// Before: Manual validation
const validateForm = () => {
  const errors = {}
  if (!name) errors.name = 'Name is required'
  if (!email) errors.email = 'Email is required'
  setErrors(errors)
}

// After: Schema-based validation
const schema = {
  type: 'object',
  properties: {
    name: { type: 'string', required: true },
    email: { type: 'string', required: true, format: 'email' }
  }
}
```

### Form Submission Migration

```typescript
// Before: Manual submission handling
const handleSubmit = (e) => {
  e.preventDefault()
  if (validateForm()) {
    submitForm({ name, email })
  }
}

// After: Formily submission
const handleSubmit = async () => {
  await form.validate()
  submitForm(form.values)
}
```

## Additional Resources

### Templates
- **`templates/migration-template.tsx`** - Reusable migration template
- **`templates/validation-converter.ts`** - Validation logic converter utility

### Reference Files
- **`references/migration-comparison.md`** - Side-by-side comparison table
- **`references/common-pitfalls.md`** - Migration pitfalls and solutions
- **`references/validation-mapping.md`** - Validation rule mapping guide

### Migration Tools
- Use automated code migration scripts for simple forms
- Create custom transformation utilities for complex forms
- Implement gradual migration wrappers for mixed environments

## Best Practices

1. **Start simple** - Migrate basic forms first to learn the pattern
2. **Maintain type safety** - Convert all forms to TypeScript
3. **Test thoroughly** - Validate each migrated form matches original behavior
4. **Document changes** - Keep track of migration decisions and patterns
5. **Iterate gradually** - Improve forms after initial migration
6. **Monitor performance** - Watch for performance issues in complex forms
7. **Train the team** - Ensure all developers understand Formily patterns
8. **Plan for rollbacks** - Keep original forms as backup during migration