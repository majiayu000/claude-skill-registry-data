---
name: react-clean-architecture
description: Clean Architecture for React Native (Expo) with TypeScript and Bun. Use this skill when creating features, refactoring code, or reviewing code in React Native projects. Enforces strict separation between Core (domain), Infrastructure (adapters), and UI layers. Implements ports/adapters pattern, Result pattern for errors, and atomic design for components.
---

# React Clean Architecture

Prescriptive architecture for React Native (Expo) applications with TypeScript and Bun.

**Stack:** React Native (Expo) • TypeScript • Bun • Zustand (client state) • React Query (server state)

**Patterns:** Ports/Adapters • Use Cases • Result Pattern • ViewModel • Atomic Design

## Core Principle

**Core depends on NOTHING.** UI and Infrastructure can import from Core, never the other way around.

```
UI ──────────────┐
                 ├──▶ Core (entities, use cases, ports)
Infrastructure ──┘
```

## Project Structure

```
src/
├── ui/                              # Global components and hooks
│   ├── components/                  # Atomic Design
│   │   ├── atoms/                   # e.g., Button, Text, Icon
│   │   ├── molecules/               # e.g., InputField, Card
│   │   ├── organisms/               # e.g., Header, Form
│   │   └── templates/               # e.g., PageLayout
│   ├── hooks/                       # Global hooks (useToggle, useDebounce)
│   └── theme/                       # Palette, fonts, spacing
│
├── modules/
│   ├── [bounded-context]/           # e.g., authentication, events, profile
│   │   ├── core/                    # Pure domain (no external dependencies)
│   │   │   ├── entities/            # Business types/interfaces
│   │   │   │   └── User.entity.ts
│   │   │   ├── ports/               # Interfaces (contracts)
│   │   │   │   └── AuthRepository.port.ts
│   │   │   └── usecases/            # Business logic
│   │   │       └── Login.usecase.ts
│   │   │
│   │   ├── infrastructure/          # Port implementations
│   │   │   └── adapters/
│   │   │       └── AuthApi.adapter.ts
│   │   │
│   │   └── ui/                      # React-specific for this context
│   │       ├── components/          # e.g., AuthenticationCard
│   │       ├── screens/             # e.g., LoginScreen.tsx
│   │       ├── hooks/               # e.g., useAuthentication.tsx
│   │       ├── stores/              # Zustand stores
│   │       │   └── auth.store.ts
│   │       └── viewModels/          # UI orchestration
│   │           └── useLogin.viewModel.tsx
│   │
│   ├── shared/                      # Shared code between bounded contexts
│   │   ├── analytics/
│   │   ├── storage/
│   │   ├── toaster/
│   │   └── utils/
│   │
│   └── app/                         # Application configuration
│       ├── dependencies/
│       │   ├── Dependencies.type.ts
│       │   ├── dependencies.dev.ts
│       │   ├── dependencies.prod.ts
│       │   └── dependencies.test-env.ts
│       ├── react/
│       │   ├── useDependencies.tsx
│       │   ├── render.tsx
│       │   └── renderHook.tsx
│       └── main.ts
│
├── constants/                       # TestIDs, screen names
├── types/                           # General types (ISO8601, DeepPartial)
└── utils/                           # Utility functions
    ├── strings/
    │   └── firstCharToUppercase.ts
    └── dates/
        └── isISO8601Before.ts
```

## File Naming Conventions

| Type                 | Extension        | Example                  |
| -------------------- | ---------------- | ------------------------ |
| Entity               | `.entity.ts`     | `User.entity.ts`         |
| Port                 | `.port.ts`       | `AuthRepository.port.ts` |
| Use Case             | `.usecase.ts`    | `Login.usecase.ts`       |
| Adapter              | `.adapter.ts`    | `AuthApi.adapter.ts`     |
| ViewModel            | `.viewModel.tsx` | `useLogin.viewModel.tsx` |
| Store                | `.store.ts`      | `auth.store.ts`          |
| Model (API response) | `.model.ts`      | `LoginResponse.model.ts` |

