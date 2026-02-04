---
name: local-first
description: Enforces local-first architecture principles for Breath of Now. Use this skill when working with data, state management, or sync features. Ensures IndexedDB (Dexie.js) is always the source of truth.
---

# Local-First Architecture Skill

Este skill garante que todas as operações de dados no Breath of Now seguem o princípio **local-first**: dados do utilizador são armazenados localmente por defeito, com cloud sync como feature premium opcional.

## Arquitectura

```
┌─────────────────────────────────────────────────┐
│                   Browser                        │
│  ┌─────────────┐  ┌─────────────┐               │
│  │ IndexedDB   │  │ Zustand     │               │
│  │ (Dexie.js)  │  │ (State)     │               │
│  │ SOURCE OF   │  │ UI State    │               │
│  │ TRUTH       │  │ Only        │               │
│  └──────┬──────┘  └──────┬──────┘               │
│         │                │                       │
│         └────────┬───────┘                       │
│                  ▼                               │
│         ┌───────────────┐                        │
│         │  Sync Engine  │  (Premium only)        │
│         │  src/lib/sync │                        │
│         └───────┬───────┘                        │
└─────────────────┼───────────────────────────────┘
                  │ (quando online + autenticado + premium)
                  ▼
         ┌───────────────┐
         │   Supabase    │
         │  (OPCIONAL)   │
         └───────────────┘
```

## Quando Usar

Aplica este skill quando:
- Criar modelos de dados ou schemas
- Implementar operações CRUD
- Construir funcionalidade de sync
- Trabalhar com preferências do utilizador
- Tratar cenários offline

## Regras Fundamentais

### Regra 1: IndexedDB é SEMPRE a Source of Truth

```typescript
// ❌ ERRADO - Fetch directo do Supabase
const { data } = await supabase.from('expenses').select('*');
setExpenses(data);

// ✅ CORRECTO - Ler da BD local
import { db } from '@/lib/db';
const expenses = await db.expenses.toArray();
setExpenses(expenses);
```

### Regra 2: Escrever Localmente Primeiro, Sync Depois

```typescript
// ❌ ERRADO - Escrever na cloud primeiro
await supabase.from('expenses').insert(expense);

// ✅ CORRECTO - Escrever localmente, queue para sync
import { db } from '@/lib/db';

await db.expenses.add({
  ...expense,
  localId: crypto.randomUUID(),
  syncStatus: 'pending',
  createdAt: new Date(),
  updatedAt: new Date()
});

// O sync engine trata o push para cloud (se premium)
```

### Regra 3: App DEVE Funcionar 100% Offline

```typescript
// ❌ ERRADO - Requer network
if (!navigator.onLine) {
  return <p>You need internet connection</p>;
}

// ✅ CORRECTO - Funciona offline por defeito
const expenses = await db.expenses.toArray();
// Mostrar dados independentemente do estado de conexão
// Apenas mostrar indicador de status offline
```

### Regra 4: Sync é Premium Only

```typescript
// ✅ CORRECTO - Verificar status premium antes de sync
import { usePremium } from '@/hooks/use-premium';

const { isPremium } = usePremium();

if (isPremium && navigator.onLine) {
  await syncEngine.sync();
}
```

## Schema Dexie.js

Localização: `/src/lib/db/index.ts`

### Estrutura Actual

```typescript
import Dexie, { Table } from 'dexie';

// Expenses (ExpenseFlow)
export interface Expense {
  id?: number;
  localId: string;           // UUID para sync
  amount: number;
  currency: string;
  category: string;
  description?: string;
  date: string;
  tags?: string[];
  isRecurring?: boolean;
  
  // Sync metadata
  syncStatus: 'synced' | 'pending' | 'conflict';
  remoteId?: string;         // Supabase ID
  createdAt: string;
  updatedAt: string;
  syncedAt?: string;
}

// FitLog
// Ver src/lib/db/fitlog-db.ts

export class BreathOfNowDB extends Dexie {
  expenses!: Table<Expense>;
  userPreferences!: Table<UserPreferences>;

  constructor() {
    super('breathofnow');
    this.version(1).stores({
      expenses: '++id, localId, date, category, syncStatus',
      userPreferences: '++id, key'
    });
  }
}

export const db = new BreathOfNowDB();
```

