---
name: violet-dashboard
description: VioletDashboard code patterns and conventions
---

# VioletDashboard Code Patterns

## Overview

VioletDashboard is a Next.js application serving Channel and Merchant dashboards through subdomain routing.

**Tech Stack:**
- Next.js 12.x with React 17
- Redux Toolkit with Redux Persist
- SCSS modules
- TypeScript (strict)

**ALL patterns in this document are MANDATORY when working on VioletDashboard.**

---

## axiosWrapper Pattern (MANDATORY)

**ALWAYS use `axiosWrapper` for ALL HTTP requests. NEVER use `fetch` or vanilla `axios`.**

### Why axiosWrapper?

- **Automatic camelCase ↔ snake_case conversion**: Client uses camelCase, backend uses snake_case
- **Standardized error handling**: Consistent error format across application
- **Authentication injection**: Automatically includes auth headers
- **Retry logic**: Built-in retry for transient failures
- **Type safety**: Full TypeScript support with generics

### Client-Side vs Server-Side

```typescript
// Client-side (from browser/component)
const response = await axiosWrapper<PreRegistration[]>(
  CONFIG_TYPE.VIOLET_PROXY_API,  // Routes through Next.js API routes
  {
    method: 'GET',
    path: 'api/merchants/pre-registrations',
    params: { page: 0, size: 20 }
  }
);

// Server-side (from API route)
const response = await axiosWrapper<PreRegistration>(
  CONFIG_TYPE.VIOLET_API,  // Direct to backend
  {
    method: 'POST',
    path: 'merchants/external/pre-register',
    data: snakecaseKeys(requestBody),
    headers: {
      [VIOLET_TOKEN_HEADER]: token
    }
  }
);
```

### ❌ DON'T Use

```typescript
// ❌ WRONG - Vanilla axios
import axios from 'axios';
const response = await axios.get('/api/merchants/pre-registrations');

// ❌ WRONG - fetch
const response = await fetch('/api/merchants/pre-registrations');
const data = await response.json();

// ❌ WRONG - Direct backend call from client
const response = await axiosWrapper(
  CONFIG_TYPE.VIOLET_API,  // ❌ Client should use VIOLET_PROXY_API
  { method: 'GET', path: 'merchants/...' }
);
```

### ✅ DO Use

```typescript
// ✅ CORRECT - axiosWrapper with proper CONFIG_TYPE
import axiosWrapper, { CONFIG_TYPE } from '@/utilities/axiosWrapper';

// Client-side: through proxy
const response = await axiosWrapper<PreRegistration[]>(
  CONFIG_TYPE.VIOLET_PROXY_API,
  {
    method: 'GET',
    path: 'api/merchants/pre-registrations',
    params: { page: 0, size: 20 }
  }
);
```

---

## Redux Thunk Pattern (MANDATORY)

Use `createAppAsyncThunk` with `axiosWrapper`. Do NOT use `fetch` or standard `createAsyncThunk`.

