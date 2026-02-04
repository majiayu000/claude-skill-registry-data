---
name: form-handling-mobile
description: React Hook Form and Zod for React Native forms. Use when implementing forms.
---

# Form Handling Mobile Skill

This skill covers React Hook Form with Zod validation for React Native.

## When to Use

Use this skill when:
- Building login/signup forms
- Creating data entry forms
- Implementing form validation
- Handling complex form state

## Core Principle

**CONTROLLED VALIDATION** - Use Zod for schema validation, React Hook Form for state.

## Installation

```bash
npm install react-hook-form @hookform/resolvers zod
```

## Basic Form

```typescript
import { View, Text, TextInput, TouchableOpacity } from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm(): React.ReactElement {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const onSubmit = (data: LoginFormData) => {
    console.log(data);
  };

  return (
    <View className="gap-4">
      <View>
        <Text className="mb-1 font-medium">Email</Text>
        <Controller
          control={control}
          name="email"
          render={({ field: { onChange, onBlur, value } }) => (
            <TextInput
              className="border border-gray-300 rounded-lg px-4 py-3"
              placeholder="Enter email"
              value={value}
              onChangeText={onChange}
              onBlur={onBlur}
              keyboardType="email-address"
              autoCapitalize="none"
              autoComplete="email"
            />
          )}
        />
        {errors.email && (
          <Text className="text-red-500 text-sm mt-1">
            {errors.email.message}
          </Text>
        )}
      </View>

      <View>
        <Text className="mb-1 font-medium">Password</Text>
        <Controller
          control={control}
          name="password"
          render={({ field: { onChange, onBlur, value } }) => (
            <TextInput
              className="border border-gray-300 rounded-lg px-4 py-3"
              placeholder="Enter password"
              value={value}
              onChangeText={onChange}
              onBlur={onBlur}
              secureTextEntry
              autoComplete="password"
            />
          )}
        />
        {errors.password && (
          <Text className="text-red-500 text-sm mt-1">
            {errors.password.message}
          </Text>
        )}
      </View>

      <TouchableOpacity
        onPress={handleSubmit(onSubmit)}
        className="bg-blue-600 py-4 rounded-lg"
      >
        <Text className="text-white text-center font-semibold">Sign In</Text>
      </TouchableOpacity>
    </View>
  );
}
```

## Complex Validation Schema

```typescript
const signupSchema = z
  .object({
    email: z.string().email('Invalid email'),
    username: z
      .string()
      .min(3, 'Username must be at least 3 characters')
      .max(20, 'Username must be at most 20 characters')
      .regex(/^[a-zA-Z0-9_]+$/, 'Only letters, numbers, and underscores'),
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Must contain uppercase letter')
      .regex(/[a-z]/, 'Must contain lowercase letter')
      .regex(/[0-9]/, 'Must contain number'),
    confirmPassword: z.string(),
    acceptTerms: z.boolean().refine((val) => val === true, {
      message: 'You must accept the terms',
    }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });
```

## Reusable Input Component

```typescript
import { Control, Controller, FieldValues, Path } from 'react-hook-form';

interface FormInputProps<T extends FieldValues> {
  control: Control<T>;
  name: Path<T>;
  label: string;
  placeholder?: string;
  secureTextEntry?: boolean;
  keyboardType?: 'default' | 'email-address' | 'numeric' | 'phone-pad';
  autoCapitalize?: 'none' | 'sentences' | 'words' | 'characters';
  error?: string;
}

export function FormInput<T extends FieldValues>({
  control,
  name,
  label,
  placeholder,
  secureTextEntry,
  keyboardType = 'default',
  autoCapitalize = 'sentences',
  error,
}: FormInputProps<T>): React.ReactElement {
  return (
    <View className="mb-4">
      <Text className="mb-1 font-medium text-gray-700">{label}</Text>
      <Controller
        control={control}
        name={name}
        render={({ field: { onChange, onBlur, value } }) => (
          <TextInput
            className={`border rounded-lg px-4 py-3 ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder={placeholder}
            value={value}
            onChangeText={onChange}
            onBlur={onBlur}
            secureTextEntry={secureTextEntry}
            keyboardType={keyboardType}
            autoCapitalize={autoCapitalize}
          />
        )}
      />
      {error && (
        <Text className="text-red-500 text-sm mt-1">{error}</Text>
      )}
    </View>
  );
}

