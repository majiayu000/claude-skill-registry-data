---
name: frontend-integration
description: "Frontend integration guides for React and Flutter with Kailash SDK workflows, including setup, API integration, state management, and best practices. Use when asking about 'frontend integration', 'React integration', 'Flutter integration', 'frontend developer', 'UI integration', 'React with Kailash', 'Flutter with Kailash', 'frontend workflow', 'API client', 'React query', or 'Flutter state management'."
---

# Kailash Frontend Integration

Guides for integrating Kailash workflows with frontend frameworks including React and Flutter.

## Overview

Frontend integration patterns for:
- React applications with Kailash workflows
- Flutter mobile/desktop apps with Kailash
- API client setup and configuration
- State management patterns
- Real-time updates and streaming

## Reference Documentation

### React Integration
- **[react-integration-quick](react-integration-quick.md)** - React integration quick start
  - Setup with Nexus API
  - React Query integration
  - TypeScript types
  - Error handling
  - State management
  - Real-time updates

### Flutter Integration
- **[flutter-integration-quick](flutter-integration-quick.md)** - Flutter integration quick start
  - HTTP client setup
  - Dart models
  - State management (Riverpod/Bloc)
  - Error handling
  - Platform-specific code

### General Frontend
- **[frontend-developer](frontend-developer.md)** - Frontend development guide
  - Architecture patterns
  - API integration
  - Authentication
  - Error handling
  - Best practices

## Integration Patterns

### React + Nexus
```typescript
import { useQuery } from '@tanstack/react-query';

// Call Kailash workflow via Nexus API
const { data, isLoading, error } = useQuery({
  queryKey: ['workflow', workflowId],
  queryFn: () => fetch(`/api/workflow/${workflowId}`, {
    method: 'POST',
    body: JSON.stringify({ input: 'data' })
  }).then(res => res.json())
});
```

### Flutter + Nexus
```dart
import 'package:http/http.dart' as http;

// Call Kailash workflow
Future<Map<String, dynamic>> executeWorkflow(String workflowId, Map<String, dynamic> input) async {
  final response = await http.post(
    Uri.parse('$baseUrl/api/workflow/$workflowId'),
    body: jsonEncode(input),
  );
  return jsonDecode(response.body);
}
```

## Architecture Patterns

### Recommended Stack

**React Applications:**
- **API Layer**: Nexus (multi-channel platform)
- **State Management**: React Query / Zustand
- **HTTP Client**: Fetch API / Axios
- **Type Safety**: TypeScript with generated types
- **UI Framework**: Shadcn, Material-UI, or custom

**Flutter Applications:**
- **API Layer**: Nexus (multi-channel platform)
- **State Management**: Riverpod / Bloc
- **HTTP Client**: http package / Dio
- **Type Safety**: Dart with generated models
- **UI Framework**: Material 3 / Cupertino

### Backend Architecture

```
Frontend (React/Flutter)
    ↓
Nexus API (Port 8000)
    ↓
Kailash Workflows
    ↓
DataFlow (Database)
    ↓
PostgreSQL/SQLite
```

## When to Use This Skill

Use this skill when you need to:
- Integrate React with Kailash workflows
- Build Flutter apps with Kailash backend
- Set up API clients for Kailash
- Implement frontend state management
- Handle errors in frontend applications
- Configure real-time updates
- Generate TypeScript/Dart types

## Best Practices

### API Integration
- ✅ Use Nexus for auto-generated APIs
- ✅ Implement proper error handling
- ✅ Use type-safe clients (TypeScript/Dart)
- ✅ Cache responses appropriately
- ✅ Handle loading and error states
- ❌ NEVER expose API keys in frontend code
- ❌ NEVER skip input validation

### State Management
- ✅ Use React Query for server state (React)
- ✅ Use Riverpod/Bloc for app state (Flutter)
- ✅ Implement optimistic updates
- ✅ Handle offline scenarios
- ❌ NEVER store sensitive data in client state

### Performance
- ✅ Implement pagination for large datasets
- ✅ Use debouncing for search/filter
- ✅ Cache API responses
- ✅ Lazy load components
- ❌ NEVER fetch all data at once

## Related Skills

- **[03-nexus](../../03-nexus/SKILL.md)** - Nexus API deployment
- **[02-dataflow](../../02-dataflow/SKILL.md)** - Database backend
- **[01-core-sdk](../../01-core-sdk/SKILL.md)** - Workflow creation

## Support

For frontend integration help, invoke:
- `react-specialist` - React integration patterns
- `flutter-specialist` - Flutter integration patterns
- `frontend-developer` - Frontend architecture
- `nexus-specialist` - API configuration