React components: `PascalCase.tsx` (e.g., `LoginScreen.tsx`, `AuthenticationCard.tsx`)

## Layer Rules

### Core (`/modules/[context]/core/`)

Core is **pure and unaware of the outside world**.

```
✅ Defines entities (types/interfaces)
✅ Defines ports (dependency interfaces)
✅ Contains use cases (business logic)
✅ Uses Result pattern for errors
✅ Can import from: types/, utils/, other files in the same core

❌ NEVER import from infrastructure/
❌ NEVER import from ui/
❌ NEVER depend on React
❌ NEVER call APIs directly
```

### Infrastructure (`/modules/[context]/infrastructure/`)

Implements ports defined in Core.

```
✅ Adapters implement ports
✅ Handles API calls, storage, external services
✅ Transforms external data → Core entities
✅ Returns Result<T, E>
✅ Can import from: core/ (ports, entities)

❌ NEVER contains business logic (just transformation/mapping)
❌ NEVER import from ui/
```

### UI (`/modules/[context]/ui/`)

Everything React-specific for the bounded context.

```
✅ Screens, components, hooks specific to the context
✅ ViewModels orchestrate: use cases → stores
✅ Zustand stores for client state
✅ Can import from: core/ (entities, use cases, ports)
✅ Can call an adapter directly for simple CRUD (via React Query)

❌ NEVER business logic in components
❌ NEVER business logic in viewModels (delegate to use cases)
```

**When to use a Use Case vs direct Adapter?**

| Situation                                 | Approach                     |
| ----------------------------------------- | ---------------------------- |
| Simple fetch, basic CRUD                  | Direct adapter + React Query |
| Business logic, validation, orchestration | Use Case                     |

```typescript
// ✅ Simple CRUD → direct adapter
const { itemRepository } = useDependencies();
const query = useQuery({
  queryKey: ["item", id],
  queryFn: () => itemRepository.getById(id),
});

// ✅ Business logic → use case
const { authRepository } = useDependencies();
const result = await new LoginUseCase(authRepository).execute({
  email,
  password,
});
```

## Result Pattern

Explicit handling of successes and errors without exceptions.

```typescript
// types/Result.ts
type Success<T> = { success: true; data: T };
type Failure<E> = { success: false; error: E };
type Result<T, E = Error> = Success<T> | Failure<E>;

const ok = <T>(data: T): Success<T> => ({ success: true, data });
const fail = <E>(error: E): Failure<E> => ({ success: false, error });

export { Result, Success, Failure, ok, fail };
```

Usage in a use case:

```typescript
// modules/authentication/core/usecases/Login.usecase.ts
import { Result, ok, fail } from "@/types/Result";
import { User } from "../entities/User.entity";
import { AuthRepository } from "../ports/AuthRepository.port";
import { AuthError } from "../entities/AuthError.entity";

interface LoginParams {
  email: string;
  password: string;
}

export class LoginUseCase {
  constructor(private authRepository: AuthRepository) {}

  async execute(params: LoginParams): Promise<Result<User, AuthError>> {
    const result = await this.authRepository.login(params);

    if (!result.success) {
      return fail(result.error);
    }

    // Business logic here if needed
    return ok(result.data);
  }
}
```

Usage in a viewModel:

```typescript
// modules/authentication/ui/viewModels/useLogin.viewModel.tsx
import { LoginUseCase } from "../../core/usecases/Login.usecase";

export const useLoginViewModel = () => {
  const { authRepository } = useDependencies();
  const [state, setState] = useState<LoginState>({ status: "idle" });

  const handlers = {
    login: async (email: string, password: string) => {
      setState({ status: "loading" });

      const result = await new LoginUseCase(authRepository).execute({
        email,
        password,
      });

      if (result.success) {
        setState({ status: "success", user: result.data });
      } else {
        setState({ status: "error", error: result.error });
      }
    },
  };

  return { state, handlers };
};
```

