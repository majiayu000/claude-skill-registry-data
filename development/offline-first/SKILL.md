---
name: offline-first
description: Local storage, data sync, and conflict resolution for offline-capable apps.
---

# Offline-First

## Storage Options

| Option | Use Case |
|--------|----------|
| AsyncStorage | Simple key-value |
| MMKV | Fast key-value |
| SQLite | Complex queries |
| WatermelonDB | Large datasets, sync |

## MMKV (Recommended)

```typescript
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV();

// Store
storage.set('user', JSON.stringify(user));
storage.set('token', 'abc123');

// Retrieve
const user = JSON.parse(storage.getString('user') || '{}');
const token = storage.getString('token');

// Delete
storage.delete('token');
```

## Sync Strategy

### Optimistic Updates

```typescript
async function updateItem(id: string, data: Partial<Item>) {
  // 1. Update local immediately
  await localDb.update(id, { ...data, _synced: false });

  // 2. Update UI
  queryClient.setQueryData(['item', id], (old) => ({
    ...old,
    ...data,
  }));

  // 3. Sync to server
  try {
    await api.updateItem(id, data);
    await localDb.update(id, { _synced: true });
  } catch (error) {
    // Queue for retry
    await syncQueue.add({ type: 'update', id, data });
  }
}
```

### Background Sync

```typescript
import NetInfo from '@react-native-community/netinfo';

NetInfo.addEventListener((state) => {
  if (state.isConnected) {
    syncQueue.processAll();
  }
});
```

## Conflict Resolution

```typescript
// Last-write-wins
if (serverItem.updatedAt > localItem.updatedAt) {
  await localDb.update(id, serverItem);
} else {
  await api.updateItem(id, localItem);
}

// Or: Manual resolution
if (hasConflict) {
  showConflictResolver(serverItem, localItem);
}
```

## Network Status

```typescript
function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    return NetInfo.addEventListener((state) => {
      setIsOnline(state.isConnected ?? false);
    });
  }, []);

  return isOnline;
}
```
