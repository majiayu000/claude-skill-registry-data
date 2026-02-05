---
alwaysApply: false
---
# Blink Codebase Skill

## Purpose
This skill helps Claude understand and work with the Blink project - a Flutter app with REST API backend for managing Cursor IDE chat sessions.

## When to Use
Load this skill when:
- Working with Flutter/Dart code in the `lib/` directory
- Modifying the REST API in `rest/cursor_chat_api.py`
- Understanding the architecture and data flow
- Debugging integration between frontend and backend
- Adding new features that span both layers

## Architecture Overview

### Tech Stack
- **Frontend**: Flutter (Dart) with Material Design 3
- **Backend**: Python FastAPI REST API
- **Database**: SQLite (Cursor's state.vscdb)
- **State Management**: Provider (configured, ready for use)

### Project Structure
```
blink/
├── lib/                    # Flutter source code
│   ├── main.dart          # App entry + theme
│   ├── models/            # Data models with fromJson/toJson
│   ├── services/          # Business logic layer
│   ├── screens/           # UI screens
│   ├── widgets/           # Reusable components
│   └── utils/             # Theme and utilities
├── rest/                  # REST API service
│   ├── cursor_chat_api.py # FastAPI server
│   ├── requirements_api.txt
│   └── start_api.sh       # Startup script
└── test/                  # Flutter tests
```

## Key Components

### 1. Data Flow
```
Flutter UI → ApiService → REST API → SQLite Database
```

**API Endpoint**: `http://127.0.0.1:8000`

### 2. Core Models
Located in `lib/models/`:

- **Chat**: Full conversation metadata
  - Fields: id, title, status, messages, isArchived, totalLinesAdded/Removed, contextUsagePercent
  - Has `fromJson()` for API responses
  
- **Message**: Individual chat messages
  - Fields: bubbleId, content, role, timestamp, hasCode, hasTodos, hasToolCall, hasThinking
  - Supports content type flags
  
- **CodeBlock**, **TodoItem**, **ToolCall**: Rich content types

### 3. Services Layer

**ApiService** (`lib/services/api_service.dart`):
- REST API communication
- Endpoints: `/health`, `/chats`, `/chats/{id}`, `/chats/{id}/metadata`
- Error handling with `ApiException`

**ChatService** (`lib/services/chat_service.dart`):
- Business logic orchestration
- Caching (5-minute expiry)
- Search and filtering capabilities
- Uses `ApiService` internally

### 4. UI Patterns

**Theme**: `lib/utils/theme.dart`
- Custom color palette (AppTheme.primary, .codeColor, etc.)
- Gradients, shadows, spacing constants
- Status color helpers

**Screens**:
- `ChatListScreen`: Search bar, filters, pull-to-refresh, shimmer loading
- `ChatDetailScreen`: Message list, stats header, rich content display

**Widgets**:
- `MessageBubble`: Gradient bubbles with content badges
- `CodeBlockViewer`: Syntax highlighting with expand/collapse
- `TodoItemWidget`, `ToolCallCard`, `ThinkingBlock`: Rich content
- `FilterSheet`: Bottom sheet with filter options
- `ChatSearchBar`: Debounced search (300ms)

## Common Patterns

### Adding a New Feature

**Frontend (Flutter)**:
1. Add model fields if needed (`lib/models/`)
2. Update API service method (`lib/services/api_service.dart`)
3. Add business logic (`lib/services/chat_service.dart`)
4. Create/update widgets (`lib/widgets/`)
5. Integrate in screens (`lib/screens/`)

**Backend (API)**:
1. Add endpoint to `rest/cursor_chat_api.py`
2. Query SQLite database (tables: `cursorDiskKV`, `ItemTable`)
3. Return JSON matching model structure

### API Response Structure
```dart
// Chat list response
{
  "total": 68,
  "returned": 10,
  "offset": 0,
  "chats": [
    {
      "chat_id": "uuid",
      "name": "Chat title",
      "created_at_iso": "2025-11-11T...",
      "message_count": 42,
      "is_archived": false,
      // ... more fields
    }
  ]
}

// Chat messages response
{
  "chat_id": "uuid",
  "message_count": 42,
  "metadata": { /* chat info */ },
  "messages": [
    {
      "bubble_id": "uuid",
      "type": 1,  // 1=user, 2=assistant
      "type_label": "user",
      "text": "Message content",
      "has_code": false,
      "has_todos": true,
      // ... more flags
    }
  ]
}
```

### Styling Guidelines
- Use `AppTheme` constants (never hardcode colors/spacing)
- Apply `AppTheme.radiusMedium` for rounded corners
- Use `AppTheme.cardShadow` for elevation
- Follow Material Design 3 principles
- Gradients for visual hierarchy

### State Management
- Provider is configured in `main.dart`
- Currently not actively used (direct service calls)
- Ready for expansion if needed

## Development Workflow

### Running the App
```bash
# Terminal 1: Start REST API
cd /path/to/blink/rest
python3 cursor_chat_api.py

# Terminal 2: Run Flutter app
cd /path/to/blink
flutter run -d macos  # or chrome, android, ios
```

### Common Tasks

**Add new API endpoint**:
1. Add method to `ApiService`
2. Add business logic to `ChatService`
3. Update UI to call the method

**Add new widget**:
1. Create file in `lib/widgets/`
2. Import `AppTheme` for styling
3. Export from parent screen/widget

**Debug API issues**:
1. Check REST API logs (console output)
2. Check Flutter console for errors
3. Verify API endpoint in `ApiService.baseUrl`
4. Test endpoint directly: `curl http://localhost:8000/health`

## Testing

### API Testing
```bash
cd rest
python3 test_api.py
```

### Flutter Testing
```bash
flutter test
flutter analyze  # Linting
```

## Dependencies

### Flutter (pubspec.yaml)
- `http`: API calls
- `provider`: State management
- `flutter_markdown`: Markdown rendering
- `shimmer`: Loading animations
- `flutter_syntax_view`: Code syntax highlighting
- `intl`: Date formatting

### Python (requirements_api.txt)
- `fastapi`: REST framework
- `uvicorn`: ASGI server
- `pydantic`: Data validation

## Troubleshooting

### Common Issues

**"Unable to connect to API"**:
- Ensure REST API is running on port 8000
- Check `ApiService.baseUrl` (use 127.0.0.1 for iOS simulator)
- For Android emulator: use `http://10.0.2.2:8000`

**"No chats found"**:
- Verify Cursor database path in `cursor_chat_api.py`
- Check database exists: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`

**Build errors**:
```bash
flutter clean
flutter pub get
```

## API Reference

### REST Endpoints

**GET /health**
- Returns: `{"status": "healthy", "total_chats": N, "total_messages": N}`

**GET /chats**
- Query params: `include_archived`, `sort_by`, `limit`, `offset`
- Returns: Paginated chat list

**GET /chats/{chat_id}**
- Query params: `include_metadata`, `limit`
- Returns: Chat with full message history

**GET /chats/{chat_id}/metadata**
- Returns: Chat metadata only (no messages)

## Progressive Disclosure

### Basic Understanding (Start Here)
- This is a Flutter app that displays Cursor IDE chat history
- It connects to a local REST API that reads from Cursor's SQLite database
- Material Design 3 with custom theme
- Search, filtering, and rich content display

### Intermediate Details
- Two-layer architecture: Flutter UI + Python REST API
- Caching strategy with 5-minute expiry
- Content types: code blocks, todos, tool calls, thinking blocks
- Real-time search with 300ms debounce

### Advanced Patterns
- Direct SQLite queries in Python backend
- JSON deserialization through model factories
- Gradient-based UI hierarchy
- Composable widget system
- Extensible for WebSocket real-time updates

## Related Resources
- Flutter docs: https://flutter.dev
- FastAPI docs: https://fastapi.tiangolo.com
- Material Design 3: https://m3.material.io
- Cursor database structure: See `rest/cursor_chat_api.py` comments