## React Query

React Query handles **server state** (remote data, cache, synchronization).

### Where to place React Query hooks?

`useQuery` / `useMutation` hooks live in the **viewModel** or in **dedicated hooks** within the bounded context.

```
modules/[context]/ui/
├── hooks/
│   ├── useItems.query.ts       # Reusable query
│   └── useCreateItem.mutation.ts
└── viewModels/
    └── useItemList.viewModel.tsx  # Can contain inline queries
```

### Query Keys

Use a factory object for consistency and autocompletion:

```typescript
// modules/items/ui/hooks/items.queryKeys.ts
export const itemsKeys = {
  all: ["items"] as const,
  lists: () => [...itemsKeys.all, "list"] as const,
  list: (filters: ItemFilters) => [...itemsKeys.lists(), filters] as const,
  details: () => [...itemsKeys.all, "detail"] as const,
  detail: (id: string) => [...itemsKeys.details(), id] as const,
};
```

### Query Hook

```typescript
// modules/items/ui/hooks/useItem.query.ts
import { useQuery } from "@tanstack/react-query";
import { useDependencies } from "@app/react/useDependencies";
import { itemsKeys } from "./items.queryKeys";

export const useItemQuery = (id: string) => {
  const { itemRepository } = useDependencies();

  return useQuery({
    queryKey: itemsKeys.detail(id),
    queryFn: () => itemRepository.getById(id),
    enabled: !!id,
  });
};
```

### Mutation Hook

```typescript
// modules/items/ui/hooks/useCreateItem.mutation.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useDependencies } from "@app/react/useDependencies";
import { CreateItemUseCase } from "../../core/usecases/CreateItem.usecase";
import { itemsKeys } from "./items.queryKeys";

export const useCreateItemMutation = () => {
  const { itemRepository } = useDependencies();
  const queryClient = useQueryClient();

  const createItemUseCase = new CreateItemUseCase(itemRepository);

  return useMutation({
    mutationFn: (params: CreateItemParams) => createItemUseCase.execute(params),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: itemsKeys.lists() });
    },
  });
};
```

### Usage in a ViewModel

```typescript
// modules/items/ui/viewModels/useItemList.viewModel.tsx
import { useItemsQuery } from "../hooks/useItems.query";
import { useCreateItemMutation } from "../hooks/useCreateItem.mutation";

export const useItemListViewModel = () => {
  const itemsQuery = useItemsQuery();
  const createItemMutation = useCreateItemMutation();

  const state = {
    items: itemsQuery.data ?? [],
    isLoading: itemsQuery.isLoading,
    error: itemsQuery.error,
  };

  const handlers = {
    createItem: (params: CreateItemParams) => createItemMutation.mutate(params),
    refresh: () => itemsQuery.refetch(),
  };

  return { state, handlers };
};
```

### React Query Conventions

| Rule                                    | Example                                |
| --------------------------------------- | -------------------------------------- |
| Query hook naming                       | `use[Entity].query.ts`                 |
| Mutation hook naming                    | `use[Action][Entity].mutation.ts`      |
| Query keys naming                       | `[entity].queryKeys.ts`                |
| Always invalidate after mutation        | `queryClient.invalidateQueries()`      |
| Use case in mutation if business logic  | `new CreateItemUseCase(...).execute()` |
| Direct adapter in query if simple fetch | `repository.getById(id)`               |

## Dependency Injection

Dependency injection system based on React Context, with environment-based configuration.

### Structure

```
modules/app/
├── dependencies/
│   ├── Dependencies.type.ts      # Dependencies interface
│   ├── dependencies.dev.ts       # Development implementation
│   ├── dependencies.prod.ts      # Production implementation
│   └── dependencies.test-env.ts  # Test implementation
├── react/
│   ├── useDependencies.tsx       # Dependencies access hook
│   └── DependenciesProvider.tsx  # React provider
└── main.ts                       # Application bootstrap
```

