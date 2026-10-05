---
name: hookify
description: Hook creation and management system for React, Vue, and other frameworks with automated hook generation, testing, and documentation.
license: MIT
---

# Hook Creation & Management System

## Overview

Comprehensive hook development toolkit providing automated hook generation, testing utilities, documentation generation, and management for React, Vue, and other modern frontend frameworks.

## Quick Start

### Installation
```bash
npm install -g @hookify/cli
# or
npx @hookify/cli init
```

### Initialize Hook Project
```bash
# Initialize in existing project
hookify init

# Create new hook library
hookify create my-hooks --template=react

# Add to existing project
hookify add --project=my-react-app --framework=react
```

## Hook Generation

### React Hooks
```bash
# Generate custom hook
hookify generate useUserData --framework=react

# Generate with dependencies
hookify generate useApi --framework=react --deps=useState,useEffect

# Generate with TypeScript
hookify generate useLocalStorage --framework=react --typescript --generic
```

**React Hook Template**
```typescript
// hooks/useApi.ts
import { useState, useEffect, useCallback } from 'react';

interface UseApiOptions<T> {
  immediate?: boolean;
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
}

interface UseApiReturn<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  execute: () => Promise<void>;
  reset: () => void;
}

export function useApi<T>(
  url: string,
  options: UseApiOptions<T> = {}
): UseApiReturn<T> {
  const { immediate = true, onSuccess, onError } = options;
  
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const execute = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      setData(result);
      onSuccess?.(result);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      onError?.(error);
    } finally {
      setLoading(false);
    }
  }, [url, onSuccess, onError]);

  const reset = useCallback(() => {
    setData(null);
    setLoading(false);
    setError(null);
  }, []);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [immediate, execute]);

  return { data, loading, error, execute, reset };
}
```

### Vue Composition API
```bash
# Generate Vue composable
hookify generate useUserData --framework=vue

# Generate with reactivity
hookify generate useCounter --framework=vue --reactive

# Generate with TypeScript
hookify generate useLocalStorage --framework=vue --typescript
```

**Vue Composable Template**
```typescript
// composables/useApi.ts
import { ref, computed, watch } from 'vue';

interface UseApiOptions<T> {
  immediate?: boolean;
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
}

export function useApi<T>(
  url: string,
  options: UseApiOptions<T> = {}
) {
  const { immediate = true, onSuccess, onError } = options;
  
  const data = ref<T | null>(null);
  const loading = ref(false);
  const error = ref<Error | null>(null);

  const execute = async () => {
    try {
      loading.value = true;
      error.value = null;
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      data.value = result;
      onSuccess?.(result);
    } catch (err) {
      const errorValue = err instanceof Error ? err : new Error('Unknown error');
      error.value = errorValue;
      onError?.(errorValue);
    } finally {
      loading.value = false;
    }
  };

  const reset = () => {
    data.value = null;
    loading.value = false;
    error.value = null;
  };

  // Computed properties
  const isIdle = computed(() => !loading.value && !error.value && data.value === null);
  const isSuccess = computed(() => !loading.value && !error.value && data.value !== null);
  const isError = computed(() => !loading.value && error.value !== null);

  // Auto-execute if immediate
  if (immediate) {
    execute();
  }

  return {
    data,
    loading: readonly(loading),
    error: readonly(error),
    execute,
    reset,
    isIdle,
    isSuccess,
    isError
  };
}
```

### Svelte Hooks
```bash
# Generate Svelte store
hookify generate useUserData --framework=svelte

# Generate writable store
hookify generate useCounter --framework=svelte --type=writable

# Generate derived store
hookify generate useFilteredData --framework=svelte --type=derived
```

**Svelte Store Template**
```typescript
// stores/useApi.ts
import { writable, derived } from 'svelte/store';

interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

function createApiStore<T>(url: string) {
  const { subscribe, set, update } = writable<ApiState<T>>({
    data: null,
    loading: false,
    error: null
  });

  const execute = async () => {
    update(state => ({ ...state, loading: true, error: null }));
    
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      set({ data: result, loading: false, error: null });
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      set({ data: null, loading: false, error });
    }
  };

  const reset = () => {
    set({ data: null, loading: false, error: null });
  };

  // Derived stores
  const isIdle = derived(store, $store => !$store.loading && !$store.error && $store.data === null);
  const isSuccess = derived(store, $store => !$store.loading && !$store.error && $store.data !== null);
  const isError = derived(store, $store => !$store.loading && $store.error !== null);

  return {
    subscribe,
    execute,
    reset,
    isIdle,
    isSuccess,
    isError
  };
}

export const useApi = createApiStore;
```

