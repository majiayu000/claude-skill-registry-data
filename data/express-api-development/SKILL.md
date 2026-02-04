---
name: express-api-development
description: Master Express.js API development with middleware, routing, validation, authentication, and production best practices. Build scalable RESTful APIs with Express.
---

# Express.js API Development

Build production-ready RESTful APIs with Express.js, including middleware, authentication, validation, error handling, and performance optimization.

## When to Use This Skill

- Building RESTful APIs
- Creating Express middleware
- Implementing authentication
- API validation and error handling
- Performance optimization
- Production deployment

## Core Patterns

### 1. Basic Express Server

```typescript
import express, { Request, Response, NextFunction } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors());
app.use(compression());

// Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Error handling
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
```

### 2. Router Pattern

```typescript
// routes/users.ts
import { Router } from 'express';
import { UserController } from '../controllers/user.controller';
import { validateUser } from '../middleware/validation';
import { authenticate } from '../middleware/auth';

const router = Router();
const controller = new UserController();

router.get('/', authenticate, controller.getAll);
router.get('/:id', authenticate, controller.getById);
router.post('/', authenticate, validateUser, controller.create);
router.put('/:id', authenticate, validateUser, controller.update);
router.delete('/:id', authenticate, controller.delete);

export default router;
```

### 3. Controller Pattern

```typescript
// controllers/user.controller.ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/user.service';

export class UserController {
  private service = new UserService();

  getAll = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const users = await this.service.findAll();
      res.json({ data: users });
    } catch (error) {
      next(error);
    }
  };

  getById = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await this.service.findById(req.params.id);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  };

  create = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await this.service.create(req.body);
      res.status(201).json({ data: user });
    } catch (error) {
      next(error);
    }
  };
}
```

### 4. Validation Middleware

```typescript
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  age: z.number().min(18).max(120).optional(),
});

export const validateUser = (req: Request, res: Response, next: NextFunction) => {
  try {
    userSchema.parse(req.body);
    next();
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ errors: error.errors });
    } else {
      next(error);
    }
  }
};
```

### 5. Authentication Middleware

```typescript
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

interface AuthRequest extends Request {
  user?: { id: string; email: string };
}

export const authenticate = (req: AuthRequest, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as { id: string; email: string };
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

## Best Practices

1. Use TypeScript for type safety
2. Implement proper error handling
3. Use middleware for cross-cutting concerns
4. Validate all input data
5. Use environment variables for configuration
6. Implement rate limiting
7. Add request logging
8. Use compression for responses
9. Implement CORS properly
10. Add security headers with Helmet

## Resources

- https://expressjs.com/
- https://github.com/goldbergyoni/nodebestpractices