### Dependencies.type.ts

Defines the contract of available dependencies in the app:

```typescript
// modules/app/dependencies/Dependencies.type.ts
import { AuthRepository } from "@modules/authentication/core/ports/AuthRepository.port";
import { ItemRepository } from "@modules/items/core/ports/ItemRepository.port";
import { StorageService } from "@modules/shared/storage/Storage.port";

export interface Dependencies {
  // Repositories
  authRepository: AuthRepository;
  itemRepository: ItemRepository;

  // Services
  storageService: StorageService;
}
```

### Environment-based implementations

```typescript
// modules/app/dependencies/dependencies.prod.ts
import { Dependencies } from "./Dependencies.type";
import { AuthApiAdapter } from "@modules/authentication/infrastructure/adapters/AuthApi.adapter";
import { ItemApiAdapter } from "@modules/items/infrastructure/adapters/ItemApi.adapter";
import { AsyncStorageAdapter } from "@modules/shared/storage/AsyncStorage.adapter";

export const prodDependencies: Dependencies = {
  authRepository: new AuthApiAdapter(),
  itemRepository: new ItemApiAdapter(),
  storageService: new AsyncStorageAdapter(),
};
```

```typescript
// modules/app/dependencies/dependencies.test-env.ts
import { Dependencies } from "./Dependencies.type";
import { AuthInMemoryAdapter } from "@modules/authentication/infrastructure/adapters/AuthInMemory.adapter";
import { ItemInMemoryAdapter } from "@modules/items/infrastructure/adapters/ItemInMemory.adapter";
import { InMemoryStorageAdapter } from "@modules/shared/storage/InMemoryStorage.adapter";

export const testDependencies: Dependencies = {
  authRepository: new AuthInMemoryAdapter(),
  itemRepository: new ItemInMemoryAdapter(),
  storageService: new InMemoryStorageAdapter(),
};
```

### main.ts

Application bootstrap with environment-based dependency selection:

```typescript
// modules/app/main.ts
import { Dependencies } from "@app/dependencies/Dependencies.type";

export class Main {
  public dependencies: Dependencies;

  constructor() {
    this.dependencies = this.setupDependencies();
  }

  setupDependencies(): Dependencies {
    let importPath;
    let dependencies: Dependencies;

    switch (process.env.NODE_ENV) {
      case "production":
        importPath = require("@app/dependencies/dependencies.prod");
        dependencies = importPath.prodDependencies;
        break;
      case "test":
        importPath = require("@app/dependencies/dependencies.test-env");
        dependencies = importPath.testDependencies;
        break;
      default:
      case "development":
        importPath = require("@app/dependencies/dependencies.dev");
        dependencies = importPath.devDependencies;
        break;
    }

    return dependencies;
  }
}

export const app = new Main();
```

### React Provider

```typescript
// modules/app/react/DependenciesProvider.tsx
import { createContext, ReactNode } from "react";
import { Dependencies } from "@app/dependencies/Dependencies.type";
import { app } from "@app/main";

export const DependenciesContext = createContext<Dependencies | null>(null);

export const DependenciesProvider = ({
  children,
  dependencies,
}: {
  children: ReactNode;
  dependencies?: Partial<Dependencies>;
}) => (
  <DependenciesContext.Provider
    value={{ ...app.dependencies, ...dependencies }}
  >
    {children}
  </DependenciesContext.Provider>
);
```

### useDependencies Hook

```typescript
// modules/app/react/useDependencies.tsx
import { useContext } from "react";
import { DependenciesContext } from "./DependenciesProvider";
import { Dependencies } from "@app/dependencies/Dependencies.type";

export const useDependencies = (): Dependencies => {
  const dependencies = useContext(DependenciesContext);

  if (!dependencies) {
    throw new Error("useDependencies must be used within DependenciesProvider");
  }

  return dependencies;
};
```

