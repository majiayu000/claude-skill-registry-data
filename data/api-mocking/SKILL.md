# 🎭 API Mocking Skill

---
name: api-mocking
description: Create mock APIs for frontend development and testing without backend dependencies
---

## 🎯 Purpose

สร้าง mock APIs สำหรับ frontend development และ testing โดยไม่ต้องพึ่ง backend จริง

## 📋 When to Use

- Frontend before backend ready
- Integration testing
- Offline development
- Demo/presentations
- Rate limiting avoidance

## 🔧 Mocking Methods

### 1. MSW (Mock Service Worker)
```typescript
// mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: 1, name: 'John' },
      { id: 2, name: 'Jane' },
    ]);
  }),
  
  http.post('/api/users', async ({ request }) => {
    const data = await request.json();
    return HttpResponse.json({ id: 3, ...data }, { status: 201 });
  }),
];
```

```typescript
// mocks/browser.ts
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

export const worker = setupWorker(...handlers);
```

### 2. JSON Server
```bash
npm install -g json-server

# db.json
{
  "users": [
    { "id": 1, "name": "John" }
  ],
  "posts": [
    { "id": 1, "title": "Hello", "userId": 1 }
  ]
}

json-server --watch db.json --port 3001
```

### 3. Local Mock Functions
```typescript
const mockApi = {
  users: {
    getAll: () => Promise.resolve([
      { id: 1, name: 'John' }
    ]),
    getById: (id: string) => Promise.resolve({ id, name: 'John' }),
    create: (data: any) => Promise.resolve({ id: Date.now(), ...data }),
  }
};

// Use in dev
const api = process.env.NODE_ENV === 'development' ? mockApi : realApi;
```

## 📊 Mock Data Generation

### Faker.js
```typescript
import { faker } from '@faker-js/faker';

function generateUsers(count: number) {
  return Array.from({ length: count }, () => ({
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    avatar: faker.image.avatar(),
  }));
}
```

### Thai Mock Data
```typescript
const thaiMockData = {
  names: ['สมชาย', 'สมหญิง', 'วิชัย', 'วันดี'],
  addresses: ['กรุงเทพฯ', 'เชียงใหม่', 'ขอนแก่น'],
  
  getRandomName: () => thaiMockData.names[Math.floor(Math.random() * thaiMockData.names.length)],
};
```

## 📝 Mock Response Templates

### Success Response
```typescript
{
  data: { /* actual data */ },
  success: true,
  message: 'Operation successful'
}
```

### Error Response
```typescript
{
  error: {
    code: 'VALIDATION_ERROR',
    message: 'Invalid input',
    details: { field: 'email', issue: 'Invalid format' }
  },
  success: false
}
```

### Paginated Response
```typescript
{
  data: [ /* items */ ],
  pagination: {
    page: 1,
    limit: 10,
    total: 100,
    totalPages: 10
  }
}
```

## ✅ Mocking Checklist

- [ ] All endpoints covered
- [ ] Realistic data
- [ ] Error scenarios
- [ ] Edge cases
- [ ] Loading delays (for UX)
- [ ] Thai content (if Thai app)

## 🔗 Related Skills

- `api-design` - Design APIs
- `testing` - Test with mocks
- `api-client-generator` - API clients