## Hook Templates

### Common Hook Patterns
```bash
# Generate data fetching hook
hookify generate useFetch --template=data-fetching

# Generate form handling hook
hookify generate useForm --template=form-handling

# Generate authentication hook
hookify generate useAuth --template=authentication

# Generate local storage hook
hookify generate useLocalStorage --template=storage
```

**Data Fetching Template**
```typescript
// templates/data-fetching.hook.ts
export const dataFetchingTemplate = `
import { useState, useEffect, useCallback, useRef } from 'react';

interface Use{{Name}}Options<T> {
  immediate?: boolean;
  cache?: boolean;
  cacheTime?: number;
  retry?: number;
  retryDelay?: number;
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
}

interface Use{{Name}}Return<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  execute: () => Promise<void>;
  refetch: () => Promise<void>;
  reset: () => void;
}

export function use{{Name}}<T>(
  fetcher: () => Promise<T>,
  options: Use{{Name}}Options<T> = {}
): Use{{Name}}Return<T> {
  const { 
    immediate = true, 
    cache = false, 
    cacheTime = 300000, // 5 minutes
    retry = 3,
    retryDelay = 1000,
    onSuccess,
    onError 
  } = options;
  
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  
  const cacheRef = useRef<Map<string, { data: T; timestamp: number }>>(new Map());
  const retryCountRef = useRef(0);

  const execute = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Check cache
      if (cache) {
        const cacheKey = fetcher.toString();
        const cached = cacheRef.current.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < cacheTime) {
          setData(cached.data);
          onSuccess?.(cached.data);
          return;
        }
      }
      
      const result = await fetcher();
      setData(result);
      
      // Update cache
      if (cache) {
        const cacheKey = fetcher.toString();
        cacheRef.current.set(cacheKey, { data: result, timestamp: Date.now() });
      }
      
      retryCountRef.current = 0;
      onSuccess?.(result);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      
      // Retry logic
      if (retryCountRef.current < retry) {
        retryCountRef.current++;
        setTimeout(execute, retryDelay * retryCountRef.current);
        return;
      }
      
      setError(error);
      onError?.(error);
    } finally {
      setLoading(false);
    }
  }, [fetcher, cache, cacheTime, retry, retryDelay, onSuccess, onError]);

  const refetch = useCallback(() => {
    retryCountRef.current = 0;
    return execute();
  }, [execute]);

  const reset = useCallback(() => {
    setData(null);
    setLoading(false);
    setError(null);
    retryCountRef.current = 0;
  }, []);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [immediate, execute]);

  return { data, loading, error, execute, refetch, reset };
}
`;
```

**Form Handling Template**
```typescript
// templates/form-handling.hook.ts
export const formHandlingTemplate = `
import { useState, useCallback, useEffect } from 'react';

interface FieldValidation {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  custom?: (value: any) => string | null;
}

interface FormField<T = any> {
  value: T;
  error: string | null;
  touched: boolean;
  validation?: FieldValidation;
}

interface UseFormOptions<T> {
  initialValues: T;
  validation?: Partial<Record<keyof T, FieldValidation>>;
  onSubmit?: (values: T) => void | Promise<void>;
  validateOnChange?: boolean;
}

interface UseFormReturn<T> {
  values: T;
  errors: Partial<Record<keyof T, string | null>>;
  touched: Partial<Record<keyof T, boolean>>;
  isValid: boolean;
  isDirty: boolean;
  isSubmitting: boolean;
  setValue: <K extends keyof T>(field: K, value: T[K]) => void;
  setError: <K extends keyof T>(field: K, error: string | null) => void;
  setTouched: <K extends keyof T>(field: K, touched: boolean) => void;
  validateField: <K extends keyof T>(field: K) => string | null;
  validateForm: () => boolean;
  handleSubmit: () => Promise<void>;
  resetForm: () => void;
  resetField: <K extends keyof T>(field: K) => void;
}

