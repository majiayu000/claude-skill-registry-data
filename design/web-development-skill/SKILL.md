---
name: web-development-skill
description: Master modern web development. Learn HTML/CSS/JavaScript fundamentals, React/Vue/Angular frameworks, Node.js backend, databases, APIs, and full-stack architectures. Use when building web applications, learning web technologies, or choosing tech stacks.
---

# Web Development Skill

Complete guide to building modern web applications from frontend to full-stack systems.

## Quick Start

### Choose Your Path

```
Frontend Only → Full Stack → Backend Focus
     ↓             ↓            ↓
  React        Next.js/      Node.js +
  Vue/        Nuxt/         Database
  Angular     Blitz
```

### Get Started in 5 Steps

1. **HTML & CSS Fundamentals** (2-3 weeks)
   - Semantic HTML
   - CSS layouts (Flexbox, Grid)
   - Responsive design

2. **JavaScript Core** (4-6 weeks)
   - ES6+ syntax
   - DOM manipulation
   - Async/await, Promises
   - Event handling

3. **Frontend Framework** (4-8 weeks)
   - React (most popular)
   - Or: Vue (easier), Angular (enterprise)
   - Components, state, hooks

4. **Backend Basics** (4-6 weeks)
   - Node.js + Express/Fastify
   - Database fundamentals
   - REST API design

5. **Deploy & Polish** (ongoing)
   - Deployment platforms (Vercel, Netlify, Heroku)
   - Performance optimization
   - Monitoring and logging

---

## Frontend Development

### **HTML & CSS Mastery**

**HTML5 Best Practices:**
```html
<!-- Semantic markup -->
<header>
  <nav>Navigation</nav>
</header>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>

<footer>
  <p>&copy; 2024</p>
</footer>

<!-- Accessibility -->
<img src="image.jpg" alt="Descriptive text">
<button aria-label="Close menu">×</button>
```

**CSS Modern Layout:**
```css
/* Flexbox - 1D layouts */
.flex-container {
  display: flex;
  justify-content: space-between;  /* horizontal */
  align-items: center;            /* vertical */
  gap: 1rem;
}

/* Grid - 2D layouts */
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: 1fr;
  }
}
```

**CSS Framework Comparison:**

| Framework | Approach | Learning Curve | Customization |
|-----------|----------|---|---|
| **Tailwind** | Utility-first | Medium | High |
| **Bootstrap** | Component-based | Low | Medium |
| **Material UI** | Design system | High | Low |
| **Bulma** | Modern, minimal | Low | High |

### **JavaScript Fundamentals**

**ES6+ Essential Features:**
```javascript
// 1. Arrow Functions
const add = (a, b) => a + b;

// 2. Destructuring
const { name, age } = user;
const [first, second] = array;

// 3. Spread Operator
const newArr = [...oldArr, newItem];
const merged = { ...obj1, ...obj2 };

// 4. Template Literals
const message = `Hello, ${name}!`;

// 5. const vs let (always use these, not var)
const CONSTANT = 5;      // Never changes
let variable = 10;       // Can change

// 6. Async/Await (modern promises)
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}

// 7. Higher-order Functions
const numbers = [1, 2, 3, 4];
const doubled = numbers
  .filter(n => n > 2)        // Filter: [3, 4]
  .map(n => n * 2)           // Map: [6, 8]
  .reduce((acc, n) => acc + n, 0);  // Reduce: 14
```

### **Frontend Frameworks**

#### React (Most Popular)
```jsx
// Function Components + Hooks (modern way)
import { useState, useEffect } from 'react';

function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Data fetching
  useEffect(() => {
    fetchUser().then(data => {
      setUser(data);
      setLoading(false);
    });
  }, []); // Empty dependency = run once

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}

export default UserProfile;
```

**Key Concepts:**
- Components: Reusable UI units
- JSX: HTML-in-JavaScript
- State: Component data (useState)
- Props: Component parameters
- Hooks: useState, useEffect, useContext
- Context API: Global state management
- Performance: React.memo, useMemo

#### Vue.js (Easier than React)
```vue
<template>
  <div class="user-profile">
    <h1>{{ user.name }}</h1>
    <p v-if="loading">Loading...</p>
    <button @click="increment">Count: {{ count }}</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const count = ref(0);
const user = ref(null);
const loading = ref(true);

onMounted(async () => {
  const data = await fetchUser();
  user.value = data;
  loading.value = false;
});

const increment = () => count.value++;
</script>

<style scoped>
.user-profile {
  padding: 1rem;
}
</style>
```

#### Angular (Enterprise)
- Full framework with dependency injection
- TypeScript-first
- RxJS for reactive programming
- Best for large enterprise applications

### **State Management**

**When to use:**
- Redux: Large apps with complex state
- Zustand: Simple, modern alternative
- Jotai: Atomic state management
- MobX: Simplified reactive state

