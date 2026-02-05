---
name: react-enterprise
description: React 19 with TypeScript 5.9.3, TanStack Query V5, Zustand, and modern patterns. React Compiler handles memoization automatically. No manual optimization needed.
triggers:
  keywords: ["react", "typescript", "tanstack query", "useQuery", "zustand", "react hook form", "zod", "component", "tsx"]
  file_patterns: ["**/src/**/*.tsx", "**/src/**/*.ts", "**/components/**/*.tsx", "**/hooks/**/*.ts", "**/pages/**/*.tsx"]
  context: ["creating react components", "frontend development", "state management", "form handling", "data fetching"]
---

# React Enterprise Patterns Skill

Modern React 19 patterns with TypeScript 5.9.3, TanStack Query V5, Zustand 5, and 2025 best practices. React Compiler handles optimization automatically.

## 🎯 When to Use This Skill

**Auto-activates when:**
- Keywords: `react`, `typescript`, `useQuery`, `useMutation`, `zustand`, `zod`, `component`
- Files: `frontend/src/`, `components/`, `hooks/`, `pages/`, `*.tsx`, `*.ts`
- Tasks: creating components, state management, data fetching, form handling, TypeScript types

**NOT for:**
- Backend API development → use `fastapi-patterns` skill
- Agent integration → use `deepagents-integration` skill
- Database operations → use `fastapi-patterns` skill

## ⚡ Quick Reference

### Top 10 Essential Patterns

```typescript
// 1. Modern Component (React 19 - No memoization needed)
import type { Agent } from '@/types/agent';

interface AgentCardProps {
  agent: Agent;
  onEdit?: (id: number) => void;
}

export function AgentCard({ agent, onEdit }: AgentCardProps) {
  // ✅ No useCallback needed - React Compiler handles it
  const handleEdit = () => onEdit?.(agent.id);
  
  return <div onClick={handleEdit}>{agent.name}</div>;
}

// 2. TanStack Query V5 - Data Fetching
import { useQuery } from '@tanstack/react-query';

export function useAgents() {
  return useQuery({
    queryKey: ['agents'],  // Must be array (V5 requirement)
    queryFn: agentsApi.getAll,
  });
}

const { data, isPending, error } = useAgents();  // Note: isPending not isLoading

// 3. Mutation with Optimistic Updates
import { useMutation, useQueryClient } from '@tanstack/react-query';

export function useCreateAgent() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: AgentCreate) => agentsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] });
    },
  });
}

// 4. Form with React Hook Form + Zod
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const agentSchema = z.object({
  name: z.string().min(1).max(100),
  model: z.string(),
  temperature: z.number().min(0).max(2),
});

type AgentFormData = z.infer<typeof agentSchema>;

function AgentForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<AgentFormData>({
    resolver: zodResolver(agentSchema),
  });
  
  const onSubmit = (data: AgentFormData) => {
    console.log(data);
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} />
      {errors.name && <span>{errors.name.message}</span>}
    </form>
  );
}

// 5. Zustand Store (Modern V5)
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface UIStore {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
}

export const useUIStore = create<UIStore>()(
  devtools((set) => ({
    sidebarOpen: true,
    toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  }))
);

// 6. WebSocket Hook
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

export function useWebSocket(url: string) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);
  
  useEffect(() => {
    const newSocket = io(url);
    
    newSocket.on('connect', () => setConnected(true));
    newSocket.on('disconnect', () => setConnected(false));
    
    setSocket(newSocket);
    
    return () => {
      newSocket.close();
    };
  }, [url]);
  
  return { socket, connected };
}

// 7. Type-Safe API Client
import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
});

// Request interceptor for auth
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 8. Const Assertions (No Enums)
// ❌ WRONG: enum (creates runtime code)
enum Status { Active = 'active' }

// ✅ CORRECT: const assertion (zero runtime)
const Status = { Active: 'active', Inactive: 'inactive' } as const;
type Status = typeof Status[keyof typeof Status];

// 9. Error Boundary
import { Component, type ReactNode, type ErrorInfo } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('Error caught:', error, info);
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback || <div>Something went wrong</div>;
    }
    return this.props.children;
  }
}

// 10. Conditional Rendering Pattern
// ✅ CORRECT: Early return pattern
function AgentList({ agents }: { agents: Agent[] }) {
  if (agents.length === 0) {
    return <EmptyState />;
  }
  
  return (
    <div>
      {agents.map((agent) => (
        <AgentCard key={agent.id} agent={agent} />
      ))}
    </div>
  );
}
```

## 📁 Project Structure