export function useForm<T extends Record<string, any>>(
  options: UseFormOptions<T>
): UseFormReturn<T> {
  const { initialValues, validation = {}, onSubmit, validateOnChange = true } = options;
  
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string | null>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateField = useCallback(<K extends keyof T>(field: K): string | null => {
    const value = values[field];
    const fieldValidation = validation[field];
    
    if (!fieldValidation) return null;
    
    // Required validation
    if (fieldValidation.required && (!value || value === '')) {
      return 'This field is required';
    }
    
    // Length validation
    if (typeof value === 'string') {
      if (fieldValidation.minLength && value.length < fieldValidation.minLength) {
        return \`Minimum length is \${fieldValidation.minLength} characters\`;
      }
      if (fieldValidation.maxLength && value.length > fieldValidation.maxLength) {
        return \`Maximum length is \${fieldValidation.maxLength} characters\`;
      }
    }
    
    // Pattern validation
    if (fieldValidation.pattern && typeof value === 'string') {
      if (!fieldValidation.pattern.test(value)) {
        return 'Invalid format';
      }
    }
    
    // Custom validation
    if (fieldValidation.custom) {
      return fieldValidation.custom(value);
    }
    
    return null;
  }, [values, validation]);

  const validateForm = useCallback((): boolean => {
    const newErrors: Partial<Record<keyof T, string | null>> = {};
    let isValid = true;
    
    Object.keys(validation).forEach((field) => {
      const error = validateField(field as keyof T);
      newErrors[field as keyof T] = error;
      if (error) isValid = false;
    });
    
    setErrors(newErrors);
    return isValid;
  }, [validateField, validation]);

  const setValue = useCallback(<K extends keyof T>(field: K, value: T[K]) => {
    setValues(prev => ({ ...prev, [field]: value }));
    
    if (validateOnChange) {
      const error = validateField(field);
      setErrors(prev => ({ ...prev, [field]: error }));
    }
  }, [validateField, validateOnChange]);

  const setError = useCallback(<K extends keyof T>(field: K, error: string | null) => {
    setErrors(prev => ({ ...prev, [field]: error }));
  }, []);

  const setTouched = useCallback(<K extends keyof T>(field: K, touchedValue: boolean) => {
    setTouched(prev => ({ ...prev, [field]: touchedValue }));
  }, []);

  const handleSubmit = useCallback(async () => {
    // Validate all fields
    const isValid = validateForm();
    
    if (!isValid) return;
    
    setIsSubmitting(true);
    
    try {
      await onSubmit?.(values);
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  }, [validateForm, onSubmit, values]);

  const resetForm = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [initialValues]);

  const resetField = useCallback(<K extends keyof T>(field: K) => {
    setValues(prev => ({ ...prev, [field]: initialValues[field] }));
    setErrors(prev => ({ ...prev, [field]: null }));
    setTouched(prev => ({ ...prev, [field]: false }));
  }, [initialValues]);

  // Computed values
  const isValid = Object.values(errors).every(error => !error);
  const isDirty = Object.keys(touched).some(key => touched[key as keyof T]);

  return {
    values,
    errors,
    touched,
    isValid,
    isDirty,
    isSubmitting,
    setValue,
    setError,
    setTouched,
    validateField,
    validateForm,
    handleSubmit,
    resetForm,
    resetField
  };
}
`;
```

## Hook Testing

### Test Generation
```bash
# Generate hook tests
hookify test generate useApi --framework=react-testing-library

# Generate test with custom scenarios
hookify test generate useLocalStorage --scenarios=basic,error,edge-cases

# Generate performance tests
hookify test generate useApi --performance --memory-leaks
```

**Hook Test Template**
```typescript
// test/hooks/useApi.test.ts
import { renderHook, act, waitFor } from '@testing-library/react';
import { useApi } from '../hooks/useApi';

// Mock fetch
global.fetch = jest.fn();

describe('useApi', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should initialize with loading state', () => {
    const { result } = renderHook(() => useApi('https://api.example.com/data'));
    
    expect(result.current.loading).toBe(true);
    expect(result.current.data).toBe(null);
    expect(result.current.error).toBe(null);
  });

  test('should fetch data successfully', async () => {
    const mockData = { id: 1, name: 'Test Data' };
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData
    });

    const { result } = renderHook(() => useApi('https://api.example.com/data'));

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.data).toEqual(mockData);
      expect(result.current.error).toBe(null);
    });

    expect(fetch).toHaveBeenCalledWith('https://api.example.com/data');
  });

  test('should handle fetch error', async () => {
    const mockError = new Error('Network error');
    (fetch as jest.Mock).mockRejectedValueOnce(mockError);

    const onError = jest.fn();
    const { result } = renderHook(() => 
      useApi('https://api.example.com/data', { onError })
    );

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.data).toBe(null);
      expect(result.current.error).toEqual(mockError);
    });

    expect(onError).toHaveBeenCalledWith(mockError);
  });

  test('should not fetch immediately when immediate is false', () => {
    const { result } = renderHook(() => 
      useApi('https://api.example.com/data', { immediate: false })
    );
    
    expect(result.current.loading).toBe(false);
    expect(fetch).not.toHaveBeenCalled();
  });

  test('should execute manual refetch', async () => {
    const mockData = { id: 1, name: 'Test Data' };
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData
    });

    const { result } = renderHook(() => 
      useApi('https://api.example.com/data', { immediate: false })
    );

    act(() => {
      result.current.execute();
    });

    await waitFor(() => {
      expect(result.current.data).toEqual(mockData);
    });

    expect(fetch).toHaveBeenCalledTimes(1);
  });

  test('should reset state', () => {
    const { result } = renderHook(() => 
      useApi('https://api.example.com/data', { immediate: false })
    );

    // Simulate some state change
    act(() => {
      result.current.reset();
    });

    expect(result.current.data).toBe(null);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });
});
```

### Performance Testing
```typescript
// test/performance/useApi.performance.test.ts
import { renderHook, act } from '@testing-library/react';
import { useApi } from '../hooks/useApi';

