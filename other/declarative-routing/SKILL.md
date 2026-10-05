---
name: declarative-routing
description: Implements declarative, URL-based navigation in Flutter applications using the go_router package. Activates when configuring routes, deep links, web URL mapping, nested navigation shells, or route guards.
version: 1.0.0
---

# Declarative Routing with GoRouter

Guide for configuring declarative routing, deep linking, and nested navigation in Flutter apps using `go_router`.

## Setup & Initialization

Add dependency:
```yaml
dependencies:
  go_router: ^14.0.0
```

Configure in `MaterialApp.router`:
```dart
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: appRouter,
      title: 'My App',
    );
  }
}
```

## Router Configuration

```dart
final appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'details/:id',
          builder: (context, state) {
            final id = state.pathParameters['id']!;
            return DetailsScreen(id: id);
          },
        ),
      ],
    ),
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
  ],
  redirect: (context, state) {
    final isAuthenticated = authService.isLoggedIn;
    final isGoingToLogin = state.matchedLocation == '/login';

    if (!isAuthenticated && !isGoingToLogin) {
      return '/login?redirect=${state.matchedLocation}';
    }
    if (isAuthenticated && isGoingToLogin) {
      return '/';
    }
    return null;
  },
);
```

## ShellRoute for Nested Navigation (Bottom Nav / Drawer)

```dart
ShellRoute(
  builder: (context, state, child) {
    return ScaffoldWithNavBar(child: child);
  },
  routes: [
    GoRoute(
      path: '/feed',
      builder: (context, state) => const FeedScreen(),
    ),
    GoRoute(
      path: '/profile',
      builder: (context, state) => const ProfileScreen(),
    ),
  ],
)
```

## Navigation Best Practices

- Use `context.go('/path')` to replace current route location.
- Use `context.push('/path')` when pushing onto the stack (e.g., detail modals).
- Always extract path parameters via `state.pathParameters` and query params via `state.uri.queryParameters`.