```
frontend/src/
├── components/                    # Reusable components
│   ├── agents/                    # Agent-specific components
│   │   ├── AgentCard.tsx          # Agent card display
│   │   ├── AgentForm.tsx          # Agent creation/edit form
│   │   └── AgentList.tsx          # Agent list with filters
│   ├── common/                    # Shared UI components
│   │   ├── Button.tsx             # Reusable button
│   │   ├── Input.tsx              # Form input
│   │   └── Modal.tsx              # Modal dialog
│   └── layout/                    # Layout components
│       ├── Header.tsx             # App header
│       └── Sidebar.tsx            # Navigation sidebar
├── hooks/                         # Custom React hooks
│   ├── useAgents.ts               # Agent data fetching
│   ├── useWebSocket.ts            # WebSocket connection
│   └── useAuth.ts                 # Authentication state
├── pages/                         # Route pages
│   ├── Dashboard.tsx              # Main dashboard
│   ├── AgentStudio.tsx            # Agent configuration
│   └── Analytics.tsx              # Analytics page
├── stores/                        # Zustand stores
│   ├── uiStore.ts                 # UI state (sidebar, theme)
│   └── authStore.ts               # Auth state (user, token)
├── api/                           # API client layer
│   ├── client.ts                  # Axios instance + interceptors
│   └── agents.ts                  # Agent API methods
├── types/                         # TypeScript types
│   ├── agent.ts                   # Agent types
│   └── user.ts                    # User types
├── utils/                         # Utility functions
│   └── formatters.ts              # Date, number formatters
├── App.tsx                        # Root component
└── main.tsx                       # Entry point
```

## 🔧 Core Patterns

### 1. Modern Component Pattern (React 19)

**No manual memoization - React Compiler handles optimization**

```typescript
import type { Agent } from '@/types/agent';

interface AgentCardProps {
  agent: Agent;
  onEdit?: (id: number) => void;
  onDelete?: (id: number) => void;
}

// ✅ CORRECT: No React.memo, no useCallback, no useMemo
export function AgentCard({ agent, onEdit, onDelete }: AgentCardProps) {
  // React Compiler optimizes these automatically
  const handleEdit = () => onEdit?.(agent.id);
  const handleDelete = () => {
    if (confirm('Delete this agent?')) {
      onDelete?.(agent.id);
    }
  };
  
  // Derived state - no useMemo needed
  const statusColor = agent.is_active ? 'green' : 'gray';
  
  return (
    <div className="border rounded-lg p-4">
      <h3 className="text-lg font-semibold">{agent.name}</h3>
      <p className="text-sm text-gray-600">{agent.description}</p>
      
      <div className="flex gap-2 mt-4">
        <button onClick={handleEdit}>Edit</button>
        <button onClick={handleDelete}>Delete</button>
      </div>
      
      <span className={`text-${statusColor}-500`}>
        {agent.is_active ? 'Active' : 'Inactive'}
      </span>
    </div>
  );
}

// ❌ WRONG: Over-optimization (unnecessary in React 19)
export const AgentCard = React.memo(({ agent, onEdit }: AgentCardProps) => {
  const handleEdit = useCallback(() => onEdit?.(agent.id), [onEdit, agent.id]);
  const statusColor = useMemo(
    () => agent.is_active ? 'green' : 'gray',
    [agent.is_active]
  );
  // ... This is now unnecessary complexity!
});
```

**Troubleshooting**:
- **Re-rendering issues** → React Compiler handles this; check if you're mutating props
- **Performance still slow** → Profile first, optimize only critical paths manually
- **When to use manual memo** → Only for expensive computations (>50ms)

---

### 2. TanStack Query V5 Pattern

**Breaking changes from V4:**
- `isLoading` → `isPending`
- `cacheTime` → `gcTime`
- `onSuccess`/`onError` removed from queries
- `queryKey` must be array