**Redux Example:**
```javascript
// 1. Actions
const INCREMENT = 'INCREMENT';
const increment = () => ({ type: INCREMENT });

// 2. Reducer
const countReducer = (state = 0, action) => {
  if (action.type === INCREMENT) return state + 1;
  return state;
};

// 3. Store
const store = createStore(countReducer);

// 4. Use in React
const count = useSelector(state => state);
const dispatch = useDispatch();

// <button onClick={() => dispatch(increment())}>+</button>
```

### **Testing**

```javascript
// Jest + React Testing Library
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('button increments count', async () => {
  render(<Counter />);
  const button = screen.getByRole('button', { name: /increment/i });

  await userEvent.click(button);
  expect(button).toHaveTextContent('Count: 1');
});
```

---

## Backend Development

### **Node.js + Express**

```javascript
const express = require('express');
const app = express();

// Middleware
app.use(express.json());
app.use(cors());

// Routes
app.get('/api/users/:id', async (req, res) => {
  try {
    const user = await User.findById(req.params.id);
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/users', async (req, res) => {
  const user = new User(req.body);
  await user.save();
  res.status(201).json(user);
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(3000, () => console.log('Server running'));
```

### **Database Integration**

**SQL (PostgreSQL):**
```javascript
const { Pool } = require('pg');
const pool = new Pool({
  user: 'username',
  password: 'password',
  host: 'localhost',
  port: 5432,
  database: 'mydb'
});

// Query
const result = await pool.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);
```

**NoSQL (MongoDB):**
```javascript
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: String,
  email: { type: String, unique: true },
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);
const user = await User.findById(id);
```

### **RESTful API Design**

**HTTP Method Best Practices:**

```
GET    /api/users          - List all users
GET    /api/users/:id      - Get single user
POST   /api/users          - Create user
PUT    /api/users/:id      - Update user (full)
PATCH  /api/users/:id      - Update user (partial)
DELETE /api/users/:id      - Delete user
```

**Status Codes:**
```
200 OK                 - Successful GET/PUT/PATCH
201 Created            - Successful POST
204 No Content         - DELETE, no response body
400 Bad Request        - Validation failed
401 Unauthorized       - Authentication required
403 Forbidden          - Authorization failed
404 Not Found          - Resource doesn't exist
500 Internal Error     - Server error
```

### **Authentication & Authorization**

**JWT (JSON Web Tokens):**
```javascript
const jwt = require('jsonwebtoken');

// Create token
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: '24h' }
);

// Verify middleware
const verifyToken = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token' });

  jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
    if (err) return res.status(401).json({ error: 'Invalid token' });
    req.userId = decoded.userId;
    next();
  });
};
```

---

## Full Stack Integration

### **Next.js Example (React + Backend)**

```javascript
// pages/api/users/[id].js - API Route
export default async function handler(req, res) {
  if (req.method === 'GET') {
    const user = await getUser(req.query.id);
    res.json(user);
  } else if (req.method === 'PUT') {
    const updated = await updateUser(req.query.id, req.body);
    res.json(updated);
  }
}

// pages/users/[id].js - Page with SSR/SSG
export default function UserPage({ user }) {
  return <h1>{user.name}</h1>;
}

// Server-side props (SSR)
export async function getServerSideProps(context) {
  const user = await getUser(context.params.id);
  return { props: { user } };
}
```

### **Performance Optimization**

**Frontend:**
```
- Code splitting (Webpack/Vite)
- Image optimization (next/image, WebP)
- CSS minification and autoprefixing
- Tree shaking (remove unused code)
- Lazy loading components
- Service Workers (offline support)
```

**Backend:**
```
- Database indexing
- Query optimization
- Caching (Redis)
- API response compression (gzip)
- Rate limiting
- Load balancing
```

---

## Modern Tech Stacks

### **Recommended Stacks**

**Full Stack (Start Here):**
```
Frontend:  React / Vue / Next.js
Backend:   Node.js + Express / Fastify
Database:  PostgreSQL
Hosting:   Vercel / Netlify (frontend)
           Heroku / Railway (backend)
```

**Enterprise:**
```
Frontend:  Angular / React
Backend:   Java Spring Boot / C# ASP.NET
Database:  PostgreSQL / Oracle
DevOps:    Docker, Kubernetes
```

**Startup Friendly:**
```
Frontend:  Next.js (full-stack)
Backend:   Next.js API Routes + Serverless
Database:  Firebase / Supabase
Hosting:   Vercel (all-in-one)
```

---

## Learning Checklist

- [ ] Understand HTML semantic elements
- [ ] Master CSS layouts (Flexbox, Grid)
- [ ] Know JavaScript ES6+ features
- [ ] Built 2-3 frontend projects
- [ ] Can manipulate DOM with vanilla JS
- [ ] Know async/await and Promises
- [ ] Learning or know a framework (React/Vue)
- [ ] Understand state management
- [ ] Built API with Node/Express
- [ ] Know SQL/NoSQL basics
- [ ] Can authenticate users (JWT)
- [ ] Deployed a full-stack app
- [ ] Ready for junior developer role!

---

**Source**: https://roadmap.sh/frontend, https://roadmap.sh/backend, https://roadmap.sh/full-stack