// Usage
<FormInput
  control={control}
  name="email"
  label="Email"
  placeholder="Enter email"
  keyboardType="email-address"
  autoCapitalize="none"
  error={errors.email?.message}
/>
```

## With Gluestack-ui

```typescript
import {
  FormControl,
  FormControlLabel,
  FormControlLabelText,
  FormControlError,
  FormControlErrorText,
  Input,
  InputField,
} from '@gluestack-ui/themed';
import { Controller, useForm } from 'react-hook-form';

export function StyledLoginForm(): React.ReactElement {
  const { control, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  return (
    <View className="gap-4">
      <FormControl isInvalid={!!errors.email}>
        <FormControlLabel>
          <FormControlLabelText>Email</FormControlLabelText>
        </FormControlLabel>
        <Controller
          control={control}
          name="email"
          render={({ field: { onChange, value } }) => (
            <Input>
              <InputField
                value={value}
                onChangeText={onChange}
                placeholder="Enter email"
                keyboardType="email-address"
                autoCapitalize="none"
              />
            </Input>
          )}
        />
        <FormControlError>
          <FormControlErrorText>
            {errors.email?.message}
          </FormControlErrorText>
        </FormControlError>
      </FormControl>
    </View>
  );
}
```

## Form with Mutation

```typescript
import { useMutation } from '@tanstack/react-query';
import { useRouter } from 'expo-router';

export function LoginFormWithMutation(): React.ReactElement {
  const router = useRouter();
  const { mutate: login, isPending } = useLoginMutation();

  const {
    control,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (data: LoginFormData) => {
    login(data, {
      onSuccess: () => {
        router.replace('/(tabs)');
      },
      onError: (error) => {
        setError('root', {
          message: error.message || 'Login failed',
        });
      },
    });
  };

  return (
    <View className="gap-4">
      {errors.root && (
        <View className="bg-red-100 p-4 rounded-lg">
          <Text className="text-red-700">{errors.root.message}</Text>
        </View>
      )}

      {/* Form fields */}

      <TouchableOpacity
        onPress={handleSubmit(onSubmit)}
        disabled={isPending}
        className={`py-4 rounded-lg ${
          isPending ? 'bg-gray-400' : 'bg-blue-600'
        }`}
      >
        <Text className="text-white text-center font-semibold">
          {isPending ? 'Signing in...' : 'Sign In'}
        </Text>
      </TouchableOpacity>
    </View>
  );
}
```

## Checkbox and Switch

```typescript
const preferencesSchema = z.object({
  emailNotifications: z.boolean(),
  pushNotifications: z.boolean(),
  newsletter: z.boolean(),
});

<Controller
  control={control}
  name="emailNotifications"
  render={({ field: { onChange, value } }) => (
    <View className="flex-row items-center justify-between py-2">
      <Text>Email Notifications</Text>
      <Switch value={value} onValueChange={onChange} />
    </View>
  )}
/>
```

## Select/Picker

```typescript
import { Picker } from '@react-native-picker/picker';

<Controller
  control={control}
  name="country"
  render={({ field: { onChange, value } }) => (
    <View className="border border-gray-300 rounded-lg">
      <Picker selectedValue={value} onValueChange={onChange}>
        <Picker.Item label="Select country" value="" />
        <Picker.Item label="United States" value="US" />
        <Picker.Item label="Canada" value="CA" />
        <Picker.Item label="Mexico" value="MX" />
      </Picker>
    </View>
  )}
/>
```

## Watch and Dynamic Fields

```typescript
function DynamicForm(): React.ReactElement {
  const { control, watch } = useForm();
  const showAdditionalFields = watch('hasAccount');

  return (
    <View>
      <Controller
        control={control}
        name="hasAccount"
        render={({ field: { onChange, value } }) => (
          <View className="flex-row items-center">
            <Switch value={value} onValueChange={onChange} />
            <Text className="ml-2">I have an account</Text>
          </View>
        )}
      />

      {showAdditionalFields && (
        <FormInput
          control={control}
          name="accountId"
          label="Account ID"
        />
      )}
    </View>
  );
}
```

## Notes

- Use Zod for type-safe validation
- Create reusable form components
- Handle loading states during submission
- Show validation errors inline
- Use setError for server errors
- Test form behavior on both platforms