```typescript
// hooks/useAgents.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { agentsApi } from '@/api/agents';
import type { AgentCreate, AgentUpdate } from '@/types/agent';

// ✅ CORRECT: V5 syntax
export function useAgents() {
  return useQuery({
    queryKey: ['agents'],  // Array required
    queryFn: agentsApi.getAll,
    staleTime: 5 * 60 * 1000,  // 5 minutes
    gcTime: 10 * 60 * 1000,    // Note: gcTime not cacheTime
  });
}

export function useAgent(id: number) {
  return useQuery({
    queryKey: ['agents', id],
    queryFn: () => agentsApi.getById(id),
    enabled: !!id,  // Only fetch if id exists
  });
}

export function useCreateAgent() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: AgentCreate) => agentsApi.create(data),
    onSuccess: () => {
      // Invalidate cache to refetch
      queryClient.invalidateQueries({ queryKey: ['agents'] });
    },
    // 🔒 Error handling in component, not here
  });
}

export function useUpdateAgent() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: AgentUpdate }) =>
      agentsApi.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['agents'] });
      queryClient.invalidateQueries({ queryKey: ['agents', variables.id] });
    },
  });
}

// Usage in component
function AgentList() {
  const { data: agents, isPending, error } = useAgents();  // Note: isPending
  const createMutation = useCreateAgent();
  
  if (isPending) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  const handleCreate = async (data: AgentCreate) => {
    try {
      await createMutation.mutateAsync(data);
      alert('Agent created!');
    } catch (err) {
      alert('Failed to create agent');
    }
  };
  
  return <div>{/* ... */}</div>;
}

// ❌ WRONG: V4 syntax (will error in V5)
export function useAgentsOld() {
  return useQuery(
    'agents',  // String key not allowed
    agentsApi.getAll,
    {
      cacheTime: 10000,  // Property doesn't exist
      onSuccess: () => {},  // Removed from queries
    }
  );
}
```

**Troubleshooting**:
- **"queryKey must be array"** → Change `'agents'` to `['agents']`
- **"cacheTime not found"** → Use `gcTime` instead
- **onSuccess not working** → Move to `mutateAsync().then()` in component

---

### 3. Form Pattern (React Hook Form + Zod)

```typescript
// components/agents/AgentForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { AgentCreate } from '@/types/agent';

// Zod schema with validation
const agentSchema = z.object({
  name: z.string().min(1, 'Name required').max(100, 'Name too long'),
  description: z.string().max(500).optional(),
  model_name: z.string().regex(/^(claude|gpt)-/, 'Invalid model'),
  temperature: z.number().min(0).max(2).default(0.7),
  max_tokens: z.number().int().min(1).max(100000).default(4096),
  planning_enabled: z.boolean().default(true),
});

type AgentFormData = z.infer<typeof agentSchema>;

interface AgentFormProps {
  initialData?: Partial<AgentFormData>;
  onSubmit: (data: AgentFormData) => void;
  onCancel?: () => void;
}

export function AgentForm({ initialData, onSubmit, onCancel }: AgentFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<AgentFormData>({
    resolver: zodResolver(agentSchema),
    defaultValues: initialData || {
      temperature: 0.7,
      max_tokens: 4096,
      planning_enabled: true,
    },
  });
  
  const handleFormSubmit = async (data: AgentFormData) => {
    try {
      await onSubmit(data);
      reset();
    } catch (error) {
      console.error('Form submission error:', error);
    }
  };
  
  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
      {/* Name field */}
      <div>
        <label htmlFor="name" className="block text-sm font-medium">
          Name *
        </label>
        <input
          id="name"
          {...register('name')}
          className="mt-1 block w-full rounded-md border-gray-300"
        />
        {errors.name && (
          <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
        )}
      </div>
      
      {/* Description field */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium">
          Description
        </label>
        <textarea
          id="description"
          {...register('description')}
          rows={3}
          className="mt-1 block w-full rounded-md border-gray-300"
        />
      </div>
      
      {/* Model selection */}
      <div>
        <label htmlFor="model_name" className="block text-sm font-medium">
          Model *
        </label>
        <select
          id="model_name"
          {...register('model_name')}
          className="mt-1 block w-full rounded-md border-gray-300"
        >
          <option value="claude-sonnet-4-5-20250929">Claude Sonnet 4.5</option>
          <option value="claude-haiku-4-20250508">Claude Haiku 4</option>
          <option value="gpt-4-turbo">GPT-4 Turbo</option>
        </select>
        {errors.model_name && (
          <p className="mt-1 text-sm text-red-600">{errors.model_name.message}</p>
        )}
      </div>
      
      {/* Temperature slider */}
      <div>
        <label htmlFor="temperature" className="block text-sm font-medium">
          Temperature: {/* Display current value */}
        </label>
        <input
          id="temperature"
          type="range"
          min="0"
          max="2"
          step="0.1"
          {...register('temperature', { valueAsNumber: true })}
          className="mt-1 block w-full"
        />
      </div>
      
      {/* Planning checkbox */}
      <div className="flex items-center">
        <input
          id="planning_enabled"
          type="checkbox"
          {...register('planning_enabled')}
          className="h-4 w-4 rounded border-gray-300"
        />
        <label htmlFor="planning_enabled" className="ml-2 text-sm">
          Enable planning system
        </label>
      </div>
      
      {/* Actions */}
      <div className="flex gap-2">
        <button
          type="submit"
          disabled={isSubmitting}
          className="px-4 py-2 bg-blue-600 text-white rounded-md"
        >
          {isSubmitting ? 'Saving...' : 'Save Agent'}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 bg-gray-200 rounded-md"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
```