```typescript
// redux/thunks/preRegistration.ts
import { createAppAsyncThunk, HasFulfilledMeta, HasRejectedMeta } from 'redux/thunks';
import axiosWrapper, { CONFIG_TYPE } from '@/utilities/axiosWrapper';
import { PreRegistrationActionType } from 'redux/actions/preRegistration';
import { PreRegistration, PreRegistrationListResult } from 'interfaces/preRegistration.interface';

// GET list - rejected meta only
export const getPreRegistrations = createAppAsyncThunk<
  PreRegistrationListResult,
  { page?: number; size?: number },
  HasRejectedMeta
>(
  PreRegistrationActionType.GET_PRE_REGISTRATIONS,
  async (params, { rejectWithValue }) => {
    try {
      const response = await axiosWrapper<PreRegistrationListResult>(
        CONFIG_TYPE.VIOLET_PROXY_API,
        {
          method: 'GET',
          path: 'api/merchants/pre-registrations',
          params,
        }
      );
      return response.data;
    } catch (err: any) {
      throw rejectWithValue(err, {
        errorMessage: err?.response?.data?.message || 'Failed to load pre-registrations',
      });
    }
  }
);

// POST create - fulfilled + rejected meta for success message
export const createPreRegistration = createAppAsyncThunk<
  PreRegistration,
  CreatePreRegistrationPayload,
  HasFulfilledMeta & HasRejectedMeta
>(
  PreRegistrationActionType.CREATE_PRE_REGISTRATION,
  async (data, { fulfillWithValue, rejectWithValue }) => {
    try {
      const response = await axiosWrapper<PreRegistration>(
        CONFIG_TYPE.VIOLET_PROXY_API,
        {
          method: 'POST',
          path: 'api/merchants/pre-register',
          data,
        }
      );
      return fulfillWithValue(response.data, {
        successMessage: 'Pre-registration created',
      });
    } catch (err: any) {
      throw rejectWithValue(err, {
        errorMessage: err?.response?.data?.message || 'Failed to create pre-registration',
      });
    }
  }
);

// PUT update - fulfilled + rejected meta
export const updatePreRegistration = createAppAsyncThunk<
  PreRegistration,
  UpdatePreRegistrationPayload,
  HasFulfilledMeta & HasRejectedMeta
>(
  PreRegistrationActionType.UPDATE_PRE_REGISTRATION,
  async ({ merchantId, ...data }, { fulfillWithValue, rejectWithValue }) => {
    try {
      const response = await axiosWrapper<PreRegistration>(
        CONFIG_TYPE.VIOLET_PROXY_API,
        {
          method: 'PUT',
          path: `api/merchants/pre-register/${merchantId}`,
          data,
        }
      );
      return fulfillWithValue(response.data, {
        successMessage: 'Pre-registration updated',
      });
    } catch (err: any) {
      throw rejectWithValue(err, {
        errorMessage: err?.response?.data?.message || 'Failed to update pre-registration',
      });
    }
  }
);

// DELETE - fulfilled + rejected meta
export const deletePreRegistration = createAppAsyncThunk<
  void,
  { merchantId: number },
  HasFulfilledMeta & HasRejectedMeta
>(
  PreRegistrationActionType.DELETE_PRE_REGISTRATION,
  async ({ merchantId }, { fulfillWithValue, rejectWithValue }) => {
    try {
      await axiosWrapper(CONFIG_TYPE.VIOLET_PROXY_API, {
        method: 'DELETE',
        path: `api/merchants/pre-register/${merchantId}`,
      });
      return fulfillWithValue(undefined, {
        successMessage: 'Pre-registration deleted',
      });
    } catch (err: any) {
      throw rejectWithValue(err, {
        errorMessage: err?.response?.data?.message || 'Failed to delete pre-registration',
      });
    }
  }
);
```

**Key points:**
- `CONFIG_TYPE.VIOLET_PROXY_API` for client-side calls (through Next.js API routes)
- `CONFIG_TYPE.VIOLET_API` for server-side calls (direct to backend)
- `rejectWithValue(err, { errorMessage })` enables automatic snackbar notifications
- `fulfillWithValue(data, { successMessage })` enables success notifications
- DELETE returns `void` (no response body expected)

---

## Redux Reducer Pattern (MANDATORY)

Use `createReducer` with `.addCase()`. Do NOT use `createSlice`.

```typescript
// redux/reducers/preRegistration.ts
import { createReducer } from '@reduxjs/toolkit';
import { PageableResult } from 'interfaces/pageable.interface';
import { PreRegistration } from 'interfaces/preRegistration.interface';
import {
  getPreRegistrations,
  createPreRegistration,
  updatePreRegistration,
  deletePreRegistration,
} from '../thunks/preRegistration';
import { clearPreRegistrations } from '../actions/preRegistration';
import withClearableState from '@/redux/reducers/withClearableState';

export interface PreRegistrationState {
  list: PreRegistration[];
  loading: boolean;
  totalElements: number;
  totalPages: number;
}

const initialState: PreRegistrationState = {
  list: [],
  loading: false,
  totalElements: 0,
  totalPages: 0,
};

const preRegistrationReducer = createReducer(initialState, (builder) => {
  builder
    // Loading states via thunk.pending (NOT manual dispatch)
    .addCase(getPreRegistrations.pending, (state) => {
      state.loading = true;
    })

    // Success states via thunk.fulfilled
    .addCase(getPreRegistrations.fulfilled, (state, action) => {
      state.loading = false;
      state.list = action.payload.content;
      state.totalElements = action.payload.totalElements;
      state.totalPages = action.payload.totalPages;
    })

    // Error states via thunk.rejected
    .addCase(getPreRegistrations.rejected, (state) => {
      state.loading = false;
    })

    .addCase(createPreRegistration.fulfilled, (state, action) => {
      state.list.unshift(action.payload);
      state.totalElements += 1;
    })

    .addCase(updatePreRegistration.fulfilled, (state, action) => {
      const index = state.list.findIndex((p) => p.merchantId === action.payload.merchantId);
      if (index !== -1) {
        state.list[index] = action.payload;
      }
    })

    .addCase(deletePreRegistration.fulfilled, (state, action) => {
      state.list = state.list.filter((p) => p.merchantId !== action.meta.arg.merchantId);
      state.totalElements -= 1;
    })

    // Synchronous clear action
    .addCase(clearPreRegistrations, () => initialState);
});

// Wrap for automatic cleanup on logout
export default withClearableState(preRegistrationReducer, initialState);
```

