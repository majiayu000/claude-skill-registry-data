---
name: expo-react-query-setup
description: Install and wire @tanstack/react-query in Expo/React Native apps (providers, query client, fetch patterns, and screen usage). Use when adding React Query to a project or extending data fetching patterns.
license: MIT
metadata:
  author: amannhimself.dev
---

# Expo React Query Setup

## Overview

How to install, configure, and use @tanstack/react-query in Expo/React Native projects.

## Quick start

- Install deps: `bunx expo install @tanstack/react-query` if a `bun.lock` file is present.
- Create a shared `queryClient` and wrap the app with `QueryClientProvider`.
- Use array query keys and export `fetchX` + `xQuery` helpers for reuse.

## Provider setup (app entry)

```tsx
// src/app/_layout.tsx (Expo Router example)
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Stack } from "expo-router";

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(tabs)" />
      </Stack>
    </QueryClientProvider>
  );
}
```

## Service + query helper pattern

```ts
// src/services/movies.ts
import { TMDB_API_BASE_URL, TMDB_API_KEY } from "@/services/config";

export type Movie = {
  id: number;
  title: string;
  vote_average: number;
  poster_path: string | null;
};

const ensureApiKey = () => {
  if (!TMDB_API_KEY) {
    throw new Error(
      "TMDB API key missing. Set EXPO_PUBLIC_TMDB_API_KEY before fetching."
    );
  }
};

export const fetchPopularMovies = async (): Promise<Movie[]> => {
  ensureApiKey();
  const res = await fetch(
    `${TMDB_API_BASE_URL}/movie/popular?language=en-US&page=1&api_key=${TMDB_API_KEY}`
  );
  if (!res.ok) throw new Error(`Movies request failed: ${res.status}`);
  return (await res.json()).results;
};

export const popularMoviesQuery = () => ({
  queryKey: ["popularMovies"],
  queryFn: fetchPopularMovies,
});
```

## Screen usage

```tsx
import { useQuery } from "@tanstack/react-query";
import { Image } from "expo-image";
import {
  ActivityIndicator,
  RefreshControl,
  ScrollView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

import { makeImageUrl } from "@/services/config";
import { popularMoviesQuery } from "@/services/movies";

export default function MoviesScreen() {
  const { data, isLoading, isError, refetch, isRefetching, error } = useQuery(
    popularMoviesQuery()
  );

  if (isLoading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#2563eb" />
        <Text>Loading popular movies…</Text>
      </View>
    );
  }

  if (isError) {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorTitle}>Could not load movies</Text>
        <Text style={styles.errorText}>
          {error instanceof Error ? error.message : "Try again."}
        </Text>
        <TouchableOpacity onPress={() => refetch()} style={styles.retry}>
          <Text style={styles.retryLabel}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView
      contentContainerStyle={styles.listContent}
      refreshControl={
        <RefreshControl refreshing={isRefetching} onRefresh={refetch} />
      }
    >
      {data?.map((movie) => {
        const posterUri = makeImageUrl(movie.poster_path);
        return (
          <View key={movie.id} style={styles.card}>
            {posterUri ? (
              <Image source={{ uri: posterUri }} style={styles.poster} />
            ) : (
              <View style={styles.posterPlaceholder}>
                <Text>No poster</Text>
              </View>
            )}
            <View style={styles.cardBody}>
              <Text style={styles.title}>{movie.title}</Text>
              <Text style={styles.meta}>★ {movie.vote_average.toFixed(1)}</Text>
            </View>
          </View>
        );
      })}
    </ScrollView>
  );
}
```

## Tips

- Keep query keys stable and array-based; include params (e.g., `["movie", id]`).
- For mutations, invalidate or refetch related queries after success.
- If you have an offline modal/provider, read connectivity before firing heavy requests.
- Use `staleTime`/`cacheTime` to tune refetching; default is fine for many screens.
- Clear cache with `queryClient.clear()` only in exceptional cases (e.g., logout).
- Guard fetchers that need public keys (e.g., TMDB) and surface friendly error/loading states with pull-to-refresh.

## Offline modal + provider (optional)

- Install: `bunx expo install expo-network` (and keep @tanstack/react-query installed).
- Connectivity provider (create `providers/ConnectivityProvider.tsx`):

```ts
import { onlineManager } from "@tanstack/react-query";
import * as Network from "expo-network";
import {
  createContext,
  PropsWithChildren,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { AppState, AppStateStatus } from "react-native";

type ConnectivityContextValue = {
  isOnline: boolean;
  refresh: () => Promise<boolean>;
};

const ConnectivityContext = createContext<ConnectivityContextValue | undefined>(
  undefined
);

const deriveOnlineStatus = (
  state: Network.NetworkState | null | undefined
): boolean => {
  if (!state) return true;
  if (state.isInternetReachable === false) return false;
  return Boolean(state.isConnected);
};

export const ConnectivityProvider = ({ children }: PropsWithChildren) => {
  const [isOnline, setIsOnline] = useState(true);

  const applyState = useCallback((state: Network.NetworkState | null) => {
    const online = deriveOnlineStatus(state);
    setIsOnline(online);
    onlineManager.setOnline(online);
  }, []);

  const refresh = useCallback(async () => {
    try {
      const state = await Network.getNetworkStateAsync();
      applyState(state);
      return deriveOnlineStatus(state);
    } catch {
      return isOnline;
    }
  }, [applyState, isOnline]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  useEffect(() => {
    const subscription = Network.addNetworkStateListener(applyState);
    const handleAppStateChange = (status: AppStateStatus) => {
      if (status === "active") refresh();
    };
    const appStateSubscription = AppState.addEventListener(
      "change",
      handleAppStateChange
    );
    return () => {
      subscription.remove();
      appStateSubscription.remove();
    };
  }, [applyState, refresh]);

  return (
    <ConnectivityContext.Provider value={{ isOnline, refresh }}>
      {children}
    </ConnectivityContext.Provider>
  );
};

export const useConnectivity = () => {
  const ctx = useContext(ConnectivityContext);
  if (!ctx)
    throw new Error("useConnectivity must be used within ConnectivityProvider");
  return ctx;
};
```