## State Management com Zustand

Zustand é para **UI state apenas**, não para persistência de dados:

```typescript
// ✅ CORRECTO - UI state em Zustand
interface AppStore {
  // Estado de sessão
  user: User | null;
  theme: 'light' | 'dark' | 'system';
  
  // UI state
  isSidebarOpen: boolean;
  activeApp: string | null;
  isLoading: boolean;
  
  // Actions
  setTheme: (theme: Theme) => void;
  toggleSidebar: () => void;
}

// ❌ ERRADO - Não guardar dados em Zustand
interface AppStore {
  expenses: Expense[];  // NÃO! Usar Dexie
  transactions: Transaction[];  // NÃO! Usar Dexie
}
```

## Sync Engine

Localização: `/src/lib/sync/`

### Estrutura

```
src/lib/sync/
├── index.ts      # Exportações principais
├── push.ts       # Push de dados locais para cloud
├── pull.ts       # Pull de dados da cloud
├── conflict.ts   # Resolução de conflitos
└── queue.ts      # Queue de operações pendentes
```

### Padrão de Uso

```typescript
import { useSync } from '@/hooks/use-sync';

function MyComponent() {
  const { syncStatus, lastSyncTime, triggerSync } = useSync();
  
  return (
    <div>
      <SyncStatus status={syncStatus} />
      <p>{t('lastSync', { time: lastSyncTime })}</p>
      <Button onClick={triggerSync}>{t('syncNow')}</Button>
    </div>
  );
}
```

## Indicador Offline

```typescript
// Componente existente: src/components/pwa/connectivity-status.tsx

import { ConnectivityStatus } from '@/components/pwa/connectivity-status';

// No layout ou header
<ConnectivityStatus />
```

## Padrões de CRUD

### Create

```typescript
async function createExpense(data: ExpenseInput) {
  const expense = {
    ...data,
    localId: crypto.randomUUID(),
    syncStatus: 'pending' as const,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
  
  const id = await db.expenses.add(expense);
  return { ...expense, id };
}
```

### Read

```typescript
async function getExpenses() {
  return await db.expenses.toArray();
}

async function getExpenseById(localId: string) {
  return await db.expenses.where('localId').equals(localId).first();
}
```

### Update

```typescript
async function updateExpense(localId: string, data: Partial<ExpenseInput>) {
  await db.expenses.where('localId').equals(localId).modify({
    ...data,
    updatedAt: new Date().toISOString(),
    syncStatus: 'pending'
  });
}
```

### Delete

```typescript
async function deleteExpense(localId: string) {
  // Soft delete para sync
  await db.expenses.where('localId').equals(localId).modify({
    deleted: true,
    deletedAt: new Date().toISOString(),
    syncStatus: 'pending'
  });
}
```

## Checklist de Verificação

Antes de completar qualquer tarefa relacionada com dados:

- [ ] Dados são lidos de IndexedDB (Dexie), não de Supabase
- [ ] Escritas vão para IndexedDB primeiro
- [ ] App funciona 100% offline
- [ ] Status de sync é tracked por registo
- [ ] Estratégia de resolução de conflitos definida
- [ ] Cloud sync está atrás de verificação premium
- [ ] Zustand contém apenas UI state, não dados

## Benefícios de Privacidade

Esta arquitectura providencia:
- ✅ **Data sovereignty**: Utilizador é dono dos dados
- ✅ **Privacy by default**: Dados não saem do dispositivo a menos que optem
- ✅ **Offline access**: Funcionalidade completa sem internet
- ✅ **Performance**: Leituras locais instantâneas
- ✅ **Controlo**: Utilizador pode exportar/apagar todos os dados localmente

---

**Lembra-te**: **Os dados do utilizador pertencem a eles. Nós estamos apenas a ajudar a organizá-los.**