**Key points:**
- Use `.addCase(thunk.pending)` for loading - NOT manual `dispatch(startLoading())`
- Use `.addCase(thunk.fulfilled)` for success
- Use `.addCase(thunk.rejected)` for errors
- Wrap with `withClearableState` for logout cleanup
- State mutations are allowed (immer handles immutability)

---

## Redux Actions Pattern

Action types and synchronous actions only. Thunks go in `redux/thunks/`.

```typescript
// redux/actions/preRegistration.ts
import { createAction } from '@reduxjs/toolkit';

// Action type enum
export enum PreRegistrationActionType {
  GET_PRE_REGISTRATIONS = 'GET_PRE_REGISTRATIONS',
  CREATE_PRE_REGISTRATION = 'CREATE_PRE_REGISTRATION',
  UPDATE_PRE_REGISTRATION = 'UPDATE_PRE_REGISTRATION',
  DELETE_PRE_REGISTRATION = 'DELETE_PRE_REGISTRATION',
  CLEAR_PRE_REGISTRATIONS = 'CLEAR_PRE_REGISTRATIONS',
}

// Payload types namespace
export namespace PayloadType {
  export interface CreatePreRegistration {
    merchantName: string;
    storeUrl: string;
    clientId: string;
    secret: string;
    installLink: string;
  }
  export interface UpdatePreRegistration {
    merchantId: number;
    merchantName?: string;
    clientId?: string;
    secret?: string;
  }
}

// Synchronous actions only
export const clearPreRegistrations = createAction(
  PreRegistrationActionType.CLEAR_PRE_REGISTRATIONS
);
```

---

## API Route Pattern (MANDATORY)

Use `nextConnectConfiguration()` with `axiosWrapper`. Do NOT use custom middleware or `fetch`.

```typescript
// pages/api/merchants/pre-register/[id].ts
import type { NextApiRequest, NextApiResponse } from 'next';
import snakecaseKeys from 'snakecase-keys';
import { NextHandler } from 'next-connect';
import { VIOLET_TOKEN_HEADER } from '@violet/shared-types/constants/headers';
import axiosWrapper, { CONFIG_TYPE } from '@/utilities/axiosWrapper';
import { getTokenWithDecodedData } from '@/utilities/auth';
import { nextConnectConfiguration } from '@/middlewares/globalApiMiddleware';

const apiRoute = nextConnectConfiguration();

// GET handler
apiRoute.get(
  async (req: NextApiRequest, res: NextApiResponse, next: NextHandler) => {
    try {
      const tokenWithDecodedData = getTokenWithDecodedData(req, res);
      const { id } = req.query;

      const result = await axiosWrapper(CONFIG_TYPE.VIOLET_API, {
        method: 'GET',
        path: `merchants/external/pre-register/${id}`,
        headers: {
          [VIOLET_TOKEN_HEADER]: tokenWithDecodedData.token,
        },
      });

      res.status(result.status).json(result.data);
    } catch (err: any) {
      next(err); // Pass to central error handler
    }
  }
);

// PUT handler
apiRoute.put(
  async (req: NextApiRequest, res: NextApiResponse, next: NextHandler) => {
    try {
      const tokenWithDecodedData = getTokenWithDecodedData(req, res);
      const { id } = req.query;

      const result = await axiosWrapper(CONFIG_TYPE.VIOLET_API, {
        method: 'PUT',
        path: `merchants/external/pre-register/${id}`,
        headers: {
          [VIOLET_TOKEN_HEADER]: tokenWithDecodedData.token,
        },
        data: snakecaseKeys(req.body),
      });

      res.status(result.status).json(result.data);
    } catch (err: any) {
      next(err);
    }
  }
);

// DELETE handler
apiRoute.delete(
  async (req: NextApiRequest, res: NextApiResponse, next: NextHandler) => {
    try {
      const tokenWithDecodedData = getTokenWithDecodedData(req, res);
      const { id } = req.query;

      const result = await axiosWrapper(CONFIG_TYPE.VIOLET_API, {
        method: 'DELETE',
        path: `merchants/external/pre-register/${id}`,
        headers: {
          [VIOLET_TOKEN_HEADER]: tokenWithDecodedData.token,
        },
      });

      res.status(result.status).json(result.data);
    } catch (err: any) {
      next(err);
    }
  }
);

export default apiRoute;
```

