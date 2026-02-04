---
name: firebase-integration
description: Firebase integration for authentication, Firestore database, and real-time data synchronization. Use when working with Firebase services in the LiveMetro app.
---

# Firebase Integration Guidelines

## When to Use This Skill
- Setting up Firebase authentication
- Querying Firestore collections
- Implementing real-time data subscriptions
- Managing user data in Firebase
- Handling Firebase errors

## Core Services

### 1. Firestore Database Structure
```
Collections:
- subwayLines/          # Line metadata (color, name)
- stations/             # Station info with coordinates
- trains/               # Real-time train positions
- trainDelays/          # Delay and disruption alerts
- congestionData/       # Train car congestion levels
- users/                # User preferences and favorites
```

### 2. Authentication Pattern
```typescript
import { auth } from '@/config/firebase';
import {
  signInAnonymously,
  onAuthStateChanged
} from 'firebase/auth';

// Anonymous authentication for basic features
const signIn = async () => {
  try {
    const result = await signInAnonymously(auth);
    return result.user;
  } catch (error) {
    console.error('Auth error:', error);
    throw error;
  }
};

// Listen to auth state changes
onAuthStateChanged(auth, (user) => {
  if (user) {
    // User is signed in
  } else {
    // User is signed out
  }
});
```

### 3. Firestore Query Pattern
```typescript
import { firestore } from '@/config/firebase';
import {
  collection,
  query,
  where,
  getDocs,
  orderBy,
  limit
} from 'firebase/firestore';

// Basic query
const getStations = async (lineId: string) => {
  try {
    const stationsRef = collection(firestore, 'stations');
    const q = query(
      stationsRef,
      where('lineId', '==', lineId),
      orderBy('sequence')
    );

    const snapshot = await getDocs(q);
    return snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  } catch (error) {
    console.error('Firestore query error:', error);
    return [];
  }
};
```

### 4. Real-time Subscription Pattern
```typescript
import { onSnapshot } from 'firebase/firestore';

// Subscribe to real-time updates
const subscribeToTrains = (
  stationId: string,
  callback: (trains: Train[]) => void
): (() => void) => {
  const trainsRef = collection(firestore, 'trains');
  const q = query(
    trainsRef,
    where('currentStationId', '==', stationId)
  );

  const unsubscribe = onSnapshot(
    q,
    (snapshot) => {
      const trains = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      } as Train));
      callback(trains);
    },
    (error) => {
      console.error('Snapshot error:', error);
    }
  );

  return unsubscribe; // Return cleanup function
};

// Usage in component
useEffect(() => {
  const unsubscribe = subscribeToTrains(stationId, setTrains);
  return () => unsubscribe(); // Cleanup on unmount
}, [stationId]);
```

### 5. Error Handling
```typescript
import { FirebaseError } from 'firebase/app';

const handleFirebaseError = (error: unknown): string => {
  if (error instanceof FirebaseError) {
    switch (error.code) {
      case 'permission-denied':
        return 'You do not have permission to access this data';
      case 'unavailable':
        return 'Firebase service is temporarily unavailable';
      case 'unauthenticated':
        return 'Please sign in to continue';
      default:
        return error.message;
    }
  }
  return 'An unexpected error occurred';
};
```

## Service Layer Pattern

### trainService.ts Example
```typescript
class TrainService {
  private static instance: TrainService;

  static getInstance(): TrainService {
    if (!TrainService.instance) {
      TrainService.instance = new TrainService();
    }
    return TrainService.instance;
  }

  async getTrainsByStation(stationId: string): Promise<Train[]> {
    // Implementation
  }

  subscribeToTrainUpdates(
    stationId: string,
    callback: (trains: Train[]) => void
  ): () => void {
    // Implementation with cleanup
  }
}

export const trainService = TrainService.getInstance();
```

## Data Caching Strategy

### Multi-tier fallback
```typescript
/**
 * Priority: Seoul API → Firebase → Local Cache
 */
const getTrainData = async (stationId: string): Promise<Train[]> => {
  try {
    // 1. Try Seoul API (primary source)
    const apiData = await seoulApi.getArrivals(stationId);
    if (apiData.length > 0) {
      await cacheData(stationId, apiData);
      return apiData;
    }
  } catch (error) {
    console.log('Seoul API failed, trying Firebase');
  }

  try {
    // 2. Fallback to Firebase
    const fbData = await trainService.getTrainsByStation(stationId);
    if (fbData.length > 0) {
      return fbData;
    }
  } catch (error) {
    console.log('Firebase failed, using cache');
  }

  // 3. Last resort: Local cache
  return await getCachedData(stationId);
};
```

## Security Rules Considerations

### Firestore Rules Pattern
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Public read for subway data
    match /stations/{stationId} {
      allow read: if true;
      allow write: if false; // Only through admin
    }

    // User-specific data
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
  }
}
```

## Best Practices

### 1. Subscription Cleanup
Always clean up Firebase subscriptions to prevent memory leaks:
```typescript
useEffect(() => {
  const unsubscribe = subscribeToData(callback);
  return () => unsubscribe();
}, [dependencies]);
```

### 2. Batch Operations
For multiple writes, use batch operations:
```typescript
import { writeBatch } from 'firebase/firestore';

const batch = writeBatch(firestore);
batch.set(docRef1, data1);
batch.update(docRef2, data2);
await batch.commit();
```

### 3. Offline Persistence
Handle offline scenarios gracefully:
```typescript
import { enableNetwork, disableNetwork } from 'firebase/firestore';

// Firestore automatically caches data for offline use
// Monitor connectivity and inform users
```

## Common Pitfalls to Avoid
- ❌ Not cleaning up subscriptions (memory leaks)
- ❌ Querying without indexes (slow performance)
- ❌ Exposing Firebase config in client code (security)
- ❌ Not handling permission errors
- ❌ Over-fetching data (use limit and pagination)

## Testing
- Mock Firebase services in tests
- Test offline scenarios
- Verify subscription cleanup
- Test error handling paths
