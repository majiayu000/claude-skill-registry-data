---
name: tanstack-form
description: Build forms in React using TanStack Form and Zod validation. Use when creating forms, handling form validation, or working with form fields.
---

# TanStack Form with Zod and Shadcn/ui

Build accessible, validated forms in React using TanStack Form with Zod schema validation.

## Core Pattern

```tsx
import { useForm } from "@tanstack/react-form"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    Field,
    FieldDescription,
    FieldError,
    FieldGroup,
    FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  title: z.string().min(5, "Title must be at least 5 characters."),
  description: z.string().min(20, "Description must be at least 20 characters."),
})

export function MyForm() {
  const form = useForm({
    defaultValues: {
      title: "",
      description: "",
    },
    validators: {
      onSubmit: formSchema,
    },
    onSubmit: async ({ value }) => {
      // Handle submission
      console.log(value)
    },
  })

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        form.handleSubmit()
      }}
    >
      <form.Field
        name="title"
        children={(field) => {
          const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
          return (
            <Field data-invalid={isInvalid}>
              <FieldLabel htmlFor={field.name}>Title</FieldLabel>
              <Input
                id={field.name}
                name={field.name}
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
                aria-invalid={isInvalid}
              />
              {isInvalid && <FieldError errors={field.state.meta.errors} />}
            </Field>
          )
        }}
      />
      <Button type="submit">Submit</Button>
    </form>
  )
}
```

## Validation Modes

TanStack Form supports different validation strategies:

```tsx
const form = useForm({
  defaultValues: { title: "", description: "" },
  validators: {
    onSubmit: formSchema,   // Validate on submit
    onChange: formSchema,   // Validate on every change
    onBlur: formSchema,     // Validate on blur
  },
})
```

## Field Types

### Input

```tsx
<form.Field
  name="username"
  children={(field) => {
    const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
    return (
      <Field data-invalid={isInvalid}>
        <FieldLabel htmlFor={field.name}>Username</FieldLabel>
        <Input
          id={field.name}
          name={field.name}
          value={field.state.value}
          onBlur={field.handleBlur}
          onChange={(e) => field.handleChange(e.target.value)}
          aria-invalid={isInvalid}
        />
        {isInvalid && <FieldError errors={field.state.meta.errors} />}
      </Field>
    )
  }}
/>
```

### Textarea

```tsx
<form.Field
  name="description"
  children={(field) => {
    const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
    return (
      <Field data-invalid={isInvalid}>
        <FieldLabel htmlFor={field.name}>Description</FieldLabel>
        <Textarea
          id={field.name}
          name={field.name}
          value={field.state.value}
          onBlur={field.handleBlur}
          onChange={(e) => field.handleChange(e.target.value)}
          aria-invalid={isInvalid}
        />
        {isInvalid && <FieldError errors={field.state.meta.errors} />}
      </Field>
    )
  }}
/>
```

### Select

```tsx
<form.Field
  name="language"
  children={(field) => {
    const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
    return (
      <Field data-invalid={isInvalid}>
        <FieldLabel htmlFor={field.name}>Language</FieldLabel>
        <Select
          name={field.name}
          value={field.state.value}
          onValueChange={field.handleChange}
        >
          <SelectTrigger id={field.name} aria-invalid={isInvalid}>
            <SelectValue placeholder="Select" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="en">English</SelectItem>
            <SelectItem value="es">Spanish</SelectItem>
          </SelectContent>
        </Select>
        {isInvalid && <FieldError errors={field.state.meta.errors} />}
      </Field>
    )
  }}
/>
```

### Checkbox (Single)

```tsx
<form.Field
  name="terms"
  children={(field) => {
    const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
    return (
      <Field orientation="horizontal" data-invalid={isInvalid}>
        <Checkbox
          id={field.name}
          name={field.name}
          checked={field.state.value}
          onCheckedChange={field.handleChange}
          aria-invalid={isInvalid}
        />
        <FieldLabel htmlFor={field.name}>Accept terms</FieldLabel>
        {isInvalid && <FieldError errors={field.state.meta.errors} />}
      </Field>
    )
  }}
/>
```

### Checkbox (Array)

Use `mode="array"` for multiple checkbox selections:

```tsx
<form.Field
  name="tasks"
  mode="array"
  children={(field) => {
    const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
    return (
      <FieldSet>
        <FieldLegend>Tasks</FieldLegend>
        <FieldGroup data-slot="checkbox-group">
          {tasks.map((task) => (
            <Field key={task.id} orientation="horizontal" data-invalid={isInvalid}>
              <Checkbox
                id={`task-${task.id}`}
                name={field.name}
                aria-invalid={isInvalid}
                checked={field.state.value.includes(task.id)}
                onCheckedChange={(checked) => {
                  if (checked) {
                    field.pushValue(task.id)
                  } else {
                    const index = field.state.value.indexOf(task.id)
                    if (index > -1) field.removeValue(index)
                  }
                }}
              />
              <FieldLabel htmlFor={`task-${task.id}`}>{task.label}</FieldLabel>
            </Field>
          ))}
        </FieldGroup>
        {isInvalid && <FieldError errors={field.state.meta.errors} />}
      </FieldSet>
    )
  }}
/>
```

### Radio Group

```tsx
<form.Field
  name="plan"
  children={(field) => {
    const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
    return (
      <FieldSet>
        <FieldLegend>Plan</FieldLegend>
        <RadioGroup
          name={field.name}
          value={field.state.value}
          onValueChange={field.handleChange}
        >
          {plans.map((plan) => (
            <Field key={plan.id} orientation="horizontal" data-invalid={isInvalid}>
              <RadioGroupItem
                value={plan.id}
                id={`plan-${plan.id}`}
                aria-invalid={isInvalid}
              />
              <FieldLabel htmlFor={`plan-${plan.id}`}>{plan.title}</FieldLabel>
            </Field>
          ))}
        </RadioGroup>
        {isInvalid && <FieldError errors={field.state.meta.errors} />}
      </FieldSet>
    )
  }}
/>
```

### Switch

```tsx
<form.Field
  name="twoFactor"
  children={(field) => {
    const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid
    return (
      <Field orientation="horizontal" data-invalid={isInvalid}>
        <FieldContent>
          <FieldLabel htmlFor={field.name}>Two-factor authentication</FieldLabel>
          <FieldDescription>Enable for extra security.</FieldDescription>
          {isInvalid && <FieldError errors={field.state.meta.errors} />}
        </FieldContent>
        <Switch
          id={field.name}
          name={field.name}
          checked={field.state.value}
          onCheckedChange={field.handleChange}
          aria-invalid={isInvalid}
        />
      </Field>
    )
  }}
/>
```

## Array Fields

Manage dynamic lists with `mode="array"`:

```tsx
const formSchema = z.object({
  emails: z
    .array(z.object({ address: z.string().email("Enter a valid email.") }))
    .min(1, "Add at least one email.")
    .max(5, "Maximum 5 emails."),
})

<form.Field
  name="emails"
  mode="array"
  children={(field) => (
    <FieldSet>
      <FieldLegend>Email Addresses</FieldLegend>
      <FieldGroup>
        {field.state.value.map((_, index) => (
          <form.Field
            key={index}
            name={`emails[${index}].address`}
            children={(subField) => {
              const isInvalid = subField.state.meta.isTouched && !subField.state.meta.isValid
              return (
                <Field data-invalid={isInvalid}>
                  <Input
                    id={`email-${index}`}
                    name={subField.name}
                    value={subField.state.value}
                    onBlur={subField.handleBlur}
                    onChange={(e) => subField.handleChange(e.target.value)}
                    aria-invalid={isInvalid}
                    type="email"
                  />
                  <Button
                    type="button"
                    variant="ghost"
                    onClick={() => field.removeValue(index)}
                    disabled={field.state.value.length <= 1}
                  >
                    Remove
                  </Button>
                  {isInvalid && <FieldError errors={subField.state.meta.errors} />}
                </Field>
              )
            }}
          />
        ))}
      </FieldGroup>
      <Button
        type="button"
        variant="outline"
        onClick={() => field.pushValue({ address: "" })}
        disabled={field.state.value.length >= 5}
      >
        Add Email
      </Button>
    </FieldSet>
  )}
/>
```

## Array Field Methods

- `field.pushValue(item)` - Add item to array
- `field.removeValue(index)` - Remove item at index
- `field.state.value.length` - Current array length

## Form Actions

```tsx
// Reset form to default values
<Button type="button" variant="outline" onClick={() => form.reset()}>
  Reset
</Button>

// Submit form
<Button type="submit">Submit</Button>
```

## Accessibility Checklist

1. Add `id` and `htmlFor` to link labels to inputs
2. Add `aria-invalid={isInvalid}` to form controls
3. Add `data-invalid={isInvalid}` to Field wrapper for styling
4. Use `FieldDescription` for help text
5. Use `FieldError` to display validation errors