### Usage

```typescript
// In a viewModel or hook
const { authRepository, storageService } = useDependencies();

// In a test — partial override, other dependencies remain real
render(
  <DependenciesProvider dependencies={{ authRepository: mockAuthRepo }}>
    <ComponentUnderTest />
  </DependenciesProvider>
);
```

## Workflows

### Creating a new feature

**Example: "Create an event" feature in the `events` bounded context**

#### Step 1: Core — Entities

Define business types.

```typescript
// modules/events/core/entities/Event.entity.ts
export interface Event {
  id: string;
  title: string;
  date: ISO8601;
  organizerId: string;
}

// modules/events/core/entities/EventError.entity.ts
export type EventError =
  | { type: "VALIDATION_ERROR"; message: string }
  | { type: "NETWORK_ERROR" }
  | { type: "UNAUTHORIZED" };
```

#### Step 2: Core — Port

Define the repository contract.

```typescript
// modules/events/core/ports/EventRepository.port.ts
import { Result } from "@/types/Result";
import { Event, EventError } from "../entities/Event.entity";

export interface CreateEventParams {
  title: string;
  date: ISO8601;
}

export interface EventRepository {
  create(params: CreateEventParams): Promise<Result<Event, EventError>>;
  getById(id: string): Promise<Result<Event, EventError>>;
  list(): Promise<Result<Event[], EventError>>;
}
```

#### Step 3: Core — Use Case (if business logic needed)

```typescript
// modules/events/core/usecases/CreateEvent.usecase.ts
import { Result, ok, fail } from "@/types/Result";
import { Event, EventError } from "../entities/Event.entity";
import {
  EventRepository,
  CreateEventParams,
} from "../ports/EventRepository.port";

export class CreateEventUseCase {
  constructor(private eventRepository: EventRepository) {}

  async execute(params: CreateEventParams): Promise<Result<Event, EventError>> {
    // Business validation
    if (params.title.length < 3) {
      return fail({ type: "VALIDATION_ERROR", message: "Title too short" });
    }

    if (new Date(params.date) < new Date()) {
      return fail({
        type: "VALIDATION_ERROR",
        message: "Date must be in future",
      });
    }

    return this.eventRepository.create(params);
  }
}
```

#### Step 4: Infrastructure — Adapter

Implement the port.

```typescript
// modules/events/infrastructure/adapters/EventApi.adapter.ts
import { Result, ok, fail } from "@/types/Result";
import { Event, EventError } from "../../core/entities/Event.entity";
import {
  EventRepository,
  CreateEventParams,
} from "../../core/ports/EventRepository.port";
import { EventApiResponse } from "./EventApiResponse.model";

export class EventApiAdapter implements EventRepository {
  private baseUrl = "https://api.example.com";

  async create(params: CreateEventParams): Promise<Result<Event, EventError>> {
    try {
      const response = await fetch(`${this.baseUrl}/events`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params),
      });

      if (!response.ok) {
        return fail({ type: "NETWORK_ERROR" });
      }

      const data: EventApiResponse = await response.json();
      return ok(this.mapToEntity(data));
    } catch {
      return fail({ type: "NETWORK_ERROR" });
    }
  }

  private mapToEntity(response: EventApiResponse): Event {
    return {
      id: response.id,
      title: response.title,
      date: response.date,
      organizerId: response.organizer_id, // snake_case → camelCase
    };
  }

  // ... other methods
}
```

#### Step 5: Register the dependency

```typescript
// modules/app/dependencies/Dependencies.type.ts
import { EventRepository } from "@modules/events/core/ports/EventRepository.port";

export interface Dependencies {
  // ... others
  eventRepository: EventRepository;
}

// modules/app/dependencies/dependencies.prod.ts
import { EventApiAdapter } from "@modules/events/infrastructure/adapters/EventApi.adapter";

export const prodDependencies: Dependencies = {
  // ... others
  eventRepository: new EventApiAdapter(),
};
```