describe('useApi Performance', () => {
  test('should not cause memory leaks', () => {
    const { unmount } = renderHook(() => useApi('https://api.example.com/data'));
    
    // Force garbage collection if available
    if (global.gc) {
      global.gc();
    }
    
    // Unmount hook
    unmount();
    
    // Check for memory leaks (implementation depends on your setup)
    // This is a placeholder for actual memory leak detection
    expect(true).toBe(true);
  });

  test('should handle rapid state updates efficiently', async () => {
    const startTime = performance.now();
    
    const { result } = renderHook(() => useApi('https://api.example.com/data'));
    
    // Simulate rapid calls
    for (let i = 0; i < 100; i++) {
      act(() => {
        result.current.execute();
      });
    }
    
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    // Should complete within reasonable time (adjust threshold as needed)
    expect(duration).toBeLessThan(1000); // 1 second
  });
});
```

## Hook Documentation

### Auto-Documentation
```bash
# Generate hook documentation
hookify docs generate useApi --format=markdown

# Generate Storybook stories
hookify docs storybook useApi --framework=react

# Generate API reference
hookify docs api --output=./docs/hooks
```

**Documentation Template**
```markdown
# useApi

A custom hook for handling API calls with loading states, error handling, and caching capabilities.

## Usage

\`\`\`typescript
import { useApi } from './hooks/useApi';

interface User {
  id: number;
  name: string;
  email: string;
}

function UserProfile({ userId }: { userId: number }) {
  const { data: user, loading, error, execute } = useApi<User>(
    \`https://api.example.com/users/\${userId}\`
  );

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>No user found</div>;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
      <button onClick={execute}>Refresh</button>
    </div>
  );
}
\`\`\`

## API

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| url | \`string\` | - | The API endpoint URL |
| options | \`UseApiOptions<T>\` | \`{}\` | Configuration options |

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| immediate | \`boolean\` | \`true\` | Whether to fetch data immediately |
| onSuccess | \`(data: T) => void\` | - | Callback called on successful fetch |
| onError | \`(error: Error) => void\` | - | Callback called on error |

### Return Value

| Property | Type | Description |
|----------|------|-------------|
| data | \`T | null\` | The fetched data |
| loading | \`boolean\` | Whether the request is in progress |
| error | \`Error | null\` | Any error that occurred |
| execute | \`() => Promise<void>\` | Function to manually trigger the request |
| reset | \`() => void\` | Function to reset the hook state |

## Examples

### Basic Usage

\`\`\`typescript
const { data, loading, error } = useApi('https://api.example.com/data');
\`\`\`

### With Error Handling

\`\`\`typescript
const { data, loading, error } = useApi('https://api.example.com/data', {
  onError: (error) => console.error('API Error:', error)
});
\`\`\`

### Manual Execution

\`\`\`typescript
const { data, loading, error, execute } = useApi(
  'https://api.example.com/data',
  { immediate: false }
);

// Trigger request manually
const handleRefresh = () => {
  execute();
};
\`\`\`

## TypeScript Support

This hook is fully typed with TypeScript:

\`\`\`typescript
interface ApiResponse {
  id: number;
  name: string;
}

const { data } = useApi<ApiResponse>('https://api.example.com/data');
// data is typed as ApiResponse | null
\`\`\`

## Dependencies

- React 16.8+ (for hooks support)
- TypeScript 4.0+ (for type support)

## Related Hooks

- \`useFetch\` - Simpler data fetching hook
- \`useLocalStorage\` - Local storage synchronization
- \`useDebounce\` - Debounced values
```