- Offline UI (create `components/OfflineModal.tsx` and export from your components index):
  - If you have a custom Text component/alias (e.g., `@/components/Text`), update the import accordingly; otherwise use `import { Text } from "react-native"`.

```tsx
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { SymbolView } from "expo-symbols";
import {
  ActivityIndicator,
  Modal,
  Platform,
  Pressable,
  StyleSheet,
  View,
} from "react-native";
import { Text } from "./Text"; // change to your project’s Text component or react-native Text

type OfflineNoticeProps = {
  onRetry?: () => Promise<void> | void;
  isChecking?: boolean;
};
type OfflineModalProps = OfflineNoticeProps & { visible: boolean };

export const OfflineNotice = ({ onRetry, isChecking }: OfflineNoticeProps) => (
  <View style={styles.card}>
    <View style={styles.iconBadge}>
      {Platform.OS === "ios" ? (
        <SymbolView
          name="wifi.slash"
          tintColor="#ef4444"
          style={{ width: 26, height: 26 }}
        />
      ) : (
        <MaterialIcons name="wifi-off" size={26} color="#ef4444" />
      )}
    </View>
    <Text style={styles.title}>You are offline</Text>
    <Text style={styles.subtitle}>
      Connect to Wi-Fi or cellular data to continue browsing.
    </Text>
    {onRetry ? (
      <Pressable
        style={({ pressed }) => [
          styles.button,
          pressed && styles.buttonPressed,
          isChecking && styles.buttonDisabled,
        ]}
        onPress={onRetry}
        disabled={isChecking}
        accessibilityRole="button"
        accessibilityLabel="Retry connection"
      >
        {isChecking ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonLabel}>Retry</Text>
        )}
      </Pressable>
    ) : null}
  </View>
);

export function OfflineModal({
  visible,
  onRetry,
  isChecking,
}: OfflineModalProps) {
  return (
    <Modal
      animationType="fade"
      transparent
      visible={visible}
      statusBarTranslucent
    >
      <View style={styles.backdrop}>
        <OfflineNotice onRetry={onRetry} isChecking={isChecking} />
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.5)",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
  card: {
    width: "100%",
    paddingVertical: 22,
    paddingHorizontal: 20,
    borderRadius: 12,
    backgroundColor: "#fff",
    alignItems: "center",
    gap: 12,
    borderWidth: 1,
    borderColor: "#E5E7EB",
  },
  iconBadge: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: "#fee2e2",
    alignItems: "center",
    justifyContent: "center",
  },
  title: { fontSize: 18, textAlign: "center" },
  subtitle: {
    fontSize: 14,
    textAlign: "center",
    lineHeight: 20,
    color: "#6b7280",
  },
  button: {
    marginTop: 4,
    backgroundColor: "#007AFF",
    paddingHorizontal: 18,
    paddingVertical: 11,
    borderRadius: 12,
    minWidth: 120,
    alignItems: "center",
  },
  buttonPressed: { opacity: 0.85 },
  buttonDisabled: { opacity: 0.65 },
  buttonLabel: { color: "#fff", fontWeight: "600" },
});
```

- Modal route (create `app/(modals)/offline.tsx`):

```tsx
import { useRouter } from "expo-router";
import { useState } from "react";
import { StyleSheet, View } from "react-native";
import { OfflineNotice } from "@/components/OfflineModal"; // adjust alias/import if not using @/
import { useConnectivity } from "@/providers/ConnectivityProvider"; // adjust alias/import if not using @/

export default function OfflineScreen() {
  const { refresh, isOnline } = useConnectivity();
  const router = useRouter();
  const [checking, setChecking] = useState(false);

  const handleRetry = async () => {
    setChecking(true);
    try {
      const online = await refresh();
      if (online || isOnline) {
        if (router.canGoBack()) router.back();
        else router.replace("/(tabs)");
      }
    } finally {
      setChecking(false);
    }
  };

  return (
    <View style={styles.container}>
      <OfflineNotice onRetry={handleRetry} isChecking={checking} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.4)",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
});
```

- Layout guard (in `app/_layout.tsx`): after wrapping with `QueryClientProvider` and `ConnectivityProvider`, watch `isOnline` and `router.replace("/(modals)/offline")` when offline, so queries pause and users see the modal.