**Key points:**
- `nextConnectConfiguration()` includes Helmet, CORS, auth middleware
- `getTokenWithDecodedData(req, res)` extracts auth from cookies
- `snakecaseKeys(req.body)` converts to backend format
- Pass errors to `next(err)` - NOT manual `res.status(500).json()`
- Response automatically converts snake_case to camelCase

---

## API Layer Constraints (MANDATORY)

**Next.js API routes in VioletDashboard MUST be lightweight proxies to the backend. NO business logic.**

This is the established architecture: "the whole reason the dashboard is structured the way it is."

### ❌ DON'T Add Business Logic

```typescript
// ❌ WRONG - Business logic in API route
export default async (req, res) => {
  const { id } = req.query;

  // ❌ NO - Data transformation
  const result = await axiosWrapper(CONFIG_TYPE.VIOLET_API, {
    method: 'GET',
    path: `merchants/external/pre-register/${id}`
  });

  // ❌ NO - Business logic here
  const transformed = {
    ...result.data,
    displayName: result.data.merchant_name,
    isActive: result.data.status === 'active',
    daysOld: calculateDaysOld(result.data.date_created)
  };

  res.status(200).json(transformed);
};
```

### ✅ DO Keep It Lightweight

```typescript
// ✅ CORRECT - Lightweight proxy
apiRoute.get(
  async (req: NextApiRequest, res: NextApiResponse, next: NextHandler) => {
    try {
      const tokenWithDecodedData = getTokenWithDecodedData(req, res);
      const { id } = req.query;

      // Pass through to backend - no transformation
      const result = await axiosWrapper(CONFIG_TYPE.VIOLET_API, {
        method: 'GET',
        path: `merchants/external/pre-register/${id}`,
        headers: {
          [VIOLET_TOKEN_HEADER]: tokenWithDecodedData.token,
        },
      });

      // Pass through response directly (camelCase conversion automatic)
      res.status(result.status).json(result.data);
    } catch (err: any) {
      next(err); // Pass to central error handler
    }
  }
);
```

### What API Routes Should Do

✅ **DO**:
- Authenticate requests (via `getTokenWithDecodedData`)
- Proxy requests to backend
- Convert camelCase ↔ snake_case (via `axiosWrapper` + `snakecaseKeys`)
- Pass through responses
- Handle errors via `next(err)`

❌ **DON'T**:
- Transform data formats
- Add computed fields
- Filter or sort data
- Implement business rules
- Cache responses (unless justified exception)

### Where Business Logic Belongs

| Logic Type | Location |
|-----------|----------|
| Data transformation | Client (components, selectors) |
| Business rules | Backend services |
| Computed values | Client (selectors, useMemo) |
| Filtering/sorting | Client (components) or backend (query params) |
| Validation | Backend (primary) + client (UX only) |

### Exceptions

The ONLY exceptions to lightweight proxy pattern:
- User management (existing pattern)
- Session handling (existing pattern)
- Explicit architectural justification documented in ADR

**If you're unsure, default to lightweight proxy.**

---

## Interface Organization

- **Shared interfaces** go in `interfaces/*.ts`
- **Component props** go INLINE in the component file

```typescript
// interfaces/preRegistration.interface.ts
import { PageableResult } from './pageable.interface';

export interface PreRegistration {
  merchantId: number;
  merchantName: string;
  storeUrl: string;
  status: PreRegistrationStatus;
  dateCreated: string;
}

export enum PreRegistrationStatus {
  PENDING = 'PENDING',
  ACTIVE = 'ACTIVE',
  FOR_DELETION = 'FOR_DELETION',
  EXPIRED = 'EXPIRED',
}

export type PreRegistrationListResult = PageableResult<PreRegistration>;
```

```typescript
// components/merchants/PreRegTable.tsx - Props inline
interface PreRegTableProps {
  data: PreRegistration[];
  loading: boolean;
  onEdit: (item: PreRegistration) => void;
  onDelete: (merchantId: number) => void;
}

export const PreRegTable: React.FC<PreRegTableProps> = ({ data, loading, onEdit, onDelete }) => {
  // Component implementation
};
```

---

## UI Component Policy: NO MATERIAL-UI (CRITICAL)

**VioletDashboard has STOPPED using Material-UI (MUI).** Do NOT create new components with MUI.

### Why No MUI?

1. **Design System Mismatch**: MUI creates problems matching VioletDashboard's custom design system
2. **Visual Inconsistency**: MUI components look different from existing designs
3. **Migration Complete**: VioletDashboard uses custom components with SCSS modules and CSS variables

