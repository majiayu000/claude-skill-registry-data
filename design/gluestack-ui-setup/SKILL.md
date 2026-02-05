---
name: gluestack-ui-setup
description: Gluestack-ui component library setup and usage. Use when implementing pre-built accessible components.
---

# Gluestack-ui Setup Skill

This skill covers Gluestack-ui component library for React Native.

## When to Use

Use this skill when:
- Need pre-built accessible components
- Implementing forms with inputs, selects, etc.
- Building modals, tooltips, popovers
- Want shadcn/ui-like experience for mobile

## Core Principle

**ACCESSIBLE BY DEFAULT** - Gluestack components are built with accessibility in mind.

## Installation

```bash
npx gluestack-ui init
```

Follow the prompts to configure:
- Style engine (NativeWind recommended)
- TypeScript
- Path aliases

## Available Components

### Form Components

```typescript
import {
  Input,
  InputField,
  InputSlot,
  InputIcon,
} from '@gluestack-ui/themed';

<Input>
  <InputSlot>
    <InputIcon as={SearchIcon} />
  </InputSlot>
  <InputField
    placeholder="Search..."
    accessibilityLabel="Search input"
  />
</Input>
```

### Button

```typescript
import { Button, ButtonText, ButtonIcon } from '@gluestack-ui/themed';

<Button size="md" variant="solid" action="primary">
  <ButtonText>Click Me</ButtonText>
</Button>

<Button size="lg" variant="outline" action="secondary">
  <ButtonIcon as={PlusIcon} />
  <ButtonText>Add Item</ButtonText>
</Button>
```

### Select

```typescript
import {
  Select,
  SelectTrigger,
  SelectInput,
  SelectPortal,
  SelectBackdrop,
  SelectContent,
  SelectItem,
} from '@gluestack-ui/themed';

<Select>
  <SelectTrigger>
    <SelectInput placeholder="Select option" />
  </SelectTrigger>
  <SelectPortal>
    <SelectBackdrop />
    <SelectContent>
      <SelectItem label="Option 1" value="1" />
      <SelectItem label="Option 2" value="2" />
      <SelectItem label="Option 3" value="3" />
    </SelectContent>
  </SelectPortal>
</Select>
```

### Checkbox

```typescript
import {
  Checkbox,
  CheckboxIndicator,
  CheckboxIcon,
  CheckboxLabel,
} from '@gluestack-ui/themed';
import { CheckIcon } from 'lucide-react-native';

<Checkbox value="agree">
  <CheckboxIndicator>
    <CheckboxIcon as={CheckIcon} />
  </CheckboxIndicator>
  <CheckboxLabel>I agree to terms</CheckboxLabel>
</Checkbox>
```

### Modal

```typescript
import {
  Modal,
  ModalBackdrop,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalCloseButton,
} from '@gluestack-ui/themed';

const [showModal, setShowModal] = useState(false);

<Modal isOpen={showModal} onClose={() => setShowModal(false)}>
  <ModalBackdrop />
  <ModalContent>
    <ModalHeader>
      <Heading>Modal Title</Heading>
      <ModalCloseButton />
    </ModalHeader>
    <ModalBody>
      <Text>Modal content goes here</Text>
    </ModalBody>
    <ModalFooter>
      <Button onPress={() => setShowModal(false)}>
        <ButtonText>Close</ButtonText>
      </Button>
    </ModalFooter>
  </ModalContent>
</Modal>
```

### Toast

```typescript
import { useToast, Toast, ToastTitle, ToastDescription } from '@gluestack-ui/themed';

function Component(): React.ReactElement {
  const toast = useToast();

  const showToast = () => {
    toast.show({
      placement: 'top',
      render: ({ id }) => (
        <Toast nativeID={id} action="success">
          <ToastTitle>Success!</ToastTitle>
          <ToastDescription>Your action was completed.</ToastDescription>
        </Toast>
      ),
    });
  };

  return (
    <Button onPress={showToast}>
      <ButtonText>Show Toast</ButtonText>
    </Button>
  );
}
```

### Alert

```typescript
import { Alert, AlertIcon, AlertText } from '@gluestack-ui/themed';
import { InfoIcon } from 'lucide-react-native';

<Alert action="info">
  <AlertIcon as={InfoIcon} />
  <AlertText>This is an informational alert.</AlertText>
</Alert>

<Alert action="error">
  <AlertIcon as={AlertCircleIcon} />
  <AlertText>Something went wrong!</AlertText>
</Alert>
```

## Combining with NativeWind

```typescript
import { Button, ButtonText } from '@gluestack-ui/themed';

// Use className for additional styling
<Button className="bg-blue-600 rounded-full">
  <ButtonText className="text-white font-bold">
    Custom Styled
  </ButtonText>
</Button>
```

## Form Example

```typescript
import { View, Text } from 'react-native';
import {
  Input,
  InputField,
  Button,
  ButtonText,
  FormControl,
  FormControlLabel,
  FormControlLabelText,
  FormControlError,
  FormControlErrorText,
} from '@gluestack-ui/themed';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type FormData = z.infer<typeof schema>;

export function LoginForm(): React.ReactElement {
  const { control, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = (data: FormData) => {
    console.log(data);
  };

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
                keyboardType="email-address"
                autoCapitalize="none"
              />
            </Input>
          )}
        />
        <FormControlError>
          <FormControlErrorText>{errors.email?.message}</FormControlErrorText>
        </FormControlError>
      </FormControl>

      <FormControl isInvalid={!!errors.password}>
        <FormControlLabel>
          <FormControlLabelText>Password</FormControlLabelText>
        </FormControlLabel>
        <Controller
          control={control}
          name="password"
          render={({ field: { onChange, value } }) => (
            <Input>
              <InputField
                value={value}
                onChangeText={onChange}
                secureTextEntry
              />
            </Input>
          )}
        />
        <FormControlError>
          <FormControlErrorText>{errors.password?.message}</FormControlErrorText>
        </FormControlError>
      </FormControl>

      <Button onPress={handleSubmit(onSubmit)}>
        <ButtonText>Sign In</ButtonText>
      </Button>
    </View>
  );
}
```

## Theming

```typescript
// gluestack-ui.config.ts
import { config } from '@gluestack-ui/config';

export default {
  ...config,
  tokens: {
    ...config.tokens,
    colors: {
      ...config.tokens.colors,
      primary500: '#3B82F6',
      primary600: '#2563EB',
    },
  },
};
```

## Notes

- Gluestack components work seamlessly with NativeWind
- All components support accessibility attributes
- Use FormControl for form validation feedback
- Toast requires ToastProvider at app root
- Modal requires OverlayProvider for proper rendering
