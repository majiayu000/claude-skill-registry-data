---
name: nextjs-firestore
description: Next.js + Firebase/Firestore統合開発パターン。型定義、データ操作、リアルタイム同期、認証に使用。Firestore、Firebase、データベース操作時に使用。
---

# Next.js + Firestore 開発スキル

Next.jsアプリケーションでFirestoreを効率的に使用するためのパターンとベストプラクティスをまとめています。

---

## このスキルを使用するタイミング

- Firestoreのデータ取得・更新を実装するとき
- 型定義（TypeScript）を作成するとき
- リアルタイムリスナーを設定するとき
- Firebase Authenticationを実装するとき
- Firestoreのセキュリティルールを設定するとき

---

## 1. 型定義パターン

### 1.1 基本的なドキュメント型

```typescript
// types/firestore.ts

// Firestoreのタイムスタンプ型
import { Timestamp } from 'firebase/firestore';

// ベース型（共通フィールド）
interface BaseDocument {
  id: string;
  createdAt: Timestamp;
  updatedAt: Timestamp;
}

// ユーザー型の例
export interface User extends BaseDocument {
  email: string;
  displayName: string;
  photoURL?: string;
  preferences: UserPreferences;
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  notifications: boolean;
}
```

### 1.2 コレクション参照型

```typescript
// Firestoreパスの型安全な定義
export const COLLECTIONS = {
  USERS: 'users',
  ROASTS: 'roasts',
  SETTINGS: 'settings',
} as const;

export type CollectionName = typeof COLLECTIONS[keyof typeof COLLECTIONS];
```

### 1.3 Converter パターン

```typescript
import { 
  DocumentData, 
  QueryDocumentSnapshot,
  FirestoreDataConverter 
} from 'firebase/firestore';

export const userConverter: FirestoreDataConverter<User> = {
  toFirestore(user: User): DocumentData {
    return {
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL ?? null,
      preferences: user.preferences,
      createdAt: user.createdAt,
      updatedAt: user.updatedAt,
    };
  },
  fromFirestore(snapshot: QueryDocumentSnapshot): User {
    const data = snapshot.data();
    return {
      id: snapshot.id,
      email: data.email,
      displayName: data.displayName,
      photoURL: data.photoURL ?? undefined,
      preferences: data.preferences,
      createdAt: data.createdAt,
      updatedAt: data.updatedAt,
    };
  },
};
```

---

## 2. データ操作パターン

### 2.1 ドキュメント取得

```typescript
import { doc, getDoc } from 'firebase/firestore';
import { db } from '@/lib/firebase';

// 単一ドキュメント取得
export async function getUser(userId: string): Promise<User | null> {
  const docRef = doc(db, COLLECTIONS.USERS, userId).withConverter(userConverter);
  const docSnap = await getDoc(docRef);
  
  if (!docSnap.exists()) {
    return null;
  }
  
  return docSnap.data();
}
```

### 2.2 コレクション取得

```typescript
import { collection, getDocs, query, where, orderBy, limit } from 'firebase/firestore';

// 条件付きクエリ
export async function getRoastsByUser(userId: string): Promise<Roast[]> {
  const roastsRef = collection(db, COLLECTIONS.ROASTS).withConverter(roastConverter);
  
  const q = query(
    roastsRef,
    where('userId', '==', userId),
    orderBy('createdAt', 'desc'),
    limit(50)
  );
  
  const querySnapshot = await getDocs(q);
  return querySnapshot.docs.map(doc => doc.data());
}
```

### 2.3 ドキュメント作成・更新

```typescript
import { doc, setDoc, updateDoc, serverTimestamp } from 'firebase/firestore';

// 新規作成
export async function createUser(userId: string, data: Omit<User, 'id' | 'createdAt' | 'updatedAt'>): Promise<void> {
  const docRef = doc(db, COLLECTIONS.USERS, userId);
  
  await setDoc(docRef, {
    ...data,
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp(),
  });
}

// 部分更新
export async function updateUser(userId: string, data: Partial<User>): Promise<void> {
  const docRef = doc(db, COLLECTIONS.USERS, userId);
  
  await updateDoc(docRef, {
    ...data,
    updatedAt: serverTimestamp(),
  });
}
```

### 2.4 トランザクション