#### Step 6: UI — Query Keys

```typescript
// modules/events/ui/hooks/events.queryKeys.ts
export const eventsKeys = {
  all: ["events"] as const,
  lists: () => [...eventsKeys.all, "list"] as const,
  details: () => [...eventsKeys.all, "detail"] as const,
  detail: (id: string) => [...eventsKeys.details(), id] as const,
};
```

#### Step 7: UI — Mutation Hook

```typescript
// modules/events/ui/hooks/useCreateEvent.mutation.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useDependencies } from "@app/react/useDependencies";
import { CreateEventUseCase } from "../../core/usecases/CreateEvent.usecase";
import { eventsKeys } from "./events.queryKeys";

export const useCreateEventMutation = () => {
  const { eventRepository } = useDependencies();
  const queryClient = useQueryClient();

  const createEventUseCase = new CreateEventUseCase(eventRepository);

  return useMutation({
    mutationFn: createEventUseCase.execute.bind(createEventUseCase),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: eventsKeys.lists() });
    },
  });
};
```

#### Step 8: UI — ViewModel

```typescript
// modules/events/ui/viewModels/useCreateEvent.viewModel.tsx
import { useState } from "react";
import { useCreateEventMutation } from "../hooks/useCreateEvent.mutation";

interface FormState {
  title: string;
  date: string;
}

export const useCreateEventViewModel = () => {
  const [form, setForm] = useState<FormState>({ title: "", date: "" });
  const mutation = useCreateEventMutation();

  const state = {
    form,
    isLoading: mutation.isPending,
    error: mutation.data?.success === false ? mutation.data.error : null,
  };

  const handlers = {
    setTitle: (title: string) => setForm((f) => ({ ...f, title })),
    setDate: (date: string) => setForm((f) => ({ ...f, date })),
    submit: () => mutation.mutate({ title: form.title, date: form.date }),
  };

  return { state, handlers };
};
```

#### Step 9: UI — Screen

```typescript
// modules/events/ui/screens/CreateEventScreen.tsx
import { useCreateEventViewModel } from "../viewModels/useCreateEvent.viewModel";

export const CreateEventScreen = () => {
  const { state, handlers } = useCreateEventViewModel();

  return (
    <View>
      <TextInput
        value={state.form.title}
        onChangeText={handlers.setTitle}
        placeholder="Event title"
      />
      <TextInput
        value={state.form.date}
        onChangeText={handlers.setDate}
        placeholder="YYYY-MM-DD"
      />
      {state.error && <Text>{state.error.message}</Text>}
      <Button
        title="Create"
        onPress={handlers.submit}
        disabled={state.isLoading}
      />
    </View>
  );
};
```

---

### Refactoring existing code

#### Identify violations

1. Business logic in a component or viewModel → extract to Use Case
2. Direct API call in a component → extract to Adapter
3. Inline type or `any` → create an Entity
4. Hardcoded dependency → extract to Port + Adapter

#### Refactoring process

```
1. Identify the violation
2. Create the target file (use case, adapter, entity)
3. Extract the code
4. Update imports
5. Verify Core doesn't import from UI/Infrastructure
6. Register new dependencies if needed
```

#### Example: extracting an API call from a component

**Before (violation):**

```typescript
// ❌ Direct API call in component
const EventList = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch("https://api.example.com/events")
      .then((r) => r.json())
      .then(setEvents);
  }, []);
};
```

**After (clean):**

```typescript
// ✅ Adapter + Query + ViewModel
const EventList = () => {
  const { state } = useEventListViewModel();

  return <FlatList data={state.events} />;
};
```

---

### Code Review Checklist

See [references/code-review-checklist.md](references/code-review-checklist.md) for the complete checklist.

## References

- [references/file-templates.md](references/file-templates.md) — Complete templates for each file type
- [references/code-review-checklist.md](references/code-review-checklist.md) — Code review checklist