### Instead of MUI, Use:

| DON'T Use (MUI) | DO Use (Custom Design System) |
|-----------------|-------------------------------|
| `<Tabs>`, `<Tab>` | Custom tabs with `<button>` + SCSS |
| `<Table>`, `<TableRow>`, `<TableCell>` | `<div>` with flexbox + SCSS modules |
| `<Dialog>`, `<DialogTitle>` | Custom modal with `<div>` + SCSS |
| `<TextField>`, `<Input>` | Custom input components |
| `<Button>` | `<button>` with SCSS (or `@/components/Button`) |
| `<IconButton>`, `<Tooltip>` | `<button>` with SCSS |
| `<Chip>` | `<span>` with SCSS classes |
| `<CircularProgress>` | `<Spinner>` component |
| `@mui/icons-material/*` | Figma SVG exports from `public/images/svg/` |

### Design System Patterns

**CSS Variables (use these):**
```scss
--primary-light          // Primary color
--secondary-color        // Borders, backgrounds
--text-color-tertiary    // Muted text
--button-background-color // Button fills
--border-default         // Standard borders
--light-gray             // Text color
```

**SCSS Modules:**
```scss
// MyComponent.module.scss
.container {
  background: var(--secondary-color);
  border: 1px solid var(--border-default);
}

.button {
  background: var(--button-background-color);
  color: var(--text-color);

  &:hover {
    background: var(--button-background-color-hover);
  }
}
```

**Icons:**
```typescript
// DON'T: Material-UI icons
import { ContentCopy, MoreVert } from '@mui/icons-material';

// DO: Figma SVG exports
import CopyIcon from '@/public/images/svg/copy.svg';
import ThreeDotsIcon from '@/public/images/svg/three-dots.svg';

// Usage
<button className={styles.iconButton}>
  <CopyIcon className={styles.icon} />
</button>
```

### Example: Tabs Without MUI

```typescript
// Custom tab navigation
const MerchantsTabNavigation = ({ activeTab, onTabChange }) => (
  <div className={styles.tabContainer}>
    <div className={styles.tabs}>
      <button
        className={`${styles.tab} ${activeTab === 'connected' ? styles.active : ''}`}
        onClick={() => onTabChange('connected')}
      >
        Connected Merchants
      </button>
      <button
        className={`${styles.tab} ${activeTab === 'pre-registered' ? styles.active : ''}`}
        onClick={() => onTabChange('pre-registered')}
      >
        Pre-Registered
      </button>
    </div>
  </div>
);
```

```scss
// MerchantsTabNavigation.module.scss
.tabContainer {
  border-bottom: 2px solid var(--secondary-color);
}

.tabs {
  display: flex;
}

.tab {
  background: none;
  border: none;
  cursor: pointer;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color-tertiary);

  &:hover {
    color: var(--primary-light);
  }

  &.active {
    color: var(--primary-light);

    &::after {
      content: '';
      position: absolute;
      bottom: -2px;
      left: 0;
      right: 0;
      height: 2px;
      background: var(--button-background-color);
    }
  }
}
```

---

## Anti-Patterns (DO NOT USE)

| Wrong | Correct |
|-------|---------|
| `@mui/material` imports | Custom components with SCSS modules |
| `@mui/icons-material` icons | Figma SVG exports from `public/images/svg/` |
| `fetch('/api/...')` | `axiosWrapper(CONFIG_TYPE.VIOLET_PROXY_API, {...})` |
| `createSlice({...})` | `createReducer(initialState, (builder) => {...})` |
| `createAsyncThunk()` | `createAppAsyncThunk<R, P, M>()` |
| `dispatch(setLoading(true))` | `.addCase(thunk.pending, ...)` in reducer |
| Props in `interfaces/` | Props inline in component file |
| Manual CORS/Helmet | `nextConnectConfiguration()` |
| `res.status(500).json({...})` | `next(err)` in API routes |
| `console.log()` in commits | Remove before PR |

---

## Path Aliases

Always use path aliases, not relative imports:

```typescript
// Correct
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';
import axiosWrapper from '@/utilities/axiosWrapper';

// Wrong
import { Button } from '../../../components/Button';
```

---

## Component Location

| Type | Location |
|------|----------|
| Reusable UI components | `components/` |
| Page-specific components | `pageComponents/` |
| Custom hooks | `hooks/` |
| Utilities | `utilities/` |
| Shared interfaces | `interfaces/` |
| Redux | `redux/actions/`, `redux/reducers/`, `redux/thunks/` |