```typescript
import { runTransaction } from 'firebase/firestore';

export async function incrementCounter(docId: string): Promise<void> {
  await runTransaction(db, async (transaction) => {
    const docRef = doc(db, 'counters', docId);
    const docSnap = await transaction.get(docRef);
    
    if (!docSnap.exists()) {
      throw new Error('Document does not exist!');
    }
    
    const currentCount = docSnap.data().count;
    transaction.update(docRef, { count: currentCount + 1 });
  });
}
```

---

## 3. リアルタイムリスナー

### 3.1 単一ドキュメントの監視

```typescript
import { doc, onSnapshot } from 'firebase/firestore';
import { useEffect, useState } from 'react';

export function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const docRef = doc(db, COLLECTIONS.USERS, userId).withConverter(userConverter);
    
    const unsubscribe = onSnapshot(
      docRef,
      (snapshot) => {
        if (snapshot.exists()) {
          setUser(snapshot.data());
        } else {
          setUser(null);
        }
        setLoading(false);
      },
      (err) => {
        setError(err);
        setLoading(false);
      }
    );

    return () => unsubscribe();
  }, [userId]);

  return { user, loading, error };
}
```

### 3.2 コレクションの監視

```typescript
import { collection, query, where, onSnapshot } from 'firebase/firestore';

export function useRoasts(userId: string) {
  const [roasts, setRoasts] = useState<Roast[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const roastsRef = collection(db, COLLECTIONS.ROASTS).withConverter(roastConverter);
    const q = query(roastsRef, where('userId', '==', userId));

    const unsubscribe = onSnapshot(q, (snapshot) => {
      const data = snapshot.docs.map(doc => doc.data());
      setRoasts(data);
      setLoading(false);
    });

    return () => unsubscribe();
  }, [userId]);

  return { roasts, loading };
}
```

---

## 4. Firebase Authentication

### 4.1 認証状態の監視

```typescript
// contexts/AuthContext.tsx
import { createContext, useContext, useEffect, useState } from 'react';
import { onAuthStateChanged, User as FirebaseUser } from 'firebase/auth';
import { auth } from '@/lib/firebase';

interface AuthContextType {
  user: FirebaseUser | null;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType>({ user: null, loading: true });

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<FirebaseUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

### 4.2 サインイン・サインアウト

```typescript
import { 
  signInWithPopup, 
  signInWithEmailAndPassword,
  signOut as firebaseSignOut,
  GoogleAuthProvider 
} from 'firebase/auth';

// Googleサインイン
export async function signInWithGoogle() {
  const provider = new GoogleAuthProvider();
  const result = await signInWithPopup(auth, provider);
  return result.user;
}

// メール/パスワードサインイン
export async function signInWithEmail(email: string, password: string) {
  const result = await signInWithEmailAndPassword(auth, email, password);
  return result.user;
}

// サインアウト
export async function signOut() {
  await firebaseSignOut(auth);
}
```

---

## 5. セキュリティルール

### 5.1 基本ルール

```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // ユーザードキュメント
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // ローストデータ
    match /roasts/{roastId} {
      allow read: if request.auth != null && resource.data.userId == request.auth.uid;
      allow create: if request.auth != null && request.resource.data.userId == request.auth.uid;
      allow update, delete: if request.auth != null && resource.data.userId == request.auth.uid;
    }
  }
}
```

---

## 6. エラーハンドリング

### 6.1 共通エラーハンドラー

```typescript
import { FirebaseError } from 'firebase/app';

export function handleFirestoreError(error: unknown): string {
  if (error instanceof FirebaseError) {
    switch (error.code) {
      case 'permission-denied':
        return 'アクセス権限がありません';
      case 'not-found':
        return 'データが見つかりません';
      case 'already-exists':
        return 'データが既に存在します';
      case 'unavailable':
        return 'サービスが一時的に利用できません';
      default:
        return `エラーが発生しました: ${error.message}`;
    }
  }
  return '予期しないエラーが発生しました';
}
```

---

## AI アシスタント指示

このスキルが有効な場合：

1. **型定義を優先**: データ構造を明確にしてから実装
2. **Converterを使用**: 型安全なデータ変換を実現
3. **エラーハンドリング**: 全ての非同期操作にtry-catchを実装
4. **リスナーのクリーンアップ**: useEffectのreturnでunsubscribeを呼ぶ

**必ず守ること**:
- `serverTimestamp()` を使用して一貫性を保つ
- セキュリティルールを考慮した実装
- ローディング状態とエラー状態を管理

**避けること**:
- クライアントサイドでのセキュリティ依存
- 無限ループのリスナー設定
- 型なしの `any` 使用