**Troubleshooting**:
- **Validation not working** → Check `resolver: zodResolver(schema)` is set
- **Form not submitting** → Verify `handleSubmit` wraps your handler
- **Type errors** → Use `z.infer<typeof schema>` for form data type

---

### 4. Zustand Store Pattern (V5)

```typescript
// stores/uiStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface UIStore {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  notifications: Notification[];
  
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  addNotification: (notification: Notification) => void;
  removeNotification: (id: string) => void;
}

// ✅ CORRECT: V5 syntax with middleware
export const useUIStore = create<UIStore>()(
  devtools(
    persist(
      (set) => ({
        sidebarOpen: true,
        theme: 'light',
        notifications: [],
        
        toggleSidebar: () =>
          set((state) => ({ sidebarOpen: !state.sidebarOpen })),
        
        setTheme: (theme) => set({ theme }),
        
        addNotification: (notification) =>
          set((state) => ({
            notifications: [...state.notifications, notification],
          })),
        
        removeNotification: (id) =>
          set((state) => ({
            notifications: state.notifications.filter((n) => n.id !== id),
          })),
      }),
      { name: 'ui-store' }  // LocalStorage key
    )
  )
);

// Usage in components
function Sidebar() {
  const { sidebarOpen, toggleSidebar } = useUIStore();
  
  // 🔒 Only re-renders when sidebarOpen changes
  return (
    <div className={sidebarOpen ? 'open' : 'closed'}>
      <button onClick={toggleSidebar}>Toggle</button>
    </div>
  );
}

// Selector for specific state
function ThemeToggle() {
  const theme = useUIStore((state) => state.theme);
  const setTheme = useUIStore((state) => state.setTheme);
  
  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
}
```

---

### 5. WebSocket Pattern

```typescript
// hooks/useWebSocket.ts
import { useEffect, useState, useCallback } from 'react';
import { io, type Socket } from 'socket.io-client';

interface UseWebSocketReturn {
  socket: Socket | null;
  connected: boolean;
  emit: (event: string, data: any) => void;
}

export function useWebSocket(url: string): UseWebSocketReturn {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);
  
  useEffect(() => {
    const newSocket = io(url, {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });
    
    newSocket.on('connect', () => {
      console.log('WebSocket connected');
      setConnected(true);
    });
    
    newSocket.on('disconnect', () => {
      console.log('WebSocket disconnected');
      setConnected(false);
    });
    
    setSocket(newSocket);
    
    return () => {
      newSocket.close();
    };
  }, [url]);
  
  const emit = useCallback(
    (event: string, data: any) => {
      if (socket?.connected) {
        socket.emit(event, data);
      }
    },
    [socket]
  );
  
  return { socket, connected, emit };
}

// Usage in component
function ExecutionMonitor({ executionId }: { executionId: number }) {
  const { socket, connected } = useWebSocket('http://localhost:8000');
  const [progress, setProgress] = useState(0);
  
  useEffect(() => {
    if (!socket) return;
    
    socket.emit('subscribe', { executionId });
    
    socket.on('progress', (data) => {
      setProgress(data.progress);
    });
    
    return () => {
      socket.off('progress');
      socket.emit('unsubscribe', { executionId });
    };
  }, [socket, executionId]);
  
  return (
    <div>
      {connected ? '🟢 Connected' : '🔴 Disconnected'}
      <div>Progress: {progress}%</div>
    </div>
  );
}
```

---

## 🎯 Best Practices Summary

### DO ✅
- Use React Compiler - no manual memoization needed
- Use TanStack Query V5 syntax (`isPending`, `gcTime`, array queryKeys)
- Use Zod for schema validation
- Use const assertions instead of enums
- Use TypeScript strict mode
- Use error boundaries for error handling
- Use Zustand for global state
- Use React Hook Form for complex forms

### DON'T ❌
- Don't use `React.memo()`, `useMemo()`, `useCallback()` unless profiled as necessary
- Don't use V4 TanStack Query syntax
- Don't use enums (use const assertions)
- Don't mutate state directly
- Don't skip TypeScript types
- Don't use any (use unknown and type guards)

---

## 📚 See Also

- **reference.md** - Complete React/TypeScript API reference
- **examples.md** - Full working component examples
- **fastapi-patterns** - Backend API integration
- **deepagents-integration** - Agent management integration