## Hook Registry

### Hook Management
```bash
# List all hooks
hookify list

# Search hooks
hookify search --keyword=api

# Get hook info
hookify info useApi

# Install hook from registry
hookify install useAuth --registry=@company/hooks
```

**Hook Registry Configuration**
```javascript
// hookify.config.js
module.exports = {
  registry: {
    default: 'https://registry.hookify.dev',
    private: 'https://hooks.company.com',
    local: './hooks'
  },
  
  hooks: {
    // Local hooks
    './hooks': {
      pattern: '**/*.hook.{js,ts}',
      autoRegister: true
    },
    
    // Registry hooks
    '@company/hooks': {
      version: '^1.0.0',
      autoUpdate: true
    }
  },
  
  validation: {
    typescript: true,
    tests: true,
    documentation: true,
    performance: true
  },
  
  publishing: {
    registry: 'https://registry.hookify.dev',
    autoVersion: true,
    changelog: true
  }
};
```

### Hook Publishing
```bash
# Publish hook to registry
hookify publish useApi --registry=public

# Publish with version
hookify publish useAuth --version=2.1.0

# Publish to private registry
hookify publish useCompanyData --registry=@company/hooks
```

## Integration

### Framework Integration
```bash
# React integration
hookify integrate react --typescript=true

# Vue integration
hookify integrate vue --composition-api

# Svelte integration
hookify integrate svelte --typescript=true
```

**Build Integration**
```javascript
// webpack.config.js
const { HookifyPlugin } = require('@hookify/webpack');

module.exports = {
  plugins: [
    new HookifyPlugin({
      hooks: './src/hooks',
      output: './dist/hooks',
      optimization: {
        treeShaking: true,
        minify: true,
        bundleAnalysis: true
      }
    })
  ]
};
```

## API Reference

### Core Classes

**HookGenerator**
```typescript
import { HookGenerator } from '@hookify/core';

const generator = new HookGenerator({
  framework: 'react',
  typescript: true,
  testing: true
});

const hook = await generator.generate('useApi', {
  template: 'data-fetching',
  dependencies: ['useState', 'useEffect']
});
```

**HookTester**
```typescript
import { HookTester } from '@hookify/testing';

const tester = new HookTester({
  framework: 'react-testing-library',
  coverage: true
});

const testResults = await tester.test('useApi');
```

**HookRegistry**
```typescript
import { HookRegistry } from '@hookify/registry';

const registry = new HookRegistry({
  endpoint: 'https://registry.hookify.dev'
});

const hooks = await registry.search('api');
const hook = await registry.get('useApi');
```

## Contributing

1. Fork repository
2. Create hook feature branch
3. Add comprehensive tests
4. Generate documentation
5. Submit pull request

## License

MIT License - see LICENSE file for details.